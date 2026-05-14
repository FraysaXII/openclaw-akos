---
language: en
status: active
canonical: true
role_owner: Experimentation Manager
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
---

# EXPERIMENTATION_AREA_CHARTER — Marketing/Experimentation sub-area

> Authored I72 P1 per `D-IH-72-A` (P0 charter ratification) + `D-IH-72-E` (Experimentation as standalone 5th sub-area, not folded under Reach). Experimentation owns the **testing** verb in the Marketing M3 ontology: A/B + multi-variant testing of Brand register choices + narrative artefacts + channel-mix variants, with measurement instrumentation feeding the experiment registry. New sub-area (no legacy role); absorbs experiment-design responsibilities scattered across legacy structure.

## 1. Mission

Experimentation exists to **measure variant performance** — turning intuition-driven Marketing decisions into evidence-driven ones. Experimentation owns the discipline of hypothesis authoring, experiment design, statistical-significance gates, instrumentation, and per-experiment registry maintenance. The output is calibrated probabilities, not lifted-vanity-metric reports.

The verb is **testing**: Experimentation owns the discipline of variant generation requests (briefing Brand for register variants; briefing Storytelling for narrative variants; briefing Reach for channel-mix variants), measurement protocol design, and per-experiment writeup.

## 2. Roles + 3-function umbrella (per D-IH-72-AB)

Experimentation roles cluster under the **Operations-side function** of the 3-function umbrella (Demand / Supply / Operations) — Experimentation is the cross-cutting measurement discipline that observes Demand + Supply variants:

| Role | `org_id` | Function umbrella | Discipline |
|:---|:---|:---|:---|
| **Experimentation Manager** | (org row) | Operations (cross-cutting) | Sub-area lead; experiment registry governance; statistical-significance gate authority; cross-discipline experiment-brief reviewer. |
| **Growth Hacker** | (org row) | Operations | Variant generation execution; rapid-iteration experiment authoring; channel-experimentation specialist. NOT a "Growth role" in the legacy sense (legacy Growth dissolved per M3); the title preserves industry-recognised vocabulary while the role lives under Experimentation. |
| **Marketing Analytics Manager** | (org row) | Operations | Instrumentation design; per-platform tracking implementation; statistical-significance computation; per-experiment writeup authoring; cross-link to RevOps Spine (P7) for revenue-impact attribution. |

Cross-function ties:
- **To Operations function (RevOps)**: Per-experiment metric attribution flows through P7 RevOps Spine `engagement_revenue_view` join. Boundary: Experimentation reports lift; RevOps reports revenue-impact.
- **To Demand function (Reach + Resonance)**: Experimentation receives variant requests from Reach (channel-mix experiments) + Resonance (post-capture nurture experiments).
- **To Supply function (Brand + Storytelling)**: Experimentation receives variant requests for register A/B (Brand) + narrative-variant A/B (Storytelling). Experimentation never authors register or narrative; only measures.

## 3. Sub-area boundary (M3 single-ownership)

Per [`MARKETING_AREA_M3_REDESIGN.md`](../../canonicals/MARKETING_AREA_M3_REDESIGN.md) §3 single-ownership contract:

- **Experimentation MEASURES variant performance** of Brand register choices + narrative artefact variants + channel-mix variants.
- **Experimentation does NOT author the brand register** (Brand sub-area only — Experimentation briefs Brand for register variants).
- **Experimentation does NOT author narrative artefacts** (Storytelling sub-area only — Experimentation briefs Storytelling for narrative variants).
- **Experimentation does NOT amplify via channels** (Reach sub-area only — Experimentation briefs Reach for channel-mix variants).
- **Experimentation does NOT deploy in 1:1 contexts** (Resonance sub-area only).

Experimentation's success metric is **calibration accuracy of pre-experiment hypotheses + statistical-significance gate hit-rate + downstream-decision adoption rate**, never raw experiment volume.

## 4. Cross-area integrations (DAMA-DMBOK posture)

Per [`akos-executable-process-catalog.mdc`](../../../../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 4:

| DAMA-DMBOK area | Experimentation posture | Reference |
|:---|:---|:---|
| **Reference & Master Data Management** | Experimentation maintains EXPERIMENT_REGISTRY (P8 deliverable per Process Catalog) as the SSOT for active + archived experiments. Cross-references ENGAGEMENT_REGISTRY + PERSONA_REGISTRY. | `Operations/RevOps/canonicals/dimensions/` (P8 mint zone). |
| **Metadata Management** | Each experiment row carries hypothesis + variants + statistical-significance threshold + outcome-direction + audience-persona-id + engagement-id metadata. | Per-experiment writeup at `_assets/advops/**/experiments/`. |
| **Data Integration & Interoperability** | Per-platform tracking adapters route through `ATTRIBUTION_ADAPTER_REGISTRY.csv` (P9). Experimentation never owns bespoke per-platform tracking. | `D-IH-72-O` Normalized Adapter Pattern + `D-IH-72-T` MarTech breadth (8 adapter classes including ATTRIBUTION). |

## 5. Process catalog (initial; full catalog at P8)

| Process | `item_id` | Cadence | Status | SOP |
|:---|:---|:---|:---|:---|
| Experiment hypothesis authoring + statistical-power calc | `mar_experimentation_dtp_hypothesis_001` (P8 mint) | event_triggered (per-experiment intake) | planned (P8) | `SOP-EXPERIMENT_HYPOTHESIS_001.md` (P8 deliverable) |
| Experiment instrumentation design + tracking implementation | `mar_experimentation_dtp_instrument_001` (P8 mint) | event_triggered (per-experiment) | planned (P8) | `SOP-EXPERIMENT_INSTRUMENT_001.md` (P8 deliverable) |
| Per-experiment writeup + decision-record authoring | `mar_experimentation_dtp_writeup_001` (P8 mint) | event_triggered (post-experiment) | planned (P8) | `SOP-EXPERIMENT_WRITEUP_001.md` (P8 deliverable) |
| Quarterly experiment-portfolio review | `mar_experimentation_dtp_portfolio_001` (P8 mint) | scheduled (quarterly) | planned (P8) | `SOP-EXPERIMENT_PORTFOLIO_REVIEW_001.md` (P8 deliverable) |

Cadences follow [`akos-executable-process-catalog.mdc`](../../../../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 3.

## 6. Activation cadence + lifecycle

- **Activation cadence**: event-triggered per-experiment + scheduled portfolio review. Always-on instrumentation discipline (tracking infrastructure stays live continuously).
- **Lifecycle status**: `active` (sub-area + 3 roles all active in baseline_organisation.csv; charter formalises operating contract).
- **Sub-area maturity**: P1 (this charter) → P8 process catalog mint (registry + 4 SOPs) → P10 closing UAT validates per-experiment writeup coverage.
- **Per `D-IH-72-E` codification**: Experimentation is **standalone**, NOT folded under Reach. The discipline measures variants across all 4 sister sub-areas; subordinating it to one would compromise its cross-discipline measurement authority.

## 7. Cross-references

- Parent: [`MARKETING_AREA_M3_REDESIGN.md`](../../canonicals/MARKETING_AREA_M3_REDESIGN.md) §2 (Experimentation sub-area) + §3 (single-ownership).
- Sister sub-areas: Brand, Reach, Resonance, Storytelling.
- Cross-area sister: `Operations/RevOps/canonicals/REVOPS_AREA_CHARTER.md`.
- Forward-link: `Operations/RevOps/canonicals/dimensions/EXPERIMENT_REGISTRY.csv` (P8 mint).
- Forward-link: `Operations/RevOps/canonicals/adapters/ATTRIBUTION_ADAPTER_REGISTRY.csv` (P9 mint per `D-IH-72-T` MarTech breadth).
- Cursor rule: [`akos-executable-process-catalog.mdc`](../../../../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rules 3 + 4.
- Decisions: `D-IH-72-A` (P0 charter), `D-IH-72-E` (Experimentation as standalone 5th sub-area), `D-IH-72-O` (Normalized Adapter Pattern), `D-IH-72-T` (MarTech adapter breadth), `D-IH-72-AB` (3-function umbrella).
