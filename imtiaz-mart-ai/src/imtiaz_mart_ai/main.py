"""
Application entry point.

Responsibilities:
1. Create FastAPI application
2. Configure middleware
3. Register API routers
4. Handle startup/shutdown events

NO business logic here. NO agent definitions here.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from imtiaz_mart_ai.config.settings import get_settings
from imtiaz_mart_ai.api.v1.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    settings = get_settings()
    print(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    
    yield
    
    print("🛑 Shutting down")


def create_app() -> FastAPI:
    """Application factory."""
    settings = get_settings()
    
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Agentic AI backend for Imtiaz Mart",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Register v1 API routes
    app.include_router(api_router, prefix="/v1")
    
    return app


app = create_app()


@app.get("/", include_in_schema=False)
async def root():
    """Root redirect to API documentation."""
    return {
        "message": "Welcome to Imtiaz Mart AI",
        "docs": "/docs",
        "health": "/v1/health",
    }