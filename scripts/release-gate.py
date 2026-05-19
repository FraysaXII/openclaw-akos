#!/usr/bin/env python3
"""AKOS release gate -- runs the governed checks before a release.

Executes strict inventory, full tests, drift check, browser smoke, and
API smoke, then reports an overall PASS or FAIL verdict. Optionally
notes when live smoke tests should be run (when AKOS_LIVE_SMOKE=1 is set).

Usage:
    py scripts/release-gate.py
    py scripts/release-gate.py --json-log
"""

from __future__ import annotations

import argparse
import datetime as _dt
import logging
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import akos.process as proc
from akos.io import REPO_ROOT
from akos.log import setup_logging
from akos.verification_profiles import governance_rubric_suites

logger = logging.getLogger("akos.release")

SCRIPTS_DIR = REPO_ROOT / "scripts"


def _today_iso() -> str:
    """Return today's date as YYYY-MM-DD.

    Used by dated default-flip helpers (e.g. D-IH-77-E IMPECCABLE bridge drift
    strict-default at 2026-06-15). Allows ``AKOS_RELEASE_GATE_TODAY=YYYY-MM-DD``
    override for testing date-aware promotions deterministically.
    """
    override = os.environ.get("AKOS_RELEASE_GATE_TODAY")
    if override:
        return override
    return _dt.date.today().isoformat()


def run_tests() -> bool:
    """Run the full test suite via scripts/test.py all."""
    logger.info("Running full test suite ...")
    result = proc.run(
        [sys.executable, str(SCRIPTS_DIR / "test.py"), "all"],
        timeout=300,
        capture=False,
    )
    return result.success


def run_inventory_check() -> bool:
    """Run the strict inventory verifier."""
    logger.info("Running strict inventory verifier ...")
    result = proc.run(
        [sys.executable, str(SCRIPTS_DIR / "legacy" / "verify_openclaw_inventory.py")],
        timeout=60,
        capture=False,
    )
    return result.success


def run_drift_check() -> bool:
    """Run the drift detection script."""
    logger.info("Running drift check ...")
    result = proc.run(
        [sys.executable, str(SCRIPTS_DIR / "check-drift.py")],
        timeout=60,
        capture=False,
    )
    return result.success


def run_browser_smoke() -> bool:
    """Run browser smoke tests. Uses Playwright when AKOS_BROWSER_SMOKE=1 or when playwright is installed."""
    logger.info("Running browser smoke ...")
    args = [sys.executable, str(SCRIPTS_DIR / "browser-smoke.py")]
    try:
        import playwright
        args.append("--playwright")
    except ImportError:
        pass
    result = proc.run(args, timeout=120, capture=False)
    if result.returncode == 2:
        # browser-smoke: Playwright workers produced no parseable JSON (hosts without browsers).
        logger.warning("browser-smoke exit 2 (workers unavailable); treating as non-blocking for release gate")
        return True
    return result.success


def run_api_smoke() -> bool:
    """Run FastAPI control plane smoke tests."""
    logger.info("Running API smoke tests ...")
    result = proc.run(
        [sys.executable, "-m", "pytest", str(REPO_ROOT / "tests" / "test_api.py"), "-v"],
        timeout=120,
        capture=False,
    )
    return result.success


def run_hlk_validation() -> bool:
    """Run HLK canonical vault validation."""
    logger.info("Running HLK vault validation ...")
    result = proc.run(
        [sys.executable, str(SCRIPTS_DIR / "validate_hlk.py")],
        timeout=60,
        capture=False,
    )
    return result.success


def run_process_list_header_check() -> bool:
    """Ensure process_list.csv header matches PROCESS_LIST_FIELDNAMES (fork drift)."""
    logger.info("Running process_list.csv header check ...")
    result = proc.run(
        [sys.executable, str(SCRIPTS_DIR / "check_process_list_header.py")],
        timeout=30,
        capture=False,
    )
    return result.success


def run_compliance_schema_drift_check() -> bool:
    """Verify every canonical compliance CSV header matches its akos.* SSOT tuple.

    Generalization of run_process_list_header_check() to the full canonical CSV
    set (22 CSVs). Authored in the 2026-05-11 release-gate hygiene pass as the
    structural prevention layer that catches the class of bug that caused the
    BASELINE_FIELDNAMES drift: a canonical CSV mutated (column appended) but a
    downstream consumer (sync script tuple / mirror DDL) was not updated in
    lockstep. Per akos-governance-remediation.mdc Design-for-Invariance.
    """
    logger.info("Running compliance schema drift check ...")
    result = proc.run(
        [sys.executable, str(SCRIPTS_DIR / "validate_compliance_schema_drift.py")],
        timeout=30,
        capture=False,
    )
    return result.success


def run_hlk_vault_links_validation() -> bool:
    """Validate internal markdown links under docs/references/hlk/v3.0/."""
    logger.info("Running HLK vault link validation ...")
    result = proc.run(
        [sys.executable, str(SCRIPTS_DIR / "validate_hlk_vault_links.py")],
        timeout=120,
        capture=False,
    )
    return result.success


def run_subdomains_registry_validation() -> bool:
    """Validate canonical SUBDOMAINS_REGISTRY.md (I62 P0 / D-IH-62-P)."""
    logger.info("Running SUBDOMAINS_REGISTRY.md validation ...")
    result = proc.run(
        [sys.executable, str(SCRIPTS_DIR / "validate_subdomains_registry.py")],
        timeout=30,
        capture=False,
    )
    return result.success


