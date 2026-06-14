"""Draft reconcile: compare live Vercel/Cloudflare/GitHub probes against registry SSOT.

Companion to SOP-LAB_COMPONENT_REGISTRY_MAINTENANCE_001 (AC-AUTOMATION). Read-only by default;
prints diff lines for operator review — does not mutate registries.

Usage:
  py scripts/lab_platform_registry_reconcile.py [--dry-run]
  py scripts/lab_platform_registry_reconcile.py --self-test
"""
from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
VERCEL_REG = (
    REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "Tech"
    / "System Owner" / "canonicals" / "dimensions" / "VERCEL_PROJECT_SETTINGS_REGISTRY.csv"
)


def _load_vercel_rows() -> list[dict[str, str]]:
    with VERCEL_REG.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _vercel_cli_available() -> bool:
    try:
        subprocess.run(
            ["vercel", "--version"],
            capture_output=True,
            check=False,
            timeout=10,
        )
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def reconcile_vercel(dry_run: bool = True) -> list[str]:
    findings: list[str] = []
    rows = _load_vercel_rows()
    if not _vercel_cli_available():
        findings.append("SKIP: vercel CLI not available — registry-only mode")
        for row in rows:
            findings.append(
                f"REGISTRY {row['setting_id']}: expected={row['expected_value'][:60]}…"
            )
        return findings
    for row in rows:
        if row["project_slug"] != "hlk-erp":
            continue
        findings.append(
            f"PROBE {row['setting_id']}: run `{row['probe_command']}` and compare to registry"
        )
    if dry_run:
        findings.append("DRY-RUN: no registry writes")
    return findings


def self_test() -> int:
    rows = _load_vercel_rows()
    if len(rows) < 6:
        print("expected >= 6 Vercel registry rows", file=sys.stderr)
        return 1
    print(f"self-test OK ({len(rows)} Vercel rows loaded)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", default=True)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    findings = reconcile_vercel(dry_run=True)
    print(json.dumps({"findings": findings}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
