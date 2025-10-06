# IntelliOptics Python SDK (trimmed import)

This directory contains a slimmed-down copy of the IntelliOptics Python SDK that ships with the
`intellioptics` package. Only the actively maintained runtime package and its supporting tests are
included so the monorepo can evolve the SDK alongside the API without carrying legacy scaffolding
or generated artifacts.

The SDK exposes both synchronous and asynchronous clients for talking to the IntelliOptics API,
helpers for encoding imagery, and a Typer-based CLI that exercises the same client surface. The
packaging metadata lives in `pyproject.toml` and points to the modules under `intellioptics/`.

## Local development

```bash
cd libs/sdk-py
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .[dev]
pytest
```

The optional `[dev]` extra installs the lightweight tooling used by the tests (`pytest` and `Pillow`).

## Contents

```text
libs/sdk-py/
├─ intellioptics/      # Runtime SDK package (client, HTTP helpers, CLI, models)
├─ tests/              # Unit tests covering the SDK surface area
└─ pyproject.toml      # Packaging definition reused by the published wheel
```

Refer to `docs/architecture.md` in the repository root for how the SDK maps onto the broader
IntelliOptics platform.
