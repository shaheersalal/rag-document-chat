import fitz
from config import CHUNK_SIZE, CHUNK_OVERLAP
from embeddings import get_embeddings
from vector_store import store_chunks


def extract_text(file_path: str) -> str:
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text


def chunk_text(text: str) -> list[str]:
    chunks = []
    start = 0

    while start < len(text):
        end = start + CHUNK_SIZE
        chunk = text[start:end]

        if chunk.strip():
            chunks.append(chunk.strip())

        start = end - CHUNK_OVERLAP

    return chunks


def ingest_document(file_path: str, filename: str):
    print(f"Extracting text from '{filename}'...")
    text = extract_text(file_path)

    if not text.strip():
        raise ValueError(f"No text extracted from '{filename}'")

    print(f"Chunking text...")
    chunks = chunk_text(text)
    print(f"Created {len(chunks)} chunks")

    print(f"Generating embeddings...")
    embeddings = get_embeddings(chunks)

    print(f"Storing in Qdrant...")
    store_chunks(chunks, embeddings, filename)

    print(f"Done. '{filename}' ingested successfully.")
    return len(chunks)