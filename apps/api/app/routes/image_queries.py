"""REST endpoints for managing image queries."""

from __future__ import annotations

import time
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..config import settings
from ..db import get_session
from ..models import Detector, ImageQuery, Stream
from ..schemas import ImageQueryCreate, ImageQueryRead, ImageQueryWaitResponse

router = APIRouter(prefix="/v1/image-queries", tags=["image-queries"])


def _parse_public_identifier(value: str, prefix: str, not_found: str) -> uuid.UUID:
    if not value.startswith(prefix):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=not_found)
    identifier = value[len(prefix) :]
    try:
        return uuid.UUID(identifier)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=not_found) from exc


def _serialize_image_query(image_query: ImageQuery) -> ImageQueryRead:
    detector = image_query.detector
    detector_id = detector.public_id if detector else None
    if detector_id is None:
        raise RuntimeError("ImageQuery is missing detector relationship")

    stream = image_query.stream
    stream_id: Optional[str] = stream.public_id if stream else None

    return ImageQueryRead(
        id=image_query.public_id,
        detector_id=detector_id,
        rtsp_source_id=stream_id,
        snapshot_url=image_query.snapshot_url,
        answer=image_query.answer,
        answer_score=image_query.answer_score,
        created_at=image_query.created_at,
        processed_at=image_query.processed_at,
    )


def _get_image_query_or_404(image_query_id: str, session: Session) -> ImageQuery:
    internal_id = _parse_public_identifier(image_query_id, "iq-", "Image query not found")
    stmt = select(ImageQuery).where(ImageQuery.id == internal_id)
    instance = session.scalars(stmt).first()
    if instance is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image query not found")
    return instance


@router.post("", response_model=ImageQueryRead, status_code=status.HTTP_201_CREATED)
def create_image_query(
    payload: ImageQueryCreate, session: Session = Depends(get_session)
) -> ImageQueryRead:
    """Create a new image query associated with a detector and optional stream."""

    try:
        detector_uuid = payload.detector_uuid()
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc

    detector_stmt = select(Detector).where(Detector.id == detector_uuid)
    detector = session.scalars(detector_stmt).first()
    if detector is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Detector not found")

    stream_obj: Optional[Stream] = None
    if payload.rtsp_source_id is not None:
        try:
            stream_uuid = payload.stream_uuid()
        except ValueError as exc:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
        stream_stmt = select(Stream).where(Stream.id == stream_uuid)
        stream_obj = session.scalars(stream_stmt).first()
        if stream_obj is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Stream not found")

    image_query = ImageQuery(
        detector=detector,
        stream=stream_obj,
        snapshot_url=str(payload.snapshot_url),
    )
    session.add(image_query)
    session.commit()
    session.refresh(image_query)
    return _serialize_image_query(image_query)


@router.get("/{image_query_id}", response_model=ImageQueryRead)
def read_image_query(image_query_id: str, session: Session = Depends(get_session)) -> ImageQueryRead:
    """Return a single image query record."""

    image_query = _get_image_query_or_404(image_query_id, session)
    return _serialize_image_query(image_query)


@router.get("/{image_query_id}/wait", response_model=ImageQueryWaitResponse)
def wait_for_image_query(
    image_query_id: str,
    session: Session = Depends(get_session),
    timeout: float | None = None,
    poll: float | None = None,
) -> ImageQueryWaitResponse:
    """Poll for completion of an image query returning when an answer is available."""

    wait_timeout = settings.image_query_wait_timeout_seconds if timeout is None else max(timeout, 0.0)
    poll_interval = settings.image_query_wait_poll_seconds if poll is None else max(poll, 0.0)
    deadline = time.monotonic() + wait_timeout

    while True:
        image_query = _get_image_query_or_404(image_query_id, session)
        if image_query.answer is not None and image_query.processed_at is not None:
            return ImageQueryWaitResponse(status="complete", result=_serialize_image_query(image_query))
        now = time.monotonic()
        if now >= deadline:
            return ImageQueryWaitResponse(status="pending", result=None)
        session.expire(image_query)
        remaining = min(poll_interval, deadline - now)
        if remaining <= 0:
            return ImageQueryWaitResponse(status="pending", result=None)
        time.sleep(remaining)
