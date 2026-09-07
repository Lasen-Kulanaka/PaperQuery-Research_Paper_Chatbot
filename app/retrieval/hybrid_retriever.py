# combines semantic search and keyword search results into one ranked list using Reciprocal Rank Fusion

from app.retrieval.vector_store import semantic_search
from app.retrieval.keyword_store import keyword_search

RRF_K = 60

def hybrid_search(query:str, k:int, paper_filter:str=None):
    """
    Combines semantic search and keyword search results using
    Reciprocal Rank Fusion (RRF), and returns the top-k merged chunks.
    """
    semantic_results = semantic_search(query, k=10, paper_filter=paper_filter)
    keyword_results = keyword_search(query, k=10, paper_filter=paper_filter)

    scores = {}
    chunk_lookup = {}

    for rank, doc in enumerate(semantic_results):
        key = doc.page_content
        scores[key] = scores.get(key,0) + 1 / (rank+RRF_K)
        chunk_lookup[key]=doc

    for rank, doc in enumerate(keyword_results):
        key = doc.page_content
        scores[key] = scores.get(key,0)+1 / (rank+RRF_K)
        chunk_lookup[key]=doc

    ranked_keys = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)

    top_chunks = [chunk_lookup[key] for key in ranked_keys[:5]]
    return top_chunks
