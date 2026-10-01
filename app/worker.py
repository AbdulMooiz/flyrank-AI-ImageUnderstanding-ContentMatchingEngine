import asyncio
import logging

from app.workers.image_batch_job import run_batch_job

logging.basicConfig(level=logging.INFO)


def main() -> None:
    asyncio.run(run_batch_job())
    print("Background processing complete.")


if __name__ == "__main__":
    main()
