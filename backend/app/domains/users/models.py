import datetime
import uuid
from typing import Any

import uuid6
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


def utc_now() -> datetime.datetime:
    return datetime.datetime.now(datetime.UTC)


def generate_uuid7() -> uuid.UUID:
    return uuid6.uuid7()


class User(Base):
    """Core NEXUS User entity representing internal system identity."""

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=generate_uuid7,
    )
    display_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="ACTIVE", nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
    )
    last_login_at: Mapped[datetime.datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Relationships
    preferences: Mapped["UserPreference | None"] = relationship(
        "UserPreference",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    auth_identities: Mapped[list["AuthIdentity"]] = relationship(  # type: ignore[name-defined] # noqa: F821
        "AuthIdentity",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    sessions: Mapped[list["Session"]] = relationship(  # type: ignore[name-defined] # noqa: F821
        "Session",
        back_populates="user",
        cascade="all, delete-orphan",
    )


class UserPreference(Base):
    """Personalization and interaction preferences for a NEXUS user."""

    __tablename__ = "user_preferences"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=generate_uuid7,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )
    language: Mapped[str] = mapped_column(String(10), default="en", nullable=False)
    response_detail: Mapped[str] = mapped_column(String(50), default="CONCISE", nullable=False)
    interaction_style: Mapped[str] = mapped_column(String(50), default="DIRECT", nullable=False)
    proactivity_level: Mapped[str] = mapped_column(String(50), default="MEDIUM", nullable=False)

    # Deferred references for future milestones (M2 Projects, M6 Devices)
    default_project_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )
    default_device_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )
    storage_mode: Mapped[str | None] = mapped_column(String(50), nullable=True)
    research_update_frequency: Mapped[str | None] = mapped_column(String(50), nullable=True)

    notification_preferences: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        default=dict,
        nullable=False,
    )
    voice_settings: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        default=dict,
        nullable=False,
    )

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
    )

    user: Mapped["User"] = relationship("User", back_populates="preferences")
