"""Golden corpus for intent regex routing (Initiative 13 — before/after benchmark).

CI always runs these against ``_classify_regex`` and ``classify_request`` (regex fallback).
For **embedding** before/after when Ollama is up, compare ``pytest -v tests/test_intent_golden.py``
output or run ``py scripts/intent_benchmark.py`` (if present) and save deltas under
``docs/wip/planning/13-madeira-research-followthrough/reports/``.
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest

pytestmark = pytest.mark.intent

from akos.intent import _classify_regex, classify_request

_FIXTURE = Path(__file__).resolve().parent / "fixtures" / "intent_golden.json"


def _load_cases():
    data = json.loads(_FIXTURE.read_text(encoding="utf-8"))
    return data["cases"]


@pytest.mark.parametrize("case", _load_cases(), ids=lambda c: c["id"])
def test_golden_regex_route(case):
    assert _classify_regex(case["query"]) == case["expect_regex_route"]


@pytest.mark.parametrize("case", _load_cases(), ids=lambda c: f"classify_{c['id']}")
def test_golden_classify_request_regex_fallback(case):
    with patch("akos.intent._get_classifier", return_value=None):
        result = classify_request(case["query"])
        assert result["route"] == case["expect_regex_route"]
        assert result["method"] == "regex"
