from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.cost import CostSummary
from app.services.cost_service import CostService

router = APIRouter(prefix="/costs", tags=["costs"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("", response_model=CostSummary)
def get_cost_summary(db: Session = Depends(get_db)):
    result = CostService(db).summary(window_start=datetime.utcnow(), window_end=datetime.utcnow())
    return CostSummary(**result)
