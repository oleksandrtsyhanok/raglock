from data_indexing.reader import Reader
from data_indexing.data_handler import DataHandler
from generation.generator import Generator
from vector_db import QdrantStorage
from fastapi import APIRouter, Request
from pydantic import BaseModel



router = APIRouter()

class IndexRequest(BaseModel):
    path: str

@router.post("/index")
async def rebuild_db(request: Request, paylaoad: IndexRequest):
    reader = Reader(paylaoad.path)
    db_qdrant: QdrantStorage = request.app.state.db_qdrant
    data_handler: DataHandler = request.app.state.data_handler

    data = reader.read_files()
    chunked_data = data_handler.chunk_data(data)
    ids, vectors, payloads = data_handler.create_embeddings(chunked_data)
    db_qdrant.upsert(ids, vectors, payloads)
    return {"status": "Indexing complete", "chunks_indexed": len(ids)}



class ChatRequest(BaseModel):
    query: str

@router.post("/chat")
async def chat_endpoint(request: Request, payload: ChatRequest):
    db_qdrant: QdrantStorage = request.app.state.db_qdrant
    generator: Generator = request.app.state.generator
    data_handler: DataHandler = request.app.state.data_handler

    query = payload.query
    query_vector = data_handler.create_query_embedding(query)
    context = db_qdrant.search(query_vector)

    response = await generator.generate_answer(query=query, contexts=context["contexts"], sources=context["sources"])

    return {"answer": response}