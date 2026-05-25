"""Integration tests for scripts/validate_synthesis_before_tranche.py + scripts/synthesis_before_tranche_check.py.

The 14th Quality Fabric specialty per ``D-IH-86-EA`` quartet (Wave R+1 P3
Commits 2a/2b; doctrine + Pydantic chassis + validator + runbook + wiring).

This file covers the *validator + runbook CLI behaviour* (subprocess + on-disk
fixtures) AND the in-process helpers (probe dispatch, charter parsing, sweep,
markdown rendering). Pure Pydantic model + enum coverage lives in
``tests/test_hlk_synthesis_before_tranche.py`` (40 tests, all PASS at Commit 2a).

Covers:

- CLI surface for both validator + runbook (--self-test exits 0).
- Validator helper invariants (enum membership, fixture instantiation,
  resolve_fire_set spot-checks, enum cardinality counts).
- Runbook probe dispatch covers exactly ``VALID_DIMENSION_CODES``.
- Runbook ``sweep_tranche()`` returns well-formed findings + summary per
  tranche class (engagement fires all 10; specialty_mint fires 8 with
  conditional triggers).
- Runbook ``_parse_yaml_frontmatter()`` handles the subset shapes used by
  the canonical ``SynthesisTrancheCharter`` schema.
- Runbook ``_charter_from_dict()`` coerces a parsed dict into a Pydantic
  charter without raising.
- Runbook ``render_report_markdown()`` produces a Markdown body conforming
  to the §3 mechanical-evidence shape (frontmatter + summary + per-dim
  table + 5-option disposition workflow).
- Runbook ``--check-charter`` end-to-end (writes a temp charter; the
  runbook parses + sweeps + writes the report when ``--emit-report`` is on).
- Runbook ``--tranche-id`` + ``--tranche-class`` inline CLI mode.
- Probes (audience / channel / scenario / brand / governance / erp_surface
  / atomicity / reversibility / closing_loop / recipient_fallback) each
  return the expected PASS / WARN / FAIL / INFO / N/A under happy + sad
  paths.

These tests are independent of any canonical CSV state (per the 14th
specialty's `--self-test` posture; there is no CSV gate at INFO ramp).
"""
from __future__ import annotations

import importlib
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_synthesis_before_tranche.py"
RUNBOOK_PATH = REPO_ROOT / "scripts" / "synthesis_before_tranche_check.py"

PYTHON = sys.executable


# Lazy imports of the in-process modules — done inside test fns to keep
# import time predictable per pytest collection.

