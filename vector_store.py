from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from config import QDRANT_URL, COLLECTION_NAME, EMBEDDING_DIMENSION
import uuid

client = QdrantClient(url=QDRANT_URL)


def create_collection():
    existing = [c.name for c in client.get_collections().collections]
    
    if COLLECTION_NAME not in existing:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=EMBEDDING_DIMENSION,
                distance=Distance.COSINE
            )
        )
        print(f"Collection '{COLLECTION_NAME}' created")
    else:
        print(f"Collection '{COLLECTION_NAME}' already exists")


def store_chunks(chunks: list[str], embeddings: list[list[float]], filename: str):
    points = [
        PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={
                "text": chunk,
                "source": filename
            }
        )
        for chunk, embedding in zip(chunks, embeddings)
    ]
    
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )
    print(f"Stored {len(points)} chunks from '{filename}'")


def search_similar(query_embedding: list[float], top_k: int = 5) -> list[dict]:
    results = client.query_points(
    collection_name=COLLECTION_NAME,
    query=query_embedding,
    limit=top_k
    ).points
    
    return [
        {
            "text": r.payload["text"],
            "source": r.payload["source"],
            "score": r.score
        }
        for r in results
    ]