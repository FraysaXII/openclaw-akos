---
initiative_id: INIT-OPENCLAW_AKOS-75
title: I75 Research area governance (full operationalization beyond P4.7 charter)
status: active
authored: 2026-05-21
last_review: 2026-05-21
inception_decision_id: D-IH-75-A
owner_role: Lead Researcher
co_owner_role: PMO
authority: Founder + Lead Researcher + PMO
language: en
parent_dependency:
  - INIT-OPENCLAW_AKOS-70
  - INIT-OPENCLAW_AKOS-84
  - INIT-OPENCLAW_AKOS-86
sibling_initiatives:
  - INIT-OPENCLAW_AKOS-71
  - INIT-OPENCLAW_AKOS-72
  - INIT-OPENCLAW_AKOS-73
linked_decisions:
  - D-IH-75-A
  - D-IH-86-CC
  - D-IH-84-G
  - D-IH-84-H
  - D-IH-70-W
linked_canonicals:
  - docs/references/hlk/v3.0/Admin/O5-1/Research/RESEARCH_AREA_CHARTER.md
  - docs/references/hlk/v3.0/Admin/O5-1/Research/Methodology/canonicals/SUBSTRATE_LANDSCAPE_DOCTRINE.md
  - docs/references/hlk/v3.0/Admin/O5-1/Research/Methodology/canonicals/SOP-RESEARCH_SUBSTRATE_AUDIT_CADENCE_001.md
  - docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/RESEARCH_HEAD_DISCIPLINE.md
authoritative_plan: docs/wip/planning/75-research-area-governance/master-roadmap.md
methodology_version_at_authoring: v3.1
program_anchors:
  - PRJ-HOL-INF-2026
---

# I75 — Research area governance (full operationalization beyond P4.7 charter)

> **Status: active** (promoted 2026-05-21 under I86 Wave O via OVERRIDE `D-IH-86-CC`; speculative-promotion debt explicitly accepted — Research Director hire OR founder-takes-role activation gate overridden so SOP buildout can proceed in parallel with the hire decision). Inception ratified by `D-IH-75-A`. Charter scaffold per `as-far-as-possible-with-defaults` pace clause.

## Lineage (why I75 promotes now under OVERRIDE)

The candidate file [`docs/wip/planning/_candidates/i75-research-area-governance.md`](../_candidates/i75-research-area-governance.md) names three prerequisites: (a) I71/I72/I73 P0 charters shipped; (b) IntelligenceOps SOP migration complete under `Research/Intelligence/` per `D-IH-70-W`; (c) Research Director hired OR founder formally takes the role. Per `D-IH-86-CC` Wave O OVERRIDE, the operator chose Option C — accept speculative-promotion debt; promote now so SOP buildout proceeds in parallel with the hire decision.

I84 P3 ratified `D-IH-84-G` (Research-area discipline-of-disciplines posture) + `D-IH-84-H` (Research substrate audit cadence + Research Lead role-class with KM Officer + Founder interim until Research Director hire). I75 charter inherits both decisions: Research Lead = role class; KM Officer + Founder are interim embodiments; Research Director hire OR founder-takes-role decision is forward-deferred without blocking SOP buildout.

## Operating story

I70 P4.7 promoted **Research** from a sub-area under `Admin/O5-1/Research/` to a **top-level area** with **four disciplines**: **Methodology** (curates the methodology pillars), **Intelligence** (HUMINT + OSINT + reserved SIGINT/MASINT), **Diagnosis** (per-engagement diagnostic templates), and **Validation** (validation-gate decision rubrics; source-reliability registry). The promotion is **structurally landed** but the disciplines are **stub-shaped**: each charter is one or two sections, not a working SOP set.

I75 fills in the disciplines:

1. **Per-discipline SOPs** (~6-8 Methodology pillars, ~5 Intelligence source-types, ~3 Diagnosis templates, ~4 Validation decision rubrics).
2. **KM Officer curriculum** (cross-coordinates I73 People/Learning Holistik Researcher curriculum).
3. **Research Director role activation** decision (forward-deferred per D-IH-84-H).
4. **IntelligenceOps SOPs migration** owners + per-source-type curriculum (P4.5 wave 3 already moved the SOPs per `D-IH-70-W`).
5. **Per-engagement intelligence cadence** (engagement-as-org-diagnostic pattern per F-51 + `DIAGNOSIS_DISCIPLINE_CHARTER` §4).

The cohering principle: **Research = the discipline of building knowledge that earns the right to be canonical**.

## Phase shape (proposed; ratified at P0)

