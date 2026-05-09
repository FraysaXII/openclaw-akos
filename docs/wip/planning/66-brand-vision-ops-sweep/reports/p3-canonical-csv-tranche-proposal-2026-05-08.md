---
phase: P3
phase_name: Ops, process, organization, catalog, SOPs
initiative: I66
date: 2026-05-08
status: tranche_proposal_pending_operator_approval
gate_kind: canonical_csv_gate
governance: akos-governance-remediation.mdc §"Canonical CSV gates", SOP-META_PROCESS_MGMT_001 §4.2-4.3
---

# I66 P3 — canonical CSV tranche proposal (2026-05-08)

> **Operator gate.** Per `.cursor/rules/akos-governance-remediation.mdc` §"Canonical CSV gates", changes to `process_list.csv` and `baseline_organisation.csv` require **explicit operator approval before committing**. This document is the proposal; commit happens only after the operator signals approval.

## What this tranche does

Operationalises the I66 P1+P2 brand canon by adding:

- **3 new role rows** to [`baseline_organisation.csv`](../../../../references/hlk/compliance/baseline_organisation.csv) — one per sub-mark (Holistika R&S Lead, Think Big Lead, HLK Tech Lab Lead). These are **new distinct roles**, not aliases of existing leadership; they specifically own the brand-expression + sub-mark-mode-of-delivery accountability. They sit alongside existing C-level roles, not above or beneath them.
- **16 new process rows** to [`process_list.csv`](../../../../references/hlk/compliance/process_list.csv) distributed across 5 role owners (Brand Manager × 4, Holistik Researcher × 4, Engagement Manager × 3, Legal Counsel × 2, Talent × 1, Brand Manager-shared-with-Tech × 2). Of these 16, **4 are HUMINT-derived** (counterparty baseline assessment, elicitation discipline, reliability grading, intelligence report) and 12 are standard brand-ops / engagement-ops / legal-ops.

After operator approval and CSV apply, **11 corresponding v3.0 SOPs** are promoted from drafts (this commit) to canonical (subsequent commit), per SOP-META §4.2-4.3 ordering (CSV before SOP for net-new `item_id`s).

## Per-row tranche detail

### Tranche A — `baseline_organisation.csv` (3 new role rows)

Schema: `org_uuid,role_name,role_description,role_full_description,access_level,reports_to,area,entity,org_id,sop_url,responsible_processes,components_used`

| # | role_name | reports_to | access | area | entity | org_id | rationale |
|:---:|:---|:---|:---:|:---|:---|:---|:---|
| A1 | `Holistika R&S Lead` | O5-1 | 4 | Research | Holistika | `org_066` | Owns the **research-first delivery mode** (per `BRAND_ARCHITECTURE.md` §"Sub-mark voice tier" Tier-1). Distinct from Holistik Researcher (which is a methodology head); this is the **engagement-mode owner** for R&S-mode counterparty work — i.e., the role that takes a research brief from intelligence-collection through operator delivery. |
| A2 | `Think Big Lead` | O5-1 | 4 | MKT | Think Big | `org_067` | Owns the **strategy-operationalisation delivery mode** (Tier-2 voice). Distinct from CMO (which is a function head across all sub-marks); this is the engagement-mode owner for Think Big-mode counterparty work — the role that takes a strategy and operationalises it. |
| A3 | `HLK Tech Lab Lead` | O5-1 | 4 | Tech | HLK Tech Lab | `org_068` | Owns the **engineering delivery mode** (Tier-2 voice). Distinct from CTO (which is a function head); this is the engagement-mode owner for HLK Tech Lab counterparty work — the role that takes a technical scope and delivers a running system. |

**`org_uuid`** values for A1-A3 will be assigned by the apply script (UUID4); not pre-allocated to avoid manual mistakes.

**`responsible_processes`** column will be populated after the corresponding `process_list.csv` rows are applied (Tranche B), via a follow-up update referenced from this same commit.

**`components_used`** — left empty; reserved for future I-NN to populate as services-delivery components are catalogued.

**Reporting line rationale** — all three Lead roles report directly to O5-1 (Chief Business Officer) rather than to an intermediate C-level. This reflects the architecture decision (D-IH-66-A) that sub-marks are **delivery modes**, not functional verticals; they cut across the C-level functions (CFO, CPO, COO, CMO, CDO, CTO) rather than nesting under any single one.

### Tranche B — `process_list.csv` (16 new process rows)

