# IntelliOptics API

The IntelliOptics API is a FastAPI service that powers the dashboard, edge
workers, and automation workflows. The codebase now includes the domain data
model, SQLAlchemy configuration, and Alembic migrations that describe the core
IntelliOptics schema.
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

Set `POSTGRES_URL` in `.env` to point at a PostgreSQL instance (e.g.
`postgresql+psycopg://username:password@localhost:5432/intellioptics`). The
application automatically initialises the SQLAlchemy engine during startup when
a database URL is present.

## Database migrations

Alembic is configured under `apps/api/migrations` with an initial revision that
creates the platform tables for users, detectors, image queries, alerts,
escalations, annotations, and streams. To run migrations locally:

```bash
cd apps/api
alembic -x sqlalchemy_url="postgresql+psycopg://..." upgrade head
```

For development against SQLite you can pass a different URL, though production
should use PostgreSQL.
The service exposes `/health` for readiness checks. Application settings are
loaded from environment variables (see `.env.example`).

## Running tests

```bash
cd /workspace/IntelliOptics-Dashboard
pytest apps/api/tests
```

Tests exercise the FastAPI router and validate the SQLAlchemy metadata so the
schema definition cannot drift.
Tests use FastAPI's `TestClient` to validate routing and payload shapes.
