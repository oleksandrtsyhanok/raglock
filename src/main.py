from vector_db import QdrantStorage
from routes.index import router
from data_indexing.data_handler import DataHandler
from generation.generator import Generator

from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db_qdrant = QdrantStorage()
    app.state.data_handler = DataHandler()
    app.state.generator = Generator()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(router, prefix='/api')