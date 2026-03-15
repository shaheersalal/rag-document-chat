from openai import OpenAI
from embeddings import get_query_embedding
from vector_store import search_similar
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def build_context(results: list[dict]) -> str:
    context = ""
    for i, result in enumerate(results):
        context += f"[{i+1}] Source: {result['source']}\n"
        context += f"{result['text']}\n\n"
    return context.strip()


def chat(query: str) -> dict:
    query_embedding = get_query_embedding(query)
    results = search_similar(query_embedding, top_k=5)

    if not results:
        return {
            "answer": "No relevant documents found. Please upload documents first.",
            "sources": []
        }

    context = build_context(results)

    system_prompt = """You are a helpful assistant that answers questions based strictly on the provided context.
If the answer is not in the context, say "I cannot find this information in the uploaded documents."
Always be precise and cite which source your answer comes from."""

    user_prompt = f"""Context:
{context}

Question: {query}

Answer based only on the context above:"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.1
    )

    answer = response.choices[0].message.content

    sources = list(set([r["source"] for r in results]))

    return {
        "answer": answer,
        "sources": sources,
        "context_used": len(results)
    }