#wraps the Gemini API into one simple function: give it a prompt, get text back.

from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import GEMINI_API_KEY, GEMINI_MODEL

llm = ChatGoogleGenerativeAI(google_api_key=GEMINI_API_KEY, model=GEMINI_MODEL)

def generate_with_gemini(prompt:str) -> str:
    """
    Sends a prompt to Gemini and returns the generated text.
    Raises an exception if the call fails (handled by the router later).
    """
    response = llm.invoke(prompt)
    content = response.content

    if isinstance(content, list):
        content = " ".join(
            block.get("text", "") if isinstance(block, dict) else str(block)
            for block in content
        )

    return content