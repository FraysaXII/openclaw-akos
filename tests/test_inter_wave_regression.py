"""Tests for akos.hlk_inter_wave_regression + scripts/inter_wave_regression_sweep.py (Wave M P2).

Covers:
- Pydantic models RegressionFindingRow + RegressionSweepReport
  validate enum membership for dimension_code, verdict, severity.
- Slug regex on report_id; ISO date on swept_at + last_review; wave
  code pattern (Wave-X or Wave-X.Y).
- Optional candidate_decision_id pattern (D-IH-NN-X).
- Runbook PROBE_REGISTRY contains exactly 12 entries matching
  ALL_DIMENSIONS.
- Each of the 12 _probe_dimension_N smoke-functions returns a non-empty
  list of valid RegressionFindingRow instances.
- ``self_test()`` exits 0; ``main()`` exits 1 on missing --wave-closing.
- Markdown + JSON emit functions write parseable output.

Per CONTRIBUTING.md Python Code Standards: type hints, ValidationError
guards, no print statements, registered under @pytest.mark.hlk so the
suite is picked up by the HLK marker group.

Decision lineage: D-IH-86-BO (paired runbook + Pydantic + tests).
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_inter_wave_regression import (  # noqa: E402
    REGRESSION_FINDING_FIELDNAMES,
    REGRESSION_SWEEP_FIELDNAMES,
    VALID_DIMENSION_CODES,
    VALID_SEVERITIES,
    VALID_VERDICTS,
    RegressionFindingRow,
    RegressionSweepReport,
)

RUNBOOK_PATH = REPO_ROOT / "scripts" / "inter_wave_regression_sweep.py"


def _minimal_finding(**overrides) -> RegressionFindingRow:
    base = {
        "dimension_code": "DIM-01-CLOSING-WAVE-SURFACES",
        "surface_path": "docs/example.md",
        "verdict": "clean",
        "proposed_rework_action": "",
        "candidate_decision_id": None,
        "severity": "low",
        "notes": "fixture",
    }
    base.update(overrides)
    return RegressionFindingRow(**base)


def _minimal_report(findings: list[RegressionFindingRow] | None = None) -> RegressionSweepReport:
    if findings is None:
        findings = [_minimal_finding()]
    counts = {v: 0 for v in ("clean", "drift", "gap", "blocked", "skip")}
    for f in findings:
        counts[f.verdict] += 1
    return RegressionSweepReport(
        report_id="regression-sweep-2026-05-21",
        wave_closing="Wave-L",
        swept_at="2026-05-21",
        swept_by="pytest",
        findings=findings,
        clean_count=counts["clean"],
        drift_count=counts["drift"],
        gap_count=counts["gap"],
        blocked_count=counts["blocked"],
        skip_count=counts["skip"],
        total_findings=len(findings),
    )


@pytest.mark.hlk
class TestRegressionFindingRow:
    def test_finding_row_valid_minimum(self):
        f = _minimal_finding()
        assert f.dimension_code == "DIM-01-CLOSING-WAVE-SURFACES"
        assert f.verdict == "clean"
        assert f.severity == "low"

    def test_finding_row_valid_with_decision_id(self):
        f = _minimal_finding(candidate_decision_id="D-IH-86-BT")
        assert f.candidate_decision_id == "D-IH-86-BT"

    def test_finding_row_invalid_dimension_enum(self):
        with pytest.raises(ValidationError):
            _minimal_finding(dimension_code="DIM-99-NOT-A-REAL-DIMENSION")

    def test_finding_row_invalid_verdict_enum(self):
        with pytest.raises(ValidationError):
            _minimal_finding(verdict="not-a-verdict")

    def test_finding_row_invalid_severity_enum(self):
        with pytest.raises(ValidationError):
            _minimal_finding(severity="catastrophic")

    def test_finding_row_invalid_decision_id_pattern(self):
        with pytest.raises(ValidationError):
            _minimal_finding(candidate_decision_id="NOT-A-DECISION-ID")

    def test_finding_row_frozen(self):
        f = _minimal_finding()
        with pytest.raises(ValidationError):
            f.verdict = "drift"  # type: ignore[misc]


@pytest.mark.hlk
class TestRegressionSweepReport:
    def test_sweep_report_valid_minimum(self):
        r = _minimal_report()
        assert r.total_findings == 1
        assert r.wave_closing == "Wave-L"

    def test_sweep_report_valid_empty_findings(self):
        r = _minimal_report(findings=[])
        assert r.total_findings == 0
        assert r.clean_count == 0

    def test_sweep_report_valid_split_wave_dot_decimal(self):
        r = _minimal_report()
        r2 = RegressionSweepReport(**{**r.model_dump(), "wave_closing": "Wave-M.5"})
        assert r2.wave_closing == "Wave-M.5"

    def test_sweep_report_invalid_wave_pattern(self):
        r = _minimal_report()
        with pytest.raises(ValidationError):
            RegressionSweepReport(**{**r.model_dump(), "wave_closing": "wave-l-lowercase"})

    def test_sweep_report_invalid_report_id_pattern(self):
        r = _minimal_report()
        with pytest.raises(ValidationError):
            RegressionSweepReport(**{**r.model_dump(), "report_id": "report-2026-05-21"})

    def test_sweep_report_invalid_swept_at_iso(self):
        r = _minimal_report()
        with pytest.raises(ValidationError):
            RegressionSweepReport(**{**r.model_dump(), "swept_at": "21-05-2026"})


@pytest.mark.hlk
class TestEnumExports:
    def test_dimension_codes_count(self):
        assert len(VALID_DIMENSION_CODES) == 12

    def test_dimension_codes_naming(self):
        for code in VALID_DIMENSION_CODES:
            assert code.startswith("DIM-")
            assert code.split("-")[1].isdigit()

    def test_verdicts_canonical(self):
        assert VALID_VERDICTS == {"clean", "drift", "gap", "blocked", "skip"}

    def test_severities_canonical(self):
        assert VALID_SEVERITIES == {"low", "medium", "high"}

    def test_finding_fieldnames_tuple_shape(self):
        assert "dimension_code" in REGRESSION_FINDING_FIELDNAMES
        assert "verdict" in REGRESSION_FINDING_FIELDNAMES
        assert "severity" in REGRESSION_FINDING_FIELDNAMES

    def test_sweep_fieldnames_tuple_shape(self):
        assert "report_id" in REGRESSION_SWEEP_FIELDNAMES
        assert "wave_closing" in REGRESSION_SWEEP_FIELDNAMES
        assert "total_findings" in REGRESSION_SWEEP_FIELDNAMES


@pytest.mark.hlk
class TestRunbookProbes:
    @classmethod
    def setup_class(cls):
        from scripts import inter_wave_regression_sweep as iwrs
        cls.iwrs = iwrs

    def test_probe_registry_has_12_entries(self):
        assert len(self.iwrs.PROBE_REGISTRY) == 12

    def test_probe_registry_matches_all_dimensions(self):
        assert set(self.iwrs.PROBE_REGISTRY.keys()) == set(self.iwrs.ALL_DIMENSIONS)

    @pytest.mark.parametrize("dim_code", [
        "DIM-01-CLOSING-WAVE-SURFACES",
        "DIM-02-SIBLING-INITIATIVE-STATUS",
        "DIM-03-I86-COORDINATOR-STATE",
        "DIM-04-QUALITY-FABRIC-SPECIALTIES",
        "DIM-05-FORWARD-CHARTER-GATES",
        "DIM-06-SIBLING-REPO-DEPLOY-POSTURE",
        "DIM-07-RENDER-PENDING-TRACKER",
        "DIM-08-PRE-EXISTING-RELEASE-GATE-FAILS",
        "DIM-09-CURSOR-RULES-DRIFT",
        "DIM-10-SKILLS-DRIFT",
        "DIM-11-UNTRACKED-FILES-AUDIT",
        "DIM-12-CANONICAL-CSV-MIRROR-PARITY",
    ])
    def test_probe_dimension_N_smoke(self, dim_code: str):
        probe = self.iwrs.PROBE_REGISTRY[dim_code]
        if dim_code == "DIM-01-CLOSING-WAVE-SURFACES":
            findings = probe("Wave-L")
        else:
            findings = probe()
        assert isinstance(findings, list)
        assert len(findings) >= 1
        for f in findings:
            assert isinstance(f, RegressionFindingRow)
            assert f.dimension_code == dim_code

    def test_run_sweep_with_subset(self):
        report = self.iwrs.run_sweep(
            "Wave-L",
            dimensions=("DIM-09-CURSOR-RULES-DRIFT", "DIM-10-SKILLS-DRIFT"),
        )
        assert isinstance(report, RegressionSweepReport)
        assert report.wave_closing == "Wave-L"
        assert report.total_findings >= 2

    def test_run_sweep_full_12_dimensions(self):
        report = self.iwrs.run_sweep("Wave-L")
        assert report.total_findings >= 12
        assert (
            report.clean_count + report.drift_count + report.gap_count
            + report.blocked_count + report.skip_count == report.total_findings
        )


@pytest.mark.hlk
class TestRunbookCLI:
    def test_self_test_mode_exits_zero(self):
        result = subprocess.run(
            [sys.executable, str(RUNBOOK_PATH), "--self-test"],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            timeout=60,
        )
        assert result.returncode == 0, result.stderr

    def test_check_mode_alias_exits_zero(self):
        result = subprocess.run(
            [sys.executable, str(RUNBOOK_PATH), "--check"],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            timeout=60,
        )
        assert result.returncode == 0, result.stderr

    def test_sweep_mode_without_wave_fails(self):
        result = subprocess.run(
            [sys.executable, str(RUNBOOK_PATH)],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert result.returncode == 1

    def test_sweep_mode_invalid_wave_pattern_fails(self):
        result = subprocess.run(
            [sys.executable, str(RUNBOOK_PATH), "--wave-closing", "not-a-wave"],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert result.returncode == 1


@pytest.mark.hlk
class TestEmitFunctions:
    def test_emit_markdown_writes_table(self, tmp_path: Path):
        from scripts import inter_wave_regression_sweep as iwrs
        report = _minimal_report()
        out = tmp_path / "regression-sweep-2026-05-21.md"
        iwrs.emit_markdown_report(report, out)
        text = out.read_text(encoding="utf-8")
        assert "Wave-L" in text
        assert "DIM-01-CLOSING-WAVE-SURFACES" in text
        assert "| Verdict | Count |" in text

    def test_emit_json_writes_valid_json(self, tmp_path: Path):
        from scripts import inter_wave_regression_sweep as iwrs
        report = _minimal_report()
        out = tmp_path / "regression-sweep-2026-05-21.json"
        iwrs.emit_json_artifact(report, out)
        data = json.loads(out.read_text(encoding="utf-8"))
        assert data["report_id"] == "regression-sweep-2026-05-21"
        assert data["wave_closing"] == "Wave-L"
        assert len(data["findings"]) == 1
        assert data["findings"][0]["dimension_code"] == "DIM-01-CLOSING-WAVE-SURFACES"
