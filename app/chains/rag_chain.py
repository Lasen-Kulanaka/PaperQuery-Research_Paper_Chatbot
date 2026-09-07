from app.retrieval.hybrid_retriever import hybrid_search
from app.generation.prompt_templates import build_rag_prompt
from app.generation.llm_router import generate_response
from app.core.config import TOP_K

def ask_questions(question: str, paper_filter:str=None) -> dict:
    """
    Full RAG pipeline: retrieve relevant chunks, build a prompt,
    generate an answer, and return it with sources.
    """
    chunks = hybrid_search(question, k=TOP_K, paper_filter=paper_filter)

    prompt = build_rag_prompt(question, chunks)

    result = generate_response(prompt)

    sources = [
        {
            "page": chunk.metadata.get("page", "unknown"),
            "content_preview": chunk.page_content[:150]
        }
        for chunk in chunks
    ]

    return{
        "answer": result["text"],
        "provider": result["provider"],
        "sources": sources
    }