"""Proveedor endpoint custom OpenAI-compatible (flux-klein y otros)."""
from __future__ import annotations

import base64
import os

import httpx

from badgegen.providers.base import ProviderError, post_with_retry

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
        # Si el endpoint no implementa /v1/images/edits, se degrada a
        # /v1/images/generations (sin referencia) tras el primer 404.
        self._edits_supported = True

    def generate(self, prompt: str, reference_images: list[bytes], n: int = 1) -> list[bytes]:
        images: list[bytes] = []
        for _ in range(n):  # n=1 por petición: máxima compatibilidad
            if reference_images and self._edits_supported:
                try:
                    images.append(self._edit_one(prompt, reference_images[0]))
                    continue
                except ProviderError as exc:
                    if "404" not in str(exc):
                        raise
                    self._edits_supported = False
            images.append(self._generate_one(prompt))
        return images

    def _headers(self) -> dict:
        return {"Authorization": f"Bearer {self.api_key}"}

    def _generate_one(self, prompt: str) -> bytes:
        response = post_with_retry(
            self.client, f"{self.base_url}/v1/images/generations",
            headers=self._headers(), timeout=self.timeout, json={
                "model": self.model,
                "prompt": prompt,
                "n": 1,
                "size": self.size,
                "response_format": "b64_json",
            })
        return base64.b64decode(response.json()["data"][0]["b64_json"])

    def _edit_one(self, prompt: str, reference: bytes) -> bytes:
        """img2img con la primera imagen de referencia como ancla de estilo."""
        styled_prompt = (
            "Create a completely NEW image in EXACTLY the same visual style as the "
            "attached reference badge (same palette, line weight, ring and typography "
            "style) but do NOT copy its content, motif or text. New badge:\n" + prompt
        )
        response = post_with_retry(
            self.client, f"{self.base_url}/v1/images/edits",
            headers=self._headers(), timeout=self.timeout,
            files={"image": ("reference.png", reference, "image/png")},
            data={
                "model": self.model,
                "prompt": styled_prompt,
                "n": "1",
                "size": self.size,
                "response_format": "b64_json",
            })
        return base64.b64decode(response.json()["data"][0]["b64_json"])
