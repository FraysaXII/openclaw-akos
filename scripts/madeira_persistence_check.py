"""Paired runbook for SOP-TECH_MADEIRA_PERSISTENCE_001 per I76 P3.

Reads `MADEIRA_PERSISTENCE_VEHICLE_REGISTRY.csv` and computes per-vehicle
freshness against each row's `staleness_days` threshold. Stale rows surface
in the human-readable summary table; `--json` emits a machine-readable shape
for downstream tooling.

Usage::

    py scripts/madeira_persistence_check.py
    py scripts/madeira_persistence_check.py --json
    py scripts/madeira_persistence_check.py --vehicle-id vehicle_decision_register

Per-vehicle behaviour:

- Skips ``status in {planned, inactive, deprecated, experimental}`` rows.
- Resolves ``vehicle_path`` against the repo root.
- Path-patterns containing ``<NN>``, ``<date>``, ``<slug>``, or glob ``*``
  are expanded via ``glob.glob`` after substituting ``<...>`` placeholders
  with ``*``; per-instance ages are reported.
- ``provenance == external_system`` rows (e.g. ``cursor:memory``) are
  reported as ``EXTERNAL`` (no mtime check; the external system owns the
  freshness signal).
- Rows with ``staleness_days`` empty (posture ``none``) are reported as
  ``NO_THRESHOLD`` (no mtime check fires).

Exit code 0 on success (regardless of whether stale rows are reported);
exit 1 only on structural failure (missing CSV / unparseable schema).
"""
from __future__ import annotations

import argparse
import csv
import glob as glob_module
import json
import logging
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.hlk_madeira_persistence_vehicle import (
    MADEIRA_PERSISTENCE_VEHICLE_FIELDNAMES,
    MadeiraPersistenceVehicleRow,
)
from akos.io import REPO_ROOT
from akos.log import setup_logging
from pydantic import ValidationError

LOG = logging.getLogger("madeira_persistence_check")

CSV_PATH = (
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "v3.0"
    / "Admin"
    / "O5-1"
    / "Envoy Tech Lab"
    / "canonicals"
    / "dimensions"
    / "MADEIRA_PERSISTENCE_VEHICLE_REGISTRY.csv"
)

# Substitute these path-pattern placeholders with `*` before glob expansion.
_PATH_PATTERN_PLACEHOLDERS = re.compile(r"<[^>]+>")

# The four verdicts a row can carry in the report.
VERDICT_FRESH = "FRESH"
VERDICT_STALE = "STALE"
VERDICT_NO_THRESHOLD = "NO_THRESHOLD"
VERDICT_MISSING = "MISSING"
VERDICT_EXTERNAL = "EXTERNAL"
VERDICT_SKIPPED = "SKIPPED"


@dataclass(frozen=True)
class VehicleVerdict:
    """One report row.

    `instance_path` is the concrete file path probed (after glob expansion);
    `None` means the path-pattern matched no files OR the row is external /
    unthresholded / skipped.
    """

    vehicle_id: str
    status: str
    instance_path: str | None
    last_modified: str | None
    age_days: int | None
    staleness_days: int | None
    staleness_posture: str
    verdict: str

    def as_dict(self) -> dict:
        return {
            "vehicle_id": self.vehicle_id,
            "status": self.status,
            "instance_path": self.instance_path,
            "last_modified": self.last_modified,
            "age_days": self.age_days,
            "staleness_days": self.staleness_days,
            "staleness_posture": self.staleness_posture,
            "verdict": self.verdict,
        }


def _coerce_row(raw: dict[str, str]) -> dict[str, object]:
    out: dict[str, object] = {k: v for k, v in raw.items() if isinstance(k, str)}
    sd = (raw.get("staleness_days") or "").strip()
    out["staleness_days"] = int(sd) if sd else None
    return out


def _load_rows() -> list[MadeiraPersistenceVehicleRow]:
    if not CSV_PATH.is_file():
        raise FileNotFoundError(f"CSV not found at {CSV_PATH}")
    parsed: list[MadeiraPersistenceVehicleRow] = []
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames != list(MADEIRA_PERSISTENCE_VEHICLE_FIELDNAMES):
            raise ValueError(
                "CSV header mismatch; run validate_madeira_persistence_vehicle.py"
            )
        for raw in reader:
            try:
                parsed.append(MadeiraPersistenceVehicleRow(**_coerce_row(raw)))
            except ValidationError as exc:
                raise ValueError(
                    f"row vehicle_id={raw.get('vehicle_id', '<empty>')} "
                    f"failed Pydantic: {exc.errors()}"
                ) from exc
    return parsed


def _expand_path_pattern(pattern: str) -> list[Path]:
    """Expand `<NN>` / `<date>` / `<slug>` placeholders + glob to concrete files.

    Returns absolute paths to existing files. Empty list when pattern matches
    nothing.
    """
    pattern_for_glob = _PATH_PATTERN_PLACEHOLDERS.sub("*", pattern)
    abs_pattern = str(REPO_ROOT / pattern_for_glob)
    matches = glob_module.glob(abs_pattern, recursive=True)
    return [Path(m) for m in matches if Path(m).is_file()]


