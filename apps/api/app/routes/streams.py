"""REST endpoints for managing video streams."""

from __future__ import annotations

import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..db import get_session
from ..models import Stream
from ..schemas import StreamCreate, StreamRead, StreamUpdate

router = APIRouter(prefix="/v1/streams", tags=["streams"])


def _parse_stream_public_id(stream_id: str) -> uuid.UUID:
    prefix = "str-"
    if not stream_id.startswith(prefix):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stream not found")
    identifier = stream_id[len(prefix) :]
    try:
        return uuid.UUID(identifier)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stream not found") from exc


def _serialize_stream(stream: Stream) -> StreamRead:
    return StreamRead(
        id=stream.public_id,
        name=stream.name,
        rtsp_url=stream.rtsp_url,
        zone_masks=stream.zone_masks,
        is_active=stream.is_active,
        created_at=stream.created_at,
        updated_at=stream.updated_at,
    )


@router.get("", response_model=List[StreamRead])
def list_streams(session: Session = Depends(get_session)) -> List[StreamRead]:
    """Return all configured streams ordered by creation time descending."""

    stmt = select(Stream).order_by(Stream.created_at.desc(), Stream.id.desc())
    streams = session.scalars(stmt).all()
    return [_serialize_stream(stream) for stream in streams]


@router.get("/{stream_id}", response_model=StreamRead)
def get_stream(stream_id: str, session: Session = Depends(get_session)) -> StreamRead:
    """Return a single stream by its public identifier."""

    internal_id = _parse_stream_public_id(stream_id)
    stmt = select(Stream).where(Stream.id == internal_id)
    stream = session.scalars(stmt).first()
    if stream is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stream not found")
    return _serialize_stream(stream)


@router.post("", response_model=StreamRead, status_code=status.HTTP_201_CREATED)
def create_stream(payload: StreamCreate, session: Session = Depends(get_session)) -> StreamRead:
    """Create a new stream configuration."""

    stream = Stream(
        name=payload.name,
        rtsp_url=payload.rtsp_url,
        zone_masks=payload.zone_masks,
        is_active=payload.is_active,
    )
    session.add(stream)
    session.commit()
    session.refresh(stream)
    return _serialize_stream(stream)


@router.patch("/{stream_id}", response_model=StreamRead)
def update_stream(stream_id: str, payload: StreamUpdate, session: Session = Depends(get_session)) -> StreamRead:
    """Partially update a stream with the provided fields."""

    internal_id = _parse_stream_public_id(stream_id)
    stmt = select(Stream).where(Stream.id == internal_id)
    stream = session.scalars(stmt).first()
    if stream is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stream not found")

    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(stream, field, value)

    session.add(stream)
    session.commit()
    session.refresh(stream)
    return _serialize_stream(stream)
