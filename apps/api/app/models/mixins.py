"""Reusable mixins for SQLAlchemy models."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import ClassVar

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from ..db import Base, GUID


class PrimaryKeyUUIDMixin:
    """Mixin providing a UUID primary key with a prefixed public identifier."""

    public_id_prefix: ClassVar[str]

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)

    @property
    def public_id(self) -> str:
        return f"{self.public_id_prefix}-{self.id}"  # type: ignore[str-format]


class TimestampMixin:
    """Mixin adding created/updated timestamps."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


class BaseModel(Base):
    """Declarative base class including UUID primary key and timestamps."""

    __abstract__ = True
    public_id_prefix: ClassVar[str]

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    @property
    def public_id(self) -> str:
        return f"{self.public_id_prefix}-{self.id}"  # type: ignore[str-format]
