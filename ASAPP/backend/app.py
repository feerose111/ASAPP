import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint
from fastapi import FastAPI
from ASAPP.backend.utils.schema import Project
from ASAPP.backend.agent.model import Planner
from contextlib import asynccontextmanager

load_dotenv()
model_id = "meta-llama/Meta-Llama-3-8B-Instruct"
hf_token = os.getenv("HF_TOKEN")

llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Meta-Llama-3-8B-Instruct",
    task="conversational",
    huggingfacehub_api_token=hf_token,
    temperature= 0.7,
    max_new_tokens= 512,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting ASAPP...")
    yield
    print("Shutting down ASAPP...")

app = FastAPI(lifespan=lifespan)

@app.post("/create_project")
async def create_plan(project : Project):
    planner = Planner(llm=llm)
    result = planner.main(project.model_dump())
    return {"project_plan": result}

@app.get("/plan")
async def get_plan():
    pass