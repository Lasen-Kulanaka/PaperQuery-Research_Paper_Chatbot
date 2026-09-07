# fallback logic: try Gemini first, and if it fails for any reason, catch the error and try Groq instead.

from app.generation.gemini_client import generate_with_gemini
from app.generation.groq_client import generate_with_groq

def generate_response(prompt:str) -> dict:
    """
    Tries Gemini first. If it fails, falls back to Groq.
    Returns the generated text along with which provider served it.
    """

    try:
        text = generate_with_gemini(prompt)
        return {"text":text, "provider":"gemini"}
    except Exception as e:
        print(f"Gemini failed:{e}. falling back to Groq.")
        text = generate_with_groq(prompt)
        return {"text":text, "provider":"groq"}