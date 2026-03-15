# RAG Document Chat API

  

A production-ready Retrieval-Augmented Generation (RAG) API that lets you upload PDF documents and chat with them using AI. Built with FastAPI, Jina AI embeddings, Qdrant vector database, and GPT-4o-mini.

  

## Architecture

```

PDF Upload → Text Extraction → Chunking → Jina Embeddings → Qdrant Storage

Query → Jina Embeddings → Vector Search → Context Building → GPT-4o-mini → Answer

```

  

## Tech Stack

  

- **FastAPI** — REST API backend

- **PyMuPDF** — PDF text extraction

- **Jina AI** — `jina-embeddings-v3` (1024D) for passage and query embeddings

- **Qdrant** — Vector database for similarity search

- **OpenAI** — GPT-4o-mini for answer generation

- **Docker** — Qdrant runs in a container

  

## Endpoints

  

| Method | Endpoint | Description |

|--------|----------|-------------|

| GET | `/` | API status and available endpoints |

| GET | `/health` | Health check |

| POST | `/upload` | Upload a PDF document |

| POST | `/chat` | Ask a question about uploaded documents |

  

## Quick Start

  

**1. Clone the repo**

```bash

git clone [https://github.com/shaheersalal/rag-document-chat.git](https://github.com/shaheersalal/rag-document-chat.git "https://github.com/shaheersalal/rag-document-chat.git")

cd rag-document-chat

```

  

**2. Install dependencies**

```bash

pip install -r requirements.txt

```

  

**3. Start Qdrant**

```bash

docker run -p 6333:6333 qdrant/qdrant

```

  

**4. Configure environment**

```bash

cp .env.example .env

# Add your API keys to .env

```

  

**5. Run the API**

```bash

uvicorn main:app --reload

```

  

**6. Open interactive docs**

```

[http://localhost:8000/docs](http://localhost:8000/docs "http://localhost:8000/docs")

```

  

## Example Usage

  

**Upload a document:**

```bash

curl -X POST [http://localhost:8000/upload](http://localhost:8000/upload "http://localhost:8000/upload") 

  -F "file=@document.pdf"

```

  

**Chat with it:**

```bash

curl -X POST [http://localhost:8000/chat](http://localhost:8000/chat "http://localhost:8000/chat") 

  -H "Content-Type: application/json" 

  -d '{"query": "What is the main topic of this document?"}'

```

  

**Response:**

```json

{

  "answer": "Based on the uploaded document... [Source: 1]",

  "sources": ["document.pdf"],

  "context_used": 5

}

```

  

## Configuration

  

| Variable | Description | Default |

|----------|-------------|---------|

| `OPENAI_API_KEY` | OpenAI API key | required |

| `JINA_API_KEY` | Jina AI API key | required |

| `QDRANT_URL` | Qdrant instance URL | `http://localhost:6333` |

| `COLLECTION_NAME` | Qdrant collection name | `documents` |

| `CHUNK_SIZE` | Characters per chunk | `500` |

| `CHUNK_OVERLAP` | Overlap between chunks | `50` |