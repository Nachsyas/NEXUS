import datetime
import uuid
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.auth.security import ForbiddenAccessError
from app.domains.projects.exceptions import ProjectNotFoundError
from app.domains.projects.models import Project
from app.domains.users.models import User, UserPreference


class UserService:
    """Service managing core User profiles and user preferences."""

    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: uuid.UUID) -> User | None:
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def update_user_profile(db: AsyncSession, user_id: uuid.UUID, display_name: str) -> User:
        user = await UserService.get_user_by_id(db, user_id)
        if not user:
            raise ForbiddenAccessError("User not found.")

        user.display_name = display_name
        user.updated_at = datetime.datetime.now(datetime.UTC)
        await db.flush()
        return user

    @staticmethod
    async def get_user_preferences(db: AsyncSession, user_id: uuid.UUID) -> UserPreference:
        result = await db.execute(select(UserPreference).where(UserPreference.user_id == user_id))
        pref = result.scalar_one_or_none()
        if not pref:
            # If preferences don't exist yet, lazily initialize them with safe defaults
            pref = UserPreference(
                user_id=user_id,
                language="en",
                response_detail="CONCISE",
                interaction_style="DIRECT",
                proactivity_level="MEDIUM",
                notification_preferences={},
                voice_settings={},
            )
            db.add(pref)
            await db.flush()
        return pref

    @staticmethod
    async def update_user_preferences(
        db: AsyncSession,
        user_id: uuid.UUID,
        updates: dict[str, Any],
    ) -> UserPreference:
        pref = await UserService.get_user_preferences(db, user_id)

        # Validate default_project_id ownership if provided
        if "default_project_id" in updates:
            target_proj_id = updates["default_project_id"]
            if target_proj_id is None:
                pref.default_project_id = None
            else:
                proj_stmt = select(Project.id).where(
                    Project.id == target_proj_id,
                    Project.user_id == user_id,
                )
                existing_proj = (await db.execute(proj_stmt)).scalar_one_or_none()
                if not existing_proj:
                    raise ProjectNotFoundError(f"Project '{target_proj_id}' not found.")
                pref.default_project_id = target_proj_id

        for key, value in updates.items():
            if key == "default_project_id":
                continue  # Handled above with ownership verification
            if value is not None and hasattr(pref, key):
                setattr(pref, key, value)

        pref.updated_at = datetime.datetime.now(datetime.UTC)
        await db.flush()
        return pref
