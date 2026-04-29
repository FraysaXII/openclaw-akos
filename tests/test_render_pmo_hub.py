"""Tests for scripts/render_pmo_hub.py (Initiative 25 P5).

Locks in the auto-gen marker contract:
- `find_markers` returns (start, end) when both markers present and ordered.
- `find_markers` returns None on missing or inverted markers.
- `render_body` is deterministic for fixed inputs.
- `render_section_with_markers` produces a sha256 that round-trips.
- `cmd_check_only` PASSes when the hub file's recorded sha256 matches the
  rendered body; FAILs (rc=1) on drift; FAILs on missing markers.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = REPO_ROOT / "scripts" / "render_pmo_hub.py"


@pytest.fixture(scope="module")
def pmo_hub_module():
    spec = importlib.util.spec_from_file_location(
        "render_pmo_hub_under_test", SCRIPT_PATH
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["render_pmo_hub_under_test"] = module
    spec.loader.exec_module(module)
    return module


def test_section_id_constant(pmo_hub_module):
    assert pmo_hub_module.SECTION_ID == "pmo_stakeholder_index_v1"


def test_find_markers_returns_none_on_missing(pmo_hub_module):
    assert pmo_hub_module.find_markers("no markers here") is None
    assert pmo_hub_module.find_markers("<!-- BEGIN_AUTOGEN section_id=pmo_stakeholder_index_v1 generated_by=x -->") is None


def test_find_markers_returns_span_on_balanced(pmo_hub_module):
    text = (
        "prefix\n"
        "<!-- BEGIN_AUTOGEN section_id=pmo_stakeholder_index_v1 generated_by=x -->\n"
        "body\n"
        "<!-- END_AUTOGEN section_id=pmo_stakeholder_index_v1 -->\n"
        "suffix\n"
    )
    span = pmo_hub_module.find_markers(text)
    assert span is not None
    start, end = span
    assert start < end
    assert "BEGIN_AUTOGEN" in text[start:end]
    assert "END_AUTOGEN" in text[start:end]


def test_find_markers_rejects_inverted_order(pmo_hub_module):
    text = (
        "<!-- END_AUTOGEN section_id=pmo_stakeholder_index_v1 -->\n"
        "<!-- BEGIN_AUTOGEN section_id=pmo_stakeholder_index_v1 generated_by=x -->\n"
    )
    assert pmo_hub_module.find_markers(text) is None


def test_render_body_is_deterministic(pmo_hub_module):
    body1 = pmo_hub_module.render_body()
    body2 = pmo_hub_module.render_body()
    assert body1 == body2


def test_render_section_with_markers_sha_matches_body(pmo_hub_module):
    import hashlib

    body = "test body content\n"
    full, sha = pmo_hub_module.render_section_with_markers(body)
    assert hashlib.sha256(body.encode("utf-8")).hexdigest() == sha
    assert "BEGIN_AUTOGEN" in full
    assert "END_AUTOGEN" in full
    assert sha in full


def test_cmd_check_only_pass_when_sha_matches(pmo_hub_module, capsys):
    """The committed `TOPIC_PMO_CLIENT_DELIVERY_HUB.md` should have a sha that matches the current rendered body."""
    if not pmo_hub_module.HUB_PATH.is_file():
        pytest.skip("TOPIC_PMO_CLIENT_DELIVERY_HUB.md not present in this checkout")
    text = pmo_hub_module.HUB_PATH.read_text(encoding="utf-8")
    rc = pmo_hub_module.cmd_check_only(text)
    captured = capsys.readouterr()
    # If sha matches, rc=0 PASS. If hub has not been auto-rendered yet, sha may
    # be missing -> WARN with rc=0. Either is acceptable; rc=1 only on drift.
    assert rc == 0, f"PMO hub auto-gen drift detected:\n{captured.out}"


def test_cmd_check_only_fail_on_missing_markers(pmo_hub_module, capsys):
    rc = pmo_hub_module.cmd_check_only("file with no markers")
    captured = capsys.readouterr()
    assert rc == 1
    assert "MARKER_NOT_FOUND" in captured.out
