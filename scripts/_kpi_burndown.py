"""One-shot KPI burndown report for I86 cluster + portfolio.

Not a governed validator. Read-only aggregator over INITIATIVE_REGISTRY +
DECISION_REGISTER + OPS_REGISTER + I86 master-roadmap §1.3 cluster siblings.
Delete after operator review.
"""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CANON = ROOT / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals"

# I86 cluster siblings per cluster-burndown-plan.md §3 (13 coordinated initiatives;
# expanded from the original master-roadmap §1.3 list of 10 to include I79 + I80
# + I89 which entered the cluster mid-burn).
CLUSTER = [
    "I74", "I75", "I76", "I78", "I79", "I80", "I81",
    "I82", "I83", "I84", "I85", "I87", "I89",
]

# Per cluster-burndown-plan §3 (2026-05-19 snapshot) — active siblings whose
# remaining-phase count we report.
ACTIVE_PHASES_REMAINING = {
    "I76": (1, 7, "P0 closed; P1..P6 pending"),
    "I81": (1, 10, "P0 closed; P1..P9 pending"),
    "I82": (1, 8, "P0 in_progress; P1..P7 pending"),
    "I89": (1, 6, "P0 in_progress; P1..P5 pending"),
    # I78 was active per the plan; registry now shows closed — confirm before report.
}


def load_csv(name: str) -> list[dict]:
    p = CANON / name
    with p.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def histo(rows: list[dict], key: str) -> Counter:
    return Counter(r.get(key, "") for r in rows)


def section(title: str) -> None:
    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


def main() -> None:
    inits = load_csv("INITIATIVE_REGISTRY.csv")
    decs = load_csv("DECISION_REGISTER.csv")
    ops = load_csv("OPS_REGISTER.csv")

    section("PORTFOLIO INITIATIVES (INITIATIVE_REGISTRY.csv)")
    total = len(inits)
    print(f"total rows: {total}")
    for s, n in histo(inits, "status").most_common():
        pct = n / total * 100
        print(f"  {s:25} {n:4d}  ({pct:5.1f}%)")

    section("I86 CLUSTER — 13 coordinated siblings (per cluster-burndown-plan §3)")
    by_id = {
        r["initiative_id"].replace("INIT-OPENCLAW_AKOS-", "I"): r for r in inits
    }
    rows_in = 0
    for k in CLUSTER:
        r = by_id.get(k)
        if r is None:
            print(f"  {k:5}  (not in INITIATIVE_REGISTRY — candidate/blocker-tracker)")
        else:
            rows_in += 1
            print(f"  {k:5}  {r['status']:18}  {r['title'][:70]}")
    print()
    closed = sum(1 for k in CLUSTER if k in by_id and by_id[k]["status"] == "closed")
    active = sum(
        1
        for k in CLUSTER
        if k in by_id and by_id[k]["status"] in ("active", "in_progress")
    )
    bt = sum(1 for k in CLUSTER if k not in by_id)
    n = len(CLUSTER)
    print(f"  CLOSED:           {closed} / {n}  ({closed / n * 100:.1f}%)")
    print(f"  ACTIVE:           {active} / {n}  ({active / n * 100:.1f}%)")
    print(f"  BLOCKER-TRACKER:  {bt} / {n}  ({bt / n * 100:.1f}%)")
    print()
    print(f"  >>> CLUSTER BURNDOWN: {closed}/{n} closed = {closed / n * 100:.1f}%")
    print(f"  >>> CLUSTER REMAINING: {n - closed}/{n} = {(n - closed) / n * 100:.1f}%")
    print()
    print("Phase-level burndown (active siblings; phases declared in cluster-burndown-plan §3):")
    tot_closed = 0
    tot_total = 0
    for k, (cl, tot, note) in ACTIVE_PHASES_REMAINING.items():
        rstatus = by_id.get(k, {}).get("status", "?")
        if rstatus == "closed":
            cl = tot  # if registry says closed, treat all phases done
        rem = tot - cl
        tot_closed += cl
        tot_total += tot
        print(f"  {k:5} {rstatus:10} {cl}/{tot} phases done ({cl / tot * 100:.0f}%); remaining={rem}; {note}")
    print(f"  TOTAL active-sibling phases: {tot_closed}/{tot_total} = {tot_closed / tot_total * 100:.1f}% done")

    section("OPS_REGISTER (forward-charters + follow-ups)")
    print(f"total rows: {len(ops)}")
    for s, n in histo(ops, "status").most_common():
        pct = n / len(ops) * 100
        print(f"  {s:15} {n:4d}  ({pct:5.1f}%)")
    print()
    # OPS originated by I86 (ops_action_id like OPS-86-N)
    i86_ops = [r for r in ops if r["ops_action_id"].startswith("OPS-86-")]
    print(f"I86-originated OPS rows: {len(i86_ops)}")
    for s, n in histo(i86_ops, "status").most_common():
        pct = n / max(len(i86_ops), 1) * 100
        print(f"  {s:15} {n:3d}  ({pct:5.1f}%)")
    print()
    print("Open OPS rows (next 25 by id):")
    opens = sorted([r for r in ops if r["status"] == "open"], key=lambda x: x["ops_action_id"])
    for r in opens[:25]:
        oid = r["ops_action_id"]
        owner = (r.get("owner_role") or "")[:20]
        title = (r.get("title") or "")[:55]
        print(f"  {oid:18}  {owner:20}  {title}")

    section("DECISION_REGISTER (ratification ledger)")
    print(f"total rows: {len(decs)}")
    for s, n in histo(decs, "status").most_common():
        pct = n / len(decs) * 100
        print(f"  {s:25} {n:4d}  ({pct:5.1f}%)")
    print()
    d86 = [r for r in decs if r["decision_id"].startswith("D-IH-86-")]
    print(f"D-IH-86-* decisions: {len(d86)}")
    for s, n in histo(d86, "status").most_common():
        pct = n / max(len(d86), 1) * 100
        print(f"  {s:25} {n:3d}  ({pct:5.1f}%)")
    print()
    print("Latest 12 D-IH-86-* decisions by decided_at:")
    d86s = sorted(d86, key=lambda x: x.get("decided_at", ""), reverse=True)[:12]
    for r in d86s:
        did = r["decision_id"]
        d = r.get("decided_at", "")
        st = r["status"]
        t = (r.get("title") or "")[:65]
        print(f"  {did:20} {d:12} {st:18} {t}")

    section("HEADLINE BURNDOWN KPIs")
    print(f"  I86 cluster:          {closed}/10 closed  ({closed * 10:>3}%)")
    print(f"  Portfolio active:     {histo(inits, 'status').get('active', 0)} / {total}")
    closed_total = histo(inits, "status").get("closed", 0)
    print(
        f"  Portfolio closed:     {closed_total} / {total}  ({closed_total / total * 100:.1f}%)"
    )
    open_ops = histo(ops, "status").get("open", 0)
    print(
        f"  OPS open backlog:     {open_ops} / {len(ops)}  ({open_ops / len(ops) * 100:.1f}%)"
    )
    i86_open = sum(1 for r in i86_ops if r["status"] == "open")
    print(
        f"  I86 OPS open:         {i86_open} / {len(i86_ops)}  ("
        f"{i86_open / max(len(i86_ops), 1) * 100:.1f}%)"
    )
    superseded = histo(decs, "status").get("superseded", 0)
    print(
        f"  Decisions superseded: {superseded} / {len(decs)}  ({superseded / len(decs) * 100:.1f}%)"
    )


if __name__ == "__main__":
    main()
