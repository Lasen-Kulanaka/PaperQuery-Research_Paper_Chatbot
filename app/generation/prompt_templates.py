def build_rag_prompt(question:str, context_chunks:list) -> str:
    """
    Builds a prompt combining retrieved context chunks with the user's question.
    """
    context_text = "\n\n".join(
        [f"[Source: page {chunk.metadata.get('page', 'unknown')}]\n{chunk.page_content}"
         for chunk in context_chunks]
    )

    prompt = f"""You are a research assistant answering questions about a research paper.
Use ONLY the context below to answer the question. If the answer isn't in the context, say you don't know.

Context: {context_text}

Question: {question}

Answer: 
"""
    return prompt