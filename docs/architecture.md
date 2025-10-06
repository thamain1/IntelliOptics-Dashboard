# IntelliOptics Architecture

The Python SDK exposes the API client alongside shared Service Bus message contracts so the
edge worker, API, and tooling agree on the schema for the `inference-jobs` and
`inference-results` topics. A full architecture write-up will follow once the edge worker is brought
into the monorepo in reviewable slices.
