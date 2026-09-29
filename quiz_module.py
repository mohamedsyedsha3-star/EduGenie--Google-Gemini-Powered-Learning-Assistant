import json
import re
from typing import Any

from gemini_client import generate_text


def clean_json_block(text: str) -> str:
    """
    Remove Markdown code fences from an LLM JSON response.
    """

    text = text.strip()

    text = re.sub(
        r"^```(?:json)?\s*",
        "",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(
        r"\s*```$",
        "",
        text,
    )

    return text.strip()


def validate_quiz(data: Any) -> list[dict]:
    """
    Validate the expected quiz structure.
    """

    if not isinstance(data, list):
        raise ValueError(
            "Quiz response must be a JSON list."
        )

    if len(data) != 3:
        raise ValueError(
            "Quiz must contain exactly three questions."
        )

    validated = []

    for index, item in enumerate(data, start=1):

        if not isinstance(item, dict):
            raise ValueError(
                f"Question {index} is not an object."
            )

        question = item.get("question")
        options = item.get("options")
        answer = item.get("answer")

        if not isinstance(question, str):
            raise ValueError(
                f"Question {index} has an invalid question."
            )

        if not isinstance(options, list) or len(options) != 4:
            raise ValueError(
                f"Question {index} must have exactly four options."
            )

        if not all(
            isinstance(option, str)
            for option in options
        ):
            raise ValueError(
                f"Question {index} contains invalid options."
            )

        if not isinstance(answer, str):
            raise ValueError(
                f"Question {index} has an invalid answer."
            )

        if answer not in options:
            raise ValueError(
                f"Question {index}'s answer must match one of its options."
            )

        validated.append(
            {
                "question": question.strip(),
                "options": [
                    option.strip()
                    for option in options
                ],
                "answer": answer.strip(),
            }
        )

    return validated


def generate_quiz(text: str) -> list[dict]:
    """
    Generate three MCQs from the supplied educational content.
    """

    if not text.strip():
        raise ValueError(
            "Please provide a topic or passage for the quiz."
        )

    prompt = f"""
You are EduGenie, an educational quiz generator.

Create exactly THREE multiple-choice questions based ONLY
on the supplied educational content.

Each question must have:
- question
- options
- answer

Rules:
- Exactly 3 questions.
- Exactly 4 options per question.
- Exactly one correct answer.
- The "answer" value must exactly match one of the four options.
- Questions should test understanding rather than random trivia.
- Distractors should be plausible.
- Do not use Markdown.
- Return ONLY valid JSON.
- Do not put the JSON inside ```json fences.

Required JSON format:

[
  {{
    "question": "Question text",
    "options": [
      "Option A",
      "Option B",
      "Option C",
      "Option D"
    ],
    "answer": "Option A"
  }}
]

Educational content:
{text}
"""

    response = generate_text(
        prompt,
        temperature=0.3,
        max_output_tokens=1800,
    )

    cleaned = clean_json_block(response)

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise ValueError(
            "Gemini returned invalid quiz JSON. "
            f"Raw response: {response}"
        ) from exc

    return validate_quiz(data)
