from __future__ import annotations

from typing import List

from sqlalchemy.orm import Session

from app.models.image import Image
from app.models.post import Post


class PostService:
    def __init__(self, db: Session):
        self.db = db

    def list_posts(self) -> List[Post]:
        return self.db.query(Post).order_by(Post.id.asc()).all()

    def get_post(self, post_id: int) -> Post | None:
        return self.db.query(Post).filter(Post.id == post_id).first()

    def get_related_images(self, post_id: int) -> List[Image]:
        post = self.get_post(post_id)
        if not post:
            return []
        return self.db.query(Image).filter(Image.post_id == post.id).order_by(Image.id.asc()).all()

    def create_post(self, data: dict) -> Post:
        post = Post(**data)
        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)
        return post
