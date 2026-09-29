from gemini_client import generate_text


def get_learning_recommendations(
    topic: str,
    learner_level: str = "beginner",
) -> str:
    """
    Generate a structured beginner-to-advanced learning path.
    """

    if not topic.strip():
        raise ValueError(
            "Please provide a topic for the learning path."
        )

    prompt = f"""
You are EduGenie, a personalized educational mentor.

Create a structured learning path for:

Topic:
{topic}

Learner level:
{learner_level}

The learning plan must contain:

1. Short introduction
2. Prerequisites
3. Beginner level
4. Intermediate level
5. Advanced level
6. Suggested timeline
7. Practice activities
8. Project ideas
9. Revision strategy
10. Recommended resource types

For each level:
- Explain what should be learned.
- List important subtopics.
- Give practical exercises.
- Explain what the learner should be able to do after completing it.

For resources:
- Suggest useful types of resources such as documentation,
  books, tutorials, courses and videos.
- Do not fabricate exact URLs.
- If mentioning a named resource, only mention well-known resources
  when you are reasonably confident that they exist.

Use clear headings and student-friendly language.
"""

    return generate_text(
        prompt,
        temperature=0.5,
        max_output_tokens=2500,
    )
