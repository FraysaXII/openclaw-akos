---
name: Operations Delivery Craft
description: >-
  Use when executing Operations area delivery work — PMO/RevOps/SMO/Engagement
  SOP pairing, PMBOK domain mapping, automation-first tranches, area-completeness
  tier gates, or I94 operational sweep packets. Codifies the HOW of Operations
  delivery per OPERATIONS_DELIVERY_DOCTRINE. Triggers on Operations delivery,
  PMO inbox/WIP, cohesion render, RevOps dispatch, AREA-03, I94 P3 ops sweep,
  automation-first pairing. Pairs with akos-operations-delivery.mdc (WHEN); this
  skill is HOW.
---

# Operations Delivery Craft

## Principle 1 — Cite thinking synthesis first

Before any P2+ tranche, read upstream SSOT:

`docs/wip/planning/94-area-architecture-and-completeness-v2/reports/i94-operations-operational-sweep-thinking-synthesis-2026-06-10.md`

Charter and doctrine must align with operator ratification (Q1=B, automation-first,
6–8h/day).

## Principle 2 — Worklist over matrix

```powershell
py scripts/validate_area_completeness.py --area Operations --next
```

Work top-down: AREA-03 (doctrine) → AREA-02 (charter) → AREA-11/13 → AREA-09 pairing.

## Principle 3 — Automation-first pairing stack

| Priority | Process family | Runbook |
|:---|:---|:---|
| 1 | WIP dashboard | `scripts/render_wip_dashboard.py` |
| 2 | Operator inbox | `scripts/render_operator_inbox.py` |
| 3 | Cohesion index | `scripts/render_operational_cohesion_index.py` |
| 4 | Mirror emit | `scripts/sync_compliance_mirrors_from_csv.py` / verify profile |
| 5 | Area completeness | `scripts/validate_area_completeness.py` |
| 6 | Engagement scaffold | `scripts/scaffold_engagement.py` |
| 7 | RevOps dispatch | `scripts/revops_dispatch.py` |

Pair SOP frontmatter `linked_runbooks:` before claiming AREA-09 progress.

## Principle 4 — PMBOK domain declaration

Each new or revised Operations SOP states which PMBOK 7 domain it serves (see
`OPERATIONS_DELIVERY_DISCIPLINE.md` §2). Project/service tag in process metadata, not
folder splits.

## Principle 5 — Gates before moves

- No IntelligenceOps file moves without P3 inline-ratify.
- No `process_list.csv` / `baseline_organisation.csv` without operator approval.
- Mirror live apply = operator SQL gate; repo emit alone is not PASS.

## Verification stack (P0–P1 minimum)

```powershell
py scripts/validate_research_action.py
py scripts/validate_hlk.py
py scripts/validate_area_completeness.py --area Operations --next
py scripts/verify.py pre_commit_fast
```

## Anti-patterns

- Minting more PMO strategy markdown instead of pairing runbooks.
- Scoring IntelligenceOps as Operations delivery.
- Claiming AREA-09 closure on 0/46 pairing.
- Forking mirror/sync scripts instead of extending existing runbooks.

## Cross-references

- [`OPERATIONS_DELIVERY_DISCIPLINE.md`](../../docs/references/hlk/v3.0/Admin/O5-1/Operations/OPERATIONS_DELIVERY_DISCIPLINE.md)
- [`OPERATIONS_AREA_CHARTER.md`](../../docs/references/hlk/v3.0/Admin/O5-1/Operations/OPERATIONS_AREA_CHARTER.md)
- [`i94-operations-operational-sweep-charter-2026-06-10.md`](../../docs/wip/planning/94-area-architecture-and-completeness-v2/reports/i94-operations-operational-sweep-charter-2026-06-10.md)