def run_playwright_baseline_validation() -> bool:
    """Validate Playwright canonical template + (opt-in) consumer-repo configs (I68 P2 / D-IH-68-B).

    Default mode: only validates the AKOS canonical template at
    ``docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/_templates/playwright.config.ts.tmpl``.
    Set ``AKOS_PLAYWRIGHT_BASELINE_SCAN_CONSUMERS=1`` to additionally scan
    sibling consumer-repo ``playwright.config.ts`` files for drift; this
    becomes default-strict in I68 P5 once sibling-repo carry-overs land.
    """
    logger.info("Running Playwright baseline validation ...")
    result = proc.run(
        [sys.executable, str(SCRIPTS_DIR / "validate_playwright_baseline.py")],
        timeout=30,
        capture=False,
    )
    return result.success


def run_sentry_release_format_validation() -> bool:
    """Validate Sentry release-format canonical doc + (opt-in) consumer scan (I68 P4 / D-IH-68-I).

    Default mode: validates only the canonical doc at
    ``docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/Repositories/SENTRY_DASHBOARD_HOLISTIKA.md``
    (presence + carries canonical ``{repo_slug}@{sha_short}`` example).
    Set ``AKOS_SENTRY_RELEASE_SCAN_CONSUMERS=1`` to additionally scan
    sibling consumer-repo ``sentry.*.config.ts`` / Python ``sentry_sdk.init(...)``
    sites for the ``release:`` field; becomes default-strict in I68 P5 once
    sibling-repo carry-overs land.
    """
    logger.info("Running Sentry release-format validation ...")
    result = proc.run(
        [sys.executable, str(SCRIPTS_DIR / "validate_sentry_release_format.py")],
        timeout=60,
        capture=False,
    )
    return result.success


def run_cicd_baseline_validation() -> bool:
    """Validate CICD baseline canonical SOP + workflow templates + (opt-in) consumer scan (I68 P5 / D-IH-68-D).

    Default mode: validates only the canonical SOP at
    ``docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/SOP-CICD_BASELINE_001.md``
    + the canonical workflow template + Render YAML stub. Set
    ``AKOS_CICD_BASELINE_SCAN_CONSUMERS=1`` to additionally scan each
    ``REPOSITORY_REGISTRY.csv`` row for valid ``ci_baseline_version`` /
    ``build_time_target_seconds`` / ``ci_baseline_optouts`` columns; becomes
    default-strict in I68 P8 closure once the canonical CSV gate ships those columns.
    """
    logger.info("Running CICD baseline validation ...")
    result = proc.run(
        [sys.executable, str(SCRIPTS_DIR / "validate_cicd_baseline.py")],
        timeout=30,
        capture=False,
    )
    return result.success


def run_brand_canon_drift_validation() -> bool:
    """Validate brand-canon self-consistency (I66 P2 / D-IH-66-J).

    Hard-fails on drift (missing canonical, internal token in external column,
    missing cross-refs, supersedes drift). The upstream boilerplate visual
    check is informational-only inside the validator.
    """
    logger.info("Running BRAND canon drift validation ...")
    result = proc.run(
        [sys.executable, str(SCRIPTS_DIR / "validate_brand_canon_drift.py")],
        timeout=30,
        capture=False,
    )
    return result.success


def run_brand_jargon_validation() -> tuple[bool, int]:
    """Run brand-jargon validation against external public surfaces (I66 P2).

    Returns ``(ok, exit_code)``. Wired as **strict-FAIL by default** since
    Initiative 66 P5 increment 3 (2026-05-09) — boilerplate is jargon-clean
    (0 hits across 134 scanned files). Soft-INFO mode is now the opt-out via
    ``AKOS_BRAND_JARGON_SOFT=1`` (used during a known-broken state, e.g. a
    refactor of forbidden-token list that temporarily produces signal).
    """
    logger.info("Running BRAND jargon validation ...")
    result = proc.run(
        [sys.executable, str(SCRIPTS_DIR / "validate_brand_jargon.py")],
        timeout=60,
        capture=False,
    )
    rc = result.returncode if hasattr(result, "returncode") else (0 if result.success else 1)
    return (result.success, rc)


def run_render_ownership_validation() -> tuple[bool, int]:
    """Run render-pipeline ownership coverage validation (I71 P5 Pack A4).

    Returns ``(ok, exit_code)``. Wired as **advisory** row (WARNING level by
    default per the §16 discipline -- render-ownership coverage is forward-
    tracked; transition hints don't block CI). Promote to PASS/FAIL by
    setting ``AKOS_RENDER_OWNERSHIP_STRICT=1`` (per-rule severity overrides
    available via ``canonicals/_validators/render-ownership-pack.yml``).

    Closes the I71 validator-pack quartet (A1 voice register + A2 Gantt
    confidence + A3 multilingual + A4 render ownership) per D-IH-71-S.
    """
    logger.info("Running RENDER OWNERSHIP coverage validation (I71 P5 Pack A4) ...")
    result = proc.run(
        [sys.executable, str(SCRIPTS_DIR / "validate_render_ownership.py")],
        timeout=60,
        capture=False,
    )
    rc = result.returncode if hasattr(result, "returncode") else (0 if result.success else 1)
    return (result.success, rc)


