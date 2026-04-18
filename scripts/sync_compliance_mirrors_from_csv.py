#!/usr/bin/env python3
"""Emit PostgreSQL upsert statements for compliance mirror tables from git CSVs.

Maps canonical ``process_list.csv`` and ``baseline_organisation.csv`` to the shapes in
``docs/wip/planning/14-holistika-internal-gtm-mops/reports/sql-proposal-stack-20260417.md``.
Does **not** connect to Supabase by default: outputs SQL for operator review / staging
``apply_migration`` after DDL exists.

Usage (repo root):

    py scripts/sync_compliance_mirrors_from_csv.py --count-only
    py scripts/sync_compliance_mirrors_from_csv.py --output /tmp/mirror-upsert.sql
    py scripts/sync_compliance_mirrors_from_csv.py --git-sha abc123def

Parent IDs: process rows are normalized and ``resolve_all_parent_ids`` is applied so
mirror content matches the same resolution as other HLK tooling.
"""

from __future__ import annotations

import argparse
import csv
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_process_csv import (  # noqa: E402
    PROCESS_LIST_FIELDNAMES,
    normalize_process_row,
    read_process_csv,
    resolve_all_parent_ids,
)

PROC_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "process_list.csv"
ORG_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "baseline_organisation.csv"

# Must match sql-proposal-stack-20260417 §4.3
BASELINE_FIELDNAMES: tuple[str, ...] = (
    "org_uuid",
    "role_name",
    "role_description",
    "role_full_description",
    "access_level",
    "reports_to",
    "area",
    "entity",
    "org_id",
    "sop_url",
    "responsible_processes",
    "components_used",
)


def _git_head_sha() -> str:
    try:
        r = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip()
    except OSError:
        pass
    return "unknown"


def _sql_text_literal(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def _emit_process_list_upserts(rows: list[dict[str, str]], source_git_sha: str) -> list[str]:
    cols_csv = ", ".join(PROCESS_LIST_FIELDNAMES)
    cols_full = cols_csv + ", source_git_sha, synced_at"
    update_sets = ", ".join(
        [f"{c} = EXCLUDED.{c}" for c in PROCESS_LIST_FIELDNAMES]
        + ["source_git_sha = EXCLUDED.source_git_sha", "synced_at = now()"]
    )
    out: list[str] = []
    out.append("-- compliance.process_list_mirror upserts (one row per statement)")
    for r in rows:
        nr = normalize_process_row(r)
        vals = ", ".join(_sql_text_literal(nr[k]) for k in PROCESS_LIST_FIELDNAMES)
        vals_full = f"{vals}, {_sql_text_literal(source_git_sha)}, now()"
        iid = nr["item_id"].strip()
        if not iid:
            continue
        out.append(
            f"INSERT INTO compliance.process_list_mirror ({cols_full}) VALUES ({vals_full}) "
            f"ON CONFLICT (item_id) DO UPDATE SET {update_sets};"
        )
    return out


def _emit_baseline_upserts(rows: list[dict[str, str]], source_git_sha: str) -> list[str]:
    cols_csv = ", ".join(BASELINE_FIELDNAMES)
    cols_full = cols_csv + ", source_git_sha, synced_at"
    update_sets = ", ".join(
        [f"{c} = EXCLUDED.{c}" for c in BASELINE_FIELDNAMES]
        + ["source_git_sha = EXCLUDED.source_git_sha", "synced_at = now()"]
    )
    out: list[str] = []
    out.append("-- compliance.baseline_organisation_mirror upserts")
    for r in rows:
        vals = ", ".join(_sql_text_literal((r.get(c) or "").strip()) for c in BASELINE_FIELDNAMES)
        vals_full = f"{vals}, {_sql_text_literal(source_git_sha)}, now()"
        oid = (r.get("org_uuid") or "").strip()
        if not oid:
            continue
        out.append(
            f"INSERT INTO compliance.baseline_organisation_mirror ({cols_full}) VALUES ({vals_full}) "
            f"ON CONFLICT (org_uuid) DO UPDATE SET {update_sets};"
        )
    return out


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except (OSError, ValueError):
            pass

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--git-sha",
        type=str,
        default=None,
        help="Provenance SHA (default: git rev-parse HEAD, or 'unknown')",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Write SQL to this file (default: stdout)",
    )
    parser.add_argument(
        "--count-only",
        action="store_true",
        help="Print row counts only; no SQL",
    )
    parser.add_argument(
        "--process-list-only",
        action="store_true",
        help="Only emit process_list_mirror statements",
    )
    parser.add_argument(
        "--baseline-only",
        action="store_true",
        help="Only emit baseline_organisation_mirror statements",
    )
    parser.add_argument(
        "--no-begin-commit",
        action="store_true",
        help="Omit BEGIN/COMMIT wrapper",
    )
    args = parser.parse_args()
    if args.process_list_only and args.baseline_only:
        print("error: --process-list-only and --baseline-only are mutually exclusive", file=sys.stderr)
        return 1

    sha = (args.git_sha or "").strip() or _git_head_sha()

    if not PROC_CSV.is_file():
        print("error: missing", PROC_CSV, file=sys.stderr)
        return 1
    if not ORG_CSV.is_file():
        print("error: missing", ORG_CSV, file=sys.stderr)
        return 1

    header, raw_proc = read_process_csv(PROC_CSV)
    if list(header) != PROCESS_LIST_FIELDNAMES:
        print("error: process_list.csv header drift vs PROCESS_LIST_FIELDNAMES", file=sys.stderr)
        return 1
    proc_rows = resolve_all_parent_ids([normalize_process_row(r) for r in raw_proc])

    with ORG_CSV.open(encoding="utf-8", newline="") as f:
        org_reader = csv.DictReader(f)
        org_fn = list(org_reader.fieldnames or [])
        if org_fn != list(BASELINE_FIELDNAMES):
            print("error: baseline_organisation.csv header drift vs script BASELINE_FIELDNAMES", file=sys.stderr)
            print("  expected:", list(BASELINE_FIELDNAMES), file=sys.stderr)
            print("  got:     ", org_fn, file=sys.stderr)
            return 1
        org_rows = [dict(r) for r in org_reader]

    if args.count_only:
        print(f"source_git_sha={sha}")
        print(f"process_list_rows={len(proc_rows)}")
        print(f"baseline_organisation_rows={len(org_rows)}")
        return 0

    blocks: list[str] = []
    if not args.baseline_only:
        blocks.extend(_emit_process_list_upserts(proc_rows, sha))
    if not args.process_list_only:
        blocks.extend(_emit_baseline_upserts(org_rows, sha))

    preamble = [
        "-- Generated by scripts/sync_compliance_mirrors_from_csv.py",
        f"-- source_git_sha: {sha}",
        "-- Apply only after compliance.process_list_mirror / baseline_organisation_mirror exist (see sql-proposal-stack).",
        "",
    ]
    if not args.no_begin_commit:
        preamble.extend(["BEGIN;", ""])

    body = "\n".join(blocks) + "\n"

    ending: list[str] = []
    if not args.no_begin_commit:
        ending = ["", "COMMIT;", ""]

    text = "\n".join(preamble) + body + "\n".join(ending)

    if args.output:
        args.output.write_text(text, encoding="utf-8")
        print("Wrote", args.output, "bytes=", len(text.encode("utf-8")))
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
