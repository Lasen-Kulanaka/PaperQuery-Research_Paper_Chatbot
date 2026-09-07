#takes the list of page Documents from Step 2 and splits them into smaller chunks suitable for embedding

from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.core.config import CHUNK_SIZE, CHUNK_OVERLAP

def chunk_documents(documents):
    """
    Splits a list of Documents into smaller chunks.
    Keeps original metadata (source, page) attached to each chunk.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size = CHUNK_SIZE,
        chunk_overlap = CHUNK_OVERLAP,
    )

    chunks = splitter.split_documents(documents)
    return chunks