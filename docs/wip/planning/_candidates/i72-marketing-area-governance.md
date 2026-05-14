---
candidate_id: I72
title: Marketing Area Governance + Persona Registry + IntelligenceOps Register Expansion
status: gated_operator
authored: 2026-05-12
last_review: 2026-05-14
parent_initiative: 70 (closing scaffold; INIT row minted at I70 closure with broader-than-Marketing scope)
priority: 2
supersedes: I67 (RevOps Discovery)
language: en
---

# I72 candidate — Marketing Area Governance + Persona Registry + IntelligenceOps Register Expansion

> **Candidate scaffold (deepened 2026-05-13; rescoped 2026-05-14).** Promoted to `active` when the operator ratifies activation via the I72 charter session (P0 of the kickoff at [`docs/wip/planning/_templates/i72-kickoff-prompt.md`](../_templates/i72-kickoff-prompt.md)). Master-roadmap to be authored at `docs/wip/planning/72-marketing-area-governance-and-persona-registry-expansion/master-roadmap.md` upon promotion.
>
> **Scope correction (2026-05-14).** The original 2026-05-13 candidate covered only **Marketing Area Governance**, but `INITIATIVE_REGISTRY.csv` row 58 had already minted `INIT-OPENCLAW_AKOS-72` at I70 closure with the **broader title** "Marketing Area Governance + Persona Registry + IntelligenceOps Register Expansion" and `inception_decision_id: D-IH-70-AC`. The forward-charter from `D-IH-70-AC` (P8.5 GOI class hunt) explicitly hands three deferrals to I72: business-developer-collaborator persona row under existing partner class; competitor-intelligence-target IntelligenceOps register schema; regulator (ENISA) / media (PR Manager) / recruiter onboarding patterns. This candidate has been **rescoped into 3 super-strands** to match the existing INIT row.

## 1. Operating story

I70 P8 redesigned Marketing into the **M3 ontology** (Brand / Reach / Resonance / Storytelling / Experimentation; per `MARKETING_AREA_M3_REDESIGN.md` + `D-IH-70-T`). I70 P8.5 ran the GOI class regression hunt and ratified four new GOI/POI enum classes (`legal_counsel_external` / `supplier_infrastructure` / `competitor_intelligence_target` / `recruiter`) plus three concrete rows; per `D-IH-70-AC`, four scope items were explicitly **forward-charted to I72** rather than landed in I70:

1. **`business-developer-collaborator` persona row** under the existing partner class — recognized as a persona within partner, not a new class.
2. **`competitor-intelligence-target` schema** — the new GOI/POI class needs an IntelligenceOps register expansion to capture intelligence-collection structure (cadence / source-type / reliability / output).
3. **Regulator-relationship roadmap** — ENISA-direct correspondence is the worked example (the EU cybersecurity agency); needs a generic SOP that future regulators inherit.
4. **Media-counterparty-onboarding pattern** — PR Manager activation triggered by media engagements; cross-coordinates with Marketing/Storytelling per `D-IH-70-X`.

The cohering principle: **I72 is the initiative that operationalises the Marketing redesign AND the unblocking of three I70-P8.5-deferred governance dimensions**. The three super-strands share the same activation moment (operator ratifies the I72 charter) but address distinct artifacts:

- **Strand A — Marketing Area Governance** (the original candidate scope; authors per-sub-area charters + the engagement-template promotion machine + RevOps activation).
- **Strand B — Persona Registry expansion** (extends `PERSONA_REGISTRY.csv` + `PERSONA_SCENARIO_REGISTRY.csv` with the business-developer-collaborator persona and any additional personas surfaced during planning; brand-jargon hygiene per `D-IH-70-I` strict).
- **Strand C — IntelligenceOps Register Expansion** (new register or extended GOI_POI_REGISTER schema; regulator + media + recruiter onboarding SOPs at `Research/Intelligence/canonicals/`; cross-link to I75 Research area governance candidate).

