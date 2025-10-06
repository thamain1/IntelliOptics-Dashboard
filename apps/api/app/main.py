"""FastAPI application factory for IntelliOptics."""

from fastapi import FastAPI

from .config import settings
from .db import configure_default_engine
from .routes import alerts, detectors, health, image_queries, streams


def create_app() -> FastAPI:
    """Build and configure a FastAPI instance."""

    app = FastAPI(title=settings.app_name, version=settings.app_version)
    app.include_router(health.router)
    app.include_router(alerts.router)
    app.include_router(detectors.router)
    app.include_router(image_queries.router)
    app.include_router(streams.router)

    @app.on_event("startup")
    def _configure_database() -> None:
        configure_default_engine()

    return app


app = create_app()
