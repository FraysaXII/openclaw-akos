---
candidate_id: I72
title: Marketing Area Governance (renamed from I67 RevOps Discovery per Conundrum 12)
status: candidate
authored: 2026-05-12
last_review: 2026-05-13
parent_initiative: 70 (closing scaffold)
priority: 2
supersedes: I67 (RevOps Discovery)
language: en
---

# I72 candidate — Marketing Area Governance

> **Candidate scaffold (deepened 2026-05-13).** Promoted to `active` when the operator ratifies activation; expected post-I71 P2 (validator packs A1–A3 unblock template-promotion machinery). Master-roadmap to be authored at `docs/wip/planning/72-marketing-area-governance/master-roadmap.md` upon promotion.

## 1. Operating story

I70 P8 redesigned Marketing into the **M3 ontology**: **Brand** (saying) + **Reach** (extending: acquisition + Demand Generation + Paid Media) + **Resonance** (deepening: Account Management + Community Manager) + **Storytelling** (conveying: PR + Thought Leadership + Corporate Marketing) + **Experimentation** (testing: Growth Hacker + Marketing Analytics). The redesign is **structurally landed** (`baseline_organisation.csv` rows + `process_list.csv` updates per `D-IH-70-Z` + `MARKETING_AREA_M3_REDESIGN.md`), but each sub-area beyond Brand still needs:

