#!/usr/bin/env python3
"""Cursor hook: remind to run HLK validation after canonical CSV edits."""

from __future__ import annotations

import json
import sys
from pathlib import PurePosixPath


def _is_canonical_csv(path: str) -> bool:
    p = PurePosixPath(path.replace("\\", "/"))
    parts = p.parts
    if "Compliance" in parts and "canonicals" in parts:
        return p.suffix.lower() == ".csv"
    name = p.name
    return name in {
        "process_list.csv",
        "baseline_organisation.csv",
        "DECISION_REGISTER.csv",
        "INITIATIVE_REGISTRY.csv",
        "OPS_REGISTER.csv",
    }


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    file_path = str(payload.get("file_path") or payload.get("path") or "")
    if file_path and _is_canonical_csv(file_path):
        # Advisory only — do not block the edit
        sys.stderr.write(
            "[akos] Canonical CSV edited — run: py scripts/validate_hlk.py "
            "and py scripts/validate_compliance_schema_drift.py when ready.\n"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
