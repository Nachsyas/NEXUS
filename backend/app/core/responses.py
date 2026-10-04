from typing import Any

from pydantic import BaseModel, Field


class SuccessEnvelope(BaseModel):
    success: bool = True
    data: Any = None
    meta: dict[str, Any] = Field(default_factory=dict)


class ErrorDetail(BaseModel):
    code: str
    message: str
    details: Any = None


class ErrorEnvelope(BaseModel):
    success: bool = False
    error: ErrorDetail


def api_success(data: Any = None, meta: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "success": True,
        "data": data,
        "meta": meta or {},
    }
