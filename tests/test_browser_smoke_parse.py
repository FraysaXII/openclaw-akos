"""Regression tests for Playwright worker stdout parsing in scripts/browser-smoke.py."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


def _load_browser_smoke():
    path = REPO_ROOT / "scripts" / "browser-smoke.py"
    spec = importlib.util.spec_from_file_location("browser_smoke_under_test", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["browser_smoke_under_test"] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def browser_smoke_mod():
    return _load_browser_smoke()


def test_parse_json_results_from_stdout_valid(browser_smoke_mod):
    fn = browser_smoke_mod.parse_json_results_from_stdout
    raw = 'noise\nJSON_RESULTS:[{"scenario": "x", "status": "FAIL", "detail": "d"}]\n'
    out = fn(raw)
    assert out is not None
    assert len(out) == 1
    assert out[0]["scenario"] == "x"
    assert out[0]["status"] == "FAIL"


def test_parse_json_results_from_stdout_none(browser_smoke_mod):
    fn = browser_smoke_mod.parse_json_results_from_stdout
    assert fn(None) is None
    assert fn("") is None
    assert fn("no json line\n") is None


def test_parse_json_results_from_stdout_bad_json(browser_smoke_mod):
    fn = browser_smoke_mod.parse_json_results_from_stdout
    assert fn("JSON_RESULTS:not-json\n") is None
