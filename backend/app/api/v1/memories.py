import uuid
from typing import Any

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import UserContext, get_current_user_context
from app.core.responses import api_success
from app.domains.memories.schemas import (
    MemoryCreate,
    MemoryForgetResponse,
    MemoryResponse,
    MemorySearchRequest,
    MemoryUpdate,
)
from app.domains.memories.service import MemoryService

router = APIRouter(prefix="/memories", tags=["Memories"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Create Memory Entry",
    description="Add a structured personal or project memory entry with secret safety and deduplication.",
)
async def create_memory(
    body: MemoryCreate,
    current_user: UserContext = Depends(get_current_user_context),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    memory = await MemoryService.create_memory(
        db=db,
        user_id=current_user.user_id,
        data=body,
    )
    await db.commit()
    data = MemoryResponse.model_validate(memory).model_dump(mode="json")
    return api_success(data)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    summary="List Memories",
    description="Retrieve caller-owned memories with status, project, and category filtering and bounded pagination.",
)
async def list_memories(
    status: str | None = Query(
        default=None, description="Filter by status (default: ACTIVE non-expired)"
    ),
    project_id: uuid.UUID | None = Query(default=None, description="Filter by project scope"),
    memory_type: str | None = Query(default=None, description="Filter by canonical memory type"),
    page: int = Query(default=1, ge=1, description="Page number (1-indexed)"),
    limit: int = Query(default=20, ge=1, le=100, description="Items per page (max 100)"),
    current_user: UserContext = Depends(get_current_user_context),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    memories, total = await MemoryService.list_memories(
        db=db,
        user_id=current_user.user_id,
        status=status,
        project_id=project_id,
        memory_type=memory_type,
        page=page,
        limit=limit,
    )
    items = [MemoryResponse.model_validate(m).model_dump(mode="json") for m in memories]
    total_pages = (total + limit - 1) // limit if total > 0 else 0
    meta = {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
    }
    return api_success(items, meta=meta)


@router.post(
    "/search",
    status_code=status.HTTP_200_OK,
    summary="Search Memories Semantically",
    description="Perform semantic vector similarity search over caller's active memories.",
)
async def search_memories(
    body: MemorySearchRequest,
    current_user: UserContext = Depends(get_current_user_context),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    hits = await MemoryService.search_memories(
        db=db,
        user_id=current_user.user_id,
        query=body.query,
        project_id=body.project_id,
        limit=body.limit,
    )
    data = [h.model_dump(mode="json") for h in hits]
    return api_success(data)


@router.get(
    "/{memory_id}",
    status_code=status.HTTP_200_OK,
    summary="Get Memory Details",
    description="Retrieve full structured details of a specific memory owned by authenticated user.",
)
async def get_memory(
    memory_id: uuid.UUID,
    current_user: UserContext = Depends(get_current_user_context),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    memory = await MemoryService.get_memory(
        db=db,
        user_id=current_user.user_id,
        memory_id=memory_id,
    )
    data = MemoryResponse.model_validate(memory).model_dump(mode="json")
    return api_success(data)


@router.patch(
    "/{memory_id}",
    status_code=status.HTTP_200_OK,
    summary="Update Memory Entry",
    description="Selectively update mutable fields of an active memory.",
)
async def update_memory(
    memory_id: uuid.UUID,
    body: MemoryUpdate,
    current_user: UserContext = Depends(get_current_user_context),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    memory = await MemoryService.update_memory(
        db=db,
        user_id=current_user.user_id,
        memory_id=memory_id,
        data=body,
    )
    await db.commit()
    data = MemoryResponse.model_validate(memory).model_dump(mode="json")
    return api_success(data)


@router.post(
    "/{memory_id}/forget",
    status_code=status.HTTP_200_OK,
    summary="Forget Memory",
    description="Transition memory status to FORGOTTEN, excluding it from context retrieval.",
)
async def forget_memory(
    memory_id: uuid.UUID,
    current_user: UserContext = Depends(get_current_user_context),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    memory = await MemoryService.forget_memory(
        db=db,
        user_id=current_user.user_id,
        memory_id=memory_id,
    )
    await db.commit()
    data = MemoryForgetResponse(
        id=memory.id,
        status=memory.status,
        forgotten_at=memory.updated_at,
    ).model_dump(mode="json")
    return api_success(data)
