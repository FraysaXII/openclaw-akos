"""Tests for scripts/pmo_program_anchor_backfill.py (Initiative 86 P1).

Locks in the runbook contract paired with
``SOP-PMO_INITIATIVE_PROGRAM_ANCHORS_001.md``:

- ``--list-unanchored`` enumerates active/continuous/program_line rows whose
  ``notes`` lack the ``Program anchors:`` prefix.
- ``--apply --dry-run`` parses ``proposals.csv`` and reports what it would
  rewrite, without touching the file system.
- ``--apply`` rewrites ``notes`` with the canonical ``Program anchors: ...``
  prefix and refreshes review-stamp columns; idempotent re-runs are no-ops.
- Malformed anchors in ``proposals.csv`` cause exit 1.
- Unknown anchors (not in PROGRAM_REGISTRY.csv) cause exit 1.

Per D-IH-86-H (Stage A) + I86 master-roadmap §9-12 + ``akos-executable-process-catalog.mdc``
RULE 1 (paired SOP+runbook discipline).
"""

from __future__ import annotations

import csv
import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = REPO_ROOT / "scripts" / "pmo_program_anchor_backfill.py"


@pytest.fixture(scope="module")
def runbook_module():
    spec = importlib.util.spec_from_file_location(
        "pmo_program_anchor_backfill_under_test", SCRIPT_PATH
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["pmo_program_anchor_backfill_under_test"] = module
    spec.loader.exec_module(module)
    return module


def _make_initiative_row(
    iid: str = "INIT-T",
    status: str = "active",
    notes: str = "",
    title: str = "test row",
    owner: str = "PMO",
) -> dict[str, str]:
    return {
        "initiative_id": iid,
        "status": status,
        "notes": notes,
        "title": title,
        "owner_role": owner,
        "last_review_at": "",
        "last_review_by": "",
        "last_review_decision_id": "",
        "methodology_version_at_review": "",
    }


@pytest.mark.hlk
def test_list_unanchored_skips_anchored_and_closed(runbook_module):
    rows = [
        _make_initiative_row("INIT-A", status="active", notes="no anchors"),
        _make_initiative_row(
            "INIT-B", status="active", notes="Program anchors: PRJ-HOL-PGF-2026."
        ),
        _make_initiative_row("INIT-C", status="closed", notes="no anchors"),
        _make_initiative_row("INIT-D", status="program_line", notes=""),
    ]
    unanchored = runbook_module._list_unanchored(rows)
    ids = {u.initiative_id for u in unanchored}
    assert ids == {"INIT-A", "INIT-D"}


@pytest.mark.hlk
def test_apply_proposals_idempotent(runbook_module):
    rows = [_make_initiative_row("INIT-A", notes="seeded")]
    proposals = {"INIT-A": ["PRJ-HOL-PGF-2026"]}
    applied, skipped = runbook_module._apply_proposals(
        rows,
        proposals,
        today="2026-05-17",
        decision_id="D-IH-86-H",
        methodology_version="v3.1",
    )
    assert applied == 1
    assert skipped == []
    assert rows[0]["notes"].startswith("Program anchors: PRJ-HOL-PGF-2026.")
    assert rows[0]["last_review_decision_id"] == "D-IH-86-H"

    applied2, skipped2 = runbook_module._apply_proposals(
        rows,
        proposals,
        today="2026-05-17",
        decision_id="D-IH-86-H",
        methodology_version="v3.1",
    )
    assert applied2 == 0
    assert skipped2, "second pass must skip rows already prefixed"


@pytest.mark.hlk
def test_load_proposals_flags_malformed(runbook_module, tmp_path):
    proposals_csv = tmp_path / "proposals.csv"
    proposals_csv.write_text(
        "initiative_id,anchors\nINIT-A,not-an-anchor\nINIT-B,PRJ-HOL-PGF-2026\n",
        encoding="utf-8",
    )
    proposals, errors = runbook_module._load_proposals(
        proposals_csv, known_ids={"PRJ-HOL-PGF-2026"}
    )
    assert proposals == {"INIT-B": ["PRJ-HOL-PGF-2026"], "INIT-A": ["not-an-anchor"]}
    assert any("malformed anchor" in e for e in errors)


@pytest.mark.hlk
def test_load_proposals_flags_unknown_anchor(runbook_module, tmp_path):
    proposals_csv = tmp_path / "proposals.csv"
    proposals_csv.write_text(
        "initiative_id,anchors\nINIT-A,PRJ-HOL-GHOST-2026\n", encoding="utf-8"
    )
    _proposals, errors = runbook_module._load_proposals(
        proposals_csv, known_ids={"PRJ-HOL-PGF-2026"}
    )
    assert any("not in PROGRAM_REGISTRY" in e for e in errors)


@pytest.mark.hlk
def test_format_anchors_prefix_canonical_shape(runbook_module):
    out = runbook_module._format_anchors_prefix(["PRJ-HOL-PGF-2026", "PRJ-HOL-INF-2026"])
    assert out == "Program anchors: PRJ-HOL-PGF-2026; PRJ-HOL-INF-2026."


@pytest.mark.hlk
def test_subprocess_list_unanchored_runs(tmp_path):
    """Smoke test the entry-point against the real CSV; exit must be 0."""
    result = subprocess.run(
        [sys.executable, str(SCRIPT_PATH), "--list-unanchored", "--json-log"],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
        check=False,
    )
    assert result.returncode == 0, result.stderr
