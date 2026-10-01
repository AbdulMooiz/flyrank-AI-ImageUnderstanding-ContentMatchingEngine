from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class VisionMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")

    subject: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1)
    attributes: list[str] = Field(..., min_length=1)
    caption: str = Field(..., min_length=1)
    confidence: float = Field(..., ge=0.0, le=1.0)

    @field_validator("attributes")
    @classmethod
    def validate_attributes(cls, value: list[str]) -> list[str]:
        if not value:
            raise ValueError("attributes cannot be empty")
        return [str(item).strip() for item in value if str(item).strip()]

    @field_validator("subject", "category", "caption")
    @classmethod
    def clean_text(cls, value: str) -> str:
        cleaned = " ".join(str(value).strip().split())
        if not cleaned:
            raise ValueError("text value cannot be empty")
        return cleaned

    @classmethod
    def from_raw(cls, payload: dict[str, Any]) -> "VisionMetadata":
        if not isinstance(payload, dict):
            raise ValueError("Vision payload must be a JSON object")
        return cls.model_validate(payload)
