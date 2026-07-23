"""
Pydantic Settings — loads .env automatically, no load_dotenv needed.
"""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


# Find .env file: look in project root (where pyproject.toml is)
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent  # src/imtiaz_mart_ai/config → project root
ENV_FILE = PROJECT_ROOT / ".env"


class Settings(BaseSettings):
    """
    All configuration lives here.
    
    Pydantic-settings automatically loads .env file.
    No need for python-dotenv or load_dotenv().
    """
    
    # ─── Application ─────────────────────────────
    APP_NAME: str = "imtiaz-mart-ai"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    
    # ─── LLM Providers ───────────────────────────
    GROQ_API_KEY: str = ""
    GROQ_BASE_URL: str = "https://api.groq.com/openai/v1"
    
    GEMINI_API_KEY: str = ""
    GEMINI_BASE_URL: str = "https://generativelanguage.googleapis.com/v1beta/openai/"
    
    # ─── Infrastructure ──────────────────────────
    REDIS_URL: str = "redis://localhost:6379"
    DATABASE_URL: str = ""
    
    # ─── Operational ─────────────────────────────
    CACHE_TTL_SECONDS: int = 1800
    CIRCUIT_FAILURE_THRESHOLD: int = 5
    CIRCUIT_RECOVERY_TIMEOUT: int = 30
    RATE_LIMIT_RPM: int = 60
    
    # Pydantic-settings v2 style
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",  # Ignore extra vars in .env
    )


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance."""
    return Settings()


def require_llm_key(provider: str) -> str:
    """Lazy validation for LLM keys."""
    settings = get_settings()
    
    if provider.lower() == "groq":
        key = settings.GROQ_API_KEY
        name = "GROQ_API_KEY"
    elif provider.lower() == "gemini":
        key = settings.GEMINI_API_KEY
        name = "GEMINI_API_KEY"
    else:
        raise ValueError(f"Unknown LLM provider: {provider}")
    
    if not key:
        raise RuntimeError(
            f"{name} is not set. "
            f"Copy .env.example to .env and fill in your API key."
        )
    
    return key