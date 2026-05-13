---
candidate_id: I75
title: Research area governance (full operationalization beyond P4.7 charter)
status: candidate
authored: 2026-05-12
last_review: 2026-05-13
parent_initiative: 70 (closing scaffold)
priority: 5
language: en
---

# I75 candidate — Research area governance

> **Candidate scaffold (deepened 2026-05-13).** Promoted to `active` when (a) I71 + I72 + I73 P0 charters are shipped, (b) the IntelligenceOps SOP migration under `Research/Intelligence/` is complete (per `D-IH-70-W`, executed during I70 P4.5 wave 3), and (c) a Research Director is hired OR the founder formally takes the role. Master-roadmap to be authored at `docs/wip/planning/75-research-area-governance/master-roadmap.md` upon promotion.

## 1. Operating story

I70 P4.7 promoted **Research** from a sub-area under `Admin/O5-1/Research/` to a **top-level area** with **four disciplines**: **Methodology** (curates the methodology pillars; coaching cadence cross-coordinates with I73 Learning), **Intelligence** (HUMINT + OSINT + reserved SIGINT/MASINT; intelligence-collection cadence per engagement), **Diagnosis** (per-engagement diagnostic templates: counterparty-baseline-reality / system-health / methodology-gap), and **Validation** (validation-gate decision rubrics; source-reliability registry). The promotion is **structurally landed** (`RESEARCH_AREA_CHARTER.md` + 4 stub charters at `Research/<discipline>/canonicals/` per I70 P4.7 commit `1e2637f`), but the disciplines are **stub-shaped**: each charter is one or two sections, not a working SOP set.

I75 fills in the disciplines:

1. **Per-discipline SOPs** (the bulk of the work): ~6-8 Methodology pillars, ~5 Intelligence source-types, ~3 Diagnosis templates, ~4 Validation decision rubrics — each with its own SOP at `Research/<discipline>/canonicals/<sop>.md`.
2. **KM Officer curriculum** (cross-coordinates I73 People/Learning Holistik Researcher curriculum): how a KM Officer curates Tier 1 WIP per `docs/wip/intelligence/`.
3. **Research Director role activation**: currently NEW per P4.7 §3; `baseline_organisation.csv` row addition deferred to I72 + I70 P4.5 wave 2/3 (already complete in `main`).
4. **IntelligenceOps SOPs migration** under `Research/Intelligence/canonicals/` per `D-IH-70-W`: P4.5 wave 3 already moved the SOPs; I75 assigns owners + per-source-type curriculum.
5. **Per-engagement intelligence cadence** (engagement-as-org-diagnostic pattern per F-51 + `DIAGNOSIS_DISCIPLINE_CHARTER` §4): when does an engagement trigger Research input? When does Research output gate engagement decisions?

The cohering principle: **Research = the discipline of building knowledge that earns the right to be canonical**. Methodology says "this pillar holds"; Intelligence says "this signal is real"; Diagnosis says "this engagement has this shape"; Validation says "this output earned canonical status". Without I75, the four disciplines are folder-shaped but not institution-shaped.

## 2. Strands

### Strand A — Per-discipline SOP buildout

| Discipline | SOP set (approximate) | Anchor |
|:---|:---|:---|
| **Methodology** | Per-pillar SOPs (~6-8 pillars; e.g. AI coexistence, computational tipping point, founder principles 2.x) | I70 P9 `FOUNDER_METHODOLOGY_VERSIONING` + `LOGIC_CHANGE_LOG`. |
| **Intelligence** | Per-source-type SOPs: HUMINT (counterparty interviews), OSINT (public-record sweep), reserved SIGINT/MASINT, plus the **Intelligence Matrix** doctrine. | I70 P4.7 stub `INTELLIGENCE_DISCIPLINE_CHARTER.md` + IntelligenceOps SOPs migrated under `Research/Intelligence/` per `D-IH-70-W`. |
| **Diagnosis** | Per-engagement diagnostic templates: `DIAGNOSTIC_BASELINE_REALITY.md`, `DIAGNOSTIC_SYSTEM_HEALTH.md`, `DIAGNOSTIC_METHODOLOGY_GAP.md`. | I70 P4.7 stub `DIAGNOSIS_DISCIPLINE_CHARTER.md`; engagement-as-org-diagnostic pattern (SUEZ proof). |
| **Validation** | Validation-gate decision rubrics + `SOURCE_RELIABILITY_REGISTRY.csv`; canonical-promotion criteria from WIP. | I70 P4.7 stub `VALIDATION_DISCIPLINE_CHARTER.md`; cross-coordinate with `WORKSPACE_BLUEPRINT_HOLISTIKA.md` §13 WIP-to-canonical promotion discipline. |

