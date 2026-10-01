from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.review import Review, ReviewDecision
from app.models.suggestion import Suggestion, SuggestionStatus
from app.services.suggestion_service import SuggestionService

router = APIRouter(prefix="/suggestions", tags=["suggestions"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("")
def list_suggestions(limit: int = 20, db: Session = Depends(get_db)):
    return SuggestionService(db).list_recent(limit=limit)


@router.post("/{suggestion_id}/approve")
def approve_suggestion(suggestion_id: int, db: Session = Depends(get_db)):
    suggestion = db.query(Suggestion).filter(Suggestion.id == suggestion_id).first()
    if not suggestion:
        raise HTTPException(status_code=404, detail="Suggestion not found")

    suggestion.status = SuggestionStatus.APPROVED
    review = db.query(Review).filter(Review.suggestion_id == suggestion_id).first()
    if review is None:
        review = Review(suggestion_id=suggestion_id, decision=ReviewDecision.APPROVED, reviewer="admin")
        db.add(review)
    else:
        review.decision = ReviewDecision.APPROVED
    db.commit()
    return {"status": "approved", "suggestion_id": suggestion_id}


@router.post("/{suggestion_id}/reject")
def reject_suggestion(suggestion_id: int, db: Session = Depends(get_db)):
    suggestion = db.query(Suggestion).filter(Suggestion.id == suggestion_id).first()
    if not suggestion:
        raise HTTPException(status_code=404, detail="Suggestion not found")

    suggestion.status = SuggestionStatus.REJECTED
    review = db.query(Review).filter(Review.suggestion_id == suggestion_id).first()
    if review is None:
        review = Review(suggestion_id=suggestion_id, decision=ReviewDecision.REJECTED, reviewer="admin")
        db.add(review)
    else:
        review.decision = ReviewDecision.REJECTED
    db.commit()
    return {"status": "rejected", "suggestion_id": suggestion_id}
