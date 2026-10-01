from __future__ import annotations

from typing import Protocol

from app.schemas.vision import VisionMetadata


class VisionProviderError(Exception):
    def __init__(self, message: str, *, provider: str | None = None, retryable: bool = False):
        super().__init__(message)
        self.provider = provider
        self.retryable = retryable


class VisionProvider(Protocol):
    async def analyze_image(self, image_path: str, source_url: str | None = None) -> VisionMetadata:
        ...
