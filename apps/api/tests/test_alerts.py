"""Tests for the alert endpoints."""

from __future__ import annotations

from datetime import timedelta

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from apps.api.app.models.enums import AlertStatus
from .factories import create_alert


def test_get_alert_by_id(client: TestClient, db_session: Session) -> None:
    alert = create_alert(db_session)

    response = client.get(f"/v1/alerts/{alert.public_id}")
    assert response.status_code == 200
    data = response.json()

    assert data["id"] == alert.public_id
    assert data["detector_id"] == alert.detector.public_id
    assert data["status"] == alert.status


def test_get_alert_not_found(client: TestClient) -> None:
    response = client.get("/v1/alerts/alrt-00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


def test_recent_alerts_ordering(client: TestClient, db_session: Session) -> None:
    older = create_alert(db_session, message="Older alert")
    newer = create_alert(db_session, message="Newer alert", status=AlertStatus.ACK)

    older.created_at = older.created_at - timedelta(minutes=5)
    db_session.add(older)
    db_session.commit()

    response = client.get("/v1/alerts/events/recent?limit=2")
    assert response.status_code == 200
    payload = response.json()

    assert len(payload) == 2
    assert [item["message"] for item in payload] == ["Newer alert", "Older alert"]
    assert payload[0]["status"] == AlertStatus.ACK
