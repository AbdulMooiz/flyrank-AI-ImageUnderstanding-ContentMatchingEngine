from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.post import PostCreate, PostRead
from app.services.post_service import PostService

router = APIRouter(prefix="/posts", tags=["posts"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("", response_model=list[PostRead])
def list_posts(db: Session = Depends(get_db)):
    return PostService(db).list_posts()


@router.get("/{post_id}", response_model=PostRead)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = PostService(db).get_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.post("", response_model=PostRead, status_code=201)
def create_post(payload: PostCreate, db: Session = Depends(get_db)):
    return PostService(db).create_post(payload.model_dump())


@router.get("/{post_id}/images")
def list_images_for_post(post_id: int, db: Session = Depends(get_db)):
    images = PostService(db).get_related_images(post_id)
    return [{"id": item.id, "filename": item.filename, "status": item.status.value if hasattr(item.status, "value") else str(item.status)} for item in images]
