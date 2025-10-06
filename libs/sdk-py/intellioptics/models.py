from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from importlib import import_module
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence

from pydantic import BaseModel, Field

_ConfigDict = getattr(import_module("pydantic"), "ConfigDict", None)





class _BaseModel(BaseModel):
    """Base model that allows unknown fields for forward compatibility."""

    if _ConfigDict is not None:  # pragma: no branch
        model_config = _ConfigDict(extra="allow")  # type: ignore[assignment]
    else:  # pragma: no cover - executed on pydantic v1
        class Config:
            extra = "allow"


class ModeEnum(str, Enum):
    BINARY = "BINARY"
    MULTICLASS = "MULTICLASS"
    COUNTING = "COUNTING"
    TEXT = "TEXT"
    BOUNDING_BOX = "BOUNDING_BOX"


class DetectorTypeEnum(str, Enum):
    DETECTOR = "DETECTOR"
    EDGE = "EDGE"


class StatusEnum(str, Enum):
    ACTIVE = "ACTIVE"
    DISABLED = "DISABLED"
    PAUSED = "PAUSED"
    DELETED = "DELETED"


class BlankEnum(str, Enum):
    BLANK = ""


class ResultTypeEnum(str, Enum):
    BINARY = "BINARY"
    COUNTING = "COUNTING"
    MULTICLASS = "MULTICLASS"
    TEXT = "TEXT"
    BOUNDING_BOX = "BOUNDING_BOX"


class ImageQueryTypeEnum(str, Enum):
    IMAGE_QUERY = "IMAGE_QUERY"


class ChannelEnum(str, Enum):
    EMAIL = "EMAIL"
    TEXT = "TEXT"


class SnoozeTimeUnitEnum(str, Enum):
    SECONDS = "SECONDS"
    MINUTES = "MINUTES"
    HOURS = "HOURS"
    DAYS = "DAYS"


class ROI(_BaseModel):
    label: str
    top_left: Sequence[float]
    bottom_right: Sequence[float]
    confidence: Optional[float] = None


class BinaryClassificationResult(_BaseModel):
    label: Optional[str] = None
    confidence: Optional[float] = None
    source: Optional[str] = None
    human_reviewed: Optional[bool] = None
    extra: Dict[str, Any] | None = None


class CountingResult(_BaseModel):
    label: Optional[str] = None
    count: Optional[int] = None
    confidence: Optional[float] = None
    extra: Dict[str, Any] | None = None


class MultiClassificationResult(_BaseModel):
    label: Optional[str] = None
    confidence: Optional[float] = None
    probabilities: Dict[str, float] | None = None


class TextRecognitionResult(_BaseModel):
    text: Optional[str] = None
    confidence: Optional[float] = None
    spans: List[Dict[str, Any]] | None = None


class BoundingBoxResult(_BaseModel):
    label: Optional[str] = None
    confidence: Optional[float] = None
    rois: List[ROI] | None = None


class Detector(_BaseModel):
    id: str
    name: str
    query: str
    group_name: Optional[str] = None
    mode: ModeEnum | str
    confidence_threshold: Optional[float] = Field(default=0.9, ge=0.0, le=1.0)
    patience_time: Optional[float] = Field(default=30.0, ge=0.0, le=3600.0)
    metadata: Optional[Dict[str, Any]] = None
    mode_configuration: Optional[Dict[str, Any]] = None
    escalation_type: Optional[str] = None
    status: StatusEnum | BlankEnum | None = None
    type: DetectorTypeEnum | str = DetectorTypeEnum.DETECTOR
    created_at: Optional[datetime] = None


class DetectorGroup(_BaseModel):
    id: str
    name: str
    description: Optional[str] = None


class PaginatedDetectorList(_BaseModel):
    count: int
    next: Optional[str] = None
    previous: Optional[str] = None
    results: List[Detector] = Field(default_factory=list)


class ImageQuery(_BaseModel):
    id: str
    detector_id: Optional[str] = None
    confidence_threshold: Optional[float] = Field(default=0.9)
    patience_time: Optional[float] = Field(default=30.0, ge=0.0, le=3600.0)
    created_at: Optional[datetime] = None
    done_processing: Optional[bool] = False
    metadata: Optional[Dict[str, Any]] = None
    query: Optional[str] = None
    result: (
        BinaryClassificationResult
        | CountingResult
        | MultiClassificationResult
        | TextRecognitionResult
        | BoundingBoxResult
        | None
    ) = None
    result_type: Optional[ResultTypeEnum | str] = None
    status: Optional[str] = None
    label: Optional[str] = None
    confidence: Optional[float] = None
    extra: Dict[str, Any] | None = None


class PaginatedImageQueryList(_BaseModel):
    count: int
    next: Optional[str] = None
    previous: Optional[str] = None
    results: List[ImageQuery] = Field(default_factory=list)


class QueryResult(_BaseModel):
    id: str
    detector_id: Optional[str] = None
    status: str
    result_type: Optional[ResultTypeEnum | str] = None
    label: Optional[str] = None
    confidence: Optional[float] = None
    extra: Dict[str, Any] | None = None


class DetectorMetadata(_BaseModel):
    id: str
    name: str
    value: str


class ApiKey(_BaseModel):
    id: str
    name: str
    prefix: str
    created_at: datetime


class ApiKeyList(_BaseModel):
    count: int
    results: List[ApiKey] = Field(default_factory=list)


class UserIdentity(_BaseModel):
    id: str
    email: str
    roles: List[str]
    tenant: Optional[str] = None


class DetectorHealth(_BaseModel):
    id: str
    status: str
    last_heartbeat_at: Optional[datetime] = None


class Alert(_BaseModel):
    id: str
    detector_id: Optional[str] = None
    image_query_id: Optional[str] = None
    status: str
    message: Optional[str] = None
    channel: Optional[str] = None
    created_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None


class Escalation(_BaseModel):
    id: str
    alert_id: str
    assigned_to: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class Annotation(_BaseModel):
    id: str
    image_query_id: str
    label_json: Dict[str, Any]
    annotator_id: Optional[str] = None
    created_at: Optional[datetime] = None


class Stream(_BaseModel):
    id: str
    name: str
    rtsp_url: Optional[str] = None
    zone_masks: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None
    created_at: Optional[datetime] = None


class PaginatedStreamList(_BaseModel):
    count: int
    next: Optional[str] = None
    previous: Optional[str] = None
    results: List[Stream] = Field(default_factory=list)


class HumanReviewPolicy(Enum):
    DEFAULT = "DEFAULT"
    ALWAYS = "ALWAYS"
    NEVER = "NEVER"


class HumanReviewSettings(_BaseModel):
    policy: HumanReviewPolicy | str = HumanReviewPolicy.DEFAULT
    instructions: Optional[str] = None


@dataclass
class Pagination:
    count: int
    next: Optional[str]
    previous: Optional[str]


@dataclass
class PaginatedResponse:
    pagination: Pagination
    results: Iterable[Any]


@dataclass
class SubmitImageQueryResponse:
    image_query: ImageQuery
    result: Optional[QueryResult]
