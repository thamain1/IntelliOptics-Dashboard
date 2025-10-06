"""Pydantic models for stream endpoints."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class StreamCreate(BaseModel):
    """Payload for creating a stream."""

    name: str = Field(min_length=1, max_length=255)
    rtsp_url: str = Field(min_length=1, description="RTSP connection string")
    zone_masks: dict[str, Any] | None = Field(default=None, description="Optional zone mask metadata")
    is_active: bool = Field(default=True)


class StreamUpdate(BaseModel):
    """Partial update payload for an existing stream."""

    name: str | None = Field(default=None, min_length=1, max_length=255)
    rtsp_url: str | None = Field(default=None, min_length=1, description="RTSP connection string")
    zone_masks: dict[str, Any] | None = Field(default=None, description="Optional zone mask metadata")
    is_active: bool | None = Field(default=None)


class StreamRead(BaseModel):
    """Response model for stream resources."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    rtsp_url: str
    zone_masks: dict[str, Any] | None
    is_active: bool
    created_at: datetime
    updated_at: datetime


__all__ = ["StreamCreate", "StreamRead", "StreamUpdate"]
