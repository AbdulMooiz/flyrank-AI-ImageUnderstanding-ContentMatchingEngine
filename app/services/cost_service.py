from __future__ import annotations

from datetime import datetime

from sqlalchemy.orm import Session


class CostService:
    def __init__(self, db: Session):
        self.db = db

    def summary(self, window_start: datetime | None = None, window_end: datetime | None = None) -> dict:
        window_start = window_start or datetime.utcnow()
        window_end = window_end or datetime.utcnow()
        return {
            "total_cost": 0.0,
            "total_tokens": 0,
            "total_requests": 0,
            "window_start": window_start,
            "window_end": window_end,
            "model": "gemini",
        }
