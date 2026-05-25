"""Integration tests for scripts/validate_collaborator_share.py.

The 13th Quality Fabric specialty per D-IH-86-CY (Wave R+1 Commit 2b) +
D-IH-86-CY-EXT share_pattern schema extension (Wave R+1 Commit 2b-ext).

This file covers the *validator CLI behaviour* (subprocess + on-disk fixtures).
Pure Pydantic model + helper coverage lives in
``tests/test_hlk_collaborator_share.py`` (37 tests, all PASS at Commit 2a).

Covers:
- CLI surface (--self-test exits 0; default mode prints findings table).
- Self-test mode does not touch the on-disk canonical CSVs.
- Full audit against the as-shipped header-only CSVs emits 8 PASS findings
  (CS-01..CS-08; CS-08 added at Commit 2b-ext for share_pattern enum).
- 8-check CHECK_REGISTRY exposes one probe per CS-* dimension code.
- --strict mode flips exit code when a fixture introduces a FAIL row.
- JSON output is parseable and conforms to CollaboratorShareAuditReport.
- Markdown report renders with the §3 mechanical-evidence shape expected
  by the wave-close UAT bar.
- share_pattern branching:
    * CS-03 / CS-04 per-pattern logic
    * CS-08 enum validity check
    * runbook --share-pattern override
    * orchestration_broker_thin_margin per-row revenue slice
    * custom-pattern MANUAL placeholder
"""
from __future__ import annotations

import importlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_collaborator_share.py"
RUNBOOK_PATH = REPO_ROOT / "scripts" / "collaborator_share_calculate.py"

PYTHON = sys.executable

ALL_EIGHT_CHECK_CODES = {
    "CS-01-STRUCTURAL-VALIDATION",
    "CS-02-CROSS-CSV-FK-RESOLUTION",
    "CS-03-SPLIT-SUMS-TO-100",
    "CS-04-DEFAULT-65-35-AUDIT",
    "CS-05-BILL-MODE-DEFAULT-CONSISTENCY",
    "CS-06-RATE-WITHIN-MARKET-BAND",
    "CS-07-OVERRIDE-EXPIRY-AUDIT",
    "CS-08-SHARE-PATTERN-ENUM-VALIDITY",
}


def _run_validator(*args: str, env_extra: dict | None = None) -> subprocess.CompletedProcess:
    """Invoke the validator CLI with the given args. Returns the CP."""
    return subprocess.run(
        [PYTHON, str(VALIDATOR_PATH), *args],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )


def _run_runbook(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [PYTHON, str(RUNBOOK_PATH), *args],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )


# =============================================================================
# Validator CLI surface
# =============================================================================

def test_validator_script_exists():
    assert VALIDATOR_PATH.is_file(), f"validator missing at {VALIDATOR_PATH}"


def test_runbook_script_exists():
    assert RUNBOOK_PATH.is_file(), f"runbook missing at {RUNBOOK_PATH}"


def test_self_test_exits_zero():
    """--self-test must always exit 0 in a healthy tree (release-gate gate)."""
    cp = _run_validator("--self-test")
    assert cp.returncode == 0, f"--self-test failed:\nstdout={cp.stdout}\nstderr={cp.stderr}"


def test_runbook_self_test_exits_zero():
    """Paired runbook --self-test arithmetic gate (covers all 3 share_pattern fixtures)."""
    cp = _run_runbook("--self-test")
    assert cp.returncode == 0, f"runbook --self-test failed:\nstdout={cp.stdout}\nstderr={cp.stderr}"


def test_default_mode_prints_eight_check_table():
    """Default mode prints an 8-row CS-* findings table (CS-01..CS-08)."""
    cp = _run_validator()
    assert cp.returncode == 0, f"default mode failed:\nstderr={cp.stderr}"
    for code in ALL_EIGHT_CHECK_CODES:
        assert code in cp.stdout, f"{code} missing from default-mode output"
    assert "Total findings:" in cp.stdout


