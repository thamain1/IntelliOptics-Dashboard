"""Pydantic schemas for image query endpoints."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Literal, Optional

from pydantic import AnyHttpUrl, BaseModel, ConfigDict, Field

from ..models.enums import ImageQueryAnswer


class ImageQueryCreate(BaseModel):
    """Payload for submitting an image query."""

    detector_id: str = Field(description="Detector public identifier (det-<uuid>)")
    rtsp_source_id: Optional[str] = Field(
        default=None, description="Optional stream identifier (str-<uuid>)"
    )
    snapshot_url: AnyHttpUrl

    def detector_uuid(self) -> uuid.UUID:
        prefix = "det-"
        if not self.detector_id.startswith(prefix):
            raise ValueError("detector_id must start with 'det-'")
        identifier = self.detector_id[len(prefix) :]
        try:
            return uuid.UUID(identifier)
        except ValueError as exc:  # pragma: no cover - defensive
            raise ValueError("detector_id must include a valid UUID") from exc

    def stream_uuid(self) -> Optional[uuid.UUID]:
        if self.rtsp_source_id is None:
            return None
        prefix = "str-"
        if not self.rtsp_source_id.startswith(prefix):
            raise ValueError("rtsp_source_id must start with 'str-'")
        identifier = self.rtsp_source_id[len(prefix) :]
        try:
            return uuid.UUID(identifier)
        except ValueError as exc:  # pragma: no cover - defensive
            raise ValueError("rtsp_source_id must include a valid UUID") from exc


class ImageQueryRead(BaseModel):
    """Response payload describing an image query."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    detector_id: str
    rtsp_source_id: Optional[str]
    snapshot_url: AnyHttpUrl
    answer: Optional[ImageQueryAnswer]
    answer_score: Optional[float]
    created_at: datetime
    processed_at: Optional[datetime]


class ImageQueryWaitResponse(BaseModel):
    """Envelope returned by the wait endpoint indicating completion state."""

    status: Literal["pending", "complete"]
    result: Optional[ImageQueryRead] = None


__all__ = [
    "ImageQueryCreate",
    "ImageQueryRead",
    "ImageQueryWaitResponse",
]
