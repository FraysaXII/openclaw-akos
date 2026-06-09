"""Validate SUPABASE_EXTENSION_MANIFEST.md (I95 EG-3 / D-IH-95-G).

Lightweight structural checks: file exists, required module IDs present,
linked cron registry on disk.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

MANIFEST_PATH = REPO_ROOT / (
    "docs/references/hlk/v3.0/Admin/O5-1/Data/Architecture/canonicals/"
    "SUPABASE_EXTENSION_MANIFEST.md"
)
CRON_CSV = REPO_ROOT / (
    "docs/references/hlk/v3.0/Admin/O5-1/Data/Architecture/canonicals/"
    "dimensions/SUPABASE_CRON_REGISTRY.csv"
)
MODULE_CSV = REPO_ROOT / (
    "docs/references/hlk/v3.0/Admin/O5-1/Data/Architecture/canonicals/"
    "dimensions/SUPABASE_MODULE_REGISTRY.csv"
)

REQUIRED_MODULE_IDS = frozenset({
    "SUPA-MOD-13",
    "SUPA-MOD-14",
    "SUPA-MOD-15",
})

REQUIRED_EXTENSIONS = frozenset({
    "pgmq",
    "pg_cron",
    "pg_net",
})


def validate_manifest() -> tuple[bool, list[str]]:
    errors: list[str] = []
    if not MANIFEST_PATH.is_file():
        return False, [f"missing {MANIFEST_PATH.relative_to(REPO_ROOT)}"]
    if not CRON_CSV.is_file():
        errors.append("SUPABASE_CRON_REGISTRY.csv missing (linked from manifest)")
    if not MODULE_CSV.is_file():
        errors.append("SUPABASE_MODULE_REGISTRY.csv missing")

    text = MANIFEST_PATH.read_text(encoding="utf-8")
    if "SUPABASE_ECOSYSTEM_GOVERNANCE.md" not in text:
        errors.append("linked_canonicals missing SUPABASE_ECOSYSTEM_GOVERNANCE.md reference")
    for mid in REQUIRED_MODULE_IDS:
        if mid not in text:
            errors.append(f"§2 matrix missing module id {mid}")
    for ext in REQUIRED_EXTENSIONS:
        if f"`{ext}`" not in text:
            errors.append(f"§2 matrix missing extension `{ext}`")
    if not re.search(r"^## 2\. Extension matrix", text, re.MULTILINE):
        errors.append("missing ## 2. Extension matrix section")

    ok = not errors
    if ok:
        print("PASS: SUPABASE_EXTENSION_MANIFEST (structural checks)")
    else:
        print(f"FAIL: SUPABASE_EXTENSION_MANIFEST ({len(errors)} error(s))")
        for e in errors:
            print(f"  - {e}")
    return ok, errors


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate Supabase extension manifest")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        assert "pgmq" in REQUIRED_EXTENSIONS
        print("validate_supabase_extension_manifest: self-test PASS")
        return 0
    ok, _ = validate_manifest()
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
