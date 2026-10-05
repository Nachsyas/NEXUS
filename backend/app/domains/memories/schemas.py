import datetime
import uuid
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.domains.memories.models import (
    PROJECT_SCOPED_MEMORY_TYPES,
    MemorySensitivity,
    MemoryType,
)


class MemoryCreate(BaseModel):
    """Schema for manual user explicit memory creation."""

    memory_type: MemoryType
    subject: str = Field(..., min_length=1, max_length=255)
    predicate: str = Field(..., min_length=1, max_length=255)
    value_text: str = Field(..., min_length=1)
    value_json: dict[str, Any] | None = None
    project_id: uuid.UUID | None = None
    importance: float = Field(default=0.5, ge=0.0, le=1.0)
    sensitivity: MemorySensitivity = MemorySensitivity.LOW
    expires_at: datetime.datetime | None = None

    @model_validator(mode="after")
    def validate_project_scope(self) -> "MemoryCreate":
        if self.memory_type in PROJECT_SCOPED_MEMORY_TYPES:
            if self.project_id is None:
                raise ValueError(
                    f"Memory type '{self.memory_type.value}' requires a valid project_id."
                )
        else:
            if self.project_id is not None:
                raise ValueError(
                    f"Memory type '{self.memory_type.value}' is a personal/global memory and cannot specify a project_id."
                )
        return self


class MemoryUpdate(BaseModel):
    """Schema for updating mutable fields of an active memory."""

    value_text: str | None = Field(default=None, min_length=1)
    value_json: dict[str, Any] | None = None
    importance: float | None = Field(default=None, ge=0.0, le=1.0)
    sensitivity: MemorySensitivity | None = None
    expires_at: datetime.datetime | None = None


class MemoryResponse(BaseModel):
    """Full representation of a structured memory entity."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    project_id: uuid.UUID | None = None
    memory_type: str
    subject: str
    predicate: str
    value_text: str
    value_json: dict[str, Any] | None = None
    summary: str
    importance: float
    confidence: float
    sensitivity: str
    source_type: str
    source_id: str | None = None
    status: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    expires_at: datetime.datetime | None = None
    superseded_by: uuid.UUID | None = None


class MemoryListResponse(BaseModel):
    """Envelope for paginated memory listings."""

    items: list[MemoryResponse]
    total: int
    limit: int
    offset: int


class MemorySearchRequest(BaseModel):
    """Payload for semantic vector search over memory items."""

    query: str = Field(..., min_length=1, max_length=1000)
    project_id: uuid.UUID | None = None
    limit: int = Field(default=10, ge=1, le=50)


class MemorySearchHit(BaseModel):
    """Item hit returned by semantic vector search."""

    id: uuid.UUID
    memory_type: str
    subject: str
    predicate: str
    value_text: str
    summary: str
    project_id: uuid.UUID | None = None
    similarity_score: float
    created_at: datetime.datetime


class MemoryForgetResponse(BaseModel):
    """Confirmation payload when a memory is forgotten."""

    id: uuid.UUID
    status: str = "FORGOTTEN"
    forgotten_at: datetime.datetime
