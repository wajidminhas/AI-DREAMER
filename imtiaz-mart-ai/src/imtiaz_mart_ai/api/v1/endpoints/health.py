

"""
Health check endpoint — tells monitoring systems if the app is alive.

Why health checks matter:
- Load balancers route traffic only to healthy instances
- Kubernetes restarts unhealthy containers automatically
- Monitoring tools (Datadog, Grafana) alert on failures
"""

from fastapi import APIRouter

from imtiaz_mart_ai.config.settings import get_settings

router = APIRouter()


@router.get("")
async def health():
    """
    Simple health check.
    
    TODO (Day 13): Add dependency checks — Redis, LLM API availability
    """
    settings = get_settings()
    
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }