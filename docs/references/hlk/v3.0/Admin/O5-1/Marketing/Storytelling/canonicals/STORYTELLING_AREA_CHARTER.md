---
language: en
status: active
canonical: true
role_owner: Brand & Narrative Manager
classification: way_of_working
intellectual_kind: charter
ssot: true
authored: 2026-05-14
last_review: 2026-05-14
last_review_at: 2026-05-14
last_review_by: CMO
last_review_decision_id: D-IH-72-A
methodology_version_at_review: v3.0
companion_to:
  - ../../canonicals/MARKETING_AREA_M3_REDESIGN.md
  - ../../Brand/canonicals/BRAND_DISCIPLINE_ONTOLOGY.md
---

# STORYTELLING_AREA_CHARTER — Marketing/Storytelling sub-area

> Authored I72 P1 per `D-IH-72-A` (P0 charter ratification) + `D-IH-70-X` (Corporate Marketing migration to Storytelling). Storytelling owns the **conveying** verb in the Marketing M3 ontology: integrating Brand register + Research outputs into narrative artefacts (case studies, press posts, thought-leadership, employer-brand collateral) deployable by Reach + Resonance. Absorbs Corporate Marketing from legacy People/Talent path.

## 1. Mission

Storytelling exists to **author the narrative artefacts** that Brand register + Research outputs alone cannot become — the integrated stories that explain Holistika to its many audiences (counterparties, investors, recruits, partners, regulators, journalists). Storytelling is the **single authoring authority** for narrative artefacts; Brand authors register, Research authors investigative outputs, Storytelling integrates them into deployable stories.

The verb is **conveying**: Storytelling owns the discipline of narrative integration, audience-aware framing, evidence-backed authorship, and artefact lifecycle (draft → review → approved → deployable → versioned).

## 2. Roles + 3-function umbrella (per D-IH-72-AB)

Storytelling roles cluster under the **Supply-side function** of the 3-function umbrella (Demand / Supply / Operations). Supply produces the artefacts that Demand-side disciplines (Reach + Resonance) deploy:

| Role | `org_id` | Function umbrella | Discipline |
|:---|:---|:---|:---|
| **Storytelling Manager** (generalist; merging into Brand & Narrative Manager at R-E) | (org row) | Supply | Sub-area lead; narrative-artefact lifecycle governance; cross-discipline integration with Brand + Research; per-engagement narrative plan. **Plus** (per D-IH-72-AN regression-amend 2026-05-15): Thought-Leadership-Editorial discipline (long-form essays, founder-corpus integration, editorial calendar coherence, conference + speaking-engagement narrative) + Corporate-Marketing discipline (employer-brand collateral, recruiter-facing narrative, investor-facing collateral, internal-comms templates, leadership-bio materials). FORWARD: at R-E (per D-IH-72-AO), this role MERGES with Brand Manager into Brand & Narrative Manager. |
| **PR Manager** (kept) | (org row) | Supply | Press posts; journalist relationships; press-release authoring; embargo + release-cycle governance. **Kept as separate role** per `D-IH-72-AN` because of distinct external press-identity mandate. Cross-link to `INTELLIGENCEOPS_REGISTER.csv` (P6) for media counterparty rows per `D-IH-72-J`. |

Cross-function ties:
- **To Demand function (Reach + Resonance)**: Storytelling produces; Reach amplifies via channels; Resonance deploys in 1:1 contexts. Boundary: Storytelling never deploys; never amplifies. Resonance + Reach never author.
- **To Supply function siblings (Brand + Research)**: Storytelling consumes Brand register (voice patterns, visual primitives, dual-register baseline reality matrix per `BRAND_BASELINE_REALITY_MATRIX.md`) + Research investigative outputs (intelligence reports, baseline-reality assessments). Never authors register; never authors raw research.
- **To Operations function (RevOps)**: Per-engagement narrative artefacts carry `engagement_id` + `template_id` foreign keys (P7 RevOps Spine) for revenue-impact attribution.

## 3. Sub-area boundary (M3 single-ownership)

Per [`MARKETING_AREA_M3_REDESIGN.md`](../../canonicals/MARKETING_AREA_M3_REDESIGN.md) §3 single-ownership contract:

