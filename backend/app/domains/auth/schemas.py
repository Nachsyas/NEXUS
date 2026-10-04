import datetime
import uuid

from pydantic import BaseModel, ConfigDict, Field

from app.domains.users.schemas import UserResponse


class AppleUserInfo(BaseModel):
    name: str | None = None
    email: str | None = None


class AppleLoginRequest(BaseModel):
    identity_token: str = Field(..., min_length=1)
    authorization_code: str | None = None
    user_info: AppleUserInfo | None = None


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse


class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(..., min_length=1)


class RefreshTokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class LogoutRequest(BaseModel):
    refresh_token: str | None = None


class LogoutResponse(BaseModel):
    message: str = "Session revoked"


class SessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    device_name: str | None = None
    ip_address: str | None = None
    created_at: datetime.datetime
    last_active_at: datetime.datetime


class SessionRevokeResponse(BaseModel):
    message: str = "Session terminated"
