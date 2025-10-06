"""Pytest fixtures for the IntelliOptics API tests."""

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from apps.api.app.main import create_app


@pytest.fixture()
def client() -> Iterator[TestClient]:
    """Provide a FastAPI test client for request/response assertions."""

    with TestClient(create_app()) as client:
        yield client
