"""Create memories table with pgvector column, indexes, and constraints.

Revision ID: 0004_memories_core
Revises: 0003_projects_and_technologies
Create Date: 2026-10-05 16:30:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0004_memories_core"
down_revision: str | None = "0003_projects_and_technologies"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "memories",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "project_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("projects.id", ondelete="CASCADE"),
            nullable=True,
        ),
        sa.Column("memory_type", sa.String(length=50), nullable=False),
        sa.Column("subject", sa.String(length=255), nullable=False),
        sa.Column("predicate", sa.String(length=255), nullable=False),
        sa.Column("value_text", sa.Text(), nullable=False),
        sa.Column(
            "value_json",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
        ),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("embedding", Vector(), nullable=True),
        sa.Column("importance", sa.Float(), nullable=False, server_default="0.5"),
        sa.Column("confidence", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("sensitivity", sa.String(length=20), nullable=False, server_default="LOW"),
        sa.Column(
            "source_type", sa.String(length=50), nullable=False, server_default="USER_EXPLICIT"
        ),
        sa.Column("source_id", sa.String(length=255), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="ACTIVE"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "superseded_by",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("memories.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.CheckConstraint(
            "importance >= 0.0 AND importance <= 1.0",
            name="chk_memories_importance_bounds",
        ),
        sa.CheckConstraint(
            "confidence >= 0.0 AND confidence <= 1.0",
            name="chk_memories_confidence_bounds",
        ),
    )

    op.create_index("ix_memories_user_id", "memories", ["user_id"])
    op.create_index("ix_memories_project_id", "memories", ["project_id"])
    op.create_index("ix_memories_user_status", "memories", ["user_id", "status"])
    op.create_index(
        "ix_memories_user_project_status", "memories", ["user_id", "project_id", "status"]
    )
    op.create_index(
        "ix_memories_user_type_status", "memories", ["user_id", "memory_type", "status"]
    )
    op.create_index("ix_memories_expires_at", "memories", ["expires_at"])
    op.create_index("ix_memories_user_updated_at", "memories", ["user_id", "updated_at"])


def downgrade() -> None:
    op.drop_index("ix_memories_user_updated_at", table_name="memories")
    op.drop_index("ix_memories_expires_at", table_name="memories")
    op.drop_index("ix_memories_user_type_status", table_name="memories")
    op.drop_index("ix_memories_user_project_status", table_name="memories")
    op.drop_index("ix_memories_user_status", table_name="memories")
    op.drop_index("ix_memories_project_id", table_name="memories")
    op.drop_index("ix_memories_user_id", table_name="memories")
    op.drop_table("memories")
