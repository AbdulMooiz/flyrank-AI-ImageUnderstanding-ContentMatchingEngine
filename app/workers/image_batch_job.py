from __future__ import annotations

import asyncio
import logging
from datetime import datetime

from app.core.config import get_settings
from app.db.session import SessionLocal
from app.integrations.vision.fake import FakeVisionProvider
from app.models.batch_job import BatchJob
from app.models.image import Image, ImageStatus

logger = logging.getLogger(__name__)


class ImageBatchJob:
    def __init__(self, provider=None, db_session=None):
        self.provider = provider or FakeVisionProvider()
        self.db_session = db_session or SessionLocal()
        self.settings = get_settings()

    async def process_batch(self) -> BatchJob:
        job = BatchJob(job_type="image_processing", status="running", total_count=0, processed_count=0, failed_count=0, flagged_count=0, remaining_count=0, started_at=datetime.utcnow())
        self.db_session.add(job)
        self.db_session.commit()
        self.db_session.refresh(job)

        images = self.db_session.query(Image).all()
        job.total_count = len(images)
        job.remaining_count = len(images)
        self.db_session.commit()

        for image in images:
            if image.status == ImageStatus.PROCESSED:
                continue
            image.status = ImageStatus.PROCESSING
            self.db_session.add(image)
            self.db_session.commit()
            try:
                metadata = await self.provider.analyze_image(image.original_path or image.filename)
                image.status = ImageStatus.PROCESSED if metadata.confidence >= self.settings.vision_confidence_threshold else ImageStatus.FLAGGED
                image.error_message = None
                self.db_session.add(image)
                self.db_session.commit()
                job.processed_count += 1
                if image.status == ImageStatus.FLAGGED:
                    job.flagged_count += 1
            except Exception as exc:
                image.status = ImageStatus.FAILED
                image.error_message = str(exc)
                self.db_session.add(image)
                self.db_session.commit()
                job.failed_count += 1
                logger.warning("Image processing failed: %s", exc)
            finally:
                job.remaining_count = max(0, job.total_count - (job.processed_count + job.failed_count + job.flagged_count))
                self.db_session.add(job)
                self.db_session.commit()

        job.status = "completed"
        job.finished_at = datetime.utcnow()
        self.db_session.add(job)
        self.db_session.commit()
        self.db_session.close()
        return job


async def run_batch_job() -> BatchJob:
    job = ImageBatchJob()
    return await job.process_batch()
