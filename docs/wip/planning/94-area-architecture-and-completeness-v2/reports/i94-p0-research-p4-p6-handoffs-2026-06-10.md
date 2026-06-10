---
parent_initiative: INIT-OPENCLAW_AKOS-94
authored: 2026-06-10
phase: P4-P6-handoffs
upstream_ssot: research-area-audit-post-io-eviction-2026-06-10.md
operator_ratification:
  q2: I94_P4_P5_P6_sequential_after_Research
linked_initiatives:
  - INIT-OPENCLAW_AKOS-75
  - INIT-OPENCLAW_AKOS-88
---

# I94 P4–P6 handoffs — Research-first sequencing (2026-06-10)

> Operator ratification: **Q2=A** — I94 P4 → P5 → P6 runs **sequentially after**
> Research remediation (OPS-86-26 + I75 P1–P2). This note defines entry criteria,
> deliverables, and verification for each phase. **Not executed in Session 1.**

## Sequencing constraint

```mermaid
flowchart LR
  R0[Research R0 OPS-86-26]
  I75[I75 P1-P2 SOP tranches]
  P4[I94 P4 handoffs doc]
  P5[I94 P5 I88 slice]
  P6[I94 P6 UAT]

  R0 --> I75 --> P4 --> P5 --> P6
```

Operations area tier is **COMPLETE** (93%, crit@L3 10/10) after P3. P4–P6 close
documentation + cross-area wiring debt without reopening P3 CSV gates.

## P4 — Cross-area handoffs (register-only tranche)

**Entry criteria**

- OPS-86-26 closed (Research SSOT single tree)
- I75 P1–P2 at least chartered (SOP paths stable under `Research/`)

**Deliverable:** `docs/references/hlk/v3.0/Admin/O5-1/Operations/canonicals/OPERATIONS_CROSS_AREA_HANDOFFS.md`

| Handoff | Contract surface | Governing rule/SOP |
|:---|:---|:---|
| Data | Mirror emit / two-plane apply | `akos-holistika-operations.mdc` |
| People | Compliance CSV gates / methodology enforcement | `SOP-META_PROCESS_MGMT_001` |
| Finance | FINOPS bridge + `registered_fact` entity gate | `SOP-FINOPS_BRIDGE_001` |
| Tech | CICD baseline + deploy-health Step 0 | `SOP-CICD_BASELINE_001` |
| Research | Intelligence report + engagement trigger routing | Post-R0 Intelligence SOPs |

**Verification:** `validate_hlk.py`; no new `process_list` rows unless operator gate.

## P5 — I88 Operations 10-pillar slice

**Entry criteria:** P4 handoffs doc merged.

**Deliverable:** `docs/wip/planning/88-cross-area-ops-wiring-review-discipline/reports/i94-operations-10-pillar-wiring-2026-06-10.md` (or dated successor)

**Mandatory edits**

- Update I88 master-roadmap §1.4 Operations paragraph: **remove IntelligenceOps under Operations**; cite Research/Intelligence ownership post-I94 P3 + OPS-86-26.
- Wire PMO ↔ Research handoff for engagement-trigger and intelligence-report surfaces.

**Verification:** `validate_area_completeness.py --area Operations --matrix` (maintain COMPLETE).

## P6 — Regression + closure UAT

**Entry criteria:** P5 report filed.

| Gate | Command |
|:---|:---|
| Area tier | `py scripts/validate_area_completeness.py --area Operations --matrix` |
| Worklist | `py scripts/validate_area_completeness.py --area Operations --next` |
| HLK | `py scripts/validate_hlk.py` |
| Fast profile | `py scripts/verify.py pre_commit_fast` |

**Deliverable:** `docs/wip/planning/94-area-architecture-and-completeness-v2/reports/uat-i94-operations-sweep-closure-2026-06-10.md` (11-section bar when executed).

## Session 1 boundary

| Phase | Session 1 status |
|:---|:---|
| P4 OPERATIONS_CROSS_AREA_HANDOFFS.md | **QUEUED** |
| P5 I88 10-pillar report | **QUEUED** |
| P6 UAT closure | **QUEUED** |

## Cross-references

- Operations sweep charter: [`i94-operations-operational-sweep-charter-2026-06-10.md`](i94-operations-operational-sweep-charter-2026-06-10.md)
- P4–P6 execution spec: [`i94-operations-p4-p6-execution-spec-2026-06-10.md`](i94-operations-p4-p6-execution-spec-2026-06-10.md)
- Research audit: [`../../75-research-area-governance/reports/research-area-audit-post-io-eviction-2026-06-10.md`](../../75-research-area-governance/reports/research-area-audit-post-io-eviction-2026-06-10.md)
- I88 master-roadmap §1.4: [`../../88-cross-area-ops-wiring-review-discipline/master-roadmap.md`](../../88-cross-area-ops-wiring-review-discipline/master-roadmap.md)
