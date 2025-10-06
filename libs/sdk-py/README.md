# IntelliOptics Python SDK (trimmed import)

This directory contains a lightweight version of the IntelliOptics Python SDK that is small enough to
review comfortably while still exercising the public contract relied upon by internal tools. The
package intentionally focuses on the small set of helper types and client methods that already exist
in the platform today:

* `IntelliOpticsClient` – synchronous wrapper around the `/health`, `/v1/detectors`, `/v1/image-queries`,
  and `/v1/alerts/events/recent` endpoints.
* `IntelliOpticsAsyncClient` – async mirror that can be reused by automation and tests.
* Dataclass models that translate JSON responses into typed Python objects.
* Shared Service Bus message contracts for inference job/result topics.

The goal is to provide a realistic but minimal reference while the full SDK is re-imported in smaller,
reviewable slices.

## Local development

```bash
cd libs/sdk-py
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .[dev]
pytest
```

The optional `[dev]` extra installs `pytest` for running the included unit tests.

## Contents

```text
libs/sdk-py/
├─ intellioptics/      # Runtime SDK package (clients + models)
├─ tests/              # Unit tests that exercise the minimal surface area
└─ pyproject.toml      # Packaging definition reused by the published wheel
```

Refer to `docs/architecture.md` in the repository root for how the SDK maps onto the broader
IntelliOptics platform.