1. **Per-sub-area charters** (Reach / Resonance / Storytelling / Experimentation) at the federated home `Marketing/<sub-area>/canonicals/`.
2. **An Account Management charter** at `Marketing/Resonance/Account Management/canonicals/` (per `D-IH-70-R`: Account Management owns the WHO of customer success, complementing SMO's WHAT).
3. **An engagement-template promotion machine** owned by RevOps — when 3+ engagements consume the same template pattern, the template gets promoted from "engagement-bespoke" to "RevOps-owned canonical" (per `WORKSPACE_BLUEPRINT_HOLISTIKA.md` §16.3 PMO → RevOps transition trigger).
4. **Activation of the RevOps owner role** (currently `gated_operator` per [I67 superseded]; the Marketing redesign provides the substrate for activation).

The cohering principle: **M3 makes Marketing legible at the discipline level; I72 makes it operational at the engagement-template level**. Engagement template promotion is the moat — it is how Marketing learns from accumulated engagements (the SUEZ + EFA + Asesoría + future-customer-N pattern, surfaced via the previous-project-pattern annex from I70 P2.4).

## 2. Strands

### Strand A — Sub-area charter authoring

| Sub-area | Charter target | Anchor |
|:---|:---|:---|
| **Reach** | `Marketing/Reach/canonicals/REACH_DISCIPLINE_CHARTER.md` | acquisition + Demand Gen + Paid Media; existing Growth folder migrates here. |
| **Resonance** | `Marketing/Resonance/canonicals/RESONANCE_DISCIPLINE_CHARTER.md` | Account Management + Community Manager; deploys Storytelling artifacts. |
| **Storytelling** | `Marketing/Storytelling/canonicals/STORYTELLING_DISCIPLINE_CHARTER.md` | PR + Thought Leadership + Corporate Marketing; **authors** narrative artifacts (case studies, thought-leadership content) per `D-IH-70-X`. |
| **Experimentation** | `Marketing/Experimentation/canonicals/EXPERIMENTATION_DISCIPLINE_CHARTER.md` | Growth Hacker + Marketing Analytics. |
| **Account Management** | `Marketing/Resonance/Account Management/canonicals/ACCOUNT_MANAGEMENT_CHARTER.md` | sub-discipline of Resonance per `D-IH-70-R`. |

### Strand B — Engagement-template promotion machine (RevOps activation)

- **Source patterns**: 6 patterns from the I70 P2.4 previous-project annex (the SUEZ → WeBuy → procure-to-pay shape; engagement diagnostic instrument; bilingual contract; per-sub-area Gantt; etc.).
- **Promotion rule**: 3 engagements consuming the same template → RevOps takes ownership; PMO retains methodology authority but cedes template iteration.
- **Carrier table**: new `ENGAGEMENT_TEMPLATE_REGISTRY.csv` at `Marketing/Resonance/Account Management/canonicals/dimensions/`.
- **ERP panel slot**: `op_revops_engagement_templates` reservation in `HLK_ERP_ARCHITECTURE.md` §4.

### Strand C — RevOps owner activation

- **Baseline row**: change RevOps row in `baseline_organisation.csv` from gated to active; `sub_area: Marketing/Resonance` (per `D-IH-70-Z` schema).
- **SOPs**: `SOP-ENGAGEMENT_TEMPLATE_PROMOTION_001.md` (the promotion machine workflow); `SOP-REVOPS_QBR_001.md` (per-engagement quarterly business review cadence).
- **Validator dependency**: requires I71 Pack **A4** (`validate_render_ownership.py`) to enforce per-deliverable owner coverage at the engagement boundary.

## 3. Phase scaffold

| Phase | Strand | Scope | Closes |
|:---|:---:|:---|:---:|
| **P0** | — | Charter + INITIATIVE / DECISION / OPS rows + master-roadmap | — |
| **P1** | A | Author 4 sub-area charters (Reach / Resonance / Storytelling / Experimentation) + Account Management charter | — |
| **P2** | B | ENGAGEMENT_TEMPLATE_REGISTRY + 6 seed rows (from I70 P2.4 annex) + Supabase mirror + ERP panel slot | OPS-72-1 |
| **P3** | B | `SOP-ENGAGEMENT_TEMPLATE_PROMOTION_001.md` + promotion-rule validator | OPS-72-2 |
| **P4** | C | RevOps activation (baseline row + 2 SOPs + handoff from PMO) | OPS-72-3 |
| **P5** | — | Closing UAT + INITIATIVE_REGISTRY closure | — |

## 4. Conundrums (open at candidate stage)

1. **C-72-1 — Template-promotion threshold**: 3 engagements is the proposed default. Does RevOps need a higher bar (5? 7?) to avoid premature canonicalization? Ratify at P2 inline-ratify gate.
2. **C-72-2 — Account Management vs Customer Success vs SMO Service Delivery**: per `D-IH-70-R`, Account Management owns the WHO and SMO owns the WHAT — but Customer Success teams in industry routinely span both. Need to verify the boundary holds for Holistika's engagement shapes. Ratify at P1 inline-ratify gate.
3. **C-72-3 — Storytelling-authors / Resonance-deploys boundary** (per `D-IH-70-X`): does this hold cleanly when the same human (a Community Manager) sometimes writes the artifact? Ratify at P1.
4. **C-72-4 — Experimentation as standalone vs sub-discipline of Reach**: M3 places it standalone; some operators argue it should be a Reach sub-discipline. Ratify at P1.
5. **C-72-5 — Engagement-template registry mirror posture**: full Supabase mirror (like ENGAGEMENT_REGISTRY) or column-extension on ENGAGEMENT_REGISTRY? Ratify at P2.

## 5. Decision preview (D-IH-72-* rows likely to mint)

- **D-IH-72-A** — sub-area charter authoring (4 disciplines + Account Management).
- **D-IH-72-B** — engagement-template promotion machine architecture (registry + SOP + validator).
- **D-IH-72-C** — RevOps owner activation (baseline row + 2 SOPs).
- **D-IH-72-D** — Storytelling/Resonance boundary ratification (P1 inline-ratify; supersedes / refines `D-IH-70-X`).
- **D-IH-72-CLOSURE** — initiative closure.

## 6. Spin-out trigger conditions

- I70 closing UAT + (optionally) v3.1 release flag — **MET** 2026-05-13.
- I71 P0 charter shipped — **MET** 2026-05-13.
- I71 P2 packs A2/A3 in CI green (template promotion machine validator dependency) — **PENDING**.
- Founder approval to activate RevOps owner — **PENDING**.

## 7. Risk register (top 5)

| Risk | Severity | Mitigation |
|:---|:---:|:---|
| Premature template promotion canonicalizes one-off patterns | High | Conundrum C-72-1 ratification; P2 promotion rule = "3 engagements OR explicit RevOps ratification". |
| Storytelling/Resonance boundary blurs in practice | Medium | Per-engagement ratification when ambiguous; codify in C-72-3 outcome at P1. |
| RevOps activation collides with PMO ownership of methodology | Medium | Strand C P4 includes explicit handoff doc; PMO retains methodology, RevOps takes templates. |
| Account Management charter conflates with SMO Account Manager (D-IH-70-AB) | Medium | Cross-charter section explicitly cites `D-IH-70-R` boundary; one human can hold both roles, but the canonicals stay separate. |
| Sub-area charters mint without operator review (volume) | Low | One sub-area per P1 commit; UAT inline-ratify per charter. |

## 8. Cross-references

- I70 P8 commit `8f2559b` (`MARKETING_AREA_M3_REDESIGN` parent + structural CSV updates).
- I70 P8.2 commit `05c9b3b` (Marketing M3 CSV migration; D-IH-70-Z schema extension).
- I67 RevOps Discovery (superseded; rename per Conundrum 12 + `D-IH-70-T`).
- I70 P2.4 previous-project pattern annex (6 patterns inform the engagement-template promotion machine).
- `WORKSPACE_BLUEPRINT_HOLISTIKA.md` §16.3 — PMO → RevOps transition trigger.
- `D-IH-70-X` (P2.5 sub-decision: Storytelling-authors / Resonance-consumes boundary).
- `D-IH-70-R` (P3 ratification: SMO vs Account Management distinction).
- `D-IH-70-AB` (P8.4: SMO baseline enrichment + SERVICE_CATALOG; Account Manager row).
- I71 master roadmap (Pack A4 dependency): [`docs/wip/planning/71-cicd-discipline-and-aiops-baseline-maturity/master-roadmap.md`](../71-cicd-discipline-and-aiops-baseline-maturity/master-roadmap.md).
- I73 candidate (People Operations + Learning) — cross-coordinates Account Management with HR onboarding rituals.
- I75 candidate (Research area governance) — KM Officer curriculum cross-links.
