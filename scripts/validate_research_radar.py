#!/usr/bin/env python3
"""Validate Research Radar chassis and optional register rows.

``--self-test`` verifies Pydantic fixtures + enum frozensets (pre_commit gate).
Full sweep mode reserved for future register-file validation.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_research_radar import (  # noqa: E402
    INTELLIGENCEOPS_REGISTER_FIELDNAMES,
    RADAR_FINDING_FIELDNAMES,
    SUBSTRATE_VOLATILITY_PROFILES,
    VALID_STALENESS_POSTURES,
    VALID_VOLATILITY_CLASSES,
    VOLATILITY_DEFAULT_STALENESS_DAYS,
    fixture_intelligenceops_radar_row,
)


def self_test() -> int:
    row = fixture_intelligenceops_radar_row()
    if row.volatility_class not in VALID_VOLATILITY_CLASSES:
        print("FAIL: volatility_class fixture")
        return 1
    if row.staleness_posture not in VALID_STALENESS_POSTURES:
        print("FAIL: staleness_posture fixture")
        return 1
    if len(INTELLIGENCEOPS_REGISTER_FIELDNAMES) != 21:
        print(f"FAIL: INTELLIGENCEOPS_REGISTER_FIELDNAMES len={len(INTELLIGENCEOPS_REGISTER_FIELDNAMES)}")
        return 1
    if len(RADAR_FINDING_FIELDNAMES) < 9:
        print("FAIL: RADAR_FINDING_FIELDNAMES too short")
        return 1
    if VOLATILITY_DEFAULT_STALENESS_DAYS["static"] is not None:
        print("FAIL: static default must be None")
        return 1
    if not SUBSTRATE_VOLATILITY_PROFILES:
        print("FAIL: SUBSTRATE_VOLATILITY_PROFILES empty")
        return 1
    resolved = row.resolved_staleness_days()
    if resolved != 90:
        print(f"FAIL: resolved_staleness_days expected 90 got {resolved}")
        return 1
    print("PASS: research-radar self-test")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()
    print("INFO: no operation; use --self-test")
    return 0


if __name__ == "__main__":
    sys.exit(main())
