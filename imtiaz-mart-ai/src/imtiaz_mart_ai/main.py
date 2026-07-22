"""
Application entry point — MINIMAL VERSION.

This main.py ONLY imports what exists right now:
- settings (we just created it)
- FastAPI (from pyproject.toml dependencies)

NO redis, NO logging module, NO api router yet.
We add them one by one as we create each file.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from imtiaz_mart_ai.config.settings import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan events: startup and shutdown.
    
    Right now this does nothing except print a message.
    We'll add Redis connection here later.
    """
    settings = get_settings()
    print(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    
    yield  # Application runs here
    
    print("🛑 Shutting down")


def create_app() -> FastAPI:
    """Application factory."""
    settings = get_settings()
    
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Agentic AI backend for Imtiaz Mart",
        lifespan=lifespan,
    )
    
    return app


# Global app instance for uvicorn
app = create_app()


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to Imtiaz Mart AI",
        "status": "running",
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}