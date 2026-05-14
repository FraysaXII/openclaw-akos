---
language: en
status: active
canonical: true
role_owner: PMO + RevOps Lead (forward; activated at P4)
classification: way_of_working
intellectual_kind: charter
ssot: true
authored: 2026-05-14
last_review: 2026-05-14
last_review_at: 2026-05-14
last_review_by: CMO
last_review_decision_id: D-IH-72-AH
methodology_version_at_review: v3.0
companion_to:
  - ../../../Marketing/canonicals/MARKETING_AREA_M3_REDESIGN.md
  - ../../../../../../../.cursor/rules/akos-executable-process-catalog.mdc
---

# REVOPS_AREA_CHARTER — Operations/RevOps area (Round 8 NEW)

> Authored I72 P1 per `D-IH-72-AH` (Round 8 Tier-1 closure: Operations/RevOps area charter at P1). RevOps is a **new area** under Operations, sibling to PMO + SMO + IntelligenceOps. Owns the **value-mapping** core function: connecting Marketing demand-side activity (Reach captures + Resonance retention) to Finance revenue + Sales pipeline through the engagement-template + engagement-revenue spine. Activation gated on I71 P5 Pack A4 (Pydantic agentic-flow finalization) per `D-IH-72-AC`; this charter formalises the operating contract pre-activation so the area is shovel-ready when the gate clears.

## 1. Mission

RevOps exists to **make revenue legible across Marketing, Sales, Finance, Data, and Tech** — the integration spine that turns disconnected sub-area outputs into a single revenue narrative. RevOps owns the discipline of:

1. **Engagement-template lifecycle** (P2-P3 deliverables): per-engagement contract patterns from intake → propose → sign → kickoff → mid-engagement → close.
2. **Engagement-revenue spine** (P7 deliverable): Supabase-level FK columns + governance views joining `engagement_id` + `template_id` to `finops.registered_fact` for per-engagement revenue attribution.
3. **Process catalog governance** (P8 deliverable): `REVOPS_PROCESS_CATALOG.yaml` cataloguing 8-12 cross-area processes (Marketing → Sales → Finance handoffs; per-engagement value-mapping cycles).
4. **Cross-area adapter registry** (P9 deliverable): 8 adapter registries (CRM + REVOPS + EMAIL + ATTRIBUTION + BILLING + COMMUNICATION + SCHEDULING + CONTRACT) per `D-IH-72-T` MarTech breadth.
5. **QBR cadence governance** (P4 deliverable): `SOP-REVOPS_QBR_001.md` codifies quarterly business-review cadence; paired with per-account QBR owned by Marketing/Resonance/Account Management.

The verb is **value-mapping**: RevOps doesn't sell, doesn't market, doesn't deliver, doesn't account. RevOps **connects** the operational data trails left by each function into a single revenue-attribution view, enabling executive decision-making on engagement-portfolio health, sub-area ROI, and forward-pipeline confidence.

## 2. Roles + 3-function umbrella (per D-IH-72-AB + D-IH-72-AD)

RevOps roles cluster under the **Operations-side function** of the 3-function umbrella (Demand / Supply / Operations). RevOps is the cross-cutting integration discipline that observes Demand + Supply outputs and translates them into Operations-readable signals:

| Role | `org_id` | Activation | Discipline |
|:---|:---|:---|:---|
| **RevOps Lead** | (P4 mint) | P4 (gated on I71 P5 Pack A4) | Area lead; engagement-revenue spine governance; cross-area adapter lifecycle authority; QBR cadence convener. |
| **RevOps Analyst** | (P4 mint) | P4 (gated on I71 P5 Pack A4) | Per-engagement revenue-attribution analysis; engagement-template promotion gatekeeping; per-quarter portfolio-health reporting. |
| **RevOps Engineer (Adapter Owner)** | (P4 mint) | P4 (gated; expansion role) | `gated_operator` until adapter-volume crosses threshold; owns adapter-lifecycle code at `Operations/RevOps/canonicals/adapters/`. |
| **RevOps Engineer (Spine Owner)** | (P4 mint) | P4 (gated; expansion role) | `gated_operator`; owns Supabase migration + governance views for the engagement-revenue spine. |
| **RevOps Data Steward** | (P4 mint) | P4 (gated; expansion role) | `gated_operator`; per-axis FK steward for the 4-axis value-mapping schema (per `D-IH-72-AF`). |
| **RevOps Strategist** | (P4 mint) | P4 (gated; expansion role) | `gated_operator`; quarterly portfolio-strategy authoring; cross-engagement pattern-mining. |
| **CRO** | (P4 mint; forward-charter) | P4 (forward-charter; activates when team scales) | Chief Revenue Officer; reports to CEO; ultimate revenue-portfolio accountability. Per `D-IH-72-AD` forward-charter: minted in baseline_organisation.csv at P4 with status=`gated_operator`; activates when revenue-portfolio scale + team size cross threshold. |
| **COO** | `org_013` | active | Chief Operating Officer; existing role; RevOps area reports through COO until CRO activates per `D-IH-72-AD`. |

