

"""
API router aggregator — combines all v1 endpoints into one router.

Why a separate router file?
- Clean imports in main.py: just one router for all v1 endpoints
- Easy versioning: v2 gets its own router later
- Centralized prefix: all v1 routes start with /v1 automatically
"""

from fastapi import APIRouter

from imtiaz_mart_ai.api.v1.endpoints import chat, health

api_router = APIRouter()

api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(health.router, prefix="/health", tags=["health"])