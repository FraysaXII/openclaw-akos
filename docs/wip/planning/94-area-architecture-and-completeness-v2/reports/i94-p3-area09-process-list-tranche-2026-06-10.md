---
authored: 2026-06-10
tranche: I94-P3-AREA-09
parent_initiative: INIT-OPENCLAW_AKOS-94
ratifying_decisions:
  - D-IH-94-A
operator_gate: ratified_both
---

# I94 P3 AREA-09 process_list pairing tranche (2026-06-10)

## Goal

Uplift the **paired SOP+runbook scorer** (`validate_area_completeness.py` AREA-09)
for Operations from **0/46** to **12/46** by extending `process_list.csv` with
`sop_path` and `runbook_path` columns and wiring the 12 P2 catalog processes.

## Schema change

| Field | Authority | Notes |
|:---|:---|:---|
| `sop_path` | `akos/hlk_process_csv.py` `PROCESS_LIST_FIELDNAMES` | Vault-relative SOP path |
| `runbook_path` | same | Repo-relative runbook script |

Non-Operations rows receive empty defaults; mirror DDL deferred (two-plane gate).

## Rows touched

**7 new Operations process rows** (distinct `item_id` per catalog entry):

| item_id | SOP | Runbook |
|:---|:---|:---|
| `ops_pmo_dtp_wip_dashboard_render_001` | SOP-PMO_WIP_DASHBOARD_RENDER_001 | `render_wip_dashboard.py` |
| `ops_pmo_dtp_operator_inbox_render_001` | SOP-PMO_OPERATOR_INBOX_RENDER_001 | `render_operator_inbox.py` |
| `ops_pmo_dtp_mirror_emit_trigger_001` | SOP-OPS_MIRROR_EMIT_TRIGGER_001 | `verify.py` |
| `ops_pmo_dtp_area_completeness_sweep_001` | SOP-OPS_AREA_COMPLETENESS_SWEEP_001 | `validate_area_completeness.py` |
| `ops_pmo_dtp_initiative_harmonisation_001` | SOP-INITIATIVE_PROCESS_HARMONISATION_001 | `validate_initiative_registry.py` |
| `ops_pmo_dtp_vault_promotion_gate_001` | SOP-PMO_VAULT_PROMOTION_GATE_001 | `validate_hlk.py` |
| `ops_smo_dtp_service_catalog_mtnce_001` | SOP-SERVICE_MGMT_001 | `validate_hlk.py` |

**5 existing rows updated** with pairing paths:

| item_id | Notes |
|:---|:---|
| `ops_pmo_dtp_cohesion_quarterly_001` | Cohesion index render |
| `hol_ops_dtp_72` | Program anchors |
| `hol_opera_dtp_311` | External adviser router |
| `tbi_ops_dtp_revops_engagement_scaffold_001` | Engagement scaffold |
| `tbi_ops_dtp_revops_qbr_001` | RevOps QBR |

## Out of scope (by design)

| Catalog id | Reason |
|:---|:---|
| `env_tech_dtp_compliance_mirror_dml_001` | Tech area, not Operations AREA-09 |
| `hol_peopl_dtp_area_governance_001` | People area |
| Portfolio SSOT row `hol_opera_dtp_310` | Workstream; split into dedicated process rows |

## Verification

```powershell
py scripts/check_process_list_header.py
py scripts/validate_hlk.py
py scripts/validate_area_completeness.py --area Operations --matrix
```

**Post-tranche AREA-09:** 12/46 paired (26% of Operations processes).

## Script

`scripts/i94_area09_process_list_tranche.py` — idempotent apply; operator-ratified 2026-06-10.