def run_audience_tags_validation() -> tuple[bool, int]:
    """Run audience-tag FK + J-OP exclusion validation (I85 P2 / D-IH-85-A/B/D).

    Returns ``(ok, exit_code)``. Wired as **INFO** row (advisory only; never
    blocks the release gate) per I85 master-roadmap — promotes to PASS/FAIL
    at I85 P4 closure after the operator-gated sweep completes.
    """
    logger.info("Running AUDIENCE TAG drift validation (I85 P2) ...")
    result = proc.run(
        [sys.executable, str(SCRIPTS_DIR / "validate_audience_tags.py")],
        timeout=30,
        capture=False,
    )
    rc = result.returncode if hasattr(result, "returncode") else (0 if result.success else 1)
    return (result.success, rc)


def run_external_render_trail_validation() -> tuple[bool, int]:
    """Run external-render trail drift gate (I86 Wave E / D-IH-86-P).

    Exit code 0 PASS, 1 FAIL. INFO-mode by default; promotes to FAIL via
    --strict flag or AKOS_RENDER_TRAIL_STRICT=1 env, once the
    external-render-pending-tracker.md reaches zero entries and operator
    ratifies the closure decision row.
    """
    logger.info("Running EXTERNAL-RENDER trail validation (I86 Wave E / D-IH-86-P) ...")
    result = proc.run(
        [sys.executable, str(SCRIPTS_DIR / "validate_external_render_trail.py")],
        timeout=30,
        capture=False,
    )
    rc = result.returncode if hasattr(result, "returncode") else (0 if result.success else 1)
    return (result.success, rc)


def run_initiative_program_anchors_validation() -> tuple[bool, int]:
    """Run INITIATIVE_REGISTRY -> PROGRAM_REGISTRY anchor validation (I86 P1 / D-IH-86-H).

    Returns ``(ok, exit_code)``. Stage A advisory mode (never blocks release
    gate) until I86 P2 promotes anchors from the ``notes`` prefix to a
    first-class ``program_anchors`` semicolon-list column with FK resolution
    in ``validate_initiative_registry.py`` (D-IH-86-J).
    """
    logger.info("Running INITIATIVE program-anchors validation (I86 P1) ...")
    result = proc.run(
        [sys.executable, str(SCRIPTS_DIR / "validate_initiative_program_anchors.py")],
        timeout=30,
        capture=False,
    )
    rc = result.returncode if hasattr(result, "returncode") else (0 if result.success else 1)
    return (result.success, rc)


def run_openclaw_plugin_pinning_validation() -> tuple[bool, int]:
    """Run OpenClaw plugin pinning validation (I87 P2 / D-IH-87-B).

    Returns ``(ok, exit_code)``. Wired as **INFO** row (advisory only; never
    blocks the release gate) per D-IH-87-B — the canonical
    config/openclaw.json.example carries the recommended allow-list;
    per-operator overrides are expected and not a release blocker.
    """
    logger.info("Running OPENCLAW plugin pinning validation (I87 P2) ...")
    result = proc.run(
        [sys.executable, str(SCRIPTS_DIR / "validate_openclaw_plugin_pinning.py")],
        timeout=30,
        capture=False,
    )
    rc = result.returncode if hasattr(result, "returncode") else (0 if result.success else 1)
    return (result.success, rc)


def run_observability_mcps_check() -> tuple[bool, int]:
    """Check user-sentry + user-langfuse MCP reachability (I71 P5 Strand B).

    Returns ``(ok, exit_code)``. Wired as **INFO** row (advisory only; never
    blocks the release gate). Populates the WORKSPACE_BLUEPRINT §18 Strand B
    observability routing rows with deterministic reachability data per
    C-71-5 every-gate-its-own-row default applied at P5 inline-ratify (see
    D-IH-71-T).

    Filesystem-only Option C implementation -- no live MCP probe, no secret
    values logged. SOC posture per ``.cursor/rules/akos-holistika-operations.mdc``.
    """
    logger.info("Running OBSERVABILITY MCP smoke (I71 P5 Strand B) ...")
    result = proc.run(
        [sys.executable, str(SCRIPTS_DIR / "check_observability_mcps.py")],
        timeout=30,
        capture=False,
    )
    rc = result.returncode if hasattr(result, "returncode") else (0 if result.success else 1)
    return (result.success, rc)


def run_review_stamp_validation() -> tuple[bool, int]:
    """Run review-stamp freshness validation (I71 P4 Strand C2).

    Returns ``(ok, exit_code)``. Wired as **INFO** (advisory only; never blocks the
    release gate). Walks the four mirrored canonical CSVs that gained the 4
    review-stamp columns at I71 P4 (`process_list.csv`, `DECISION_REGISTER.csv`,
    `INITIATIVE_REGISTRY.csv`, `OPS_REGISTER.csv`) and emits stale-row (warning),
    missing-stamp (info), and invalid-decision-ref (error) advisories. Stale +
    missing rows surface to the sidecar inbox at
    ``docs/wip/planning/REVIEW_STAMP_INBOX.md`` for incremental operator backfill.

    Exit 0 = no errors (warnings + info still possible); release-gate row stays
    INFO regardless of validator exit code per the kickoff "advisory row in
    release-gate, never blocks" contract for the freshness signal.
    """
    logger.info("Running review-stamp freshness validation (I71 P4) ...")
    result = proc.run(
        [sys.executable, str(SCRIPTS_DIR / "validate_review_stamps.py"), "--no-inbox"],
        timeout=60,
        capture=False,
    )
    rc = result.returncode if hasattr(result, "returncode") else (0 if result.success else 1)
    return (result.success, rc)