### Strand B — KM Officer curriculum

- `KM_OFFICER_CURRICULUM.md` at `Research/Methodology/canonicals/curriculum/` — how a KM Officer curates Tier 1 WIP per `docs/wip/intelligence/`; cross-coordinates I73 People/Learning Holistik Researcher curriculum.
- Per-quarter cadence: WIP review → promotion candidate identification → Validation discipline gate → canonical landing.
- Cross-link: `docs/wip/intelligence/README.md` (already authored at I70 P4.7) gets an "owner: KM Officer" annotation.

### Strand C — Research Director role activation

- Refresh `RESEARCH_AREA_CHARTER.md` to reflect activated Research Director.
- `SOP-RESEARCH_LEAD_001.md`: how the Research Director coordinates the 4 disciplines + Research Analyst + KM Officer + Holistik Researcher.
- Cross-link: I72 RevOps activation (Strand C P4) and I73 People Operations activation (Strand C P3) provide the activation precedent.

### Strand D — Per-engagement intelligence cadence

- `SOP-ENGAGEMENT_INTELLIGENCE_CADENCE_001.md` at `Research/Intelligence/canonicals/`: intake → research input → engagement decision gate.
- Cross-link Diagnosis discipline: every engagement opens with a baseline-reality diagnostic; Validation gate decides which findings become canonical input.
- Cross-link `SOP-ENGAGEMENT_TEMPLATE_PROMOTION_001.md` (I72 Strand B) so research findings can promote engagement-templates.

## 3. Phase scaffold

| Phase | Strand | Scope | Closes |
|:---|:---:|:---|:---:|
| **P0** | — | Charter + INITIATIVE / DECISION / OPS rows + master-roadmap | — |
| **P1** | A (Methodology) | ~6-8 per-pillar Methodology SOPs | OPS-75-1 |
| **P2** | A (Intelligence) | Per-source-type Intelligence SOPs + Intelligence Matrix codification | OPS-75-2 |
| **P3** | A (Diagnosis + Validation) | 3 Diagnosis templates + 4 Validation rubrics + `SOURCE_RELIABILITY_REGISTRY.csv` | OPS-75-3 |
| **P4** | B | KM Officer curriculum (cross-coordinated with I73 P1 Holistik Researcher curriculum) | OPS-75-4 |
| **P5** | C | Research Director activation (`SOP-RESEARCH_LEAD_001.md` + charter refresh) | OPS-75-5 |
| **P6** | D | Per-engagement intelligence cadence SOP + Diagnosis-Validation gate cross-links | OPS-75-6 |
| **P7** | — | Closing UAT + INITIATIVE_REGISTRY closure | — |

## 4. Conundrums (open at candidate stage)

1. **C-75-1 — Methodology pillar count**: 6 vs 8 pillars vs operator-driven discovery? The founder principles 2.x suggest ~6 stable; a 7th + 8th may emerge. Default = author known pillars at P1; new pillars open follow-on rows. Ratify pre-P1.
2. **C-75-2 — Intelligence vs Compliance overlap**: Intelligence (Research) gathers external signals; Compliance (People) governs regulatory perimeter. When does an OSINT sweep become a Compliance audit? Default = Intelligence reads, Compliance acts. Ratify at P2 inline-ratify gate.
3. **C-75-3 — Diagnosis output ownership**: a per-engagement Diagnosis output is a Research output OR a PMO engagement artifact? Default = Research authors, PMO consumes. Ratify at P3.
4. **C-75-4 — KM Officer vs Holistik Researcher boundary**: KM Officer curates Tier 1 WIP; Holistik Researcher contributes Tier 1 WIP. Operator may want to merge under one role for the first cohort. Cross-link C-73-1 (cohort size). Ratify at P4 inline-ratify gate.
5. **C-75-5 — Validation gate authority**: the Validation discipline owns the canonical-promotion criteria. Does it have veto on PMO-led promotions? Default = co-sign required (PMO + Validation). Ratify at P3.

