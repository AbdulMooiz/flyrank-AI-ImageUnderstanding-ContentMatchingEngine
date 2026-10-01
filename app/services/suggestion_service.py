from __future__ import annotations

from typing import List

from sqlalchemy.orm import Session

from app.models.suggestion import Suggestion


class SuggestionService:
    def __init__(self, db: Session):
        self.db = db

    def list_recent(self, limit: int = 20) -> List[Suggestion]:
        return self.db.query(Suggestion).order_by(Suggestion.id.desc()).limit(limit).all()

    def create_suggestion(self, **data) -> Suggestion:
        suggestion = Suggestion(**data)
        self.db.add(suggestion)
        self.db.commit()
        self.db.refresh(suggestion)
        return suggestion
