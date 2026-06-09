"""Validate SUPABASE_EDGE_FUNCTION_REGISTRY.csv (I95 EG-3 / D-IH-95-G).

Checks schema + repo_path exists under supabase/functions/.
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_supabase_edge_function_registry_csv import (  # noqa: E402
    SUPABASE_EDGE_FUNCTION_REGISTRY_FIELDNAMES,
    SupabaseEdgeFunctionRegistryRow,
)
from pydantic import ValidationError  # noqa: E402

CSV_PATH = REPO_ROOT / (
    "docs/references/hlk/v3.0/Admin/O5-1/Data/Architecture/canonicals/"
    "dimensions/SUPABASE_EDGE_FUNCTION_REGISTRY.csv"
)
ORG_CSV = (
    REPO_ROOT
    / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals"
    / "baseline_organisation.csv"
)
RPA_CSV = (
    REPO_ROOT
    / "docs/references/hlk/v3.0/Admin/O5-1/Data/Governance/canonicals"
    / "dimensions/RPA_ADAPTER_REGISTRY.csv"
)


def _load_set(path: Path, key: str) -> set[str]:
    with path.open(encoding="utf-8", newline="") as fh:
        return {(r.get(key) or "").strip() for r in csv.DictReader(fh) if (r.get(key) or "").strip()}


def validate_csv() -> tuple[bool, list[str]]:
    errors: list[str] = []
    if not CSV_PATH.is_file():
        return False, [f"missing {CSV_PATH.relative_to(REPO_ROOT)}"]

    roles = _load_set(ORG_CSV, "role_name")
    adapters = _load_set(RPA_CSV, "adapter_id")

    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if tuple(reader.fieldnames or ()) != SUPABASE_EDGE_FUNCTION_REGISTRY_FIELDNAMES:
            return False, ["Header mismatch vs SUPABASE_EDGE_FUNCTION_REGISTRY_FIELDNAMES"]
        seen_ids: set[str] = set()
        seen_slugs: set[str] = set()
        rows = list(reader)

    for line_no, row in enumerate(rows, start=2):
        fid = row.get("function_id", "")
        slug = row.get("function_slug", "")
        if fid in seen_ids:
            errors.append(f"L{line_no}: duplicate function_id {fid!r}")
        seen_ids.add(fid)
        if slug in seen_slugs:
            errors.append(f"L{line_no}: duplicate function_slug {slug!r}")
        seen_slugs.add(slug)
        try:
            parsed = SupabaseEdgeFunctionRegistryRow.model_validate(row)
        except ValidationError as exc:
            errors.append(f"L{line_no}: Pydantic {exc.errors()[0]['msg']}")
            continue
        if parsed.owner_role not in roles:
            errors.append(f"L{line_no}: owner_role {parsed.owner_role!r} not in baseline_organisation")
        if parsed.rpa_adapter_id and parsed.rpa_adapter_id not in adapters:
            errors.append(f"L{line_no}: rpa_adapter_id {parsed.rpa_adapter_id!r} not in RPA_ADAPTER_REGISTRY")
        fn_dir = REPO_ROOT / "supabase" / "functions" / parsed.function_slug
        if not fn_dir.is_dir():
            errors.append(f"L{line_no}: missing function directory {fn_dir.relative_to(REPO_ROOT)}")

    ok = not errors
    if ok:
        print(f"PASS: SUPABASE_EDGE_FUNCTION_REGISTRY ({len(rows)} functions)")
    else:
        print(f"FAIL: SUPABASE_EDGE_FUNCTION_REGISTRY ({len(errors)} error(s))")
        for e in errors:
            print(f"  - {e}")
    return ok, errors


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate Supabase edge-function registry")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        row = SupabaseEdgeFunctionRegistryRow(
            function_id="SUPA-EF-99",
            function_slug="test-fn",
            repo_path="supabase/functions/test-fn/",
            invoke_pattern="manual",
            verify_jwt="true",
            owner_role="System Owner",
            status="forward",
        )
        assert row.function_slug == "test-fn"
        print("validate_supabase_edge_function_registry: self-test PASS")
        return 0
    ok, _ = validate_csv()
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
