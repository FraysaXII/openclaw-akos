#!/usr/bin/env python3
"""Run named verification profiles from config/verification-profiles.json (SSOT).

Usage:
    py scripts/verify.py --list
    py scripts/verify.py pre_commit
    py scripts/verify.py pre_commit --dry-run
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.io import REPO_ROOT as _ROOT
from akos.verification_profiles import (
    iter_profile_steps,
    list_profile_ids,
    profile_description,
    resolve_argv,
)

assert _ROOT == REPO_ROOT, "repo root mismatch"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run verification profile steps (see config/verification-profiles.json)",
    )
    parser.add_argument(
        "profile",
        nargs="?",
        help="Profile id (e.g. pre_commit, optional_executor_harness). Use --list.",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        dest="list_profiles",
        help="List profile ids and descriptions",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print steps and resolved argv without running",
    )
    args = parser.parse_args()

    if args.list_profiles:
        for pid in list_profile_ids():
            print(f"  {pid:32s}  {profile_description(pid)}")
        return 0

    if not args.profile:
        parser.print_help()
        return 1

    # Normalize kebab to underscore for copy-paste friendliness
    name = str(args.profile).replace("-", "_")
    try:
        steps = list(iter_profile_steps(name))
    except KeyError as e:
        print(f"Error: {e}", file=sys.stderr)
        print("Use: py scripts/verify.py --list", file=sys.stderr)
        return 1
    if not steps:
        print("No steps in profile.", file=sys.stderr)
        return 1

    for step in steps:
        cmd = resolve_argv(step.argv, repo_root=REPO_ROOT)
        label = f"{name} / {step.step_id}"
        if args.dry_run:
            print(f"[DRY-RUN] {label}")
            print(f"          {' '.join(cmd)}")
            print(f"          # {step.description}")
            continue
        print()
        print("  " + "-" * 56)
        print(f"  {label}")
        print(f"  {step.description}")
        print("  " + "-" * 56, flush=True)
        rc = subprocess.call(cmd, cwd=str(REPO_ROOT))
        if rc != 0:
            print(f"\n  Stopped: step {step.step_id!r} exit {rc}", file=sys.stderr)
            return int(rc)
    if args.dry_run:
        return 0
    print()
    print("  All steps in profile completed.\n", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
