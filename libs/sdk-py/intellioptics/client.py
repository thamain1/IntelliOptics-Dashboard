"""Minimal IntelliOptics API client used by the dashboard monorepo."""

from __future__ import annotations

import asyncio
import time
from typing import Awaitable, Callable, Optional, Sequence

import httpx

from .models import (
    AlertEvent,
    Detector,
    DetectorCreate,
    ImageQuery,
    ImageQueryResult,
    parse_alerts,
    parse_detectors,
)

USER_AGENT = "intellioptics-sdk/0.1"


class IntelliOpticsError(RuntimeError):
    """Base error raised by the SDK."""


class IntelliOpticsClient:
    """Synchronous client for interacting with the IntelliOptics API."""

    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        *,
        timeout: float = 10.0,
        transport: Optional[httpx.BaseTransport] = None,
    ) -> None:
        headers = {"User-Agent": USER_AGENT}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        self._client = httpx.Client(
            base_url=base_url.rstrip("/"),
            timeout=timeout,
            headers=headers,
            transport=transport,
        )

    def close(self) -> None:
        self._client.close()

    def health(self) -> bool:
        response = self._client.get("/health")
        if response.status_code == 200:
            return True
        if response.status_code == 503:
            return False
        raise IntelliOpticsError(f"Unexpected status from /health: {response.status_code}")

    def list_detectors(self) -> Sequence[Detector]:
        response = self._client.get("/v1/detectors")
        response.raise_for_status()
        return parse_detectors(response.json())

    def create_detector(self, detector: DetectorCreate) -> Detector:
        response = self._client.post("/v1/detectors", json=detector.to_payload())
        response.raise_for_status()
        return Detector.from_dict(response.json())

    def get_detector(self, detector_id: str) -> Detector:
        response = self._client.get(f"/v1/detectors/{detector_id}")
        response.raise_for_status()
        return Detector.from_dict(response.json())

    def submit_image_query(
        self,
        detector_id: str,
        *,
        image_bytes: Optional[bytes] = None,
        snapshot_url: Optional[str] = None,
    ) -> ImageQuery:
        payload = {"detector_id": detector_id}
        files = None
        if image_bytes is not None:
            files = {"file": ("snapshot.jpg", image_bytes, "image/jpeg")}
        if snapshot_url is not None:
            payload["snapshot_url"] = snapshot_url
        response = self._client.post("/v1/image-queries", data=payload, files=files)
        response.raise_for_status()
        return ImageQuery.from_dict(response.json())

    def wait_for_image_query(
        self,
        query_id: str,
        *,
        poll_interval: float = 1.0,
        timeout: float = 30.0,
        sleep_fn: Callable[[float], None] = time.sleep,
    ) -> ImageQueryResult:
        deadline = time.monotonic() + timeout
        while True:
            response = self._client.get(f"/v1/image-queries/{query_id}/wait")
            if response.status_code == 404:
                raise IntelliOpticsError(f"Image query {query_id} not found")
            response.raise_for_status()
            payload = response.json()
            if payload.get("answer"):
                return ImageQueryResult.from_dict(payload)
            if time.monotonic() >= deadline:
                raise IntelliOpticsError("Timed out waiting for image query result")
            sleep_fn(poll_interval)

    def recent_alerts(self, limit: int = 20) -> Sequence[AlertEvent]:
        response = self._client.get("/v1/alerts/events/recent", params={"limit": limit})
        response.raise_for_status()
        return parse_alerts(response.json())

    def __enter__(self) -> "IntelliOpticsClient":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()


class IntelliOpticsAsyncClient:
    """Async variant of :class:`IntelliOpticsClient`."""

    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        *,
        timeout: float = 10.0,
        transport: Optional[httpx.AsyncBaseTransport] = None,
    ) -> None:
        headers = {"User-Agent": USER_AGENT}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        self._client = httpx.AsyncClient(
            base_url=base_url.rstrip("/"),
            timeout=timeout,
            headers=headers,
            transport=transport,
        )

    async def close(self) -> None:
        await self._client.aclose()

    async def health(self) -> bool:
        response = await self._client.get("/health")
        if response.status_code == 200:
            return True
        if response.status_code == 503:
            return False
        raise IntelliOpticsError(f"Unexpected status from /health: {response.status_code}")

    async def list_detectors(self) -> Sequence[Detector]:
        response = await self._client.get("/v1/detectors")
        response.raise_for_status()
        return parse_detectors(response.json())

    async def create_detector(self, detector: DetectorCreate) -> Detector:
        response = await self._client.post("/v1/detectors", json=detector.to_payload())
        response.raise_for_status()
        return Detector.from_dict(response.json())

    async def submit_image_query(
        self,
        detector_id: str,
        *,
        image_bytes: Optional[bytes] = None,
        snapshot_url: Optional[str] = None,
    ) -> ImageQuery:
        payload = {"detector_id": detector_id}
        files = None
        if image_bytes is not None:
            files = {"file": ("snapshot.jpg", image_bytes, "image/jpeg")}
        if snapshot_url is not None:
            payload["snapshot_url"] = snapshot_url
        response = await self._client.post("/v1/image-queries", data=payload, files=files)
        response.raise_for_status()
        return ImageQuery.from_dict(response.json())

    async def wait_for_image_query(
        self,
        query_id: str,
        *,
        poll_interval: float = 1.0,
        timeout: float = 30.0,
        sleep_fn: Callable[[float], Awaitable[None]] = asyncio.sleep,
    ) -> ImageQueryResult:
        deadline = time.monotonic() + timeout
        while True:
            response = await self._client.get(f"/v1/image-queries/{query_id}/wait")
            if response.status_code == 404:
                raise IntelliOpticsError(f"Image query {query_id} not found")
            response.raise_for_status()
            payload = response.json()
            if payload.get("answer"):
                return ImageQueryResult.from_dict(payload)
            if time.monotonic() >= deadline:
                raise IntelliOpticsError("Timed out waiting for image query result")
            await sleep_fn(poll_interval)

    async def recent_alerts(self, limit: int = 20) -> Sequence[AlertEvent]:
        response = await self._client.get("/v1/alerts/events/recent", params={"limit": limit})
        response.raise_for_status()
        return parse_alerts(response.json())

    async def __aenter__(self) -> "IntelliOpticsAsyncClient":
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.close()
