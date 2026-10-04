import uuid
from typing import Any

from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import UserContext, get_current_user_context
from app.core.responses import api_success
from app.domains.auth.schemas import (
    AppleLoginRequest,
    LogoutRequest,
    RefreshTokenRequest,
)
from app.domains.auth.service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth & Identity"])


@router.post(
    "/apple",
    status_code=status.HTTP_200_OK,
    summary="Sign in with Apple",
    description="Verify Apple identity token, resolve/create internal user, and issue session tokens.",
)
async def login_with_apple(
    body: AppleLoginRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    client_ip = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")
    client_metadata = {
        "ip_address": client_ip,
        "user_agent": user_agent,
        "device_name": request.headers.get("x-device-name", "Apple Client"),
    }

    result = await AuthService.login_with_apple(
        db=db,
        request=body,
        client_metadata=client_metadata,
    )
    return api_success(result.model_dump(mode="json"))


@router.post(
    "/refresh",
    status_code=status.HTTP_200_OK,
    summary="Refresh Session Tokens",
    description="Rotate refresh token, issue a new access token, and detect token replay.",
)
async def refresh_token(
    body: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    result = await AuthService.refresh_session(
        db=db,
        refresh_token=body.refresh_token,
    )
    return api_success(result.model_dump(mode="json"))


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    summary="Logout Session",
    description="Revoke the current active session.",
)
async def logout(
    body: LogoutRequest | None = None,
    current_user: UserContext = Depends(get_current_user_context),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    refresh_token_str = body.refresh_token if body else None
    await AuthService.logout(
        db=db,
        user_id=current_user.user_id,
        session_id=current_user.session_id,
        refresh_token=refresh_token_str,
    )
    return api_success({"message": "Session revoked"})


@router.get(
    "/sessions",
    status_code=status.HTTP_200_OK,
    summary="List Active User Sessions",
    description="Retrieve all non-revoked active login sessions for the authenticated user.",
)
async def get_sessions(
    current_user: UserContext = Depends(get_current_user_context),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    sessions = await AuthService.list_user_sessions(
        db=db,
        user_id=current_user.user_id,
    )
    return api_success([s.model_dump(mode="json") for s in sessions])


@router.delete(
    "/sessions/{session_id}",
    status_code=status.HTTP_200_OK,
    summary="Revoke Specific Session",
    description="Revoke a specific active session belonging to the authenticated user.",
)
async def revoke_session(
    session_id: uuid.UUID,
    current_user: UserContext = Depends(get_current_user_context),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    await AuthService.revoke_user_session(
        db=db,
        user_id=current_user.user_id,
        session_id=session_id,
    )
    return api_success({"message": "Session terminated"})
