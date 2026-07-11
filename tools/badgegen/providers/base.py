"""Utilidades comunes de providers: errores y reintentos con backoff."""
from __future__ import annotations

import time

import httpx


class ProviderError(Exception):
    pass


def post_with_retry(client: httpx.Client, url: str, *, json: dict | None = None,
                    data: dict | None = None, files: dict | None = None,
                    headers: dict | None = None, retries: int = 3,
                    timeout: float = 120, sleep=time.sleep) -> httpx.Response:
    for attempt in range(retries + 1):
        response = client.post(url, json=json, data=data, files=files,
                               headers=headers, timeout=timeout)
        if response.status_code == 429 or response.status_code >= 500:
            if attempt == retries:
                raise ProviderError(
                    f"HTTP {response.status_code} tras {retries} reintentos: {response.text[:200]}"
                )
            sleep(2 ** (attempt + 1))
            continue
        if response.status_code >= 400:
            raise ProviderError(f"HTTP {response.status_code}: {response.text[:500]}")
        return response
    raise ProviderError("inalcanzable")
