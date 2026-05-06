"""Initiative 59 P4 — tests for scripts/render_operator_inbox.py."""

from __future__ import annotations

import csv
import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

# Load the renderer as a module without invoking its CLI.
_RENDER_MODULE_SPEC = importlib.util.spec_from_file_location(
    "render_operator_inbox_under_test",
    REPO_ROOT / "scripts" / "render_operator_inbox.py",
)
assert _RENDER_MODULE_SPEC is not None and _RENDER_MODULE_SPEC.loader is not None
_renderer = importlib.util.module_from_spec(_RENDER_MODULE_SPEC)
sys.modules["render_operator_inbox_under_test"] = _renderer
_RENDER_MODULE_SPEC.loader.exec_module(_renderer)


def _seed_csvs(tmp_path: Path, ops_rows: list[dict[str, str]], init_rows: list[dict[str, str]]) -> None:
    ops_path = tmp_path / "OPS_REGISTER.csv"
    init_path = tmp_path / "INITIATIVE_REGISTRY.csv"
    org_path = tmp_path / "baseline_organisation.csv"
    ops_fields = list(ops_rows[0].keys()) if ops_rows else ["ops_action_id", "status", "owner_class"]
    with ops_path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=ops_fields, lineterminator="\n")
        w.writeheader()
        for r in ops_rows:
            w.writerow(r)
    init_fields = list(init_rows[0].keys()) if init_rows else ["initiative_id", "title"]
    with init_path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=init_fields, lineterminator="\n")
        w.writeheader()
        for r in init_rows:
            w.writerow(r)
    with org_path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["role_name", "display_name"], lineterminator="\n")
        w.writeheader()
        w.writerow({"role_name": "PMO", "display_name": "Programme Management Office"})


