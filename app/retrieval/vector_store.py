#embeds chunks and stores/retrieves them from Chroma

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from app.core.config import EMBEDDING_MODEL, CHROMA_DIR

embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

def get_vector_store():
    """
    Loads (or creates) the persistent Chroma vector store.
    """
    vector_store = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings,
    )
    return vector_store

def add_chunks_to_store(chunks):
    """
    Embeds and stores a list of chunks in Chroma.
    """
    vector_store = get_vector_store()
    vector_store.add_documents(chunks)

def semantic_search(query: str, k:int, paper_filter:str=None):
    """
    Returns the top-k most similar chunks to the query.
    If paper_filter is given, only searches within that paper.
    """
    vector_store = get_vector_store()
    filter_dict = {"source": paper_filter} if paper_filter else None
    results = vector_store.similarity_search(query, k=5, filter=filter_dict)
    return results