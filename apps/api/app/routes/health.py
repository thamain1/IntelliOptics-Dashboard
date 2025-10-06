"""Health-check endpoint."""

from datetime import datetime, timezone
from typing import Any, Dict

from fastapi import APIRouter

from ..config import settings

router = APIRouter(tags=["health"])


@router.get("/health", summary="Readiness probe")
def healthcheck() -> Dict[str, Any]:
    """Return a simple readiness document for monitoring."""

    return {
        "status": "ok",
        "service": settings.app_name,
        "version": settings.app_version,
        "timestamp": datetime.now(tz=timezone.utc).isoformat(),
    }
