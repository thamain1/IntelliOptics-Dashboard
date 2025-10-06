"""Escalation model definition."""

from __future__ import annotations

import uuid
from typing import Optional

from sqlalchemy import Enum, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .enums import EscalationStatus
from .mixins import BaseModel


class Escalation(BaseModel):
    """Represents human triage of an alert."""

    __tablename__ = "escalations"
    public_id_prefix = "esc"

    alert_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("alerts.id", ondelete="CASCADE"), nullable=False)
    assigned_to_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[EscalationStatus] = mapped_column(
        Enum(EscalationStatus, name="escalation_status"), nullable=False
    )

    alert: Mapped["Alert"] = relationship(back_populates="escalations")
    assignee: Mapped[Optional["User"]] = relationship(back_populates="escalations")

    def __repr__(self) -> str:  # pragma: no cover
        return f"Escalation(id={self.public_id}, status={self.status})"


from .alert import Alert  # noqa: E402
from .user import User  # noqa: E402
