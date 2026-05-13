---
candidate_id: I73
title: People Operations + Learning curriculum
status: candidate
authored: 2026-05-12
last_review: 2026-05-13
parent_initiative: 70 (closing scaffold)
priority: 3
language: en
---

# I73 candidate — People Operations + Learning curriculum

> **Candidate scaffold (deepened 2026-05-13).** Promoted to `active` when (a) I71 + I72 P0 charters are shipped, (b) the first Holistik Researcher is hired (per `D-IH-70-M` cohort tag activation), and (c) the founder formally onboards a People Operations role. Master-roadmap to be authored at `docs/wip/planning/73-people-operations-and-learning-curriculum/master-roadmap.md` upon promotion.

## 1. Operating story

I70 P8.3 hard-removed the Talent monolith and split People into **four sub-disciplines**: **Compliance** (the existing role, now with `sub_area: People/Compliance`), **Ethics** (new — `Ethics Advisor`, owns `ETHICAL_AUTOMATION_POSTURE.md`), **Learning** (new — `Learning Curator`, owns the Holistik Researcher onboarding curriculum + methodology-pillar coaching), and **People Operations** (new — `People Operations Lead`, owns hiring + onboarding + payroll + offboarding). The split is **structurally landed** in `baseline_organisation.csv` (D-IH-70-AA), but the discipline content is mostly aspirational:

1. **Learning charter** at `People/Learning/canonicals/LEARNING_CHARTER.md` — empty stub today; needs full per-pillar curriculum + methodology-pillar coaching cadence.
2. **Holistik Researcher onboarding curriculum** — referenced in `D-IH-70-M` (cohort tag) but not yet authored; cross-coordinates with **I75** (Research area governance) for per-discipline reading list.
3. **Ethics+Learning inseparability** — operator's thesis "we become unethical when we unlearn" makes Ethics + Learning a Holistika brand differentiator. Cross-link content schedule to `ETHICAL_AUTOMATION_POSTURE.md` quarterly review cadence (per §5).
4. **People Operations SOPs** — hiring (`SOP-HIRING_LIFECYCLE_001.md`), onboarding (`SOP-ONBOARDING_001.md`), payroll (`SOP-PAYROLL_OPS_001.md`), offboarding (`SOP-OFFBOARDING_001.md`).
5. **Compliance scope clarification** — when does People/Compliance own a process vs PMO/Compliance vs Ethics? The split was deliberate (Compliance owns regulatory/contractual; Ethics owns AI-overreach/automation posture); needs an explicit boundary doc.

The cohering principle: **People = the discipline of growing humans inside the OS** — Learning grows them in methodology; Ethics grows them in posture; People Operations grows the process that hires/onboards/pays/offboards them; Compliance grows the regulatory perimeter. Without I73, the four sub-disciplines exist as `baseline_organisation.csv` rows but not as governable institutions.

## 2. Strands

### Strand A — Learning charter + Holistik Researcher curriculum

| Deliverable | Location | Anchor |
|:---|:---|:---|
| `LEARNING_CHARTER.md` | `People/Learning/canonicals/` | Methodology-pillar coaching cadence (per the ~6-8 pillars from I75 Research area). |
| `HOLISTIK_RESEARCHER_ONBOARDING_CURRICULUM.md` | `People/Learning/canonicals/curriculum/` | Per-discipline reading list + per-pillar exercises + cohort cadence. |
| `LEARNING_OPS_BACKLOG.csv` | `People/Learning/canonicals/dimensions/` | Cohort cohorts + status + methodology-version-at-onboarding. |

### Strand B — Ethics+Learning inseparability operationalization

- Cross-link the Learning curriculum content schedule to `ETHICAL_AUTOMATION_POSTURE.md` §5 (quarterly review cadence).
- Author `SOP-ETHICS_LEARNING_REVIEW_001.md`: how Ethics Advisor + Learning Curator co-review the curriculum quarterly.
- Brand-positioning rationale codified in `BRAND_VOICE_FOUNDATION.md` (refresh) — "we become unethical when we unlearn" as a Holistika differentiator.

### Strand C — People Operations SOPs

| SOP | Location | Anchor |
|:---|:---|:---|
| `SOP-HIRING_LIFECYCLE_001.md` | `People/People Operations/canonicals/` | Per-role baseline-organisation row creation; counterparty contract (per `BRAND_COUNTERPARTY_README_CONTRACT`). |
| `SOP-ONBOARDING_001.md` | same | Day-1 / week-1 / month-1 cadence; cross-link Learning curriculum activation. |
| `SOP-PAYROLL_OPS_001.md` | same | Counterparty register integration (`FINOPS_COUNTERPARTY_REGISTER`); FINOPS `finops.*` ledger. |
| `SOP-OFFBOARDING_001.md` | same | Asset return + access revocation + final review stamp. |

### Strand D — Compliance/Ethics boundary

- `PEOPLE_COMPLIANCE_VS_ETHICS_BOUNDARY.md` at `People/Compliance/canonicals/`: explicit table of which process classes are Compliance vs Ethics vs cross-owned.
- `process_list.csv` updates for any orphans surfaced during boundary ratification.

## 3. Phase scaffold

