from gemini_client import generate_text


def answer_question(question: str) -> str:
    """
    Answer a student's academic/general knowledge question.
    """

    if not question.strip():
        raise ValueError(
            "Please enter a question."
        )

    prompt = f"""
You are EduGenie, an educational AI assistant.

Answer the student's question accurately and clearly.

Rules:
1. Give the direct answer first.
2. Explain the answer briefly.
3. Use simple language suitable for students.
4. If useful, provide a short example.
5. Do not invent facts.
6. If the question is ambiguous, clearly mention the ambiguity.
7. Do not unnecessarily make the answer long.

Student question:
{question}
"""

    return generate_text(prompt)
