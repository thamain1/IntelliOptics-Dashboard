"""Tests covering the /v1/streams endpoints."""

from __future__ import annotations

from datetime import timedelta

from fastapi.testclient import TestClient

from apps.api.tests.factories import create_stream


def test_list_streams_returns_streams(client: TestClient, db_session) -> None:
    first = create_stream(db_session, name="Loading Dock")
    first.created_at = first.created_at - timedelta(minutes=5)
    db_session.add(first)
    db_session.commit()
    db_session.refresh(first)

    second = create_stream(db_session, name="Front Door")

    response = client.get("/v1/streams")
    assert response.status_code == 200
    body = response.json()
    # Streams should be ordered by creation time descending
    assert [item["id"] for item in body] == [second.public_id, first.public_id]


def test_create_stream_persists_record(client: TestClient, db_session) -> None:
    payload = {
        "name": "Warehouse Cam",
        "rtsp_url": "rtsp://example.com/warehouse",
        "zone_masks": {"zone": "A"},
        "is_active": True,
    }

    response = client.post("/v1/streams", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["rtsp_url"] == payload["rtsp_url"]
    assert data["zone_masks"] == payload["zone_masks"]
    assert data["is_active"] is True

    get_response = client.get(f"/v1/streams/{data['id']}")
    assert get_response.status_code == 200
    assert get_response.json()["name"] == payload["name"]


def test_update_stream_applies_partial_changes(client: TestClient, db_session) -> None:
    stream = create_stream(db_session, name="Old Name", zone_masks={"mask": 1})

    response = client.patch(
        f"/v1/streams/{stream.public_id}",
        json={"name": "New Name", "zone_masks": None, "is_active": False},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["name"] == "New Name"
    assert payload["zone_masks"] is None
    assert payload["is_active"] is False


def test_get_stream_returns_404_for_unknown_id(client: TestClient) -> None:
    response = client.get("/v1/streams/str-00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


def test_update_stream_returns_404_for_unknown_id(client: TestClient) -> None:
    response = client.patch(
        "/v1/streams/str-00000000-0000-0000-0000-000000000000",
        json={"name": "Updated"},
    )
    assert response.status_code == 404
