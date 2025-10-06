"""Enumerations shared across database models."""

from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    ANALYST = "analyst"
    VIEWER = "viewer"


class DetectorMode(str, Enum):
    BINARY = "binary"
    MULTICLASS = "multiclass"


class ImageQueryAnswer(str, Enum):
    YES = "YES"
    NO = "NO"
    UNKNOWN = "UNKNOWN"


class AlertStatus(str, Enum):
    OPEN = "open"
    ACK = "ack"
    RESOLVED = "resolved"


class AlertChannel(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    WEBHOOK = "webhook"


class EscalationStatus(str, Enum):
    OPEN = "open"
    ACK = "ack"
    RESOLVED = "resolved"
