from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class PostBase(BaseModel):
    title: str
    content: str
    source: str = "manual"


class PostCreate(PostBase):
    pass


class PostRead(PostBase):
    id: int
    status: str = "draft"

    class Config:
        orm_mode = True


class PostSearchResult(BaseModel):
    post_id: int
    score: float
    rank: int
    subject: str
    label: str
    reason: str


class PostCandidate(BaseModel):
    image_id: Optional[int] = None
    post_id: int
    similarity: float = Field(default=0.0, ge=0.0, le=1.0)
    rank: int = 1
    accepted: bool = True
    mismatch_reason: Optional[str] = None
