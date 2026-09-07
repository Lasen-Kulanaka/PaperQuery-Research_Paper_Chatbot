#builds a BM25 keyword index over the same chunks, so we can do exact keyword matching alongside semantic search.

from rank_bm25 import BM25Okapi

bm25_index = None
bm25_chunks = []

def build_bm25_index(chunks):
    """
    Builds a BM25 index from a list of chunks.
    Call this whenever new chunks are added.
    """
    global bm25_index, bm25_chunks

    bm25_chunks = chunks
    tokenized_corpus = [doc.page_content.split() for doc in chunks]
    bm25_index = BM25Okapi(tokenized_corpus)

def keyword_search(query:str, k:int=5, paper_filter:str=None):
    """
    Returns the top-k chunks most relevant to the query using BM25 keyword matching.
    If paper_filter is given, only considers chunks from that paper.
    """
    if bm25_index is None:
        return []

    tokenized_query = query.split()
    scores = bm25_index.get_scores(tokenized_query)

    scored_chunks = list(zip(bm25_chunks, scores))

    if paper_filter:
        scored_chunks = [
            (chunk, score) for chunk, score in scored_chunks
            if chunk.metadata.get("source") == paper_filter
        ]

    scored_chunks.sort(key=lambda x: x[1], reverse=True)
    top_chunks = [chunk for chunk, score in scored_chunks[:k]]
    return top_chunks