Strand A is the heaviest authoring strand (5 charters + 2 SOPs + 1 registry + 1 activation handoff). Strands B + C are smaller per-deliverable but both **cross-coordinate** with Research / People initiatives — Strand B with I73 (recruiter onboarding routes through People Operations); Strand C with I75 (IntelligenceOps SOPs already migrated under `Research/Intelligence/canonicals/` per `D-IH-70-W`).

## 2. Strands

### Strand A — Marketing Area Governance

The original 2026-05-13 candidate scope; preserved intact below as three sub-strands.

#### A.1 — Sub-area charter authoring

| Sub-area | Charter target | Anchor |
|:---|:---|:---|
| **Reach** | `Marketing/Reach/canonicals/REACH_DISCIPLINE_CHARTER.md` | acquisition + Demand Gen + Paid Media; existing Growth folder migrates here. |
| **Resonance** | `Marketing/Resonance/canonicals/RESONANCE_DISCIPLINE_CHARTER.md` | Account Management + Community Manager; deploys Storytelling artifacts. |
| **Storytelling** | `Marketing/Storytelling/canonicals/STORYTELLING_DISCIPLINE_CHARTER.md` | PR + Thought Leadership + Corporate Marketing; **authors** narrative artifacts (case studies, thought-leadership content) per `D-IH-70-X`. Cross-link to Strand C media-counterparty-onboarding. |
| **Experimentation** | `Marketing/Experimentation/canonicals/EXPERIMENTATION_DISCIPLINE_CHARTER.md` | Growth Hacker + Marketing Analytics. |
| **Account Management** | `Marketing/Resonance/Account Management/canonicals/ACCOUNT_MANAGEMENT_CHARTER.md` | sub-discipline of Resonance per `D-IH-70-R`. |

#### A.2 — Engagement-template promotion machine

- **Source patterns**: 6 patterns from the I70 P2.4 previous-project annex (the SUEZ → WeBuy → procure-to-pay shape; engagement diagnostic instrument; bilingual contract; per-sub-area Gantt; etc.).
- **Promotion rule**: 3 engagements consuming the same template → RevOps takes ownership; PMO retains methodology authority but cedes template iteration. **Threshold ratified pre-charter at C-72-1.**
- **Carrier table**: new `ENGAGEMENT_TEMPLATE_REGISTRY.csv` at `Marketing/Resonance/Account Management/canonicals/dimensions/`.
- **ERP panel slot**: `op_revops_engagement_templates` reservation in `HLK_ERP_ARCHITECTURE.md` §4.

#### A.3 — RevOps owner activation

- **Baseline row**: change RevOps row in `baseline_organisation.csv` from gated to active; `sub_area: Marketing/Resonance` (per `D-IH-70-Z` schema).
- **SOPs**: `SOP-ENGAGEMENT_TEMPLATE_PROMOTION_001.md` (the promotion machine workflow); `SOP-REVOPS_QBR_001.md` (per-engagement quarterly business review cadence).
- **Validator dependency (HARD)**: requires I71 Pack **A4** (`validate_render_ownership.py`) to enforce per-deliverable owner coverage at the engagement boundary. Pack A4 ships in **I71 P5** (not P2, contrary to earlier kickoff wording — corrected 2026-05-14).

### Strand B — Persona Registry expansion

Per `D-IH-70-AC`: business-developer-collaborator deferred to I72 as a persona within the existing partner class. Strand B operationalises this:

