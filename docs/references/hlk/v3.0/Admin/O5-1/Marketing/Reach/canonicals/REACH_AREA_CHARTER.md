---
language: en
status: active
canonical: true
role_owner: Reach Manager
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

# REACH_AREA_CHARTER — Marketing/Reach sub-area

> Authored I72 P1 per `D-IH-72-A` (P0 charter ratification) + `D-IH-72-Z` (Round 7 GTM-to-Reach migration). Reach owns the **extending** verb in the Marketing M3 ontology: amplifying narrative artefacts authored by Storytelling through paid + organic + partner channels into qualified pipeline. Replaces the legacy `Marketing/Growth/` folder; absorbs Paid Media Manager + Demand Generation; sources GTM SOPs from former Growth path (now under `Reach/canonicals/`).

## 1. Mission

Reach exists to **extend the audience for Holistika narrative artefacts** without authoring them. Reach is the discipline of channel selection, audience targeting, paid spend governance, organic distribution, partner amplification, and inbound capture — measured in qualified pipeline and engagement-readiness signals, never in vanity engagement metrics.

The verb is **extending**: Reach takes a narrative artefact (case study, thought-leadership post, employer-brand collateral, ENISA evidence dossier) authored by Storytelling, integrating Brand register + Research outputs, and amplifies it through the right channel mix to reach the right audience at the right time.

## 2. Roles + 3-function umbrella (per D-IH-72-AB; updated per D-IH-72-AN regression-amend 2026-05-15)

Reach roles cluster under the **Demand-side function** of the 3-function umbrella (Demand / Supply / Operations).

Per `D-IH-72-AN` (regression-amend 2026-05-15) and the operator's "disciplines ≠ roles, no horizontal bloat" principle, the role taxonomy is **slim**: Reach Manager is a generalist holding all Reach disciplines (Demand-Generation + Paid-Media absorbed as disciplines). Headcount expansion at growth stage uses additional Reach Manager seats with discipline-specifying suffix (e.g., Reach Manager - Demand Gen / Reach Manager - Paid Media), not separate role rows.

| Role | `org_id` | Function umbrella | Disciplines held |
|:---|:---|:---|:---|
| **Reach Manager** (generalist) | (org row at baseline_organisation.csv) | Demand | Sub-area lead; channel mix governance; per-engagement reach plan; cross-area liaison with Storytelling + Experimentation. **Plus** (per D-IH-72-AN): Demand-Generation discipline (inbound capture; lead-flow instrumentation; SLA enforcement per `SOP-GTM_INBOUND_SLA_001.md`; CRM + Calendly integration; SEO/SEM execution; MQL/SQL pipeline progression) + Paid-Media discipline (paid spend governance; ad-platform vendor management; creative-variant brief authoring with variants flowing to Experimentation for measurement; per-channel budget envelopes). |

Cross-function ties:
- **To Operations function (RevOps)**: Reach hands off captured leads to RevOps engagement-template promotion (per `SOP-ENGAGEMENT_TEMPLATE_PROMOTION_001.md` at `Operations/RevOps/canonicals/`, P3 deliverable).
- **To Demand function siblings (Resonance)**: Reach captures top-of-funnel; Resonance owns relationship deepening post-capture. Boundary: Reach ends at lead-qualified-by-pipeline-criteria; Resonance begins at lead-claimed-by-account-team.
- **To Supply function (Brand + Storytelling)**: Reach is a downstream consumer of Brand register (visual primitives, voice patterns) + Storytelling artefacts. Reach never authors register; never authors narrative; only amplifies.

## 3. Sub-area boundary (M3 single-ownership)

Per [`MARKETING_AREA_M3_REDESIGN.md`](../../canonicals/MARKETING_AREA_M3_REDESIGN.md) §3 single-ownership contract:

- **Reach AMPLIFIES narrative artefacts** via channels (paid media, content distribution, partner amplification).
- **Reach does NOT author the brand register** (Brand sub-area only).
- **Reach does NOT author narrative artefacts** (Storytelling sub-area only).
- **Reach does NOT measure variant performance** (Experimentation sub-area only — Reach hands creative variants to Experimentation; Experimentation reports lift back).
- **Reach does NOT deepen 1:1 relationships post-capture** (Resonance sub-area only).

Reach's success metric is **qualified pipeline contributed per channel per engagement cycle**, not impressions, clicks, or open-rate. Vanity engagement metrics are Experimentation's input signals, not Reach's KPI.

## 4. Cross-area integrations (DAMA-DMBOK posture)