Per `D-IH-72-AC` (Round 7 RevOps activation gating): RevOps Lead + RevOps Analyst flip from gated to active at P4 entry **only after** I71 P5 Pack A4 ships (Pydantic agentic-flow finalization). The 4 expansion roles + CRO remain `gated_operator` indefinitely.

## 3. Area boundary (single-ownership)

Per the M3 single-ownership pattern extended to Operations:

- **RevOps INTEGRATES revenue + pipeline data** across Marketing + Sales + Finance + Data + Tech.
- **RevOps does NOT own the source-of-truth for any single function's data.** Marketing owns Marketing data; Sales owns Sales data; Finance owns Finance data. RevOps owns the **integration views** + **cross-function FK schemas** + **adapter contracts**.
- **RevOps does NOT replace PMO** (PMO owns delivery cadence + program governance) or SMO (SMO owns service-management cadence per `SOP-SERVICE_MGMT_001.md`).
- **RevOps does NOT own per-account relationships** (Marketing/Resonance/Account Management owns the 1:1 relationship; RevOps owns the revenue-attribution view of that relationship).
- **RevOps does NOT own per-engagement delivery** (PMO + delivery-area owners own delivery; RevOps observes engagement-level revenue impact).

RevOps's success metric is **revenue-attribution coverage (% of revenue traceable to engagement_id + template_id) + adapter health (% green per quarter) + cross-function decision-cycle reduction**, never raw revenue volume (that belongs to CRO).

## 4. Cross-area integrations (DAMA-DMBOK posture, primary author)

