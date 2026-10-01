from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class CostSummary(BaseModel):
    total_cost: float
    total_tokens: int
    total_requests: int
    window_start: datetime
    window_end: datetime
    model: str = "gemini"
