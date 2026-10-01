from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.batch_job import BatchJob
from app.schemas.job import BatchJobRead
from app.workers.image_batch_job import run_batch_job

router = APIRouter(prefix="/jobs", tags=["jobs"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("", response_model=list[BatchJobRead])
def list_jobs(db: Session = Depends(get_db)):
    return db.query(BatchJob).order_by(BatchJob.id.desc()).all()


@router.get("/{job_id}", response_model=BatchJobRead)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(BatchJob).filter(BatchJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.post("/run", response_model=BatchJobRead)
async def run_job():
    job = await run_batch_job()
    return job


@router.post("/images/process", response_model=BatchJobRead)
async def process_images_job():
    return await run_batch_job()