def _redirect_paths(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(_renderer, "OPS_REGISTER_CSV", tmp_path / "OPS_REGISTER.csv")
    monkeypatch.setattr(_renderer, "INITIATIVE_REGISTRY_CSV", tmp_path / "INITIATIVE_REGISTRY.csv")
    monkeypatch.setattr(_renderer, "ORG_CSV", tmp_path / "baseline_organisation.csv")
    monkeypatch.setattr(_renderer, "INBOX_PATH", tmp_path / "OPERATOR_INBOX.md")


def test_filter_only_open_operator_or_mixed(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    ops_rows = [
        {"ops_action_id": "OPS-58-2", "title": "Rotate OpenAI key", "originating_initiative_id": "INIT-OPENCLAW_AKOS-58", "forwarded_to_initiative_id": "", "owner_class": "operator", "owner_role": "PMO", "status": "open", "rice_score": "144", "rice_impact": "", "linked_decision_ids": "", "linked_policies": "", "originating_at": "", "closed_at": "", "notes": "high"},
        {"ops_action_id": "OPS-99-1", "title": "engineering only", "originating_initiative_id": "INIT-OPENCLAW_AKOS-99", "forwarded_to_initiative_id": "", "owner_class": "engineering", "owner_role": "PMO", "status": "open", "rice_score": "200", "rice_impact": "", "linked_decision_ids": "", "linked_policies": "", "originating_at": "", "closed_at": "", "notes": ""},
        {"ops_action_id": "OPS-99-2", "title": "closed already", "originating_initiative_id": "INIT-OPENCLAW_AKOS-99", "forwarded_to_initiative_id": "", "owner_class": "operator", "owner_role": "PMO", "status": "closed", "rice_score": "10", "rice_impact": "", "linked_decision_ids": "", "linked_policies": "", "originating_at": "", "closed_at": "2026-05-01", "notes": ""},
        {"ops_action_id": "OPS-58-4", "title": "GraphRAG", "originating_initiative_id": "INIT-OPENCLAW_AKOS-58", "forwarded_to_initiative_id": "", "owner_class": "mixed", "owner_role": "PMO", "status": "open", "rice_score": "15", "rice_impact": "", "linked_decision_ids": "", "linked_policies": "", "originating_at": "", "closed_at": "", "notes": ""},
    ]
    init_rows = [
        {"initiative_id": "INIT-OPENCLAW_AKOS-58", "title": "Cycle 2"},
        {"initiative_id": "INIT-OPENCLAW_AKOS-99", "title": "Test 99"},
    ]
    _seed_csvs(tmp_path, ops_rows, init_rows)
    _redirect_paths(tmp_path, monkeypatch)

    block, count = _renderer._render_block()
    assert count == 2
    assert "OPS-58-2" in block
    assert "OPS-58-4" in block
    assert "OPS-99-1" not in block
    assert "OPS-99-2" not in block


def test_rice_desc_sort(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    ops_rows = [
        {"ops_action_id": "OPS-A", "title": "low", "originating_initiative_id": "INIT-OPENCLAW_AKOS-58", "forwarded_to_initiative_id": "", "owner_class": "operator", "owner_role": "PMO", "status": "open", "rice_score": "10", "rice_impact": "", "linked_decision_ids": "", "linked_policies": "", "originating_at": "", "closed_at": "", "notes": ""},
        {"ops_action_id": "OPS-B", "title": "high", "originating_initiative_id": "INIT-OPENCLAW_AKOS-58", "forwarded_to_initiative_id": "", "owner_class": "operator", "owner_role": "PMO", "status": "open", "rice_score": "144", "rice_impact": "", "linked_decision_ids": "", "linked_policies": "", "originating_at": "", "closed_at": "", "notes": ""},
        {"ops_action_id": "OPS-C", "title": "mid", "originating_initiative_id": "INIT-OPENCLAW_AKOS-58", "forwarded_to_initiative_id": "", "owner_class": "operator", "owner_role": "PMO", "status": "open", "rice_score": "70", "rice_impact": "", "linked_decision_ids": "", "linked_policies": "", "originating_at": "", "closed_at": "", "notes": ""},
    ]
    init_rows = [{"initiative_id": "INIT-OPENCLAW_AKOS-58", "title": "Cycle 2"}]
    _seed_csvs(tmp_path, ops_rows, init_rows)
    _redirect_paths(tmp_path, monkeypatch)

    block, count = _renderer._render_block()
    assert count == 3
    assert block.index("OPS-B") < block.index("OPS-C") < block.index("OPS-A")


def test_initiative_title_join(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    ops_rows = [
        {"ops_action_id": "OPS-58-2", "title": "Rotate OpenAI key", "originating_initiative_id": "INIT-OPENCLAW_AKOS-58", "forwarded_to_initiative_id": "", "owner_class": "operator", "owner_role": "PMO", "status": "open", "rice_score": "144", "rice_impact": "", "linked_decision_ids": "", "linked_policies": "", "originating_at": "", "closed_at": "", "notes": ""},
    ]
    init_rows = [{"initiative_id": "INIT-OPENCLAW_AKOS-58", "title": "Cycle 2 — multi-track forward"}]
    _seed_csvs(tmp_path, ops_rows, init_rows)
    _redirect_paths(tmp_path, monkeypatch)

    block, _ = _renderer._render_block()
    assert "Cycle 2 — multi-track forward" in block


def test_owner_role_label_join(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    ops_rows = [
        {"ops_action_id": "OPS-58-2", "title": "x", "originating_initiative_id": "INIT-OPENCLAW_AKOS-58", "forwarded_to_initiative_id": "", "owner_class": "operator", "owner_role": "PMO", "status": "open", "rice_score": "144", "rice_impact": "", "linked_decision_ids": "", "linked_policies": "", "originating_at": "", "closed_at": "", "notes": ""},
    ]
    init_rows = [{"initiative_id": "INIT-OPENCLAW_AKOS-58", "title": "Cycle 2"}]
    _seed_csvs(tmp_path, ops_rows, init_rows)
    _redirect_paths(tmp_path, monkeypatch)

    block, _ = _renderer._render_block()
    assert "operator (Programme Management Office)" in block


def test_determinism(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    ops_rows = [
        {"ops_action_id": "OPS-58-2", "title": "Rotate OpenAI key", "originating_initiative_id": "INIT-OPENCLAW_AKOS-58", "forwarded_to_initiative_id": "", "owner_class": "operator", "owner_role": "PMO", "status": "open", "rice_score": "144", "rice_impact": "", "linked_decision_ids": "", "linked_policies": "", "originating_at": "", "closed_at": "", "notes": ""},
    ]
    init_rows = [{"initiative_id": "INIT-OPENCLAW_AKOS-58", "title": "Cycle 2"}]
    _seed_csvs(tmp_path, ops_rows, init_rows)
    _redirect_paths(tmp_path, monkeypatch)

    a, _ = _renderer._render_full()
    b, _ = _renderer._render_full()
    assert a == b
    assert _renderer._sha256(a) == _renderer._sha256(b)


def test_empty_when_nothing_open(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    ops_rows = [
        {"ops_action_id": "OPS-99-1", "title": "engineering only", "originating_initiative_id": "INIT-OPENCLAW_AKOS-99", "forwarded_to_initiative_id": "", "owner_class": "engineering", "owner_role": "PMO", "status": "open", "rice_score": "200", "rice_impact": "", "linked_decision_ids": "", "linked_policies": "", "originating_at": "", "closed_at": "", "notes": ""},
    ]
    init_rows = [{"initiative_id": "INIT-OPENCLAW_AKOS-99", "title": "Test 99"}]
    _seed_csvs(tmp_path, ops_rows, init_rows)
    _redirect_paths(tmp_path, monkeypatch)

    block, count = _renderer._render_block()
    assert count == 0
    assert "_No open operator/mixed actions._" in block


def test_missing_csv_files_graceful(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(_renderer, "OPS_REGISTER_CSV", tmp_path / "missing.csv")
    monkeypatch.setattr(_renderer, "INITIATIVE_REGISTRY_CSV", tmp_path / "missing.csv")
    monkeypatch.setattr(_renderer, "ORG_CSV", tmp_path / "missing.csv")
    monkeypatch.setattr(_renderer, "INBOX_PATH", tmp_path / "OPERATOR_INBOX.md")
    block, count = _renderer._render_block()
    assert count == 0
    assert "_No open operator/mixed actions._" in block


def test_pipe_in_field_is_escaped(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    ops_rows = [
        {"ops_action_id": "OPS-58-2", "title": "with | pipe", "originating_initiative_id": "INIT-OPENCLAW_AKOS-58", "forwarded_to_initiative_id": "", "owner_class": "operator", "owner_role": "PMO", "status": "open", "rice_score": "144", "rice_impact": "", "linked_decision_ids": "", "linked_policies": "", "originating_at": "", "closed_at": "", "notes": "a | b"},
    ]
    init_rows = [{"initiative_id": "INIT-OPENCLAW_AKOS-58", "title": "Cycle 2"}]
    _seed_csvs(tmp_path, ops_rows, init_rows)
    _redirect_paths(tmp_path, monkeypatch)

    block, _ = _renderer._render_block()
    assert "with \\| pipe" in block
    assert "a \\| b" in block
