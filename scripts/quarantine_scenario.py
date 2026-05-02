#!/usr/bin/env python3
"""Initiative 49 P10 — quarantine a persona scenario row.

Sets ``lifecycle_status=quarantined`` and appends a dated reason into ``notes``
without disturbing other columns. Persists to ``PERSONA_SCENARIO_REGISTRY.csv``
atomically (rename-on-write).

Usage::

    py scripts/quarantine_scenario.py --scenario-id SCN-... --reason "<text>"
    py scripts/quarantine_scenario.py --scenario-id SCN-... --reason "<text>" --dry-run
    py scripts/quarantine_scenario.py --scenario-id SCN-... --release  # back to active

Refer to ``SOP-MADEIRA_SCENARIO_LIFECYCLE_001.md`` §5.2 for the operator
contract; this script is the deterministic execution path. Schema gating is
covered by ``akos.hlk_persona_scenario_csv.VALID_LIFECYCLE_STATUSES``.
"""

from __future__ import annotations

import argparse
import csv
import datetime as _dt
import shutil
import sys
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_persona_scenario_csv import (
    PERSONA_SCENARIO_REGISTRY_FIELDNAMES,
    VALID_LIFECYCLE_STATUSES,
)
from akos.io import REPO_ROOT as IO_REPO_ROOT

CSV_PATH = (
    IO_REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "compliance"
    / "dimensions"
    / "PERSONA_SCENARIO_REGISTRY.csv"
)

QUARANTINE_NOTE_PREFIX = "I49-QUARANTINE"


def _read_rows(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        fieldnames = list(reader.fieldnames or [])
        if fieldnames != list(PERSONA_SCENARIO_REGISTRY_FIELDNAMES):
            raise ValueError(
                "CSV header mismatch; run migrate_persona_registry_i49_columns.py first"
            )
        return list(reader), fieldnames


def _write_rows(path: Path, rows: Iterable[dict[str, str]]) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    try:
        with tmp.open("w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(
                fh, fieldnames=list(PERSONA_SCENARIO_REGISTRY_FIELDNAMES), extrasaction="ignore"
            )
            writer.writeheader()
            writer.writerows(rows)
        shutil.move(str(tmp), str(path))
    finally:
        if tmp.exists():
            tmp.unlink(missing_ok=True)


def _today_iso() -> str:
    return _dt.date.today().isoformat()


def quarantine_scenario(
    csv_path: Path,
    *,
    scenario_id: str,
    reason: str,
    release: bool,
    today: str | None = None,
    dry_run: bool = False,
) -> dict[str, object]:
    """Mutate one scenario row.

    Returns a result dict with `found`, `before`, `after`, `note_appended`.
    """
    rows, _ = _read_rows(csv_path)
    found = False
    before_status: str | None = None
    after_status: str | None = None
    note_appended = False
    today = today or _today_iso()

    for r in rows:
        if (r.get("scenario_id") or "").strip() != scenario_id:
            continue
        found = True
        before_status = (r.get("lifecycle_status") or "").strip()
        if release:
            after_status = "active"
            r["lifecycle_status"] = after_status
        else:
            after_status = "quarantined"
            r["lifecycle_status"] = after_status
            note = f"{QUARANTINE_NOTE_PREFIX} {today}: {reason.strip()}"
            existing = (r.get("notes") or "").strip()
            r["notes"] = (existing + (" | " if existing else "") + note)[:1024]
            note_appended = True
        break

    if not found:
        return {"found": False, "before": None, "after": None, "note_appended": False}

    if after_status not in VALID_LIFECYCLE_STATUSES:
        raise ValueError(f"invalid lifecycle_status target {after_status!r}")

    if not dry_run:
        _write_rows(csv_path, rows)

    return {
        "found": True,
        "before": before_status,
        "after": after_status,
        "note_appended": note_appended,
        "dry_run": dry_run,
    }


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--scenario-id", required=True, help="scenario_id of the registry row to mutate")
    grp = ap.add_mutually_exclusive_group(required=True)
    grp.add_argument("--reason", help="Operator rationale (recorded in notes column with date prefix)")
    grp.add_argument(
        "--release", action="store_true",
        help="Move the row from quarantined back to active (no note appended)",
    )
    ap.add_argument("--dry-run", action="store_true", help="Compute change but do not persist")
    return ap.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    if not CSV_PATH.is_file():
        print("FAIL: PERSONA_SCENARIO_REGISTRY.csv missing", file=sys.stderr)
        return 2
    try:
        result = quarantine_scenario(
            CSV_PATH,
            scenario_id=args.scenario_id,
            reason=args.reason or "",
            release=bool(args.release),
            dry_run=bool(args.dry_run),
        )
    except ValueError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    if not result["found"]:
        print(f"FAIL: scenario_id {args.scenario_id!r} not found in registry", file=sys.stderr)
        return 1

    action = "RELEASED" if args.release else "QUARANTINED"
    suffix = " (dry-run)" if args.dry_run else ""
    print(
        f"{action}{suffix}: scenario_id={args.scenario_id} "
        f"lifecycle_status: {result['before']!r} -> {result['after']!r}",
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
