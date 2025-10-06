"""SQLAlchemy model for platform users."""

from __future__ import annotations

from typing import List

from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .enums import UserRole
from .mixins import BaseModel


class User(BaseModel):
    """Represents an authenticated IntelliOptics user."""

    __tablename__ = "users"
    public_id_prefix = "usr"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole, name="user_role"), nullable=False)

    detectors: Mapped[List["Detector"]] = relationship(back_populates="creator", cascade="all,delete")
    escalations: Mapped[List["Escalation"]] = relationship(back_populates="assignee")
    annotations: Mapped[List["Annotation"]] = relationship(back_populates="annotator")

    def __repr__(self) -> str:  # pragma: no cover - repr helper
        return f"User(id={self.id}, email={self.email!r}, role={self.role})"


from .annotation import Annotation  # noqa: E402
from .detector import Detector  # noqa: E402  # circular import resolution
from .escalation import Escalation  # noqa: E402
