---
authored: 2026-06-10
tranche: I94-P2-research-mini
parent_initiative: INIT-OPENCLAW_AKOS-94
research_class: internal_sweep
novel_framing: false
---

# I94 P0 research mini-note — P2 executable catalog (2026-06-10)

Internal sweep only (no external ledger extension). Confirms pairing targets against existing Operations `process_list` rows and `scripts/`.

## Operations process_list inventory

- **46** `item_granularity=process` rows with `area=Operations` (AREA-09 denominator).
- **0** rows carry dedicated `sop_path` / `runbook_path` columns — pairing prose lives in `description` / `instructions` for some rows (e.g. `hol_ops_dtp_72`, RevOps QBR/scaffold rows) but the area scorer does not parse those fields yet.

## Script reuse (automation-first)

| Charter priority | Existing script | SOP before P2 |
|:---|:---|:---|
| WIP render | `render_wip_dashboard.py` | None (docstring only) |
| Inbox render | `render_operator_inbox.py` | None |
| Cohesion index | `render_operational_cohesion_index.py` | Doctrine pairing only |
| Program anchors | `pmo_program_anchor_backfill.py` | `SOP-PMO_INITIATIVE_PROGRAM_ANCHORS_001` |
| Adviser router | `export_adviser_handoff.py` | `SOP-EXTERNAL_ADVISER_ENGAGEMENT_001` (no linked_runbooks) |
| Engagement scaffold | `scaffold_engagement.py` | `SOP-ENGAGEMENT_SCAFFOLDING_001` |
| Mirror emit | `verify.py compliance_mirror_emit` | Tech SOP only |
| Area sweep | `validate_area_completeness.py` | People meta-SOP only |
| Harmonisation | `validate_initiative_registry.py` | SOP without runbook FK |
| Vault promotion | `validate_hlk.py` | SOP without runbook FK |
| RevOps QBR | template validators | `SOP-REVOPS_QBR_001` |
| Service catalog | `validate_hlk.py` | `SOP-SERVICE_MGMT_001` without runbook FK |

## Conclusion

No novel external research required — I72/I86/I93 precedents cover executable catalog pairing. P2 mints `OPERATIONS_PROCESS_CATALOG.yaml` + five minimal PMO SOPs + frontmatter/runbook cross-refs on seven existing SOPs. AREA-09 scorer uplift deferred to process_list column tranche (operator gate).
