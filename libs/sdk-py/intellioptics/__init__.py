"""Python SDK for interacting with the IntelliOptics API."""

from .client import IntelliOpticsClient, IntelliOpticsAsyncClient
from .models import (
    AlertEvent,
    Detector,
    DetectorCreate,
    ImageQuery,
    ImageQueryResult,
)

__all__ = [
    "IntelliOpticsClient",
    "IntelliOpticsAsyncClient",
    "Detector",
    "DetectorCreate",
    "ImageQuery",
    "ImageQueryResult",
    "AlertEvent",
]

__version__ = "0.1.0"