## 5. Decision preview (D-IH-75-* rows likely to mint)

- **D-IH-75-A** — Methodology pillar SOP architecture (per-pillar SOP shape + cadence).
- **D-IH-75-B** — Intelligence per-source-type SOPs + Intelligence Matrix codification.
- **D-IH-75-C** — Diagnosis templates + Validation rubrics + SOURCE_RELIABILITY_REGISTRY architecture.
- **D-IH-75-D** — KM Officer curriculum (cross-coordinated with `D-IH-73-A`).
- **D-IH-75-E** — Research Director activation (`SOP-RESEARCH_LEAD_001.md`).
- **D-IH-75-F** — Per-engagement intelligence cadence SOP.
- **D-IH-75-CLOSURE** — initiative closure.

## 6. Spin-out trigger conditions

- I70 closing UAT — **MET** 2026-05-13.
- I71 P0 charter — **MET** 2026-05-13.
- I72 P0 charter — **PENDING**.
- I73 P0 charter — **PENDING**.
- I70 P4.5 wave 3 federated-canonicals migration (IntelligenceOps SOPs migrated under `Research/Intelligence/`) — **MET** (commit `f0c8e9f`).
- First Research Director hire OR founder formally takes the role — **PENDING**.

## 7. Risk register (top 5)

| Risk | Severity | Mitigation |
|:---|:---:|:---|
| Per-discipline SOP buildout sprawls beyond ~3 weeks of effort | High | Strict per-discipline phase budget (P1–P3); each phase has acceptance criteria; no scope creep into adjacent disciplines mid-phase. |
| Intelligence/Compliance boundary blurs (OSINT sweep that triggers Compliance action) | Medium | C-75-2 inline-ratify gate at P2; case-law table grows with edge cases; cross-link `BRAND_JARGON_AUDIT.md` for adversarial OSINT. |
| KM Officer/Holistik Researcher merge confuses I73 cohort onboarding | Medium | C-75-4 inline-ratify gate at P4; cross-coordinate with C-73-1 (I73 cohort size); both can ratify simultaneously. |
| Validation gate veto blocks PMO-led promotions | Medium | C-75-5 default = co-sign; document escalation path (Founder breaks tie). |
| Research Director hiring lag → P5 stalls | Medium | Founder can take the role for 1-2 quarters; P5 charter authoring proceeds; first hire UAT later. |

## 8. Cross-references

- I70 P4.7 commit `1e2637f` (`RESEARCH_AREA_CHARTER` + 4 discipline charter stubs + Tier 1 WIP README).
- I70 P4.5 wave 3 commit `f0c8e9f` (IntelligenceOps SOPs migrated under `Research/Intelligence/canonicals/`).
- `D-IH-70-S` (P3 ratification: Research as new top-level area).
- `D-IH-70-W` (P2.5 sub-decision: IntelligenceOps placement under Research/Intelligence).
- Conundrum 11 — Research area as new top-level (R2 discipline-led design).
- `WORKSPACE_BLUEPRINT_HOLISTIKA.md` §17 (3-tier WIP topology; Research owns Tier 1).
- `WORKSPACE_BLUEPRINT_HOLISTIKA.md` §13 (WIP-to-canonical promotion discipline; Validation gate consumer).
- I70 P9 commit `882a946` (`FOUNDER_METHODOLOGY_VERSIONING` + `LOGIC_CHANGE_LOG`; Methodology pillar source).
- I71 master roadmap (review-stamp dimension dependency for SOP versioning): [`docs/wip/planning/71-cicd-discipline-and-aiops-baseline-maturity/master-roadmap.md`](../71-cicd-discipline-and-aiops-baseline-maturity/master-roadmap.md).
- I72 candidate (Marketing Area Governance) — engagement-template promotion machine cross-coordinates with Per-engagement intelligence cadence (Strand D).
- I73 candidate (People Operations + Learning) — KM Officer curriculum + Holistik Researcher curriculum cross-coordinate.
