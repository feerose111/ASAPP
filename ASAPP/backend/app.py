import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint
from fastapi import FastAPI
from ASAPP.backend.utils.schema import Project, Query
from ASAPP.backend.agent.model import Planner
from ASAPP.backend.agent.chat_bot import ContextChatbot
from contextlib import asynccontextmanager
from ASAPP.backend.utils.config_loader import PLAN_MODEL
from ASAPP.backend.utils.chroma_db_connect import DbConnector
from typing import Optional

from fastapi import HTTPException


load_dotenv()
model_id = PLAN_MODEL
hf_token = os.getenv("HF_TOKEN")

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
    print("Starting ASAPP...")
    yield
    print("Shutting down ASAPP...")

app = FastAPI(lifespan=lifespan)

@app.post("/create_project")
async def create_plan(project : Project):
    global chroma
    planner = Planner(llm=llm)
    result = planner.main(project.model_dump())

    chroma = DbConnector()
    chroma.add_context(result)
    return {"project_plan": result}

@app.post("/chat")
async def chat_bot(query: Query):
    """Chat with context-aware assistant using ChromaDB"""
    global chroma, llm

    if chroma is None:
        raise HTTPException(
            status_code=400,
            detail="Chat not initialized. Please create a project first."
        )

    # Only runs if chroma exists
    try:
        bot = ContextChatbot(project_plan="", llm=llm, chroma=chroma)
        response = bot.get_response(query.message)
        return {"reply": response}

    except Exception as e:
        import traceback
        full_error = traceback.format_exc()
        print(full_error)  # Print to cons
        raise HTTPException(status_code=500, detail=str(e))


