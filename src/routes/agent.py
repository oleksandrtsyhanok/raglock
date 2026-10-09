from data_indexing.data_handler import DataHandler
from generation.generator import Generator
from vector_db import QdrantStorage

from agents.agent_engine import Agent
from config.loader import get_config
from config.settings import Settings

from fastapi import APIRouter, Request
from pydantic import BaseModel

agent_router = APIRouter()

class ChatRequest(BaseModel):
    query: str

@agent_router.post("/agent")
async def chat_endpoint(request: Request, payload: ChatRequest):
    agent: Agent = request.app.state.agent

    try:
        response = await agent.agent_loop(payload.query)
    except Exception as e:
        response = str(e)
    return {"answer": response}