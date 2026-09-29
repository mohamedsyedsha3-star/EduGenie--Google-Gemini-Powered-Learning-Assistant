from functools import lru_cache

from config import settings


@lru_cache(maxsize=1)
def load_local_model():
    """
    Load LaMini-Flan-T5 lazily.

    The model is loaded only when an explanation is requested.
    """

    from transformers import (
        AutoTokenizer,
        AutoModelForSeq2SeqLM,
    )

    tokenizer = AutoTokenizer.from_pretrained(
        settings.LOCAL_EXPLANATION_MODEL
    )

    model = AutoModelForSeq2SeqLM.from_pretrained(
        settings.LOCAL_EXPLANATION_MODEL
    )

    return tokenizer, model


def explain_with_local_model(topic: str) -> str:
    """
    Explain a concept using the local LaMini-Flan-T5 model.
    """

    import torch

    tokenizer, model = load_local_model()

    prompt = (
        "Explain the following educational concept in simple language. "
        "Assume the learner is a beginner. "
        "Give a short definition, explanation and example.\n\n"
        f"Concept: {topic}"
    )

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512,
    )

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=180,
            num_beams=4,
            early_stopping=True,
        )

    result = tokenizer.decode(
        output[0],
        skip_special_tokens=True,
    )

    return result.strip()


def explain_with_gemini(topic: str) -> str:
    """
    Gemini fallback for explanations.
    """

    from gemini_client import generate_text

    prompt = f"""
You are EduGenie, an educational tutor.

Explain this concept to a beginner:

{topic}

Use this structure:

Definition:
...

Simple explanation:
...

Example:
...

Key point:
...

Use simple language and avoid unnecessary technical terminology.
"""

    return generate_text(
        prompt,
        temperature=0.3,
        max_output_tokens=1000,
    )


def explain_topic(topic: str) -> str:
    """
    Explain a concept using the configured local model.

    If local inference fails, Gemini is used as a fallback.
    """

    if not topic.strip():
        raise ValueError(
            "Please enter a topic to explain."
        )

    if settings.USE_LOCAL_EXPLANATION:

        try:
            return explain_with_local_model(
                topic
            )

        except Exception as local_error:

            print(
                "Local explanation model failed. "
                "Falling back to Gemini."
            )

            try:
                return explain_with_gemini(
                    topic
                )

            except Exception as gemini_error:
                raise RuntimeError(
                    "Both local explanation and Gemini "
                    "explanation failed.\n"
                    f"Local error: {local_error}\n"
                    f"Gemini error: {gemini_error}"
                ) from gemini_error

    return explain_with_gemini(topic)

