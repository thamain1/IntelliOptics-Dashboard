"""Video stream model."""

from __future__ import annotations

from typing import List, Optional

from sqlalchemy import Boolean, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .mixins import BaseModel


class Stream(BaseModel):
    """Represents an RTSP video stream."""

    __tablename__ = "streams"
    public_id_prefix = "str"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    rtsp_url: Mapped[str] = mapped_column(Text, nullable=False)
    zone_masks: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    image_queries: Mapped[List["ImageQuery"]] = relationship(back_populates="stream")

    def __repr__(self) -> str:  # pragma: no cover
        return f"Stream(id={self.public_id}, name={self.name!r})"


from .image_query import ImageQuery  # noqa: E402
