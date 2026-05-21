"""Tests for akos.hlk_index_integrity + scripts/baseline_index_sweep.py.

Covers:
- Pydantic models IndexFreshnessRow + IndexFreshnessReport validate
  enum membership for dimension_code, verdict, severity, sweep_trigger.
- Slug regex on report_id; ISO date on swept_at; optional
  candidate_decision_id pattern (D-IH-NN-X).
- Runbook PROBE_REGISTRY contains exactly 8 entries matching
  VALID_INDEX_DIMENSION_CODES.
- BASELINE_INDEX_DIMENSION_CODES (6) and CONDITIONAL_INDEX_DIMENSION_CODES
  (2) are disjoint and their union equals VALID_INDEX_DIMENSION_CODES per
  the canonical §2 baseline/conditional split.
- Each of the 8 probe functions returns a list of IndexFreshnessRow.
- self_test() exits 0; validator wrapper --self-test exits 0; full sweep
  with --output produces parseable markdown + JSON.

Per CONTRIBUTING.md Python Code Standards: type hints, ValidationError
guards, no print statements, registered under @pytest.mark.hlk so the
suite is picked up by the HLK marker group.

Decision lineage:
- D-IH-86-CD (canonical mint + INFO ramp; paired runbook + Pydantic +
  tests at Wave N P3).
- D-IH-86-CE (8-dimension probe set ratification).
- D-IH-86-CF (paired SOP+runbook gate per akos-executable-process-
  catalog.mdc Rule 1).
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

from akos.hlk_index_integrity import (  # noqa: E402
    BASELINE_INDEX_DIMENSION_CODES,
    CONDITIONAL_INDEX_DIMENSION_CODES,
    INDEX_FRESHNESS_FIELDNAMES,
    INDEX_FRESHNESS_REPORT_FIELDNAMES,
    VALID_INDEX_DIMENSION_CODES,
    VALID_INDEX_SEVERITIES,
    VALID_INDEX_VERDICTS,
    VALID_SWEEP_TRIGGERS,
    IndexFreshnessReport,
    IndexFreshnessRow,
)

RUNBOOK_PATH = REPO_ROOT / "scripts" / "baseline_index_sweep.py"
VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_index_freshness.py"


ALL_DOCTRINE_DIMENSIONS: tuple[str, ...] = (
    "IDX-01-PLANNING-README-INITIATIVE-COUNT",
    "IDX-02-PRECEDENCE-CSV-COVERAGE",
    "IDX-03-CHANGELOG-WAVE-COVERAGE",
    "IDX-04-INITIATIVE-DEPENDENCIES-FRESHNESS",
    "IDX-05-USER-GUIDE-ROLE-PROCESS-COUNTS",
    "IDX-06-ARCHITECTURE-HLK-REGISTRY-COVERAGE",
    "IDX-07-PLANNING-FOLDER-FILESYSTEM-PARITY",
    "IDX-08-QUALITY-FABRIC-SPECIALTY-COUNT",
)


EXPECTED_BASELINE: frozenset[str] = frozenset({
    "IDX-01-PLANNING-README-INITIATIVE-COUNT",
    "IDX-02-PRECEDENCE-CSV-COVERAGE",
    "IDX-03-CHANGELOG-WAVE-COVERAGE",
    "IDX-04-INITIATIVE-DEPENDENCIES-FRESHNESS",
    "IDX-07-PLANNING-FOLDER-FILESYSTEM-PARITY",
    "IDX-08-QUALITY-FABRIC-SPECIALTY-COUNT",
})


EXPECTED_CONDITIONAL: frozenset[str] = frozenset({
    "IDX-05-USER-GUIDE-ROLE-PROCESS-COUNTS",
    "IDX-06-ARCHITECTURE-HLK-REGISTRY-COVERAGE",
})


def _minimal_finding(**overrides) -> IndexFreshnessRow:
    base = {
        "dimension_code": "IDX-01-PLANNING-README-INITIATIVE-COUNT",
        "index_path": "docs/wip/planning/README.md",
        "verdict": "fresh",
        "drift_summary": "",
        "proposed_fix_action": "",
        "candidate_decision_id": None,
        "severity": "low",
        "notes": "fixture",
    }
    base.update(overrides)
    return IndexFreshnessRow(**base)


def _minimal_report(findings: list[IndexFreshnessRow] | None = None) -> IndexFreshnessReport:
    if findings is None:
        findings = [_minimal_finding()]
    counts = {v: 0 for v in ("fresh", "drift", "gap", "blocked", "skip")}
    for f in findings:
        counts[f.verdict] += 1
    return IndexFreshnessReport(
        report_id="index-sweep-2026-05-21",
        sweep_trigger="wave_close",
        swept_at="2026-05-21",
        swept_by="pytest",
        findings=findings,
        fresh_count=counts["fresh"],
        drift_count=counts["drift"],
        gap_count=counts["gap"],
        blocked_count=counts["blocked"],
        skip_count=counts["skip"],
        total_findings=len(findings),
    )


@pytest.mark.hlk
class TestIndexFreshnessRow:
    def test_finding_row_valid_minimum(self):
        f = _minimal_finding()
        assert f.dimension_code == "IDX-01-PLANNING-README-INITIATIVE-COUNT"
        assert f.verdict == "fresh"
        assert f.severity == "low"

    def test_finding_row_valid_with_decision_id(self):
        f = _minimal_finding(candidate_decision_id="D-IH-86-CD")
        assert f.candidate_decision_id == "D-IH-86-CD"

    def test_finding_row_invalid_dimension_enum(self):
        with pytest.raises(ValidationError):
            _minimal_finding(dimension_code="IDX-99-NOT-A-REAL-DIMENSION")

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
class TestIndexFreshnessReport:
    def test_sweep_report_valid_minimum(self):
        r = _minimal_report()
        assert r.total_findings == 1
        assert r.sweep_trigger == "wave_close"

    def test_sweep_report_valid_empty_findings(self):
        r = _minimal_report(findings=[])
        assert r.total_findings == 0
        assert r.fresh_count == 0

    def test_sweep_report_valid_optional_suffix(self):
        r = _minimal_report()
        r2 = IndexFreshnessReport(
            **{**r.model_dump(), "report_id": "index-sweep-2026-05-21-waveclose"}
        )
        assert r2.report_id == "index-sweep-2026-05-21-waveclose"

    def test_sweep_report_invalid_report_id_pattern(self):
        r = _minimal_report()
        with pytest.raises(ValidationError):
            IndexFreshnessReport(**{**r.model_dump(), "report_id": "report-2026-05-21"})

    def test_sweep_report_invalid_swept_at_iso(self):
        r = _minimal_report()
        with pytest.raises(ValidationError):
            IndexFreshnessReport(**{**r.model_dump(), "swept_at": "21-05-2026"})

    def test_sweep_report_invalid_sweep_trigger(self):
        r = _minimal_report()
        with pytest.raises(ValidationError):
            IndexFreshnessReport(**{**r.model_dump(), "sweep_trigger": "ad_hoc"})


@pytest.mark.hlk
class TestEnumExports:
    def test_dimension_codes_count(self):
        assert len(VALID_INDEX_DIMENSION_CODES) == 8

    def test_dimension_codes_match_doctrine(self):
        assert VALID_INDEX_DIMENSION_CODES == set(ALL_DOCTRINE_DIMENSIONS)

    def test_dimension_codes_naming(self):
        for code in VALID_INDEX_DIMENSION_CODES:
            assert code.startswith("IDX-")
            parts = code.split("-")
            assert parts[1].isdigit() and 1 <= int(parts[1]) <= 8

    def test_baseline_count_is_six(self):
        assert len(BASELINE_INDEX_DIMENSION_CODES) == 6
        assert BASELINE_INDEX_DIMENSION_CODES == EXPECTED_BASELINE

    def test_conditional_count_is_two(self):
        assert len(CONDITIONAL_INDEX_DIMENSION_CODES) == 2
        assert CONDITIONAL_INDEX_DIMENSION_CODES == EXPECTED_CONDITIONAL

    def test_baseline_and_conditional_are_disjoint(self):
        assert not (BASELINE_INDEX_DIMENSION_CODES & CONDITIONAL_INDEX_DIMENSION_CODES)

    def test_baseline_union_conditional_equals_all(self):
        assert (
            BASELINE_INDEX_DIMENSION_CODES | CONDITIONAL_INDEX_DIMENSION_CODES
            == VALID_INDEX_DIMENSION_CODES
        )

    def test_verdicts_canonical(self):
        assert VALID_INDEX_VERDICTS == {"fresh", "drift", "gap", "blocked", "skip"}

    def test_severities_canonical(self):
        assert VALID_INDEX_SEVERITIES == {"low", "medium", "high"}

    def test_sweep_triggers_canonical(self):
        assert VALID_SWEEP_TRIGGERS == {
            "wave_close", "canonical_csv_mint", "on_demand", "pre_commit_self_test"
        }

    def test_finding_fieldnames_tuple_shape(self):
        assert "dimension_code" in INDEX_FRESHNESS_FIELDNAMES
        assert "verdict" in INDEX_FRESHNESS_FIELDNAMES
        assert "severity" in INDEX_FRESHNESS_FIELDNAMES

    def test_sweep_fieldnames_tuple_shape(self):
        assert "report_id" in INDEX_FRESHNESS_REPORT_FIELDNAMES
        assert "sweep_trigger" in INDEX_FRESHNESS_REPORT_FIELDNAMES
        assert "total_findings" in INDEX_FRESHNESS_REPORT_FIELDNAMES


@pytest.mark.hlk
class TestRunbookProbes:
    @classmethod
    def setup_class(cls):
        from scripts import baseline_index_sweep as bis
        cls.bis = bis

    def test_probe_registry_has_8_entries(self):
        assert len(self.bis.PROBE_REGISTRY) == 8

    def test_probe_registry_matches_pydantic_enum(self):
        """SSOT invariant: the runbook's PROBE_REGISTRY keys equal the Pydantic VALID_INDEX_DIMENSION_CODES."""
        assert set(self.bis.PROBE_REGISTRY.keys()) == VALID_INDEX_DIMENSION_CODES

    @pytest.mark.parametrize("dim_code", list(ALL_DOCTRINE_DIMENSIONS))
    def test_probe_dimension_N_smoke(self, dim_code: str):
        """Each probe returns a list of valid IndexFreshnessRow instances."""
        probe = self.bis.PROBE_REGISTRY[dim_code]
        findings = probe()
        assert isinstance(findings, list)
        for f in findings:
            assert isinstance(f, IndexFreshnessRow)
            assert f.dimension_code == dim_code

    def test_run_sweep_baseline_only(self):
        report = self.bis.run_sweep(sweep_trigger="on_demand", baseline_only=True)
        assert isinstance(report, IndexFreshnessReport)
        assert (
            report.fresh_count + report.drift_count + report.gap_count
            + report.blocked_count + report.skip_count == report.total_findings
        )

    def test_run_sweep_full_8_dimensions(self):
        report = self.bis.run_sweep(sweep_trigger="on_demand")
        assert (
            report.fresh_count + report.drift_count + report.gap_count
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

    def test_validator_self_test_mode_exits_zero(self):
        result = subprocess.run(
            [sys.executable, str(VALIDATOR_PATH), "--self-test"],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            timeout=60,
        )
        assert result.returncode == 0, result.stderr


@pytest.mark.hlk
class TestEmitFunctions:
    def test_write_outputs_writes_markdown_and_json(self, tmp_path: Path):
        from scripts import baseline_index_sweep as bis
        report = _minimal_report()
        md = tmp_path / "index-sweep-2026-05-21.md"
        md_path, json_path = bis.write_outputs(report, md)
        assert md_path.exists()
        assert json_path.exists()
        text = md_path.read_text(encoding="utf-8")
        assert "IDX-01-PLANNING-README-INITIATIVE-COUNT" in text
        assert "wave_close" in text
        data = json.loads(json_path.read_text(encoding="utf-8"))
        assert data["report_id"] == "index-sweep-2026-05-21"
        assert data["sweep_trigger"] == "wave_close"
        assert len(data["findings"]) == 1
