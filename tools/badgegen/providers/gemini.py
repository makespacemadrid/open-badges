"""Proveedor nano banana: API Gemini de generación de imagen, REST directo."""
from __future__ import annotations

import base64

import httpx

from badgegen.providers.base import ProviderError, post_with_retry

API_BASE = "https://generativelanguage.googleapis.com/v1beta"
DEFAULT_MODEL = "gemini-3.1-flash-image"


class GeminiProvider:
    name = "gemini"

    def __init__(self, api_key: str, model: str = DEFAULT_MODEL,
                 client: httpx.Client | None = None):
        self.api_key = api_key
        self.model = model
        self.client = client or httpx.Client()

    def generate(self, prompt: str, reference_images: list[bytes], n: int = 1) -> list[bytes]:
        parts: list[dict] = [{"text": prompt}]
        for ref in reference_images:
            parts.append({"inline_data": {
                "mime_type": "image/png",
                "data": base64.b64encode(ref).decode(),
            }})
        url = f"{API_BASE}/models/{self.model}:generateContent"
        headers = {"x-goog-api-key": self.api_key}
        images: list[bytes] = []
        for _ in range(n):
            response = post_with_retry(
                self.client, url, json={"contents": [{"parts": parts}]}, headers=headers
            )
            images.append(self._extract_image(response.json()))
        return images

    @staticmethod
    def _extract_image(data: dict) -> bytes:
        for candidate in data.get("candidates", []):
            for part in candidate.get("content", {}).get("parts", []):
                blob = part.get("inlineData") or part.get("inline_data")
                if blob and blob.get("data"):
                    return base64.b64decode(blob["data"])
        raise ProviderError(f"respuesta sin imagen: {str(data)[:300]}")
