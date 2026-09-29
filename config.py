import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")


class Settings:
    """Central application configuration."""

    APP_NAME: str = os.getenv(
        "APP_NAME",
        "EduGenie"
    )

    APP_VERSION: str = os.getenv(
        "APP_VERSION",
        "1.0.0"
    )

    DEBUG: bool = os.getenv(
        "DEBUG",
        "true"
    ).lower() == "true"

    HOST: str = os.getenv(
        "HOST",
        "127.0.0.1"
    )

    PORT: int = int(
        os.getenv(
            "PORT",
            "8000"
        )
    )

    GEMINI_API_KEY: str = os.getenv(
        "GEMINI_API_KEY",
        ""
    )

    GEMINI_MODEL: str = os.getenv(
        "GEMINI_MODEL",
        "gemini-2.5-flash"
    )

    USE_LOCAL_EXPLANATION: bool = os.getenv(
        "USE_LOCAL_EXPLANATION",
        "true"
    ).lower() == "true"

    LOCAL_EXPLANATION_MODEL: str = os.getenv(
        "LOCAL_EXPLANATION_MODEL",
        "MBZUAI/LaMini-Flan-T5-783M"
    )

    MAX_INPUT_LENGTH: int = int(
        os.getenv(
            "MAX_INPUT_LENGTH",
            "12000"
        )
    )

    GEMINI_TEMPERATURE: float = float(
        os.getenv(
            "GEMINI_TEMPERATURE",
            "0.4"
        )
    )

    GEMINI_MAX_OUTPUT_TOKENS: int = int(
        os.getenv(
            "GEMINI_MAX_OUTPUT_TOKENS",
            "2048"
        )
    )


settings = Settings()
