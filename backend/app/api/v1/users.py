from typing import Any

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import UserContext, get_current_user_context
from app.core.responses import api_success
from app.domains.auth.security import ForbiddenAccessError
from app.domains.users.schemas import (
    UserPreferenceResponse,
    UserPreferenceUpdateRequest,
    UserResponse,
    UserUpdateRequest,
)
from app.domains.users.service import UserService

router = APIRouter(prefix="", tags=["User & Preferences"])


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    summary="Get Current User Profile",
    description="Retrieve the profile of the currently authenticated user.",
)
async def get_me(
    current_user: UserContext = Depends(get_current_user_context),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    user = await UserService.get_user_by_id(db, current_user.user_id)
    if not user:
        raise ForbiddenAccessError("User not found.")
    data = UserResponse.model_validate(user).model_dump(mode="json")
    return api_success(data)


@router.patch(
    "/me",
    status_code=status.HTTP_200_OK,
    summary="Update User Profile",
    description="Update mutable fields of the authenticated user profile (e.g. display_name).",
)
async def update_me(
    body: UserUpdateRequest,
    current_user: UserContext = Depends(get_current_user_context),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    user = await UserService.update_user_profile(
        db=db,
        user_id=current_user.user_id,
        display_name=body.display_name,
    )
    return api_success({"id": str(user.id), "display_name": user.display_name})


@router.get(
    "/me/preferences",
    status_code=status.HTTP_200_OK,
    summary="Get User Preferences",
    description="Retrieve the interaction and system preferences of the authenticated user.",
)
async def get_my_preferences(
    current_user: UserContext = Depends(get_current_user_context),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    pref = await UserService.get_user_preferences(db, current_user.user_id)
    data = UserPreferenceResponse.model_validate(pref).model_dump(mode="json")
    return api_success(data)


@router.patch(
    "/me/preferences",
    status_code=status.HTTP_200_OK,
    summary="Update User Preferences",
    description="Update interaction preferences for the authenticated user.",
)
async def update_my_preferences(
    body: UserPreferenceUpdateRequest,
    current_user: UserContext = Depends(get_current_user_context),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    pref = await UserService.update_user_preferences(
        db=db,
        user_id=current_user.user_id,
        updates=body.model_dump(exclude_unset=True),
    )
    return api_success(
        {
            "updated": True,
            "preferences": UserPreferenceResponse.model_validate(pref).model_dump(mode="json"),
        }
    )
