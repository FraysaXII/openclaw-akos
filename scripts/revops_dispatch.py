"""RevOps process catalog dispatcher (Initiative 72 P8).

Per `D-IH-72-N` (process catalog architecture) + `D-IH-72-Q` (cadence taxonomy:
on_demand | scheduled | event_triggered | gated_operator) + the new Cursor rule
`.cursor/rules/akos-executable-process-catalog.mdc` (SOP + executable runbook
pairing).

Reads ``REVOPS_PROCESS_CATALOG.yaml`` and routes invocation by cadence:
- ``on_demand`` -> CLI args (operator invokes directly)
- ``scheduled`` -> cron pickup (operator/CI invokes per schedule_cron cell)
- ``event_triggered`` -> webhook listener / release-gate hook (operator/system
  invokes when trigger condition fires)
- ``gated_operator`` -> AskQuestion-style ratification gate first (operator
  approves before runbook fires)

Usage:
    py scripts/revops_dispatch.py --list                     # list all processes
    py scripts/revops_dispatch.py --process <id>             # invoke process
    py scripts/revops_dispatch.py --cadence on_demand        # filter by cadence
    py scripts/revops_dispatch.py --aic <aic-id>             # filter by AIC role_owner

Pre-execution discipline (per akos-executable-process-catalog.mdc Rule 1):
- Every process declares both `sop_path` (operator-facing canonical) and
  `runbook_pointer` (executable artifact). The dispatcher logs the SOP path
  before invoking the runbook so the AIC can read the SOP per Rule 1's
  AIC-as-human-equivalent semantics.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml  # PyYAML is in requirements.txt

REPO_ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = (
    REPO_ROOT
    / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1"
    / "Operations" / "RevOps" / "canonicals"
    / "REVOPS_PROCESS_CATALOG.yaml"
)


def load_catalog() -> dict[str, Any]:
    if not CATALOG_PATH.exists():
        print(f"FAIL: catalog not found at {CATALOG_PATH}", file=sys.stderr)
        sys.exit(1)
    with CATALOG_PATH.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def list_processes(catalog: dict[str, Any], cadence_filter: str | None = None,
                   aic_filter: str | None = None) -> int:
    processes = catalog.get("processes", [])
    print()
    print(f"  REVOPS_PROCESS_CATALOG (version {catalog.get('version', '?')})")
    print("  =" * 25)
    for p in processes:
        if cadence_filter and p.get("cadence") != cadence_filter:
            continue
        if aic_filter and p.get("role_owner_aic") != aic_filter:
            continue
        cad = p.get("cadence", "?")
        sched = p.get("schedule_cron", p.get("trigger", "-"))
        ls = p.get("lifecycle_status", "?")
        print(f"  {p['id']:<40} cadence={cad:<16} schedule/trigger={sched:<25} lifecycle={ls}")
        print(f"    SOP:     {p.get('sop_path', '?')}")
        print(f"    Runbook: {p.get('runbook_pointer', '?')}")
        print(f"    AIC:     {p.get('role_owner_aic', '-')}")
        print()
    return 0


def invoke_process(catalog: dict[str, Any], process_id: str) -> int:
    processes = catalog.get("processes", [])
    p = next((x for x in processes if x.get("id") == process_id), None)
    if p is None:
        print(f"FAIL: process {process_id!r} not found in catalog", file=sys.stderr)
        return 1
    print()
    print(f"  Invoking process: {p['id']}")
    print(f"  Cadence: {p['cadence']}")
    print(f"  SOP path (read first per Rule 1 AIC-as-human-equivalent):")
    print(f"    {p.get('sop_path', '?')}")
    print(f"  Runbook pointer:")
    print(f"    {p.get('runbook_pointer', '?')}")
    print(f"  Acceptance criteria (human):")
    print(f"    {p.get('acceptance_criteria_human', '?').strip()}")
    print(f"  Acceptance criteria (automation):")
    print(f"    {p.get('acceptance_criteria_automation', '?').strip()}")
    if p["cadence"] == "gated_operator":
        print()
        print("  GATED_OPERATOR cadence: invoke runbook only after operator approval.")
        print("  This dispatcher logs the contract and exits 0; the runbook is")
        print("  expected to be invoked through an operator-ratification flow")
        print("  (AskQuestion in Cursor; manual operator command in CLI).")
    elif p.get("lifecycle_status") == "scaffold":
        print()
        print("  SCAFFOLD lifecycle_status: runbook not yet wired. Logging contract only.")
        print("  Runbook implementation lands at I72 follow-up or downstream initiative.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="RevOps process catalog dispatcher (I72 P8)")
    parser.add_argument("--list", action="store_true", help="list all catalog entries")
    parser.add_argument("--process", help="invoke a specific process by id")
    parser.add_argument("--cadence", choices=["on_demand", "scheduled", "event_triggered", "gated_operator"],
                        help="filter --list output by cadence")
    parser.add_argument("--aic", help="filter --list output by AIC role_owner")
    args = parser.parse_args()

    catalog = load_catalog()

    if args.list:
        return list_processes(catalog, cadence_filter=args.cadence, aic_filter=args.aic)
    if args.process:
        return invoke_process(catalog, args.process)
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
