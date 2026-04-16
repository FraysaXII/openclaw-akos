#!/usr/bin/env python3
"""Thin operator dispatcher — forwards to canonical scripts (no duplicate logic).

Usage:
    py scripts/akos_operator.py bootstrap [-- …]
    py scripts/akos_operator.py doctor [-- …]
    py scripts/akos_operator.py serve-api [-- …]
    py scripts/akos_operator.py test [group] [-- pytest-args]
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def _forward(script: str, forwarded: list[str]) -> int:
    cmd = [sys.executable, str(REPO_ROOT / "scripts" / script), *forwarded]
    return subprocess.call(cmd, cwd=str(REPO_ROOT))


def main() -> int:
    parser = argparse.ArgumentParser(description="AKOS operator script dispatcher")
    parser.add_argument(
        "command",
        choices=("bootstrap", "doctor", "serve-api", "test"),
        help="Which canonical script to run",
    )
    parser.add_argument(
        "rest",
        nargs=argparse.REMAINDER,
        help="Arguments passed through to the target script",
    )
    args = parser.parse_args()
    tail = list(args.rest)
    if tail and tail[0] == "--":
        tail = tail[1:]

    if args.command == "bootstrap":
        return _forward("bootstrap.py", tail)
    if args.command == "doctor":
        return _forward("doctor.py", tail)
    if args.command == "serve-api":
        return _forward("serve-api.py", tail)
    if args.command == "test":
        group = tail[0] if tail else "all"
        extra = tail[1:] if len(tail) > 1 else []
        return _forward("test.py", [group, *extra])
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
