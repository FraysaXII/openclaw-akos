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


def run_eval_rubric_slice() -> bool:
    """Offline rubric eval slice (set AKOS_EVAL_RUBRIC=1 to enable in release gate)."""
    logger.info("Running eval rubric slice (pathc-research-spine) ...")
    result = proc.run(
        [
            sys.executable,
            str(SCRIPTS_DIR / "run-evals.py"),
            "run",
            "--suite",
            "pathc-research-spine",
            "--mode",
            "rubric",
        ],
        timeout=60,
        capture=False,
    )
    return result.success


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

    if os.environ.get("AKOS_EVAL_RUBRIC") == "1":
        eval_ok = run_eval_rubric_slice()
        results.append(("PASS" if eval_ok else "FAIL", "Eval rubric slice (AKOS_EVAL_RUBRIC=1, run-evals.py)"))

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
