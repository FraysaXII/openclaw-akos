#!/usr/bin/env python3
"""Initiative 49 P10 — quarantine a persona scenario row.

I51 P4 (D-IH-51-B): adds ``--auto-from-flake-history`` mode that consults
``POL-EVAL-FLAKE-THRESHOLD-V1`` (POLICY_REGISTER.csv) and quarantines
scenarios whose consecutive-FAIL count meets the threshold.

Sets ``lifecycle_status=quarantined`` and appends a dated reason into ``notes``
without disturbing other columns. Persists to ``PERSONA_SCENARIO_REGISTRY.csv``
atomically (rename-on-write).

Usage::

    py scripts/quarantine_scenario.py --scenario-id SCN-... --reason "<text>"
    py scripts/quarantine_scenario.py --scenario-id SCN-... --reason "<text>" --dry-run
    py scripts/quarantine_scenario.py --scenario-id SCN-... --release  # back to active
    py scripts/quarantine_scenario.py --auto-from-flake-history <path.json>
    py scripts/quarantine_scenario.py --auto-from-flake-history <path.json> --dry-run

Flake-history JSON schema (``--auto-from-flake-history``):

    [
      {"scenario_id": "SCN-...", "consecutive_failures": 4, "last_run_iso": "2026-..."},
      ...
    ]

Threshold sourced from POLICY row ``POL-EVAL-FLAKE-THRESHOLD-V1``
(``policy_text`` token ``min_consecutive_failures=N``); default 3 if the row
is missing (warn). The threshold is documented in
``docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/POLICY_REGISTER.csv``.

Refer to ``SOP-MADEIRA_SCENARIO_LIFECYCLE_001.md`` §5.2 for the operator
contract; this script is the deterministic execution path. Schema gating is
covered by ``akos.hlk_persona_scenario_csv.VALID_LIFECYCLE_STATUSES``.
"""

from __future__ import annotations

import argparse
import csv
import datetime as _dt
import json
import re
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
from akos.hlk_policy_register_csv import POLICY_REGISTER_FIELDNAMES
from akos.io import REPO_ROOT as IO_REPO_ROOT

CSV_PATH = (
    IO_REPO_ROOT
    / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals"
    / "dimensions"
    / "PERSONA_SCENARIO_REGISTRY.csv"
)
POLICY_CSV = (
    IO_REPO_ROOT
    / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals"
    / "dimensions"
    / "POLICY_REGISTER.csv"
)

QUARANTINE_NOTE_PREFIX = "I49-QUARANTINE"
FLAKE_QUARANTINE_NOTE_PREFIX = "I51-FLAKE-QUARANTINE"
DEFAULT_FLAKE_THRESHOLD = 3
FLAKE_POLICY_ID = "POL-EVAL-FLAKE-THRESHOLD-V1"
_THRESHOLD_TOKEN_RE = re.compile(r"min_consecutive_failures\s*=\s*(\d+)")


def _read_flake_threshold(policy_csv: Path) -> tuple[int, str]:
    """I51 P4 D-IH-51-B: read POL-EVAL-FLAKE-THRESHOLD-V1.

    Returns (threshold, source) where source is "policy" or "default".
    Default fallback uses ``DEFAULT_FLAKE_THRESHOLD``.
    """
    if not policy_csv.is_file():
        return DEFAULT_FLAKE_THRESHOLD, "default"
    with policy_csv.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if list(reader.fieldnames or []) != list(POLICY_REGISTER_FIELDNAMES):
            return DEFAULT_FLAKE_THRESHOLD, "default"
        for row in reader:
            if (row.get("policy_id") or "").strip() != FLAKE_POLICY_ID:
                continue
            text = row.get("policy_text") or ""
            match = _THRESHOLD_TOKEN_RE.search(text)
            if match:
                try:
                    n = int(match.group(1))
                    if n >= 1:
                        return n, "policy"
                except ValueError:
                    pass
    return DEFAULT_FLAKE_THRESHOLD, "default"


def _load_flake_history(path: Path) -> list[dict[str, object]]:
    """I51 P4: read the operator-curated flake history JSON.

    Schema: list of objects, each with at minimum ``scenario_id`` (string)
    and ``consecutive_failures`` (int >= 0). Other keys are ignored
    (e.g., ``last_run_iso`` is informational).
    """
    raw = path.read_text(encoding="utf-8-sig")
    data = json.loads(raw)
    if not isinstance(data, list):
        raise ValueError(f"flake-history root must be a JSON array, got {type(data).__name__}")
    out: list[dict[str, object]] = []
    for i, entry in enumerate(data):
        if not isinstance(entry, dict):
            raise ValueError(f"flake-history entry [{i}] is not an object")
        sid = (entry.get("scenario_id") or "")
        if not isinstance(sid, str) or not sid.strip():
            raise ValueError(f"flake-history entry [{i}] missing scenario_id")
        cf = entry.get("consecutive_failures")
        if not isinstance(cf, int) or cf < 0:
            raise ValueError(
                f"flake-history entry [{i}] ({sid}): consecutive_failures must be int >= 0"
            )
        out.append(dict(entry))
    return out


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


