import datetime
import uuid
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    display_name: str | None = None
    status: str = "ACTIVE"
    created_at: datetime.datetime
    last_login_at: datetime.datetime | None = None


class UserUpdateRequest(BaseModel):
    display_name: str = Field(..., min_length=1, max_length=255)


class UserPreferenceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    language: str = "en"
    response_detail: str = "CONCISE"
    interaction_style: str = "DIRECT"
    proactivity_level: str = "MEDIUM"
    default_project_id: uuid.UUID | None = None
    default_device_id: uuid.UUID | None = None
    storage_mode: str | None = None
    research_update_frequency: str | None = None
    notification_preferences: dict[str, Any] = Field(default_factory=dict)
    voice_settings: dict[str, Any] = Field(default_factory=dict)


class UserPreferenceUpdateRequest(BaseModel):
    language: str | None = Field(None, max_length=10)
    response_detail: str | None = Field(None, pattern="^(CONCISE|DETAILED|TECHNICAL)$")
    interaction_style: str | None = Field(None, pattern="^(DIRECT|EXPLORATORY)$")
    proactivity_level: str | None = Field(None, pattern="^(LOW|MEDIUM|HIGH)$")
    default_project_id: uuid.UUID | None = None
    default_device_id: uuid.UUID | None = None
    storage_mode: str | None = None
    research_update_frequency: str | None = None
    notification_preferences: dict[str, Any] | None = None
    voice_settings: dict[str, Any] | None = None


class UserPreferenceUpdateResponse(BaseModel):
    updated: bool = True
    preferences: UserPreferenceResponse
