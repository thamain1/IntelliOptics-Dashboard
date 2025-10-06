"""Tests for the SQLAlchemy metadata and helper properties."""

from __future__ import annotations

import uuid

from sqlalchemy import create_engine, inspect

from apps.api.app.db import Base
from apps.api.app.models import (
    Alert,
    Annotation,
    Detector,
    Escalation,
    ImageQuery,
    Stream,
    User,
)

# Touch the model classes to ensure SQLAlchemy registers them with the metadata.
_ = (Alert, Annotation, Detector, Escalation, ImageQuery, Stream, User)
from apps.api.app.models.enums import AlertChannel, AlertStatus, DetectorMode, ImageQueryAnswer, UserRole


def test_metadata_creates_expected_tables() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    inspector = inspect(engine)
    tables = set(inspector.get_table_names())
    assert {
        "users",
        "detectors",
        "streams",
        "image_queries",
        "alerts",
        "escalations",
        "annotations",
    }.issubset(tables)


def test_public_id_generation() -> None:
    user = User(id=uuid.uuid4(), email="user@example.com", password_hash=None, role=UserRole.ADMIN)
    detector = Detector(
        id=uuid.uuid4(),
        name="Test Detector",
        mode=DetectorMode.BINARY,
        query="detect defects",
        confidence_threshold=0.5,
        is_active=True,
        created_by_id=user.id,
    )
    image_query = ImageQuery(
        id=uuid.uuid4(),
        detector_id=detector.id,
        snapshot_url="https://example.com/blob.jpg",
    )
    alert = Alert(
        id=uuid.uuid4(),
        detector_id=detector.id,
        image_query_id=image_query.id,
        status=AlertStatus.OPEN,
        message="test alert",
        channel=AlertChannel.EMAIL,
    )
    annotation = Annotation(
        id=uuid.uuid4(),
        image_query_id=image_query.id,
        label_json={"boxes": []},
    )

    assert user.public_id.startswith("usr-")
    assert detector.public_id.startswith("det-")
    assert image_query.public_id.startswith("iq-")
    assert alert.public_id.startswith("alrt-")
    assert annotation.public_id.startswith("ann-")


def test_enum_values_match_spec() -> None:
    assert {role.value for role in UserRole} == {"admin", "analyst", "viewer"}
    assert {mode.value for mode in DetectorMode} == {"binary", "multiclass"}
    assert {answer.value for answer in ImageQueryAnswer} == {"YES", "NO", "UNKNOWN"}
    assert {status.value for status in AlertStatus} == {"open", "ack", "resolved"}
    assert {channel.value for channel in AlertChannel} == {"email", "sms", "webhook"}
