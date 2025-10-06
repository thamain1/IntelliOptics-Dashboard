"""Alert model definition."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import List

from sqlalchemy import Enum, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .enums import AlertChannel, AlertStatus
from .mixins import BaseModel


class Alert(BaseModel):
    """Represents an alert raised by a detector/image query."""

    __tablename__ = "alerts"
    public_id_prefix = "alrt"

    detector_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("detectors.id", ondelete="CASCADE"), nullable=False)
    image_query_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("image_queries.id", ondelete="CASCADE"), nullable=False
    )
    status: Mapped[AlertStatus] = mapped_column(Enum(AlertStatus, name="alert_status"), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    channel: Mapped[AlertChannel] = mapped_column(Enum(AlertChannel, name="alert_channel"), nullable=False)
    resolved_at: Mapped[datetime | None] = mapped_column(nullable=True)

    detector: Mapped["Detector"] = relationship(back_populates="alerts")
    image_query: Mapped["ImageQuery"] = relationship(back_populates="alerts")
    escalations: Mapped[List["Escalation"]] = relationship(back_populates="alert")

    def __repr__(self) -> str:  # pragma: no cover
        return f"Alert(id={self.public_id}, status={self.status}, channel={self.channel})"


from .escalation import Escalation  # noqa: E402
from .detector import Detector  # noqa: E402
from .image_query import ImageQuery  # noqa: E402
