import datetime
import enum
import uuid
from typing import Any

import uuid6
from pgvector.sqlalchemy import Vector
from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Float,
    ForeignKey,
    Index,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


def utc_now() -> datetime.datetime:
    return datetime.datetime.now(datetime.UTC)


def generate_uuid7() -> uuid.UUID:
    return uuid6.uuid7()


class MemoryType(enum.StrEnum):
    PERSONAL_FACT = "PERSONAL_FACT"
    PREFERENCE = "PREFERENCE"
    INTEREST = "INTEREST"
    SKILL = "SKILL"
    GOAL = "GOAL"
    PROJECT_FACT = "PROJECT_FACT"
    PROJECT_DECISION = "PROJECT_DECISION"
    PROJECT_PROGRESS = "PROJECT_PROGRESS"
    PROJECT_NEXT_ACTION = "PROJECT_NEXT_ACTION"
    BEHAVIOR_PATTERN = "BEHAVIOR_PATTERN"


PROJECT_SCOPED_MEMORY_TYPES = {
    MemoryType.PROJECT_FACT,
    MemoryType.PROJECT_DECISION,
    MemoryType.PROJECT_PROGRESS,
    MemoryType.PROJECT_NEXT_ACTION,
}


class MemoryStatus(enum.StrEnum):
    ACTIVE = "ACTIVE"
    SUPERSEDED = "SUPERSEDED"
    EXPIRED = "EXPIRED"
    FORGOTTEN = "FORGOTTEN"
    PENDING_CONFIRMATION = "PENDING_CONFIRMATION"


class MemorySensitivity(enum.StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    RESTRICTED = "RESTRICTED"


class MemorySourceType(enum.StrEnum):
    CONVERSATION = "CONVERSATION"
    USER_EXPLICIT = "USER_EXPLICIT"
    PROJECT_UPDATE = "PROJECT_UPDATE"
    DOCUMENT = "DOCUMENT"
    SYSTEM_INFERENCE = "SYSTEM_INFERENCE"
    BEHAVIORAL_INFERENCE = "BEHAVIORAL_INFERENCE"


class Memory(Base):
    """Canonical NEXUS Memory entity representing structured, qualified personal and project meaning."""

    __tablename__ = "memories"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=generate_uuid7,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    project_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    memory_type: Mapped[str] = mapped_column(String(50), nullable=False)
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    predicate: Mapped[str] = mapped_column(String(255), nullable=False)
    identity_subject: Mapped[str] = mapped_column(String(255), nullable=False)
    identity_predicate: Mapped[str] = mapped_column(String(255), nullable=False)
    value_text: Mapped[str] = mapped_column(Text, nullable=False)
    value_json: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    embedding = mapped_column(Vector(), nullable=True)

    importance: Mapped[float] = mapped_column(Float, default=0.5, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    sensitivity: Mapped[str] = mapped_column(
        String(20),
        default=MemorySensitivity.LOW.value,
        nullable=False,
    )
    source_type: Mapped[str] = mapped_column(
        String(50),
        default=MemorySourceType.USER_EXPLICIT.value,
        nullable=False,
    )
    source_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(
        String(50),
        default=MemoryStatus.ACTIVE.value,
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
    expires_at: Mapped[datetime.datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    superseded_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("memories.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="memories")  # type: ignore[name-defined] # noqa: F821
    project: Mapped["Project | None"] = relationship("Project", back_populates="memories")  # type: ignore[name-defined] # noqa: F821
    superseding_memory: Mapped["Memory | None"] = relationship(
        "Memory",
        remote_side=[id],
        foreign_keys=[superseded_by],
    )

    __table_args__ = (
        CheckConstraint(
            "importance >= 0.0 AND importance <= 1.0",
            name="chk_memories_importance_bounds",
        ),
        CheckConstraint(
            "confidence >= 0.0 AND confidence <= 1.0",
            name="chk_memories_confidence_bounds",
        ),
        Index("ix_memories_user_status", "user_id", "status"),
        Index("ix_memories_user_project_status", "user_id", "project_id", "status"),
        Index("ix_memories_user_type_status", "user_id", "memory_type", "status"),
        Index(
            "ix_memories_identity_lookup",
            "user_id",
            "project_id",
            "memory_type",
            "identity_subject",
            "identity_predicate",
            "status",
        ),
        Index("ix_memories_expires_at", "expires_at"),
        Index("ix_memories_user_updated_at", "user_id", "updated_at"),
    )
