# IntelliOptics Architecture

The monorepo currently contains three major workstreams:

* `apps/api` – FastAPI backend. The current baseline exposes an application
  factory, environment-driven settings, and a `/health` endpoint with pytest
  coverage so we can add authenticated business endpoints incrementally.
* `apps/web` – Next.js dashboard (port of the original frontend).
* `libs/sdk-py` – Python SDK with the REST client and shared Service Bus
  message contracts.

Upcoming pull requests will extend the API with authentication, persistence,
and Service Bus integrations before reconnecting the edge worker import and
infrastructure definitions.
