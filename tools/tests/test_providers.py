import base64
import json

import httpx
import pytest

from badgegen.providers import get_provider
from badgegen.providers.base import ProviderError, post_with_retry
from badgegen.providers.gemini import GeminiProvider
from badgegen.providers.openai_compat import OpenAICompatProvider

PNG = b"\x89PNG-fake-bytes"
PNG_B64 = base64.b64encode(PNG).decode()


def _client(handler):
    return httpx.Client(transport=httpx.MockTransport(handler))


def test_retry_then_success():
    calls = {"n": 0}
    sleeps = []

    def handler(request):
        calls["n"] += 1
        if calls["n"] < 3:
            return httpx.Response(429)
        return httpx.Response(200, json={"ok": True})

    resp = post_with_retry(_client(handler), "http://x/y", json={}, sleep=sleeps.append)
    assert resp.status_code == 200 and calls["n"] == 3
    assert sleeps == [2, 4]


def test_4xx_raises_without_retry():
    def handler(request):
        return httpx.Response(400, text="bad prompt")

    with pytest.raises(ProviderError, match="bad prompt"):
        post_with_retry(_client(handler), "http://x/y", json={}, sleep=lambda s: None)


def test_retries_exhausted_raises():
    calls = {"n": 0}
    sleeps = []

    def handler(request):
        calls["n"] += 1
        return httpx.Response(500, text="boom")

    with pytest.raises(ProviderError, match="3 reintentos"):
        post_with_retry(_client(handler), "http://x/y", json={}, sleep=sleeps.append)
    assert calls["n"] == 4
    assert sleeps == [2, 4, 8]


def test_gemini_generate_parses_inline_data():
    seen = {}

    def handler(request):
        seen["body"] = json.loads(request.content)
        seen["key"] = request.headers.get("x-goog-api-key")
        seen["url"] = str(request.url)
        return httpx.Response(200, json={
            "candidates": [{"content": {"parts": [
                {"text": "aquí tienes"},
                {"inlineData": {"mimeType": "image/png", "data": PNG_B64}},
            ]}}]
        })

    p = GeminiProvider("KEY", client=_client(handler))
    out = p.generate("un badge", [b"ref-bytes"], n=2)
    assert out == [PNG, PNG]
    assert seen["key"] == "KEY"
    parts = seen["body"]["contents"][0]["parts"]
    assert parts[0]["text"].startswith("un badge")
    assert "style reference" in parts[0]["text"]  # nota de estilo al llevar referencias
    assert parts[1]["inline_data"]["data"] == base64.b64encode(b"ref-bytes").decode()
    from badgegen.providers.gemini import DEFAULT_MODEL

    assert f"{DEFAULT_MODEL}:generateContent" in seen["url"]


def test_gemini_no_image_in_response_raises():
    def handler(request):
        return httpx.Response(200, json={"candidates": [{"content": {"parts": [{"text": "no puedo"}]}}]})

    with pytest.raises(ProviderError, match="sin imagen"):
        GeminiProvider("KEY", client=_client(handler)).generate("x", [], n=1)


def test_openai_compat_generate():
    seen = {}

    def handler(request):
        seen["auth"] = request.headers.get("authorization")
        seen["body"] = json.loads(request.content)
        seen["url"] = str(request.url)
        return httpx.Response(200, json={"data": [{"b64_json": PNG_B64}]})

    p = OpenAICompatProvider("http://flux.local/", "TOKEN", "flux-klein", client=_client(handler))
    out = p.generate("un badge", [], n=1)  # sin referencias → /generations
    assert out == [PNG]
    assert seen["url"] == "http://flux.local/v1/images/generations"
    assert seen["auth"] == "Bearer TOKEN"
    assert seen["body"]["model"] == "flux-klein" and seen["body"]["n"] == 1
    assert seen["body"]["response_format"] == "b64_json"
    assert seen["body"]["prompt"] == "un badge"
    assert seen["body"]["size"] == "1024x1024"


def test_openai_compat_edits_with_reference():
    seen = {}

    def handler(request):
        seen["url"] = str(request.url)
        seen["content_type"] = request.headers.get("content-type", "")
        seen["content"] = request.content
        return httpx.Response(200, json={"data": [{"b64_json": PNG_B64}]})

    p = OpenAICompatProvider("http://flux.local", "TOKEN", "flux-klein", client=_client(handler))
    out = p.generate("un badge nuevo", [b"ref-style-bytes"], n=1)
    assert out == [PNG]
    assert seen["url"] == "http://flux.local/v1/images/edits"
    assert seen["content_type"].startswith("multipart/form-data")
    assert b"ref-style-bytes" in seen["content"]        # la referencia viaja
    assert b"un badge nuevo" in seen["content"]         # el prompt original
    assert b"do NOT copy its content" in seen["content"]  # instrucción de estilo
    assert b"flux-klein" in seen["content"]


def test_openai_compat_edits_404_falls_back_to_generations():
    urls = []

    def handler(request):
        urls.append(request.url.path)
        if request.url.path.endswith("/edits"):
            return httpx.Response(404, text="not found")
        return httpx.Response(200, json={"data": [{"b64_json": PNG_B64}]})

    p = OpenAICompatProvider("http://flux.local", "TOKEN", "flux-klein", client=_client(handler))
    out = p.generate("un badge", [b"ref"], n=2)
    assert out == [PNG, PNG]
    # tras el primer 404 no reintenta /edits
    assert urls == ["/v1/images/edits", "/v1/images/generations", "/v1/images/generations"]


def test_get_provider_factory(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "G")
    monkeypatch.setenv("CUSTOM_BASE_URL", "http://flux.local")
    monkeypatch.setenv("CUSTOM_API_KEY", "C")
    monkeypatch.setenv("CUSTOM_IMAGE_MODEL", "flux-klein")
    assert get_provider(None).name == "gemini"
    assert get_provider("custom").model == "flux-klein"
    assert get_provider("custom", model="otro").model == "otro"
    monkeypatch.delenv("GEMINI_API_KEY")
    with pytest.raises(ProviderError, match="GEMINI_API_KEY"):
        get_provider("gemini")
