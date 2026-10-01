from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BatchJobRead(BaseModel):
    id: int
    job_type: str
    status: str
    total_count: int
    processed_count: int
    failed_count: int
    flagged_count: int
    remaining_count: int
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None

    class Config:
        orm_mode = True
