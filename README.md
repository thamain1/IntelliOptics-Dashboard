# IntelliOptics Monorepo

This repository hosts IntelliOptics, a platform that spans the FastAPI backend, the Next.js dashboard, an edge inference worker, and supporting shared libraries.

## Repository layout

```
intellioptics-dashboard/
├─ apps/
│  ├─ api/   # FastAPI backend (migrated from backend/)
│  ├─ web/   # Next.js dashboard (migrated from frontend/)
│  └─ edge/  # Placeholder for the edge worker import
├─ libs/
│  └─ sdk-py/  # IntelliOptics Python SDK (trimmed import)
│  └─ sdk-py/  # Placeholder for the Python SDK
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

The edge worker will be imported in smaller follow-up pull requests so the review tooling does not choke on binary dependencies. The Python SDK has been reintroduced here as a trimmed import that only keeps the actively maintained runtime package and tests. Each application folder contains a `.env.example` to document its required configuration.