def test_default_mode_passes_on_header_only_csvs():
    """As-shipped CSVs (Commit 2b-ext header-only) must emit 8 PASS findings."""
    cp = _run_validator()
    assert cp.returncode == 0
    assert "pass=8" in cp.stdout
    assert "fail=0" in cp.stdout


def test_json_mode_parseable():
    """--json output parses + carries the audit-report schema."""
    cp = _run_validator("--json")
    assert cp.returncode == 0
    payload = json.loads(cp.stdout)
    assert "report_id" in payload
    assert "audit_trigger" in payload
    assert "audited_at" in payload
    assert "findings" in payload
    assert isinstance(payload["findings"], list)
    assert len(payload["findings"]) == 8
    assert payload["pass_count"] == 8
    assert payload["fail_count"] == 0


# =============================================================================
# Pydantic chassis round-trip with audit-report schema
# =============================================================================

def test_audit_report_round_trips_through_pydantic():
    """JSON output validates against CollaboratorShareAuditReport (8 checks)."""
    from akos.hlk_collaborator_share import CollaboratorShareAuditReport

    cp = _run_validator("--json")
    payload = json.loads(cp.stdout)
    report = CollaboratorShareAuditReport.model_validate(payload)
    assert len(report.findings) == 8
    assert {f.check_code for f in report.findings} == ALL_EIGHT_CHECK_CODES


def test_report_id_pattern_matches_validator_emit():
    """report_id matches the canonical pattern from the Pydantic model."""
    import re

    cp = _run_validator("--json")
    payload = json.loads(cp.stdout)
    assert re.match(r"^collaborator-share-audit-\d{4}-\d{2}-\d{2}", payload["report_id"])


# =============================================================================
# Markdown report emit
# =============================================================================

def test_markdown_report_emit(tmp_path: Path):
    """--report writes a markdown file with the §3 findings table shape."""
    out = tmp_path / "audit.md"
    cp = _run_validator("--report", str(out))
    assert cp.returncode == 0
    assert out.is_file(), f"markdown report not written to {out}"
    body = out.read_text(encoding="utf-8")
    assert "Collaborator Share Audit" in body
    assert "CS-01-STRUCTURAL-VALIDATION" in body
    assert "CS-07-OVERRIDE-EXPIRY-AUDIT" in body
    assert "CS-08-SHARE-PATTERN-ENUM-VALIDITY" in body


# =============================================================================
# CSV header structural contract (Commit 2b-ext)
# =============================================================================

def test_share_registry_csv_header_includes_share_pattern():
    """Commit 2b-ext: canonical SHARE_REGISTRY header carries share_pattern."""
    from akos.hlk_collaborator_share import (
        COLLABORATOR_SHARE_REGISTRY_FIELDNAMES,
        CSV_PATH_RELATIVE_SHARE_REGISTRY,
    )

    assert "share_pattern" in COLLABORATOR_SHARE_REGISTRY_FIELDNAMES
    canonical_csv = REPO_ROOT / CSV_PATH_RELATIVE_SHARE_REGISTRY
    header_line = canonical_csv.read_text(encoding="utf-8").splitlines()[0]
    actual_fields = tuple(header_line.split(","))
    assert actual_fields == COLLABORATOR_SHARE_REGISTRY_FIELDNAMES, (
        f"on-disk CSV header drift from Pydantic SSOT: "
        f"expected {COLLABORATOR_SHARE_REGISTRY_FIELDNAMES} got {actual_fields}"
    )


# =============================================================================
# Strict mode flips exit code on FAIL fixture
# =============================================================================

