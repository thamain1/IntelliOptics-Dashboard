"""REST endpoints for managing detectors."""

from __future__ import annotations

import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..db import get_session
from ..models import Detector, User
from ..schemas import DetectorCreate, DetectorRead

router = APIRouter(prefix="/v1/detectors", tags=["detectors"])


def _parse_detector_public_id(detector_id: str) -> uuid.UUID:
    prefix = "det-"
    if not detector_id.startswith(prefix):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Detector not found")
    identifier = detector_id[len(prefix) :]
    try:
        return uuid.UUID(identifier)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Detector not found") from exc


def _serialize_detector(detector: Detector) -> DetectorRead:
    creator = detector.creator
    created_by = creator.public_id if creator else None
    if created_by is None:
        raise RuntimeError("Detector is missing a creator relationship")
    return DetectorRead(
        id=detector.public_id,
        name=detector.name,
        mode=detector.mode,
        query=detector.query,
        confidence_threshold=detector.confidence_threshold,
        is_active=detector.is_active,
        created_by=created_by,
        created_at=detector.created_at,
        updated_at=detector.updated_at,
    )


@router.get("", response_model=List[DetectorRead])
def list_detectors(session: Session = Depends(get_session)) -> List[DetectorRead]:
    """Return all detectors ordered by creation time descending."""

    stmt = select(Detector).order_by(Detector.created_at.desc())
    detectors = session.scalars(stmt).all()
    return [_serialize_detector(detector) for detector in detectors]


@router.get("/{detector_id}", response_model=DetectorRead)
def get_detector(detector_id: str, session: Session = Depends(get_session)) -> DetectorRead:
    """Return a single detector by its public identifier."""

    internal_id = _parse_detector_public_id(detector_id)
    stmt = select(Detector).where(Detector.id == internal_id)
    detector = session.scalars(stmt).first()
    if detector is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Detector not found")
    return _serialize_detector(detector)


@router.post("", response_model=DetectorRead, status_code=status.HTTP_201_CREATED)
def create_detector(payload: DetectorCreate, session: Session = Depends(get_session)) -> DetectorRead:
    """Create a new detector owned by the provided user."""

    try:
        creator_uuid = payload.creator_uuid()
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc

    user_stmt = select(User).where(User.id == creator_uuid)
    creator = session.scalars(user_stmt).first()
    if creator is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Creator not found")

    detector = Detector(
        name=payload.name,
        mode=payload.mode,
        query=payload.query,
        confidence_threshold=payload.confidence_threshold,
        is_active=payload.is_active,
        creator=creator,
    )
    session.add(detector)
    session.commit()
    session.refresh(detector)
    return _serialize_detector(detector)
