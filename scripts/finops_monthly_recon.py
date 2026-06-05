#!/usr/bin/env python3
"""Monthly FINOPS reconciliation report (FINANCE-AREA-FULL F3).

Generates a dated recon artefact covering:
- FINOPS counterparty register row count vs M2 floor
- FINOPS-SPINE dataops probe summary
- ``registered_fact`` entity-gate posture (SKIP until ``thi_finan_dtp_306``)

Usage::

    py scripts/finops_monthly_recon.py --report
    py scripts/finops_monthly_recon.py --report --month 2026-06
    py scripts/finops_monthly_recon.py --self-test
"""
from __future__ import annotations

import argparse
import csv
import datetime as _dt
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_dataops_quality import FINOPS_M2_COUNTERPARTY_ROW_FLOOR  # noqa: E402
from scripts.dataops_quality_check import run_sweep  # noqa: E402

REGISTER_CSV = (
    REPO_ROOT
    / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/finops"
    / "FINOPS_COUNTERPARTY_REGISTER.csv"
)
DEFAULT_REPORT_DIR = (
    REPO_ROOT
    / "docs/wip/planning/88-cross-area-ops-wiring-review-discipline/reports"
)


def _counterparty_row_count() -> int:
    if not REGISTER_CSV.is_file():
        return 0
    with REGISTER_CSV.open(encoding="utf-8", newline="") as fh:
        return sum(1 for _ in csv.DictReader(fh))


def _run_script(script: str, *extra: str) -> tuple[int, str]:
    result = subprocess.run(
        [sys.executable, script, *extra],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode, (result.stdout + result.stderr).strip()


def build_report(month: str) -> str:
    today = _dt.date.today().isoformat()
    register_n = _counterparty_row_count()
    m2_pass = register_n >= FINOPS_M2_COUNTERPARTY_ROW_FLOOR

    ledger_rc, ledger_out = _run_script("scripts/validate_finops_ledger.py")
    spine = run_sweep("mirror_table", data_fam="FINOPS-SPINE")
    spine_lines = "\n".join(
        f"| {row.dimension_code} | {row.verdict} | {row.notes[:80]} |"
        for row in spine.findings
    )

    m2_verdict = "PASS" if m2_pass else "FAIL"
    ledger_verdict = "PASS" if ledger_rc == 0 else "FAIL"
    spine_verdict = "PASS" if spine.gap_count == 0 else "FAIL"

    return f"""---
report_kind: finops_monthly_recon
month: {month}
authored: {today}
program: FINANCE-AREA-FULL
phase: F3
entity_gate_process: thi_finan_dtp_306
registered_fact_verdict: SKIP
---

# FINOPS monthly recon — {month}

## Summary

| Check | Evidence | Verdict |
|:---|:---|:---|
| Counterparty register rows | {register_n} (floor {FINOPS_M2_COUNTERPARTY_ROW_FLOOR}) | {m2_verdict} |
| `validate_finops_ledger.py` | rc={ledger_rc} | {ledger_verdict} |
| FINOPS-SPINE dataops sweep | clean={spine.clean_count} gap={spine.gap_count} | {spine_verdict} |
| `finops.registered_fact` live rows | entity gate open | SKIP |

## FINOPS-SPINE probes

| Dimension | Verdict | Notes |
|:---|:---|:---|
{spine_lines}

## Entity gate (M3 partial)

Production monetary facts in `finops.registered_fact` are **deferred** until
entity readiness process `thi_finan_dtp_306` closes. Synthetic validator coverage
via `validate_finops_ledger.py` remains the git SSOT check at F3.

## Mirror apply (operator SQL gate)

Generate DML with:

```powershell
py scripts/sync_compliance_mirrors_from_csv.py --finops-counterparty-register-only --output docs/wip/planning/88-cross-area-ops-wiring-review-discipline/artifacts/finops-counterparty-mirror-upsert.sql
```

Apply per `akos-holistika-operations.mdc` after operator approval.

## Validator excerpt

```
{ledger_out[:1200]}
```
"""


def run_self_test() -> int:
    report = build_report("self-test")
    if "FINOPS-SPINE" not in report or "SKIP" not in report:
        print("FAIL: report missing expected sections")
        return 1
    if _counterparty_row_count() < FINOPS_M2_COUNTERPARTY_ROW_FLOOR:
        print("FAIL: counterparty register below M2 floor")
        return 1
    print("PASS (self-test)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--report", action="store_true", help="Write monthly recon markdown")
    parser.add_argument("--month", default=_dt.date.today().strftime("%Y-%m"))
    parser.add_argument("--stdout", action="store_true", help="Print report instead of writing file")
    args = parser.parse_args()

    if args.self_test:
        return run_self_test()

    if args.report:
        body = build_report(args.month)
        if args.stdout:
            print(body)
            return 0
        DEFAULT_REPORT_DIR.mkdir(parents=True, exist_ok=True)
        out_path = DEFAULT_REPORT_DIR / f"finops-recon-{args.month}.md"
        out_path.write_text(body, encoding="utf-8")
        print(f"Wrote {out_path.relative_to(REPO_ROOT)}")
        return 0

    print("INFO: use --report or --self-test")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
