---
parent_initiative: INIT-OPENCLAW_AKOS-94
authored: 2026-06-10
intellectual_kind: process_list_tranche_preview
status: ratified
operator_ratification: applied 2026-06-10 batch2 Q1-A pair-all-20
linked_decisions:
  - D-IH-94-A
upstream:
  - i94-operations-master-sweep-design-2026-06-10.md
  - i94-operations-cross-area-execution-map-2026-06-10.md
  - scripts/i94_area09_process_list_tranche.py
---

# I94 P7 T2 — AREA-09 process_list pairing preview (20 rows)

> **Purpose:** Operator-ratification packet for the second pairing tranche (P7 T2) on
> Operations `process_list.csv`. Extends P3 (12 pairings in
> [`scripts/i94_area09_process_list_tranche.py`](../../../../scripts/i94_area09_process_list_tranche.py)).
> **Not committed** — canonical CSV gate pending AskQuestion approval.

## Baseline

| Signal | Value |
|:---|:---|
| Operations process rows (granularity=process) | 53 |
| Paired after P3 | 12 |
| Unpaired (empty `sop_path` or `runbook_path`) | 41 |
| P7 T2 proposal | 20 rows |
| Target after P7 (if all ratified) | ~32/53 paired |

Priority order per [master sweep design §5 P7](i94-operations-master-sweep-design-2026-06-10.md):
PMO dtp (5–7) → RevOps (5–6) → Engagement (4–5) → mirror/compliance triggers (2–3).

Handoff classes per [cross-area execution map](i94-operations-cross-area-execution-map-2026-06-10.md).

## P7 T2 candidate table (20 rows)

