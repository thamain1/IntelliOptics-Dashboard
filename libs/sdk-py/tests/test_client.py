from __future__ import annotations

import asyncio
from typing import Any, Dict, List, Tuple

import httpx
import pytest

from intellioptics.client import IntelliOpticsAsyncClient, IntelliOpticsClient, IntelliOpticsError
from intellioptics.models import DetectorCreate

_ResponseKey = Tuple[str, str]
_ResponseValue = Tuple[int, Any]


class _Responder:
    def __init__(self) -> None:
        self._responses: Dict[_ResponseKey, List[_ResponseValue]] = {}

    def add(self, method: str, path: str, json: Any, status_code: int = 200) -> None:
        key = (method.upper(), path)
        self._responses.setdefault(key, []).append((status_code, json))

    def __call__(self, request: httpx.Request) -> httpx.Response:
        key = (request.method.upper(), request.url.path)
        queue = self._responses.get(key)
        if queue:
            status, payload = queue.pop(0)
        else:
            status, payload = 404, {"detail": "not found"}
        return httpx.Response(status, json=payload, request=request)


@pytest.fixture()
def transport() -> httpx.MockTransport:
    responder = _Responder()
    transport = httpx.MockTransport(responder)
    transport.responder = responder  # type: ignore[attr-defined]
    return transport


def test_create_and_list_detectors(transport: httpx.MockTransport) -> None:
    responder = transport.responder  # type: ignore[attr-defined]
    responder.add(
        "GET",
        "/v1/detectors",
        json=[
            {
                "id": "det-1",
                "name": "Demo",
                "mode": "binary",
                "query": "demo",
                "confidence_threshold": 0.5,
                "is_active": True,
            }
        ],
    )
    responder.add(
        "POST",
        "/v1/detectors",
        json={
            "id": "det-2",
            "name": "New",
            "mode": "binary",
            "query": "door",
            "confidence_threshold": 0.6,
            "is_active": True,
        },
    )

    client = IntelliOpticsClient("https://api.local", transport=transport)
    detectors = client.list_detectors()
    assert detectors[0].id == "det-1"

    created = client.create_detector(
        DetectorCreate(name="New", mode="binary", query="door", confidence_threshold=0.6)
    )
    assert created.id == "det-2"


def test_wait_for_image_query_success(transport: httpx.MockTransport) -> None:
    responder = transport.responder  # type: ignore[attr-defined]
    responder.add("GET", "/v1/image-queries/iq-1/wait", json={"id": "iq-1"}, status_code=200)
    responder.add(
        "GET",
        "/v1/image-queries/iq-1/wait",
        json={"id": "iq-1", "answer": "YES", "score": 0.9},
        status_code=200,
    )

    sleep_calls = []

    def fake_sleep(_: float) -> None:
        sleep_calls.append(True)

    client = IntelliOpticsClient("https://api.local", transport=transport)
    result = client.wait_for_image_query("iq-1", poll_interval=0.01, timeout=0.1, sleep_fn=fake_sleep)
    assert result.answer == "YES"
    assert sleep_calls  # ensure we actually waited


def test_wait_for_image_query_timeout(transport: httpx.MockTransport) -> None:
    responder = transport.responder  # type: ignore[attr-defined]
    responder.add("GET", "/v1/image-queries/iq-1/wait", json={"id": "iq-1"}, status_code=200)

    client = IntelliOpticsClient("https://api.local", transport=transport)
    with pytest.raises(IntelliOpticsError):
        client.wait_for_image_query("iq-1", poll_interval=0.0, timeout=0.0)


def test_async_health(transport: httpx.MockTransport) -> None:
    responder = transport.responder  # type: ignore[attr-defined]
    responder.add("GET", "/health", json={"status": "ok"}, status_code=200)

    async def runner() -> None:
        async with IntelliOpticsAsyncClient("https://api.local", transport=transport) as client:
            assert await client.health() is True

    asyncio.run(runner())