| Deliverable | Location | Anchor |
|:---|:---|:---|
| `PERSONA_REGISTRY.csv` row(s) | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/PERSONA_REGISTRY.csv` | New persona: business-developer-collaborator (partner class). Discovery may surface additional personas. |
| `PERSONA_SCENARIO_REGISTRY.csv` row(s) | sibling path | Per-persona scenarios for engagement-shape rehearsal. |
| Brand-voice register check | per I71 Pack A1 | New persona prose audited via `validate_brand_voice_register.py` strict mode (post-I71 P1 ship). |

The persona/scenario boundary is `C-72-6` (ratify pre-charter).

### Strand C — IntelligenceOps Register Expansion

Per `D-IH-70-AC`: competitor-intelligence-target schema + regulator-relationship roadmap (ENISA worked example) + media-counterparty-onboarding pattern (PR Manager activation) + recruiter onboarding pattern.

| Deliverable | Location | Anchor |
|:---|:---|:---|
| Schema decision (extend GOI_POI_REGISTER vs sibling INTELLIGENCEOPS_REGISTER) | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/` OR `Research/Intelligence/canonicals/dimensions/` | `C-72-7` ratify pre-charter. |
| Regulator-relationship roadmap SOP | `Research/Intelligence/canonicals/SOP-REGULATOR_RELATIONSHIP_001.md` (generic) + ENISA worked-example annex. | `D-IH-70-AC` notes; `C-72-8` ratify pre-charter. |
| Media-counterparty-onboarding pattern | `Marketing/Storytelling/canonicals/SOP-MEDIA_ONBOARDING_001.md` + cross-link from `Research/Intelligence/canonicals/`. | `C-72-9` placement ratification. |
| Recruiter onboarding pattern | cross-link to I73 People Operations Lead activation; recruiter row stays in IntelligenceOps register but onboarding SOP lives at `People/People Operations/canonicals/`. | `C-72-10` cross-link decision. |
| ERP panel slot | `op_intelligenceops_register` (if separate register chosen). | `HLK_ERP_ARCHITECTURE.md` §4 reservation. |

Strand C explicitly cross-coordinates with **I75 Research area governance candidate** — IntelligenceOps SOPs were already migrated to `Research/Intelligence/canonicals/` per `D-IH-70-W` at I70 P4.5 wave 3, so the agent must verify those before authoring new ones.

## 3. Phase scaffold

| Phase | Strand | Scope | Closes | I71 dependency |
|:---|:---:|:---|:---:|:---:|
| **P0** | — | Charter + INIT activation + DECISION rows + OPS rows + master-roadmap | — | none |
| **P1** | A.1 | Author 5 sub-area charters (Reach / Resonance / Storytelling / Experimentation + Account Management) | OPS-72-6 | none |
| **P2** | A.2 | ENGAGEMENT_TEMPLATE_REGISTRY + 6 seed rows + Supabase mirror + ERP panel slot | OPS-72-1 | none |
| **P3** | A.2 | `SOP-ENGAGEMENT_TEMPLATE_PROMOTION_001.md` + promotion-rule validator | OPS-72-2 | none |
| **P4** | A.3 | RevOps activation (baseline row + 2 SOPs + handoff from PMO) | OPS-72-3 | **HARD: I71 P5 Pack A4** |
| **P5** | B | Persona Registry expansion (business-developer-collaborator + any surfaced personas) | OPS-72-4 | none |
| **P6** | C | IntelligenceOps Register Expansion (schema + regulator/media/recruiter SOPs) | OPS-72-5 | none |
| **P7** | — | Closing UAT + INITIATIVE_REGISTRY closure | — | none |

P5 and P6 are **independent** of Marketing P1–P4 and can run in parallel after P0 charter lands.

## 4. Conundrums (open at candidate stage)

**Strand A (Marketing) conundrums (carried over from 2026-05-13 candidate):**