| # | process_id | role_parent_1 | item_name | proposed sop_path | proposed runbook_path | handoff class | SOP status | rationale |
|---:|:---|:---|:---|:---|:---|:---|:---|:---|
| 1 | `hol_opera_dtp_310` | PMO | PMO project portfolio SSOT | `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/SOP-PMO_INITIATIVE_PROGRAM_ANCHORS_001.md` | `scripts/pmo_program_anchor_backfill.py` | OPS-LOCAL-DO | **exists** | Portfolio anchor backfill; reuses P3 `hol_ops_dtp_72` pairing pattern for program-layer SSOT. |
| 2 | `thi_opera_dtp_201` | PMO | Product Requirements Definition | `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/SOP-INITIATIVE_GOVERNANCE_001.md` | `scripts/validate_initiative_registry.py` | OPS-LOCAL-DO | **exists** | Initiative charter PRD gate; daily spine links WIP dashboard to governed roadmaps. |
| 3 | `thi_opera_dtp_220` | PMO | Phased Delivery Plan and Critical Path | `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/SOP-INITIATIVE_GOVERNANCE_001.md` | `scripts/validate_initiative_registry.py` | OPS-LOCAL-DO | **exists** | Phase-dependency integrity; same SOP+validator as row 2 (harmonised governance cluster). |
| 4 | `hol_opera_dtp_300` | PMO | Benchmark UX Review Cycle | `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/SOP-PMO_OPERATIONAL_COHESION_INDEX_RENDER_001.md` | `scripts/render_operational_cohesion_index.py` | OPS-LOCAL-DO | **exists** | Quarterly cohesion index sub-process; automation already wired at P2. |
| 5 | `thi_opera_dtp_250` | PMO | Benchmark UX Review and Gap Register | `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/SOP-PMO_OPERATIONAL_COHESION_INDEX_RENDER_001.md` | `scripts/render_operational_cohesion_index.py` | OPS-LOCAL-DO | **exists** | Gap-register input to cohesion render; pairs to existing quarterly block. |
| 6 | `hol_opera_dtp_148` | Operations | Program Management | `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/SOP-INITIATIVE_PROCESS_HARMONISATION_001.md` | `scripts/validate_initiative_registry.py` | OPS-TRIG-COMPLIANCE | **exists** | `manifests_processes` FK harmonisation (D-IH-59-G); fires People/Compliance CSV gate on new process rows. |
| 7 | `hol_opera_dtp_103` | Operations | List Existing Use Cases | `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/SOP-PMO_VAULT_PROMOTION_GATE_001.md` | `scripts/validate_hlk.py` | OPS-TRIG-COMPLIANCE | **exists** | Vault promotion from WIP → process_list; operator CSV gate before canonical mint. |
| 8 | `tbi_ops_dtp_revops_revenue_rollup_001` | PMO | RevOps weekly revenue rollup refresh | `docs/references/hlk/v3.0/Admin/O5-1/Operations/RevOps/canonicals/SOP-REVENUE_ROLLUP_001.md` | `scripts/validate_revops_spine.py` | OPS-TRIG-FINOPS | **exists** | FINOPS bridge companion; weekly rollup validator already in spine. |
| 9 | `tbi_ops_dtp_revops_persona_audit_001` | PMO | RevOps persona registry audit | `docs/references/hlk/v3.0/Admin/O5-1/Operations/RevOps/canonicals/SOP-PERSONA_AUDIT_001.md` | `scripts/validate_persona_registry.py` | OPS-TRIG-RESEARCH | **exists** | Marketing-owned registers; RevOps-orchestrated audit (I72 R-B backfill). |
| 10 | `tbi_ops_dtp_revops_crm_sync_001` | PMO | RevOps daily CRM adapter sync | `docs/references/hlk/v3.0/Admin/O5-1/Operations/RevOps/canonicals/SOP-REVOPS_CRM_SYNC_001.md` | `scripts/revops_dispatch.py` | OPS-LOCAL-DO | **TBI** | Row minted at I79 P6 with `pattern_normalized_adapter`; SOP not yet authored — runbook exists. |
| 11 | `tbi_ops_dtp_revops_regulator_checkpoint_001` | PMO | RevOps quarterly regulator-relationship checkpoint | `docs/references/hlk/v3.0/Admin/O5-1/Operations/RevOps/canonicals/SOP-REVOPS_REGULATOR_CHECKPOINT_001.md` | `scripts/revops_dispatch.py` | OPS-TRIG-RESEARCH | **TBI** | IntelligenceOps register trigger; pairs to Research IO paths post OPS-86-26. |
| 12 | `tbi_ops_dtp_revops_media_review_001` | PMO | RevOps event-triggered media counterparty review | `docs/references/hlk/v3.0/Admin/O5-1/Operations/RevOps/canonicals/SOP-REVOPS_MEDIA_REVIEW_001.md` | `scripts/revops_dispatch.py` | OPS-TRIG-RESEARCH | **TBI** | Event-triggered IO handoff; `revops_dispatch.py` is interim runbook until SOP mint. |
| 13 | `thi_opera_dtp_288` | Operations | LEADS WEB Centralization and BD Routing | `docs/references/hlk/v3.0/Admin/O5-1/Operations/RevOps/canonicals/SOP-FINOPS_BRIDGE_001.md` | `scripts/revops_dispatch.py` | OPS-TRIG-FINOPS | **exists** | Engagement signing → FINOPS counterparty bridge; load-bearing cross-area trigger. |
| 14 | `hol_ops_dtp_71` | PMO | Delivery Management | `docs/references/hlk/v3.0/Admin/O5-1/Operations/Engagement/SOP-ENG_ENGAGEMENT_DESIGN_001.md` | `scripts/scaffold_engagement.py` | OPS-LOCAL-DO | **exists** | Core engagement scaffold entry; automation-first pairing per operations-delivery RULE 2. |
| 15 | `hol_eng_prc_estimation_001` | PMO | Engagement estimation discipline | `docs/references/hlk/v3.0/Admin/O5-1/Operations/Engagement/canonicals/SOP-ENG_ESTIMATION_DISCIPLINE_001.md` | `scripts/estimate_engagement.py` | OPS-LOCAL-DO | **exists** | Dedicated estimation SOP+runbook; net-new process row from I94 P2. |
| 16 | `thi_opera_dtp_97` | Operations | List of Requirements | `docs/references/hlk/v3.0/Admin/O5-1/Operations/Engagement/SOP-ENG_ENGAGEMENT_DESIGN_001.md` | `scripts/scaffold_engagement.py` | OPS-LOCAL-DO | **exists** | Discovery artefact under engagement design; shares scaffold runbook. |
| 17 | `thi_opera_dtp_121` | Operations | List Objectives | `docs/references/hlk/v3.0/Admin/O5-1/Operations/Engagement/SOP-ENG_ENGAGEMENT_DESIGN_001.md` | `scripts/scaffold_engagement.py` | OPS-LOCAL-DO | **exists** | Charter-phase objective capture; same engagement-design pair. |
| 18 | `thi_opera_dtp_129` | Operations | Define Project Scope | `docs/references/hlk/v3.0/Admin/O5-1/Operations/Engagement/SOP-ENG_ENGAGEMENT_DESIGN_001.md` | `scripts/scaffold_engagement.py` | OPS-LOCAL-DO | **exists** | Scope definition gate before estimation (row 15). |
| 19 | `hol_opera_dtp_312` | Operations | Adviser open questions register maintenance | `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md` | `scripts/validate_adviser_questions.py` | OPS-TRIG-COMPLIANCE | **exists** | ADVOPS register maintenance; compliance CSV + mirror emit path. |
| 20 | `hol_ops_pis_3` | Process Owner | Process Identification & Scoping | `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/SOP-PMO_PROCESS_LIST_CSV_MAINTENANCE_001.md` | `scripts/validate_hlk.py` | OPS-TRIG-COMPLIANCE | **exists** | Process governance framework row; canonical CSV maintenance SOP (hooks gate). |

