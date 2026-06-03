---
intellectual_kind: decision_brief
ops_id: OPS-86-1
initiative_id: INIT-OPENCLAW_AKOS-86
parent_initiative: INIT-OPENCLAW_AKOS-90
authored: 2026-06-01
status: pending_operator
linked_decisions:
  - D-IH-86-A
  - D-IH-86-B
  - D-IH-90-L
linked_packet: ../composer-packets/packet-ops-86-1-cluster-closure.md
language: en
---

# Decision brief — OPS-86-1 (I86 cluster closure strategy)

## Question

How does the I86 cluster coordinator close without re-opening completed brand-domain work (`D-IH-86-FK`) while the nine-sibling burndown still has open OPS rows?

## Evidence

- [`86-initiative-cluster-execution-coordinator/master-roadmap.md`](../../86-initiative-cluster-execution-coordinator/master-roadmap.md) — sibling table + wave cadence.
- [`OPS_REGISTER.csv`](../../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/OPS_REGISTER.csv) row **OPS-86-1** — `open`, PMO owner, inception D-IH-86-A..E.
- I90 P0 closed OPS-86-3/16/17; P3.5 closed OPS-90-* routing ordnance — cluster mechanical debt now concentrates in P3b/P3c execution, not re-charter.

## Options

| Option | Summary | Tradeoff |
|:---|:---|:---|
| **A — Wave-close bundle** | Close I86 when I90 P3d + I91 Phase F + I92 P1 UAT evidence land; OPS-86-1 flips `closed` in same commit as coordinator UAT. | Clean narrative; waits on I91/I92. |
| **B — OPS-only closure** | Close OPS-86-1 when all `OPS-86-*` rows are `closed` or explicitly `parked` (24/25); INITIATIVE_REGISTRY I86 stays `active` until sibling INIT rows close. | Separates coordination row from initiative lifecycle. |
| **C — Split coordinator** | Mint I90 as permanent “ordnance” owner; demote I86 to historical archive at next wave U. | More registry churn; matches two-seat routing doctrine. |

## Recommendation (agent default)

**Option B** — OPS-86-1 closes when the OPS backlog table in [`p3a-gate-clearance-2026-06-01.md`](../p3a-gate-clearance-2026-06-01.md) shows every P3a–P3d row either executed, parked with tracker path, or forward-chartered with decision ID. I86 `INIT` status flip remains gated on cluster UAT per Option A’s evidence rows.

## Execution seat

Composer does **not** edit INITIATIVE_REGISTRY for I86 in P3b — only after operator ratifies this brief and P3d cluster UAT is drafted.

## Ratification target

`D-IH-90-Z` (proposed) or append rationale to **D-IH-86-A** amendment row at I86 wave-close.
