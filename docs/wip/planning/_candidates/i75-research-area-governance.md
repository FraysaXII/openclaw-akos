---
candidate_id: I75
title: Research area governance (full operationalization beyond P4.7 charter)
status: candidate
authored: 2026-05-12
parent_initiative: 70 (closing scaffold)
priority: 5
---

# I75 candidate — Research area governance

## 1. Scope

Operationalizes the Research area beyond I70 P4.7's charter stubs. Per `RESEARCH_AREA_CHARTER.md` + the 4 discipline charter stubs (METHODOLOGY / INTELLIGENCE / DIAGNOSIS / VALIDATION):

- Full per-discipline SOPs at each `Research/<discipline>/canonicals/`:
  - **Methodology**: per-pillar SOPs (~6-8 pillars expected).
  - **Intelligence**: per-source-type SOPs (HUMINT + OSINT + SIGINT/MASINT reserved); intelligence-collection cadence per-engagement.
  - **Diagnosis**: per-engagement diagnostic templates (counterparty-baseline-reality / system-health / methodology-gap).
  - **Validation**: validation-gate decision rubrics; source-reliability registry.
- KM Officer curriculum (curates Tier 1 WIP per `docs/wip/intelligence/`; cross-references I73 People/Learning curriculum).
- Research Director role activation (currently NEW per P4.7 §3; baseline_organisation.csv addition deferred to I72 + P4.5 wave 2/3).
- Research Analyst expanded scope (Methodology + Intelligence + Diagnosis + Validation cross-cutting).
- IntelligenceOps SOPs migrated under Research/Intelligence per D-IH-70-W (P4.5 wave 3 deferred).
- Per-engagement intelligence cadence (engagement-as-org-diagnostic pattern per F-51 + DIAGNOSIS_DISCIPLINE_CHARTER §4).

## 2. Why priority 5 (last)

- P4.7 ships the parent + 4 stub charters; mature operationalization is significant SOP authoring effort.
- IntelligenceOps SOP migration depends on P4.5 wave 3.
- Research Director role activation depends on baseline_organisation.csv updates from I72 + P4.5 wave 2/3.
- KM Officer curriculum cross-coordinates with I73 People/Learning curriculum.
- The discipline structure is in place (P4.7); maturation can pace later.

## 3. Spin-out trigger conditions

- I70 closing UAT + v3.1 release flag.
- I71 + I72 + I73 P0 charters shipped.
- P4.5 wave 3 federated-canonicals migration complete (IntelligenceOps SOPs migrated under Research/Intelligence).
- First Research Director hire OR founder formally takes the role.

## 4. Cross-references

- I70 P4.7 commit `1e2637f` (RESEARCH_AREA_CHARTER + 4 discipline charter stubs + Tier 1 WIP README).
- D-IH-70-S (P3 ratification: Research as new top-level area).
- D-IH-70-W (P2.5 sub-decision: IntelligenceOps placement under Research/Intelligence).
- Conundrum 11 — Research area as new top-level (R2 discipline-led).
- WORKSPACE_BLUEPRINT_HOLISTIKA §17 (3-tier WIP topology; Research owns Tier 1).
- I73 People/Learning curriculum — cross-coordinates KM Officer curriculum.