### Priority mix (actual)

| Bucket | Rows | IDs |
|:---|---:|:---|
| PMO dtp / governance | 7 | #1–7 |
| RevOps lifecycle | 6 | #8–13 |
| Engagement client delivery | 5 | #14–18 |
| Mirror / compliance triggers | 2 | #19–20 |

## SOP / runbook verification summary

| Status | Count | process_ids |
|:---|---:|:---|
| SOP **exists** | 17 | all except #10, #11, #12 |
| SOP **TBI** (to be implemented) | 3 | `tbi_ops_dtp_revops_crm_sync_001`, `tbi_ops_dtp_revops_regulator_checkpoint_001`, `tbi_ops_dtp_revops_media_review_001` |
| Runbook **exists** (all 20) | 20 | — |

### P7 blockers — missing SOPs

Three RevOps rows have **runbooks** (`scripts/revops_dispatch.py`) but **no vault SOP yet**:

1. **`SOP-REVOPS_CRM_SYNC_001.md`** — daily CRM adapter sync (`tbi_ops_dtp_revops_crm_sync_001`).
2. **`SOP-REVOPS_REGULATOR_CHECKPOINT_001.md`** — quarterly regulator checkpoint (`tbi_ops_dtp_revops_regulator_checkpoint_001`).
3. **`SOP-REVOPS_MEDIA_REVIEW_001.md`** — event-triggered media review (`tbi_ops_dtp_revops_media_review_001`).

**Recommended posture for operator ratification:**

- **Option A (recommended):** Pair all 20 rows now with proposed paths; mint the 3 TBI SOPs in the same P7 commit wave (before CSV tranche lands) per SOP-META order.
- **Option B:** Pair 17 rows with existing SOPs; defer rows #10–12 to P8 with explicit forward-charter.
- **Option C:** Pair all 20 with TBI placeholder paths; block mirror emit until SOPs land (violates automation-first intent).

## Handoff class distribution

| Class | Rows |
|:---|---:|
| OPS-LOCAL-DO | 11 |
| OPS-TRIG-COMPLIANCE | 4 |
| OPS-TRIG-FINOPS | 2 |
| OPS-TRIG-RESEARCH | 3 |

## Deferred from P7 T2 (not in this 20)

High-value unpaired rows held for P8 T3 or retire/merge inline-ratify:

- Legacy Engage charter tasks (`thi_opera_dtp_120`–`124`, `127`–`129` duplicates beyond scope rows).
- Process governance framework TBD rows (`tbd_tbd_dtp_73`, `tbd_tbd_dtp_74`).
- Data Architect PGF rows (`hol_ops_sd_5`, `hol_ops_pdm_4`, `hol_ops_pdiu_6`, `hol_opera_dtp_276`).
- IntelligenceOps eviction candidate (`gtm_research_dtp_7` Office Automation → Research, not Operations).
- SMO inbound SLA (`holistika_reach_dtp_003`) — Marketing/Reach owns SOP; Operations trigger only.

## Verification matrix (post-ratification commit)

```powershell
py scripts/validate_hlk.py
py scripts/validate_process_list_pairing.py
py scripts/validate_area_completeness.py --area Operations --matrix
py scripts/synthesis_before_tranche_check.py --tranche-id i94-ops-P7 --tranche-class canonical_csv_mint
```

## Script extension note

Extend [`scripts/i94_area09_process_list_tranche.py`](../../../../scripts/i94_area09_process_list_tranche.py) `PAIRINGS` dict with the 20 tuples above (mirror P3 pattern). Do **not** run write mode until operator approves this preview.

## Cross-references

- P3 tranche script: [`scripts/i94_area09_process_list_tranche.py`](../../../../scripts/i94_area09_process_list_tranche.py)
- Master sweep P7: [`i94-operations-master-sweep-design-2026-06-10.md`](i94-operations-master-sweep-design-2026-06-10.md) §4 P7, §5
- Cross-area map: [`i94-operations-cross-area-execution-map-2026-06-10.md`](i94-operations-cross-area-execution-map-2026-06-10.md)
