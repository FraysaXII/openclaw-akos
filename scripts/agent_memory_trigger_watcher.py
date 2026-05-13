#!/usr/bin/env python3
"""Initiative 47 P13 item 3 — Agent memory trigger watcher (D-IH-47-G).

Cron-ready watcher for the I46 P4 AGENT_MEMORY_DEFERRED_ADR triggers. Reads
the 3 trigger condition signals and emits a heads-up report when ANY trigger
fires. Designed to run on a weekly cron (Sunday 09:00 CET); operator
intervention required (script never auto-acts on a fire).

## 3 triggers (per `docs/references/hlk/v3.0/Envoy Tech Lab/Neo4j/AGENT_MEMORY_DEFERRED_ADR.md`)

1. **Multi-tenant load** — SKILL_REGISTRY has any row with tenant_scope != 'shared'
2. **Conversation depth** — >=10% of MADEIRA traces in 7d window with skills_invoked_count >= 4
3. **Compliance ask** — operator forwards an external retrospective audit query
   (cannot be auto-detected; reported as 'awaiting operator input')

## Output

Writes a trigger report to:
``artifacts/agent-memory-triggers/trigger-watch-<UTC-timestamp>.json``

Exit codes:
- 0: no triggers fired
- 1: at least one trigger fired (CI mode opt-in)

Run::

    py scripts/agent_memory_trigger_watcher.py
    py scripts/agent_memory_trigger_watcher.py --hard-fail-on-trigger  # CI-mode
    py scripts/agent_memory_trigger_watcher.py --since-days 14         # custom window
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parent.parent
ARTIFACTS = REPO / "artifacts" / "agent-memory-triggers"
ARTIFACTS.mkdir(parents=True, exist_ok=True)

SKILL_CSV = REPO / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "dimensions" / "SKILL_REGISTRY.csv"


@dataclass
class TriggerStatus:
    """Per-trigger fire state."""

    trigger_id: str
    name: str
    fired: bool
    detail: str
    awaiting_operator: bool = False


def check_multi_tenant_trigger() -> TriggerStatus:
    """Trigger 1: SKILL_REGISTRY has any tenant_scope != 'shared'."""
    if not SKILL_CSV.is_file():
        return TriggerStatus(
            trigger_id="trigger_1_multi_tenant",
            name="Multi-tenant load (Initiative 34 ship)",
            fired=False,
            detail="SKILL_REGISTRY.csv not found; cannot check.",
            awaiting_operator=True,
        )
    with SKILL_CSV.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    non_shared = [
        r for r in rows
        if (r.get("tenant_scope") or "shared").strip() and (r.get("tenant_scope") or "").strip() != "shared"
    ]
    if non_shared:
        ids = [r.get("skill_id", "") for r in non_shared]
        return TriggerStatus(
            trigger_id="trigger_1_multi_tenant",
            name="Multi-tenant load (Initiative 34 ship)",
            fired=True,
            detail=f"{len(non_shared)} skill(s) carry tenant_scope != 'shared': {', '.join(ids)}",
        )
    return TriggerStatus(
        trigger_id="trigger_1_multi_tenant",
        name="Multi-tenant load (Initiative 34 ship)",
        fired=False,
        detail=f"All {len(rows)} skills carry tenant_scope='shared'; I34 not yet shipped.",
    )


def check_conversation_depth_trigger(*, since_days: int = 7, threshold_pct: float = 10.0,
                                     skills_invoked_min: int = 4) -> TriggerStatus:
    """Trigger 2: >=N% of MADEIRA traces in window with skills_invoked >= K.

    Source: ``compliance.eval_run`` mirror (I45 P4 + I47 P10 + I47 P13 item 4).
    Today the mirror is empty (P13 item 4 wires live writes); when populated,
    this query becomes meaningful. Until then, trigger reports 'awaiting data'.
    """
    return TriggerStatus(
        trigger_id="trigger_2_conversation_depth",
        name=f"Conversation depth (>={threshold_pct}% of MADEIRA traces with skills_invoked >= {skills_invoked_min} in {since_days}d)",
        fired=False,
        detail=(
            "compliance.eval_run mirror is the data source. P13 item 4 wires live "
            "writes; until enough MADEIRA traces accumulate (target: 30+ days of "
            "production traffic) this trigger reports awaiting-data. Re-evaluate "
            "after I47 P15 closure + 30 days of operator usage."
        ),
        awaiting_operator=True,
    )


def check_compliance_ask_trigger() -> TriggerStatus:
    """Trigger 3: operator forwards an external retrospective audit query.

    Cannot be auto-detected. Reports 'awaiting operator input'; operator marks
    fired manually by editing ``artifacts/agent-memory-triggers/MANUAL_FIRE.txt``
    (a single-line file with the audit-ask description).
    """
    manual_fire = ARTIFACTS / "MANUAL_FIRE.txt"
    if manual_fire.is_file():
        text = manual_fire.read_text(encoding="utf-8").strip()
        return TriggerStatus(
            trigger_id="trigger_3_compliance_ask",
            name="Compliance ask (external retrospective audit query)",
            fired=True,
            detail=f"Operator marked fired via MANUAL_FIRE.txt: {text[:200]}",
        )
    return TriggerStatus(
        trigger_id="trigger_3_compliance_ask",
        name="Compliance ask (external retrospective audit query)",
        fired=False,
        detail=(
            "Awaiting operator input. To mark fired, write the audit-ask description "
            "to artifacts/agent-memory-triggers/MANUAL_FIRE.txt (single line)."
        ),
        awaiting_operator=True,
    )


def emit_report(statuses: list[TriggerStatus]) -> Path:
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = ARTIFACTS / f"trigger-watch-{ts}.json"
    payload: dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "adr_url": "docs/references/hlk/v3.0/Envoy Tech Lab/Neo4j/AGENT_MEMORY_DEFERRED_ADR.md",
        "triggers": [asdict(s) for s in statuses],
        "any_fired": any(s.fired for s in statuses),
        "any_awaiting": any(s.awaiting_operator for s in statuses),
    }
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="I47 P13 agent memory trigger watcher")
    parser.add_argument(
        "--since-days", type=int, default=7,
        help="Lookback window for trigger 2 (conversation depth); default 7 days",
    )
    parser.add_argument(
        "--threshold-pct", type=float, default=10.0,
        help="Trigger 2 threshold percentage; default 10%%",
    )
    parser.add_argument(
        "--skills-invoked-min", type=int, default=4,
        help="Trigger 2 skills_invoked_count minimum; default 4",
    )
    parser.add_argument(
        "--hard-fail-on-trigger", action="store_true",
        help="Exit non-zero when any trigger fires (CI mode).",
    )
    parser.add_argument("--quiet", action="store_true", help="Suppress per-trigger printing")
    args = parser.parse_args()

    statuses = [
        check_multi_tenant_trigger(),
        check_conversation_depth_trigger(
            since_days=args.since_days,
            threshold_pct=args.threshold_pct,
            skills_invoked_min=args.skills_invoked_min,
        ),
        check_compliance_ask_trigger(),
    ]
    out = emit_report(statuses)

    if not args.quiet:
        print("\n  Agent Memory Trigger Watch (I47 P13 item 3; ADR-46-A reopens on ANY fire)")
        print("  " + "=" * 70)
        for s in statuses:
            tag = "[FIRED]" if s.fired else ("[AWAIT]" if s.awaiting_operator else "[ -- ]")
            print(f"  {tag} {s.trigger_id} - {s.name}")
            print(f"           detail: {s.detail}")
        print(f"\n  Report written: {out}")

    fired = sum(1 for s in statuses if s.fired)
    if fired and args.hard_fail_on_trigger:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
