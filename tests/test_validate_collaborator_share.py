"""Integration tests for scripts/validate_collaborator_share.py.

The 13th Quality Fabric specialty per D-IH-86-DA quintet (Wave R+1
Commits 2a/2b/2b-ext/2c-a/2c-b) + the Wave R+2 doctrine rewrite
(D-IH-86-EJ..EN; Commits 1-3) that:

- replaced the pre-rewrite 3-shape share_pattern enum
  (deep_partner_65_35 / orchestration_broker_thin_margin / custom) with
  the 4-base + 1-stackable-overlay enum
  (deep_partner_65_35 / bd_intro_only / joint_venture_aventure /
   consulting_direct, with bd_commission_overlay as the only overlay);
- added methodology_readiness as a mandatory enum gating share_pattern
  eligibility (D-IH-86-EN);
- added the parallel_invoice_stream_indicator boolean column
  (D-IH-86-EK);
- added CS-09 (overlay-base pairing + methodology-pattern coherence)
  as the ninth audit check (D-IH-86-EJ).

This file covers the *validator CLI behaviour* (subprocess + on-disk
fixtures). Pure Pydantic model + helper coverage lives in
``tests/test_hlk_collaborator_share.py``. Pure runbook arithmetic
coverage lives in ``tests/test_collaborator_share_calculate.py``.

Covers:
- CLI surface (--self-test exits 0; default mode prints findings table).
- Self-test mode does not touch the on-disk canonical CSVs.
- Full audit against the as-shipped header-only CSVs emits 9 PASS
  findings (CS-01..CS-09).
- 9-check CHECK_REGISTRY exposes one probe per CS-* dimension code.
- --strict mode flips exit code when a fixture introduces a FAIL row.
- JSON output is parseable and conforms to CollaboratorShareAuditReport.
- Markdown report renders with the §3 mechanical-evidence shape expected
  by the wave-close UAT bar.
- share_pattern branching (Wave R+2 4-base + 1-overlay enum):
    * CS-03 across-rows sum-to-100 for overlay engagements
    * CS-08 enum validity (4-base post-rewrite)
    * CS-09 overlay-base pairing (consulting_direct + bd_commission_overlay)
    * CS-09 standalone-overlay rejection (no base row)
    * CS-09 methodology-pattern coherence
      (methodology_naive disallows deep_partner_65_35)
    * runbook --share-pattern override (4 base patterns) + JSON schema
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

ALL_NINE_CHECK_CODES = {
    "CS-01-STRUCTURAL-VALIDATION",
    "CS-02-CROSS-CSV-FK-RESOLUTION",
    "CS-03-SPLIT-SUMS-TO-100",
    "CS-04-DEFAULT-65-35-AUDIT",
    "CS-05-BILL-MODE-DEFAULT-CONSISTENCY",
    "CS-06-RATE-WITHIN-MARKET-BAND",
    "CS-07-OVERRIDE-EXPIRY-AUDIT",
    "CS-08-SHARE-PATTERN-ENUM-VALIDITY",
    "CS-09-OVERLAY-BASE-PAIRING-VALIDITY",
}


def _run_validator(*args: str) -> subprocess.CompletedProcess:
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


# ===========================================================================
# Validator CLI surface
# ===========================================================================

def test_validator_script_exists():
    assert VALIDATOR_PATH.is_file(), f"validator missing at {VALIDATOR_PATH}"


def test_runbook_script_exists():
    assert RUNBOOK_PATH.is_file(), f"runbook missing at {RUNBOOK_PATH}"


def test_self_test_exits_zero():
    """--self-test must always exit 0 in a healthy tree (release-gate gate)."""
    cp = _run_validator("--self-test")
    assert cp.returncode == 0, (
        f"--self-test failed:\nstdout={cp.stdout}\nstderr={cp.stderr}"
    )


def test_runbook_self_test_exits_zero():
    """Paired runbook --self-test arithmetic gate (covers fixtures A..E:
    the 4 base patterns + the unified TRUE-MARGIN formula)."""
    cp = _run_runbook("--self-test")
    assert cp.returncode == 0, (
        f"runbook --self-test failed:\nstdout={cp.stdout}\nstderr={cp.stderr}"
    )


# ===========================================================================
# In-process default-mode tests (header-only fixture; avoid coupling to
# pre-existing on-disk SHARE_REGISTRY drift that is repaired at Commit 5
# per D-IH-86-EJ-EXT migration SQL + SUEZ row recommercialisation).
#
# These tests verify the VALIDATOR's BEHAVIOUR on a clean header-only
# fixture — which is what the as-shipped on-disk state will be after
# Commit 5 lands. The subprocess-based --self-test and --help tests
# stay because they don't depend on the on-disk SHARE_REGISTRY rows.
# Helper definitions (_seed_fixture_dir + _point_validator_at_fixture)
# live below in the "Strict mode flips exit code on FAIL fixture" section
# because they're shared between strict-mode + CS-NN per-fixture tests.
# ===========================================================================


def _run_audit_on_empty_fixture(monkeypatch, tmp_path: Path):
    """Run validator's run_audit() in-process against a header-only fixture.

    Returns the CollaboratorShareAuditReport. This is the in-process
    counterpart to subprocess-based ``_run_validator()`` and is the
    correct shape for testing validator behaviour without coupling to
    the current on-disk canonical-CSV state (which carries pre-existing
    Wave R+2 drift fixed at Commit 5 per D-IH-86-EJ-EXT migration SQL).
    """
    _seed_fixture_dir(tmp_path, share_rows=[])
    import scripts.validate_collaborator_share as vcs_mod
    importlib.reload(vcs_mod)
    _point_validator_at_fixture(monkeypatch, vcs_mod, tmp_path)
    return vcs_mod.run_audit(audit_trigger="on_demand", audited_by="pytest")


def test_run_audit_returns_nine_findings_on_header_only_fixture(
    monkeypatch, tmp_path: Path,
):
    """In-process: run_audit on a header-only fixture must emit exactly
    9 findings (one per CS-* dimension code in CHECK_REGISTRY)."""
    report = _run_audit_on_empty_fixture(monkeypatch, tmp_path)
    assert len(report.findings) == 9
    assert {f.check_code for f in report.findings} == ALL_NINE_CHECK_CODES


def test_run_audit_passes_on_header_only_fixture(monkeypatch, tmp_path: Path):
    """In-process: header-only fixture must yield 9 PASS findings + 0 FAIL.
    Locks the contract: an as-shipped clean-slate canonical CSV set yields
    a green audit (the steady-state post-Commit 5 baseline).
    """
    report = _run_audit_on_empty_fixture(monkeypatch, tmp_path)
    assert report.pass_count == 9, (
        f"expected pass_count=9 on header-only fixture; got "
        f"pass={report.pass_count}/fail={report.fail_count}/"
        f"warn={report.warn_count} "
        f"verdicts={[(f.check_code, f.verdict) for f in report.findings]}"
    )
    assert report.fail_count == 0


def test_run_audit_emits_pydantic_serializable_report(monkeypatch, tmp_path: Path):
    """In-process: run_audit output round-trips through
    CollaboratorShareAuditReport (JSON dump → model_validate) carrying
    the audit-report schema."""
    from akos.hlk_collaborator_share import CollaboratorShareAuditReport

    report = _run_audit_on_empty_fixture(monkeypatch, tmp_path)
    payload = report.model_dump(mode="json")
    for key in (
        "report_id",
        "audit_trigger",
        "audited_at",
        "findings",
        "pass_count",
        "fail_count",
    ):
        assert key in payload, f"missing audit-report schema key {key!r}"

    round_tripped = CollaboratorShareAuditReport.model_validate(payload)
    assert len(round_tripped.findings) == 9
    assert {f.check_code for f in round_tripped.findings} == ALL_NINE_CHECK_CODES


def test_run_audit_report_id_matches_canonical_pattern(monkeypatch, tmp_path: Path):
    """In-process: report_id matches the canonical pattern
    ``collaborator-share-audit-YYYY-MM-DD-*`` from the Pydantic model."""
    import re

    report = _run_audit_on_empty_fixture(monkeypatch, tmp_path)
    assert re.match(
        r"^collaborator-share-audit-\d{4}-\d{2}-\d{2}", report.report_id
    ), f"report_id {report.report_id!r} does not match canonical pattern"


# ===========================================================================
# Markdown report emit (in-process via render_markdown helper)
# ===========================================================================


def test_render_markdown_emits_nine_check_table(monkeypatch, tmp_path: Path):
    """render_markdown() over a header-only fixture report contains the
    §3 findings table shape expected by the wave-close UAT bar, with
    rows for all 9 CS-* codes (CS-09 added at Wave R+2 Commit 3)."""
    import scripts.validate_collaborator_share as vcs_mod
    importlib.reload(vcs_mod)
    _seed_fixture_dir(tmp_path, share_rows=[])
    _point_validator_at_fixture(monkeypatch, vcs_mod, tmp_path)

    report = vcs_mod.run_audit(audit_trigger="on_demand", audited_by="pytest")
    body = vcs_mod.render_markdown(report)

    assert "Collaborator Share Audit" in body
    for code in ALL_NINE_CHECK_CODES:
        assert code in body, f"render_markdown body missing {code}"
    assert "## Findings" in body
    assert "| Check | Subject |" in body


# ===========================================================================
# CSV header structural contract (Wave R+2 Commit 2 — 20 columns)
# ===========================================================================

def test_share_registry_pydantic_ssot_has_twenty_columns():
    """Wave R+2 Commit 2 (D-IH-86-EJ/EK/EN): the Pydantic SSOT tuple
    ``COLLABORATOR_SHARE_REGISTRY_FIELDNAMES`` carries 20 columns including
    share_overlay + methodology_readiness + parallel_invoice_stream_indicator.

    This test locks the **SSOT shape**. The on-disk CSV header is repaired
    at Commit 5 of the Wave R+2 doctrine rewrite tranche per the
    D-IH-86-EJ-EXT migration SQL; until then, the on-disk header carries
    the legacy 17-column shape and the SUEZ rows authored under that shape.
    """
    from akos.hlk_collaborator_share import (
        COLLABORATOR_SHARE_REGISTRY_FIELDNAMES,
    )

    assert "share_pattern" in COLLABORATOR_SHARE_REGISTRY_FIELDNAMES
    assert "share_overlay" in COLLABORATOR_SHARE_REGISTRY_FIELDNAMES
    assert "methodology_readiness" in COLLABORATOR_SHARE_REGISTRY_FIELDNAMES
    assert (
        "parallel_invoice_stream_indicator" in COLLABORATOR_SHARE_REGISTRY_FIELDNAMES
    )
    assert len(COLLABORATOR_SHARE_REGISTRY_FIELDNAMES) == 20, (
        f"Wave R+2 SHARE_REGISTRY schema is 20 cols; got "
        f"{len(COLLABORATOR_SHARE_REGISTRY_FIELDNAMES)}"
    )


@pytest.mark.xfail(
    reason=(
        "on-disk SHARE_REGISTRY header carries legacy 17-col shape per "
        "pre-Wave-R+2 SUEZ authoring; migration SQL "
        "D-IH-86-EJ-EXT lands at Commit 5 of the Wave R+2 doctrine "
        "rewrite tranche. Test flips to PASS once Commit 5 lands."
    ),
    strict=True,
)
def test_share_registry_on_disk_header_matches_pydantic_ssot():
    """The canonical CSV header on disk equals the Pydantic SSOT tuple.

    Currently xfail-strict — flips to PASS at Commit 5 of the Wave R+2
    doctrine rewrite tranche when the migration SQL + recommercialised
    SUEZ rows land together. xfail-strict ensures Commit 5 cannot
    silently land without the SSOT/disk parity restored (test will
    XPASS and the suite turns red).
    """
    from akos.hlk_collaborator_share import (
        COLLABORATOR_SHARE_REGISTRY_FIELDNAMES,
        CSV_PATH_RELATIVE_SHARE_REGISTRY,
    )

    canonical_csv = REPO_ROOT / CSV_PATH_RELATIVE_SHARE_REGISTRY
    header_line = canonical_csv.read_text(encoding="utf-8").splitlines()[0]
    actual_fields = tuple(header_line.split(","))
    assert actual_fields == COLLABORATOR_SHARE_REGISTRY_FIELDNAMES, (
        f"on-disk CSV header drift from Pydantic SSOT: "
        f"expected {COLLABORATOR_SHARE_REGISTRY_FIELDNAMES} got {actual_fields}"
    )


# ===========================================================================
# Strict mode flips exit code on FAIL fixture
# ===========================================================================

def _build_share_registry_row(
    share_id: str,
    engagement_id: str,
    share_pattern: str = "deep_partner_65_35",
    share_overlay: str = "",
    holistika_pct: int = 65,
    collaborator_pct: int = 35,
    methodology_readiness: str = "methodology_trained",
    override_id: str = "",
    collaborator_id: str = "POI-PRT-PYTEST",
    parallel_invoice: str = "false",
) -> str:
    """Build a 20-column CSV row aligned with the current canonical SSOT
    header per ``COLLABORATOR_SHARE_REGISTRY_FIELDNAMES``.

    Field order (per Wave R+2 Commit 2 / D-IH-86-EJ/EK/EN):
      1.  share_id
      2.  engagement_id
      3.  collaborator_id
      4.  engagement_model_id
      5.  share_pattern
      6.  share_overlay
      7.  holistika_share_pct
      8.  collaborator_share_pct
      9.  collaborator_billed_rate
      10. collaborator_billed_rate_currency
      11. collaborator_role_class
      12. methodology_readiness
      13. share_override_decision_id
      14. status
      15. signed_at
      16. signed_by_collaborator
      17. signed_by_holistika
      18. last_review_at
      19. notes
      20. parallel_invoice_stream_indicator
    """
    return (
        f"{share_id},{engagement_id},{collaborator_id},"
        f"eng_model_percentage_collaborator,{share_pattern},{share_overlay},"
        f"{holistika_pct},{collaborator_pct},"
        f"250,EUR,advisor,{methodology_readiness},"
        f"{override_id},active,2026-01-01,,,2026-01-01,pytest fixture,"
        f"{parallel_invoice}\n"
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
    monkeypatch.setattr(
        vcs_mod, "SHARE_REGISTRY_CSV", tmp_path / "COLLABORATOR_SHARE_REGISTRY.csv"
    )
    monkeypatch.setattr(
        vcs_mod,
        "VENDOR_BILLED_CSV",
        tmp_path / "HOLISTIKA_VENDOR_SERVICES_BILLED.csv",
    )
    monkeypatch.setattr(
        vcs_mod,
        "OVERLAP_CLAUSES_CSV",
        tmp_path / "PARTNER_OVERLAP_EXCLUSION_CLAUSES.csv",
    )
    monkeypatch.setattr(
        vcs_mod, "MARKET_RATE_CSV", tmp_path / "COLLABORATOR_MARKET_RATE_REFERENCE.csv"
    )
    monkeypatch.setattr(
        vcs_mod, "RATE_OVERRIDES_CSV", tmp_path / "COLLABORATOR_RATE_OVERRIDES.csv"
    )


def test_strict_mode_flips_exit_code_on_fail(monkeypatch, tmp_path: Path):
    """--strict-equivalent: a CS-03 split-sum FAIL row produces a fail
    finding in the report (CI release-gate exits non-zero when run_audit
    is invoked with --strict).
    """
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
        f
        for f in report.findings
        if f.check_code == "CS-03-SPLIT-SUMS-TO-100" and f.verdict == "fail"
    ]
    assert cs03_fail, (
        f"expected CS-03 fail finding for split=60+30; got findings: "
        f"{[(f.check_code, f.verdict) for f in report.findings]}"
    )
    assert report.fail_count >= 1


# ===========================================================================
# CS-08: share_pattern enum validity (4-base post-rewrite)
# ===========================================================================

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
        f
        for f in report.findings
        if f.check_code == "CS-08-SHARE-PATTERN-ENUM-VALIDITY"
        and f.verdict == "fail"
    ]
    assert cs08_fail, (
        f"expected CS-08 fail finding for invalid_pattern_name; got: "
        f"{[(f.check_code, f.verdict) for f in report.findings]}"
    )


def test_cs08_fails_on_removed_legacy_pattern(monkeypatch, tmp_path: Path):
    """CS-08: the pre-rewrite ``orchestration_broker_thin_margin`` value
    is no longer in VALID_SHARE_PATTERNS → CS-08 must FAIL on it. This
    locks in the migration: any legacy row carrying the removed value
    must be supersedeed at Commit 5 (D-IH-86-EJ migration SQL).
    """
    legacy_row = _build_share_registry_row(
        share_id="SHARE-LEGACY-OB-001",
        engagement_id="ENG-LEGACY-1",
        share_pattern="orchestration_broker_thin_margin",
    )
    _seed_fixture_dir(tmp_path, share_rows=[legacy_row])

    import scripts.validate_collaborator_share as vcs_mod
    importlib.reload(vcs_mod)
    _point_validator_at_fixture(monkeypatch, vcs_mod, tmp_path)

    report = vcs_mod.run_audit(audit_trigger="on_demand", audited_by="pytest")
    cs08_fail = [
        f
        for f in report.findings
        if f.check_code == "CS-08-SHARE-PATTERN-ENUM-VALIDITY"
        and f.verdict == "fail"
    ]
    assert cs08_fail, (
        f"expected CS-08 fail on removed orchestration_broker_thin_margin; "
        f"got: {[(f.check_code, f.verdict) for f in report.findings]}"
    )


# ===========================================================================
# CS-03: across-rows split-sum-to-100 for overlay engagements
# ===========================================================================

def test_cs03_across_rows_overlay_engagement_passes_on_closure(
    monkeypatch, tmp_path: Path,
):
    """CS-03 overlay variant: a consulting_direct base row (85/0) + a
    bd_commission_overlay sibling row (0/15) must close at 100% across-
    rows for the same engagement_id. Both at correct anchors → CS-03 PASS.
    """
    rows = [
        _build_share_registry_row(
            share_id="SHARE-OVL-BASE-A",
            engagement_id="ENG-OVL-1",
            share_pattern="consulting_direct",
            share_overlay="",  # base row
            holistika_pct=85,
            collaborator_pct=0,
            methodology_readiness="methodology_trained",
            collaborator_id="POI-PRT-A",
        ),
        _build_share_registry_row(
            share_id="SHARE-OVL-OVL-B",
            engagement_id="ENG-OVL-1",
            share_pattern="consulting_direct",
            share_overlay="bd_commission_overlay",
            holistika_pct=0,
            collaborator_pct=15,
            methodology_readiness="methodology_trained",
            collaborator_id="POI-PRT-B",
        ),
    ]
    _seed_fixture_dir(tmp_path, share_rows=rows)

    import scripts.validate_collaborator_share as vcs_mod
    importlib.reload(vcs_mod)
    _point_validator_at_fixture(monkeypatch, vcs_mod, tmp_path)

    report = vcs_mod.run_audit(audit_trigger="on_demand", audited_by="pytest")
    cs03_findings = [
        f for f in report.findings if f.check_code == "CS-03-SPLIT-SUMS-TO-100"
    ]
    assert cs03_findings, "CS-03 finding missing entirely"
    assert not any(f.verdict == "fail" for f in cs03_findings), (
        f"unexpected CS-03 FAIL for 85+0/0+15=100; got: "
        f"{[(f.verdict, (f.drift_summary or '')[:80]) for f in cs03_findings]}"
    )


def test_cs03_across_rows_overlay_engagement_fails_on_drift(
    monkeypatch, tmp_path: Path,
):
    """CS-03 overlay variant: when an overlay engagement's row totals
    don't close at 100 across-rows, CS-03 FAILs.
    """
    rows = [
        _build_share_registry_row(
            share_id="SHARE-OVL-DRIFT-A",
            engagement_id="ENG-OVL-DRIFT",
            share_pattern="consulting_direct",
            share_overlay="",
            holistika_pct=85,
            collaborator_pct=0,
            methodology_readiness="methodology_trained",
            collaborator_id="POI-PRT-A",
        ),
        # Bad: 85 + 0 + 0 + 10 = 95% across-rows (not 100).
        _build_share_registry_row(
            share_id="SHARE-OVL-DRIFT-B",
            engagement_id="ENG-OVL-DRIFT",
            share_pattern="consulting_direct",
            share_overlay="bd_commission_overlay",
            holistika_pct=0,
            collaborator_pct=10,
            methodology_readiness="methodology_trained",
            collaborator_id="POI-PRT-B",
        ),
    ]
    _seed_fixture_dir(tmp_path, share_rows=rows)

    import scripts.validate_collaborator_share as vcs_mod
    importlib.reload(vcs_mod)
    _point_validator_at_fixture(monkeypatch, vcs_mod, tmp_path)

    report = vcs_mod.run_audit(audit_trigger="on_demand", audited_by="pytest")
    cs03_fail = [
        f
        for f in report.findings
        if f.check_code == "CS-03-SPLIT-SUMS-TO-100" and f.verdict == "fail"
    ]
    assert cs03_fail, (
        f"expected CS-03 across-rows FAIL for 85+0/0+10=95; got: "
        f"{[(f.check_code, f.verdict, (f.drift_summary or '')[:80]) for f in report.findings]}"
    )


# ===========================================================================
# CS-09: overlay-base pairing + methodology-pattern coherence
# ===========================================================================

def test_cs09_overlay_with_invalid_base_pairing_fails(
    monkeypatch, tmp_path: Path,
):
    """CS-09: bd_commission_overlay paired with a base row whose
    share_pattern is NOT in
    ``VALID_OVERLAY_BASE_PAIRINGS["bd_commission_overlay"]``
    (= {consulting_direct, deep_partner_65_35}) must FAIL. Here:
    bd_intro_only base is NOT a permitted pairing.
    """
    rows = [
        _build_share_registry_row(
            share_id="SHARE-CS09-BAD-BASE",
            engagement_id="ENG-CS09-BAD",
            share_pattern="bd_intro_only",
            share_overlay="",
            holistika_pct=85,
            collaborator_pct=15,
            methodology_readiness="methodology_trained",
            collaborator_id="POI-PRT-A",
        ),
        _build_share_registry_row(
            share_id="SHARE-CS09-BAD-OVL",
            engagement_id="ENG-CS09-BAD",
            share_pattern="bd_intro_only",
            share_overlay="bd_commission_overlay",
            holistika_pct=0,
            collaborator_pct=0,
            methodology_readiness="methodology_trained",
            collaborator_id="POI-PRT-B",
        ),
    ]
    _seed_fixture_dir(tmp_path, share_rows=rows)

    import scripts.validate_collaborator_share as vcs_mod
    importlib.reload(vcs_mod)
    _point_validator_at_fixture(monkeypatch, vcs_mod, tmp_path)

    report = vcs_mod.run_audit(audit_trigger="on_demand", audited_by="pytest")
    cs09_fail = [
        f
        for f in report.findings
        if f.check_code == "CS-09-OVERLAY-BASE-PAIRING-VALIDITY"
        and f.verdict == "fail"
    ]
    assert cs09_fail, (
        f"expected CS-09 FAIL for bd_intro_only + bd_commission_overlay; "
        f"got: {[(f.check_code, f.verdict, (f.drift_summary or '')[:80]) for f in report.findings]}"
    )


def test_cs09_overlay_without_base_row_fails(monkeypatch, tmp_path: Path):
    """CS-09: a standalone overlay row (no base row in the same
    engagement) must FAIL because overlays cannot exist without their
    sibling base row to anchor against.
    """
    standalone_overlay = _build_share_registry_row(
        share_id="SHARE-CS09-STANDALONE",
        engagement_id="ENG-CS09-STANDALONE",
        share_pattern="consulting_direct",
        share_overlay="bd_commission_overlay",
        holistika_pct=0,
        collaborator_pct=15,
        methodology_readiness="methodology_trained",
        collaborator_id="POI-PRT-A",
    )
    _seed_fixture_dir(tmp_path, share_rows=[standalone_overlay])

    import scripts.validate_collaborator_share as vcs_mod
    importlib.reload(vcs_mod)
    _point_validator_at_fixture(monkeypatch, vcs_mod, tmp_path)

    report = vcs_mod.run_audit(audit_trigger="on_demand", audited_by="pytest")
    cs09_fail = [
        f
        for f in report.findings
        if f.check_code == "CS-09-OVERLAY-BASE-PAIRING-VALIDITY"
        and f.verdict == "fail"
    ]
    assert cs09_fail, (
        f"expected CS-09 FAIL for standalone overlay without base row; "
        f"got: {[(f.check_code, f.verdict, (f.drift_summary or '')[:80]) for f in report.findings]}"
    )


def test_cs09_methodology_pattern_incoherence_fails(
    monkeypatch, tmp_path: Path,
):
    """CS-09: a methodology_naive collaborator with share_pattern =
    deep_partner_65_35 violates the methodology→pattern permissibility
    matrix (35% share requires methodology contribution). Must FAIL.
    """
    incoherent_row = _build_share_registry_row(
        share_id="SHARE-CS09-METH-001",
        engagement_id="ENG-CS09-METH",
        share_pattern="deep_partner_65_35",
        share_overlay="",
        holistika_pct=65,
        collaborator_pct=35,
        methodology_readiness="methodology_naive",  # not permitted for deep_partner
        collaborator_id="POI-PRT-A",
    )
    _seed_fixture_dir(tmp_path, share_rows=[incoherent_row])

    import scripts.validate_collaborator_share as vcs_mod
    importlib.reload(vcs_mod)
    _point_validator_at_fixture(monkeypatch, vcs_mod, tmp_path)

    report = vcs_mod.run_audit(audit_trigger="on_demand", audited_by="pytest")
    cs09_fail = [
        f
        for f in report.findings
        if f.check_code == "CS-09-OVERLAY-BASE-PAIRING-VALIDITY"
        and f.verdict == "fail"
    ]
    assert cs09_fail, (
        f"expected CS-09 FAIL for methodology_naive + deep_partner_65_35; "
        f"got: {[(f.check_code, f.verdict, (f.drift_summary or '')[:80]) for f in report.findings]}"
    )


def test_cs09_clean_overlay_engagement_passes(monkeypatch, tmp_path: Path):
    """CS-09: a properly paired consulting_direct base + bd_commission_overlay
    sibling with coherent methodology_readiness on both rows must PASS.
    Counterpart to test_cs03_across_rows_overlay_engagement_passes_on_closure;
    this asserts the CS-09 dimension specifically.
    """
    rows = [
        _build_share_registry_row(
            share_id="SHARE-CS09-OK-BASE",
            engagement_id="ENG-CS09-OK",
            share_pattern="consulting_direct",
            share_overlay="",
            holistika_pct=85,
            collaborator_pct=0,
            methodology_readiness="methodology_trained",
            collaborator_id="POI-PRT-A",
        ),
        _build_share_registry_row(
            share_id="SHARE-CS09-OK-OVL",
            engagement_id="ENG-CS09-OK",
            share_pattern="consulting_direct",
            share_overlay="bd_commission_overlay",
            holistika_pct=0,
            collaborator_pct=15,
            methodology_readiness="methodology_trained",
            collaborator_id="POI-PRT-B",
        ),
    ]
    _seed_fixture_dir(tmp_path, share_rows=rows)

    import scripts.validate_collaborator_share as vcs_mod
    importlib.reload(vcs_mod)
    _point_validator_at_fixture(monkeypatch, vcs_mod, tmp_path)

    report = vcs_mod.run_audit(audit_trigger="on_demand", audited_by="pytest")
    cs09_findings = [
        f
        for f in report.findings
        if f.check_code == "CS-09-OVERLAY-BASE-PAIRING-VALIDITY"
    ]
    assert cs09_findings, "CS-09 finding missing entirely"
    assert not any(f.verdict == "fail" for f in cs09_findings), (
        f"unexpected CS-09 FAIL for clean overlay engagement; got: "
        f"{[(f.verdict, (f.drift_summary or '')[:80]) for f in cs09_findings]}"
    )


# ===========================================================================
# CHECK_REGISTRY shape (paired with self-test invariants)
# ===========================================================================

def test_check_registry_exposes_nine_probes():
    """The validator module's CHECK_REGISTRY exposes exactly 9 probes
    (CS-01..CS-09; CS-09 added at Wave R+2 Commit 3 for overlay-base
    pairing + methodology-pattern coherence per D-IH-86-EJ).
    """
    import scripts.validate_collaborator_share as vcs_mod
    importlib.reload(vcs_mod)
    assert hasattr(vcs_mod, "CHECK_REGISTRY"), (
        "CHECK_REGISTRY missing from validate_collaborator_share.py"
    )
    codes = set(vcs_mod.CHECK_REGISTRY.keys())
    assert codes == ALL_NINE_CHECK_CODES, f"CHECK_REGISTRY codes mismatch: {codes}"


# ===========================================================================
# Worked-example runbook smoke (per-pattern CLI + JSON shape)
#
# In-depth runbook arithmetic + multi-row aggregate + advisory-note tests
# live in tests/test_collaborator_share_calculate.py. The smokes below
# verify CLI parity with the validator's view of the 4-base enum + the
# new per_row_breakdowns JSON shape.
# ===========================================================================

def test_runbook_deep_partner_default_split():
    """deep_partner_65_35: 100k revenue, 20k pass-through → benefits 80k,
    split 52k/28k (65/35 anchor)."""
    cp = _run_runbook(
        "--engagement-id", "ENG-PYTEST-DP-2026",
        "--revenue", "100000",
        "--direct-cost", "20000",
        "--share-pattern", "deep_partner_65_35",
    )
    assert cp.returncode == 0, f"stderr={cp.stderr}"
    assert "Benefits" in cp.stdout
    assert "80000.00 EUR" in cp.stdout
    assert "52000.00 EUR" in cp.stdout
    assert "28000.00 EUR" in cp.stdout


def test_runbook_bd_intro_only_default_split():
    """bd_intro_only: 100k revenue, 20k pass-through → benefits 80k,
    split 68k/12k (85/15 anchor)."""
    cp = _run_runbook(
        "--engagement-id", "ENG-PYTEST-BD-2026",
        "--revenue", "100000",
        "--direct-cost", "20000",
        "--share-pattern", "bd_intro_only",
        "--emit-json",
    )
    assert cp.returncode == 0, f"stderr={cp.stderr}"
    payload = json.loads(cp.stdout)
    assert payload["primary_row_share_pattern"] == "bd_intro_only"
    assert payload["benefits"] == 80_000.0
    assert payload["per_row_breakdowns"][0]["holistika_share_amount"] == 68_000.0
    assert payload["per_row_breakdowns"][0]["collaborator_share_amount"] == 12_000.0


def test_runbook_joint_venture_default_split():
    """joint_venture_aventure: 100k revenue, 20k pass-through → 80k
    benefits, 50/50 split = 40k each."""
    cp = _run_runbook(
        "--engagement-id", "ENG-PYTEST-JV-2026",
        "--revenue", "100000",
        "--direct-cost", "20000",
        "--share-pattern", "joint_venture_aventure",
        "--emit-json",
    )
    assert cp.returncode == 0, f"stderr={cp.stderr}"
    payload = json.loads(cp.stdout)
    assert payload["primary_row_share_pattern"] == "joint_venture_aventure"
    assert payload["benefits"] == 80_000.0
    assert payload["per_row_breakdowns"][0]["holistika_share_amount"] == 40_000.0
    assert payload["per_row_breakdowns"][0]["collaborator_share_amount"] == 40_000.0


def test_runbook_consulting_direct_solo_default_split():
    """consulting_direct SOLO (no overlay): 100k revenue, 20k pass-through
    → 80k benefits, 100/0 = 80k Holistika + 0 collaborator."""
    cp = _run_runbook(
        "--engagement-id", "ENG-PYTEST-CD-2026",
        "--revenue", "100000",
        "--direct-cost", "20000",
        "--share-pattern", "consulting_direct",
        "--emit-json",
    )
    assert cp.returncode == 0, f"stderr={cp.stderr}"
    payload = json.loads(cp.stdout)
    assert payload["primary_row_share_pattern"] == "consulting_direct"
    assert payload["benefits"] == 80_000.0
    assert payload["per_row_breakdowns"][0]["holistika_share_amount"] == 80_000.0
    assert payload["per_row_breakdowns"][0]["collaborator_share_amount"] == 0.0
    assert payload["per_row_breakdowns"][0]["holistika_share_pct"] == 100
    assert payload["per_row_breakdowns"][0]["collaborator_share_pct"] == 0


def test_runbook_json_output_carries_wave_r_plus_two_schema_keys():
    """Wave R+2 Commit 3 runbook JSON output schema: top-level
    primary_row_share_pattern + per_row_breakdowns list + across-rows
    aggregate keys + advisory_notes list. (Pre-rewrite top-level
    share_pattern + share_amount keys are gone.)
    """
    cp = _run_runbook(
        "--engagement-id", "ENG-PYTEST-SCHEMA-2026",
        "--revenue", "50000",
        "--direct-cost", "10000",
        "--share-pattern", "deep_partner_65_35",
        "--emit-json",
    )
    assert cp.returncode == 0, f"stderr={cp.stderr}"
    payload = json.loads(cp.stdout)

    for key in (
        "engagement_id",
        "currency",
        "revenue",
        "cost_lines",
        "total_costs",
        "benefits",
        "primary_row_share_pattern",
        "per_row_breakdowns",
        "across_rows_total_holistika_pct",
        "across_rows_total_collaborator_pct",
        "across_rows_split_sums_to_100",
        "across_rows_holistika_amount",
        "across_rows_collaborator_amount",
        "share_row_present",
        "share_row_id",
        "advisory_notes",
        "computed_at",
    ):
        assert key in payload, f"Wave R+2 JSON schema missing top-level key {key!r}"

    # Pre-rewrite top-level keys are GONE per D-IH-86-EJ.
    for removed_key in (
        "share_pattern",  # → primary_row_share_pattern
        "holistika_share_amount",  # → per_row_breakdowns[*]["holistika_share_amount"]
        "collaborator_share_amount",  # → per_row_breakdowns[*]["collaborator_share_amount"]
        "split_default",  # → per_row_breakdowns[*]["split_matches_anchor"]
    ):
        assert removed_key not in payload, (
            f"removed pre-rewrite top-level key {removed_key!r} still present"
        )

    assert isinstance(payload["per_row_breakdowns"], list)
    assert isinstance(payload["advisory_notes"], list)
    assert len(payload["per_row_breakdowns"]) >= 1
    for row in payload["per_row_breakdowns"]:
        for row_key in (
            "share_pattern",
            "share_overlay",
            "holistika_share_pct",
            "collaborator_share_pct",
            "anchor_holistika_pct",
            "anchor_collaborator_pct",
            "split_matches_anchor",
            "holistika_share_amount",
            "collaborator_share_amount",
        ):
            assert row_key in row, (
                f"per-row breakdown missing key {row_key!r}: row={row}"
            )


def test_runbook_share_pattern_choices_includes_all_four_bases():
    """CLI --share-pattern choice list mirrors VALID_SHARE_PATTERNS (4
    base patterns post-Wave R+2 rewrite). Pre-rewrite values
    orchestration_broker_thin_margin + custom are no longer in --help.
    """
    cp = _run_runbook("--help")
    assert cp.returncode == 0
    for pat in (
        "deep_partner_65_35",
        "bd_intro_only",
        "joint_venture_aventure",
        "consulting_direct",
    ):
        assert pat in cp.stdout, f"missing {pat!r} from --share-pattern choices"

    for removed in ("orchestration_broker_thin_margin", "custom"):
        assert removed not in cp.stdout, (
            f"removed pre-rewrite pattern {removed!r} still in --help choices"
        )


def test_runbook_share_overlay_choice_advertised():
    """CLI --share-overlay choice list includes the one valid overlay
    bd_commission_overlay (per VALID_SHARE_OVERLAYS at Wave R+2 Commit 2).
    """
    cp = _run_runbook("--help")
    assert cp.returncode == 0
    assert "bd_commission_overlay" in cp.stdout, (
        "CLI --share-overlay missing bd_commission_overlay choice"
    )
