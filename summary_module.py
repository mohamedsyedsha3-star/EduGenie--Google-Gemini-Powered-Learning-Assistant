from gemini_client import generate_text


def summarize_text(text: str) -> str:
    """
    Summarize educational content while retaining important information.
    """

    if not text.strip():
        raise ValueError(
            "Please provide text to summarize."
        )

    prompt = f"""
You are EduGenie, an educational summarization assistant.

Summarize the following educational passage.

Requirements:
- Preserve the important facts.
- Remove repetition.
- Use simple language.
- Keep important names, dates, definitions and concepts.
- Organize the result into short paragraphs or bullet points when useful.
- Do not add information that is not present in the passage.

Passage:
{text}
"""

    return generate_text(
        prompt,
        temperature=0.25,
        max_output_tokens=1500,
    )