| Phase | Purpose | Deliverable | Effort | Pause-point |
|:---|:---|:---|---:|:---|
| **P0** | Charter + Research Director hire decision (or founder-takes-role) ratify | D-IH-75-A..F; OPS-75-1..4 | 1-2d | **operator-required gate** (Research Director hire decision per D-IH-84-H) |
| **P1** | Methodology discipline SOPs (~6-8 pillar SOPs minted at status:charter) | SOP set under `Research/Methodology/canonicals/`; `process_list.csv` tranche | 5-7d | **canonical-CSV gate** (process_list tranche per `akos-governance-remediation.mdc`) |
| **P2** | Intelligence discipline SOPs (~5 source-type SOPs; HUMINT/OSINT/reserved SIGINT-MASINT + Intelligence Matrix) | SOP set under `Research/Intelligence/canonicals/`; process_list tranche | 4-6d | **canonical-CSV gate** |
| **P3** | Diagnosis discipline SOPs (~3 templates: baseline-reality + system-health + methodology-gap) | SOP set under `Research/Diagnosis/canonicals/`; process_list tranche | 3-4d | **canonical-CSV gate** |
| **P4** | Validation discipline SOPs (~4 decision rubrics + `SOURCE_RELIABILITY_REGISTRY.csv` mint) | SOP set + registry CSV under `Research/Validation/canonicals/`; PRECEDENCE row | 3-4d | **canonical-CSV gate** |
| **P5** | KM Officer curriculum + per-engagement intelligence cadence + IntelligenceOps owner assignments | Curriculum doc; cadence SOP; owner table | 2-3d | standard |
| **P6** | Closure + Research Director onboarding handover (if hired) OR founder-role stabilization | Closure pause record; UAT report | 0.5d | closure-mega-ratify |

Total estimated effort: **18-26 days** for full operationalization across the 4 disciplines.

## Decisions preview

| ID | Question | Owner | Status entering | Close-out |
|:---|:---|:---|:---|:---|
| **D-IH-75-A** | I75 mega-charter scope — 4-discipline SOP buildout + KM Officer curriculum + Research Director activation | Research Lead + PMO | RATIFIED via D-IH-86-CC OVERRIDE | this commit |
| **D-IH-75-B** | Research Director hire posture (external hire / founder-takes-role / interim continues) | Founder | Proposed (operator-required gate) | P0 |
| **D-IH-75-C** | Methodology pillar SOP set (which pillars get individual SOPs vs consolidated SOPs) | Research Lead + Founder | Proposed | P1 |
| **D-IH-75-D** | Intelligence source-type SOP set (HUMINT depth; OSINT scope; reserved sigint/masint posture) | Research Lead | Proposed | P2 |
| **D-IH-75-E** | Diagnosis template depth (3 templates sufficient or expand) | Research Lead + Engagement Lead | Proposed | P3 |
| **D-IH-75-F** | SOURCE_RELIABILITY_REGISTRY.csv schema + governance | Research Lead + System Owner | Proposed | P4 |

## Risks (top 5)

| ID | Risk | L | I | Mitigation |
|:---|:---|:---:|:---:|:---|
| **R-IH-75-1** | Research Director hire delayed; KM Officer + Founder interim continues indefinitely | High | Medium | Per D-IH-84-H interim posture acceptable; D-IH-75-B P0 ratify decides hire-or-defer cleanly |
| **R-IH-75-2** | SOP buildout dilutes Research Lead bandwidth (Tier 1 WIP curation already heavy) | Medium | High | P0 cadence: 2 SOPs/week max; defer remaining SOPs to next operator cycle if bandwidth shrinks |
| **R-IH-75-3** | process_list.csv tranches require operator approval at every phase | High | Medium | Batched operator-approval gates per phase entry (P1/P2/P3/P4); operator pause records filed per `akos-agent-checkpoint-discipline.mdc` |
| **R-IH-75-4** | Per-engagement intelligence cadence collides with engagement-team Marketing/Research handoffs | Medium | Medium | P5 cadence SOP explicit about handoff seam with Marketing/Research per F-51 |
| **R-IH-75-5** | I71/I72/I73 not yet closed at I75 P1+ entry | Medium | Medium | Per D-IH-86-CC OVERRIDE accepted; I71/I72/I73 closure tracked separately |

## Closure criteria

- Charter (P0..P6) ratified.
- 4-discipline SOP set complete (Methodology + Intelligence + Diagnosis + Validation).
- KM Officer curriculum + per-engagement intelligence cadence SOPs minted.
- Research Director hire decision recorded (hired OR founder-takes-role OR interim continues with explicit rationale).
- IntelligenceOps SOP owner assignments complete.
- Closure UAT report at `reports/uat-i75-closure-<YYYY-MM-DD>.md`.

## Cross-references

- Candidate: [`i75-research-area-governance.md`](../_candidates/i75-research-area-governance.md).
- Promotion override: `D-IH-86-CC` (Wave O OVERRIDE).
- Research substrate audit cadence: `D-IH-84-G` + `D-IH-84-H` (I84 P3 ratifications; backfilled at I86 Wave N N.5).
- Research Area Charter: [`RESEARCH_AREA_CHARTER.md`](../../../references/hlk/v3.0/Admin/O5-1/Research/RESEARCH_AREA_CHARTER.md).
- Research Head Discipline: [`RESEARCH_HEAD_DISCIPLINE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/RESEARCH_HEAD_DISCIPLINE.md).
- Cluster coordinator: [I86](../86-initiative-cluster-execution-coordinator/master-roadmap.md).
- Governing rules: [`akos-applied-research-discipline.mdc`](../../../.cursor/rules/akos-applied-research-discipline.mdc), [`akos-people-discipline-of-disciplines.mdc`](../../../.cursor/rules/akos-people-discipline-of-disciplines.mdc), [`akos-governance-remediation.mdc`](../../../.cursor/rules/akos-governance-remediation.mdc).
