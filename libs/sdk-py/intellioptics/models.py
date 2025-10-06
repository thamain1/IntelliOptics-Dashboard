"""Typed models used by the IntelliOptics SDK."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Iterable, Optional, Tuple


def _parse_datetime(value: Optional[str]) -> Optional[datetime]:
    if value is None:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:  # pragma: no cover - defensive guard
        raise ValueError(f"Invalid datetime value: {value!r}") from exc


@dataclass(frozen=True)
class DetectorCreate:
    """Data required to create a detector via the API."""

    name: str
    mode: str
    query: str
    confidence_threshold: float = 0.5
    is_active: bool = True

    def to_payload(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "mode": self.mode,
            "query": self.query,
            "confidence_threshold": self.confidence_threshold,
            "is_active": self.is_active,
        }


@dataclass(frozen=True)
class Detector:
    """Representation of a detector returned by the API."""

    id: str
    name: str
    mode: str
    query: str
    confidence_threshold: float
    is_active: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "Detector":
        return cls(
            id=payload["id"],
            name=payload["name"],
            mode=payload["mode"],
            query=payload.get("query", ""),
            confidence_threshold=float(payload.get("confidence_threshold", 0.0)),
            is_active=bool(payload.get("is_active", False)),
            created_at=_parse_datetime(payload.get("created_at")),
            updated_at=_parse_datetime(payload.get("updated_at")),
        )


@dataclass(frozen=True)
class ImageQuery:
    """Metadata describing an image query request."""

    id: str
    detector_id: str
    snapshot_url: Optional[str]
    created_at: Optional[datetime] = None
    processed_at: Optional[datetime] = None

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "ImageQuery":
        return cls(
            id=payload["id"],
            detector_id=payload["detector_id"],
            snapshot_url=payload.get("snapshot_url"),
            created_at=_parse_datetime(payload.get("created_at")),
            processed_at=_parse_datetime(payload.get("processed_at")),
        )


@dataclass(frozen=True)
class ImageQueryResult:
    """Final answer returned from the API when an image query completes."""

    id: str
    answer: str
    score: Optional[float] = None
    processed_at: Optional[datetime] = None

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "ImageQueryResult":
        return cls(
            id=payload["id"],
            answer=payload.get("answer", "UNKNOWN"),
            score=payload.get("score"),
            processed_at=_parse_datetime(payload.get("processed_at")),
        )


@dataclass(frozen=True)
class AlertEvent:
    """Simplified alert event representation returned from the API."""

    id: str
    detector_id: str
    message: str
    status: str
    channel: Optional[str] = None
    created_at: Optional[datetime] = None

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "AlertEvent":
        return cls(
            id=payload["id"],
            detector_id=payload.get("detector_id", ""),
            message=payload.get("message", ""),
            status=payload.get("status", ""),
            channel=payload.get("channel"),
            created_at=_parse_datetime(payload.get("created_at")),
        )


def parse_detectors(payload: Iterable[Dict[str, Any]]) -> Tuple[Detector, ...]:
    return tuple(Detector.from_dict(item) for item in payload)


def parse_alerts(payload: Iterable[Dict[str, Any]]) -> Tuple[AlertEvent, ...]:
    return tuple(AlertEvent.from_dict(item) for item in payload)
