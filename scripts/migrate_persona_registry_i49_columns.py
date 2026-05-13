#!/usr/bin/env python3
"""One-time column migration Initiative 49 — PERSONA_SCENARIO_REGISTRY.csv.

Adds ``priority_score``, ``safety_lane``, ``release_blocking`` before ``notes``.
Safe to run multiple times (no-op when header already matches SSOT).
"""

from __future__ import annotations

import csv
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_persona_scenario_csv import PERSONA_SCENARIO_REGISTRY_FIELDNAMES
from akos.io import REPO_ROOT as IO_REPO_ROOT

CSV_PATH = IO_REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "dimensions" / "PERSONA_SCENARIO_REGISTRY.csv"


def main() -> int:
    if not CSV_PATH.is_file():
        print("SKIP: PERSONA_SCENARIO_REGISTRY.csv absent")
        return 0

    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        got = reader.fieldnames or []
        if list(got) == list(PERSONA_SCENARIO_REGISTRY_FIELDNAMES):
            print("SKIP: Header already migrated (I49 columns present)")
            return 0
        rows = list(reader)

    legacy_tail = tuple(got[-2:])
    if legacy_tail != ("lifecycle_status", "notes"):
        print(f"FAIL: Unexpected header tail {legacy_tail}; full={got!r}")
        return 1

    out_rows: list[dict[str, str]] = []
    for r in rows:
        normalized: dict[str, str] = {fn: (r.get(fn) or "").strip() for fn in got}
        normalized["priority_score"] = ""
        normalized["safety_lane"] = ""
        normalized["release_blocking"] = ""
        out_rows.append(normalized)

    tmp_path = CSV_PATH.with_suffix(".csv.i49tmp")
    try:
        with tmp_path.open("w", encoding="utf-8", newline="") as fh_out:
            w = csv.DictWriter(
                fh_out,
                fieldnames=list(PERSONA_SCENARIO_REGISTRY_FIELDNAMES),
                extrasaction="ignore",
            )
            w.writeheader()
            slim: list[dict[str, str]] = []
            for r in out_rows:
                slim.append({fn: str(r.get(fn, "") or "") for fn in PERSONA_SCENARIO_REGISTRY_FIELDNAMES})
            w.writerows(slim)
        shutil.move(str(tmp_path), str(CSV_PATH))
    finally:
        if tmp_path.is_file():
            tmp_path.unlink(missing_ok=True)
    print(f"Migrated {len(out_rows)} rows to I49 extended PERSONA_SCENARIO_REGISTRY header.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
