"""Schemas for alert responses."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from ..models.enums import AlertChannel, AlertStatus


class AlertRead(BaseModel):
    """Serialized representation of an alert."""

    id: str
    detector_id: str
    image_query_id: str
    status: AlertStatus
    message: str
    channel: AlertChannel
    created_at: datetime
    updated_at: datetime
    resolved_at: datetime | None = None

    model_config = {
        "from_attributes": True,
    }


__all__ = ["AlertRead"]
