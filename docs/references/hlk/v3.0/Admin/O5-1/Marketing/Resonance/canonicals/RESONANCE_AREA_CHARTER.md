---
language: en
status: active
canonical: true
role_owner: Resonance Manager
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
  - Account Management/canonicals/ACCOUNT_MANAGEMENT_CHARTER.md
---

# RESONANCE_AREA_CHARTER — Marketing/Resonance sub-area

> Authored I72 P1 per `D-IH-72-A` (P0 charter ratification) + `D-IH-72-AA` (Community Manager sub-area migration). Resonance owns the **deepening** verb in the Marketing M3 ontology: deploying Storytelling artefacts in 1:1 and small-group contexts to deepen relationship health, retention, and customer success. Absorbs Community Manager from legacy Social; introduces Account Management as a first-class role per `D-IH-70-R`.

## 1. Mission

Resonance exists to **deepen relationships post-capture** — turning a captured lead (handed off by Reach) into a sustained, healthy, expanding counterparty relationship across the engagement lifecycle. Resonance never authors register; never authors narrative; only deploys what Brand + Storytelling have produced into 1:1 + community contexts.

The verb is **deepening**: Resonance owns the discipline of relationship maintenance, account expansion, retention forecasting, community moments, and post-engagement nurture. Where Reach asks "did the audience hear us?", Resonance asks "is the relationship healthy and growing?".

## 2. Roles + 3-function umbrella (per D-IH-72-AB)

Resonance roles cluster under the **Demand-side function** of the 3-function umbrella but specifically the post-capture cycle:

| Role | `org_id` | Function umbrella | Discipline |
|:---|:---|:---|:---|
| **Resonance Manager** | (org row at baseline_organisation.csv) | Demand (post-capture) | Sub-area lead; relationship-health KPI ownership; cross-role coordination between Account Management + Community Manager. |
| **Account Management Manager** | (org row) | Demand (post-capture) | 1:1 counterparty relationship maintenance; renewals; expansion proposals; per-account QBR cadence. New first-class role per `D-IH-70-R`. See nested charter `Account Management/canonicals/ACCOUNT_MANAGEMENT_CHARTER.md`. |
| **Community Manager** | `org_032` | Demand (post-capture) | Community moments (events, peer-cohort programs, customer-advisory boards); narrative artefact deployment in community channels; sub_area=Resonance per `D-IH-72-AA` migration from legacy Social. |

Cross-function ties:
- **To Operations function (RevOps)**: Resonance owns relationship-health signals; RevOps owns the engagement-revenue spine (per P7) that monetises those signals into renewal + expansion forecasts. Boundary: Resonance reports relationship-health; RevOps reports revenue-impact.
- **To Demand function siblings (Reach)**: Reach hands off lead at qualified-pipeline criterion; Resonance owns from claim-by-account-team forward.
- **To Supply function (Brand + Storytelling)**: Resonance consumes Brand register (cobranding pattern, visual primitives) + Storytelling artefacts (case studies for QBR decks, thought-leadership for community sessions).

## 3. Sub-area boundary (M3 single-ownership)

Per [`MARKETING_AREA_M3_REDESIGN.md`](../../canonicals/MARKETING_AREA_M3_REDESIGN.md) §3 single-ownership contract:

- **Resonance CONSUMES narrative artefacts** in 1:1 contexts (Account Management deploys case studies in account reviews; Community Manager amplifies thought-leadership in community moments).
- **Resonance does NOT author net-new narrative artefacts.** If a counterparty interaction surfaces a need for a net-new artefact, Resonance briefs Storytelling — never drafts the artefact itself.
- **Resonance does NOT amplify via paid channels** (Reach sub-area only).
- **Resonance does NOT measure variant performance** (Experimentation sub-area only).
- **Resonance does NOT author the brand register** (Brand sub-area only).

Resonance's success metric is **relationship health (per `BRAND_BASELINE_REALITY_MATRIX.md` external register: counterparty understanding) + retention rate + expansion rate**, never narrative production volume or amplification reach.

