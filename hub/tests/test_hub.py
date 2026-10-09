import os
import sys
from pathlib import Path

import httpx
import pytest
import respx
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
os.environ["GRID_ACCESS_TOKEN"] = "test-secret-token"

from hub.hub import app

client = TestClient(app)


def test_status_endpoint():
    resp = client.get("/status")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "GRID_ONLINE"


def test_proxy_generate_no_token():
    resp = client.post("/proxy/generate", json={"model": "m", "prompt": "hi"})
    assert resp.status_code in (401, 403)


def test_proxy_generate_invalid_token():
    resp = client.post(
        "/proxy/generate",
        json={"model": "m", "prompt": "hi"},
        headers={"Authorization": "Bearer wrong-token"},
    )
    assert resp.status_code == 401


@respx.mock
def test_proxy_generate_upstream_success():
    respx.post("http://localhost:11434/api/generate").mock(
        return_value=httpx.Response(200, json={"response": "hello from grid"})
    )

    resp = client.post(
        "/proxy/generate",
        json={"model": "llama3.2:1b", "prompt": "hello"},
        headers={"Authorization": "Bearer test-secret-token"},
    )
    assert resp.status_code == 200
    assert resp.json()["response"] == "hello from grid"


@respx.mock
def test_proxy_generate_upstream_error():
    respx.post("http://localhost:11434/api/generate").mock(
        side_effect=httpx.ConnectError("refused")
    )

    resp = client.post(
        "/proxy/generate",
        json={"model": "llama3.2:1b", "prompt": "hello"},
        headers={"Authorization": "Bearer test-secret-token"},
    )
    assert resp.status_code == 502
    assert resp.json()["detail"] == "Upstream request failed"


def test_proxy_generate_missing_required_fields():
    resp = client.post(
        "/proxy/generate",
        json={},
        headers={"Authorization": "Bearer test-secret-token"},
    )
    assert resp.status_code == 422