| Phase | Strand | Scope | Closes |
|:---|:---:|:---|:---:|
| **P0** | — | Charter + INITIATIVE / DECISION / OPS rows + master-roadmap | — |
| **P1** | A | `LEARNING_CHARTER.md` + Holistik Researcher curriculum (per-pillar reading list + cohort cadence) | OPS-73-1 |
| **P2** | B | Ethics+Learning quarterly co-review SOP + brand-voice refresh | OPS-73-2 |
| **P3** | C | 4 People Operations SOPs (hiring + onboarding + payroll + offboarding) | OPS-73-3 |
| **P4** | D | Compliance/Ethics boundary doc + process_list orphan reassignments | OPS-73-4 |
| **P5** | — | First Holistik Researcher cohort onboarded (operator-driven; UAT) | — |
| **P6** | — | Closing UAT + INITIATIVE_REGISTRY closure | — |

## 4. Conundrums (open at candidate stage)

1. **C-73-1 — Cohort size for Holistik Researcher onboarding**: 1 vs 2 vs 3+ at first cohort? Operator's bet on AI-coexistence pacing determines this. Ratify pre-P1 (architectural; not execution-time).
2. **C-73-2 — Curriculum versioning vs methodology versioning**: should the curriculum carry its own version cadence (curriculum-v1, v2, …) or always anchor to the methodology version (v3.1)? Default = anchor; ratify at P1.
3. **C-73-3 — Ethics+Learning quarterly review owner**: Ethics Advisor leads with Learning Curator co-reviewing, OR balanced co-ownership? Default = Ethics leads; ratify at P2.
4. **C-73-4 — Payroll SOP scope**: pure ops (counterparty + ledger entries) vs include benefits/tax doctrine? Default = pure ops; benefits/tax is a separate I7N initiative. Ratify at P3.
5. **C-73-5 — Compliance/Ethics boundary edge cases**: GDPR/data-protection (Compliance), AI-overreach posture (Ethics), but what about AI-content-disclosure to customers? Default = Ethics primary, Compliance co-owner. Ratify at P4 inline-ratify gate.

## 5. Decision preview (D-IH-73-* rows likely to mint)

- **D-IH-73-A** — Learning charter + Holistik Researcher curriculum architecture.
- **D-IH-73-B** — Ethics+Learning quarterly co-review SOP.
- **D-IH-73-C** — People Operations SOPs (4-deliverable bundle).
- **D-IH-73-D** — Compliance/Ethics boundary ratification (P4 inline-ratify).
- **D-IH-73-E** — first Holistik Researcher cohort UAT (P5).
- **D-IH-73-CLOSURE** — initiative closure.

## 6. Spin-out trigger conditions

- I70 closing UAT — **MET** 2026-05-13.
- I71 P0 charter — **MET** 2026-05-13.
- I72 P0 charter — **PENDING**.
- First Holistik Researcher hired (or operator commits to a hiring window) — **PENDING**.
- Founder approval to formally onboard People Operations Lead — **PENDING**.

## 7. Risk register (top 5)

| Risk | Severity | Mitigation |
|:---|:---:|:---|
| Curriculum drifts from methodology version (no anchor cadence) | High | C-73-2 default = anchor to methodology; review-stamp dimension (I71 P4 outcome) tracks `methodology_version_at_review`. |
| Ethics+Learning becomes an empty ritual without operational teeth | High | Strand B explicit quarterly cadence + brand-voice refresh; cross-link to `ETHICAL_AUTOMATION_POSTURE` §5. |
| People Operations SOPs collide with FINOPS payroll / counterparty register | Medium | C-73-4 default = pure ops; cross-link to `FINOPS_COUNTERPARTY_REGISTER` rather than duplicate. |
| Compliance/Ethics boundary disputes mid-execution | Medium | C-73-5 inline-ratify gate at P4; case-law table grows as edge cases land. |
| Holistik Researcher cohort onboarding before curriculum is mature | Medium | P5 UAT is the gate; if curriculum is thin, push the cohort to next quarter. |

## 8. Cross-references

- I70 P8.3 commit `0222322` (`PEOPLE_AREA_RESTRUCTURE` parent + 4 sub-role baseline rows).
- I70 P9 commit `882a946` (`ETHICAL_AUTOMATION_POSTURE.md`; Ethics+Learning inseparability §5).
- `D-IH-70-Q` (P3 ratification: People area restructure).
- `D-IH-70-AA` (P8.3 execution: Talent monolith hard-removal + 4 sub-roles).
- `D-IH-70-M` (P3 ratification: Holistik Researcher = role row + cohort tag).
- Founder principles 2.1 (AI coexistence) + 2.2 (CSOLT lesson — humans + AI must learn together).
- I71 master roadmap (review-stamp dimension dependency for curriculum versioning): [`docs/wip/planning/71-cicd-discipline-and-aiops-baseline-maturity/master-roadmap.md`](../71-cicd-discipline-and-aiops-baseline-maturity/master-roadmap.md).
- I72 candidate (Marketing Area Governance) — cross-coordinates Account Management with onboarding rituals.
- I75 candidate (Research area governance) — KM Officer curriculum cross-coordinates with Holistik Researcher curriculum.
