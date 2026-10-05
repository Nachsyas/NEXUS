import datetime
import uuid
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

ProjectStatusLiteral = Literal["IDEA", "PLANNING", "ACTIVE", "PAUSED", "COMPLETED", "ARCHIVED"]
ProjectPriorityLiteral = Literal["LOW", "NORMAL", "HIGH"]


class ProjectTechnologyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: uuid.UUID
    name: str
    category: str | None = None
    version: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict, alias="tech_metadata")
    created_at: datetime.datetime
    updated_at: datetime.datetime


class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    status: ProjectStatusLiteral = "PLANNING"
    priority: ProjectPriorityLiteral | None = "NORMAL"
    summary: str | None = None
    progress: int | None = Field(default=0, ge=0, le=100)
    technologies: list[str] = Field(default_factory=list)


class ProjectUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    status: ProjectStatusLiteral | None = None
    priority: ProjectPriorityLiteral | None = None
    summary: str | None = None
    progress: int | None = Field(None, ge=0, le=100)
    technologies: list[str] | None = None


class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    slug: str
    description: str | None = None
    status: str
    priority: str | None = None
    is_active: bool
    summary: str | None = None
    progress: int | None = 0
    technologies: list[ProjectTechnologyResponse] = Field(default_factory=list)
    created_at: datetime.datetime
    updated_at: datetime.datetime
    archived_at: datetime.datetime | None = None


class ProjectActivateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    slug: str
    is_active: bool


class ProjectArchiveResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    status: str
    is_active: bool
    archived_at: datetime.datetime | None


class ProjectContextResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    project_id: uuid.UUID
    name: str
    slug: str
    summary: str | None = None
    status: str
    priority: str | None = None
    progress: int | None = 0
    is_active: bool
    active_technologies: list[str] = Field(default_factory=list)
