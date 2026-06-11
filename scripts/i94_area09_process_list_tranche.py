#!/usr/bin/env python3
"""I94 P3 AREA-09 process_list pairing tranche (operator-ratified 2026-06-10)."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_process_csv import PROCESS_LIST_FIELDNAMES, normalize_process_row, write_process_csv

PL = REPO_ROOT / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/process_list.csv"
VAULT = "docs/references/hlk/v3.0/Admin/O5-1/Operations"

PAIRINGS: dict[str, tuple[str, str]] = {
    "ops_pmo_dtp_wip_dashboard_render_001": (
        f"{VAULT}/PMO/canonicals/SOP-PMO_WIP_DASHBOARD_RENDER_001.md",
        "scripts/render_wip_dashboard.py",
    ),
    "ops_pmo_dtp_operator_inbox_render_001": (
        f"{VAULT}/PMO/canonicals/SOP-PMO_OPERATOR_INBOX_RENDER_001.md",
        "scripts/render_operator_inbox.py",
    ),
    "ops_pmo_dtp_cohesion_quarterly_001": (
        f"{VAULT}/PMO/canonicals/SOP-PMO_OPERATIONAL_COHESION_INDEX_RENDER_001.md",
        "scripts/render_operational_cohesion_index.py",
    ),
    "hol_ops_dtp_72": (
        f"{VAULT}/PMO/canonicals/SOP-PMO_INITIATIVE_PROGRAM_ANCHORS_001.md",
        "scripts/pmo_program_anchor_backfill.py",
    ),
    "hol_opera_dtp_311": (
        f"{VAULT}/PMO/SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md",
        "scripts/export_adviser_handoff.py",
    ),
    "tbi_ops_dtp_revops_engagement_scaffold_001": (
        f"{VAULT}/RevOps/canonicals/SOP-ENGAGEMENT_SCAFFOLDING_001.md",
        "scripts/scaffold_engagement.py",
    ),
    "ops_pmo_dtp_mirror_emit_trigger_001": (
        f"{VAULT}/PMO/canonicals/SOP-OPS_MIRROR_EMIT_TRIGGER_001.md",
        "scripts/verify.py",
    ),
    "ops_pmo_dtp_area_completeness_sweep_001": (
        f"{VAULT}/PMO/canonicals/SOP-OPS_AREA_COMPLETENESS_SWEEP_001.md",
        "scripts/validate_area_completeness.py",
    ),
    "ops_pmo_dtp_initiative_harmonisation_001": (
        f"{VAULT}/PMO/SOP-INITIATIVE_PROCESS_HARMONISATION_001.md",
        "scripts/validate_initiative_registry.py",
    ),
    "ops_pmo_dtp_vault_promotion_gate_001": (
        f"{VAULT}/PMO/canonicals/SOP-PMO_VAULT_PROMOTION_GATE_001.md",
        "scripts/validate_hlk.py",
    ),
    "tbi_ops_dtp_revops_qbr_001": (
        f"{VAULT}/RevOps/canonicals/SOP-REVOPS_QBR_001.md",
        "scripts/validate_engagement_template_registry.py",
    ),
    "ops_smo_dtp_service_catalog_mtnce_001": (
        f"{VAULT}/SMO/canonicals/SOP-SERVICE_MGMT_001.md",
        "scripts/validate_hlk.py",
    ),
}

P7_T2_PAIRINGS: dict[str, tuple[str, str]] = {
    "hol_opera_dtp_310": (
        f"{VAULT}/PMO/canonicals/SOP-PMO_INITIATIVE_PROGRAM_ANCHORS_001.md",
        "scripts/pmo_program_anchor_backfill.py",
    ),
    "thi_opera_dtp_201": (
        f"{VAULT}/PMO/SOP-INITIATIVE_GOVERNANCE_001.md",
        "scripts/validate_initiative_registry.py",
    ),
    "thi_opera_dtp_220": (
        f"{VAULT}/PMO/SOP-INITIATIVE_GOVERNANCE_001.md",
        "scripts/validate_initiative_registry.py",
    ),
    "hol_opera_dtp_300": (
        f"{VAULT}/PMO/canonicals/SOP-PMO_OPERATIONAL_COHESION_INDEX_RENDER_001.md",
        "scripts/render_operational_cohesion_index.py",
    ),
    "thi_opera_dtp_250": (
        f"{VAULT}/PMO/canonicals/SOP-PMO_OPERATIONAL_COHESION_INDEX_RENDER_001.md",
        "scripts/render_operational_cohesion_index.py",
    ),
    "hol_opera_dtp_148": (
        f"{VAULT}/PMO/SOP-INITIATIVE_PROCESS_HARMONISATION_001.md",
        "scripts/validate_initiative_registry.py",
    ),
    "hol_opera_dtp_103": (
        f"{VAULT}/PMO/canonicals/SOP-PMO_VAULT_PROMOTION_GATE_001.md",
        "scripts/validate_hlk.py",
    ),
    "tbi_ops_dtp_revops_revenue_rollup_001": (
        f"{VAULT}/RevOps/canonicals/SOP-REVENUE_ROLLUP_001.md",
        "scripts/validate_revops_spine.py",
    ),
    "tbi_ops_dtp_revops_persona_audit_001": (
        f"{VAULT}/RevOps/canonicals/SOP-PERSONA_AUDIT_001.md",
        "scripts/validate_persona_registry.py",
    ),
    "tbi_ops_dtp_revops_crm_sync_001": (
        f"{VAULT}/RevOps/canonicals/SOP-REVOPS_CRM_SYNC_001.md",
        "scripts/revops_dispatch.py",
    ),
    "tbi_ops_dtp_revops_regulator_checkpoint_001": (
        f"{VAULT}/RevOps/canonicals/SOP-REVOPS_REGULATOR_CHECKPOINT_001.md",
        "scripts/revops_dispatch.py",
    ),
    "tbi_ops_dtp_revops_media_review_001": (
        f"{VAULT}/RevOps/canonicals/SOP-REVOPS_MEDIA_REVIEW_001.md",
        "scripts/revops_dispatch.py",
    ),
    "thi_opera_dtp_288": (
        f"{VAULT}/RevOps/canonicals/SOP-FINOPS_BRIDGE_001.md",
        "scripts/revops_dispatch.py",
    ),
    "hol_ops_dtp_71": (
        f"{VAULT}/Engagement/SOP-ENG_ENGAGEMENT_DESIGN_001.md",
        "scripts/scaffold_engagement.py",
    ),
    "hol_eng_prc_estimation_001": (
        f"{VAULT}/Engagement/canonicals/SOP-ENG_ESTIMATION_DISCIPLINE_001.md",
        "scripts/estimate_engagement.py",
    ),
    "thi_opera_dtp_97": (
        f"{VAULT}/Engagement/SOP-ENG_ENGAGEMENT_DESIGN_001.md",
        "scripts/scaffold_engagement.py",
    ),
    "thi_opera_dtp_121": (
        f"{VAULT}/Engagement/SOP-ENG_ENGAGEMENT_DESIGN_001.md",
        "scripts/scaffold_engagement.py",
    ),
    "thi_opera_dtp_129": (
        f"{VAULT}/Engagement/SOP-ENG_ENGAGEMENT_DESIGN_001.md",
        "scripts/scaffold_engagement.py",
    ),
    "hol_opera_dtp_312": (
        f"{VAULT}/PMO/SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md",
        "scripts/validate_adviser_questions.py",
    ),
    "hol_ops_pis_3": (
        f"{VAULT}/PMO/SOP-PMO_PROCESS_LIST_CSV_MAINTENANCE_001.md",
        "scripts/validate_hlk.py",
    ),
}

ALL_PAIRINGS = {**PAIRINGS, **P7_T2_PAIRINGS}

NEW_ROWS: list[dict[str, str]] = [
    {
        "type": "Internal",
        "orientation": "Employee",
        "entity": "Holistika",
        "area": "Operations",
        "role_parent_1": "PMO",
        "role_owner": "PMO",
        "item_parent_2": "Think Big Operational Excellence",
        "item_parent_2_id": "thi_opera_prj_1",
        "item_parent_1": "Program Management",
        "item_parent_1_id": "hol_opera_dtp_148",
        "item_name": "PMO WIP dashboard render",
        "item_id": "ops_pmo_dtp_wip_dashboard_render_001",
        "item_granularity": "process",
        "description": "Auto-render WIP_DASHBOARD.md from initiative master-roadmap frontmatter (I94 P2 T1).",
        "last_review_at": "2026-06-10",
        "last_review_by": "PMO",
        "last_review_decision_id": "D-IH-94-A",
        "methodology_version_at_review": "v3.1",
        "cadence_type": "scheduled",
        "inherited_pattern_id": "pattern_paired_sop_runbook",
    },
    {
        "type": "Internal",
        "orientation": "Employee",
        "entity": "Holistika",
        "area": "Operations",
        "role_parent_1": "PMO",
        "role_owner": "PMO",
        "item_parent_2": "Think Big Operational Excellence",
        "item_parent_2_id": "thi_opera_prj_1",
        "item_parent_1": "Program Management",
        "item_parent_1_id": "hol_opera_dtp_148",
        "item_name": "PMO operator inbox render",
        "item_id": "ops_pmo_dtp_operator_inbox_render_001",
        "item_granularity": "process",
        "description": "Ranked OPERATOR_INBOX.md from OPS_REGISTER.csv (I94 P2 T1).",
        "last_review_at": "2026-06-10",
        "last_review_by": "PMO",
        "last_review_decision_id": "D-IH-94-A",
        "methodology_version_at_review": "v3.1",
        "cadence_type": "scheduled",
        "inherited_pattern_id": "pattern_paired_sop_runbook",
    },
    {
        "type": "Internal",
        "orientation": "Employee",
        "entity": "Holistika",
        "area": "Operations",
        "role_parent_1": "PMO",
        "role_owner": "PMO",
        "item_parent_2": "Think Big Operational Excellence",
        "item_parent_2_id": "thi_opera_prj_1",
        "item_parent_1": "Holistika Process Governance Framework",
        "item_parent_1_id": "hol_ops_pgf_1",
        "item_name": "Compliance mirror emit trigger (Operations plane)",
        "item_id": "ops_pmo_dtp_mirror_emit_trigger_001",
        "item_granularity": "process",
        "description": "Operations triggers git-to-SQL compliance mirror emit; operator applies via two-plane gate.",
        "last_review_at": "2026-06-10",
        "last_review_by": "PMO",
        "last_review_decision_id": "D-IH-94-A",
        "methodology_version_at_review": "v3.1",
        "cadence_type": "gated_operator",
        "inherited_pattern_id": "pattern_dataops_discipline",
    },
    {
        "type": "Internal",
        "orientation": "Employee",
        "entity": "Holistika",
        "area": "Operations",
        "role_parent_1": "PMO",
        "role_owner": "COO",
        "item_parent_2": "Think Big Operational Excellence",
        "item_parent_2_id": "thi_opera_prj_1",
        "item_parent_1": "Holistika Process Governance Framework",
        "item_parent_1_id": "hol_ops_pgf_1",
        "item_name": "Operations area completeness sweep",
        "item_id": "ops_pmo_dtp_area_completeness_sweep_001",
        "item_granularity": "process",
        "description": "16-component matrix + --next worklist for Operations tier gate (I94).",
        "last_review_at": "2026-06-10",
        "last_review_by": "COO",
        "last_review_decision_id": "D-IH-94-A",
        "methodology_version_at_review": "v3.1",
        "cadence_type": "event_triggered",
        "inherited_pattern_id": "pattern_area_buildout",
    },
    {
        "type": "Internal",
        "orientation": "Employee",
        "entity": "Holistika",
        "area": "Operations",
        "role_parent_1": "PMO",
        "role_owner": "PMO",
        "item_parent_2": "Think Big Operational Excellence",
        "item_parent_2_id": "thi_opera_prj_1",
        "item_parent_1": "Holistika Process Governance Framework",
        "item_parent_1_id": "hol_ops_pgf_1",
        "item_name": "Initiative governance harmonisation",
        "item_id": "ops_pmo_dtp_initiative_harmonisation_001",
        "item_granularity": "process",
        "description": "manifests_processes FK between INITIATIVE_REGISTRY and process_list (D-IH-59-G).",
        "last_review_at": "2026-06-10",
        "last_review_by": "PMO",
        "last_review_decision_id": "D-IH-94-A",
        "methodology_version_at_review": "v3.1",
        "cadence_type": "event_triggered",
        "inherited_pattern_id": "pattern_paired_sop_runbook",
    },
    {
        "type": "Internal",
        "orientation": "Employee",
        "entity": "Holistika",
        "area": "Operations",
        "role_parent_1": "PMO",
        "role_owner": "PMO",
        "item_parent_2": "Think Big Operational Excellence",
        "item_parent_2_id": "thi_opera_prj_1",
        "item_parent_1": "Program Management",
        "item_parent_1_id": "hol_opera_dtp_148",
        "item_name": "Vault promotion gate",
        "item_id": "ops_pmo_dtp_vault_promotion_gate_001",
        "item_granularity": "process",
        "description": "Promote stable WIP intent into process_list with operator CSV gate.",
        "last_review_at": "2026-06-10",
        "last_review_by": "PMO",
        "last_review_decision_id": "D-IH-94-A",
        "methodology_version_at_review": "v3.1",
        "cadence_type": "gated_operator",
        "inherited_pattern_id": "pattern_paired_sop_runbook",
    },
    {
        "type": "Internal",
        "orientation": "Employee",
        "entity": "Think Big",
        "area": "Operations",
        "role_parent_1": "COO",
        "role_owner": "SMO",
        "item_parent_2": "Think Big PMO and operating model program",
        "item_parent_2_id": "hlk_prog_think_big_pmo",
        "item_parent_1": "Service catalog and capability definition",
        "item_parent_1_id": "gtm_ws_service_catalog",
        "item_name": "Service catalog maintenance (SMO)",
        "item_id": "ops_smo_dtp_service_catalog_mtnce_001",
        "item_granularity": "process",
        "description": "Weekly SERVICE_CATALOG.csv + SLA_MATRIX.md review rhythm.",
        "last_review_at": "2026-06-10",
        "last_review_by": "SMO",
        "last_review_decision_id": "D-IH-94-A",
        "methodology_version_at_review": "v3.1",
        "cadence_type": "scheduled",
        "inherited_pattern_id": "pattern_paired_sop_runbook",
    },
]


def main() -> int:
    rows: list[dict[str, str]] = []
    with PL.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            rows.append(normalize_process_row(row))

    existing_ids = {r["item_id"] for r in rows}
    for tpl in NEW_ROWS:
        if tpl["item_id"] not in existing_ids:
            row = {k: "" for k in PROCESS_LIST_FIELDNAMES}
            row.update(tpl)
            rows.append(row)

    for row in rows:
        iid = (row.get("item_id") or "").strip()
        if iid in ALL_PAIRINGS:
            sop, rb = ALL_PAIRINGS[iid]
            row["sop_path"] = sop
            row["runbook_path"] = rb

    write_process_csv(PL, rows)
    paired_ops = sum(
        1
        for r in rows
        if (r.get("area") or "").strip() == "Operations"
        and (r.get("item_granularity") or "").strip() == "process"
        and (r.get("sop_path") or "").strip()
        and (r.get("runbook_path") or "").strip()
    )
    print(f"Wrote {len(rows)} rows; Operations paired processes={paired_ops}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
