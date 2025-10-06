"""Shared messaging contracts for Service Bus integration.

These types mirror the `inference-jobs` and `inference-results` topics used by
the edge workers and cloud fallback processors.  They provide light-weight
helpers for serialising payloads to and from dictionaries so the same schema
can be reused by the API, edge apps, and any tooling built on top of the SDK.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional


class InferenceAnswer(str, Enum):
    """Possible answers returned from an inference result."""

    YES = "YES"
    NO = "NO"
    UNKNOWN = "UNKNOWN"


def _ensure_aware(dt: Optional[datetime]) -> Optional[datetime]:
    if dt is None:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


def _to_iso(dt: Optional[datetime]) -> Optional[str]:
    aware = _ensure_aware(dt)
    if aware is None:
        return None
    return aware.isoformat()


def _parse_datetime(value: Optional[str]) -> Optional[datetime]:
    if value in (None, ""):
        return None
    parsed = datetime.fromisoformat(value)
    return _ensure_aware(parsed)


@dataclass(slots=True)
class InferenceJobMessage:
    """Payload published to the `inference-jobs` topic."""

    job_id: str
    model_id: str
    detector_id: str
    requested_by: str
    image_blob_url: Optional[str] = None
    rtsp_ref: Optional[str] = None
    deadline: Optional[datetime] = None
    trace: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.deadline = _ensure_aware(self.deadline)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "job_id": self.job_id,
            "model_id": self.model_id,
            "detector_id": self.detector_id,
            "requested_by": self.requested_by,
            "image_blob_url": self.image_blob_url,
            "rtsp_ref": self.rtsp_ref,
            "deadline": _to_iso(self.deadline),
            "trace": self.trace or None,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "InferenceJobMessage":
        return cls(
            job_id=data["job_id"],
            model_id=data["model_id"],
            detector_id=data["detector_id"],
            requested_by=data["requested_by"],
            image_blob_url=data.get("image_blob_url"),
            rtsp_ref=data.get("rtsp_ref"),
            deadline=_parse_datetime(data.get("deadline")),
            trace=data.get("trace") or {},
        )


@dataclass(slots=True)
class InferenceResultMessage:
    """Payload published to the `inference-results` topic."""

    job_id: str
    answer: InferenceAnswer
    score: float
    model_revision: Optional[str] = None
    processed_at: Optional[datetime] = None

    def __post_init__(self) -> None:
        self.processed_at = _ensure_aware(self.processed_at)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "job_id": self.job_id,
            "answer": self.answer.value,
            "score": self.score,
            "model_rev": self.model_revision,
            "processed_at": _to_iso(self.processed_at),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "InferenceResultMessage":
        return cls(
            job_id=data["job_id"],
            answer=InferenceAnswer(data["answer"]),
            score=float(data["score"]),
            model_revision=data.get("model_rev"),
            processed_at=_parse_datetime(data.get("processed_at")),
        )

