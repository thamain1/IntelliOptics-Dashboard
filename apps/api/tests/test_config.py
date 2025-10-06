"""Settings helper tests."""

from __future__ import annotations

from apps.api.app.config import Settings


def test_database_url_coerces_psycopg_driver() -> None:
    settings = Settings(postgres_url="postgresql://user:pass@localhost:5432/db")
    assert settings.database_url() == "postgresql+psycopg://user:pass@localhost:5432/db"


def test_database_url_preserves_driver() -> None:
    settings = Settings(postgres_url="postgresql+psycopg://user:pass@localhost:5432/db")
    assert settings.database_url() == "postgresql+psycopg://user:pass@localhost:5432/db"