def run_brand_voice_register_validation() -> tuple[bool, int]:
    """Run per-locale voice-register validation (I66 P2).

    Returns ``(ok, exit_code)``. Wired as **strict-FAIL by default** since
    Initiative 66 P5 increment 3 (2026-05-09) — boilerplate i18n rewrite
    (`framework`→`marco metodológico` ES + KiRBe descriptions cleaned EN/ES/FR)
    closes the previous register hits. Soft-INFO mode is now the opt-out via
    ``AKOS_BRAND_VOICE_REGISTER_SOFT=1``.
    """
    logger.info("Running BRAND voice-register validation ...")
    result = proc.run(
        [sys.executable, str(SCRIPTS_DIR / "validate_brand_voice_register.py")],
        timeout=30,
        capture=False,
    )
    rc = result.returncode if hasattr(result, "returncode") else (0 if result.success else 1)
    return (result.success, rc)


def run_brand_voice_vale() -> tuple[str, str]:
    """Run the Tier 1 Vale sibling (I71 P2 / D-IH-71-O).

    Returns ``(level, description)`` directly so callers can append the row
    without an additional PASS/FAIL ladder. Two host-conditional branches:

    - **Vale binary absent**: append ``SKIP`` with a note that surfaces the
      missing binary to the operator (Vale ships as a precompiled Go binary;
      install via the operator-host package manager). The generator + style
      files still land at commit time; CI integration becomes live once the
      operator installs Vale.
    - **Vale binary present**: invoke
      ``vale --config=.vale.ini docs/references/hlk/v3.0/`` and report
      PASS / FAIL based on exit code. Because ``MinAlertLevel = warning``
      per C-71-Vale-1 default, any warning-level hit causes a FAIL row; the
      operator can promote / demote the level by editing ``.vale.ini``.

    Scope rationale: Vale runs against the **active vault only**
    (``docs/references/hlk/v3.0/``) per ``PRECEDENCE.md`` reference-only /
    canonical boundary. The ``Research & Logic/`` (v2.7) subtree is
    reference-only and not governed by v3.0 brand canonicals — see
    ``SOP-RELEASE_TAXONOMY_001 §5`` (cross-lane interaction). Scoping the
    invocation prevents Vale from tripping over malformed YAML frontmatter
    in historical reference docs that are intentionally out of governance.

    Sibling row to ``run_brand_voice_register_validation()`` -- both surfaces
    run alongside one another (regex chassis names violations cheaply; Vale
    catches grammar patterns the regex cannot express). Per D-IH-71-J the row
    is placed adjacent to the regex row in the release-gate output for
    operator scannability.
    """
    logger.info("Running BRAND voice Vale sibling (Tier 1 deterministic-NLP layer) ...")
    if shutil.which("vale") is None:
        return (
            "SKIP",
            "BRAND voice Vale sibling (deterministic-NLP layer; vale binary not installed on host; "
            "I71 P2 / C-71-Vale-1 / D-IH-71-O; install Vale -> auto-flips to PASS/FAIL)",
        )
    config_path = REPO_ROOT / ".vale.ini"
    if not config_path.exists():
        return (
            "SKIP",
            "BRAND voice Vale sibling (.vale.ini absent at repo root; regenerate via "
            "scripts/generate_vale_styles.py + author .vale.ini per I71 P2 §P2 Step 2d)",
        )
    # Scope Vale to docs/references/hlk/v3.0/ (active vault) per PRECEDENCE.md
    # reference-only / canonical boundary; the v2.7 Research & Logic subtree is
    # reference-only and not governed by v3.0 brand canonicals (see I71 P3
    # SOP-RELEASE_TAXONOMY_001 §5 cross-lane interaction).
    vale_scan_target = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0"
    result = proc.run(
        ["vale", f"--config={config_path}", str(vale_scan_target)],
        timeout=120,
        capture=False,
    )
    rc = result.returncode if hasattr(result, "returncode") else (0 if result.success else 1)
    if rc == 0:
        return (
            "PASS",
            "BRAND voice Vale sibling (deterministic-NLP layer; 0 hits at warning level; "
            "I71 P2 / C-71-Vale-1 default warning / D-IH-71-O)",
        )
    return (
        "FAIL",
        f"BRAND voice Vale sibling (deterministic-NLP layer; vale exit={rc}; "
        "I71 P2 / C-71-Vale-1 default warning / D-IH-71-O)",
    )


def run_brand_baseline_reality_validation() -> tuple[bool, int]:
    """Run dual-register contract validation (I66 P2 / D-IH-66-M).

    Returns ``(ok, exit_code)``. Wired as **INFO** until I66 P5+P6 close
    (decks land with proper companion structure). Flips to FAIL when
    ``AKOS_BRAND_BASELINE_REALITY_STRICT=1``.
    """
    logger.info("Running BRAND baseline-reality dual-register validation ...")
    result = proc.run(
        [sys.executable, str(SCRIPTS_DIR / "validate_brand_baseline_reality_drift.py")],
        timeout=30,
        capture=False,
    )
    rc = result.returncode if hasattr(result, "returncode") else (0 if result.success else 1)
    return (result.success, rc)