def _import_validator():
    spec = importlib.util.spec_from_file_location(
        "validate_synthesis_before_tranche_mod", VALIDATOR_PATH
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


def _import_runbook():
    spec = importlib.util.spec_from_file_location(
        "synthesis_before_tranche_check_mod", RUNBOOK_PATH
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


def _run(path: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [PYTHON, str(path), *args],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )


# =============================================================================
# Script presence + basic CLI surface
# =============================================================================


def test_validator_script_exists():
    assert VALIDATOR_PATH.is_file(), f"validator missing at {VALIDATOR_PATH}"


def test_runbook_script_exists():
    assert RUNBOOK_PATH.is_file(), f"runbook missing at {RUNBOOK_PATH}"


def test_validator_self_test_exits_zero():
    """--self-test must always exit 0 in a healthy tree (release-gate gate)."""
    cp = _run(VALIDATOR_PATH, "--self-test")
    assert cp.returncode == 0, (
        f"validator --self-test failed:\nstdout={cp.stdout}\nstderr={cp.stderr}"
    )
    assert "PASS" in cp.stdout


def test_runbook_self_test_exits_zero():
    cp = _run(RUNBOOK_PATH, "--self-test")
    assert cp.returncode == 0, (
        f"runbook --self-test failed:\nstdout={cp.stdout}\nstderr={cp.stderr}"
    )
    assert "PASS" in cp.stdout


def test_validator_default_mode_equals_self_test():
    """At INFO ramp (D-IH-86-ED), default mode == --self-test (no FAIL)."""
    cp = _run(VALIDATOR_PATH)
    assert cp.returncode == 0
    assert "PASS" in cp.stdout


def test_runbook_default_mode_equals_self_test():
    """No args and no charter → run self-test rather than parsing nothing."""
    cp = _run(RUNBOOK_PATH)
    assert cp.returncode == 0
    assert "PASS" in cp.stdout


def test_validator_help_mentions_self_test():
    cp = _run(VALIDATOR_PATH, "--help")
    assert cp.returncode == 0
    assert "--self-test" in cp.stdout
    assert "SYNTHESIS_BEFORE_TRANCHE" in cp.stdout


def test_runbook_help_mentions_check_charter():
    cp = _run(RUNBOOK_PATH, "--help")
    assert cp.returncode == 0
    assert "--check-charter" in cp.stdout
    assert "--emit-report" in cp.stdout


# =============================================================================
# Validator in-process helper coverage
# =============================================================================


def test_validator_enum_invariants_pass():
    mod = _import_validator()
    assert mod._verify_enum_invariants() == []


def test_validator_enum_cardinality_pass():
    mod = _import_validator()
    assert mod._verify_enum_membership_counts() == []


def test_validator_pydantic_fixtures_instantiate():
    mod = _import_validator()
    assert mod._verify_pydantic_fixtures() == []


def test_validator_resolve_fire_set_consistent():
    mod = _import_validator()
    assert mod._verify_resolve_fire_set() == []


def test_validator_self_test_returns_zero():
    mod = _import_validator()
    rc = mod.self_test()
    assert rc == 0


# =============================================================================
# Runbook probe dispatch + chassis
# =============================================================================


def test_runbook_probe_dispatch_covers_all_dimensions():
    mod = _import_runbook()
    from akos.hlk_synthesis_before_tranche import VALID_DIMENSION_CODES

    assert set(mod._DIMENSION_PROBE_DISPATCH) == VALID_DIMENSION_CODES


def test_runbook_probe_dispatch_no_orphans():
    mod = _import_runbook()
    from akos.hlk_synthesis_before_tranche import VALID_DIMENSION_CODES

    extra = set(mod._DIMENSION_PROBE_DISPATCH) - VALID_DIMENSION_CODES
    assert extra == set()


def test_runbook_self_test_returns_zero():
    mod = _import_runbook()
    rc = mod.self_test()
    assert rc == 0


# =============================================================================
# sweep_tranche() per tranche class
# =============================================================================


def _build_charter(**overrides):
    from akos.hlk_synthesis_before_tranche import SynthesisTrancheCharter

    defaults = dict(
        tranche_id="test-tranche",
        tranche_class="specialty_mint",
        tranche_title="test tranche title",
        audiences_named=["J-OP"],
        channels_named=[],
        scenarios_named=[],
        brand_register="internal-corpint",
        ratifying_decisions=["D-IH-86-EA"],
        erp_surface_citations=[],
        is_atomic_commit=True,
        reversibility_class="medium",
        reversibility_rationale="reversible via git revert",
        closing_loop_test="self-test PASS",
        recipient_fallback_channel="n/a",
    )
    defaults.update(overrides)
    return SynthesisTrancheCharter(**defaults)


def test_sweep_specialty_mint_complete_passes():
    mod = _import_runbook()
    charter = _build_charter(tranche_class="specialty_mint")
    findings, summary = mod.sweep_tranche(charter)
    assert summary.fail_count == 0
    assert summary.synthesis_complete is True
    # specialty_mint fires 8 dimensions with conditional triggers on
    assert summary.dimensions_fired == 8


def test_sweep_engagement_fires_all_ten():
    mod = _import_runbook()
    charter = _build_charter(
        tranche_class="engagement",
        audiences_named=["J-OP", "J-CU"],
        channels_named=["CHAN-EMAIL-OUTBOUND"],
        scenarios_named=["scenario-SUEZ-PRA"],
        erp_surface_citations=["operator-dashboard"],
        recipient_fallback_channel="CHAN-EMAIL-OUTBOUND",
    )
    findings, summary = mod.sweep_tranche(charter)
    assert summary.dimensions_fired == 10
    assert summary.fail_count == 0


def test_sweep_missing_governance_fails_synthesis():
    mod = _import_runbook()
    charter = _build_charter(
        tranche_class="specialty_mint",
        ratifying_decisions=[],
    )
    findings, summary = mod.sweep_tranche(charter)
    fail_dims = {f.dimension_code for f in findings if f.status == "FAIL"}
    assert "SYN-05-GOVERNANCE-RATIFICATION-LINEAGE" in fail_dims
    assert summary.synthesis_complete is False
    assert summary.fail_count >= 1


def test_sweep_missing_closing_loop_fails_synthesis():
    mod = _import_runbook()
    charter = _build_charter(closing_loop_test="")
    findings, summary = mod.sweep_tranche(charter)
    fail_dims = {f.dimension_code for f in findings if f.status == "FAIL"}
    assert "SYN-09-CLOSING-LOOP-TEST" in fail_dims
    assert summary.synthesis_complete is False


def test_sweep_missing_reversibility_fails_synthesis():
    mod = _import_runbook()
    charter = _build_charter(reversibility_rationale="")
    findings, summary = mod.sweep_tranche(charter)
    fail_dims = {f.dimension_code for f in findings if f.status == "FAIL"}
    assert "SYN-08-REVERSIBILITY-DECLARATION" in fail_dims


def test_sweep_engagement_missing_erp_surface_warns():
    mod = _import_runbook()
    charter = _build_charter(
        tranche_class="engagement",
        erp_surface_citations=[],
        audiences_named=["J-OP", "J-CU"],
        channels_named=["CHAN-EMAIL-OUTBOUND"],
        scenarios_named=["s1"],
        recipient_fallback_channel="CHAN-EMAIL-OUTBOUND",
    )
    findings, summary = mod.sweep_tranche(charter)
    warn_dims = {f.dimension_code for f in findings if f.status == "WARN"}
    assert "SYN-06-ERP-SURFACE-CITATION" in warn_dims


def test_sweep_finding_rows_carry_severity_in_recommendation_text():
    mod = _import_runbook()
    charter = _build_charter()
    findings, _ = mod.sweep_tranche(charter)
    for f in findings:
        assert f.recommendation_text.startswith("severity_class=")


# =============================================================================
# _parse_yaml_frontmatter helper
# =============================================================================


def test_parse_yaml_frontmatter_simple_key_value():
    mod = _import_runbook()
    text = (
        "---\n"
        "tranche_id: T1\n"
        "tranche_class: specialty_mint\n"
        "is_atomic_commit: true\n"
        "---\n"
        "body line\n"
    )
    data = mod._parse_yaml_frontmatter(text)
    assert data["tranche_id"] == "T1"
    assert data["tranche_class"] == "specialty_mint"
    assert data["is_atomic_commit"] is True


def test_parse_yaml_frontmatter_inline_list():
    mod = _import_runbook()
    text = (
        "---\n"
        'audiences_named: ["J-OP", "J-CU"]\n'
        "---\n"
    )
    data = mod._parse_yaml_frontmatter(text)
    assert data["audiences_named"] == ["J-OP", "J-CU"]


def test_parse_yaml_frontmatter_bullet_list():
    mod = _import_runbook()
    text = (
        "---\n"
        "ratifying_decisions:\n"
        "  - D-IH-86-EA\n"
        "  - D-IH-86-EB\n"
        "tranche_class: specialty_mint\n"
        "---\n"
    )
    data = mod._parse_yaml_frontmatter(text)
    assert data["ratifying_decisions"] == ["D-IH-86-EA", "D-IH-86-EB"]
    assert data["tranche_class"] == "specialty_mint"


def test_parse_yaml_frontmatter_no_frontmatter_returns_empty():
    mod = _import_runbook()
    assert mod._parse_yaml_frontmatter("plain body, no frontmatter\n") == {}


def test_parse_yaml_frontmatter_quoted_string():
    mod = _import_runbook()
    text = (
        "---\n"
        'tranche_title: "Wave R+1 P3 Commit 2b"\n'
        "---\n"
    )
    data = mod._parse_yaml_frontmatter(text)
    assert data["tranche_title"] == "Wave R+1 P3 Commit 2b"


# =============================================================================
# _charter_from_dict coercion
# =============================================================================


def test_charter_from_dict_uses_defaults_for_missing_keys():
    mod = _import_runbook()
    charter = mod._charter_from_dict({"tranche_id": "T1", "tranche_class": "specialty_mint"})
    assert charter.tranche_id == "T1"
    assert charter.tranche_class == "specialty_mint"
    assert charter.audiences_named == ["J-OP"]  # default
    assert charter.brand_register == "internal-corpint"  # default
    assert charter.is_atomic_commit is True  # default


def test_charter_from_dict_round_trip_with_lists():
    mod = _import_runbook()
    charter = mod._charter_from_dict(
        {
            "tranche_id": "T2",
            "tranche_class": "engagement",
            "audiences_named": ["J-OP", "J-CU"],
            "ratifying_decisions": ["D-IH-86-EA"],
            "closing_loop_test": "manual check",
        }
    )
    assert charter.audiences_named == ["J-OP", "J-CU"]
    assert charter.ratifying_decisions == ["D-IH-86-EA"]


# =============================================================================
# render_report_markdown
# =============================================================================


def test_render_report_markdown_has_required_sections():
    mod = _import_runbook()
    charter = _build_charter()
    findings, summary = mod.sweep_tranche(charter)
    md = mod.render_report_markdown(charter, findings, summary)
    assert md.startswith("---")
    assert "intellectual_kind: synthesis_before_tranche_report" in md
    assert "## Tranche charter" in md
    assert "## Summary" in md
    assert "## Per-dimension findings" in md
    assert "## Disposition workflow" in md
    assert "scope-complete" in md
    assert "escalate-to-blocker-tracker" in md


def test_render_report_markdown_escapes_pipes_in_findings():
    mod = _import_runbook()
    charter = _build_charter(
        tranche_class="specialty_mint",
        audiences_named=["J-OP|with|pipes"],
    )
    findings, summary = mod.sweep_tranche(charter)
    md = mod.render_report_markdown(charter, findings, summary)
    # Pipes inside finding_text should be escaped so they don't break the
    # markdown table.
    assert "J-OP\\|with\\|pipes" in md


# =============================================================================
# End-to-end CLI: --check-charter + --emit-report
# =============================================================================


def _write_charter_file(tmp_path: Path) -> Path:
    """Write a minimal valid charter markdown to tmp_path/charter.md."""
    body = (
        "---\n"
        "tranche_id: test-e2e-tranche\n"
        "tranche_class: specialty_mint\n"
        'tranche_title: "test e2e tranche"\n'
        'audiences_named: ["J-OP"]\n'
        "ratifying_decisions:\n"
        "  - D-IH-86-EA\n"
        "  - D-IH-86-EB\n"
        "brand_register: internal-corpint\n"
        "is_atomic_commit: true\n"
        "reversibility_class: medium\n"
        'reversibility_rationale: "revert via git revert"\n'
        'closing_loop_test: "self-test PASS"\n'
        "recipient_fallback_channel: n/a\n"
        "---\n"
        "Body of the charter\n"
    )
    p = tmp_path / "charter.md"
    p.write_text(body, encoding="utf-8")
    return p


def test_runbook_check_charter_end_to_end(tmp_path: Path):
    charter_path = _write_charter_file(tmp_path)
    reports_dir = tmp_path / "reports"
    cp = _run(
        RUNBOOK_PATH,
        "--check-charter",
        str(charter_path),
        "--emit-report",
        "--reports-dir",
        str(reports_dir),
    )
    assert cp.returncode == 0, (
        f"--check-charter failed:\nstdout={cp.stdout}\nstderr={cp.stderr}"
    )
    assert "Synthesis report written" in cp.stdout
    # Exactly one report should be written
    written = list(reports_dir.glob("synthesis-check-*.md"))
    assert len(written) == 1, (
        f"expected 1 report under {reports_dir}, got {len(written)}"
    )
    md = written[0].read_text(encoding="utf-8")
    assert "test-e2e-tranche" in md
    assert "specialty_mint" in md


def test_runbook_check_charter_missing_file_fails():
    cp = _run(
        RUNBOOK_PATH,
        "--check-charter",
        "/nonexistent/charter.md",
    )
    assert cp.returncode == 4
    assert "FAIL" in cp.stdout


def test_runbook_check_charter_no_frontmatter_fails(tmp_path: Path):
    p = tmp_path / "no-frontmatter.md"
    p.write_text("plain body\n", encoding="utf-8")
    cp = _run(RUNBOOK_PATH, "--check-charter", str(p))
    assert cp.returncode == 5
    assert "FAIL" in cp.stdout


def test_runbook_inline_cli_mode_missing_class_fails():
    cp = _run(
        RUNBOOK_PATH,
        "--tranche-id",
        "inline-test",
    )
    # tranche_id present but tranche_class missing
    assert cp.returncode == 6
    assert "tranche-class" in cp.stdout


def test_runbook_inline_cli_mode_minimal_passes():
    cp = _run(
        RUNBOOK_PATH,
        "--tranche-id",
        "inline-test",
        "--tranche-class",
        "specialty_mint",
        "--ratifying-decisions",
        "D-IH-86-EA",
        "--closing-loop-test",
        "verified",
    )
    assert cp.returncode == 0, (
        f"inline CLI mode failed:\nstdout={cp.stdout}\nstderr={cp.stderr}"
    )
    assert "inline-test" in cp.stdout
    assert "specialty_mint" in cp.stdout


# =============================================================================
# Individual probe behaviour (happy + sad path)
# =============================================================================


def test_probe_audience_pass_with_named():
    mod = _import_runbook()
    charter = _build_charter(audiences_named=["J-OP", "J-CU"])
    status, _, disp = mod._probe_audience(charter)
    assert status == "PASS"
    assert disp == "scope-complete"


def test_probe_audience_fail_when_empty():
    mod = _import_runbook()
    charter = _build_charter(audiences_named=[])
    status, _, disp = mod._probe_audience(charter)
    assert status == "FAIL"
    assert disp == "scope-extend"


def test_probe_channel_info_when_empty():
    mod = _import_runbook()
    charter = _build_charter(channels_named=[])
    status, _, _ = mod._probe_channel(charter)
    assert status == "INFO"


def test_probe_scenario_info_when_empty():
    mod = _import_runbook()
    charter = _build_charter(scenarios_named=[])
    status, _, _ = mod._probe_scenario(charter)
    assert status == "INFO"


def test_probe_brand_register_pass_when_set():
    mod = _import_runbook()
    charter = _build_charter(brand_register="internal-corpint")
    status, _, _ = mod._probe_brand_register(charter)
    assert status == "PASS"


def test_probe_governance_fail_when_empty():
    mod = _import_runbook()
    charter = _build_charter(ratifying_decisions=[])
    status, _, _ = mod._probe_governance(charter)
    assert status == "FAIL"


def test_probe_erp_surface_warn_for_engagement_when_empty():
    mod = _import_runbook()
    charter = _build_charter(tranche_class="engagement", erp_surface_citations=[])
    status, _, _ = mod._probe_erp_surface(charter)
    assert status == "WARN"


def test_probe_erp_surface_na_for_specialty_mint_when_empty():
    mod = _import_runbook()
    charter = _build_charter(tranche_class="specialty_mint", erp_surface_citations=[])
    status, _, _ = mod._probe_erp_surface(charter)
    assert status == "N/A"


def test_probe_atomicity_warn_when_false():
    mod = _import_runbook()
    charter = _build_charter(is_atomic_commit=False)
    status, _, _ = mod._probe_atomicity(charter)
    assert status == "WARN"


def test_probe_reversibility_fail_when_rationale_missing():
    mod = _import_runbook()
    charter = _build_charter(reversibility_rationale="")
    status, _, _ = mod._probe_reversibility(charter)
    assert status == "FAIL"


def test_probe_closing_loop_fail_when_empty():
    mod = _import_runbook()
    charter = _build_charter(closing_loop_test="")
    status, _, _ = mod._probe_closing_loop(charter)
    assert status == "FAIL"


def test_probe_recipient_fallback_na_for_specialty_mint_with_value():
    """Even when value present, runbook treats it as PASS (string truthy)."""
    mod = _import_runbook()
    charter = _build_charter(recipient_fallback_channel="n/a (governance)")
    status, _, _ = mod._probe_recipient_fallback(charter)
    assert status == "PASS"


# =============================================================================
# Sanity: validator + runbook share the same enum chassis
# =============================================================================


def test_validator_and_runbook_share_same_dimension_codes():
    val_mod = _import_validator()
    run_mod = _import_runbook()
    assert val_mod.VALID_DIMENSION_CODES == run_mod.VALID_DIMENSION_CODES


def test_dimension_severity_class_covers_all_dimensions():
    val_mod = _import_validator()
    assert (
        set(val_mod.DIMENSION_SEVERITY_CLASS) == val_mod.VALID_DIMENSION_CODES
    )
