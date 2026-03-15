import requests
from config import JINA_API_KEY, JINA_MODEL, EMBEDDING_DIMENSION

def get_embeddings(texts: list[str]) -> list[list[float]]:
    url = "https://api.jina.ai/v1/embeddings"
    
    headers = {
        "Authorization": f"Bearer {JINA_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": JINA_MODEL,
        "task": "retrieval.passage",
        "dimensions": EMBEDDING_DIMENSION,
        "input": texts
    }
    
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    
    data = response.json()
    return [item["embedding"] for item in data["data"]]


def get_query_embedding(query: str) -> list[float]:
    url = "https://api.jina.ai/v1/embeddings"
    
    headers = {
        "Authorization": f"Bearer {JINA_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": JINA_MODEL,
        "task": "retrieval.query",
        "dimensions": EMBEDDING_DIMENSION,
        "input": [query]
    }
    
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    
    data = response.json()
    return data["data"][0]["embedding"]