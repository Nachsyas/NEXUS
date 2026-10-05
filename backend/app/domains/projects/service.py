import re
import unicodedata
import uuid
from typing import Any

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domains.projects.exceptions import (
    ProjectInvalidStateError,
    ProjectNotFoundError,
)
from app.domains.projects.models import (
    Project,
    ProjectTechnology,
    utc_now,
)
from app.domains.projects.schemas import ProjectCreate, ProjectUpdate


def slugify(value: str) -> str:
    """Convert string into URL-friendly, lowercased slug."""
    normalized = unicodedata.normalize("NFKD", value)
    ascii_encoded = normalized.encode("ascii", "ignore").decode("ascii")
    lowered = ascii_encoded.lower()
    cleaned = re.sub(r"[^a-z0-9]+", "-", lowered).strip("-")
    return cleaned if cleaned else "project"


class ProjectService:
    """Service managing Project lifecycle, ownership, technologies, and context."""

    @staticmethod
    async def generate_unique_slug(db: AsyncSession, user_id: uuid.UUID, name: str) -> str:
        """Generate a deterministic, per-user unique slug handling collisions."""
        base_slug = slugify(name)
        candidate = base_slug
        counter = 2
        while True:
            stmt = select(Project.id).where(
                Project.user_id == user_id,
                Project.slug == candidate,
            )
            existing = (await db.execute(stmt)).scalar_one_or_none()
            if not existing:
                return candidate
            candidate = f"{base_slug}-{counter}"
            counter += 1

    @staticmethod
    async def create_project(
        db: AsyncSession,
        user_id: uuid.UUID,
        data: ProjectCreate,
    ) -> Project:
        clean_name = data.name.strip()
        if not clean_name:
            raise ValueError("Project name cannot be empty.")

        slug = await ProjectService.generate_unique_slug(db, user_id, clean_name)

        project = Project(
            user_id=user_id,
            name=clean_name,
            slug=slug,
            description=data.description,
            status=data.status,
            priority=data.priority,
            summary=data.summary,
            progress=data.progress,
            is_active=False,
        )

        if data.technologies:
            seen: set[str] = set()
            for tech_name in data.technologies:
                clean_tech = tech_name.strip()
                if clean_tech and clean_tech.lower() not in seen:
                    seen.add(clean_tech.lower())
                    project.technologies.append(
                        ProjectTechnology(name=clean_tech, tech_metadata={})
                    )

        db.add(project)
        await db.flush()
        return await ProjectService.get_project(db, user_id, project.id)

    @staticmethod
    async def list_projects(
        db: AsyncSession,
        user_id: uuid.UUID,
        include_archived: bool = False,
        status: str | None = None,
        is_active: bool | None = None,
        page: int = 1,
        limit: int = 20,
    ) -> tuple[list[Project], int]:
        query = select(Project).where(Project.user_id == user_id)

        if status is not None:
            query = query.where(Project.status == status)
        elif not include_archived:
            query = query.where(Project.status != "ARCHIVED")

        if is_active is not None:
            query = query.where(Project.is_active == is_active)

        # Count total matches
        count_stmt = select(func.count()).select_from(query.subquery())
        total = (await db.execute(count_stmt)).scalar_one()

        # Paginate and order
        offset = (page - 1) * limit
        paginated_query = (
            query.options(selectinload(Project.technologies))
            .order_by(Project.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        result = await db.execute(paginated_query)
        projects = list(result.scalars().all())
        return projects, total

    @staticmethod
    async def get_project(
        db: AsyncSession,
        user_id: uuid.UUID,
        project_id: uuid.UUID,
    ) -> Project:
        stmt = (
            select(Project)
            .where(Project.id == project_id, Project.user_id == user_id)
            .options(selectinload(Project.technologies))
        )
        result = await db.execute(stmt)
        project = result.scalar_one_or_none()
        if not project:
            raise ProjectNotFoundError(f"Project {project_id} not found.")
        return project

    @staticmethod
    async def update_project(
        db: AsyncSession,
        user_id: uuid.UUID,
        project_id: uuid.UUID,
        data: ProjectUpdate,
    ) -> Project:
        project = await ProjectService.get_project(db, user_id, project_id)

        if data.name is not None:
            clean_name = data.name.strip()
            if not clean_name:
                raise ValueError("Project name cannot be empty.")
            project.name = clean_name

        if data.description is not None:
            project.description = data.description

        if data.status is not None:
            if data.status == "ARCHIVED":
                project.status = "ARCHIVED"
                project.archived_at = utc_now()
                project.is_active = False
            else:
                project.status = data.status
                if project.archived_at is not None:
                    project.archived_at = None

        if data.priority is not None:
            project.priority = data.priority

        if data.summary is not None:
            project.summary = data.summary

        if data.progress is not None:
            project.progress = data.progress

        if data.technologies is not None:
            seen = set()
            clean_techs = []
            for t in data.technologies:
                clean_t = t.strip()
                if clean_t and clean_t.lower() not in seen:
                    seen.add(clean_t.lower())
                    clean_techs.append(clean_t)

            existing_map = {t.name.lower(): t for t in project.technologies}
            # Keep existing that are still in payload
            project.technologies = [t for t in project.technologies if t.name.lower() in seen]
            # Add newly provided technologies
            for t_name in clean_techs:
                if t_name.lower() not in existing_map:
                    project.technologies.append(ProjectTechnology(name=t_name, tech_metadata={}))

        project.updated_at = utc_now()
        await db.flush()
        return project

    @staticmethod
    async def activate_project(
        db: AsyncSession,
        user_id: uuid.UUID,
        project_id: uuid.UUID,
    ) -> Project:
        project = await ProjectService.get_project(db, user_id, project_id)

        if project.status == "ARCHIVED":
            raise ProjectInvalidStateError("Cannot activate an archived project.")

        if project.is_active:
            return project

        now = utc_now()
        # Deactivate any currently active project for this user
        await db.execute(
            update(Project)
            .where(Project.user_id == user_id, Project.is_active)
            .values(is_active=False, updated_at=now)
        )

        project.is_active = True
        project.updated_at = now
        await db.flush()
        return project

    @staticmethod
    async def archive_project(
        db: AsyncSession,
        user_id: uuid.UUID,
        project_id: uuid.UUID,
    ) -> Project:
        project = await ProjectService.get_project(db, user_id, project_id)

        now = utc_now()
        project.status = "ARCHIVED"
        project.archived_at = now
        project.is_active = False
        project.updated_at = now
        await db.flush()
        return project

    @staticmethod
    async def get_project_context(
        db: AsyncSession,
        user_id: uuid.UUID,
        project_id: uuid.UUID,
    ) -> dict[str, Any]:
        project = await ProjectService.get_project(db, user_id, project_id)
        active_techs = [t.name for t in project.technologies]
        return {
            "project_id": project.id,
            "name": project.name,
            "slug": project.slug,
            "summary": project.summary,
            "status": project.status,
            "priority": project.priority,
            "progress": project.progress or 0,
            "is_active": project.is_active,
            "active_technologies": active_techs,
            "memory_count": 0,
            "knowledge_count": 0,
        }
