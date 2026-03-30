from langchain_huggingface import HuggingFaceEndpoint
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.project_schema import Project, Query
from agent.model import Planner
from agent.chat_bot import ContextChatbot
from contextlib import asynccontextmanager
from utils.config import settings
from db.chroma_db_connect import DbConnector
from typing import Optional
from fastapi import HTTPException
from utils.logger import LoggerManager

logger = LoggerManager(use_console=True)
print(settings.PLAN_MODEL)
llm = HuggingFaceEndpoint(
    repo_id= settings.PLAN_MODEL,
    task="conversational",
    huggingfacehub_api_token=settings.HF_TOKEN,
    temperature= 0.7,
   max_new_tokens = 512
)

print(f"✓ LLM initialized with max_new_tokens=256")
logger.log("INFO", "LLM Init", {"max_new_tokens": 256, "model": settings.PLAN_MODEL})

#global initialization
chroma: Optional[DbConnector] =  None
fallback_chroma: DbConnector = DbConnector()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.log("INFO", "Server Started", {"message": "FastAPI ASAPP started."})
    yield
    logger.log("INFO", "Server Stopped", {"message": "FastAPI ASAPP Stopped."})

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for dev (later restrict)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Create project using provided parameters
@app.post("/create_project")
async def create_plan(project : Project):
    global chroma
    try:
        logger.log("INFO", "Project Started", {"message": f"Project Started: project.project_name"})
        planner = Planner(llm=llm)
        result = planner.main(project.model_dump())
        print(result)

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
    """Chat with context-aware assistant using ChromaDB (or without context if project not created)"""
    global chroma, fallback_chroma, llm

    try:
        logger.log("INFO", "Chat Request", {"query": query.message})

        active_chroma = chroma or fallback_chroma
        has_project = chroma is not None

        # Chat with context if project exists, without context otherwise
        bot = ContextChatbot(
            project_plan="",
            llm=llm,
            chroma=active_chroma,
            has_project= has_project
        )
        response = bot.get_response(query.message)

        if response:
            logger.log("INFO", "Chat Response", {"response_snipit": response[:80]})
        else:
            logger.log("WARNING", "Chat Response", {"response": "Empty response from bot"})

        return {
            "reply": response,
            "has_context": has_project  # Tell frontend if using context
        }

    except Exception as e:
        import traceback
        full_error = traceback.format_exc()
        logger.log("ERROR", "Chat Error", {"error": str(e), "trace": full_error})
        raise HTTPException(status_code=500, detail=str(e))


