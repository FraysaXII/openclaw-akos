"""Unit + integration tests for scripts/peopl_research_substrate_audit_cadence.py.

Covers each CLI mode with valid + invalid input pairs per CONTRIBUTING.md
Python Code Standards. Pair these with scripts/test.py group discovery
(auto-discovered under tests/ root; no group registration required).

Paired SOP: docs/references/hlk/v3.0/Research/Methodology/canonicals/SOP-RESEARCH_SUBSTRATE_AUDIT_CADENCE_001.md
Paired runbook: scripts/peopl_research_substrate_audit_cadence.py
Decision lineage: D-IH-84-A; D-IH-84-G; D-IH-84-H
"""
from __future__ import annotations

import datetime as dt
import importlib
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))


@pytest.fixture(scope="module")
def runbook_module():
    """Import the runbook module once per test module."""
    module_name = "peopl_research_substrate_audit_cadence"
    if module_name in sys.modules:
        return importlib.reload(sys.modules[module_name])
    return importlib.import_module(module_name)


# ---------- Module structural tests ---------------------------------------


def test_module_imports_clean(runbook_module) -> None:
    """The module imports without raising; expected attributes present."""
    assert hasattr(runbook_module, "main")
    assert hasattr(runbook_module, "STALENESS_THRESHOLD_DAYS")
    assert hasattr(runbook_module, "SUBSTRATE_REGISTRY_CSV")
    assert hasattr(runbook_module, "PAIRED_SOP")
    assert hasattr(runbook_module, "DOCTRINE_CANONICAL")


def test_paired_canonicals_exist(runbook_module) -> None:
    """The paired SOP + doctrine canonicals exist at the declared paths."""
    assert runbook_module.PAIRED_SOP.is_file(), (
        f"Paired SOP missing at {runbook_module.PAIRED_SOP}"
    )
    assert runbook_module.DOCTRINE_CANONICAL.is_file(), (
        f"Doctrine canonical missing at {runbook_module.DOCTRINE_CANONICAL}"
    )


def test_substrate_registry_csv_exists(runbook_module) -> None:
    """SUBSTRATE_REGISTRY.csv exists at the canonical path."""
    assert runbook_module.SUBSTRATE_REGISTRY_CSV.is_file()


def test_quarter_folder_regex(runbook_module) -> None:
    """Validates the substrate-audit-YYYY-QN folder name regex."""
    rx = runbook_module.QUARTER_FOLDER_RE
    assert rx.match("substrate-audit-2026-Q2") is not None
    assert rx.match("substrate-audit-2026-Q3-off-cycle-cursor-ga") is not None
    assert rx.match("substrate-audit-2026-Q5") is None  # only Q1-Q4 valid
    assert rx.match("substrate-audit-26-Q2") is None  # 4-digit year only
    assert rx.match("random-folder") is None


# ---------- Default mode (no args) ----------------------------------------


def test_default_mode_no_args(runbook_module, capsys) -> None:
    """Default mode: prints usage summary; returns 0."""
    exit_code = runbook_module.main([])
    assert exit_code == 0
    captured = capsys.readouterr()
    # Usage block should mention the SOP + canonical paths
    assert "Research Substrate Audit Cadence Runbook" in captured.out
    assert "SUBSTRATE_REGISTRY" in captured.out
    assert "--staleness-check" in captured.out


# ---------- Staleness-check mode ------------------------------------------


def test_staleness_check_with_fresh_rows(runbook_module, capsys, monkeypatch) -> None:
    """Staleness check passes when registry rows are recent."""
    # Force "today" to be near the registry's actual last_audit_date (2026-05-17)
    # so all rows look fresh regardless of the calendar at test execution time.
    fixed_today = dt.date(2026, 5, 17)
    monkeypatch.setattr(runbook_module, "_today", lambda: fixed_today)
    exit_code = runbook_module.main(["--staleness-check"])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert "Staleness check" in captured.out
    assert "PASS" in captured.out


def test_staleness_check_with_stale_rows(runbook_module, capsys, monkeypatch) -> None:
    """Staleness check FAILs when last_audit_date is > 90 days old."""
    # Push "today" far enough that the seeded 2026-05-17 dates look ancient.
    fixed_today = dt.date(2027, 1, 1)
    monkeypatch.setattr(runbook_module, "_today", lambda: fixed_today)
    exit_code = runbook_module.main(["--staleness-check"])
    assert exit_code == 1
    captured = capsys.readouterr()
    assert "Stale rows" in captured.out
    assert "FAIL" in captured.out


# ---------- UAT-mode (quarterly report parse + FK resolution) -------------


def test_uat_mode_valid_report(runbook_module, tmp_path) -> None:
    """UAT-mode passes a well-formed report citing registered SUBS-* ids."""
    report = tmp_path / "2026-Q2-substrate-audit.md"
    report.write_text(
        "---\n"
        "title: Q2 substrate audit\n"
        "language: en\n"
        "---\n\n"
        "# Q2 substrate audit\n\n"
        "Cites `SUBS-HOLISTIKA-OPENCLAW` and `SUBS-LANGCHAIN-AI-LANGCHAIN`.\n",
        encoding="utf-8",
    )
    exit_code = runbook_module.main(["--uat-mode", str(report)])
    assert exit_code == 0


