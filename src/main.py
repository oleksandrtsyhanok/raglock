from vector_db import QdrantStorage
from routes.index import router
from data_indexing.data_handler import DataHandler
from generation.generator import Generator

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db_qdrant = QdrantStorage()
    app.state.data_handler = DataHandler()
    app.state.generator = Generator()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Angular dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix='/api')