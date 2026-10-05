"""Create projects and project_technologies tables and add default_project_id FK.

Revision ID: 0003_projects_and_technologies
Revises: 0002_identity_and_sessions
Create Date: 2026-10-05 07:15:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0003_projects_and_technologies"
down_revision: str | None = "0002_identity_and_sessions"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # 1. projects table
    op.create_table(
        "projects",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("slug", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="PLANNING"),
        sa.Column("priority", sa.String(length=50), nullable=True, server_default="NORMAL"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("progress", sa.Integer(), nullable=True, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("archived_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("user_id", "slug", name="uq_projects_user_slug"),
        sa.CheckConstraint(
            "progress >= 0 AND progress <= 100",
            name="chk_projects_progress_bounds",
        ),
    )

    op.create_index("ix_projects_user_id", "projects", ["user_id"])
    op.create_index(
        "uq_projects_user_active",
        "projects",
        ["user_id"],
        unique=True,
        postgresql_where=sa.text("is_active = true"),
    )

    # 2. project_technologies table
    op.create_table(
        "project_technologies",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column(
            "project_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("projects.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("category", sa.String(length=50), nullable=True),
        sa.Column("version", sa.String(length=50), nullable=True),
        sa.Column(
            "metadata",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("project_id", "name", name="uq_project_technologies_project_name"),
    )

    op.create_index(
        "ix_project_technologies_project_id",
        "project_technologies",
        ["project_id"],
    )

    # 3. Foreign key on user_preferences.default_project_id
    op.create_foreign_key(
        "fk_user_preferences_default_project_id",
        "user_preferences",
        "projects",
        ["default_project_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_user_preferences_default_project_id",
        "user_preferences",
        type_="foreignkey",
    )
    op.drop_index(
        "ix_project_technologies_project_id",
        table_name="project_technologies",
    )
    op.drop_table("project_technologies")
    op.drop_index("uq_projects_user_active", table_name="projects")
    op.drop_index("ix_projects_user_id", table_name="projects")
    op.drop_table("projects")
