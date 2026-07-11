"""Proveedor endpoint custom OpenAI-compatible (flux-klein y otros)."""
from __future__ import annotations

import base64
import os

import httpx

from badgegen.providers.base import post_with_retry

# Endpoints self-hosted cargan el modelo en frío: la primera generación puede
# tardar varios minutos.
DEFAULT_TIMEOUT = 600.0


class OpenAICompatProvider:
    name = "custom"

    def __init__(self, base_url: str, api_key: str, model: str,
                 size: str = "1024x1024", timeout: float | None = None,
                 client: httpx.Client | None = None):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model
        self.size = size
        self.timeout = timeout if timeout is not None else float(
            os.environ.get("CUSTOM_TIMEOUT", DEFAULT_TIMEOUT)
        )
        self.client = client or httpx.Client()

    def generate(self, prompt: str, reference_images: list[bytes], n: int = 1) -> list[bytes]:
        # Este endpoint no acepta imágenes de referencia; se ignoran.
        url = f"{self.base_url}/v1/images/generations"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        images: list[bytes] = []
        for _ in range(n):  # n=1 por petición: máxima compatibilidad
            response = post_with_retry(self.client, url, headers=headers, timeout=self.timeout, json={
                "model": self.model,
                "prompt": prompt,
                "n": 1,
                "size": self.size,
                "response_format": "b64_json",
            })
            images.append(base64.b64decode(response.json()["data"][0]["b64_json"]))
        return images
