"""Detector model definition."""

from __future__ import annotations

import uuid
from typing import List

from sqlalchemy import Boolean, Enum, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .enums import DetectorMode
from .mixins import BaseModel


class Detector(BaseModel):
    """A configured model that inspects image queries."""

    __tablename__ = "detectors"
    public_id_prefix = "det"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    mode: Mapped[DetectorMode] = mapped_column(Enum(DetectorMode, name="detector_mode"), nullable=False)
    query: Mapped[str] = mapped_column(Text, nullable=False)
    confidence_threshold: Mapped[float] = mapped_column(Float, nullable=False, default=0.5)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    created_by_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    creator: Mapped["User"] = relationship(back_populates="detectors")
    image_queries: Mapped[List["ImageQuery"]] = relationship(back_populates="detector")
    alerts: Mapped[List["Alert"]] = relationship(back_populates="detector")

    def __repr__(self) -> str:  # pragma: no cover
        return f"Detector(id={self.public_id}, name={self.name!r}, mode={self.mode})"


from .alert import Alert  # noqa: E402
from .image_query import ImageQuery  # noqa: E402
from .user import User  # noqa: E402