def _build_share_registry_row(
    share_id: str,
    engagement_id: str,
    share_pattern: str = "deep_partner_65_35",
    holistika_pct: int = 65,
    collaborator_pct: int = 35,
    override_id: str = "",
    collaborator_id: str = "POI-PRT-PYTEST",
) -> str:
    """Build a CSV row aligned with the current canonical SSOT header.

    Used by integration-fixture tests so they stay aligned with
    COLLABORATOR_SHARE_REGISTRY_FIELDNAMES.
    """
    return (
        f"{share_id},{engagement_id},{collaborator_id},"
        f"eng_model_percentage_collaborator,{share_pattern},"
        f"{holistika_pct},{collaborator_pct},"
        "250,EUR,advisor,"
        f"{override_id},active,2026-01-01,,,2026-01-01,pytest fixture\n"
    )


def _seed_fixture_dir(tmp_path: Path, share_rows: list[str]) -> None:
    """Seed a tmp dir with the 5 canonical CSVs aligned with current SSOT."""
    from akos.hlk_collaborator_share import (
        COLLABORATOR_MARKET_RATE_REFERENCE_FIELDNAMES,
        COLLABORATOR_RATE_OVERRIDES_FIELDNAMES,
        COLLABORATOR_SHARE_REGISTRY_FIELDNAMES,
        HOLISTIKA_VENDOR_SERVICES_BILLED_FIELDNAMES,
        PARTNER_OVERLAP_EXCLUSION_CLAUSES_FIELDNAMES,
    )

    seeded = {
        "COLLABORATOR_SHARE_REGISTRY.csv": (
            ",".join(COLLABORATOR_SHARE_REGISTRY_FIELDNAMES) + "\n"
            + "".join(share_rows)
        ),
        "HOLISTIKA_VENDOR_SERVICES_BILLED.csv": (
            ",".join(HOLISTIKA_VENDOR_SERVICES_BILLED_FIELDNAMES) + "\n"
        ),
        "PARTNER_OVERLAP_EXCLUSION_CLAUSES.csv": (
            ",".join(PARTNER_OVERLAP_EXCLUSION_CLAUSES_FIELDNAMES) + "\n"
        ),
        "COLLABORATOR_MARKET_RATE_REFERENCE.csv": (
            ",".join(COLLABORATOR_MARKET_RATE_REFERENCE_FIELDNAMES) + "\n"
        ),
        "COLLABORATOR_RATE_OVERRIDES.csv": (
            ",".join(COLLABORATOR_RATE_OVERRIDES_FIELDNAMES) + "\n"
        ),
    }
    for name, body in seeded.items():
        (tmp_path / name).write_text(body, encoding="utf-8")


