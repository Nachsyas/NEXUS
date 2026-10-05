import datetime
import enum
import uuid
from typing import Any

import uuid6
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


def utc_now() -> datetime.datetime:
    return datetime.datetime.now(datetime.UTC)


def generate_uuid7() -> uuid.UUID:
    return uuid6.uuid7()


class ProjectStatus(enum.StrEnum):
    IDEA = "IDEA"
    PLANNING = "PLANNING"
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    ARCHIVED = "ARCHIVED"


class ProjectPriority(enum.StrEnum):
    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"


class Project(Base):
    """Canonical NEXUS Project entity representing persistent contextual boundaries."""

    __tablename__ = "projects"

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
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(
        String(50),
        default=ProjectStatus.PLANNING.value,
        nullable=False,
    )
    priority: Mapped[str | None] = mapped_column(
        String(50),
        default=ProjectPriority.NORMAL.value,
        nullable=True,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    progress: Mapped[int | None] = mapped_column(Integer, default=0, nullable=True)

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
    archived_at: Mapped[datetime.datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="projects")  # type: ignore[name-defined] # noqa: F821
    technologies: Mapped[list["ProjectTechnology"]] = relationship(
        "ProjectTechnology",
        back_populates="project",
        cascade="all, delete-orphan",
        order_by="ProjectTechnology.name",
        lazy="selectin",
    )

    __table_args__ = (
        UniqueConstraint("user_id", "slug", name="uq_projects_user_slug"),
        CheckConstraint(
            "progress >= 0 AND progress <= 100",
            name="chk_projects_progress_bounds",
        ),
        Index(
            "uq_projects_user_active",
            "user_id",
            unique=True,
            postgresql_where=(is_active == True),  # noqa: E712
        ),
    )


class ProjectTechnology(Base):
    """Canonical technology entry associated with a project context."""

    __tablename__ = "project_technologies"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=generate_uuid7,
    )
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[str | None] = mapped_column(String(50), nullable=True)
    version: Mapped[str | None] = mapped_column(String(50), nullable=True)
    tech_metadata: Mapped[dict[str, Any]] = mapped_column(
        "metadata",
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

    # Relationships
    project: Mapped["Project"] = relationship("Project", back_populates="technologies")

    __table_args__ = (
        UniqueConstraint("project_id", "name", name="uq_project_technologies_project_name"),
    )
