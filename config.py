from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
JINA_API_KEY = os.getenv("JINA_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "documents")
JINA_MODEL = "jina-embeddings-v3"
EMBEDDING_DIMENSION = 1024
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50