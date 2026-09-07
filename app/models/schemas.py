# simple Pydantic models defining what your API accepts as input and returns as output

from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    """Request body for POST /chat"""
    question : str
    paper: Optional[str] = None

class Source(BaseModel):
    """A single source chunk used to answer a question"""
    page:int
    content_preview:str

class ChatResponse(BaseModel):
    """Response body for POST /chat"""
    answer:str
    provider:str
    sources:List[Source]

class UploadResponse(BaseModel):
    """Response body for POST /upload"""
    filename:str
    chunks_created:int
    message:str

class PapersResponse(BaseModel):
    """Response body for GET /papers"""
    papers: List[str]