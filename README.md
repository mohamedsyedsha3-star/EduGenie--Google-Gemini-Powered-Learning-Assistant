# EduGenie

EduGenie is an AI-powered educational assistant built with:

- FastAPI
- Google Gemini API
- Python
- Jinja2
- HTML
- CSS
- JavaScript
- Hugging Face Transformers
- LaMini-Flan-T5

## Features

EduGenie provides:

1. Question answering
2. Concept explanation
3. MCQ quiz generation
4. Text summarization
5. Personalized learning paths

## Architecture

Frontend:

HTML + CSS + JavaScript

        |
        v

FastAPI Backend

        |
        +----------------+
        |                |
        v                v
   Gemini API       Local AI Model
                    LaMini-Flan-T5

## API Endpoints

GET /

GET /health

POST /qa

POST /explain

POST /quiz

POST /summarize

POST /learn/recommendations

## Installation

Create a virtual environment:

Windows:

python -m venv .venv

.venv\Scripts\activate

macOS/Linux:

python3 -m venv .venv

source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt

## Environment Configuration

Copy:

.env.example

to:

.env

Add your Gemini API key:

GEMINI_API_KEY=YOUR_KEY

## Run

python -m uvicorn main:app --reload

Open:

http://127.0.0.1:8000

## API Documentation

FastAPI automatically provides:

http://127.0.0.1:8000/docs

Alternative documentation:

http://127.0.0.1:8000/redoc

## Health Check

Open:

http://127.0.0.1:8000/health

## Testing

Question:

Which is the largest ocean?

Explanation:

Photosynthesis

Quiz:

The Pythagoras theorem

Summary:

Paste a long educational paragraph.

Learning Path:

SQL

## Local AI Model

The explanation module can use:

MBZUAI/LaMini-Flan-T5-783M

The model is downloaded automatically the first time it is required.

If local inference fails, EduGenie falls back to Gemini.

To disable the local model:

USE_LOCAL_EXPLANATION=false

## Security

Never commit:

.env

to Git.

Never expose the Gemini API key in:

- HTML
- JavaScript
- GitHub
- screenshots
- public repositories

The API key belongs on the backend.

## Troubleshooting

If Gemini requests fail:

1. Check GEMINI_API_KEY.
2. Check your internet connection.
3. Check that the configured Gemini model is available to your API account.
4. Check the terminal error.

If the local model fails:

Set:

USE_LOCAL_EXPLANATION=false

This makes explanations use Gemini.

## Development

Start with:

python -m uvicorn main:app --reload

The --reload option automatically restarts the server when Python files change.
