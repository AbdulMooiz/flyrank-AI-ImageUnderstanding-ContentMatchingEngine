from __future__ import annotations

from app.core.config import get_settings
from app.integrations.vision.base import VisionProviderError
from app.schemas.vision import VisionMetadata


class VisionProcessingService:
    def __init__(self, provider):
        self.provider = provider
        self.settings = get_settings()

    async def process_image(self, image_path: str, source_url: str | None = None) -> VisionMetadata:
        metadata = await self.provider.analyze_image(image_path, source_url=source_url)
        if metadata.confidence < self.settings.vision_confidence_threshold:
            metadata.model_extra = metadata.model_extra or {}
            metadata.model_extra["low_confidence"] = True
        return metadata

    async def validate_and_process(self, image_path: str, source_url: str | None = None) -> VisionMetadata:
        try:
            return await self.process_image(image_path, source_url=source_url)
        except VisionProviderError as exc:
            raise exc