Schema: `type,orientation,entity,area,role_parent_1,role_owner,item_parent_2,item_parent_2_id,item_parent_1,item_parent_1_id,item_name,item_id,item_granularity,time_hours_par,description,instructions,addundum_extras,confidence,count_name,frequency,quality`

#### B1-B4 — Brand-canon governance (Brand Manager × 4)

| # | item_id | item_name | item_granularity | granularity | role_owner | frequency | description |
|:---:|:---|:---|:---|:---:|:---|:---:|:---|
| B1 | `tbi_mkt_prc_brand_canon_mtnce_001` | Brand canon maintenance | process | 4 | Brand Manager | 12 | Per-quarter review of all 13 BRAND_*.md canonicals + cross-reference integrity check. Triggers a tranche update if a canonical is older than 12 months without a structural review. |
| B2 | `tbi_mkt_prc_voice_drift_triage_001` | Brand voice drift triage | process | 4 | Brand Manager | 4 | Monthly review of `validate_brand_jargon.py` + `validate_brand_voice_register.py` soft-INFO output; classify each hit as (a) accept-canon-change, (b) require-source-fix, or (c) defer. |
| B3 | `tbi_mkt_prc_register_matrix_review_001` | Register matrix per-audience review | process | 4 | Brand Manager | 2 | Bi-annual review of `BRAND_REGISTER_MATRIX.md` + `BRAND_BASELINE_REALITY_MATRIX.md` per-audience entries. Updates rows when an audience's signature pattern shifts. |
| B4 | `tbi_mkt_prc_jargon_audit_review_001` | Jargon audit registry update | process | 4 | Brand Manager | 4 | Quarterly review of `BRAND_JARGON_AUDIT.md` + `BRAND_ABBREVIATIONS.md` against newly observed external prose drift. |

#### B5-B8 — IntelligenceOps (Holistik Researcher × 4) — the HUMINT-derived processes

| # | item_id | item_name | role_owner | frequency | description |
|:---:|:---|:---|:---|:---:|:---|
| B5 | `hol_res_prc_counterparty_baseline_assess_001` | Counterparty baseline reality assessment | Holistik Researcher | per-engagement | Pre-engagement structured assessment of counterparty (audience type, decision-maker shape, declared and inferred posture, known anti-patterns). Internal-register output; never rendered to counterparty. |
| B6 | `hol_res_prc_elicitation_discipline_001` | Elicitation discipline | Holistik Researcher | per-engagement | Per-engagement elicitation plan: choice of approach techniques (direct interrogation / direct elicitation / indirect elicitation / provocation), discovery questions, listening-protocol checklist, post-engagement follow-up cadence. |
| B7 | `hol_res_prc_reliability_grading_001` | Source reliability grading | Holistik Researcher | per-engagement | Adapted-from-Admiralty A-F × 1-6 grading of every source consulted in an engagement. Internal-register; never rendered to counterparty. |
| B8 | `hol_res_prc_intelligence_report_001` | Intelligence report | Holistik Researcher | per-engagement | BLUF-led, source-graded internal-register report produced after a counterparty engagement. Counterpart of the external-register research brief or engagement report. |

#### B9-B11 — Engagement operations (Engagement Manager × 3)

| # | item_id | item_name | role_owner | frequency | description |
|:---:|:---|:---|:---|:---:|:---|
| B9 | `hol_eng_prc_discovery_questionnaire_001` | Discovery questionnaire ops | Engagement Manager | per-engagement | External-register discovery questionnaire delivery; templated per audience (investor / SME / advisor / ENISA / partner / recruiter / customer); internal-register companion is B6. |
| B10 | `hol_eng_prc_proposal_001` | Proposal generation | Engagement Manager | per-engagement | Templated proposal (scope + price posture + per-cell mapping into the SERVICE_OFFERING_CATALOG); produced after baseline assessment + elicitation cycle. |
| B11 | `hol_eng_prc_engagement_design_001` | Engagement design (multi-cell) | Engagement Manager | per-engagement | When the engagement spans multiple SERVICE_OFFERING_CATALOG cells, this process governs cell-to-cell transition design + per-phase deliverable lock + per-phase voice-tier consistency. |

> **Note on `Engagement Manager`**: this role does not exist in the current `baseline_organisation.csv` and is **not** added in this tranche. Per the operator's Round-3 simplification, B9-B11 use `role_owner: Brand Manager` as a temporary placeholder; a future I-NN (or operator-led mid-cycle update) introduces `Engagement Manager` as a dedicated role. For this tranche we keep the role_owner column compatible with existing baseline.

