import json

import httpx
import pytest

from badgegen import qc
from badgegen.providers.base import ProviderError


def _client(handler):
    return httpx.Client(transport=httpx.MockTransport(handler))


def test_judge_parses_json_verdict():
    seen = {}

    def handler(request):
        seen["body"] = json.loads(request.content)
        verdict = json.dumps({"score": 2, "issues": ["texto ilegible", "tipografía rota"]})
        return httpx.Response(200, json={
            "candidates": [{"content": {"parts": [{"text": verdict}]}}]
        })

    r = qc.judge_legibility(b"png-bytes", "KEY", client=_client(handler))
    assert r.score == 2
    assert "texto ilegible" in r.issues
    cfg = seen["body"]["generationConfig"]
    assert cfg["responseMimeType"] == "application/json"
    parts = seen["body"]["contents"][0]["parts"]
    assert any("inline_data" in p for p in parts)


def test_judge_invalid_json_raises():
    def handler(request):
        return httpx.Response(200, json={
            "candidates": [{"content": {"parts": [{"text": "esto no es json"}]}}]
        })

    with pytest.raises(ProviderError):
        qc.judge_legibility(b"png", "KEY", client=_client(handler))
