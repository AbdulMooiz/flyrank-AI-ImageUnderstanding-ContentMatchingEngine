from __future__ import annotations

import base64
import json
from pathlib import Path

import httpx

from app.core.config import get_settings
from app.integrations.vision.base import VisionProviderError
from app.schemas.vision import VisionMetadata


class GeminiVisionProvider:
    def __init__(self, api_key: str | None = None, model_name: str | None = None, client: httpx.AsyncClient | None = None):
        settings = get_settings()
        self.api_key = api_key or settings.gemini_api_key
        self.model_name = model_name or settings.gemini_vision_model
        self.client = client or httpx.AsyncClient(timeout=30.0)

    async def analyze_image(self, image_path: str, source_url: str | None = None) -> VisionMetadata:
        if not self.api_key:
            raise VisionProviderError("Gemini API key missing", provider="gemini", retryable=False)

        file_path = Path(image_path)
        if not file_path.exists():
            raise VisionProviderError(f"Image file not found: {image_path}", provider="gemini", retryable=False)

        mime_type = "image/jpeg" if file_path.suffix.lower() in {".jpg", ".jpeg"} else "image/png"
        image_bytes = file_path.read_bytes()
        base64_data = base64.b64encode(image_bytes).decode("utf-8")

        payload = {
            "contents": [
                {
                    "parts": [
                        {"inline_data": {"mime_type": mime_type, "data": base64_data}},
                        {"text": "Return only valid JSON with this exact schema: {\"subject\": string, \"category\": string, \"attributes\": [string], \"caption\": string, \"confidence\": number between 0 and 1}. Do not include markdown and do not add extra keys."},
                    ]
                }
            ]
        }

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent?key={self.api_key}"
        response = await self.client.post(url, json=payload)
        if response.status_code >= 400:
            raise VisionProviderError(f"Gemini provider error: {response.text}", provider="gemini", retryable=True)

        try:
            data = response.json()
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            payload_obj = json.loads(text)
            return VisionMetadata.model_validate(payload_obj)
        except (KeyError, TypeError, ValueError, IndexError) as exc:
            raise VisionProviderError("Malformed Gemini response", provider="gemini", retryable=False) from exc
