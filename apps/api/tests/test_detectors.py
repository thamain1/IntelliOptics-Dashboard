"""Tests for detector CRUD endpoints."""

from __future__ import annotations

import uuid

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from apps.api.app.models import Detector
from apps.api.app.models.enums import DetectorMode
from .factories import create_detector, create_user


def test_create_detector(client: TestClient, db_session: Session) -> None:
    user = create_user(db_session)

    payload = {
        "name": "Perimeter Watch",
        "mode": DetectorMode.BINARY.value,
        "query": "Alert when a person crosses the fence",
        "confidence_threshold": 0.7,
        "is_active": True,
        "created_by": user.public_id,
    }

    response = client.post("/v1/detectors", json=payload)
    assert response.status_code == 201
    data = response.json()

    assert data["name"] == payload["name"]
    assert data["mode"] == DetectorMode.BINARY.value
    assert data["created_by"] == user.public_id
    assert data["id"].startswith("det-")

    stored = db_session.get(Detector, uuid.UUID(data["id"].split("-", 1)[1]))
    assert stored is not None
    assert stored.name == payload["name"]


def test_list_detectors_returns_created_items(client: TestClient, db_session: Session) -> None:
    detector = create_detector(db_session)

    response = client.get("/v1/detectors")
    assert response.status_code == 200
    payload = response.json()

    assert isinstance(payload, list)
    assert len(payload) == 1
    item = payload[0]
    assert item["id"] == detector.public_id
    assert item["created_by"] == detector.creator.public_id


def test_get_detector_returns_404_for_unknown(client: TestClient) -> None:
    response = client.get("/v1/detectors/det-00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


def test_create_detector_requires_existing_user(client: TestClient, db_session: Session) -> None:
    payload = {
        "name": "Unknown Creator",
        "mode": DetectorMode.BINARY.value,
        "query": "Test",
        "confidence_threshold": 0.5,
        "is_active": True,
        "created_by": "usr-00000000-0000-0000-0000-000000000000",
    }

    response = client.post("/v1/detectors", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Creator not found"
