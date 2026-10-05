import datetime
import json
import uuid
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.domains.memories.models import (
    PROJECT_SCOPED_MEMORY_TYPES,
    MemorySensitivity,
    MemoryType,
)

MAX_MEMORY_VALUE_TEXT_CHARS = 10000
MAX_MEMORY_VALUE_JSON_BYTES = 65536  # 64 KB safety bound
MAX_MEMORY_VALUE_JSON_DEPTH = 5


def validate_value_json_bound(v: dict[str, Any] | None) -> dict[str, Any] | None:
    """Enforce serialized byte size and recursion depth bounds on structured value_json."""
    if v is None:
        return None

    def _check_depth(obj: Any, current_depth: int = 1) -> None:
        if current_depth > MAX_MEMORY_VALUE_JSON_DEPTH:
            raise ValueError(
                f"value_json exceeds maximum allowed nesting depth of {MAX_MEMORY_VALUE_JSON_DEPTH}."
            )
        if isinstance(obj, dict):
            for val in obj.values():
                _check_depth(val, current_depth + 1)
        elif isinstance(obj, (list, tuple)):
            for item in obj:
                _check_depth(item, current_depth + 1)

    _check_depth(v)

    try:
        raw = json.dumps(v)
    except (TypeError, ValueError) as err:
        raise ValueError("value_json must be valid JSON-serializable data.") from err

    if len(raw.encode("utf-8")) > MAX_MEMORY_VALUE_JSON_BYTES:
        raise ValueError(
            f"value_json serialized size exceeds maximum limit of {MAX_MEMORY_VALUE_JSON_BYTES} bytes."
        )

    return v


class MemoryCreate(BaseModel):
    """Schema for manual user explicit memory creation."""

    memory_type: MemoryType
    subject: str = Field(..., min_length=1, max_length=255)
    predicate: str = Field(..., min_length=1, max_length=255)
    value_text: str = Field(..., min_length=1, max_length=MAX_MEMORY_VALUE_TEXT_CHARS)
    value_json: dict[str, Any] | None = None
    project_id: uuid.UUID | None = None
    importance: float = Field(default=0.5, ge=0.0, le=1.0)
    sensitivity: MemorySensitivity = MemorySensitivity.LOW
    expires_at: datetime.datetime | None = None

    @field_validator("value_json")
    @classmethod
    def check_value_json_bound(cls, v: dict[str, Any] | None) -> dict[str, Any] | None:
        return validate_value_json_bound(v)

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

    value_text: str | None = Field(
        default=None, min_length=1, max_length=MAX_MEMORY_VALUE_TEXT_CHARS
    )
    value_json: dict[str, Any] | None = None
    importance: float | None = Field(default=None, ge=0.0, le=1.0)
    sensitivity: MemorySensitivity | None = None
    expires_at: datetime.datetime | None = None

    @field_validator("value_json")
    @classmethod
    def check_value_json_bound(cls, v: dict[str, Any] | None) -> dict[str, Any] | None:
        return validate_value_json_bound(v)


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
