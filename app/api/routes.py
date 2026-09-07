# wires everything together into actual HTTP endpoints.

from fastapi import APIRouter, UploadFile, File
import os

from app.core.config import UPLOAD_DIR
from app.ingestion.loader import load_pdf
from app.ingestion.chunker import chunk_documents
from app.retrieval.vector_store import add_chunks_to_store
from app.retrieval.keyword_store import build_bm25_index
from app.chains.rag_chain import ask_questions
from app.models.schemas import ChatRequest,ChatResponse,UploadResponse, PapersResponse

router = APIRouter()

all_chunks = []

@router.post("/upload", response_model=UploadResponse)
async def upload_paper(file: UploadFile = File(...)):
    """
    Uploads a PDF, extracts text, chunks it, and indexes it
    in both the vector store (Chroma) and keyword store (BM25).
    """
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path,"wb") as f:
        content = await file.read()
        f.write(content)

    docs = load_pdf(file_path)
    chunks = chunk_documents(docs)

    add_chunks_to_store(chunks)

    all_chunks.extend(chunks)
    build_bm25_index(all_chunks)

    return UploadResponse(
        filename=file.filename,
        chunks_created=len(chunks),
        message="Paper uploaded and indexed successfully."
    )

@router.get("/papers", response_model=PapersResponse)
async def list_papers():
    """
    Returns the list of unique papers uploaded so far.
    """
    sources = {chunk.metadata.get("source") for chunk in all_chunks}
    return PapersResponse(papers=sorted(s for s in sources if s))

@router.post("/chat", response_model=ChatResponse)
async def chat (request: ChatRequest):
    """
    Answers a question using the RAG pipeline over all uploaded papers.
    """
    result = ask_questions(request.question, paper_filter=request.paper)
    return ChatResponse(**result)