## 4. Cross-area integrations (DAMA-DMBOK posture)

Per [`akos-executable-process-catalog.mdc`](../../../../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 4:

| DAMA-DMBOK area | Resonance posture | Reference |
|:---|:---|:---|
| **Reference & Master Data Management** | Resonance consumes ENGAGEMENT_REGISTRY + PERSONA_REGISTRY (P5 expansion adds business-developer-collaborator + scenario rows per `D-IH-72-G`) as MDM authorities. | `Operations/RevOps/canonicals/dimensions/ENGAGEMENT_TEMPLATE_REGISTRY.csv` (P2) |
| **Metadata Management** | Per-account interactions carry `engagement_id` + `account_id` + `persona_id` foreign keys. Wired through P7 RevOps Spine. | `governance.engagement_revenue_view` (P7) |
| **Data Integration & Interoperability** | Account-level CRM integrations route through `CRM_ADAPTER_REGISTRY.csv` (P9 Normalized Adapter Pattern). Resonance never owns bespoke per-account integrations. | `D-IH-72-O` Normalized Adapter Pattern |

## 5. Process catalog (initial; full catalog at P8)

| Process | `item_id` | Cadence | Status | SOP |
|:---|:---|:---|:---|:---|
| Per-account QBR cadence | `mar_resonance_dtp_qbr_001` (P8 mint) | scheduled (quarterly) | planned (P8) | `SOP-RESONANCE_QBR_001.md` (P8 deliverable) |
| Community moment authoring | `mar_resonance_dtp_community_moment_001` (P8 mint) | event_triggered (campaign cadence) | planned (P8) | `SOP-COMMUNITY_MOMENT_001.md` (P8 deliverable) |
| Renewal + expansion proposal authoring | `mar_account_dtp_renewal_001` (P8 mint) | scheduled (per-engagement renewal cycle) | planned (P8) | `SOP-ACCOUNT_RENEWAL_001.md` (P8 deliverable; nested) |

P8 process catalog mint will populate cadences per [`akos-executable-process-catalog.mdc`](../../../../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 3.

## 6. Activation cadence + lifecycle

- **Activation cadence**: continuous (always-on per active engagement). Per-engagement Resonance plan authored at engagement P0; relationship-health review monthly; QBR quarterly; renewal proposal at engagement-end-minus-90-days.
- **Lifecycle status**: `active` (sub-area + Resonance Manager + Community Manager active in baseline_organisation.csv; Account Management Manager active per D-IH-70-R + this charter formalisation).
- **Round 7 D-IH-72-AA migration**: Community Manager `sub_area` flipped from legacy `Social` to `Resonance` (already reflected in baseline_organisation.csv pre-I72; this charter cites it).

## 7. Cross-references

- Parent: [`MARKETING_AREA_M3_REDESIGN.md`](../../canonicals/MARKETING_AREA_M3_REDESIGN.md) §2 (Resonance sub-area) + §3 (single-ownership).
- Nested: [`Account Management/canonicals/ACCOUNT_MANAGEMENT_CHARTER.md`](Account%20Management/canonicals/ACCOUNT_MANAGEMENT_CHARTER.md) (sibling sub-charter at P1).
- Sister sub-areas: Brand, Reach, Storytelling, Experimentation.
- Cross-area sister: `Operations/RevOps/canonicals/REVOPS_AREA_CHARTER.md`.
- Cursor rule: [`akos-executable-process-catalog.mdc`](../../../../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rules 3 + 4.
- Brand register source: `../../Brand/canonicals/BRAND_BASELINE_REALITY_MATRIX.md` (external-register vocabulary for counterparty-facing prose).
- Decisions: `D-IH-72-A` (P0 charter), `D-IH-70-R` (Account Management as first-class role), `D-IH-72-AA` (Community Manager → Resonance migration), `D-IH-72-AB` (3-function umbrella), `D-IH-72-G` (Persona scenario expansion at P5).
