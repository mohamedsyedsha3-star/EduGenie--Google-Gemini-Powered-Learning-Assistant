from typing import Any

from google import genai
from google.genai import types

from config import settings


_client = None


def get_gemini_client():
    """
    Create the Gemini client lazily.

    This prevents application startup from failing simply because
    an API key has not been configured yet.
    """
    global _client

    if _client is not None:
        return _client

    if not settings.GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured. "
            "Create a .env file and add your Gemini API key."
        )

    _client = genai.Client(
        api_key=settings.GEMINI_API_KEY
    )

    return _client


def generate_text(
    prompt: str,
    temperature: float | None = None,
    max_output_tokens: int | None = None,
) -> str:
    """
    Generate text using Gemini.
    """

    client = get_gemini_client()

    temperature = (
        settings.GEMINI_TEMPERATURE
        if temperature is None
        else temperature
    )

    max_output_tokens = (
        settings.GEMINI_MAX_OUTPUT_TOKENS
        if max_output_tokens is None
        else max_output_tokens
    )

    response = client.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_output_tokens,
        ),
    )

    text = getattr(response, "text", None)

    if not text:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return text.strip()
