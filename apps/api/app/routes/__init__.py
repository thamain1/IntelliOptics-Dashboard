"""API route registrations."""

from . import alerts, detectors, health, image_queries, streams

__all__ = ["alerts", "detectors", "health", "image_queries", "streams"]
from . import alerts, detectors, health, image_queries

__all__ = ["alerts", "detectors", "health", "image_queries"]
from . import detectors, health, image_queries

__all__ = ["detectors", "health", "image_queries"]
from . import detectors, health

__all__ = ["detectors", "health"]
from . import health

__all__ = ["health"]
