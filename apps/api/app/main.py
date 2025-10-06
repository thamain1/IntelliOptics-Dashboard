"""FastAPI application factory for IntelliOptics."""

from fastapi import FastAPI

from .config import settings
from .routes import health


def create_app() -> FastAPI:
    """Build and configure a FastAPI instance."""

    app = FastAPI(title=settings.app_name, version=settings.app_version)
    app.include_router(health.router)
    return app


app = create_app()
