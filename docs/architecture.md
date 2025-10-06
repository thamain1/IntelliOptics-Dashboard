# IntelliOptics Architecture

The monorepo currently contains three major workstreams:

* `apps/api` – FastAPI backend. The service exposes an application factory,
  environment-driven settings, and `/health`, `/v1/detectors`, `/v1/image-queries`,
  read-only `/v1/alerts`, and `/v1/streams` endpoints. SQLAlchemy models and migrations cover
  the core domain tables (users, detectors, streams, image queries, alerts,
  escalations, annotations) so persistence work can proceed in small, reviewable
  increments.
* `apps/web` – Next.js dashboard (port of the original frontend).
* `libs/sdk-py` – Python SDK with the REST client and shared Service Bus
  message contracts.

Upcoming pull requests will extend the API with authentication, additional CRUD
operations, and Service Bus integrations before reconnecting the edge worker
import and infrastructure definitions.
