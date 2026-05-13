#!/usr/bin/env python3
"""Initiative 59 P1.5 sync gate - decision-log.md headers <-> DECISION_REGISTER.csv.

Per **D-IH-59-B** two-layer SSOT: per-initiative ``decision-log.md`` files stay
canonical for prose (full alternatives + rationale + reversibility narrative);
``DECISION_REGISTER.csv`` is canonical for governed metadata (queryable index;
FK targets).

This validator is **advisory by default** (exits 0 even on drift) per
**D-IH-59-E** + the realities of legacy initiative audits: many older
``decision-log.md`` files were authored before the registry existed; full
audit is best-effort and idempotent. It surfaces drift counts in the report
so future cycles can chip at the gap.

Pass ``--strict`` to fail-loud (used inside dedicated audit cycles).

Usage::

    py scripts/validate_decision_register_decision_log_md_sync.py
    py scripts/validate_decision_register_decision_log_md_sync.py --strict
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.io import REPO_ROOT

CSV_PATH = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "DECISION_REGISTER.csv"
PLANNING_ROOT = REPO_ROOT / "docs" / "wip" / "planning"

DECISION_HEADER_RE = re.compile(r"^##\s+(D-IH-[A-Za-z0-9-]+)\s*[—-]")


def _csv_decision_ids(path: Path) -> set[str]:
    if not path.is_file():
        return set()
    with path.open(encoding="utf-8", newline="") as fh:
        return {
            (row.get("decision_id") or "").strip()
            for row in csv.DictReader(fh)
            if (row.get("decision_id") or "").strip()
        }


def _md_decision_ids() -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    if not PLANNING_ROOT.is_dir():
        return out
    for log in PLANNING_ROOT.rglob("decision-log.md"):
        rel = log.relative_to(REPO_ROOT).as_posix()
        for line in log.read_text(encoding="utf-8").splitlines():
            m = DECISION_HEADER_RE.match(line)
            if m:
                out.setdefault(m.group(1), []).append(rel)
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true", help="exit 1 on drift")
    args = parser.parse_args()

    print("\n  DECISION_REGISTER decision-log.md sync")
    print("  " + "=" * 40)

    csv_ids = _csv_decision_ids(CSV_PATH)
    md_ids_to_files = _md_decision_ids()
    md_ids = set(md_ids_to_files.keys())

    only_md = md_ids - csv_ids
    only_csv = csv_ids - md_ids

    print(f"  CSV decision_ids:    {len(csv_ids)}")
    print(f"  MD decision headers: {len(md_ids)}")
    print(f"  Common:              {len(csv_ids & md_ids)}")
    print(f"  In MD not CSV:       {len(only_md)}")
    print(f"  In CSV not MD:       {len(only_csv)}")

    if only_md:
        print("  Top examples in MD not in CSV (audit candidates):")
        for did in sorted(only_md)[:10]:
            paths = md_ids_to_files[did]
            print(f"    - {did} (in {paths[0]})")
        if len(only_md) > 10:
            print(f"    ... and {len(only_md) - 10} more")

    if only_csv:
        print("  In CSV but no matching MD header (review):")
        for did in sorted(only_csv)[:10]:
            print(f"    - {did}")

    if args.strict and (only_md or only_csv):
        print("  FAIL: --strict mode")
        return 1

    print("  PASS (advisory; --strict to fail-loud)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
