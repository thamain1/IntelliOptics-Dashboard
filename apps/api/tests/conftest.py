"""Pytest fixtures for the IntelliOptics API tests."""

from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from apps.api.app.db import Base, configure_engine, get_engine, get_session_factory

import pytest
from fastapi.testclient import TestClient

from apps.api.app.main import create_app


@pytest.fixture()
def database(tmp_path: Path) -> Iterator[None]:
    """Initialise a SQLite database for each test run."""

    db_path = tmp_path / "test.db"
    configure_engine(f"sqlite+pysqlite:///{db_path}")
    engine = get_engine()
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    try:
        yield
    finally:
        Base.metadata.drop_all(engine)
        engine.dispose()


@pytest.fixture()
def client(database: None) -> Iterator[TestClient]:
def client() -> Iterator[TestClient]:
    """Provide a FastAPI test client for request/response assertions."""

    with TestClient(create_app()) as client:
        yield client


@pytest.fixture()
def db_session(database: None) -> Iterator[Session]:
    """Return a SQLAlchemy session bound to the test database."""

    session_factory = get_session_factory()
    session = session_factory()
    try:
        yield session
        session.commit()
    finally:
        session.rollback()
        session.close()
