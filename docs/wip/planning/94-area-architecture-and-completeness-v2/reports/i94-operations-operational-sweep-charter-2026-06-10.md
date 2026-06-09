---
parent_initiative: INIT-OPENCLAW_AKOS-94
authored: 2026-06-10
phase: P0-P6
upstream_ssot: i94-operations-operational-sweep-thinking-synthesis-2026-06-10.md
ratifying_decisions:
  - D-IH-94-A
operator_ratification:
  q1_scope: B_full_sweep
  q2_priority: automation-first
  q3_capacity: 6-8h_per_day_until_gtm
linked_decisions:
  - D-IH-94-A
---

# I94 Operations operational sweep charter (2026-06-10)

> **Upstream SSOT:** [`i94-operations-operational-sweep-thinking-synthesis-2026-06-10.md`](i94-operations-operational-sweep-thinking-synthesis-2026-06-10.md)
> (thinking-seat `c4097ca4`). This charter **expands** Step 4 of that synthesis;
> it does not replace it.

Operator ratification (binding): **Q1=B Full sweep** | **Q2=automation-first** |
**Q3=6–8h/day until GTM**.

## 1. Mission

Deliver an Operations area that **executes** Holistika's delivery spine — PMO
program cadence, RevOps value-mapping, SMO service rhythm, Engagement client
delivery — with enough automation that a solo operator + AIC pair runs programs
without touching ops mechanics. Target: **crit@L3 10/10** on area-completeness
matrix (from 9/10 at sweep start).

## 2. Phase dependency

```mermaid
flowchart LR
  P0[P0 Research] --> P1[P1 Doctrine]
  P1 --> P2[P2 Exec catalog T1]
  P2 --> P3[P3 Placement]
  P3 --> P4[P4 Cross-area handoffs]
  P4 --> P5[P5 I88 Ops slice]
  P5 --> P6[P6 Regression UAT]
```

## 3. Phased execution

### P0 — Research (this commit)

| Deliverable | Path |
|:---|:---|
| Thinking synthesis SSOT | `i94-operations-operational-sweep-thinking-synthesis-2026-06-10.md` |
| Source ledger (≥120+120) | `i94-operations-area-source-ledger.csv` |
| Research synthesis | `i94-operations-area-research-synthesis-2026-06-10.md` |
| This charter | `i94-operations-operational-sweep-charter-2026-06-10.md` |
| Session doctrine | `i94-p3-session-doctrine-2026-06-10.md` |

Verification: `py scripts/validate_research_action.py` (ledger schema).

### P1 — Doctrine mint (this commit)

| Deliverable | Path | AREA component |
|:---|:---|:---:|
| Operations area charter | `Operations/OPERATIONS_AREA_CHARTER.md` | AREA-02 |
| Delivery doctrine (PMBOK 7) | `Operations/OPERATIONS_DELIVERY_DOCTRINE.md` | AREA-03 |
| Area README | `Operations/README.md` | AREA-13 |
| Cursor rule | `.cursor/rules/akos-operations-delivery.mdc` | AREA-11 |
| Paired skill | `.cursor/skills/operations-delivery-craft/SKILL.md` | AREA-11 |
| PRECEDENCE rows | `PRECEDENCE.md` | AREA-07 |

Gate: operator doctrine review (`D-IH-94-C` reserved). No `process_list.csv` edits.

### P2 — Executable catalog T1 (automation-first)

Pair **12 critical** SOP+runbook processes (no new `item_id`s unless pairing requires):

1. PMO WIP dashboard render
2. PMO operator inbox render
3. Operational cohesion index render
4. Initiative program anchor backfill
5. External adviser engagement router
6. Engagement scaffold (RevOps)
7. Compliance mirror emit trigger
8. Area completeness sweep (`--area Operations --next`)
9. Initiative governance harmonisation
10. Vault promotion gate
11. RevOps QBR cadence
12. Service catalog maintenance (SMO)

Wire new runbook steps into `config/verification-profiles.json` where applicable.
AREA-09 enhancing — not closure-blocking alone.

### P3 — Placement (operator gate)

| Action | Gate |
|:---|:---|
| IntelligenceOps SOPs → Research area | File-move + inline-ratify |
| Engagement subfolder FK to baseline roster | AREA-16 remediation |
| business-strategy forward tracker (I95 L6) | Scope-overlap tracker; no moves in P3 without ratification |

### P4 — Cross-area handoffs

Document execution contracts (register-only tranche):

- **Data:** mirror emit / two-plane apply (`akos-holistika-operations.mdc`)
- **People:** compliance CSV gates / methodology enforcement
- **Finance:** FINOPS bridge SOP + registered_fact entity gate
- **Tech:** CICD baseline + deploy-health Step 0 fleet hygiene

### P5 — I88 deep slice

Operations 10-pillar wiring review report under I88 initiative folder;
`on_demand` + scheduled cadence per executable process catalog.

### P6 — Regression + UAT

| Gate | Command |
|:---|:---|
| Area tier | `py scripts/validate_area_completeness.py --area Operations --matrix` |
| Worklist | `py scripts/validate_area_completeness.py --area Operations --next` |
| HLK | `py scripts/validate_hlk.py` |
| Fast CI | `py scripts/verify.py pre_commit_fast` |

Optional PASS-WITH-FOLLOWUP on AREA-09 pairing cliff if 12/46 paired at P2.

## 4. 16-component target matrix

See thinking synthesis Step 4 for current→target table. P1 closes AREA-02/03/11/13
gaps; P2 lifts AREA-09; P3 closes AREA-15/16; P6 confirms crit@L3 10/10.

## 5. Cross-initiative links

| INIT | Link |
|:---|:---|
| I94 | Parent — area completeness v2 |
| I88 | P5 Operations 10-pillar slice |
| I89 | ERP panels consume cohesion routing |
| I93 | Mirror + component matrix pattern |
| I95 | Burndown rank 5; L6 biz-strategy overlap |
| I86 | Wave-close regression at P6 |

## 6. Verification matrix (P0–P1)

```powershell
py scripts/validate_research_action.py
py scripts/validate_hlk.py
py scripts/validate_area_completeness.py --area Operations --next
py scripts/verify.py pre_commit_fast
```
