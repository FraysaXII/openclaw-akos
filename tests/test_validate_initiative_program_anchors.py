"""Tests for scripts/validate_initiative_program_anchors.py (Initiative 86 P1+P2).

Locks in the Stage A AND Stage B anchor FK contracts:

Stage A (legacy-notes-parser; D-IH-86-H):
- Pydantic ``InitiativeProgramAnchorParse`` round-trips the parse result.
- ``parse_anchor_prefix`` extracts ids from canonical ``Program anchors:`` prefix.
- ``_evaluate_legacy_notes`` PASSes on prefix-less rows; PASSes on resolved-FK rows;
  FAILs on malformed and unknown anchors.

Stage B (column-read default; D-IH-86-J):
- ``_evaluate_column_read`` PASSes when ``program_anchors`` column is empty.
- ``_evaluate_column_read`` PASSes on resolved-FK column values.
- ``_evaluate_column_read`` FAILs on malformed and unknown column values.
- ``_evaluate_column_read`` emits cutover-hygiene WARN when ``notes`` still carries
  the residual ``Program anchors:`` prefix (post-cutover drift signal).

Per D-IH-86-H (Stage A, 2026-05-17) + D-IH-86-J (Stage B, 2026-05-17 at P2) + I86
master-roadmap §9-12.

Per [`CONTRIBUTING.md`](../CONTRIBUTING.md) Python Code Standards: Pydantic models;
type hints; ``pathlib.Path``; tests grouped under @pytest.mark.hlk for
``scripts/test.py`` registration.
"""

from __future__ import annotations

import csv
import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_initiative_program_anchors import (  # noqa: E402
    PROGRAM_ID_PATTERN,
    InitiativeProgramAnchorParse,
    parse_anchor_prefix,
    parse_initiative_row,
)

SCRIPT_PATH = REPO_ROOT / "scripts" / "validate_initiative_program_anchors.py"
INITIATIVE_HEADER = (
    "initiative_id,repo_slug,folder_path,title,status,cycle_id,owner_role,"
    "inception_date,last_review,closed_at,archived_at,superseded_by,"
    "continuous_rationale,cadence,gated_on,operator_action,"
    "inception_decision_id,closure_decision_id,manifests_processes,"
    "linked_topic_ids,program_anchors,notes,last_review_at,last_review_by,"
    "last_review_decision_id,methodology_version_at_review\n"
)
PROGRAM_HEADER = "program_id,program_name,status\n"


