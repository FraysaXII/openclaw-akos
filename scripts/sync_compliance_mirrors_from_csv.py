#!/usr/bin/env python3
"""Emit PostgreSQL upsert statements for compliance mirror tables from git CSVs.

Maps canonical ``process_list.csv``, ``baseline_organisation.csv``, and optionally
``FINOPS_COUNTERPARTY_REGISTER.csv`` to compliance mirror shapes in
``docs/wip/planning/14-holistika-internal-gtm-mops/reports/sql-proposal-stack-20260417.md``
(Initiative 18 FINOPS counterparty mirror DDL under ``scripts/sql/i18_phase1_staging/``).
Does **not** connect to Supabase by default: outputs SQL for operator review / staging
``apply_migration`` after DDL exists.

Usage (repo root):

    py scripts/sync_compliance_mirrors_from_csv.py --count-only
    py scripts/sync_compliance_mirrors_from_csv.py --finops-counterparty-register-only --output /tmp/finops-upsert.sql
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

from akos.hlk_adviser_disciplines_csv import ADVISER_ENGAGEMENT_DISCIPLINES_FIELDNAMES  # noqa: E402
from akos.hlk_adviser_questions_csv import ADVISER_OPEN_QUESTIONS_FIELDNAMES  # noqa: E402
from akos.hlk_finops_counterparty_csv import FINOPS_COUNTERPARTY_REGISTER_FIELDNAMES  # noqa: E402
from akos.hlk_founder_filed_instruments_csv import FOUNDER_FILED_INSTRUMENTS_FIELDNAMES  # noqa: E402
from akos.hlk_goipoi_csv import GOIPOI_REGISTER_FIELDNAMES  # noqa: E402
from akos.hlk_program_registry_csv import PROGRAM_REGISTRY_FIELDNAMES  # noqa: E402
from akos.hlk_process_csv import (  # noqa: E402
    PROCESS_LIST_FIELDNAMES,
    normalize_process_row,
    read_process_csv,
    resolve_all_parent_ids,
)

PROC_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "process_list.csv"
ORG_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "baseline_organisation.csv"
FINOPS_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "FINOPS_COUNTERPARTY_REGISTER.csv"
GOIPOI_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "GOI_POI_REGISTER.csv"
ADVISER_DISCIPLINES_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "ADVISER_ENGAGEMENT_DISCIPLINES.csv"
ADVISER_QUESTIONS_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "ADVISER_OPEN_QUESTIONS.csv"
FILED_INSTRUMENTS_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "FOUNDER_FILED_INSTRUMENTS.csv"
PROGRAM_REGISTRY_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "dimensions" / "PROGRAM_REGISTRY.csv"

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


def _emit_finops_counterparty_upserts(rows: list[dict[str, str]], source_git_sha: str) -> list[str]:
    cols_csv = ", ".join(FINOPS_COUNTERPARTY_REGISTER_FIELDNAMES)
    cols_full = cols_csv + ", source_git_sha, synced_at"
    update_sets = ", ".join(
        [f"{c} = EXCLUDED.{c}" for c in FINOPS_COUNTERPARTY_REGISTER_FIELDNAMES]
        + ["source_git_sha = EXCLUDED.source_git_sha", "synced_at = now()"]
    )
    out: list[str] = []
    out.append("-- compliance.finops_counterparty_register_mirror upserts")
    for r in rows:
        vals = ", ".join(_sql_text_literal((r.get(c) or "").strip()) for c in FINOPS_COUNTERPARTY_REGISTER_FIELDNAMES)
        vals_full = f"{vals}, {_sql_text_literal(source_git_sha)}, now()"
        cid = (r.get("counterparty_id") or "").strip()
        if not cid:
            continue
        out.append(
            f"INSERT INTO compliance.finops_counterparty_register_mirror ({cols_full}) VALUES ({vals_full}) "
            f"ON CONFLICT (counterparty_id) DO UPDATE SET {update_sets};"
        )
    return out


def _emit_goipoi_upserts(rows: list[dict[str, str]], source_git_sha: str) -> list[str]:
    cols_csv = ", ".join(GOIPOI_REGISTER_FIELDNAMES)
    cols_full = cols_csv + ", source_git_sha, synced_at"
    update_sets = ", ".join(
        [f"{c} = EXCLUDED.{c}" for c in GOIPOI_REGISTER_FIELDNAMES]
        + ["source_git_sha = EXCLUDED.source_git_sha", "synced_at = now()"]
    )
    out: list[str] = []
    out.append("-- compliance.goipoi_register_mirror upserts")
    for r in rows:
        vals = ", ".join(_sql_text_literal((r.get(c) or "").strip()) for c in GOIPOI_REGISTER_FIELDNAMES)
        vals_full = f"{vals}, {_sql_text_literal(source_git_sha)}, now()"
        ref = (r.get("ref_id") or "").strip()
        if not ref:
            continue
        out.append(
            f"INSERT INTO compliance.goipoi_register_mirror ({cols_full}) VALUES ({vals_full}) "
            f"ON CONFLICT (ref_id) DO UPDATE SET {update_sets};"
        )
    return out


def _emit_adviser_disciplines_upserts(rows: list[dict[str, str]], source_git_sha: str) -> list[str]:
    cols_csv = ", ".join(ADVISER_ENGAGEMENT_DISCIPLINES_FIELDNAMES)
    cols_full = cols_csv + ", source_git_sha, synced_at"
    update_sets = ", ".join(
        [f"{c} = EXCLUDED.{c}" for c in ADVISER_ENGAGEMENT_DISCIPLINES_FIELDNAMES]
        + ["source_git_sha = EXCLUDED.source_git_sha", "synced_at = now()"]
    )
    out: list[str] = []
    out.append("-- compliance.adviser_engagement_disciplines_mirror upserts")
    for r in rows:
        vals = ", ".join(_sql_text_literal((r.get(c) or "").strip()) for c in ADVISER_ENGAGEMENT_DISCIPLINES_FIELDNAMES)
        vals_full = f"{vals}, {_sql_text_literal(source_git_sha)}, now()"
        did = (r.get("discipline_id") or "").strip()
        if not did:
            continue
        out.append(
            f"INSERT INTO compliance.adviser_engagement_disciplines_mirror ({cols_full}) VALUES ({vals_full}) "
            f"ON CONFLICT (discipline_id) DO UPDATE SET {update_sets};"
        )
    return out


def _emit_adviser_questions_upserts(rows: list[dict[str, str]], source_git_sha: str) -> list[str]:
    cols_csv = ", ".join(ADVISER_OPEN_QUESTIONS_FIELDNAMES)
    cols_full = cols_csv + ", source_git_sha, synced_at"
    update_sets = ", ".join(
        [f"{c} = EXCLUDED.{c}" for c in ADVISER_OPEN_QUESTIONS_FIELDNAMES]
        + ["source_git_sha = EXCLUDED.source_git_sha", "synced_at = now()"]
    )
    out: list[str] = []
    out.append("-- compliance.adviser_open_questions_mirror upserts")
    for r in rows:
        vals = ", ".join(_sql_text_literal((r.get(c) or "").strip()) for c in ADVISER_OPEN_QUESTIONS_FIELDNAMES)
        vals_full = f"{vals}, {_sql_text_literal(source_git_sha)}, now()"
        qid = (r.get("question_id") or "").strip()
        if not qid:
            continue
        out.append(
            f"INSERT INTO compliance.adviser_open_questions_mirror ({cols_full}) VALUES ({vals_full}) "
            f"ON CONFLICT (question_id) DO UPDATE SET {update_sets};"
        )
    return out


def _emit_founder_filed_instruments_upserts(rows: list[dict[str, str]], source_git_sha: str) -> list[str]:
    cols_csv = ", ".join(FOUNDER_FILED_INSTRUMENTS_FIELDNAMES)
    cols_full = cols_csv + ", source_git_sha, synced_at"
    update_sets = ", ".join(
        [f"{c} = EXCLUDED.{c}" for c in FOUNDER_FILED_INSTRUMENTS_FIELDNAMES]
        + ["source_git_sha = EXCLUDED.source_git_sha", "synced_at = now()"]
    )
    out: list[str] = []
    out.append("-- compliance.founder_filed_instruments_mirror upserts")
    for r in rows:
        vals = ", ".join(_sql_text_literal((r.get(c) or "").strip()) for c in FOUNDER_FILED_INSTRUMENTS_FIELDNAMES)
        vals_full = f"{vals}, {_sql_text_literal(source_git_sha)}, now()"
        iid = (r.get("instrument_id") or "").strip()
        if not iid:
            continue
        out.append(
            f"INSERT INTO compliance.founder_filed_instruments_mirror ({cols_full}) VALUES ({vals_full}) "
            f"ON CONFLICT (instrument_id) DO UPDATE SET {update_sets};"
        )
    return out


def _emit_program_registry_upserts(rows: list[dict[str, str]], source_git_sha: str) -> list[str]:
    """Initiative 23 P2 mirror upsert emitter for compliance.program_registry_mirror.

    Same shape as the other Wave-2 mirrors (DAMA-pure projection of CSV; semicolon-list
    columns stored verbatim as TEXT; Neo4j projection extends from CSV separately).
    """
    cols_csv = ", ".join(PROGRAM_REGISTRY_FIELDNAMES)
    cols_full = cols_csv + ", source_git_sha, synced_at"
    update_sets = ", ".join(
        [f"{c} = EXCLUDED.{c}" for c in PROGRAM_REGISTRY_FIELDNAMES]
        + ["source_git_sha = EXCLUDED.source_git_sha", "synced_at = now()"]
    )
    out: list[str] = []
    out.append("-- compliance.program_registry_mirror upserts (Initiative 23)")
    for r in rows:
        vals = ", ".join(_sql_text_literal((r.get(c) or "").strip()) for c in PROGRAM_REGISTRY_FIELDNAMES)
        vals_full = f"{vals}, {_sql_text_literal(source_git_sha)}, now()"
        pid = (r.get("program_id") or "").strip()
        if not pid:
            continue
        out.append(
            f"INSERT INTO compliance.program_registry_mirror ({cols_full}) VALUES ({vals_full}) "
            f"ON CONFLICT (program_id) DO UPDATE SET {update_sets};"
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
        "--finops-counterparty-register-only",
        action="store_true",
        help="Only emit finops_counterparty_register_mirror statements (requires FINOPS_COUNTERPARTY_REGISTER.csv)",
    )
    parser.add_argument(
        "--goipoi-register-only",
        action="store_true",
        help="Only emit goipoi_register_mirror statements (requires GOI_POI_REGISTER.csv)",
    )
    parser.add_argument(
        "--adviser-disciplines-only",
        action="store_true",
        help="Only emit adviser_engagement_disciplines_mirror statements (requires ADVISER_ENGAGEMENT_DISCIPLINES.csv)",
    )
    parser.add_argument(
        "--adviser-questions-only",
        action="store_true",
        help="Only emit adviser_open_questions_mirror statements (requires ADVISER_OPEN_QUESTIONS.csv)",
    )
    parser.add_argument(
        "--founder-filed-instruments-only",
        action="store_true",
        help="Only emit founder_filed_instruments_mirror statements (requires FOUNDER_FILED_INSTRUMENTS.csv)",
    )
    parser.add_argument(
        "--program-registry-only",
        action="store_true",
        help="Only emit program_registry_mirror statements (requires dimensions/PROGRAM_REGISTRY.csv) [Initiative 23]",
    )
    parser.add_argument(
        "--no-begin-commit",
        action="store_true",
        help="Omit BEGIN/COMMIT wrapper",
    )
    args = parser.parse_args()
    mode_flags = sum(
        1
        for x in (
            args.process_list_only,
            args.baseline_only,
            args.finops_counterparty_register_only,
            args.goipoi_register_only,
            args.adviser_disciplines_only,
            args.adviser_questions_only,
            args.founder_filed_instruments_only,
            args.program_registry_only,
        )
        if x
    )
    if mode_flags > 1:
        print(
            "error: at most one of --process-list-only, --baseline-only, "
            "--finops-counterparty-register-only, --goipoi-register-only, "
            "--adviser-disciplines-only, --adviser-questions-only, "
            "--founder-filed-instruments-only, --program-registry-only",
            file=sys.stderr,
        )
        return 1

    sha = (args.git_sha or "").strip() or _git_head_sha()

    if args.finops_counterparty_register_only:
        if not FINOPS_CSV.is_file():
            print("error: missing", FINOPS_CSV, file=sys.stderr)
            return 1
        with FINOPS_CSV.open(encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            fn = list(reader.fieldnames or [])
            if fn != list(FINOPS_COUNTERPARTY_REGISTER_FIELDNAMES):
                print(
                    "error: FINOPS_COUNTERPARTY_REGISTER.csv header drift vs FINOPS_COUNTERPARTY_REGISTER_FIELDNAMES",
                    file=sys.stderr,
                )
                print("  expected:", list(FINOPS_COUNTERPARTY_REGISTER_FIELDNAMES), file=sys.stderr)
                print("  got:     ", fn, file=sys.stderr)
                return 1
            finops_rows = [dict(r) for r in reader]
        if args.count_only:
            print(f"source_git_sha={sha}")
            print(f"finops_counterparty_register_rows={len(finops_rows)}")
            return 0
        blocks = _emit_finops_counterparty_upserts(finops_rows, sha)
        preamble = [
            "-- Generated by scripts/sync_compliance_mirrors_from_csv.py",
            f"-- source_git_sha: {sha}",
            "-- Apply only after compliance.finops_counterparty_register_mirror exists (Initiative 18 DDL).",
            "",
        ]
        if not args.no_begin_commit:
            preamble.extend(["BEGIN;", ""])
        body = "\n".join(blocks) + "\n"
        ending = ["", "COMMIT;", ""] if not args.no_begin_commit else []
        text = "\n".join(preamble) + body + "\n".join(ending)
        if args.output:
            args.output.write_text(text, encoding="utf-8")
            print("Wrote", args.output, "bytes=", len(text.encode("utf-8")))
        else:
            sys.stdout.write(text)
        return 0

    if args.goipoi_register_only:
        if not GOIPOI_CSV.is_file():
            print("error: missing", GOIPOI_CSV, file=sys.stderr)
            return 1
        with GOIPOI_CSV.open(encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            fn = list(reader.fieldnames or [])
            if fn != list(GOIPOI_REGISTER_FIELDNAMES):
                print(
                    "error: GOI_POI_REGISTER.csv header drift vs GOIPOI_REGISTER_FIELDNAMES",
                    file=sys.stderr,
                )
                print("  expected:", list(GOIPOI_REGISTER_FIELDNAMES), file=sys.stderr)
                print("  got:     ", fn, file=sys.stderr)
                return 1
            goipoi_rows = [dict(r) for r in reader]
        if args.count_only:
            print(f"source_git_sha={sha}")
            print(f"goipoi_register_rows={len(goipoi_rows)}")
            return 0
        blocks = _emit_goipoi_upserts(goipoi_rows, sha)
        preamble = [
            "-- Generated by scripts/sync_compliance_mirrors_from_csv.py",
            f"-- source_git_sha: {sha}",
            "-- Apply only after compliance.goipoi_register_mirror exists (Initiative 21 DDL).",
            "",
        ]
        if not args.no_begin_commit:
            preamble.extend(["BEGIN;", ""])
        body = "\n".join(blocks) + "\n"
        ending = ["", "COMMIT;", ""] if not args.no_begin_commit else []
        text = "\n".join(preamble) + body + "\n".join(ending)
        if args.output:
            args.output.write_text(text, encoding="utf-8")
            print("Wrote", args.output, "bytes=", len(text.encode("utf-8")))
        else:
            sys.stdout.write(text)
        return 0

    if args.adviser_disciplines_only:
        if not ADVISER_DISCIPLINES_CSV.is_file():
            print("error: missing", ADVISER_DISCIPLINES_CSV, file=sys.stderr)
            return 1
        with ADVISER_DISCIPLINES_CSV.open(encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            fn = list(reader.fieldnames or [])
            if fn != list(ADVISER_ENGAGEMENT_DISCIPLINES_FIELDNAMES):
                print(
                    "error: ADVISER_ENGAGEMENT_DISCIPLINES.csv header drift vs ADVISER_ENGAGEMENT_DISCIPLINES_FIELDNAMES",
                    file=sys.stderr,
                )
                print("  expected:", list(ADVISER_ENGAGEMENT_DISCIPLINES_FIELDNAMES), file=sys.stderr)
                print("  got:     ", fn, file=sys.stderr)
                return 1
            ad_rows = [dict(r) for r in reader]
        if args.count_only:
            print(f"source_git_sha={sha}")
            print(f"adviser_engagement_disciplines_rows={len(ad_rows)}")
            return 0
        blocks = _emit_adviser_disciplines_upserts(ad_rows, sha)
        preamble = [
            "-- Generated by scripts/sync_compliance_mirrors_from_csv.py",
            f"-- source_git_sha: {sha}",
            "-- Apply only after compliance.adviser_engagement_disciplines_mirror exists (Initiative 21 DDL).",
            "",
        ]
        if not args.no_begin_commit:
            preamble.extend(["BEGIN;", ""])
        body = "\n".join(blocks) + "\n"
        ending = ["", "COMMIT;", ""] if not args.no_begin_commit else []
        text = "\n".join(preamble) + body + "\n".join(ending)
        if args.output:
            args.output.write_text(text, encoding="utf-8")
            print("Wrote", args.output, "bytes=", len(text.encode("utf-8")))
        else:
            sys.stdout.write(text)
        return 0

    if args.adviser_questions_only:
        if not ADVISER_QUESTIONS_CSV.is_file():
            print("error: missing", ADVISER_QUESTIONS_CSV, file=sys.stderr)
            return 1
        with ADVISER_QUESTIONS_CSV.open(encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            fn = list(reader.fieldnames or [])
            if fn != list(ADVISER_OPEN_QUESTIONS_FIELDNAMES):
                print(
                    "error: ADVISER_OPEN_QUESTIONS.csv header drift vs ADVISER_OPEN_QUESTIONS_FIELDNAMES",
                    file=sys.stderr,
                )
                print("  expected:", list(ADVISER_OPEN_QUESTIONS_FIELDNAMES), file=sys.stderr)
                print("  got:     ", fn, file=sys.stderr)
                return 1
            aq_rows = [dict(r) for r in reader]
        if args.count_only:
            print(f"source_git_sha={sha}")
            print(f"adviser_open_questions_rows={len(aq_rows)}")
            return 0
        blocks = _emit_adviser_questions_upserts(aq_rows, sha)
        preamble = [
            "-- Generated by scripts/sync_compliance_mirrors_from_csv.py",
            f"-- source_git_sha: {sha}",
            "-- Apply only after compliance.adviser_open_questions_mirror exists (Initiative 21 DDL).",
            "",
        ]
        if not args.no_begin_commit:
            preamble.extend(["BEGIN;", ""])
        body = "\n".join(blocks) + "\n"
        ending = ["", "COMMIT;", ""] if not args.no_begin_commit else []
        text = "\n".join(preamble) + body + "\n".join(ending)
        if args.output:
            args.output.write_text(text, encoding="utf-8")
            print("Wrote", args.output, "bytes=", len(text.encode("utf-8")))
        else:
            sys.stdout.write(text)
        return 0

    if args.founder_filed_instruments_only:
        if not FILED_INSTRUMENTS_CSV.is_file():
            print("error: missing", FILED_INSTRUMENTS_CSV, file=sys.stderr)
            return 1
        with FILED_INSTRUMENTS_CSV.open(encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            fn = list(reader.fieldnames or [])
            if fn != list(FOUNDER_FILED_INSTRUMENTS_FIELDNAMES):
                print(
                    "error: FOUNDER_FILED_INSTRUMENTS.csv header drift vs FOUNDER_FILED_INSTRUMENTS_FIELDNAMES",
                    file=sys.stderr,
                )
                print("  expected:", list(FOUNDER_FILED_INSTRUMENTS_FIELDNAMES), file=sys.stderr)
                print("  got:     ", fn, file=sys.stderr)
                return 1
            fi_rows = [dict(r) for r in reader]
        if args.count_only:
            print(f"source_git_sha={sha}")
            print(f"founder_filed_instruments_rows={len(fi_rows)}")
            return 0
        blocks = _emit_founder_filed_instruments_upserts(fi_rows, sha)
        preamble = [
            "-- Generated by scripts/sync_compliance_mirrors_from_csv.py",
            f"-- source_git_sha: {sha}",
            "-- Apply only after compliance.founder_filed_instruments_mirror exists (Initiative 21 DDL).",
            "",
        ]
        if not args.no_begin_commit:
            preamble.extend(["BEGIN;", ""])
        body = "\n".join(blocks) + "\n"
        ending = ["", "COMMIT;", ""] if not args.no_begin_commit else []
        text = "\n".join(preamble) + body + "\n".join(ending)
        if args.output:
            args.output.write_text(text, encoding="utf-8")
            print("Wrote", args.output, "bytes=", len(text.encode("utf-8")))
        else:
            sys.stdout.write(text)
        return 0

    if args.program_registry_only:
        if not PROGRAM_REGISTRY_CSV.is_file():
            print("error: missing", PROGRAM_REGISTRY_CSV, file=sys.stderr)
            return 1
        with PROGRAM_REGISTRY_CSV.open(encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            fn = list(reader.fieldnames or [])
            if fn != list(PROGRAM_REGISTRY_FIELDNAMES):
                print(
                    "error: PROGRAM_REGISTRY.csv header drift vs PROGRAM_REGISTRY_FIELDNAMES",
                    file=sys.stderr,
                )
                print("  expected:", list(PROGRAM_REGISTRY_FIELDNAMES), file=sys.stderr)
                print("  got:     ", fn, file=sys.stderr)
                return 1
            pr_rows = [dict(r) for r in reader]
        if args.count_only:
            print(f"source_git_sha={sha}")
            print(f"program_registry_rows={len(pr_rows)}")
            return 0
        blocks = _emit_program_registry_upserts(pr_rows, sha)
        preamble = [
            "-- Generated by scripts/sync_compliance_mirrors_from_csv.py",
            f"-- source_git_sha: {sha}",
            "-- Apply only after compliance.program_registry_mirror exists (Initiative 23 DDL).",
            "",
        ]
        if not args.no_begin_commit:
            preamble.extend(["BEGIN;", ""])
        body = "\n".join(blocks) + "\n"
        ending = ["", "COMMIT;", ""] if not args.no_begin_commit else []
        text = "\n".join(preamble) + body + "\n".join(ending)
        if args.output:
            args.output.write_text(text, encoding="utf-8")
            print("Wrote", args.output, "bytes=", len(text.encode("utf-8")))
        else:
            sys.stdout.write(text)
        return 0

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

    finops_n = 0
    finops_rows: list[dict[str, str]] = []
    if FINOPS_CSV.is_file():
        with FINOPS_CSV.open(encoding="utf-8", newline="") as f:
            fr = csv.DictReader(f)
            if list(fr.fieldnames or []) == list(FINOPS_COUNTERPARTY_REGISTER_FIELDNAMES):
                finops_rows = [dict(r) for r in fr]
                finops_n = len(finops_rows)

    goipoi_n = 0
    goipoi_rows: list[dict[str, str]] = []
    if GOIPOI_CSV.is_file():
        with GOIPOI_CSV.open(encoding="utf-8", newline="") as f:
            gr = csv.DictReader(f)
            if list(gr.fieldnames or []) == list(GOIPOI_REGISTER_FIELDNAMES):
                goipoi_rows = [dict(r) for r in gr]
                goipoi_n = len(goipoi_rows)

    ad_n = 0
    ad_rows: list[dict[str, str]] = []
    if ADVISER_DISCIPLINES_CSV.is_file():
        with ADVISER_DISCIPLINES_CSV.open(encoding="utf-8", newline="") as f:
            ar = csv.DictReader(f)
            if list(ar.fieldnames or []) == list(ADVISER_ENGAGEMENT_DISCIPLINES_FIELDNAMES):
                ad_rows = [dict(r) for r in ar]
                ad_n = len(ad_rows)

    aq_n = 0
    aq_rows: list[dict[str, str]] = []
    if ADVISER_QUESTIONS_CSV.is_file():
        with ADVISER_QUESTIONS_CSV.open(encoding="utf-8", newline="") as f:
            qr = csv.DictReader(f)
            if list(qr.fieldnames or []) == list(ADVISER_OPEN_QUESTIONS_FIELDNAMES):
                aq_rows = [dict(r) for r in qr]
                aq_n = len(aq_rows)

    fi_n = 0
    fi_rows: list[dict[str, str]] = []
    if FILED_INSTRUMENTS_CSV.is_file():
        with FILED_INSTRUMENTS_CSV.open(encoding="utf-8", newline="") as f:
            ir = csv.DictReader(f)
            if list(ir.fieldnames or []) == list(FOUNDER_FILED_INSTRUMENTS_FIELDNAMES):
                fi_rows = [dict(r) for r in ir]
                fi_n = len(fi_rows)

    pr_n = 0
    pr_rows: list[dict[str, str]] = []
    if PROGRAM_REGISTRY_CSV.is_file():
        with PROGRAM_REGISTRY_CSV.open(encoding="utf-8", newline="") as f:
            pr_reader = csv.DictReader(f)
            if list(pr_reader.fieldnames or []) == list(PROGRAM_REGISTRY_FIELDNAMES):
                pr_rows = [dict(r) for r in pr_reader]
                pr_n = len(pr_rows)

    if args.count_only:
        print(f"source_git_sha={sha}")
        print(f"process_list_rows={len(proc_rows)}")
        print(f"baseline_organisation_rows={len(org_rows)}")
        print(f"finops_counterparty_register_rows={finops_n}")
        print(f"goipoi_register_rows={goipoi_n}")
        print(f"adviser_engagement_disciplines_rows={ad_n}")
        print(f"adviser_open_questions_rows={aq_n}")
        print(f"founder_filed_instruments_rows={fi_n}")
        print(f"program_registry_rows={pr_n}")
        return 0

    blocks: list[str] = []
    if not args.baseline_only:
        blocks.extend(_emit_process_list_upserts(proc_rows, sha))
    if not args.process_list_only:
        blocks.extend(_emit_baseline_upserts(org_rows, sha))
    if not args.process_list_only and not args.baseline_only and finops_rows:
        blocks.extend(_emit_finops_counterparty_upserts(finops_rows, sha))
    if not args.process_list_only and not args.baseline_only and goipoi_rows:
        blocks.extend(_emit_goipoi_upserts(goipoi_rows, sha))
    if not args.process_list_only and not args.baseline_only and ad_rows:
        blocks.extend(_emit_adviser_disciplines_upserts(ad_rows, sha))
    if not args.process_list_only and not args.baseline_only and aq_rows:
        blocks.extend(_emit_adviser_questions_upserts(aq_rows, sha))
    if not args.process_list_only and not args.baseline_only and fi_rows:
        blocks.extend(_emit_founder_filed_instruments_upserts(fi_rows, sha))
    if not args.process_list_only and not args.baseline_only and pr_rows:
        blocks.extend(_emit_program_registry_upserts(pr_rows, sha))

    preamble = [
        "-- Generated by scripts/sync_compliance_mirrors_from_csv.py",
        f"-- source_git_sha: {sha}",
        "-- Apply only after compliance.process_list_mirror / baseline_organisation_mirror / finops_counterparty_register_mirror exist.",
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