def auto_quarantine_from_flake_history(
    csv_path: Path,
    flake_history: list[dict[str, object]],
    *,
    threshold: int,
    today: str | None = None,
    dry_run: bool = False,
) -> dict[str, object]:
    """I51 P4 D-IH-51-B: auto-quarantine scenarios above the flake threshold.

    Returns a summary dict with ``threshold``, ``candidates``, ``quarantined``,
    ``skipped_already_quarantined``, ``not_found``, and ``per_scenario`` entries.
    """
    today = today or _today_iso()
    rows, _ = _read_rows(csv_path)
    by_sid: dict[str, dict[str, str]] = {(r.get("scenario_id") or "").strip(): r for r in rows}

    candidates: list[dict[str, object]] = []
    quarantined: list[str] = []
    skipped_already: list[str] = []
    not_found: list[str] = []
    no_change: list[str] = []
    for entry in flake_history:
        sid = str(entry["scenario_id"]).strip()
        cf = int(entry["consecutive_failures"])
        if cf < threshold:
            no_change.append(sid)
            continue
        candidates.append({"scenario_id": sid, "consecutive_failures": cf})
        target = by_sid.get(sid)
        if target is None:
            not_found.append(sid)
            continue
        before = (target.get("lifecycle_status") or "").strip()
        if before == "quarantined":
            skipped_already.append(sid)
            continue
        target["lifecycle_status"] = "quarantined"
        note = (
            f"{FLAKE_QUARANTINE_NOTE_PREFIX} {today}: "
            f"consecutive_failures={cf} >= threshold={threshold} "
            f"({FLAKE_POLICY_ID})"
        )
        existing = (target.get("notes") or "").strip()
        target["notes"] = (existing + (" | " if existing else "") + note)[:1024]
        quarantined.append(sid)

    if quarantined and not dry_run:
        _write_rows(csv_path, rows)

    return {
        "threshold": threshold,
        "candidates": candidates,
        "quarantined": quarantined,
        "skipped_already_quarantined": skipped_already,
        "not_found": not_found,
        "no_change_below_threshold": no_change,
        "dry_run": dry_run,
    }


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    grp = ap.add_mutually_exclusive_group(required=True)
    grp.add_argument(
        "--scenario-id",
        help="scenario_id of the registry row to mutate (single-row mode)",
    )
    grp.add_argument(
        "--auto-from-flake-history",
        type=Path,
        default=None,
        help=(
            "I51 P4 D-IH-51-B: path to JSON flake-history file; auto-quarantine "
            "scenarios with consecutive_failures >= POL-EVAL-FLAKE-THRESHOLD-V1."
        ),
    )
    # Single-row sub-args (only meaningful with --scenario-id):
    sub = ap.add_mutually_exclusive_group(required=False)
    sub.add_argument(
        "--reason",
        help="Operator rationale (recorded in notes column with date prefix)",
    )
    sub.add_argument(
        "--release", action="store_true",
        help="Move the row from quarantined back to active (no note appended)",
    )
    ap.add_argument("--dry-run", action="store_true", help="Compute change but do not persist")
    args = ap.parse_args(argv)
    # Single-row mode requires either --reason or --release.
    if args.scenario_id and not (args.reason or args.release):
        ap.error("--scenario-id requires either --reason or --release")
    return args


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    if not CSV_PATH.is_file():
        print("FAIL: PERSONA_SCENARIO_REGISTRY.csv missing", file=sys.stderr)
        return 2

    if args.auto_from_flake_history is not None:
        # I51 P4 — bulk mode.
        if not args.auto_from_flake_history.is_file():
            print(f"FAIL: flake-history file not found: {args.auto_from_flake_history}", file=sys.stderr)
            return 2
        try:
            history = _load_flake_history(args.auto_from_flake_history)
        except (ValueError, json.JSONDecodeError) as exc:
            print(f"FAIL: malformed flake-history: {exc}", file=sys.stderr)
            return 1
        threshold, source = _read_flake_threshold(POLICY_CSV)
        if source == "default":
            print(
                f"WARNING: {FLAKE_POLICY_ID} not found in POLICY_REGISTER.csv; "
                f"using default threshold={threshold}.",
                file=sys.stderr,
            )
        try:
            summary = auto_quarantine_from_flake_history(
                CSV_PATH,
                history,
                threshold=threshold,
                dry_run=bool(args.dry_run),
            )
        except ValueError as exc:
            print(f"FAIL: {exc}", file=sys.stderr)
            return 1
        suffix = " (dry-run)" if args.dry_run else ""
        print(
            f"AUTO-QUARANTINE{suffix}: threshold={summary['threshold']} ({source}); "
            f"history_rows={len(history)}; candidates={len(summary['candidates'])}; "
            f"quarantined={len(summary['quarantined'])}; "
            f"skipped_already_quarantined={len(summary['skipped_already_quarantined'])}; "
            f"not_found={len(summary['not_found'])}; "
            f"below_threshold={len(summary['no_change_below_threshold'])}"
        )
        for sid in summary["quarantined"]:
            print(f"  -> quarantined: {sid}")
        for sid in summary["skipped_already_quarantined"]:
            print(f"  =  already quarantined: {sid}")
        for sid in summary["not_found"]:
            print(f"  ?  not in registry: {sid}", file=sys.stderr)
        return 0

    # Single-row mode (existing I49 P10 path).
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
