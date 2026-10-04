"""Create users, auth_identities, user_preferences, sessions, and rotated_token_hashes tables.

Revision ID: 0002_identity_and_sessions
Revises: 0001_baseline_schema
Create Date: 2026-10-04 12:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0002_identity_and_sessions"
down_revision: str | None = "0001_baseline_schema"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # 1. users table
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("display_name", sa.String(length=255), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="ACTIVE"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_login_at", sa.DateTime(timezone=True), nullable=True),
    )

    # 2. auth_identities table
    op.create_table(
        "auth_identities",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("provider", sa.String(length=50), nullable=False, server_default="APPLE"),
        sa.Column("provider_subject", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_verified_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint(
            "provider", "provider_subject", name="uq_auth_identities_provider_subject"
        ),
    )
    op.create_index("ix_auth_identities_user_id", "auth_identities", ["user_id"])

    # 3. user_preferences table
    op.create_table(
        "user_preferences",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        ),
        sa.Column("language", sa.String(length=10), nullable=False, server_default="en"),
        sa.Column(
            "response_detail", sa.String(length=50), nullable=False, server_default="CONCISE"
        ),
        sa.Column(
            "interaction_style", sa.String(length=50), nullable=False, server_default="DIRECT"
        ),
        sa.Column(
            "proactivity_level", sa.String(length=50), nullable=False, server_default="MEDIUM"
        ),
        sa.Column("default_project_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("default_device_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("storage_mode", sa.String(length=50), nullable=True),
        sa.Column("research_update_frequency", sa.String(length=50), nullable=True),
        sa.Column(
            "notification_preferences",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
        sa.Column(
            "voice_settings",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_user_preferences_user_id", "user_preferences", ["user_id"])

    # 4. sessions table
    op.create_table(
        "sessions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("device_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("refresh_token_hash", sa.String(length=64), nullable=False),
        sa.Column("token_family_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("rotation_counter", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_used_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revocation_reason", sa.String(length=100), nullable=True),
        sa.Column("client_metadata", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    )
    op.create_index("ix_sessions_user_id", "sessions", ["user_id"])
    op.create_index("ix_sessions_refresh_token_hash", "sessions", ["refresh_token_hash"])
    op.create_index("ix_sessions_token_family_id", "sessions", ["token_family_id"])

    # 5. rotated_token_hashes table for token reuse detection
    op.create_table(
        "rotated_token_hashes",
        sa.Column("token_hash", sa.String(length=64), primary_key=True, nullable=False),
        sa.Column(
            "session_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("sessions.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("token_family_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("rotated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "ix_rotated_token_hashes_family_id", "rotated_token_hashes", ["token_family_id"]
    )


def downgrade() -> None:
    op.drop_index(
        "ix_rotated_token_hashes_family_id", table_name="rotated_token_hashes", if_exists=True
    )
    op.drop_table("rotated_token_hashes", if_exists=True)

    op.drop_index("ix_sessions_token_family_id", table_name="sessions", if_exists=True)
    op.drop_index("ix_sessions_refresh_token_hash", table_name="sessions", if_exists=True)
    op.drop_index("ix_sessions_user_id", table_name="sessions", if_exists=True)
    op.drop_table("sessions", if_exists=True)

    op.drop_index("ix_user_preferences_user_id", table_name="user_preferences", if_exists=True)
    op.drop_table("user_preferences", if_exists=True)

    op.drop_index("ix_auth_identities_user_id", table_name="auth_identities", if_exists=True)
    op.drop_table("auth_identities", if_exists=True)

    op.drop_table("users", if_exists=True)