def _check_one_instance(
    row: MadeiraPersistenceVehicleRow,
    instance: Path,
    today: datetime,
) -> VehicleVerdict:
    mtime = datetime.fromtimestamp(instance.stat().st_mtime, tz=timezone.utc)
    age_days = (today - mtime).days
    if row.staleness_days is None:
        verdict = VERDICT_NO_THRESHOLD
    elif age_days > row.staleness_days:
        verdict = VERDICT_STALE
    else:
        verdict = VERDICT_FRESH
    try:
        rel_path = str(instance.relative_to(REPO_ROOT))
    except ValueError:
        rel_path = str(instance)
    return VehicleVerdict(
        vehicle_id=row.vehicle_id,
        status=row.status,
        instance_path=rel_path,
        last_modified=mtime.date().isoformat(),
        age_days=age_days,
        staleness_days=row.staleness_days,
        staleness_posture=row.staleness_posture,
        verdict=verdict,
    )


def _check_row(
    row: MadeiraPersistenceVehicleRow, today: datetime
) -> list[VehicleVerdict]:
    """Produce one or more verdict rows for a vehicle."""
    if row.status != "active":
        return [
            VehicleVerdict(
                vehicle_id=row.vehicle_id,
                status=row.status,
                instance_path=None,
                last_modified=None,
                age_days=None,
                staleness_days=row.staleness_days,
                staleness_posture=row.staleness_posture,
                verdict=VERDICT_SKIPPED,
            )
        ]

    if row.provenance == "external_system":
        return [
            VehicleVerdict(
                vehicle_id=row.vehicle_id,
                status=row.status,
                instance_path=row.vehicle_path,
                last_modified=None,
                age_days=None,
                staleness_days=row.staleness_days,
                staleness_posture=row.staleness_posture,
                verdict=VERDICT_EXTERNAL,
            )
        ]

    instances = _expand_path_pattern(row.vehicle_path)
    if not instances:
        return [
            VehicleVerdict(
                vehicle_id=row.vehicle_id,
                status=row.status,
                instance_path=row.vehicle_path,
                last_modified=None,
                age_days=None,
                staleness_days=row.staleness_days,
                staleness_posture=row.staleness_posture,
                verdict=VERDICT_MISSING,
            )
        ]

    return [_check_one_instance(row, inst, today) for inst in instances]


def _format_table(verdicts: list[VehicleVerdict]) -> str:
    """Pretty-print verdicts as a human-readable summary table."""
    if not verdicts:
        return "(no rows to report)"

    headers = (
        "vehicle_id",
        "status",
        "last_modified",
        "age_d",
        "thr_d",
        "posture",
        "verdict",
    )
    rows = [
        (
            v.vehicle_id,
            v.status,
            v.last_modified or "-",
            str(v.age_days) if v.age_days is not None else "-",
            str(v.staleness_days) if v.staleness_days is not None else "-",
            v.staleness_posture,
            v.verdict,
        )
        for v in verdicts
    ]
    widths = [max(len(h), *(len(r[i]) for r in rows)) for i, h in enumerate(headers)]

    def _fmt(parts: tuple[str, ...]) -> str:
        return "  ".join(p.ljust(widths[i]) for i, p in enumerate(parts))

    lines = [_fmt(headers), _fmt(tuple("-" * w for w in widths))]
    lines.extend(_fmt(r) for r in rows)
    return "\n".join(lines)


def _summarise(verdicts: list[VehicleVerdict]) -> dict:
    counts: dict[str, int] = {}
    for v in verdicts:
        counts[v.verdict] = counts.get(v.verdict, 0) + 1
    return counts


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="MADEIRA persistence vehicle freshness check (I76 P3 paired runbook)."
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON to stdout (default: human table).",
    )
    parser.add_argument(
        "--vehicle-id",
        type=str,
        default=None,
        help="Check a single vehicle (e.g. 'vehicle_decision_register').",
    )
    args = parser.parse_args(argv)

    if not args.json:
        setup_logging(level=logging.INFO)

    try:
        rows = _load_rows()
    except (FileNotFoundError, ValueError) as exc:
        if args.json:
            print(json.dumps({"error": str(exc)}))
        else:
            LOG.error(str(exc))
        return 1

    if args.vehicle_id:
        rows = [r for r in rows if r.vehicle_id == args.vehicle_id]
        if not rows:
            if args.json:
                print(json.dumps({"error": f"vehicle_id={args.vehicle_id} not found"}))
            else:
                LOG.error("vehicle_id=%s not found in registry", args.vehicle_id)
            return 1

    today = datetime.now(tz=timezone.utc)
    verdicts: list[VehicleVerdict] = []
    for row in rows:
        verdicts.extend(_check_row(row, today))

    if args.json:
        print(
            json.dumps(
                {
                    "checked_at": today.isoformat(),
                    "summary": _summarise(verdicts),
                    "rows": [v.as_dict() for v in verdicts],
                },
                indent=2,
            )
        )
        return 0

    print(_format_table(verdicts))
    print()
    summary = _summarise(verdicts)
    summary_line = ", ".join(f"{k}={v}" for k, v in sorted(summary.items()))
    LOG.info("MADEIRA persistence check: %s", summary_line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
