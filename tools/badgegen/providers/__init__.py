from __future__ import annotations

import os

from badgegen.providers.base import ProviderError
from badgegen.providers.gemini import DEFAULT_MODEL, GeminiProvider
from badgegen.providers.openai_compat import OpenAICompatProvider


def _require(var: str) -> str:
    value = os.environ.get(var)
    if not value:
        raise ProviderError(f"falta {var} en tools/.env")
    return value


def get_provider(name: str | None, model: str | None = None):
    name = name or "gemini"
    if name == "gemini":
        return GeminiProvider(_require("GEMINI_API_KEY"),
                              model=model or os.environ.get("GEMINI_IMAGE_MODEL") or DEFAULT_MODEL)
    if name == "custom":
        return OpenAICompatProvider(
            _require("CUSTOM_BASE_URL"),
            _require("CUSTOM_API_KEY"),
            model=model or _require("CUSTOM_IMAGE_MODEL"),
            size=os.environ.get("CUSTOM_IMAGE_SIZE", "1024x1024"),
        )
    raise ProviderError(f"proveedor desconocido: {name} (usa gemini|custom)")
