"""Python SDK for interacting with the IntelliOptics platform."""

from .client import IntelliOpticsAsyncClient, IntelliOpticsClient
from .messaging import InferenceAnswer, InferenceJobMessage, InferenceResultMessage
from .models import (
    AlertEvent,
    Detector,
    DetectorCreate,
    ImageQuery,
    ImageQueryResult,
    parse_alerts,
    parse_detectors,
)

__all__ = [
    "IntelliOpticsAsyncClient",
    "IntelliOpticsClient",
    "Detector",
    "DetectorCreate",
    "ImageQuery",
    "ImageQueryResult",
    "AlertEvent",
    "parse_detectors",
    "parse_alerts",
    "InferenceAnswer",
    "InferenceJobMessage",
    "InferenceResultMessage",
]

__version__ = "0.1.0"
