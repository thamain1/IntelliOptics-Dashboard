# IntelliOptics API

The IntelliOptics API is a FastAPI service that powers the dashboard, edge
workers, and automation workflows. The codebase now includes the domain data
model, SQLAlchemy configuration, and Alembic migrations that describe the core
IntelliOptics schema. The initial `/v1/detectors` and `/v1/image-queries`
endpoints expose detector CRUD helpers plus image submission, retrieval, and
status polling backed by these models.

## Getting started

```bash
cd apps/api
uv sync  # or pip install -e .[dev]
uvicorn apps.api.app.main:app --reload
```

Set `POSTGRES_URL` in `.env` to point at a PostgreSQL instance (e.g.
`postgresql+psycopg://username:password@localhost:5432/intellioptics`). The
application automatically initialises the SQLAlchemy engine during startup when
a database URL is present. Optional `IMAGE_QUERY_WAIT_TIMEOUT_SECONDS` and
`IMAGE_QUERY_WAIT_POLL_SECONDS` knobs control the `/wait` polling behaviour for
both production and test environments.

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

## REST endpoints

The service currently exposes:

* `GET /health` – health probe used by the deployment platform.
* `POST /v1/detectors` – create a detector tied to an existing `usr-` user id.
* `GET /v1/detectors` – list detectors ordered by creation time.
* `GET /v1/detectors/{detector_id}` – fetch a detector by its `det-` identifier.
* `POST /v1/image-queries` – record a snapshot or RTSP reference for downstream inference.
* `GET /v1/image-queries/{image_query_id}` – retrieve an image query by its `iq-` id.
* `GET /v1/image-queries/{image_query_id}/wait` – poll for completion with optional `timeout`/`poll` overrides.

Subsequent pull requests will layer authentication, remaining CRUD operations,
and additional resources following the OpenAPI-first workflow described in the
project specification.

## Running tests

```bash
cd /workspace/IntelliOptics-Dashboard
pytest apps/api/tests
```

Tests exercise the FastAPI routers, validate the SQLAlchemy metadata, and cover
the detector and image query endpoint behaviours.
