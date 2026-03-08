#!/usr/bin/env python3
"""AKOS release gate -- runs all required checks before a release.

Executes the full test suite and drift check, then reports an overall
PASS or FAIL verdict. Optionally notes when live smoke tests should be
run (when AKOS_LIVE_SMOKE=1 is set).

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


def run_drift_check() -> bool:
    """Run the drift detection script."""
    logger.info("Running drift check ...")
    result = proc.run(
        [sys.executable, str(SCRIPTS_DIR / "check-drift.py")],
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

    test_ok = run_tests()
    results.append(("PASS" if test_ok else "FAIL", "Test suite (scripts/test.py all)"))

    drift_ok = run_drift_check()
    results.append(("PASS" if drift_ok else "FAIL", "Drift check (scripts/check-drift.py)"))

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
