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
import logging
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import akos.process as proc
from akos.io import REPO_ROOT
from akos.log import setup_logging
from akos.verification_profiles import governance_rubric_suites

logger = logging.getLogger("akos.release")

SCRIPTS_DIR = REPO_ROOT / "scripts"


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

    Returns ``(ok, exit_code)``. Wired as **INFO** in the gate verdict until
    Initiative 66 P5 closes (boilerplate rewrite). Strict-fail mode flips on
    when ``AKOS_BRAND_JARGON_STRICT=1`` is set.
    """
    logger.info("Running BRAND jargon validation ...")
    result = proc.run(
        [sys.executable, str(SCRIPTS_DIR / "validate_brand_jargon.py")],
        timeout=60,
        capture=False,
    )
    rc = result.returncode if hasattr(result, "returncode") else (0 if result.success else 1)
    return (result.success, rc)


def run_brand_voice_register_validation() -> tuple[bool, int]:
    """Run per-locale voice-register validation (I66 P2).

    Returns ``(ok, exit_code)``. Wired as **INFO** until I66 P5 closes
    (boilerplate i18n rewrite). Flips to FAIL when
    ``AKOS_BRAND_VOICE_REGISTER_STRICT=1``.
    """
    logger.info("Running BRAND voice-register validation ...")
    result = proc.run(
        [sys.executable, str(SCRIPTS_DIR / "validate_brand_voice_register.py")],
        timeout=30,
        capture=False,
    )
    rc = result.returncode if hasattr(result, "returncode") else (0 if result.success else 1)
    return (result.success, rc)


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

    vault_links_ok = run_hlk_vault_links_validation()
    results.append(("PASS" if vault_links_ok else "FAIL", "HLK vault links (scripts/validate_hlk_vault_links.py)"))

    subdomains_ok = run_subdomains_registry_validation()
    results.append(("PASS" if subdomains_ok else "FAIL", "SUBDOMAINS_REGISTRY.md (scripts/validate_subdomains_registry.py)"))

    brand_canon_ok = run_brand_canon_drift_validation()
    results.append(("PASS" if brand_canon_ok else "FAIL", "BRAND canon drift (scripts/validate_brand_canon_drift.py, I66 P2)"))

    jargon_ok, jargon_rc = run_brand_jargon_validation()
    if os.environ.get("AKOS_BRAND_JARGON_STRICT") == "1":
        results.append(("PASS" if jargon_ok else "FAIL", "BRAND jargon (scripts/validate_brand_jargon.py, strict)"))
    else:
        results.append((
            "INFO",
            f"BRAND jargon (scripts/validate_brand_jargon.py, soft until I66 P5; exit={jargon_rc})",
        ))

    voice_ok, voice_rc = run_brand_voice_register_validation()
    if os.environ.get("AKOS_BRAND_VOICE_REGISTER_STRICT") == "1":
        results.append(("PASS" if voice_ok else "FAIL", "BRAND voice register (scripts/validate_brand_voice_register.py, strict)"))
    else:
        results.append((
            "INFO",
            f"BRAND voice register (scripts/validate_brand_voice_register.py, soft until I66 P5; exit={voice_rc})",
        ))

    baseline_ok, baseline_rc = run_brand_baseline_reality_validation()
    if os.environ.get("AKOS_BRAND_BASELINE_REALITY_STRICT") == "1":
        results.append(("PASS" if baseline_ok else "FAIL", "BRAND baseline-reality (scripts/validate_brand_baseline_reality_drift.py, strict)"))
    else:
        results.append((
            "INFO",
            f"BRAND baseline-reality (scripts/validate_brand_baseline_reality_drift.py, soft until I66 P6; exit={baseline_rc})",
        ))

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

    all_passed = all(level == "PASS" for level, _ in results if level != "INFO")

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
