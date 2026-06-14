"""Validate SUPABASE_AUTH_REGISTRY.csv (I99 EG-5 / D-IH-99-J)."""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_supabase_auth_registry_csv import (  # noqa: E402
    SUPABASE_AUTH_REGISTRY_FIELDNAMES,
    SupabaseAuthRegistryRow,
)
from pydantic import ValidationError  # noqa: E402

CSV_PATH = REPO_ROOT / (
    "docs/references/hlk/v3.0/Admin/O5-1/Data/Architecture/canonicals/"
    "dimensions/SUPABASE_AUTH_REGISTRY.csv"
)
ORG_CSV = (
    REPO_ROOT
    / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals"
    / "baseline_organisation.csv"
)


def _load_set(path: Path, key: str) -> set[str]:
    with path.open(encoding="utf-8", newline="") as fh:
        return {(r.get(key) or "").strip() for r in csv.DictReader(fh) if (r.get(key) or "").strip()}


def validate_csv() -> tuple[bool, list[str]]:
    errors: list[str] = []
    if not CSV_PATH.is_file():
        return False, [f"missing {CSV_PATH.relative_to(REPO_ROOT)}"]

    roles = _load_set(ORG_CSV, "role_name")

    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if tuple(reader.fieldnames or ()) != SUPABASE_AUTH_REGISTRY_FIELDNAMES:
            return False, ["Header mismatch vs SUPABASE_AUTH_REGISTRY_FIELDNAMES"]
        seen_ids: set[str] = set()
        rows = list(reader)

    for line_no, row in enumerate(rows, start=2):
        rid = row.get("auth_row_id", "")
        if rid in seen_ids:
            errors.append(f"L{line_no}: duplicate auth_row_id {rid!r}")
        seen_ids.add(rid)
        try:
            parsed = SupabaseAuthRegistryRow.model_validate(row)
        except ValidationError as exc:
            errors.append(f"L{line_no}: Pydantic {exc.errors()[0]['msg']}")
            continue
        if parsed.owner_role not in roles:
            errors.append(f"L{line_no}: owner_role {parsed.owner_role!r} not in baseline_organisation")

    ok = not errors
    if ok:
        print(f"PASS: SUPABASE_AUTH_REGISTRY ({len(rows)} rows)")
    else:
        print(f"FAIL: SUPABASE_AUTH_REGISTRY ({len(errors)} error(s))")
        for e in errors:
            print(f"  - {e}")
    return ok, errors


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate Supabase Auth registry")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        row = SupabaseAuthRegistryRow(
            auth_row_id="SUPA-AUTH-99",
            row_kind="provider",
            surface_key="test",
            posture="active",
            owner_role="System Owner",
        )
        assert row.surface_key == "test"
        print("validate_supabase_auth_registry: self-test PASS")
        return 0
    ok, _ = validate_csv()
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
