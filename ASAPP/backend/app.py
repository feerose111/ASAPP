import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint
from fastapi import FastAPI
from ASAPP.backend.db.schema import Project, Query
from ASAPP.backend.agent.model import Planner
from ASAPP.backend.agent.chat_bot import ContextChatbot
from contextlib import asynccontextmanager
from ASAPP.backend.utils.config_loader import PLAN_MODEL
from ASAPP.backend.db.chroma_db_connect import DbConnector
from typing import Optional
from fastapi import HTTPException
from ASAPP.backend.utils.logger import LoggerManager, ConsoleLogger, JSONFileLogger

load_dotenv()
model_id = PLAN_MODEL
hf_token = os.getenv("HF_TOKEN")

logger = LoggerManager(use_console=True)
logger.attach(ConsoleLogger())
logger.attach(JSONFileLogger())


llm = HuggingFaceEndpoint(
    repo_id= PLAN_MODEL,
    task="conversational",
    huggingfacehub_api_token=hf_token,
    temperature= 0.7,
    max_new_tokens= 512
)

#global initialization
chroma: Optional[DbConnector] =  None

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.log("INFO", "Server Started", {"message": "FastAPI ASAPP started."})
    yield
    logger.log("INFO", "Server Stopped", {"message": "FastAPI ASAPP Stopped."})

app = FastAPI(lifespan=lifespan)

#Create project using provided parameters
@app.post("/create_project")
async def create_plan(project : Project):
    global chroma
    try:
        logger.log("INFO", "Project Started", {"message": f"Project Started: project.project_name"})
        planner = Planner(llm=llm)
        result = planner.main(project.model_dump())

        chroma = DbConnector()
        chroma.add_context(result)
        logger.log("INFO", "Project Created", {"message": f"Project Created Successfully."})

        return {"project_plan": result}
    except Exception as e:
        import traceback
        full_error = traceback.format_exc()
        logger.log("ERROR", "Project Creation Failed.", {"error": str(e),"trace": full_error})

#Used for Chatting with chatbot that take user query as well as context from previous chats
@app.post("/chat")
async def chat_bot(query: Query):
    """Chat with context-aware assistant using ChromaDB"""
    global chroma, llm

    if chroma is None:
        logger.log("WARNING", "Chat Attempt Without Project", {"query": query.message })
        raise HTTPException(
            status_code=400,
            detail="Chat not initialized. Please create a project first."
        )

    # Only runs if chroma exists
    try:
        logger.log("INFO", "Chat Request", {"query": query.message})
        bot = ContextChatbot(project_plan="", llm=llm, chroma=chroma)
        response = bot.get_response(query.message)
        logger.log("INFO", "Chat Response", {"response_snipit": response[:80]})
        return {"reply": response}

    except Exception as e:
        import traceback
        full_error = traceback.format_exc()
        logger.log("ERROR", "Chat Error", {"error": str(e),"trace": full_error})
        raise HTTPException(status_code=500, detail=str(e))


