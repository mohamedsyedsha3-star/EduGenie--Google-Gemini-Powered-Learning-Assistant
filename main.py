from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from config import settings
from explanation_module import explain_topic
from learning_path import get_learning_recommendations
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text


BASE_DIR = Path(__file__).resolve().parent


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "EduGenie - Google Gemini Powered Learning Assistant"
    ),
)


app.mount(
    "/static",
    StaticFiles(
        directory=str(BASE_DIR / "static")
    ),
    name="static",
)


templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


# ============================================================
# Pydantic request models
# ============================================================

class TextRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=settings.MAX_INPUT_LENGTH,
    )


class LearningPathRequest(BaseModel):
    topic: str = Field(
        ...,
        min_length=1,
        max_length=settings.MAX_INPUT_LENGTH,
    )

    level: str = Field(
        default="beginner",
        max_length=50,
    )


# ============================================================
# Frontend
# ============================================================

@app.get(
    "/",
    response_class=HTMLResponse,
)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "app_name": settings.APP_NAME,
            "version": settings.APP_VERSION,
        },
    )


# ============================================================
# Health check
# ============================================================

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "gemini_configured": bool(
            settings.GEMINI_API_KEY
        ),
        "local_explanation_enabled": (
            settings.USE_LOCAL_EXPLANATION
        ),
    }


# ============================================================
# Q&A
# ============================================================

@app.post("/qa")
async def qa(request: TextRequest):

    try:
        result = answer_question(
            request.text
        )

        return {
            "success": True,
            "task": "qa",
            "result": result,
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


# ============================================================
# Explanation
# ============================================================

@app.post("/explain")
async def explain(request: TextRequest):

    try:
        result = explain_topic(
            request.text
        )

        return {
            "success": True,
            "task": "explain",
            "result": result,
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


# ============================================================
# Quiz
# ============================================================

@app.post("/quiz")
async def quiz(request: TextRequest):

    try:
        result = generate_quiz(
            request.text
        )

        return {
            "success": True,
            "task": "quiz",
            "result": result,
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


# ============================================================
# Summarization
# ============================================================

@app.post("/summarize")
async def summarize(request: TextRequest):

    try:
        result = summarize_text(
            request.text
        )

        return {
            "success": True,
            "task": "summary",
            "result": result,
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


# ============================================================
# Learning recommendations
# ============================================================

@app.post("/learn/recommendations")
async def learning_recommendations(
    request: LearningPathRequest,
):

    try:

        result = get_learning_recommendations(
            request.topic,
            request.level,
        )

        return {
            "success": True,
            "task": "learning_path",
            "result": result,
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


# ============================================================
# Development entry point
# ============================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
