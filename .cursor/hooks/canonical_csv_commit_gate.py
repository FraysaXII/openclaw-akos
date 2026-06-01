#!/usr/bin/env python3
"""Cursor hook: pause git commit when canonical HLK CSV paths appear in the command."""

from __future__ import annotations

import json
import re
import sys

_CANONICAL_MARKERS = (
    "People/Compliance/canonicals/",
    "process_list.csv",
    "baseline_organisation.csv",
    "DECISION_REGISTER.csv",
    "INITIATIVE_REGISTRY.csv",
    "OPS_REGISTER.csv",
)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        json.dump({"permission": "allow"}, sys.stdout)
        return 0

    command = str(payload.get("command") or "")
    if not re.search(r"\bgit\s+commit\b", command, re.IGNORECASE):
        json.dump({"permission": "allow"}, sys.stdout)
        return 0

    if any(marker in command for marker in _CANONICAL_MARKERS):
        json.dump(
            {
                "permission": "ask",
                "userMessage": (
                    "This commit may touch canonical HLK CSVs or registries. "
                    "Confirm operator approval and run py scripts/validate_hlk.py "
                    "per akos-baseline-governance.mdc."
                ),
            },
            sys.stdout,
        )
        return 0

    json.dump({"permission": "allow"}, sys.stdout)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
