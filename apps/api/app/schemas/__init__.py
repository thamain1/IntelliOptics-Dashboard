"""Pydantic schemas exposed by the IntelliOptics API."""

from .detector import DetectorCreate, DetectorRead

__all__ = [
    "DetectorCreate",
    "DetectorRead",
]