def run_brand_vision_drift_validation() -> bool:
    """Run public vision drift validation (I66 P7)."""
    logger.info("Running BRAND vision drift validation ...")
    result = proc.run(
        [sys.executable, str(SCRIPTS_DIR / "validate_brand_vision_drift.py")],
        timeout=30,
        capture=False,
    )
    return result.success


def run_impeccable_bridge_drift_validation() -> tuple[bool, int]:
    """Run Impeccable bridge drift gate (I77 P2 / D-IH-77-C).

    Returns ``(ok, exit_code)``. Wired as **INFO** until I77 P3 closure
    (per master-roadmap §"Drift gate" soft-30d-then-strict default).
    Flips to **PASS / FAIL** when ``AKOS_IMPECCABLE_BRIDGE_DRIFT_STRICT=1``.
    """
    logger.info("Running IMPECCABLE bridge drift validation ...")
    result = proc.run(
        [sys.executable, str(SCRIPTS_DIR / "validate_impeccable_bridge_drift.py")],
        timeout=30,
        capture=False,
    )
    rc = result.returncode if hasattr(result, "returncode") else (0 if result.success else 1)
    return (result.success, rc)


def run_dossier_companion_drift_validation() -> bool:
    """Run deck/dossier companion validation (I66 P7)."""
    logger.info("Running dossier companion drift validation ...")
    result = proc.run(
        [sys.executable, str(SCRIPTS_DIR / "validate_dossier_companion_drift.py")],
        timeout=30,
        capture=False,
    )
    return result.success


def run_external_repo_contract_check() -> bool:
    """Check governance posture of every non-reference Holistika-tracked repo.

    Reads ``REPOSITORY_REGISTRY.csv`` + the latest ``REPO_HEALTH_SNAPSHOT.csv``
    and validates: contract presence, mirror-rule presence, contract freshness
    (default 90 days), and sha256 alignment between consumer mirror copy and
    AKOS template. Failures here block the release per the bless pattern.
    """
    logger.info("Running external repo contract check ...")
    freshness = os.environ.get("AKOS_EXTERNAL_REPO_FRESHNESS_DAYS", "90")
    result = proc.run(
        [sys.executable, str(SCRIPTS_DIR / "check_external_repo_contract.py"),
         "--freshness-days", freshness],
        timeout=30,
        capture=False,
    )
    return result.success


def run_unblessed_registry_rows_detection() -> bool:
    """Soft / informational: surface un-blessed external repo rows.

    Never fails the gate by default — operators see a NEEDS_BLESS line and can
    run ``scripts/bless_external_repo.py --repo-slug <slug>``.
    Set ``AKOS_UNBLESSED_STRICT=1`` to flip to a hard FAIL (used in nightly
    automation).
    """
    logger.info("Running un-blessed registry row detection ...")
    cmd = [sys.executable, str(SCRIPTS_DIR / "detect_unblessed_registry_rows.py")]
    if os.environ.get("AKOS_UNBLESSED_STRICT") == "1":
        cmd.append("--strict")
    result = proc.run(cmd, timeout=30, capture=False)
    return result.success


def run_external_repo_ci_posture_check() -> bool:
    """Check CI/CD + observability posture of blessed external repos.

    Filesystem-only by default in release-gate (live checks slow runs and
    require ``gh`` / ``vercel`` auth). Set ``AKOS_EXTERNAL_REPO_CI_LIVE=1``
    to enable live checks against GitHub / Vercel / Sentry.
    """
    logger.info("Running external repo CI/CD posture check ...")
    live = os.environ.get("AKOS_EXTERNAL_REPO_CI_LIVE") == "1"
    cmd = [sys.executable, str(SCRIPTS_DIR / "check_external_repo_ci_posture.py")]
    if not live:
        cmd.append("--skip-live")
    result = proc.run(cmd, timeout=120, capture=False)
    return result.success


def run_operator_inbox_check() -> tuple[bool, int]:
    """Determinism check on docs/wip/planning/OPERATOR_INBOX.md (I59 P4).

    Soft / informational: returns ``(stale, exit_code)`` where ``stale`` is
    True only when the on-disk file would change on a fresh render. The
    release-gate caller emits an INFO row but never fails the verdict on this.
    """
    logger.info("Running operator inbox determinism check ...")
    result = proc.run(
        [sys.executable, str(SCRIPTS_DIR / "render_operator_inbox.py"), "--check-only"],
        timeout=30,
        capture=False,
    )
    return (not result.success, result.returncode if hasattr(result, "returncode") else (0 if result.success else 1))


