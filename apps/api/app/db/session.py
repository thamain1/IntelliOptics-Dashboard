"""Database session configuration and FastAPI dependency wiring."""

from __future__ import annotations

from contextlib import contextmanager
from typing import Generator, Optional

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from ..config import settings

_engine: Optional[Engine] = None
_SessionFactory: Optional[sessionmaker[Session]] = None


def configure_engine(database_url: str) -> None:
    """Initialise the global SQLAlchemy engine and session factory."""

    if not database_url:
        raise RuntimeError("DATABASE_URL is empty; set POSTGRES_URL in the environment")

    connect_args = {"check_same_thread": False} if database_url.startswith("sqlite") else {}

    engine = create_engine(database_url, future=True, echo=False, connect_args=connect_args)
    session_factory = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)

    global _engine, _SessionFactory
    _engine = engine
    _SessionFactory = session_factory


def get_engine() -> Engine:
    """Return the configured SQLAlchemy engine."""

    if _engine is None:
        raise RuntimeError("Database engine has not been configured")
    return _engine


def get_session_factory() -> sessionmaker[Session]:
    """Return the configured session factory."""

    if _SessionFactory is None:
        raise RuntimeError("Session factory has not been configured")
    return _SessionFactory


@contextmanager
def session_scope() -> Generator[Session, None, None]:
    """Provide a transactional scope around a series of operations."""

    session_factory = get_session_factory()
    session = session_factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_session() -> Generator[Session, None, None]:
    """FastAPI dependency that yields a database session."""

    session_factory = get_session_factory()
    session = session_factory()
    try:
        yield session
    finally:
        session.close()


def configure_default_engine() -> None:
    """Configure the engine using the current settings if not already configured."""

    if _engine is None and settings.postgres_url:
        configure_engine(settings.database_url())
