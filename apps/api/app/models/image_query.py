"""Image query model."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Enum, Float, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .enums import ImageQueryAnswer
from .mixins import BaseModel


class ImageQuery(BaseModel):
    """Represents an image classification request and response."""

    __tablename__ = "image_queries"
    public_id_prefix = "iq"

    detector_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("detectors.id", ondelete="CASCADE"), nullable=False)
    rtsp_source_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("streams.id"), nullable=True)
    snapshot_url: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[Optional[ImageQueryAnswer]] = mapped_column(
        Enum(ImageQueryAnswer, name="image_query_answer"), nullable=True
    )
    answer_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    processed_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    detector: Mapped["Detector"] = relationship(back_populates="image_queries")
    stream: Mapped[Optional["Stream"]] = relationship(back_populates="image_queries")
    alerts: Mapped[list["Alert"]] = relationship(back_populates="image_query")
    annotations: Mapped[list["Annotation"]] = relationship(back_populates="image_query")

    def __repr__(self) -> str:  # pragma: no cover
        return f"ImageQuery(id={self.public_id}, detector_id={self.detector_id})"


from .alert import Alert  # noqa: E402
from .annotation import Annotation  # noqa: E402
from .detector import Detector  # noqa: E402
from .stream import Stream  # noqa: E402
