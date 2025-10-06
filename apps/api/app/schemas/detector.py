"""Pydantic models for detector endpoints."""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from ..models.enums import DetectorMode


class DetectorCreate(BaseModel):
    """Payload for creating a detector."""

    name: str = Field(min_length=1, max_length=255)
    mode: DetectorMode
    query: str = Field(min_length=1)
    confidence_threshold: float = Field(default=0.5, ge=0.0, le=1.0)
    is_active: bool = Field(default=True)
    created_by: str = Field(description="Creator user public identifier (usr-<uuid>)")

    def creator_uuid(self) -> uuid.UUID:
        """Extract the UUID component from the provided creator identifier."""

        prefix = "usr-"
        if not self.created_by.startswith(prefix):
            raise ValueError("created_by must start with 'usr-'")
        identifier = self.created_by[len(prefix) :]
        try:
            return uuid.UUID(identifier)
        except ValueError as exc:  # pragma: no cover - defensive
            raise ValueError("created_by must include a valid UUID") from exc


class DetectorRead(BaseModel):
    """Response model for detector resources."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    mode: DetectorMode
    query: str
    confidence_threshold: float
    is_active: bool
    created_by: str
    created_at: datetime
    updated_at: datetime


__all__ = ["DetectorCreate", "DetectorRead"]
