"""Read-only alert endpoints."""

from __future__ import annotations

import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from ..db import get_session
from ..models import Alert
from ..schemas import AlertRead

router = APIRouter(prefix="/v1/alerts", tags=["alerts"])


def _parse_alert_public_id(alert_id: str) -> uuid.UUID:
    prefix = "alrt-"
    if not alert_id.startswith(prefix):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alert not found")
    identifier = alert_id[len(prefix) :]
    try:
        return uuid.UUID(identifier)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alert not found") from exc


def _serialize_alert(alert: Alert) -> AlertRead:
    detector = alert.detector
    image_query = alert.image_query
    if detector is None or image_query is None:
        raise RuntimeError("Alert is missing required relationships")
    return AlertRead(
        id=alert.public_id,
        detector_id=detector.public_id,
        image_query_id=image_query.public_id,
        status=alert.status,
        message=alert.message,
        channel=alert.channel,
        created_at=alert.created_at,
        updated_at=alert.updated_at,
        resolved_at=alert.resolved_at,
    )


@router.get("/events/recent", response_model=List[AlertRead])
def recent_alerts(
    limit: int = Query(20, ge=1, le=100),
    session: Session = Depends(get_session),
) -> List[AlertRead]:
    """Return the most recent alerts limited by the provided size."""

    stmt = (
        select(Alert)
        .options(selectinload(Alert.detector), selectinload(Alert.image_query))
        .order_by(Alert.created_at.desc())
        .limit(limit)
    )
    alerts = session.scalars(stmt).all()
    return [_serialize_alert(alert) for alert in alerts]


@router.get("/{alert_id}", response_model=AlertRead)
def get_alert(alert_id: str, session: Session = Depends(get_session)) -> AlertRead:
    """Return a single alert by its public identifier."""

    internal_id = _parse_alert_public_id(alert_id)
    stmt = (
        select(Alert)
        .options(selectinload(Alert.detector), selectinload(Alert.image_query))
        .where(Alert.id == internal_id)
    )
    alert = session.scalars(stmt).first()
    if alert is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alert not found")
    return _serialize_alert(alert)


__all__ = ["router"]
