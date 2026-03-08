"""Live smoke tests for the AKOS control plane.

These tests hit actual HTTP endpoints and require a running server.
They are skipped unless the AKOS_LIVE_SMOKE environment variable is set to "1".

Run:
    AKOS_LIVE_SMOKE=1 python -m pytest tests/test_live_smoke.py -v
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

import pytest

LIVE_SMOKE = os.environ.get("AKOS_LIVE_SMOKE") == "1"
BASE_URL = "http://127.0.0.1:8420"

pytestmark = pytest.mark.live


def _get_json(path: str) -> dict | list:
    """Send a GET request and parse the JSON response."""
    url = f"{BASE_URL}{path}"
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))


@pytest.mark.skipif(not LIVE_SMOKE, reason="AKOS_LIVE_SMOKE not set")
def test_health_endpoint_live() -> None:
    data = _get_json("/health")
    assert isinstance(data, dict)
    assert data.get("status") == "ok"


@pytest.mark.skipif(not LIVE_SMOKE, reason="AKOS_LIVE_SMOKE not set")
def test_agents_endpoint_live() -> None:
    data = _get_json("/agents")
    assert isinstance(data, list)
    assert len(data) == 4, f"Expected 4 agents, got {len(data)}"