def test_uat_mode_unresolved_substrate_id(runbook_module, tmp_path, capsys) -> None:
    """UAT-mode FAILs when report cites a SUBS-* id not in the registry."""
    report = tmp_path / "2026-Q3-substrate-audit.md"
    report.write_text(
        "---\ntitle: bogus\nlanguage: en\n---\n\n"
        "# Bogus report\n\n"
        "Cites `SUBS-DOES-NOT-EXIST-IN-REGISTRY`.\n",
        encoding="utf-8",
    )
    exit_code = runbook_module.main(["--uat-mode", str(report)])
    assert exit_code == 1
    captured = capsys.readouterr()
    assert "Unresolved" in captured.out
    assert "FAIL" in captured.out


def test_uat_mode_missing_report(runbook_module, tmp_path) -> None:
    """UAT-mode FAILs gracefully when the report path doesn't exist."""
    missing = tmp_path / "does-not-exist.md"
    exit_code = runbook_module.main(["--uat-mode", str(missing)])
    # Per module convention: missing report file -> errors list, returns 1
    # (the FileNotFoundError path returns 2; here the path simply doesn't
    # resolve to a file so we fall through to the "not a file" branch).
    assert exit_code == 1


# ---------- Emit-delta mode -----------------------------------------------


def test_emit_delta_with_two_reports(runbook_module, tmp_path, capsys) -> None:
    """Emit-delta produces a Markdown delta between two reports."""
    prior = tmp_path / "2026-Q2-substrate-audit.md"
    prior.write_text(
        "# Q2\nCites `SUBS-HOLISTIKA-OPENCLAW` `SUBS-LANGCHAIN-AI-LANGCHAIN`.\n",
        encoding="utf-8",
    )
    current = tmp_path / "2026-Q3-substrate-audit.md"
    current.write_text(
        "# Q3\nCites `SUBS-HOLISTIKA-OPENCLAW` `SUBS-ANYSPHERE-CURSOR-SDK`.\n",
        encoding="utf-8",
    )
    exit_code = runbook_module.main(["--emit-delta", str(prior), str(current)])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert "SUBS-ANYSPHERE-CURSOR-SDK" in captured.out  # added
    assert "SUBS-LANGCHAIN-AI-LANGCHAIN" in captured.out  # removed
    assert "Net added" in captured.out
    assert "Net removed" in captured.out


def test_emit_delta_missing_prior(runbook_module, tmp_path, capsys) -> None:
    """Emit-delta FAILs when one of the two report paths is missing."""
    prior = tmp_path / "missing-prior.md"  # not created
    current = tmp_path / "current.md"
    current.write_text("# Current\n", encoding="utf-8")
    exit_code = runbook_module.main(["--emit-delta", str(prior), str(current)])
    assert exit_code == 1
    captured = capsys.readouterr()
    assert "Missing report" in captured.out


# ---------- List-quarters mode --------------------------------------------


def test_list_quarters(runbook_module, capsys) -> None:
    """List-quarters surfaces discovered substrate-audit-YYYY-QN folders."""
    exit_code = runbook_module.main(["--list-quarters"])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert "Substrate audit quarter folders" in captured.out
    # The founding Q2 2026 folder should be discovered when present
    intelligence_root = REPO_ROOT / "docs" / "wip" / "intelligence"
    expected_q2 = intelligence_root / "substrate-audit-2026-Q2"
    if expected_q2.is_dir():
        assert "substrate-audit-2026-Q2" in captured.out


# ---------- Helpers --------------------------------------------------------


def test_parse_iso_date_valid(runbook_module) -> None:
    assert runbook_module._parse_iso_date("2026-05-17") == dt.date(2026, 5, 17)


def test_parse_iso_date_invalid(runbook_module) -> None:
    assert runbook_module._parse_iso_date("not-a-date") is None
    assert runbook_module._parse_iso_date("") is None


def test_format_summary_includes_counts(runbook_module) -> None:
    rows = [
        {"status": "active", "akos_integration_state": "in-production"},
        {"status": "active", "akos_integration_state": "pilot"},
        {"status": "candidate", "akos_integration_state": "candidate"},
    ]
    summary = runbook_module._format_summary(rows)
    assert "Total rows: 3" in summary
    assert "active=2" in summary
    assert "candidate=1" in summary


def test_extract_substrate_ids_from_report(runbook_module, tmp_path) -> None:
    report = tmp_path / "r.md"
    report.write_text(
        "# X\nCites `SUBS-FOO-BAR` and `SUBS-LANG-LANG` plus `SUBS-FOO-BAR` again.\n",
        encoding="utf-8",
    )
    ids = runbook_module._extract_substrate_ids_from_report(report)
    assert ids == {"SUBS-FOO-BAR", "SUBS-LANG-LANG"}
