import datetime
import hashlib
import secrets
import uuid
from typing import Any

import jwt
import uuid6

from app.core.config import settings


class AuthenticationError(Exception):
    """Base exception for authentication failures."""

    def __init__(self, code: str, message: str, status_code: int = 401) -> None:
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class InvalidCredentialsError(AuthenticationError):
    def __init__(self, message: str = "Invalid credentials or token.") -> None:
        super().__init__(code="AUTH_INVALID_CREDENTIALS", message=message, status_code=401)


class TokenExpiredError(AuthenticationError):
    def __init__(self, message: str = "Token has expired.") -> None:
        super().__init__(code="AUTH_TOKEN_EXPIRED", message=message, status_code=401)


class RefreshTokenReusedError(AuthenticationError):
    def __init__(self, message: str = "Refresh token reuse detected. Session terminated.") -> None:
        super().__init__(code="AUTH_REFRESH_TOKEN_REUSED", message=message, status_code=401)


class ForbiddenAccessError(AuthenticationError):
    def __init__(self, message: str = "Access forbidden.") -> None:
        super().__init__(code="FORBIDDEN_ACCESS", message=message, status_code=403)


def hash_token(token: str) -> str:
    """Compute SHA-256 hex digest of an opaque token string."""
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def generate_opaque_token() -> str:
    """Generate a cryptographically secure 256-bit random opaque string."""
    return secrets.token_urlsafe(32)


def create_access_token(
    user_id: uuid.UUID,
    session_id: uuid.UUID,
    expires_delta: datetime.timedelta | None = None,
) -> str:
    """Create a signed HS256 JWT access token (ADR-020)."""
    now = datetime.datetime.now(datetime.UTC)
    if expires_delta is not None:
        exp = now + expires_delta
    else:
        exp = now + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    payload: dict[str, Any] = {
        "sub": str(user_id),
        "session_id": str(session_id),
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
        "jti": str(uuid6.uuid7()),
    }
    encoded_jwt = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )
    return encoded_jwt


def decode_access_token(token: str) -> dict[str, Any]:
    """Decode and cryptographically verify an HS256 JWT access token."""
    try:
        payload: dict[str, Any] = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload
    except jwt.ExpiredSignatureError as exc:
        raise TokenExpiredError("Access token signature has expired.") from exc
    except jwt.InvalidTokenError as exc:
        raise InvalidCredentialsError("Invalid access token.") from exc
