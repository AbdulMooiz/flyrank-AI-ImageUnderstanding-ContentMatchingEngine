from __future__ import annotations

from app.core.config import get_settings
from app.db.session import SessionLocal
from app.models.image import Image, ImageMetadata, ImageStatus
from app.models.post import Post


def seed() -> None:
    db = SessionLocal()
    try:
        if db.query(Post).count() == 0:
            posts = [
                Post(title="Red fox behavior in forests", content="The behavior of red foxes in forests and their role in the ecosystem."),
                Post(title="Wolf pack dynamics", content="Wolf social structure and pack hunting behavior in cold climates."),
                Post(title="Dog companionship", content="How dogs interact with humans and the concept of loyalty."),
                Post(title="Bear habitat and foraging", content="Bears searching for food in forested terrain.")
            ]
            db.add_all(posts)
            db.commit()

        if db.query(Image).count() == 0:
            images = [
                Image(external_id="fox-01", filename="fox-01.jpg", source_url="https://example.com/fox-01.jpg", original_path="/tmp/fox-01.jpg", status=ImageStatus.PROCESSED),
                Image(external_id="wolf-01", filename="wolf-01.jpg", source_url="https://example.com/wolf-01.jpg", original_path="/tmp/wolf-01.jpg", status=ImageStatus.PROCESSED),
                Image(external_id="dog-01", filename="dog-01.jpg", source_url="https://example.com/dog-01.jpg", original_path="/tmp/dog-01.jpg", status=ImageStatus.PROCESSED),
                Image(external_id="bear-01", filename="bear-01.jpg", source_url="https://example.com/bear-01.jpg", original_path="/tmp/bear-01.jpg", status=ImageStatus.PROCESSED),
                Image(external_id="deer-01", filename="deer-01.jpg", source_url="https://example.com/deer-01.jpg", original_path="/tmp/deer-01.jpg", status=ImageStatus.PROCESSED),
            ]
            db.add_all(images)
            db.commit()

            metadata_records = [
                ImageMetadata(image_id=images[0].id, subject="red fox", category="animal", attributes=["orange fur", "wild", "forest"], caption="A red fox standing in a forest", confidence=0.94),
                ImageMetadata(image_id=images[1].id, subject="wolf", category="animal", attributes=["gray fur", "wild", "forest"], caption="A gray wolf in a forest", confidence=0.95),
                ImageMetadata(image_id=images[2].id, subject="dog", category="animal", attributes=["friendly", "domestic", "outdoor"], caption="A dog lying outdoors", confidence=0.91),
                ImageMetadata(image_id=images[3].id, subject="bear", category="animal", attributes=["large", "forest", "wild"], caption="A bear in a forest", confidence=0.93),
                ImageMetadata(image_id=images[4].id, subject="deer", category="animal", attributes=["brown fur", "wild", "meadow"], caption="A deer in a meadow", confidence=0.92),
            ]
            db.add_all(metadata_records)
            db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    settings = get_settings()
    print(f"Seeding data using {settings.database_url}")
    seed()
    print("Seed data complete.")
