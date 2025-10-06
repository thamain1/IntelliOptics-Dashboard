"""Test data factories for the IntelliOptics API."""

from __future__ import annotations

import uuid

from sqlalchemy.orm import Session

from apps.api.app.models import Alert, Detector, ImageQuery, Stream, User
from apps.api.app.models.enums import (
    AlertChannel,
    AlertStatus,
    DetectorMode,
    ImageQueryAnswer,
    UserRole,
)


def create_user(
    session: Session,
    email: str | None = None,
    role: UserRole = UserRole.ADMIN,
) -> User:
    """Persist and return a user instance for tests."""

    chosen_email = email or f"owner-{uuid.uuid4().hex}@example.com"
    user = User(email=chosen_email, role=role, password_hash="x")
from typing import Optional

from sqlalchemy.orm import Session

from apps.api.app.models import Detector, Stream, User
from apps.api.app.models.enums import DetectorMode, UserRole


def create_user(session: Session, email: str = "owner@example.com", role: UserRole = UserRole.ADMIN) -> User:
    """Persist and return a user instance for tests."""

    user = User(email=email, role=role, password_hash="x")
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def create_detector(
    session: Session,
    *,
    creator: User | None = None,
    creator: Optional[User] = None,
    name: str = "Perimeter Watch",
    query: str = "Alert when a person crosses the fence",
    mode: DetectorMode = DetectorMode.BINARY,
    confidence_threshold: float = 0.6,
    is_active: bool = True,
) -> Detector:
    """Persist a detector for testing purposes."""

    owner = creator or create_user(session)
    detector = Detector(
        name=name,
        mode=mode,
        query=query,
        confidence_threshold=confidence_threshold,
        is_active=is_active,
        creator=owner,
    )
    session.add(detector)
    session.commit()
    session.refresh(detector)
    return detector


def create_stream(
    session: Session,
    *,
    name: str = "Loading Dock",
    rtsp_url: str = "rtsp://camera.example/stream",
    zone_masks: dict | None = None,
    zone_masks: Optional[dict] = None,
    is_active: bool = True,
) -> Stream:
    """Persist a stream record suitable for associations."""

    stream = Stream(name=name, rtsp_url=rtsp_url, zone_masks=zone_masks, is_active=is_active)
    session.add(stream)
    session.commit()
    session.refresh(stream)
    return stream


def create_image_query(
    session: Session,
    *,
    detector: Detector | None = None,
    stream: Stream | None = None,
    snapshot_url: str = "https://example.blob.core.windows.net/images/sample.jpg",
    answer: ImageQueryAnswer | None = None,
    answer_score: float | None = None,
) -> ImageQuery:
    """Persist an image query associated with an existing detector/stream."""

    bound_detector = detector or create_detector(session)
    bound_stream = stream or create_stream(session)
    image_query = ImageQuery(
        detector=bound_detector,
        stream=bound_stream,
        snapshot_url=snapshot_url,
        answer=answer,
        answer_score=answer_score,
    )
    session.add(image_query)
    session.commit()
    session.refresh(image_query)
    return image_query


def create_alert(
    session: Session,
    *,
    detector: Detector | None = None,
    image_query: ImageQuery | None = None,
    status: AlertStatus = AlertStatus.OPEN,
    message: str = "Suspicious activity detected",
    channel: AlertChannel = AlertChannel.EMAIL,
) -> Alert:
    """Persist an alert referencing an image query."""

    bound_image_query = image_query or create_image_query(session, detector=detector)
    alert = Alert(
        detector=bound_image_query.detector,
        image_query=bound_image_query,
        status=status,
        message=message,
        channel=channel,
    )
    session.add(alert)
    session.commit()
    session.refresh(alert)
    return alert


__all__ = [
    "create_alert",
    "create_detector",
    "create_image_query",
    "create_stream",
    "create_user",
]
__all__ = ["create_user", "create_detector", "create_stream"]