**Revised assignment**: B9-B11 → `role_owner: Brand Manager` (temporary; flag in description for future re-assignment).

#### B12-B13 — Legal ops (Legal Counsel × 2)

| # | item_id | item_name | role_owner | frequency | description |
|:---:|:---|:---|:---|:---:|:---|
| B12 | `hol_lgl_prc_trademark_monitoring_001` | Trademark monitoring | Legal Counsel | 12 | Quarterly review of EUIPO + OEPM filing status for all Holistika marks (umbrella + 3 sub-marks + 5 product marks per `BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md`). |
| B13 | `hol_lgl_prc_ip_register_mtnce_001` | IP register maintenance | Legal Counsel | 4 | Quarterly update of the IP register (registered marks, applications-in-progress, oppositions, renewals due). |

#### B14 — Talent / People (Talent × 1)

| # | item_id | item_name | role_owner | frequency | description |
|:---:|:---|:---|:---|:---:|:---|
| B14 | `tbi_ppl_prc_founder_bio_mtnce_001` | Founder bio canonical maintenance | Talent | 4 | Quarterly review + update of `SOP-PEOPLE_FOUNDER_BIO_001.md` (founder bio + per-audience FAQ + anonymised track-record). Drift-gate-checked against external-register canon. |

#### B15-B16 — Template + drift-gate operations (Brand Manager × 2)

| # | item_id | item_name | role_owner | frequency | description |
|:---:|:---|:---|:---|:---:|:---|
| B15 | `tbi_mkt_prc_template_registry_mtnce_001` | Brand template registry maintenance | Brand Manager | 4 | Quarterly review of the brand template registry (decks, dossiers, email signatures, press kit, recruiter copy, partner pitch, founder bio); ensures every template references canonical brand assets. Operationalised via `governance.brand_template_registry` (P6). |
| B16 | `tbi_mkt_prc_drift_gate_ops_001` | Brand drift gate operations | Brand Manager | 4 | Quarterly review of `validate_brand_*` gate signals; promotes soft-INFO findings to hard-FAIL when source-fixes land; deprecates findings when the underlying canon changes. |

**Subtotals**:

- Brand Manager (incl. B9-B11 placeholder): 9 rows
- Holistik Researcher: 4 rows
- Legal Counsel: 2 rows
- Talent: 1 row
- **Total: 16 rows**

## Field defaults (tranche apply)

For columns not specified per row above, the apply uses these defaults (matching the dominant pattern in existing rows):

| Column | Default value (per-row) |
|:---|:---|
| `type` | `Internal` |
| `orientation` | `Employee` |
| `entity` | `Holistika` (B1-B4, B12-B16); `Holistika` (B5-B8 — Research area is Holistika-entity); `Holistika` (B9-B11) |
| `area` | `MKT` (B1-B4, B14-B16); `Research` (B5-B8); `MKT` (B9-B11 — until Engagement Manager exists); `Legal` (B12-B13) |
| `role_parent_1` | `CMO` (MKT rows); `Holistik Researcher` (Research rows); `Legal Counsel` (Legal rows); `Talent` (B14) |
| `item_parent_2` / `item_parent_2_id` | (empty — these are top-level project-anchored processes; no two-deep parent) |
| `item_parent_1` | (per-cluster project anchor — see § Project anchoring below) |
| `item_parent_1_id` | (corresponding `*_prj_*` id; created as part of this tranche if not present) |
| `time_hours_par` | (empty — to be calibrated post-rollout) |
| `instructions` | (link to corresponding SOP — added once SOPs are promoted) |
| `addundum_extras` | (empty) |
| `confidence` | `2` (initial draft confidence; rises to `3` after first quarterly cycle) |
| `count_name` | `1` |
| `quality` | `medium` (rises to `high` after first cycle observation) |

## Project anchoring (`item_parent_1`)

Per the existing schema's parent-chain pattern, each new process row needs a `item_parent_1` (project) it belongs to. Tranche B uses 4 project anchors:

- **`tbi_mkt_prj_brand_governance_001`** — Brand governance (anchor for B1-B4, B14-B16) — **may need to be added as a new project row in the same tranche if it does not already exist.**
- **`hol_res_prj_intelligence_ops_001`** — IntelligenceOps program (anchor for B5-B8) — **new project row; added in same tranche.**
- **`hol_eng_prj_engagement_ops_001`** — Engagement ops program (anchor for B9-B11) — **new project row; added in same tranche.**
- **`hol_lgl_prj_brand_legal_001`** — Brand legal ops (anchor for B12-B13) — **new project row; added in same tranche.**