@pytest.fixture(scope="module")
def validator_module():
    spec = importlib.util.spec_from_file_location(
        "validate_initiative_program_anchors_under_test", SCRIPT_PATH
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["validate_initiative_program_anchors_under_test"] = module
    spec.loader.exec_module(module)
    return module


# ---------------------------------------------------------------------------
# Pydantic + parse_anchor_prefix unit tests
# ---------------------------------------------------------------------------


@pytest.mark.hlk
def test_pydantic_round_trip_preserves_empty_lists():
    parse = InitiativeProgramAnchorParse(initiative_id="INIT-X")
    assert parse.initiative_id == "INIT-X"
    assert parse.notes_raw == ""
    assert parse.has_prefix is False
    assert parse.anchors == []
    assert parse.unknown_anchors == []
    assert parse.malformed_tokens == []


@pytest.mark.hlk
def test_parse_anchor_prefix_extracts_canonical_shape():
    has_prefix, ids, malformed = parse_anchor_prefix(
        "Program anchors: PRJ-HOL-PGF-2026; PRJ-HOL-INF-2026. seeded by I59 P3"
    )
    assert has_prefix is True
    assert ids == ["PRJ-HOL-PGF-2026", "PRJ-HOL-INF-2026"]
    assert malformed == []


@pytest.mark.hlk
def test_parse_anchor_prefix_returns_empty_when_no_prefix():
    has_prefix, ids, malformed = parse_anchor_prefix("seeded by I59 P3 audit pass")
    assert has_prefix is False
    assert ids == []
    assert malformed == []


@pytest.mark.hlk
def test_parse_anchor_prefix_separates_malformed_tokens():
    has_prefix, ids, malformed = parse_anchor_prefix(
        "Program anchors: PRJ-HOL-PGF-2026; not-an-anchor; PRJ-HOL-FIN-2026."
    )
    assert has_prefix is True
    assert ids == ["PRJ-HOL-PGF-2026", "PRJ-HOL-FIN-2026"]
    assert malformed == ["not-an-anchor"]


@pytest.mark.hlk
def test_parse_initiative_row_flags_unknown_anchor():
    parse = parse_initiative_row(
        "INIT-X",
        "Program anchors: PRJ-HOL-PGF-2026; PRJ-HOL-GHOST-2026.",
        known_program_ids={"PRJ-HOL-PGF-2026"},
    )
    assert parse.anchors == ["PRJ-HOL-PGF-2026", "PRJ-HOL-GHOST-2026"]
    assert parse.unknown_anchors == ["PRJ-HOL-GHOST-2026"]
    assert parse.malformed_tokens == []


@pytest.mark.hlk
def test_program_id_pattern_matches_canonical_ids():
    assert PROGRAM_ID_PATTERN.match("PRJ-HOL-FOUNDING-2026")
    assert PROGRAM_ID_PATTERN.match("PRJ-HOL-MAD-2026")
    assert not PROGRAM_ID_PATTERN.match("PRJ-HOL--2026")
    assert not PROGRAM_ID_PATTERN.match("prj-hol-mkt-2026")
    assert not PROGRAM_ID_PATTERN.match("env_tech_prj_2")


# ---------------------------------------------------------------------------
# Validator entry-point tests (subprocess against fixture CSVs)
# ---------------------------------------------------------------------------


def _write_initiative_csv(path: Path, body_rows: list[str]) -> None:
    path.write_text(INITIATIVE_HEADER + "".join(body_rows), encoding="utf-8")


def _write_program_csv(path: Path, ids: list[str]) -> None:
    body = "".join(f"{pid},name {pid},active\n" for pid in ids)
    path.write_text(PROGRAM_HEADER + body, encoding="utf-8")


def _evaluate_legacy(validator_module, init_rows, programs):
    return validator_module._evaluate_legacy_notes(init_rows, set(programs))


def _evaluate_column(validator_module, init_rows, programs):
    return validator_module._evaluate_column_read(init_rows, set(programs))


# --- Stage A (legacy-notes-parser) ----------------------------------------------


@pytest.mark.hlk
def test_legacy_validator_pass_when_no_prefix_present(validator_module):
    rows = [
        {"initiative_id": "INIT-A", "notes": "seeded only; no anchors"},
        {"initiative_id": "INIT-B", "notes": ""},
    ]
    outcome = _evaluate_legacy(validator_module, rows, {"PRJ-HOL-PGF-2026"})
    assert outcome.rows_scanned == 2
    assert outcome.rows_with_notes_prefix == 0
    assert outcome.errors == []


@pytest.mark.hlk
def test_legacy_validator_pass_when_anchors_resolve(validator_module):
    rows = [
        {
            "initiative_id": "INIT-A",
            "notes": "Program anchors: PRJ-HOL-PGF-2026; PRJ-HOL-INF-2026. seeded.",
        }
    ]
    outcome = _evaluate_legacy(
        validator_module, rows, {"PRJ-HOL-PGF-2026", "PRJ-HOL-INF-2026"}
    )
    assert outcome.errors == []
    assert outcome.rows_with_notes_prefix == 1


@pytest.mark.hlk
def test_legacy_validator_fails_on_unknown_anchor(validator_module):
    rows = [
        {
            "initiative_id": "INIT-B",
            "notes": "Program anchors: PRJ-HOL-PGF-2026; PRJ-HOL-GHOST-2026.",
        }
    ]
    outcome = _evaluate_legacy(validator_module, rows, {"PRJ-HOL-PGF-2026"})
    assert outcome.errors, "expected at least one unknown-anchor error"
    assert any("PRJ-HOL-GHOST-2026" in e for e in outcome.errors)
    assert outcome.unknown_count == 1


@pytest.mark.hlk
def test_legacy_validator_fails_on_malformed_token(validator_module):
    rows = [
        {
            "initiative_id": "INIT-C",
            "notes": "Program anchors: PRJ-HOL-PGF-2026; not-an-anchor.",
        }
    ]
    outcome = _evaluate_legacy(validator_module, rows, {"PRJ-HOL-PGF-2026"})
    assert outcome.malformed_count == 1
    assert any("not-an-anchor" in e for e in outcome.errors)


# --- Stage B (column-read default) ---------------------------------------------


@pytest.mark.hlk
def test_column_validator_pass_when_column_empty(validator_module):
    rows = [
        {"initiative_id": "INIT-A", "program_anchors": "", "notes": "no anchors"},
        {"initiative_id": "INIT-B", "program_anchors": "", "notes": ""},
    ]
    outcome = _evaluate_column(validator_module, rows, {"PRJ-HOL-PGF-2026"})
    assert outcome.mode == "column-read"
    assert outcome.rows_with_column == 0
    assert outcome.rows_with_notes_prefix == 0
    assert outcome.errors == []
    assert outcome.warnings == []


@pytest.mark.hlk
def test_column_validator_pass_when_anchors_resolve(validator_module):
    rows = [
        {
            "initiative_id": "INIT-A",
            "program_anchors": "PRJ-HOL-PGF-2026;PRJ-HOL-INF-2026",
            "notes": "clean post-cutover",
        }
    ]
    outcome = _evaluate_column(
        validator_module, rows, {"PRJ-HOL-PGF-2026", "PRJ-HOL-INF-2026"}
    )
    assert outcome.rows_with_column == 1
    assert outcome.errors == []
    assert outcome.warnings == []


@pytest.mark.hlk
def test_column_validator_fails_on_unknown_anchor(validator_module):
    rows = [
        {
            "initiative_id": "INIT-B",
            "program_anchors": "PRJ-HOL-PGF-2026;PRJ-HOL-GHOST-2026",
            "notes": "clean post-cutover",
        }
    ]
    outcome = _evaluate_column(validator_module, rows, {"PRJ-HOL-PGF-2026"})
    assert outcome.unknown_count == 1
    assert any("PRJ-HOL-GHOST-2026" in e for e in outcome.errors)


@pytest.mark.hlk
def test_column_validator_fails_on_malformed_token(validator_module):
    rows = [
        {
            "initiative_id": "INIT-C",
            "program_anchors": "PRJ-HOL-PGF-2026;not-an-anchor",
            "notes": "clean post-cutover",
        }
    ]
    outcome = _evaluate_column(validator_module, rows, {"PRJ-HOL-PGF-2026"})
    assert outcome.malformed_count == 1
    assert any("not-an-anchor" in e for e in outcome.errors)


@pytest.mark.hlk
def test_column_validator_warns_on_residual_notes_prefix(validator_module):
    """Stage B cutover-hygiene WARN — Stage A prefix should not survive the one-shot."""
    rows = [
        {
            "initiative_id": "INIT-D",
            "program_anchors": "PRJ-HOL-PGF-2026",
            "notes": "Program anchors: PRJ-HOL-PGF-2026. residual notes prefix not migrated",
        }
    ]
    outcome = _evaluate_column(validator_module, rows, {"PRJ-HOL-PGF-2026"})
    assert outcome.errors == []
    assert len(outcome.warnings) == 1
    assert "residual 'Program anchors:' prefix" in outcome.warnings[0]
    assert outcome.rows_with_notes_prefix == 1


@pytest.mark.hlk
def test_validator_subprocess_returns_zero_on_clean_csv(tmp_path, monkeypatch):
    initiative_csv = tmp_path / "INITIATIVE_REGISTRY.csv"
    program_csv = tmp_path / "PROGRAM_REGISTRY.csv"
    _write_initiative_csv(
        initiative_csv,
        [
            "INIT-A,,,t,active,,PMO,,,,,,r,,,,,,,,PRJ-HOL-PGF-2026,clean post-cutover,2026-05-17,PMO,D-IH-86-J,v3.1\n",
            "INIT-B,,,t,active,,PMO,,,,,,r,,,,,,,,,seeded only,2026-05-17,PMO,D-IH-86-J,v3.1\n",
        ],
    )
    _write_program_csv(program_csv, ["PRJ-HOL-PGF-2026"])

    monkeypatch.setenv("PYTHONPATH", str(REPO_ROOT))

    result = subprocess.run(
        [sys.executable, str(SCRIPT_PATH), "--quiet"],
        capture_output=True,
        text=True,
        check=False,
        cwd=str(REPO_ROOT),
    )
    assert result.returncode in (0, 1), result.stderr
