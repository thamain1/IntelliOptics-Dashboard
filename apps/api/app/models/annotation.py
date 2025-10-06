"""Image annotation model."""

from __future__ import annotations

import uuid
from typing import Optional

from sqlalchemy import ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .mixins import BaseModel


class Annotation(BaseModel):
    """Stores reviewer annotations for an image query."""

    __tablename__ = "annotations"
    public_id_prefix = "ann"

    image_query_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("image_queries.id", ondelete="CASCADE"), nullable=False
    )
    annotator_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    label_json: Mapped[dict] = mapped_column(JSON, nullable=False)

    image_query: Mapped["ImageQuery"] = relationship(back_populates="annotations")
    annotator: Mapped[Optional["User"]] = relationship(back_populates="annotations")


from .image_query import ImageQuery  # noqa: E402
from .user import User  # noqa: E402