Per [`akos-executable-process-catalog.mdc`](../../../../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 4 (DAMA-DMBOK 2.0 alignment):

| DAMA-DMBOK area | Reach posture | Reference |
|:---|:---|:---|
| **Reference & Master Data Management** | Reach consumes ENGAGEMENT_REGISTRY (engagement_id) + ENGAGEMENT_TEMPLATE_REGISTRY (P2) + PERSONA_REGISTRY (P5 expansion) as MDM authorities. Never duplicates. | `Operations/RevOps/canonicals/dimensions/ENGAGEMENT_TEMPLATE_REGISTRY.csv` (P2) |
| **Metadata Management** | Per-channel campaigns carry `engagement_id` + `template_id` + `persona_id` foreign keys. Wired through P7 Strand D.1 RevOps Integration Spine (engagement_revenue_view). | `governance.engagement_revenue_view` (P7) |
| **Data Integration & Interoperability** | Channel adapters (paid platform connectors) MUST land at `Operations/RevOps/canonicals/adapters/CRM_ADAPTER_REGISTRY.csv` (P9) — not as Reach-owned bespoke integrations. Reach declares channel needs; RevOps owns adapter lifecycle. | `D-IH-72-O` Normalized Adapter Pattern |

## 5. Process catalog (initial; full catalog at P8)

| Process | `item_id` | Cadence | Status | SOP |
|:---|:---|:---|:---|:---|
| Holistika Internal GTM Proof Run (90-Day) | `holistika_reach_dtp_001` (renamed from `_gtm_dtp_001` per D-IH-72-Z) | scheduled (90-day cycle) | active | `SOP-GTM_QUALIFICATION_001.md` (migrated to `Reach/canonicals/`) |
| Agency Partner Proposal Intake + Fit Assessment | `holistika_reach_dtp_002` (renamed from `_gtm_dtp_002`) | event_triggered (inbound proposal) | active | `SOP-GTM_BD_HANDOFF_001.md` (migrated to `Reach/canonicals/`) |
| Inbound Response SLA (Holistika Services) | `holistika_reach_dtp_003` (renamed from `_gtm_dtp_003`) | event_triggered (every inbound) | active | `SOP-GTM_INBOUND_SLA_001.md` (migrated to `Reach/canonicals/`; PMO co-owned for cross-area lead routing) |

Cadences follow [`akos-executable-process-catalog.mdc`](../../../../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 3 taxonomy (`on_demand`, `scheduled`, `event_triggered`, `gated_operator`).

Future processes added at I72 P8 (Strand D.2 Process Catalog) will populate `REVOPS_PROCESS_CATALOG.yaml` cross-area entries that touch Reach (lead-flow handoff, paid-spend governance gate, channel-mix QBR).

## 6. Activation cadence + lifecycle

- **Activation cadence**: continuous (Reach is an always-on discipline). Per-engagement reach plans authored at engagement P0; channel-spend envelopes reviewed quarterly per `SOP-REVOPS_QBR_001.md` (P4 deliverable).
- **Lifecycle status**: `active` (sub-area + 3 roles all active in baseline_organisation.csv as of pre-I72; charter formalises the operating contract).
- **Deprecation pathway**: legacy `Marketing/Growth/` folder DEPRECATED per D-IH-72-Z; SOPs migrated to `Reach/canonicals/` (Phase 1 of this charter); `Marketing/Growth/` becomes a redirect-only stub at P1 close.

## 7. Cross-references

- Parent: [`MARKETING_AREA_M3_REDESIGN.md`](../../canonicals/MARKETING_AREA_M3_REDESIGN.md) §2 (Reach sub-area) + §3 (single-ownership).
- Sister sub-areas: Brand (`../../Brand/canonicals/`), Resonance (`../../Resonance/canonicals/`), Storytelling (`../../Brand/canonicals/`), Experimentation (`../../Experimentation/canonicals/`).
- Migrated SOPs: `SOP-GTM_QUALIFICATION_001.md`, `SOP-GTM_BD_HANDOFF_001.md`, `SOP-GTM_INBOUND_SLA_001.md` (all at `Reach/canonicals/` post-P1).
- Forward-link: `SOP-ENGAGEMENT_TEMPLATE_PROMOTION_001.md` (P3 at `Operations/RevOps/canonicals/`) — receives qualified leads from Reach.
- Cursor rule: [`akos-executable-process-catalog.mdc`](../../../../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rules 3 + 4.
- Decisions: `D-IH-72-A` (P0 charter), `D-IH-72-AA` (Social dissolution; Paid Media migration), `D-IH-72-Z` (GTM-to-Reach SOP migration), `D-IH-72-AB` (3-function umbrella).
- Cross-area sister: `Operations/RevOps/canonicals/REVOPS_AREA_CHARTER.md` (P1 sibling).