- **Storytelling AUTHORS narrative artefacts** integrating Brand register + Research outputs.
- **Storytelling does NOT author the brand register** (Brand sub-area only — voice patterns, visual primitives, BRAND_VISION).
- **Storytelling does NOT author raw research** (Research/Intelligence sub-area only — intelligence reports, baseline-reality assessments).
- **Storytelling does NOT amplify via channels** (Reach sub-area only).
- **Storytelling does NOT deploy in 1:1 contexts** (Resonance sub-area only).
- **Storytelling does NOT measure variant performance** (Experimentation sub-area only — narrative-variant A/B tests are Experimentation's measurement scope).

Storytelling's success metric is **narrative artefact velocity + recipient comprehension + downstream amplification yield**, never raw register volume or research volume.

## 4. Cross-area integrations (DAMA-DMBOK posture)

Per [`akos-executable-process-catalog.mdc`](../../../../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 4:

| DAMA-DMBOK area | Storytelling posture | Reference |
|:---|:---|:---|
| **Reference & Master Data Management** | Storytelling consumes BRAND_REGISTER_MATRIX + ENGAGEMENT_REGISTRY + PERSONA_REGISTRY (P5) as MDM authorities. Per-artefact metadata pins `persona_id` + `engagement_id` for downstream attribution. | `Marketing/Brand/canonicals/BRAND_REGISTER_MATRIX.md`. |
| **Metadata Management** | Each narrative artefact carries `intellectual_kind` (case-study / press-release / thought-leadership / employer-brand) + `audience_persona_id` + `engagement_id` + `confidence_level` frontmatter. | `_assets/advops/**/dossier_*.md` pattern. |
| **Data Integration & Interoperability** | Press-release distribution adapters (PR-platform connectors) route through `COMMUNICATION_ADAPTER_REGISTRY.csv` (P9). Storytelling never owns bespoke distribution integrations. | `D-IH-72-O` Normalized Adapter Pattern + `D-IH-72-T` MarTech breadth. |

Cross-link to `INTELLIGENCEOPS_REGISTER.csv` (P6 deliverable per `D-IH-72-H`) for **media counterparty rows** per `D-IH-72-J`: Storytelling authors media-facing artefacts; IntelligenceOps tracks the media counterparty relationship lifecycle.

## 5. Process catalog (initial; full catalog at P8)

| Process | `item_id` | Cadence | Status | SOP |
|:---|:---|:---|:---|:---|
| Per-engagement case-study authoring | `mar_storytelling_dtp_case_study_001` (P8 mint) | event_triggered (engagement close + consent) | planned (P8) | `SOP-CASE_STUDY_AUTHORING_001.md` (P8 deliverable) |
| Press-release authoring + embargo cycle | `mar_storytelling_dtp_press_release_001` (P8 mint) | event_triggered (newsworthy event) | planned (P8) | `SOP-PRESS_RELEASE_001.md` (P8 deliverable; cross-linked to `SOP-MEDIA_ONBOARDING_001.md` at P6) |
| Thought-leadership long-form authoring | `mar_storytelling_dtp_thought_leadership_001` (P8 mint) | scheduled (monthly cadence) | planned (P8) | `SOP-THOUGHT_LEADERSHIP_001.md` (P8 deliverable) |
| Employer-brand collateral authoring | `mar_storytelling_dtp_employer_brand_001` (P8 mint) | scheduled (recruitment-cycle cadence) | planned (P8) | `SOP-EMPLOYER_BRAND_001.md` (P8 deliverable; cross-linked to People/Talent recruiter onboarding at I73 per `D-IH-72-K`). |

Cadences follow [`akos-executable-process-catalog.mdc`](../../../../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 3.

## 6. Activation cadence + lifecycle

- **Activation cadence**: continuous (always-on). Per-engagement narrative plan authored at engagement P0 alongside Reach plan + Account Management playbook.
- **Lifecycle status**: `active` (sub-area + Storytelling Manager + PR Manager + Thought Leadership Editor + Corporate Marketing all active in baseline_organisation.csv; charter formalises operating contract).
- **Round 7 D-IH-70-X migration**: Corporate Marketing `sub_area` flipped from legacy `People/Talent` to `Storytelling` (already reflected in baseline_organisation.csv pre-I72; this charter cites it).

## 7. Cross-references

- Parent: [`MARKETING_AREA_M3_REDESIGN.md`](../../canonicals/MARKETING_AREA_M3_REDESIGN.md) §2 (Storytelling sub-area) + §3 (single-ownership).
- Sister sub-areas: Brand, Reach, Resonance, Experimentation.
- Cross-area sister: `Operations/RevOps/canonicals/REVOPS_AREA_CHARTER.md`.
- Cross-area integrations: `INTELLIGENCEOPS_REGISTER.csv` (P6 — media counterparty per `D-IH-72-J`); `SOP-MEDIA_ONBOARDING_001.md` (P6); `SOP-RECRUITER_ONBOARDING_001.md` (target I73 per `D-IH-72-K`).
- Brand sources: `BRAND_REGISTER_MATRIX.md`, `BRAND_BASELINE_REALITY_MATRIX.md`, `BRAND_VISION.md`, `BRAND_DISCIPLINE_ONTOLOGY.md`.
- Cursor rule: [`akos-executable-process-catalog.mdc`](../../../../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rules 3 + 4.
- Decisions: `D-IH-72-A` (P0 charter), `D-IH-70-X` (Corporate Marketing → Storytelling), `D-IH-72-J` (media counterparty IntelligenceOps row), `D-IH-72-K` (recruiter onboarding cross-link), `D-IH-72-AB` (3-function umbrella).
