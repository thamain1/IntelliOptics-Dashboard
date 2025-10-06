"""Tests for the image query endpoints."""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from apps.api.app.models import ImageQuery
from apps.api.app.models.enums import ImageQueryAnswer
from .factories import create_detector, create_stream


def test_create_image_query(client: TestClient, db_session: Session) -> None:
    detector = create_detector(db_session)
    stream = create_stream(db_session)

    payload = {
        "detector_id": detector.public_id,
        "rtsp_source_id": stream.public_id,
        "snapshot_url": "https://example.blob.core.windows.net/images/test.jpg",
    }

    response = client.post("/v1/image-queries", json=payload)
    assert response.status_code == 201
    data = response.json()

    assert data["detector_id"] == detector.public_id
    assert data["rtsp_source_id"] == stream.public_id
    assert data["snapshot_url"] == payload["snapshot_url"]

    stored = db_session.query(ImageQuery).one()
    assert stored.snapshot_url == payload["snapshot_url"]


def test_create_image_query_requires_known_detector(client: TestClient) -> None:
    payload = {
        "detector_id": "det-00000000-0000-0000-0000-000000000000",
        "snapshot_url": "https://example.blob.core.windows.net/images/test.jpg",
    }

    response = client.post("/v1/image-queries", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Detector not found"


def test_read_image_query(client: TestClient, db_session: Session) -> None:
    detector = create_detector(db_session)
    image_query = ImageQuery(detector=detector, snapshot_url="https://example.com/image.jpg")
    db_session.add(image_query)
    db_session.commit()

    response = client.get(f"/v1/image-queries/{image_query.public_id}")
    assert response.status_code == 200
    data = response.json()

    assert data["id"] == image_query.public_id
    assert data["detector_id"] == detector.public_id
    assert data["answer"] is None


def test_wait_for_image_query_returns_pending(client: TestClient, db_session: Session) -> None:
    detector = create_detector(db_session)
    image_query = ImageQuery(detector=detector, snapshot_url="https://example.com/image.jpg")
    db_session.add(image_query)
    db_session.commit()

    response = client.get(f"/v1/image-queries/{image_query.public_id}/wait?timeout=0")
    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "pending"
    assert data["result"] is None


def test_wait_for_image_query_returns_complete(client: TestClient, db_session: Session) -> None:
    detector = create_detector(db_session)
    image_query = ImageQuery(
        detector=detector,
        snapshot_url="https://example.com/image.jpg",
        answer=ImageQueryAnswer.YES,
        answer_score=0.9,
        processed_at=datetime.now(tz=timezone.utc),
    )
    db_session.add(image_query)
    db_session.commit()

    response = client.get(f"/v1/image-queries/{image_query.public_id}/wait")
    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "complete"
    assert data["result"]["id"] == image_query.public_id
    assert data["result"]["answer"] == ImageQueryAnswer.YES.value
