import uuid
from typing import Any

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import UserContext, get_current_user_context
from app.core.responses import api_success
from app.domains.projects.schemas import (
    ProjectActivateResponse,
    ProjectArchiveResponse,
    ProjectContextResponse,
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
)
from app.domains.projects.service import ProjectService

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Create New Project",
    description="Create a new project workspace belonging to the authenticated user.",
)
async def create_project(
    body: ProjectCreate,
    current_user: UserContext = Depends(get_current_user_context),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    project = await ProjectService.create_project(
        db=db,
        user_id=current_user.user_id,
        data=body,
    )
    await db.commit()
    data = ProjectResponse.model_validate(project).model_dump(mode="json")
    return api_success(data)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    summary="List User Projects",
    description="Retrieve a bounded, paginated list of projects owned by the authenticated user.",
)
async def list_projects(
    include_archived: bool = Query(default=False, description="Include archived projects"),
    status: str | None = Query(default=None, description="Filter by status"),
    is_active: bool | None = Query(default=None, description="Filter by active focus state"),
    page: int = Query(default=1, ge=1, description="Page number (1-indexed)"),
    limit: int = Query(default=20, ge=1, le=100, description="Items per page (max 100)"),
    current_user: UserContext = Depends(get_current_user_context),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    projects, total = await ProjectService.list_projects(
        db=db,
        user_id=current_user.user_id,
        include_archived=include_archived,
        status=status,
        is_active=is_active,
        page=page,
        limit=limit,
    )
    items = [ProjectResponse.model_validate(p).model_dump(mode="json") for p in projects]
    total_pages = (total + limit - 1) // limit if total > 0 else 0
    meta = {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
    }
    return api_success(items, meta=meta)


@router.get(
    "/{project_id}",
    status_code=status.HTTP_200_OK,
    summary="Get Project Details",
    description="Retrieve detailed metadata of a specific project owned by the authenticated user.",
)
async def get_project(
    project_id: uuid.UUID,
    current_user: UserContext = Depends(get_current_user_context),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    project = await ProjectService.get_project(
        db=db,
        user_id=current_user.user_id,
        project_id=project_id,
    )
    data = ProjectResponse.model_validate(project).model_dump(mode="json")
    return api_success(data)


@router.patch(
    "/{project_id}",
    status_code=status.HTTP_200_OK,
    summary="Update Project Metadata",
    description="Update mutable fields of a project (e.g. name, description, status, progress).",
)
async def update_project(
    project_id: uuid.UUID,
    body: ProjectUpdate,
    current_user: UserContext = Depends(get_current_user_context),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    project = await ProjectService.update_project(
        db=db,
        user_id=current_user.user_id,
        project_id=project_id,
        data=body,
    )
    await db.commit()
    data = ProjectResponse.model_validate(project).model_dump(mode="json")
    return api_success(data)


@router.post(
    "/{project_id}/activate",
    status_code=status.HTTP_200_OK,
    summary="Activate Project",
    description="Set the project as currently active focus. Atomically deactivates prior active project.",
)
async def activate_project(
    project_id: uuid.UUID,
    current_user: UserContext = Depends(get_current_user_context),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    project = await ProjectService.activate_project(
        db=db,
        user_id=current_user.user_id,
        project_id=project_id,
    )
    await db.commit()
    data = ProjectActivateResponse.model_validate(project).model_dump(mode="json")
    return api_success(data)


@router.post(
    "/{project_id}/archive",
    status_code=status.HTTP_200_OK,
    summary="Archive Project",
    description="Archive project historically without deletion. Automatically clears active state.",
)
async def archive_project(
    project_id: uuid.UUID,
    current_user: UserContext = Depends(get_current_user_context),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    project = await ProjectService.archive_project(
        db=db,
        user_id=current_user.user_id,
        project_id=project_id,
    )
    await db.commit()
    data = ProjectArchiveResponse.model_validate(project).model_dump(mode="json")
    return api_success(data)


@router.get(
    "/{project_id}/context",
    status_code=status.HTTP_200_OK,
    summary="Get Project Context Metadata",
    description="Deterministic project metadata context foundation (zero M3+ memories or AI retrieval).",
)
async def get_project_context(
    project_id: uuid.UUID,
    current_user: UserContext = Depends(get_current_user_context),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    context_data = await ProjectService.get_project_context(
        db=db,
        user_id=current_user.user_id,
        project_id=project_id,
    )
    data = ProjectContextResponse.model_validate(context_data).model_dump(mode="json")
    return api_success(data)
