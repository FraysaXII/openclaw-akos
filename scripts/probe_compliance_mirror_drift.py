#!/usr/bin/env python3
"""Compliance mirror drift probe (Initiative 23 P4).

Two modes:

1. ``--emit-sql`` — print a single SQL block the operator pastes into the
   user-supabase MCP `execute_sql` tool. The block returns one JSON-shaped
   row per mirror with the live row count, plus the canonical CSV row counts
   computed locally. Operator pastes the JSON result into
   ``artifacts/probes/mirror-drift-<YYYYMMDD>.json``.

2. ``--verify`` (default) — read the most recent
   ``artifacts/probes/mirror-drift-*.json`` (or one supplied via ``--from-file``),
   compare against the canonical CSV row counts, and PASS / FAIL accordingly.
   When no fresh artifact exists, **SKIPs gracefully** with a runbook pointer
   (does not block CI).

The probe is **operator-pasted on purpose**: running MCP from CI requires a
service-role token that we are not putting in CI. Local-and-paste is the SOC
posture per ``akos-holistika-operations.mdc`` §"Operator SQL gate" and
``akos-governance-remediation.mdc``.

SOC: this script never reads or writes the service-role token. It only emits
the SQL the operator runs in their authenticated MCP session and parses the
JSON they paste back.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.io import REPO_ROOT

HLK_COMPLIANCE = REPO_ROOT / "docs" / "references" / "hlk" / "compliance"
ARTIFACTS_DIR = REPO_ROOT / "artifacts" / "probes"

# Canonical CSV path -> mirror table -> count column the operator pastes.
MIRROR_CONTRACT: list[tuple[str, Path, str]] = [
    ("compliance.process_list_mirror", HLK_COMPLIANCE / "process_list.csv", "process_list_rows"),
    ("compliance.baseline_organisation_mirror", HLK_COMPLIANCE / "baseline_organisation.csv", "baseline_organisation_rows"),
    ("compliance.finops_counterparty_register_mirror", HLK_COMPLIANCE / "FINOPS_COUNTERPARTY_REGISTER.csv", "finops_counterparty_register_rows"),
    ("compliance.goipoi_register_mirror", HLK_COMPLIANCE / "GOI_POI_REGISTER.csv", "goipoi_register_rows"),
    ("compliance.adviser_engagement_disciplines_mirror", HLK_COMPLIANCE / "ADVISER_ENGAGEMENT_DISCIPLINES.csv", "adviser_engagement_disciplines_rows"),
    ("compliance.adviser_open_questions_mirror", HLK_COMPLIANCE / "ADVISER_OPEN_QUESTIONS.csv", "adviser_open_questions_rows"),
    ("compliance.founder_filed_instruments_mirror", HLK_COMPLIANCE / "FOUNDER_FILED_INSTRUMENTS.csv", "founder_filed_instruments_rows"),
    ("compliance.program_registry_mirror", HLK_COMPLIANCE / "dimensions" / "PROGRAM_REGISTRY.csv", "program_registry_rows"),
]


def count_csv_rows(path: Path) -> int | None:
    if not path.is_file():
        return None
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.reader(fh)
        try:
            next(reader)  # header
        except StopIteration:
            return 0
        return sum(1 for _ in reader)


def csv_counts() -> dict[str, int]:
    out: dict[str, int] = {}
    for table, csv_path, key in MIRROR_CONTRACT:
        rows = count_csv_rows(csv_path)
        if rows is None:
            # CSV absent: skip the corresponding mirror.
            continue
        out[key] = rows
    return out


def emit_sql() -> str:
    """Emit a single JSON-shaped SELECT the operator pastes into MCP execute_sql."""
    select_parts: list[str] = []
    for table, _csv_path, key in MIRROR_CONTRACT:
        select_parts.append(
            f"SELECT '{key}' AS table_name, COUNT(*)::text AS row_count FROM {table}"
        )
    sql = " UNION ALL ".join(select_parts) + " ORDER BY 1;"
    return sql


def cmd_emit_sql() -> int:
    print("-- Initiative 23 P4 mirror drift probe")
    print("-- Operator runs this in user-supabase MCP `execute_sql` (service_role implicit)")
    print("-- and pastes the JSON result into artifacts/probes/mirror-drift-<YYYYMMDD>.json")
    print()
    print(emit_sql())
    print()
    print("-- After pasting, run: py scripts/probe_compliance_mirror_drift.py --verify")
    return 0


def latest_probe_artifact() -> Path | None:
    if not ARTIFACTS_DIR.is_dir():
        return None
    matches = sorted(ARTIFACTS_DIR.glob("mirror-drift-*.json"))
    return matches[-1] if matches else None


def cmd_verify(from_file: Path | None) -> int:
    print("\n  COMPLIANCE_MIRROR_DRIFT probe verifier")
    print("  " + "=" * 40)
    artifact = from_file or latest_probe_artifact()
    if artifact is None or not artifact.is_file():
        print("  SKIP: no probe artifact found under artifacts/probes/mirror-drift-*.json")
        print("  Operator runbook:")
        print("    1. py scripts/probe_compliance_mirror_drift.py --emit-sql")
        print("    2. Run the printed SQL via user-supabase MCP `execute_sql`")
        print("    3. Save the JSON result to artifacts/probes/mirror-drift-<YYYYMMDD>.json")
        print("    4. py scripts/probe_compliance_mirror_drift.py --verify")
        return 0

    try:
        artifact_label = str(artifact.relative_to(REPO_ROOT))
    except ValueError:
        artifact_label = str(artifact)
    print(f"  artifact: {artifact_label}")
    raw = artifact.read_text(encoding="utf-8")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"  FAIL: artifact is not valid JSON ({exc})")
        return 1

    if not isinstance(data, list):
        print("  FAIL: artifact must be a JSON array of {table_name, row_count}")
        return 1

    live: dict[str, int] = {}
    for entry in data:
        if not isinstance(entry, dict):
            continue
        table = str(entry.get("table_name") or entry.get("name") or "").strip()
        count = entry.get("row_count")
        if not table or count is None:
            continue
        try:
            live[table] = int(count)
        except (TypeError, ValueError):
            print(f"  FAIL: non-integer row_count for {table!r}: {count!r}")
            return 1

    csv_count_map = csv_counts()
    drift: list[str] = []
    rows: list[tuple[str, int | None, int | None, str]] = []
    keys = set(live.keys()) | set(csv_count_map.keys())
    for key in sorted(keys):
        canonical = csv_count_map.get(key)
        live_count = live.get(key)
        if canonical is None or live_count is None or canonical != live_count:
            mark = "FAIL"
            drift.append(f"{key}: csv={canonical} live={live_count}")
        else:
            mark = "ok"
        rows.append((key, canonical, live_count, mark))

    for key, canonical, live_count, mark in rows:
        print(f"  [{mark:>4}]  {key:<48s}  csv={canonical}  live={live_count}")

    if drift:
        print(f"  FAIL: {len(drift)} mirror(s) drift")
        return 1
    print("  PASS: all mirrors in parity with canonical CSV row counts")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument(
        "--emit-sql",
        action="store_true",
        help="Print the JSON-shaped SELECT for operator MCP execute_sql; exit 0",
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Verify the latest artifacts/probes/mirror-drift-*.json against canonical CSVs (default)",
    )
    parser.add_argument(
        "--from-file",
        type=Path,
        default=None,
        help="Verify against a specific artifact file instead of the latest",
    )
    args = parser.parse_args()
    if args.emit_sql:
        return cmd_emit_sql()
    return cmd_verify(args.from_file)


if __name__ == "__main__":
    raise SystemExit(main())