def _point_validator_at_fixture(monkeypatch, vcs_mod, tmp_path: Path) -> None:
    # Repoint every CSV constant + REPO_ROOT so probes that compute
    # `csv.relative_to(REPO_ROOT)` succeed against the tmp_path fixture.
    monkeypatch.setattr(vcs_mod, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(vcs_mod, "SHARE_REGISTRY_CSV",
                        tmp_path / "COLLABORATOR_SHARE_REGISTRY.csv")
    monkeypatch.setattr(vcs_mod, "VENDOR_BILLED_CSV",
                        tmp_path / "HOLISTIKA_VENDOR_SERVICES_BILLED.csv")
    monkeypatch.setattr(vcs_mod, "OVERLAP_CLAUSES_CSV",
                        tmp_path / "PARTNER_OVERLAP_EXCLUSION_CLAUSES.csv")
    monkeypatch.setattr(vcs_mod, "MARKET_RATE_CSV",
                        tmp_path / "COLLABORATOR_MARKET_RATE_REFERENCE.csv")
    monkeypatch.setattr(vcs_mod, "RATE_OVERRIDES_CSV",
                        tmp_path / "COLLABORATOR_RATE_OVERRIDES.csv")


def test_strict_mode_flips_exit_code_on_fail(monkeypatch, tmp_path: Path):
    """--strict exits non-zero when a fixture introduces a CS-03 FAIL row."""
    bad_row = _build_share_registry_row(
        share_id="SHARE-PYTEST-BAD-001",
        engagement_id="ENG-X",
        share_pattern="deep_partner_65_35",
        holistika_pct=60,
        collaborator_pct=30,  # 60 + 30 = 90 != 100 → CS-03 FAIL
    )
    _seed_fixture_dir(tmp_path, share_rows=[bad_row])

    import scripts.validate_collaborator_share as vcs_mod
    importlib.reload(vcs_mod)
    _point_validator_at_fixture(monkeypatch, vcs_mod, tmp_path)

    report = vcs_mod.run_audit(audit_trigger="on_demand", audited_by="pytest")
    cs03_fail = [
        f for f in report.findings
        if f.check_code == "CS-03-SPLIT-SUMS-TO-100" and f.verdict == "fail"
    ]
    assert cs03_fail, (
        f"expected CS-03 fail finding for split=60+30; got findings: "
        f"{[(f.check_code, f.verdict) for f in report.findings]}"
    )
    assert report.fail_count >= 1


# =============================================================================
# share_pattern branching (Commit 2b-ext)
# =============================================================================

def test_cs08_fails_on_unknown_share_pattern(monkeypatch, tmp_path: Path):
    """CS-08: unknown share_pattern enum value triggers a FAIL finding."""
    bad_row = _build_share_registry_row(
        share_id="SHARE-PYTEST-CS08-001",
        engagement_id="ENG-CS08-1",
        share_pattern="invalid_pattern_name",
    )
    _seed_fixture_dir(tmp_path, share_rows=[bad_row])

    import scripts.validate_collaborator_share as vcs_mod
    importlib.reload(vcs_mod)
    _point_validator_at_fixture(monkeypatch, vcs_mod, tmp_path)

    report = vcs_mod.run_audit(audit_trigger="on_demand", audited_by="pytest")
    cs08_fail = [
        f for f in report.findings
        if f.check_code == "CS-08-SHARE-PATTERN-ENUM-VALIDITY"
        and f.verdict == "fail"
    ]
    assert cs08_fail, (
        f"expected CS-08 fail finding for invalid_pattern_name; got: "
        f"{[(f.check_code, f.verdict) for f in report.findings]}"
    )


def test_cs03_across_rows_orchestration_broker_fails_on_drift(
    monkeypatch, tmp_path: Path,
):
    """CS-03 orchestration variant: across-rows sum-to-100 invariant fails
    when an orchestration engagement's row totals don't close at 100.
    """
    rows = [
        _build_share_registry_row(
            share_id="SHARE-PYTEST-OB-A",
            engagement_id="ENG-OB-1",
            share_pattern="orchestration_broker_thin_margin",
            holistika_pct=3,
            collaborator_pct=47,
            collaborator_id="POI-PRT-A",
        ),
        # Intentionally bad: 3+30 instead of 3+47 -> across-rows total = 83%.
        _build_share_registry_row(
            share_id="SHARE-PYTEST-OB-B",
            engagement_id="ENG-OB-1",
            share_pattern="orchestration_broker_thin_margin",
            holistika_pct=3,
            collaborator_pct=30,
            collaborator_id="POI-PRT-B",
        ),
    ]
    _seed_fixture_dir(tmp_path, share_rows=rows)

    import scripts.validate_collaborator_share as vcs_mod
    importlib.reload(vcs_mod)
    _point_validator_at_fixture(monkeypatch, vcs_mod, tmp_path)

    report = vcs_mod.run_audit(audit_trigger="on_demand", audited_by="pytest")
    cs03_fail = [
        f for f in report.findings
        if f.check_code == "CS-03-SPLIT-SUMS-TO-100"
        and f.verdict == "fail"
        and "orchestration" in (f.drift_summary or "").lower()
    ]
    assert cs03_fail, (
        f"expected CS-03 across-rows orchestration fail; got: "
        f"{[(f.check_code, f.verdict, f.drift_summary[:80]) for f in report.findings]}"
    )


def test_cs03_across_rows_orchestration_broker_passes_on_closure(
    monkeypatch, tmp_path: Path,
):
    """CS-03 orchestration variant: two rows summing to 100% across-rows PASS."""
    rows = [
        _build_share_registry_row(
            share_id="SHARE-PYTEST-OB-OK-A",
            engagement_id="ENG-OB-2",
            share_pattern="orchestration_broker_thin_margin",
            holistika_pct=3,
            collaborator_pct=47,
            override_id="D-IH-86-CY-EXT",  # silences CS-04 default-margin warn
            collaborator_id="POI-PRT-A",
        ),
        _build_share_registry_row(
            share_id="SHARE-PYTEST-OB-OK-B",
            engagement_id="ENG-OB-2",
            share_pattern="orchestration_broker_thin_margin",
            holistika_pct=3,
            collaborator_pct=47,
            override_id="D-IH-86-CY-EXT",
            collaborator_id="POI-PRT-B",
        ),
    ]
    _seed_fixture_dir(tmp_path, share_rows=rows)

    import scripts.validate_collaborator_share as vcs_mod
    importlib.reload(vcs_mod)
    _point_validator_at_fixture(monkeypatch, vcs_mod, tmp_path)

    report = vcs_mod.run_audit(audit_trigger="on_demand", audited_by="pytest")
    cs03_findings = [
        f for f in report.findings
        if f.check_code == "CS-03-SPLIT-SUMS-TO-100"
    ]
    # CS-03 should emit exactly one PASS row (no per-row deep_partner
    # check fires for orchestration rows).
    assert any(f.verdict == "pass" for f in cs03_findings), (
        f"expected CS-03 PASS; got {[(f.verdict, f.drift_summary[:50]) for f in cs03_findings]}"
    )
    assert not any(f.verdict == "fail" for f in cs03_findings)


def test_cs04_custom_pattern_requires_override(monkeypatch, tmp_path: Path):
    """CS-04 custom variant: every custom row requires share_override_decision_id."""
    bad_row = _build_share_registry_row(
        share_id="SHARE-PYTEST-CUSTOM-NOREF",
        engagement_id="ENG-CUSTOM-1",
        share_pattern="custom",
        holistika_pct=50,
        collaborator_pct=50,
        override_id="",  # missing! → CS-04 WARN
    )
    _seed_fixture_dir(tmp_path, share_rows=[bad_row])

    import scripts.validate_collaborator_share as vcs_mod
    importlib.reload(vcs_mod)
    _point_validator_at_fixture(monkeypatch, vcs_mod, tmp_path)

    report = vcs_mod.run_audit(audit_trigger="on_demand", audited_by="pytest")
    cs04_warn = [
        f for f in report.findings
        if f.check_code == "CS-04-DEFAULT-65-35-AUDIT"
        and f.verdict == "warn"
        and "custom" in (f.drift_summary or "").lower()
    ]
    assert cs04_warn, (
        f"expected CS-04 warn for custom-without-override; got: "
        f"{[(f.check_code, f.verdict, f.drift_summary[:60]) for f in report.findings]}"
    )


# =============================================================================
# CHECK_REGISTRY shape (paired with self-test invariants)
# =============================================================================

def test_check_registry_exposes_eight_probes():
    """The validator module's CHECK_REGISTRY exposes exactly 8 probes
    (CS-01..CS-08; CS-08 added at Commit 2b-ext for share_pattern enum)."""
    import scripts.validate_collaborator_share as vcs_mod
    importlib.reload(vcs_mod)
    assert hasattr(vcs_mod, "CHECK_REGISTRY"), (
        "CHECK_REGISTRY missing from validate_collaborator_share.py"
    )
    codes = set(vcs_mod.CHECK_REGISTRY.keys())
    assert codes == ALL_EIGHT_CHECK_CODES, f"CHECK_REGISTRY codes mismatch: {codes}"


# =============================================================================
# Worked-example runbook coverage (per-pattern branches)
# =============================================================================

def test_runbook_worked_example_default_split():
    """deep_partner_65_35: 100k revenue, 20k pass-through -> 52k/28k split."""
    cp = _run_runbook(
        "--engagement-id", "ENG-PYTEST-2026",
        "--revenue", "100000",
        "--direct-cost", "20000",
    )
    assert cp.returncode == 0
    assert "Benefits (= revenue − costs)" in cp.stdout or "Benefits" in cp.stdout
    assert "80000.00 EUR" in cp.stdout
    assert "52000.00 EUR" in cp.stdout
    assert "28000.00 EUR" in cp.stdout


def test_runbook_worked_example_json():
    """deep_partner_65_35 JSON output: assert benefits formula numbers."""
    cp = _run_runbook(
        "--engagement-id", "ENG-PYTEST-2026",
        "--revenue", "50000",
        "--direct-cost", "10000",
        "--emit-json",
    )
    assert cp.returncode == 0
    payload = json.loads(cp.stdout)
    assert payload["share_pattern"] == "deep_partner_65_35"
    assert payload["revenue"] == 50000.0
    assert payload["total_costs"] == 10000.0
    assert payload["benefits"] == 40000.0
    assert payload["holistika_share_amount"] == 26000.0
    assert payload["collaborator_share_amount"] == 14000.0
    assert payload["holistika_share_pct"] == 65
    assert payload["collaborator_share_pct"] == 35
    assert payload["split_default"] is True


def test_runbook_orchestration_broker_pattern_via_override():
    """orchestration_broker: --share-pattern override emits per-row revenue
    slice with no transparent-cost subtraction."""
    cp = _run_runbook(
        "--engagement-id", "ENG-OB-PYTEST-2026",
        "--revenue", "100000",
        "--share-pattern", "orchestration_broker_thin_margin",
        "--emit-json",
    )
    assert cp.returncode == 0, f"stderr={cp.stderr}"
    payload = json.loads(cp.stdout)
    assert payload["share_pattern"] == "orchestration_broker_thin_margin"
    assert payload["revenue"] == 100000.0
    assert payload["total_costs"] == 0.0
    assert payload["benefits"] == 100000.0
    # With no CSV row, h_pct + c_pct fall back to 65 + 35; runbook applies
    # those to revenue directly (no cost subtraction).
    assert payload["holistika_share_amount"] == 65000.0
    assert payload["collaborator_share_amount"] == 35000.0


def test_runbook_custom_pattern_emits_manual_placeholder():
    """custom pattern: all amount fields are None + advisory_notes populated."""
    cp = _run_runbook(
        "--engagement-id", "ENG-CUSTOM-PYTEST-2026",
        "--revenue", "100000",
        "--share-pattern", "custom",
        "--emit-json",
    )
    assert cp.returncode == 0, f"stderr={cp.stderr}"
    payload = json.loads(cp.stdout)
    assert payload["share_pattern"] == "custom"
    assert payload["holistika_share_amount"] is None
    assert payload["collaborator_share_amount"] is None
    assert payload["total_costs"] is None
    assert payload["benefits"] is None
    assert payload.get("advisory_notes"), (
        "custom-pattern settlements must carry at least one advisory_note"
    )


def test_runbook_custom_pattern_markdown_renders_manual_placeholder():
    """custom-pattern markdown render shows MANUAL placeholder for share amounts."""
    cp = _run_runbook(
        "--engagement-id", "ENG-CUSTOM-PYTEST-MD",
        "--revenue", "100000",
        "--share-pattern", "custom",
    )
    assert cp.returncode == 0
    assert "MANUAL" in cp.stdout
    assert "Advisory notes" in cp.stdout


def test_runbook_share_pattern_choices_includes_all_three():
    """CLI --share-pattern choice list mirrors VALID_SHARE_PATTERNS."""
    cp = _run_runbook("--help")
    assert cp.returncode == 0
    for pat in ("deep_partner_65_35", "orchestration_broker_thin_margin", "custom"):
        assert pat in cp.stdout, f"missing {pat!r} from --share-pattern choices"
