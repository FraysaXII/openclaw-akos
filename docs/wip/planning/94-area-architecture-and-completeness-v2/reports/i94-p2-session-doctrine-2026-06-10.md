---
authored: 2026-06-10
tranche: I94-P2-exec-catalog-T1
parent_initiative: INIT-OPENCLAW_AKOS-94
upstream_ssot: i94-operations-operational-sweep-thinking-synthesis-2026-06-10.md
ratifying_decisions:
  - D-IH-94-A
operator_ratification:
  q1_scope: B_full_sweep
  q2_priority: automation-first
  q3_capacity: 6-8h_per_day_until_gtm
---

# I94 P2 — executable catalog T1 session doctrine (2026-06-10)

Binding execution card for automation-first SOP+runbook pairing (12 processes).

## Paired processes (T1)

| # | Catalog id | SOP | Runbook |
|:---:|:---|:---|:---|
| 1 | `pmo_wip_dashboard_render` | `SOP-PMO_WIP_DASHBOARD_RENDER_001.md` | `scripts/render_wip_dashboard.py` |
| 2 | `pmo_operator_inbox_render` | `SOP-PMO_OPERATOR_INBOX_RENDER_001.md` | `scripts/render_operator_inbox.py` |
| 3 | `operational_cohesion_index_render` | `SOP-PMO_OPERATIONAL_COHESION_INDEX_RENDER_001.md` | `scripts/render_operational_cohesion_index.py` |
| 4 | `initiative_program_anchors` | `SOP-PMO_INITIATIVE_PROGRAM_ANCHORS_001.md` | `scripts/pmo_program_anchor_backfill.py` |
| 5 | `external_adviser_router` | `SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md` | `scripts/export_adviser_handoff.py` |
| 6 | `engagement_scaffold` | `SOP-ENGAGEMENT_SCAFFOLDING_001.md` | `scripts/scaffold_engagement.py` |
| 7 | `compliance_mirror_emit_trigger` | `SOP-OPS_MIRROR_EMIT_TRIGGER_001.md` | `scripts/verify.py` (`compliance_mirror_emit`) |
| 8 | `area_completeness_sweep` | `SOP-OPS_AREA_COMPLETENESS_SWEEP_001.md` | `scripts/validate_area_completeness.py` |
| 9 | `initiative_harmonisation` | `SOP-INITIATIVE_PROCESS_HARMONISATION_001.md` | `scripts/validate_initiative_registry.py` |
| 10 | `vault_promotion_gate` | `SOP-PMO_VAULT_PROMOTION_GATE_001.md` | `scripts/validate_hlk.py` |
| 11 | `revops_qbr_cycle` | `SOP-REVOPS_QBR_001.md` | `scripts/validate_engagement_template_registry.py` |
| 12 | `service_catalog_maintenance` | `SOP-SERVICE_MGMT_001.md` | `scripts/validate_hlk.py` |

SSOT metadata: [`OPERATIONS_PROCESS_CATALOG.yaml`](../../../../references/hlk/v3.0/Admin/O5-1/Operations/canonicals/OPERATIONS_PROCESS_CATALOG.yaml).

## AREA-09 delta note

`validate_area_completeness.py` probes `process_list.csv` columns `sop_path` + `runbook_path` (not yet in `PROCESS_LIST_FIELDNAMES`). Vault pairing is complete in catalog + SOP frontmatter; **scorer remains 0/46** until operator-gated process_list column tranche. Forward debt documented — not a P2 blocker (AREA-09 is enhancing).

## Verification matrix (P2)

```powershell
py scripts/validate_hlk.py
py scripts/validate_area_completeness.py --area Operations --matrix
py scripts/validate_area_completeness.py --area Operations --next
py scripts/verify.py pre_commit_fast
```

## Gates honored

- No `process_list.csv` / `baseline_organisation.csv` edits
- No IntelligenceOps file moves

## P3 preview (do not start in P2)

- IntelligenceOps SOPs → Research (file-move + inline-ratify)
- Engagement subfolder FK (AREA-16)
- business-strategy forward tracker (I95 L6)