def run_eval_rubric_slice() -> bool:
    """Offline rubric eval slice (set AKOS_EVAL_RUBRIC=1 to enable in release gate)."""
    for suite in governance_rubric_suites():
        logger.info("Running eval rubric slice (%s) ...", suite)
        result = proc.run(
            [
                sys.executable,
                str(SCRIPTS_DIR / "run-evals.py"),
                "run",
                "--suite",
                suite,
                "--mode",
                "rubric",
            ],
            timeout=120,
            capture=False,
        )
        if not result.success:
            return False
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="AKOS release gate")
    parser.add_argument("--json-log", action="store_true", help="JSON logging output")
    args = parser.parse_args()

    setup_logging(json_output=args.json_log)

    results: list[tuple[str, str]] = []

    inventory_ok = run_inventory_check()
    results.append(("PASS" if inventory_ok else "FAIL", "Strict inventory (legacy/verify_openclaw_inventory.py)"))

    test_ok = run_tests()
    results.append(("PASS" if test_ok else "FAIL", "Test suite (scripts/test.py all)"))

    drift_ok = run_drift_check()
    results.append(("PASS" if drift_ok else "FAIL", "Drift check (scripts/check-drift.py)"))

    browser_ok = run_browser_smoke()
    results.append(("PASS" if browser_ok else "FAIL", "Browser smoke (scripts/browser-smoke.py)"))

    api_ok = run_api_smoke()
    results.append(("PASS" if api_ok else "FAIL", "API smoke (pytest tests/test_api.py -v)"))

    hlk_ok = run_hlk_validation()
    results.append(("PASS" if hlk_ok else "FAIL", "HLK vault validation (scripts/validate_hlk.py)"))

    header_ok = run_process_list_header_check()
    results.append(("PASS" if header_ok else "FAIL", "process_list.csv header (scripts/check_process_list_header.py)"))

    schema_drift_ok = run_compliance_schema_drift_check()
    results.append((
        "PASS" if schema_drift_ok else "FAIL",
        "Compliance schema drift (scripts/validate_compliance_schema_drift.py — 22 canonical CSVs vs akos.* SSOT tuples; release-gate hygiene 2026-05-11)",
    ))

    vault_links_ok = run_hlk_vault_links_validation()
    results.append(("PASS" if vault_links_ok else "FAIL", "HLK vault links (scripts/validate_hlk_vault_links.py)"))

    revops_spine_proc = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "validate_revops_spine.py")],
        cwd=str(REPO_ROOT),
        check=False,
    )
    results.append((
        "PASS" if revops_spine_proc.returncode == 0 else "FAIL",
        "RevOps Spine integrity (scripts/validate_revops_spine.py, I72 P7 D-IH-72-M)",
    ))

    adapter_registries_proc = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "validate_adapter_registries.py")],
        cwd=str(REPO_ROOT),
        check=False,
    )
    results.append((
        "PASS" if adapter_registries_proc.returncode == 0 else "FAIL",
        "Adapter registries (scripts/validate_adapter_registries.py, I72 P9 D-IH-72-O + D-IH-72-T + D-IH-72-W)",
    ))

    process_list_pairing_proc = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "validate_process_list_pairing.py")],
        cwd=str(REPO_ROOT),
        check=False,
    )
    results.append((
        "PASS" if process_list_pairing_proc.returncode == 0 else "FAIL",
        "Process_list pairing (scripts/validate_process_list_pairing.py, I72 P9 D-IH-72-U)",
    ))

    rendering_registry_proc = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "validate_rendering_pipeline_registry.py")],
        cwd=str(REPO_ROOT),
        check=False,
    )
    results.append((
        "PASS" if rendering_registry_proc.returncode == 0 else "FAIL",
        "Rendering pipeline registry (scripts/validate_rendering_pipeline_registry.py, I77 P4.C D-IH-77-I)",
    ))

    subdomains_ok = run_subdomains_registry_validation()
    results.append(("PASS" if subdomains_ok else "FAIL", "SUBDOMAINS_REGISTRY.md (scripts/validate_subdomains_registry.py)"))

    brand_canon_ok = run_brand_canon_drift_validation()
    results.append(("PASS" if brand_canon_ok else "FAIL", "BRAND canon drift (scripts/validate_brand_canon_drift.py, I66 P2)"))

    playwright_ok = run_playwright_baseline_validation()
    if os.environ.get("AKOS_PLAYWRIGHT_BASELINE_SCAN_CONSUMERS") == "1":
        results.append((
            "PASS" if playwright_ok else "FAIL",
            "Playwright baseline (scripts/validate_playwright_baseline.py, I68 P2; consumer-scan strict via AKOS_PLAYWRIGHT_BASELINE_SCAN_CONSUMERS=1)",
        ))
    else:
        results.append((
            "PASS" if playwright_ok else "FAIL",
            "Playwright baseline (scripts/validate_playwright_baseline.py, I68 P2; canonical-template only — set AKOS_PLAYWRIGHT_BASELINE_SCAN_CONSUMERS=1 for consumer-repo scan)",
        ))

    sentry_release_ok = run_sentry_release_format_validation()
    if os.environ.get("AKOS_SENTRY_RELEASE_SCAN_CONSUMERS") == "1":
        results.append((
            "PASS" if sentry_release_ok else "FAIL",
            "Sentry release-format (scripts/validate_sentry_release_format.py, I68 P4; consumer-scan strict via AKOS_SENTRY_RELEASE_SCAN_CONSUMERS=1)",
        ))
    else:
        results.append((
            "PASS" if sentry_release_ok else "FAIL",
            "Sentry release-format (scripts/validate_sentry_release_format.py, I68 P4; canonical-doc only — set AKOS_SENTRY_RELEASE_SCAN_CONSUMERS=1 for consumer-repo scan)",
        ))

    cicd_baseline_ok = run_cicd_baseline_validation()
    if os.environ.get("AKOS_CICD_BASELINE_SCAN_CONSUMERS") == "1":
        results.append((
            "PASS" if cicd_baseline_ok else "FAIL",
            "CICD baseline (scripts/validate_cicd_baseline.py, I68 P5; consumer-scan strict via AKOS_CICD_BASELINE_SCAN_CONSUMERS=1)",
        ))
    else:
        results.append((
            "PASS" if cicd_baseline_ok else "FAIL",
            "CICD baseline (scripts/validate_cicd_baseline.py, I68 P5; canonical-SOP+templates only — set AKOS_CICD_BASELINE_SCAN_CONSUMERS=1 for consumer-row scan)",
        ))

    jargon_ok, jargon_rc = run_brand_jargon_validation()
    if os.environ.get("AKOS_BRAND_JARGON_SOFT") == "1":
        results.append((
            "INFO",
            f"BRAND jargon (scripts/validate_brand_jargon.py, soft mode opted-in via AKOS_BRAND_JARGON_SOFT=1; exit={jargon_rc})",
        ))
    else:
        results.append(("PASS" if jargon_ok else "FAIL", "BRAND jargon (scripts/validate_brand_jargon.py, strict — default since I66 P5 incr 3)"))

    voice_ok, voice_rc = run_brand_voice_register_validation()
    if os.environ.get("AKOS_BRAND_VOICE_REGISTER_SOFT") == "1":
        results.append((
            "INFO",
            f"BRAND voice register (scripts/validate_brand_voice_register.py, soft mode opted-in via AKOS_BRAND_VOICE_REGISTER_SOFT=1; exit={voice_rc})",
        ))
    else:
        results.append((
            "PASS" if voice_ok else "FAIL",
            "BRAND voice register (scripts/validate_brand_voice_register.py, strict — default since I66 P5 incr 3 "
            "+ I71 P1 Pack A1 expansion: 7 AI-tone tic families + EN locale + 3-axis audience matrix "
            "+ Storytelling/Resonance boundary + Round 3 Layers 5-9 — strict-day-1 per D-IH-71-F + C-71-8)",
        ))

    vale_level, vale_description = run_brand_voice_vale()
    results.append((vale_level, vale_description))

    baseline_ok, baseline_rc = run_brand_baseline_reality_validation()
    # I89 P0 D-IH-89-E ratified 2026-05-17: BBR drift-gate flipped from INFO to FAIL
    # immediately at I89 P0. Maximum drift protection from day one. OPS-86-5 ADVOPS
    # triage closed 2026-05-18 (D-IH-89-G + D-IH-89-H) - all PRJ-HOL- internal-register
    # leaks cleared from external-facing ENISA dossiers + adviser-handoff exports +
    # boilerplate prose. Hot-fix lane: set AKOS_BRAND_BASELINE_REALITY_SOFT=1 to
    # temporarily downgrade to INFO if a future regression blocks an urgent commit
    # (R-IH-89-1 mitigation). Re-flip immediately after the blocking commit lands.
    if os.environ.get("AKOS_BRAND_BASELINE_REALITY_SOFT") == "1":
        results.append((
            "INFO",
            f"BRAND baseline-reality (scripts/validate_brand_baseline_reality_drift.py, soft via AKOS_BRAND_BASELINE_REALITY_SOFT=1; exit={baseline_rc})",
        ))
    else:
        results.append(("PASS" if baseline_ok else "FAIL", "BRAND baseline-reality (scripts/validate_brand_baseline_reality_drift.py, strict — default since I89 P0 D-IH-89-E)"))

    brand_vision_ok = run_brand_vision_drift_validation()
    results.append(("PASS" if brand_vision_ok else "FAIL", "BRAND vision drift (scripts/validate_brand_vision_drift.py, I66 P7)"))

    impeccable_bridge_ok, impeccable_bridge_rc = run_impeccable_bridge_drift_validation()
    # I77 P3 D-IH-77-E ratified dual-strict posture (Q2 Option C, 2026-05-16):
    # - Today (P2 ship 2026-05-16): soft default + env-var override available.
    # - 2026-06-15 onward: strict default (no env var needed) per dated promotion below.
    # - CI workflows: set AKOS_IMPECCABLE_BRIDGE_DRIFT_STRICT=1 today so CI is already
    #   strict pre-promotion (zero-surprise; the 2026-06-15 default-flip only changes
    #   local-dev behavior). See docs/wip/planning/77-impeccable-brand-bridge-refresh/
    #   reports/uat-impeccable-all-surfaces-2026-05-16.md §6 D-IH-77-E.
    _impeccable_default_strict = (
        os.environ.get("AKOS_IMPECCABLE_BRIDGE_DRIFT_STRICT") == "1"
        or _today_iso() >= "2026-06-15"
    )
    if _impeccable_default_strict:
        results.append((
            "PASS" if impeccable_bridge_ok else "FAIL",
            "IMPECCABLE bridge drift (scripts/validate_impeccable_bridge_drift.py, strict)",
        ))
    else:
        results.append((
            "INFO",
            f"IMPECCABLE bridge drift (scripts/validate_impeccable_bridge_drift.py, "
            f"soft until 2026-06-15 default-flip per D-IH-77-E; exit={impeccable_bridge_rc})",
        ))

    dossier_companion_ok = run_dossier_companion_drift_validation()
    results.append(("PASS" if dossier_companion_ok else "FAIL", "Dossier companion drift (scripts/validate_dossier_companion_drift.py, I66 P7)"))

    repo_contract_ok = run_external_repo_contract_check()
    results.append(("PASS" if repo_contract_ok else "FAIL", "External repo contract (scripts/check_external_repo_contract.py)"))

    ci_posture_ok = run_external_repo_ci_posture_check()
    results.append(("PASS" if ci_posture_ok else "FAIL", "External repo CI/CD posture (scripts/check_external_repo_ci_posture.py)"))

    unblessed_ok = run_unblessed_registry_rows_detection()
    if os.environ.get("AKOS_UNBLESSED_STRICT") == "1":
        results.append(("PASS" if unblessed_ok else "FAIL", "REPOSITORY_REGISTRY un-blessed rows (scripts/detect_unblessed_registry_rows.py, strict)"))
    else:
        results.append(("INFO", "REPOSITORY_REGISTRY un-blessed rows (scripts/detect_unblessed_registry_rows.py, soft)"))

    if os.environ.get("AKOS_EVAL_RUBRIC") == "1":
        eval_ok = run_eval_rubric_slice()
        results.append(("PASS" if eval_ok else "FAIL", "Eval rubric slice (AKOS_EVAL_RUBRIC=1, run-evals.py)"))

    review_stamp_ok, review_stamp_rc = run_review_stamp_validation()
    results.append((
        "INFO",
        f"Review-stamp freshness (scripts/validate_review_stamps.py — 4 mirrored canonicals process_list/decision/initiative/ops; 180-day window; advisory only; I71 P4 D-IH-71-Q; exit={review_stamp_rc})",
    ))

    render_ownership_ok, render_ownership_rc = run_render_ownership_validation()
    if os.environ.get("AKOS_RENDER_OWNERSHIP_STRICT") == "1":
        results.append((
            "PASS" if render_ownership_ok else "FAIL",
            f"BRAND render ownership (scripts/validate_render_ownership.py, STRICT via AKOS_RENDER_OWNERSHIP_STRICT=1; I71 P5 Pack A4 / D-IH-71-S; exit={render_ownership_rc})",
        ))
    else:
        results.append((
            "INFO",
            f"BRAND render ownership (scripts/validate_render_ownership.py — WORKSPACE_BLUEPRINT §16 canonical 9-row matrix; advisory default per §16 discipline; I71 P5 Pack A4 / D-IH-71-S; exit={render_ownership_rc})",
        ))

    observability_ok, observability_rc = run_observability_mcps_check()
    results.append((
        "INFO",
        f"Strand B observability MCP smoke (scripts/check_observability_mcps.py — user-sentry + user-langfuse reachability; never blocks; I71 P5 / D-IH-71-T; C-71-5 every-gate-its-own-row; reachable={'yes' if observability_ok else 'partial'}; exit={observability_rc})",
    ))

    plugin_pinning_ok, plugin_pinning_rc = run_openclaw_plugin_pinning_validation()
    results.append((
        "INFO",
        f"OpenClaw plugin pinning (scripts/validate_openclaw_plugin_pinning.py — config/openclaw.json.example allow-list policy; advisory only; I87 P2 / D-IH-87-B; ok={'yes' if plugin_pinning_ok else 'no'}; exit={plugin_pinning_rc})",
    ))

    audience_tags_ok, audience_tags_rc = run_audience_tags_validation()
    results.append((
        "INFO",
        f"Audience-tag drift (scripts/validate_audience_tags.py — AUDIENCE_REGISTRY.csv FK-validation + J-OP exclusion; advisory until I85 P4 sweep closure; I85 P2 / D-IH-85-A/B/D; ok={'yes' if audience_tags_ok else 'no'}; exit={audience_tags_rc})",
    ))

    render_trail_ok, render_trail_rc = run_external_render_trail_validation()
    results.append((
        "INFO",
        f"External-render trail (scripts/validate_external_render_trail.py — audience-class\u2192render-format matrix; advisory until external-render-pending-tracker.md reaches zero entries; I86 Wave E / D-IH-86-P; ok={'yes' if render_trail_ok else 'no'}; exit={render_trail_rc})",
    ))

    initiative_anchors_ok, initiative_anchors_rc = run_initiative_program_anchors_validation()
    results.append((
        "INFO",
        f"INITIATIVE program-anchors (scripts/validate_initiative_program_anchors.py — INITIATIVE_REGISTRY.notes prefix FK-resolves to PROGRAM_REGISTRY.csv; Stage A advisory until I86 P2 column-promotion; I86 P1 / D-IH-86-H + D-IH-86-J; ok={'yes' if initiative_anchors_ok else 'no'}; exit={initiative_anchors_rc})",
    ))

    inbox_stale, _ = run_operator_inbox_check()
    if inbox_stale:
        results.append(("INFO", "Operator inbox stale — re-run scripts/render_operator_inbox.py (non-blocking; I59 P4)"))
    else:
        results.append(("INFO", "Operator inbox up to date (I59 P4)"))

    freshness_result = proc.run(
        [sys.executable, str(SCRIPTS_DIR / "check_active_initiative_freshness.py")],
        timeout=30,
        capture=False,
    )
    results.append(("INFO", "Active initiative freshness canary (I59 P5)" + (" — stale items flagged" if freshness_result.success else "")))

    live_smoke = os.environ.get("AKOS_LIVE_SMOKE") == "1"
    if live_smoke:
        results.append(("INFO", "Live smoke tests should be run (AKOS_LIVE_SMOKE=1)"))

    all_passed = all(level == "PASS" for level, _ in results if level not in ("INFO", "SKIP"))

    print()
    print("=" * 56)
    print("  AKOS Release Gate")
    print("=" * 56)
    print()
    for level, description in results:
        print(f"  [{level}] {description}")
    print()
    print("-" * 56)
    verdict = "PASS" if all_passed else "FAIL"
    print(f"  Verdict: {verdict}")
    print("-" * 56)
    print()

    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