1. **C-72-1 — Template-promotion threshold**: 3 engagements is the proposed default. Does RevOps need a higher bar (5? 7?) to avoid premature canonicalization? **Ratify pre-charter** (architectural; not deferrable to P2).
2. **C-72-2 — Account Management vs Customer Success vs SMO Service Delivery**: per `D-IH-70-R`, Account Management owns the WHO and SMO owns the WHAT — but Customer Success teams in industry routinely span both. Ratify at P1 inline-ratify gate.
3. **C-72-3 — Storytelling-authors / Resonance-deploys boundary** (per `D-IH-70-X`): does this hold cleanly when the same human (a Community Manager) sometimes writes the artifact? Ratify at P1.
4. **C-72-4 — Experimentation as standalone vs sub-discipline of Reach**: M3 places it standalone; some operators argue it should be a Reach sub-discipline. Ratify at P1.
5. **C-72-5 — Engagement-template registry mirror posture**: full Supabase mirror (like ENGAGEMENT_REGISTRY) or column-extension on ENGAGEMENT_REGISTRY? Ratify at P2.

**Strand B + C conundrums (added 2026-05-14):**

6. **C-72-6 — Persona registry vs scenario registry boundary**: business-developer-collaborator goes in `PERSONA_REGISTRY.csv` as a persona row OR in `PERSONA_SCENARIO_REGISTRY.csv` as a scenario row OR both? Default = both (persona row + scenario row). **Ratify pre-charter.**
7. **C-72-7 — IntelligenceOps register architecture**: extend `GOI_POI_REGISTER.csv` with schema columns (regulator_specific / media_specific / recruiter_specific fields) OR mint a sibling `INTELLIGENCEOPS_REGISTER.csv`? Default = sibling register (cleaner; doesn't widen GOI_POI rows). **Ratify pre-charter.**
8. **C-72-8 — Regulator-relationship roadmap shape**: one canonical SOP at `Research/Intelligence/canonicals/SOP-REGULATOR_RELATIONSHIP_ENISA.md` OR a generic SOP that ENISA + future regulators inherit? Default = generic with ENISA worked-example annex. **Ratify pre-charter.**
9. **C-72-9 — Media-counterparty-onboarding placement**: Strand A.1 (Storytelling charter) OR Strand C (IntelligenceOps register)? Default = both — Storytelling charter cross-links to IntelligenceOps register media row; PR Manager activation lives at Storytelling but the register row lives at Research. **Ratify pre-charter.**
10. **C-72-10 — Recruiter onboarding placement**: Strand C (IntelligenceOps register) OR I73 (People Operations Lead activation)? Default = register row at IntelligenceOps + onboarding SOP at People/People Operations + cross-link via `D-IH-72-I`. **Ratify pre-charter.**

## 5. Decision preview (D-IH-72-* rows likely to mint at P0)

- **D-IH-72-A** — Strand A.1 sub-area charter authoring (4 disciplines + Account Management).
- **D-IH-72-B** — Strand A.2 engagement-template promotion machine architecture (registry + SOP + validator + threshold per C-72-1 verdict).
- **D-IH-72-C** — Strand A.3 RevOps owner activation (baseline row + 2 SOPs; gated on I71 P5 Pack A4).
- **D-IH-72-D** — Strand B persona registry vs scenario registry boundary (C-72-6 verdict).
- **D-IH-72-E** — Strand B business-developer-collaborator persona row architecture.
- **D-IH-72-F** — Strand C IntelligenceOps register architecture (extend vs sibling; C-72-7 verdict).
- **D-IH-72-G** — Strand C regulator-relationship roadmap shape (C-72-8 verdict).
- **D-IH-72-H** — Strand C media-counterparty-onboarding placement (C-72-9 verdict).
- **D-IH-72-I** — Strand C recruiter onboarding cross-link to I73 (C-72-10 verdict).
- **D-IH-72-CHARTER** (or **D-IH-72-J**) — I72 charter ratification (3 super-strands; activates `INIT-OPENCLAW_AKOS-72` from `gated_operator` to `active`).
- **D-IH-72-CLOSURE** — initiative closure (P7).

## 6. Spin-out trigger conditions

- I70 closing UAT — **MET** 2026-05-13.
- I71 P0 charter shipped — **MET** 2026-05-13.
- I71 P1 Pack A1 (brand voice register) shipped on `main` — **MET** 2026-05-14.
- I71 P5 Pack A4 (render ownership) shipped — **PENDING** (only required for P4 RevOps activation; does NOT block P0–P3, P5, P6).
- Founder approval to activate RevOps owner — **PENDING** (required at P4).
- Existing `INIT-OPENCLAW_AKOS-72` row in `gated_operator` status — **MET** (row 58, awaiting activation).

## 7. Risk register (top 5)

| Risk | Severity | Mitigation |
|:---|:---:|:---|
| Premature template promotion canonicalizes one-off patterns | High | C-72-1 ratification pre-charter; P2 promotion rule = "3 engagements OR explicit RevOps ratification". |
| Strand B + C scope explosion (operator surfaces many additional personas / new register schemas mid-execution) | High | Pre-charter conundrum ratification (C-72-6 through C-72-10) locks the architecture; new personas / regulators added in execution-time inline-ratify gates, not architecture changes. |
| RevOps activation collides with PMO ownership of methodology | Medium | Strand A.3 P4 includes explicit handoff doc; PMO retains methodology, RevOps takes templates. |
| Account Management charter conflates with SMO Account Manager (D-IH-70-AB) | Medium | Cross-charter section explicitly cites `D-IH-70-R` boundary; one human can hold both roles, but the canonicals stay separate. |
| Strand C IntelligenceOps register duplicates I75 P2 Intelligence per-source-type SOPs | High | Pre-execution audit at P6 verifies no duplication with `Research/Intelligence/canonicals/` SOPs migrated at I70 P4.5 wave 3 per `D-IH-70-W`; cross-coordinate with I75 candidate at P6 inline-ratify. |

## 8. Cross-references

- I70 P8 commit `8f2559b` (`MARKETING_AREA_M3_REDESIGN` parent + structural CSV updates).
- I70 P8.2 commit `05c9b3b` (Marketing M3 CSV migration; `D-IH-70-Z` schema extension).
- I70 P8.4 commit `88aece7` (SMO baseline enrichment; `D-IH-70-AB` Account Manager).
- I70 P8.5 commit `5b3b9be` (GOI class hunt; `D-IH-70-AC` forward-charter to I72; `D-IH-70-AD` stance dimension).
- I67 RevOps Discovery (superseded; rename per Conundrum 12 + `D-IH-70-T`).
- I70 P2.4 previous-project pattern annex (6 patterns inform the engagement-template promotion machine).
- `WORKSPACE_BLUEPRINT_HOLISTIKA.md` §16.3 — PMO → RevOps transition trigger.
- `D-IH-70-AC` — **inception decision** for `INIT-OPENCLAW_AKOS-72`; forward-charter source for Strands B + C.
- `D-IH-70-X` (P2.5 sub-decision: Storytelling-authors / Resonance-consumes boundary).
- `D-IH-70-R` (P3 ratification: SMO vs Account Management distinction).
- `D-IH-70-AB` (P8.4: SMO baseline enrichment + SERVICE_CATALOG; Account Manager row).
- `D-IH-70-W` (P2.5 sub-decision: IntelligenceOps placement under Research/Intelligence; Strand C cross-coordinate target).
- `D-IH-70-AD` (stance dimension; cross-link Strand C IntelligenceOps register).
- I71 master roadmap (Pack A4 dependency for Strand A.3 only): [`docs/wip/planning/71-cicd-discipline-and-aiops-baseline-maturity/master-roadmap.md`](../71-cicd-discipline-and-aiops-baseline-maturity/master-roadmap.md).
- I73 candidate (People Operations + Learning) — recruiter onboarding cross-link per Strand C `D-IH-72-I`.
- I75 candidate (Research area governance) — IntelligenceOps SOPs cross-coordinate per Strand C; KM Officer curriculum cross-links Strand A.1 sub-area charters.
- I72 kickoff template: [`docs/wip/planning/_templates/i72-kickoff-prompt.md`](../_templates/i72-kickoff-prompt.md).
