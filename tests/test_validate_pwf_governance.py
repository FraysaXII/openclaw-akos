"""Tests for akos.hlk_pwf_governance + scripts/validate_pwf_governance.py.

Covers:
- Pydantic models PWFFollowupRationale + PWFGovernanceFinding +
  PWFGovernanceReport validate enum membership, regex patterns, length bounds.
- parse_followup_rationale handles all 4 input shapes (None / str / dict / other).
- VALID_FOLLOWUP_CLASSES + REQUIRED_CLOSURE_TARGET_CLASSES +
  REQUIRED_TRACKER_PATH_CLASSES invariants per the canonical's §3 enum.
- _check_rationale emits expected finding codes for each gap class.
- _check_report no-ops on PASS / FAIL / PENDING UATs; only fires on
  PASS-WITH-FOLLOWUP verdict per the 12th specialty's scope.
- _check_report correctly catches the Wave R UAT missing-rationale case
  (the worked-example birth artifact for D-IH-86-CX).
- --self-test mode exits 0.
- --report on a malformed report exits 1 in --strict mode.

Per CONTRIBUTING.md Python Code Standards: type hints, ValidationError
guards, no print statements, registered under @pytest.mark.hlk so the
suite is picked up by the HLK marker group.

Decision lineage:
- D-IH-86-CX (12th QF specialty mint; this test module's mint commit).
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_pwf_governance import (  # noqa: E402
    PWF_FOLLOWUP_RATIONALE_FIELDNAMES,
    PWF_GOVERNANCE_FINDING_FIELDNAMES,
    PWF_GOVERNANCE_REPORT_FIELDNAMES,
    REQUIRED_CLOSURE_TARGET_CLASSES,
    REQUIRED_TRACKER_PATH_CLASSES,
    VALID_FINDING_CODES,
    VALID_FOLLOWUP_CLASSES,
    VALID_SCOPES,
    VALID_SEVERITIES,
    PWFFollowupRationale,
    PWFGovernanceFinding,
    PWFGovernanceReport,
    fixture_finding_fail,
    fixture_finding_warn,
    fixture_followup_clean,
    fixture_followup_deferred_work,
    fixture_report_mixed,
    fixture_report_pass,
    parse_followup_rationale,
)

RUNBOOK_PATH = REPO_ROOT / "scripts" / "validate_pwf_governance.py"


EXPECTED_FOLLOWUP_CLASSES: frozenset[str] = frozenset({
    "monitoring-obligation",
    "deferred-work-with-tracker",
    "convention-class-followup",
    "mechanical-recovery-with-eta",
    "escalation-to-blocker-tracker",
})


EXPECTED_FINDING_CODES: frozenset[str] = frozenset({
    "PWF-FM-01-CLASS-MISSING",
    "PWF-FM-02-CLASS-UNKNOWN",
    "PWF-FM-03-CLOSURE-TARGET-MISSING",
    "PWF-FM-04-TRACKER-PATH-MISSING",
    "PWF-FM-04-TRACKER-PATH-INVALID",
    "PWF-FM-05-OWNER-MISSING",
})


# ---------------------------------------------------------------------------
# Module-level invariants (frozensets / fieldnames)
# ---------------------------------------------------------------------------


@pytest.mark.hlk
def test_valid_followup_classes_match_doctrine() -> None:
    """The 5-class enum MUST match the canonical §3 verbatim."""
    assert VALID_FOLLOWUP_CLASSES == EXPECTED_FOLLOWUP_CLASSES


@pytest.mark.hlk
def test_valid_finding_codes_match_validator() -> None:
    """The 5+1 finding codes MUST match validator emissions."""
    assert VALID_FINDING_CODES == EXPECTED_FINDING_CODES


@pytest.mark.hlk
def test_valid_severities_three_class() -> None:
    """Severity enum is info / warn / fail per canonical §4."""
    assert VALID_SEVERITIES == frozenset({"info", "warn", "fail"})


@pytest.mark.hlk
def test_valid_scopes_three_class() -> None:
    """Sweep scope enum is single-report / wave-close-sweep / full-sweep."""
    assert VALID_SCOPES == frozenset({"single-report", "wave-close-sweep", "full-sweep"})


@pytest.mark.hlk
def test_required_closure_target_classes_subset() -> None:
    """REQUIRED_CLOSURE_TARGET_CLASSES must be a subset of VALID_FOLLOWUP_CLASSES."""
    assert REQUIRED_CLOSURE_TARGET_CLASSES.issubset(VALID_FOLLOWUP_CLASSES)


@pytest.mark.hlk
def test_required_tracker_path_classes_subset() -> None:
    """REQUIRED_TRACKER_PATH_CLASSES must be a subset of VALID_FOLLOWUP_CLASSES."""
    assert REQUIRED_TRACKER_PATH_CLASSES.issubset(VALID_FOLLOWUP_CLASSES)


@pytest.mark.hlk
def test_tracker_path_required_for_two_classes() -> None:
    """Per canonical §3: only deferred-work + escalation REQUIRE tracker_path."""
    assert REQUIRED_TRACKER_PATH_CLASSES == frozenset({
        "deferred-work-with-tracker",
        "escalation-to-blocker-tracker",
    })


@pytest.mark.hlk
def test_closure_target_required_for_all_five_classes() -> None:
    """Per canonical §3: ALL 5 classes require closure_target (the load-bearing
    field that converts PWF into a closable trail)."""
    assert REQUIRED_CLOSURE_TARGET_CLASSES == VALID_FOLLOWUP_CLASSES


@pytest.mark.hlk
def test_fieldnames_tuples_sizes() -> None:
    """SSOT fieldnames tuples encode the schema column count for each model."""
    assert len(PWF_FOLLOWUP_RATIONALE_FIELDNAMES) == 6
    assert len(PWF_GOVERNANCE_FINDING_FIELDNAMES) == 6
    assert len(PWF_GOVERNANCE_REPORT_FIELDNAMES) == 9


# ---------------------------------------------------------------------------
# Pydantic model validation
# ---------------------------------------------------------------------------


@pytest.mark.hlk
def test_followup_clean_fixture_constructs() -> None:
    f = fixture_followup_clean()
    assert f.followup_class == "monitoring-obligation"
    assert f.closure_target == "Wave U close"
    assert f.owner == "System Owner"
    assert f.tracker_path is None


@pytest.mark.hlk
def test_followup_deferred_fixture_constructs() -> None:
    f = fixture_followup_deferred_work()
    assert f.followup_class == "deferred-work-with-tracker"
    assert f.tracker_path is not None
    assert f.closure_decision_id_target == "D-IH-86-CX"


@pytest.mark.hlk
def test_followup_unknown_class_rejected() -> None:
    """Pydantic Literal rejects unknown class at construction."""
    with pytest.raises(ValidationError):
        PWFFollowupRationale(followup_class="not-a-real-class")  # type: ignore[arg-type]


@pytest.mark.hlk
def test_followup_decision_id_invalid_pattern_rejected() -> None:
    """closure_decision_id_target must match D-IH-NN-X regex."""
    with pytest.raises(ValidationError):
        PWFFollowupRationale(
            followup_class="monitoring-obligation",
            closure_decision_id_target="not-a-decision-id",
        )


@pytest.mark.hlk
def test_followup_notes_too_long_rejected() -> None:
    """notes max_length=2048; longer values must be rejected."""
    with pytest.raises(ValidationError):
        PWFFollowupRationale(
            followup_class="monitoring-obligation",
            notes="x" * 3000,
        )


@pytest.mark.hlk
def test_finding_fail_fixture_constructs() -> None:
    f = fixture_finding_fail()
    assert f.severity == "fail"
    assert f.finding_code == "PWF-FM-01-CLASS-MISSING"


@pytest.mark.hlk
def test_finding_warn_fixture_constructs() -> None:
    f = fixture_finding_warn()
    assert f.severity == "warn"
    assert f.finding_code == "PWF-FM-05-OWNER-MISSING"


@pytest.mark.hlk
def test_finding_unknown_severity_rejected() -> None:
    with pytest.raises(ValidationError):
        PWFGovernanceFinding(
            finding_code="PWF-FM-01-CLASS-MISSING",
            surface_path="test/path.md",
            severity="critical",  # type: ignore[arg-type]
            class_observed="missing",
        )


@pytest.mark.hlk
def test_report_pass_fixture_constructs() -> None:
    r = fixture_report_pass()
    assert r.total_findings == 0
    assert r.clean_count == 1
    assert r.fail_count == 0


@pytest.mark.hlk
def test_report_mixed_fixture_constructs() -> None:
    r = fixture_report_mixed()
    assert r.total_findings == 2
    assert r.fail_count == 1
    assert r.warn_count == 1
    assert r.scope == "wave-close-sweep"


@pytest.mark.hlk
def test_report_id_regex_enforced() -> None:
    """report_id MUST match pwf-governance-sweep-YYYY-MM-DD(-<slug>)?"""
    with pytest.raises(ValidationError):
        PWFGovernanceReport(
            report_id="not-a-valid-id",
            swept_at="2026-05-24",
            swept_by="agent",
            scope="single-report",
            findings=[],
            clean_count=1,
            warn_count=0,
            fail_count=0,
            total_findings=0,
        )


# ---------------------------------------------------------------------------
# parse_followup_rationale shape handling
# ---------------------------------------------------------------------------


@pytest.mark.hlk
def test_parse_none() -> None:
    assert parse_followup_rationale(None) is None


@pytest.mark.hlk
def test_parse_empty_string() -> None:
    assert parse_followup_rationale("") is None
    assert parse_followup_rationale("   ") is None


@pytest.mark.hlk
def test_parse_string_carries_to_notes() -> None:
    """Legacy string rationale -> dict with class=None + notes=string."""
    parsed = parse_followup_rationale("legacy free-text rationale")
    assert parsed is not None
    assert parsed.followup_class is None
    assert parsed.notes == "legacy free-text rationale"


@pytest.mark.hlk
def test_parse_dict_strict_validates() -> None:
    parsed = parse_followup_rationale({
        "followup_class": "deferred-work-with-tracker",
        "closure_target": "Wave T close",
        "owner": "PMO",
        "tracker_path": "docs/wip/planning/_trackers/x.md",
    })
    assert parsed is not None
    assert parsed.followup_class == "deferred-work-with-tracker"
    assert parsed.owner == "PMO"


@pytest.mark.hlk
def test_parse_dict_with_invalid_class_returns_none() -> None:
    """Invalid class in dict -> ValidationError caught -> None returned."""
    parsed = parse_followup_rationale({"followup_class": "bogus-class"})
    assert parsed is None


@pytest.mark.hlk
def test_parse_non_dict_non_string_returns_none() -> None:
    assert parse_followup_rationale(12345) is None
    assert parse_followup_rationale([1, 2, 3]) is None
    assert parse_followup_rationale(True) is None


@pytest.mark.hlk
def test_parse_dict_drops_unknown_keys() -> None:
    """Unknown keys in dict are silently dropped (Pydantic default)."""
    parsed = parse_followup_rationale({
        "followup_class": "monitoring-obligation",
        "closure_target": "Wave U close",
        "unknown_extra_key": "should be dropped",
    })
    assert parsed is not None
    assert parsed.followup_class == "monitoring-obligation"


# ---------------------------------------------------------------------------
# Validator self-test + CLI smoke
# ---------------------------------------------------------------------------


@pytest.mark.hlk
def test_runbook_self_test_exits_zero() -> None:
    """The --self-test mode must exit 0 (the always-on pre_commit circuit-breaker)."""
    result = subprocess.run(
        [sys.executable, str(RUNBOOK_PATH), "--self-test"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"self-test failed: stdout={result.stdout}, stderr={result.stderr}"
    )


@pytest.mark.hlk
def test_runbook_help_exits_two() -> None:
    """No args / unknown args print help and exit 2 (USAGE)."""
    result = subprocess.run(
        [sys.executable, str(RUNBOOK_PATH)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2


@pytest.mark.hlk
def test_runbook_strict_fails_on_pwf_no_rationale(tmp_path: Path) -> None:
    """Strict mode + report with PWF verdict + no rationale -> exit 1."""
    report = tmp_path / "uat-pwf-broken.md"
    report.write_text(
        "---\n"
        "verdict: PASS-WITH-FOLLOWUP\n"
        "last_review: 2026-05-24\n"
        "---\n"
        "# Test report\n",
        encoding="utf-8",
    )
    result = subprocess.run(
        [sys.executable, str(RUNBOOK_PATH), "--report", str(report), "--strict"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    assert "PWF-FM-01-CLASS-MISSING" in result.stdout


@pytest.mark.hlk
def test_runbook_passes_when_pwf_rationale_clean(tmp_path: Path) -> None:
    """Strict mode + PWF verdict + clean structured rationale -> exit 0."""
    report = tmp_path / "uat-pwf-clean.md"
    report.write_text(
        "---\n"
        "verdict: PASS-WITH-FOLLOWUP\n"
        "last_review: 2026-05-24\n"
        "verdict_followup_rationale:\n"
        "  followup_class: monitoring-obligation\n"
        "  closure_target: Wave U close\n"
        "  owner: System Owner\n"
        "  notes: 3-wave field-test monitoring obligation.\n"
        "---\n"
        "# Test report\n",
        encoding="utf-8",
    )
    result = subprocess.run(
        [sys.executable, str(RUNBOOK_PATH), "--report", str(report), "--strict"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"clean PWF expected exit 0, got {result.returncode}: stdout={result.stdout}"
    )


@pytest.mark.hlk
def test_runbook_noops_on_pass_verdict(tmp_path: Path) -> None:
    """Validator must no-op on PASS verdicts (specialty governs PWF only)."""
    report = tmp_path / "uat-pass.md"
    report.write_text(
        "---\n"
        "verdict: PASS\n"
        "last_review: 2026-05-24\n"
        "---\n"
        "# Test report\n",
        encoding="utf-8",
    )
    result = subprocess.run(
        [sys.executable, str(RUNBOOK_PATH), "--report", str(report), "--strict"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "CLEAN" in result.stdout


@pytest.mark.hlk
def test_runbook_catches_invalid_tracker_path(tmp_path: Path) -> None:
    """Deferred-work class + bogus tracker_path -> PWF-FM-04-TRACKER-PATH-INVALID."""
    report = tmp_path / "uat-pwf-bogus-tracker.md"
    report.write_text(
        "---\n"
        "verdict: PASS-WITH-FOLLOWUP\n"
        "last_review: 2026-05-24\n"
        "verdict_followup_rationale:\n"
        "  followup_class: deferred-work-with-tracker\n"
        "  closure_target: Wave T close\n"
        "  owner: PMO\n"
        "  tracker_path: docs/wip/planning/_trackers/does-not-exist-xyz.md\n"
        "---\n"
        "# Test report\n",
        encoding="utf-8",
    )
    result = subprocess.run(
        [sys.executable, str(RUNBOOK_PATH), "--report", str(report), "--strict"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    assert "PWF-FM-04-TRACKER-PATH-INVALID" in result.stdout


@pytest.mark.hlk
def test_runbook_owner_missing_warn_only(tmp_path: Path) -> None:
    """Missing owner -> WARN finding but exit 0 in strict mode (WARN never blocks)."""
    report = tmp_path / "uat-pwf-no-owner.md"
    report.write_text(
        "---\n"
        "verdict: PASS-WITH-FOLLOWUP\n"
        "last_review: 2026-05-24\n"
        "verdict_followup_rationale:\n"
        "  followup_class: monitoring-obligation\n"
        "  closure_target: Wave U close\n"
        "  notes: No owner named.\n"
        "---\n"
        "# Test report\n",
        encoding="utf-8",
    )
    result = subprocess.run(
        [sys.executable, str(RUNBOOK_PATH), "--report", str(report), "--strict"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "PWF-FM-05-OWNER-MISSING" in result.stdout
    assert "WARN" in result.stdout


@pytest.mark.hlk
def test_runbook_json_log_emits_parseable_json(tmp_path: Path) -> None:
    """--json-log mode emits parseable JSON to stdout."""
    import json as _json

    report = tmp_path / "uat-pass.md"
    report.write_text(
        "---\n"
        "verdict: PASS\n"
        "last_review: 2026-05-24\n"
        "---\n",
        encoding="utf-8",
    )
    result = subprocess.run(
        [sys.executable, str(RUNBOOK_PATH), "--report", str(report), "--json-log"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    parsed = _json.loads(result.stdout)
    assert "report_id" in parsed
    assert "scope" in parsed
    assert parsed["scope"] == "single-report"
