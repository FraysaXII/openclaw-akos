"""Validate SUPABASE_CRON_REGISTRY.csv (I95 EG-3 / D-IH-95-G).

Checks schema + migration_ref exists + target_function_slug in edge registry.
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_supabase_cron_registry_csv import (  # noqa: E402
    SUPABASE_CRON_REGISTRY_FIELDNAMES,
    SupabaseCronRegistryRow,
)
from akos.hlk_supabase_edge_function_registry_csv import (  # noqa: E402
    SUPABASE_EDGE_FUNCTION_REGISTRY_FIELDNAMES,
)
from pydantic import ValidationError  # noqa: E402

CSV_PATH = REPO_ROOT / (
    "docs/references/hlk/v3.0/Admin/O5-1/Data/Architecture/canonicals/"
    "dimensions/SUPABASE_CRON_REGISTRY.csv"
)
EDGE_CSV = REPO_ROOT / (
    "docs/references/hlk/v3.0/Admin/O5-1/Data/Architecture/canonicals/"
    "dimensions/SUPABASE_EDGE_FUNCTION_REGISTRY.csv"
)
ORG_CSV = (
    REPO_ROOT
    / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals"
    / "baseline_organisation.csv"
)


def _load_set(path: Path, key: str) -> set[str]:
    with path.open(encoding="utf-8", newline="") as fh:
        return {(r.get(key) or "").strip() for r in csv.DictReader(fh) if (r.get(key) or "").strip()}


def _edge_slugs() -> set[str]:
    if not EDGE_CSV.is_file():
        return set()
    with EDGE_CSV.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if tuple(reader.fieldnames or ()) != SUPABASE_EDGE_FUNCTION_REGISTRY_FIELDNAMES:
            return set()
        return {(r.get("function_slug") or "").strip() for r in reader if (r.get("function_slug") or "").strip()}


def validate_csv() -> tuple[bool, list[str]]:
    errors: list[str] = []
    if not CSV_PATH.is_file():
        return False, [f"missing {CSV_PATH.relative_to(REPO_ROOT)}"]

    roles = _load_set(ORG_CSV, "role_name")
    edge_slugs = _edge_slugs()

    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if tuple(reader.fieldnames or ()) != SUPABASE_CRON_REGISTRY_FIELDNAMES:
            return False, ["Header mismatch vs SUPABASE_CRON_REGISTRY_FIELDNAMES"]
        seen_ids: set[str] = set()
        seen_names: set[str] = set()
        rows = list(reader)

    for line_no, row in enumerate(rows, start=2):
        jid = row.get("job_id", "")
        jname = row.get("job_name", "")
        if jid in seen_ids:
            errors.append(f"L{line_no}: duplicate job_id {jid!r}")
        seen_ids.add(jid)
        if jname in seen_names:
            errors.append(f"L{line_no}: duplicate job_name {jname!r}")
        seen_names.add(jname)
        try:
            parsed = SupabaseCronRegistryRow.model_validate(row)
        except ValidationError as exc:
            errors.append(f"L{line_no}: Pydantic {exc.errors()[0]['msg']}")
            continue
        if parsed.owner_role not in roles:
            errors.append(f"L{line_no}: owner_role {parsed.owner_role!r} not in baseline_organisation")
        mig = REPO_ROOT / parsed.migration_ref
        if not mig.is_file():
            errors.append(f"L{line_no}: missing migration {parsed.migration_ref}")
        if edge_slugs and parsed.target_function_slug not in edge_slugs:
            errors.append(
                f"L{line_no}: target_function_slug {parsed.target_function_slug!r} "
                "not in SUPABASE_EDGE_FUNCTION_REGISTRY"
            )

    ok = not errors
    if ok:
        print(f"PASS: SUPABASE_CRON_REGISTRY ({len(rows)} jobs)")
    else:
        print(f"FAIL: SUPABASE_CRON_REGISTRY ({len(errors)} error(s))")
        for e in errors:
            print(f"  - {e}")
    return ok, errors


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate Supabase cron registry")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        row = SupabaseCronRegistryRow(
            job_id="SUPA-CR-99",
            job_name="test_job",
            schedule_cron="0 * * * *",
            target_function_slug="test-fn",
            migration_ref="supabase/migrations/README.md",
            auth_pattern="none",
            owner_role="System Owner",
            status="active",
        )
        assert row.job_name == "test_job"
        print("validate_supabase_cron_registry: self-test PASS")
        return 0
    ok, _ = validate_csv()
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
