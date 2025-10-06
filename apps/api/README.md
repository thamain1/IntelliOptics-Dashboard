# IntelliOptics API

The IntelliOptics API is a FastAPI service that powers the dashboard, edge
workers, and automation workflows. The current implementation provides a
structured application skeleton with configuration management, a health
endpoint, and pytest coverage so we can iterate on the authenticated CRUD
surface in focused follow-up pull requests.

## Getting started

```bash
cd apps/api
uv sync  # or pip install -e .[dev]
uvicorn apps.api.app.main:app --reload
```

The service exposes `/health` for readiness checks. Application settings are
loaded from environment variables (see `.env.example`).

## Running tests

```bash
cd /workspace/IntelliOptics-Dashboard
pytest apps/api/tests
```

Tests use FastAPI's `TestClient` to validate routing and payload shapes.
