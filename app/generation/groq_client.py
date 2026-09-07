from langchain_groq import ChatGroq
from app.core.config import GROQ_API_KEY, GROQ_MODEL

llm = ChatGroq(api_key = GROQ_API_KEY, model=GROQ_MODEL)\

def generate_with_groq(prompt:str) -> str:
    """
    Sends a prompt to Groq and returns the generated text.
    Raises an exception if the call fails (handled by the router later).
    """

    response = llm.invoke(prompt)
    return response.content