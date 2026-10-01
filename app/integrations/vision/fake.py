from __future__ import annotations

from pathlib import Path

from app.integrations.vision.base import VisionProviderError
from app.schemas.vision import VisionMetadata


class FakeVisionProvider:
    async def analyze_image(self, image_path: str, source_url: str | None = None) -> VisionMetadata:
        name = Path(image_path).name.lower()

        if "fox" in name:
            return VisionMetadata(
                subject="red fox",
                category="animal",
                attributes=["orange fur", "wild", "forest"],
                caption="A red fox standing in a forest",
                confidence=0.94,
            )
        if "wolf" in name:
            return VisionMetadata(
                subject="wolf",
                category="animal",
                attributes=["gray fur", "wild", "forest"],
                caption="A gray wolf in a forest",
                confidence=0.96,
            )
        if "dog" in name:
            return VisionMetadata(
                subject="dog",
                category="animal",
                attributes=["friendly", "domestic", "outdoor"],
                caption="A dog standing outdoors",
                confidence=0.91,
            )
        if "bear" in name:
            return VisionMetadata(
                subject="bear",
                category="animal",
                attributes=["large", "wild", "forest"],
                caption="A bear in a forest",
                confidence=0.92,
            )
        if "deer" in name:
            return VisionMetadata(
                subject="deer",
                category="animal",
                attributes=["brown fur", "wild", "meadow"],
                caption="A deer in a meadow",
                confidence=0.89,
            )
        if "invalid" in name:
            raise VisionProviderError("Malformed provider response", provider="fake", retryable=False)

        return VisionMetadata(
            subject="unknown animal",
            category="animal",
            attributes=["wild"],
            caption="An animal in the wild",
            confidence=0.68,
        )
