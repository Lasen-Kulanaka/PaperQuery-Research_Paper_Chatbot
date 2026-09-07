import os
from dotenv import load_dotenv

load_dotenv()

#API keys load
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

#Models
GEMINI_MODEL = "gemini-flash-latest"
GROQ_MODEL = "openai/gpt-oss-120b"
EMBEDDING_MODEL =  "sentence-transformers/all-MiniLM-L6-v2"

#Chunking
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150

#Retrieval
TOP_K = 5

#DBs
UPLOAD_DIR = "data/uploads"
CHROMA_DIR = "data/chroma_db"