RevOps is the **primary author** of the DAMA-DMBOK 2.0 alignment posture for the Holistika operating system. Per [`akos-executable-process-catalog.mdc`](../../../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 4:

| DAMA-DMBOK area | RevOps role | Reference |
|:---|:---|:---|
| **Reference & Master Data Management** | RevOps owns ENGAGEMENT_REGISTRY (existing) + ENGAGEMENT_TEMPLATE_REGISTRY (P2 mint) + cross-area MDM coordination. Per `D-IH-72-Y` Round 7 path migration, all RevOps canonicals live under `Operations/RevOps/canonicals/`. | `Operations/RevOps/canonicals/dimensions/`. |
| **Metadata Management** | RevOps maintains the 4-axis value-mapping schema (per `D-IH-72-AF` Round 8): adds 7 new columns to `process_list.csv` at P4 (4 axis FKs + 3 revenue value cells). Per `D-IH-72-V` cascade: schema migration cascades to akos SSOT module + Pydantic validators + Supabase mirror DDL + release-gate. | `process_list.csv` (P4 schema migration). |
| **Data Integration & Interoperability** | RevOps owns 8 adapter registries per `D-IH-72-O` Normalized Adapter Pattern + `D-IH-72-T` MarTech breadth. Each adapter declares `status` (active / inactive / planned / deprecated / experimental) per [`akos-executable-process-catalog.mdc`](../../../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 2. | `Operations/RevOps/canonicals/adapters/` (P9 mint zone). |

Per `D-IH-72-W` (cross-initiative dependencies feature-flag pattern): RevOps spine deliverables touching I73 (recruiter onboarding) + I75 (Research/Intelligence cross-coordination) carry `TODO[I73-DEPENDENCY]` + `TODO[I75-DEPENDENCY]` markers in code; release-gate informational warnings until forward initiatives ship.

## 5. Process catalog (initial; full catalog at P8)

| Process | `item_id` | Cadence | Status | SOP |
|:---|:---|:---|:---|:---|
| Engagement-template intake + fit assessment | `tbi_mkt_dtp_revops_template_intake_001` (P3 mint) | event_triggered (per-engagement intake) | planned (P3) | `SOP-ENGAGEMENT_TEMPLATE_INTAKE_001.md` (P3 deliverable) |
| Engagement-template promotion (intake → active template) | `tbi_mkt_dtp_revops_template_promotion_001` (P3 mint) | gated_operator (per-template promotion review) | planned (P3) | `SOP-ENGAGEMENT_TEMPLATE_PROMOTION_001.md` (P3 deliverable) |
| Quarterly business review (revenue-impact mapping) | `tbi_ops_dtp_revops_qbr_001` (P4 mint) | scheduled (quarterly) | planned (P4) | `SOP-REVOPS_QBR_001.md` (P4 deliverable) |
| Engagement-revenue spine maintenance | `tbi_ops_dtp_revops_spine_maintenance_001` (P7 mint) | scheduled (per-quarter integrity check) | planned (P7) | `SOP-REVOPS_SPINE_MAINTENANCE_001.md` (P7 deliverable) |
| Cross-area process catalog governance (intake + promotion + retire) | `tbi_ops_dtp_revops_catalog_governance_001` (P8 mint) | scheduled (monthly catalog review) | planned (P8) | `SOP-REVOPS_CATALOG_GOVERNANCE_001.md` (P8 deliverable) |
| Adapter lifecycle governance (intake + status transitions + retire) | `tbi_ops_dtp_revops_adapter_lifecycle_001` (P9 mint) | scheduled (quarterly adapter review) | planned (P9) | `SOP-REVOPS_ADAPTER_LIFECYCLE_001.md` (P9 deliverable) |

Cadences follow [`akos-executable-process-catalog.mdc`](../../../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 3.

## 6. Activation cadence + lifecycle

- **Activation cadence**: gated. Area minted at P1 (this charter); operational deliverables (template registry, promotion SOP, RevOps Lead/Analyst, spine, catalog, adapters) ship across P2-P9. Full activation at P10 closing UAT.
- **Lifecycle status**: `planned` → `active` at P4 entry (gated on I71 P5 Pack A4).
- **Pre-activation posture**: PMO interim-owns RevOps deliverables until P4 activation per `D-IH-72-AH`. PMO + RevOps Lead transition documented in P4 deliverables.
- **Round 8 D-IH-72-AH codification**: this charter is the formal mint of the Operations/RevOps area at P1, even though operational activation is gated to P4. Charter-first / activation-second pattern matches the M3 redesign approach (charter authored I70 P8; per-sub-area roles activated I72).

## 7. Cross-references

- Sibling Operations areas: PMO (`../../PMO/`), SMO (`../../SMO/canonicals/SOP-SERVICE_MGMT_001.md`), IntelligenceOps (`../../IntelligenceOps/`).
- Cross-area Marketing sister: [`MARKETING_AREA_M3_REDESIGN.md`](../../../Marketing/canonicals/MARKETING_AREA_M3_REDESIGN.md) — RevOps is the operational counterpart to the M3 redesign.
- Cross-area integrations: `Marketing/Reach/canonicals/REACH_AREA_CHARTER.md`, `Marketing/Resonance/canonicals/RESONANCE_AREA_CHARTER.md`, `Marketing/Resonance/Account Management/canonicals/ACCOUNT_MANAGEMENT_CHARTER.md`, `Marketing/Storytelling/canonicals/STORYTELLING_AREA_CHARTER.md`, `Marketing/Experimentation/canonicals/EXPERIMENTATION_AREA_CHARTER.md`.
- Forward deliverables: P2 (`ENGAGEMENT_TEMPLATE_REGISTRY.csv`), P3 (`SOP-ENGAGEMENT_TEMPLATE_PROMOTION_001.md`), P4 (RevOps role activation + 7-col schema migration + `SOP-REVOPS_QBR_001.md`), P7 (engagement-revenue spine), P8 (`REVOPS_PROCESS_CATALOG.yaml`), P9 (8 adapter registries).
- Cursor rule: [`akos-executable-process-catalog.mdc`](../../../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rules 1-5.
- Decisions: `D-IH-72-A` (P0 charter), `D-IH-72-AC` (RevOps activation gating on I71 P5 Pack A4), `D-IH-72-AD` (RevOps role taxonomy + CRO/COO forward-charter), `D-IH-72-AF` (process_list 7-col schema extension), `D-IH-72-AH` (Operations/RevOps area charter at P1), `D-IH-72-AB` (3-function umbrella), `D-IH-72-V` (schema cascade), `D-IH-72-W` (cross-initiative feature-flag pattern), `D-IH-72-Y` (Round 7 path migration to Operations/RevOps/canonicals/), `D-IH-72-O` (Normalized Adapter Pattern), `D-IH-72-T` (MarTech adapter breadth).
