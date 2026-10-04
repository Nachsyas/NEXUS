import datetime
import uuid
from dataclasses import dataclass

from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.domains.auth.models import Session
from app.domains.auth.security import (
    InvalidCredentialsError,
    TokenExpiredError,
    decode_access_token,
)

bearer_scheme = HTTPBearer(auto_error=False)


@dataclass(frozen=True)
class UserContext:
    user_id: uuid.UUID
    session_id: uuid.UUID


async def get_current_user_context(
    _request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> UserContext:
    if not credentials or credentials.scheme.lower() != "bearer":
        raise InvalidCredentialsError("Missing or malformed Authorization header.")

    # 1. Decode and verify JWT signature and expiration
    payload = decode_access_token(credentials.credentials)

    sub_str = payload.get("sub")
    session_id_str = payload.get("session_id")
    if not sub_str or not session_id_str:
        raise InvalidCredentialsError("Access token claims missing sub or session_id.")

    try:
        user_id = uuid.UUID(sub_str)
        session_id = uuid.UUID(session_id_str)
    except ValueError as exc:
        raise InvalidCredentialsError("Malformed user_id or session_id.") from exc

    # 2. Check session state in database
    now = datetime.datetime.now(datetime.UTC)
    stmt = select(Session).where(Session.id == session_id, Session.user_id == user_id)
    result = await db.execute(stmt)
    session = result.scalar_one_or_none()

    if not session:
        raise InvalidCredentialsError("Session does not exist.")

    if session.revoked_at is not None:
        raise InvalidCredentialsError("Session has been revoked.")

    if session.expires_at < now:
        raise TokenExpiredError("Session has expired.")

    return UserContext(user_id=user_id, session_id=session_id)
