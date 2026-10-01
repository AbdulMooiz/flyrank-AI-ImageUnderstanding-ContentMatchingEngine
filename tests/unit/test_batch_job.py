import asyncio

from app.workers.image_batch_job import ImageBatchJob


def test_batch_job_processes_images() -> None:
    async def _run():
        job = ImageBatchJob()
        result = await job.process_batch()
        assert result.status == "completed"
        assert result.total_count >= 0

    asyncio.run(_run())
