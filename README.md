# IntelliOptics Monorepo

This repository hosts IntelliOptics, a platform that spans the FastAPI backend,
the Next.js dashboard, an edge inference worker, and supporting shared
libraries.

## Repository layout

```
intellioptics-dashboard/
├─ apps/
│  ├─ api/   # FastAPI backend (domain models, migrations, health + detector endpoints, tests)
│  ├─ api/   # FastAPI backend (domain models, migrations, health endpoint, tests)
│  ├─ api/   # FastAPI backend (application skeleton with health endpoint + tests)
│  ├─ web/   # Next.js dashboard (migrated from frontend/)
│  └─ edge/  # Placeholder for the edge worker import
├─ libs/
│  └─ sdk-py/  # IntelliOptics Python SDK (trimmed import)
├─ functions/
│  └─ alerts/  # Azure Functions placeholder
├─ infra/
│  ├─ bicep/
│  ├─ helm/
│  └─ github/
├─ ops/
│  ├─ runbooks/
│  └─ scripts/
└─ docs/
   └─ architecture.md
```

The edge worker will be imported in smaller follow-up pull requests so the
review tooling does not choke on binary dependencies. The Python SDK has been
reintroduced here as a trimmed import that only keeps the actively maintained
runtime package and tests. Each application folder contains a `.env.example` to
document its required configuration.

The API now defines the relational schema for IntelliOptics using SQLAlchemy and
ships an initial Alembic migration so the database can be provisioned in CI and
local development environments. The first REST surfaces focus on `/v1/detectors`
and `/v1/image-queries`, demonstrating the persistence layer in action with
detector CRUD helpers, image submission, retrieval, and long-poll status checks.
local development environments. The first REST surface focuses on `/v1/detectors`
create/list/read operations, demonstrating the persistence layer in action.
local development environments.

### Development quick start

* `apps/api` contains the FastAPI service. Install dependencies with `uv sync`
or `pip install -e .[dev]`, then run `uvicorn apps.api.app.main:app --reload`.
  * Use Alembic via `alembic upgrade head` to apply database migrations once
    `POSTGRES_URL` is configured.
* `apps/web` contains the Next.js dashboard.
* `libs/sdk-py` provides the Python SDK and shared messaging contracts.

Refer to the documentation under `docs/` and runbooks under `ops/` for deeper
platform guidance.
