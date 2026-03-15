from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import shutil

from config import COLLECTION_NAME
from vector_store import create_collection
from ingestion import ingest_document
from chat import chat

app = FastAPI(
    title="RAG Document Chat API",
    description="Upload documents and chat with them using AI",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.on_event("startup")
async def startup():
    create_collection()
    print(f"RAG API started. Collection: {COLLECTION_NAME}")


@app.get("/")
def root():
    return {
        "status": "running",
        "endpoints": {
            "upload": "POST /upload",
            "chat": "POST /chat",
            "health": "GET /health"
        }
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files supported")

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        chunks_count = ingest_document(file_path, file.filename)
        return {
            "message": f"Successfully ingested '{file.filename}'",
            "chunks_created": chunks_count,
            "filename": file.filename
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class ChatRequest(BaseModel):
    query: str


@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    try:
        result = chat(request.query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))