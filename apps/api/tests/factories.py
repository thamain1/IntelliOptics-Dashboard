"""Test data factories for the IntelliOptics API."""

from __future__ import annotations

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
    zone_masks: Optional[dict] = None,
    is_active: bool = True,
) -> Stream:
    """Persist a stream record suitable for associations."""

    stream = Stream(name=name, rtsp_url=rtsp_url, zone_masks=zone_masks, is_active=is_active)
    session.add(stream)
    session.commit()
    session.refresh(stream)
    return stream


__all__ = ["create_user", "create_detector", "create_stream"]
