

"""
Pydantic Settings validates environment variables at startup.

If GROQ_API_KEY is missing, the app REFUSES to start.
No silent failures. No None checks scattered through your code.
"""

import os
from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    All configuration lives here. One source of truth.
    
    Why Pydantic Settings?
    - Auto-loads from .env file
    - Validates types (REDIS_URL must be a string)
    - Caches with @lru_cache (created once, reused everywhere)
    """
    
    # ─── Application ─────────────────────────────
    APP_NAME: str = "imtiaz-mart-ai"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    
    # ─── LLM Providers ───────────────────────────
    GROQ_API_KEY: str
    GROQ_BASE_URL: str = "https://api.groq.com/openai/v1"
    
    GEMINI_API_KEY: str
    GEMINI_BASE_URL: str = "https://generativelanguage.googleapis.com/v1beta/openai/"
    
    # ─── Infrastructure ──────────────────────────
    REDIS_URL: str = "redis://localhost:6379"
    
    # ─── Operational ─────────────────────────────
    CACHE_TTL_SECONDS: int = 1800
    CIRCUIT_FAILURE_THRESHOLD: int = 5
    CIRCUIT_RECOVERY_TIMEOUT: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    """
    Cached settings instance.
    
    Called from anywhere: settings = get_settings()
    Always returns the same object (efficient, consistent).
    """
    return Settings()