So the actual count is **20 new rows** (4 project anchors + 16 process rows), not 16. The 16 in the I66 plan refers to the leaf processes; the 4 project anchors are infrastructure to make the parent chain valid.

## Validation impact

After apply, the following validators must continue to pass:

| Validator | Expected impact |
|:---|:---|
| `validate_hlk.py` | PASS — referential integrity preserved (all `role_owner` values resolve to existing or newly-added roles; all `item_parent_1_id` values resolve to project rows added in same tranche). |
| `validate_initiative_registry.py` | No impact (registry not touched). |
| `validate_brand_canon_drift.py` | No impact (canonicals not touched). |
| `validate_brand_jargon.py` | No new hits (process_list rows are internal SOPs, jargon validator scope is consumer repos only). |
| `check_process_list_header.py` | PASS — header unchanged. |

## SOP-META compliance

Per `SOP-META_PROCESS_MGMT_001.md` §4.2-4.3 (CSV before SOP for net-new `item_id`s):

- 16 leaf processes + 4 project anchors = 20 new rows in `process_list.csv` **before** the corresponding 11 v3.0 SOPs are finalised.
- The 11 SOPs are drafted in the **same commit** as this tranche proposal (this commit, no CSV touch yet) but ship as `status: draft` until the canonical CSV apply lands.
- Once operator approves Tranche A + B and the CSVs are applied, a **separate commit** promotes the 11 SOPs from `status: draft` to `status: active` and updates the `process_list.csv` `instructions` column with SOP cross-links.

## Risk register (this tranche)

| Risk | Mitigation |
|:---|:---|
| Engagement Manager role missing — B9-B11 use Brand Manager as placeholder | Documented in row descriptions; future I-NN re-assigns. |
| 4 IntelligenceOps rows (B5-B8) introduce new role accountability for Holistik Researcher | Aligns with existing Holistik Researcher role description ("Governs the application of HUMINT techniques"); not a stretch. |
| 3 sub-mark Lead rows may conflict with existing CFO/CMO/CTO if not carefully positioned | Reporting line is O5-1 (not a C-level); rows describe **delivery-mode** ownership distinct from C-level **function** ownership. |
| Project anchors created in the same tranche as leaf processes (chicken-and-egg) | Apply script writes project rows first, leaf rows second; validator runs after all writes are done. |
| `org_uuid` collision | UUID4 generation has 2^122 namespace; collision probability negligible. |

## Operator approval checklist (canonical-CSV gate)

Before this tranche is applied to `baseline_organisation.csv` + `process_list.csv`, operator confirms:

1. ☐ **3 sub-mark Lead rows** at access level 4 reporting to O5-1 are the right position (NOT under CTO / CMO / Holistik Researcher; sub-marks are delivery modes that cut across C-level functions).
2. ☐ **`org_id` allocation** (`org_066`, `org_067`, `org_068`) is acceptable, or operator wants different IDs.
3. ☐ **16 leaf processes** distribution across role owners (Brand Manager × 9, Holistik Researcher × 4, Legal Counsel × 2, Talent × 1) is correct, or operator wants re-distribution.
4. ☐ **4 IntelligenceOps processes** owned by `Holistik Researcher` is correct (some operators might prefer a dedicated `Intelligence Officer` role).
5. ☐ **B9-B11 placeholder** (`Brand Manager` until `Engagement Manager` exists) is acceptable as-is, or operator wants `Engagement Manager` added in this tranche.
6. ☐ **4 project anchor rows** as additional infrastructure is acceptable.
7. ☐ **Item-ID convention** (`tbi_mkt_prc_*`, `hol_res_prc_*`, `hol_eng_prc_*`, `hol_lgl_prc_*`, `tbi_ppl_prc_*`) is consistent with existing convention.

If any item is ambiguous, the operator's response proposes the right change; the agent applies and re-presents.

## Cross-references

- Master tranche file (to be created on operator approval): `docs/wip/planning/66-brand-vision-ops-sweep/reports/p3-canonical-csv-tranche-applied-<YYYY-MM-DD>.md` documenting actual UUIDs assigned + apply log.
- I66 master-roadmap §"P3 — Ops, process, organization, catalog, SOPs"
- `akos-governance-remediation.mdc` §"Canonical CSV gates"
- `SOP-META_PROCESS_MGMT_001.md` §4.2-4.3
- D-IH-66-E (service catalog), D-IH-66-F (IntelligenceOps SOPs), D-IH-66-G (Engagement ops SOPs)
