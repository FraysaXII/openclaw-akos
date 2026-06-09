#!/usr/bin/env python3
"""One-off seed generator for CANONICAL_GOVERNANCE_REGISTRY.csv (P95-GOV-1).

Run from repo root::

    py scripts/_one_off/seed_canonical_governance_registry_p95_gov1.py

Idempotent: overwrites the registry CSV with 74 vault-inventory rows per charter §2.
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))

from akos.hlk_canonical_governance_registry_csv import (  # noqa: E402
    CANONICAL_GOVERNANCE_REGISTRY_FIELDNAMES,
    EXPECTED_VAULT_CSV_COUNT,
)

VAULT_ROOT = REPO / "docs" / "references" / "hlk" / "v3.0"
OUT = (
    REPO
    / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions"
    / "CANONICAL_GOVERNANCE_REGISTRY.csv"
)
CANONICAL_REGISTRY = (
    REPO
    / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/CANONICAL_REGISTRY.csv"
)

# Charter §2 overrides keyed by repo-relative csv_path (posix).
# Keys omitted fall back to path heuristics.
CHARTER: dict[str, dict[str, str]] = {
    "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/baseline_organisation.csv": {
        "asset_class": "compliance_mirror",
        "plane1_validator": "validate_hlk.py",
        "plane1_in_validate_hlk": "true",
        "plane2_mirror_table": "compliance.baseline_organisation_mirror",
        "plane2_sync_policy": "active",
        "plane2_emit_profile": "main",
        "precedence_registered": "true",
        "canonical_registry_id": "baseline_organisation",
        "enum_parity_required": "true",
        "delete_reconcile_pk": "org_id",
        "owning_area": "People_Compliance",
        "owning_role": "Compliance",
    },
    "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/process_list.csv": {
        "asset_class": "compliance_mirror",
        "plane1_validator": "validate_hlk.py",
        "plane1_in_validate_hlk": "true",
        "plane2_mirror_table": "compliance.process_list_mirror",
        "plane2_sync_policy": "active",
        "plane2_emit_profile": "main",
        "precedence_registered": "true",
        "canonical_registry_id": "process_list",
        "enum_parity_required": "true",
        "delete_reconcile_pk": "item_id",
        "owning_area": "People_Compliance",
        "owning_role": "Compliance",
    },
    "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv": {
        "plane1_validator": "validate_decision_register.py",
        "plane2_emit_profile": "main",
        "canonical_registry_id": "decision_register",
    },
    "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_REGISTRY.csv": {
        "plane1_validator": "validate_initiative_registry.py",
        "plane2_emit_profile": "main",
        "canonical_registry_id": "initiative_registry",
    },
    "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/OPS_REGISTER.csv": {
        "plane1_validator": "validate_ops_register.py",
        "plane2_emit_profile": "main",
        "canonical_registry_id": "ops_register",
    },
    "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/CYCLE_REGISTER.csv": {
        "plane1_validator": "validate_cycle_register.py",
        "plane2_emit_profile": "main",
        "canonical_registry_id": "cycle_register",
    },
    "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/REPOSITORY_REGISTRY.csv": {
        "plane1_validator": "validate_repository_registry.py",
        "plane2_emit_profile": "main",
        "canonical_registry_id": "repository_registry",
    },
    "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/REPO_HEALTH_SNAPSHOT.csv": {
        "plane1_validator": "validate_repo_health_snapshot.py",
        "plane2_emit_profile": "main",
        "canonical_registry_id": "repo_health_snapshot",
    },
    "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/CANONICAL_REGISTRY.csv": {
        "asset_class": "git_only",
        "plane1_validator": "validate_canonical_registry.py",
        "plane1_in_validate_hlk": "false",
        "plane2_sync_policy": "git_only",
        "plane2_emit_profile": "none",
        "precedence_registered": "true",
        "canonical_registry_id": "",
        "enum_parity_required": "false",
        "notes": "Meta-registry; not mirrored; P95-GOV-2 index backfill",
    },
    "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/finops/FINOPS_COUNTERPARTY_REGISTER.csv": {
        "asset_class": "finops_mirror",
        "plane1_validator": "validate_finops_counterparty_register.py",
        "plane2_emit_profile": "main",
        "canonical_registry_id": "finops_counterparty_register",
    },
    "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/techops/COMPONENT_SERVICE_MATRIX.csv": {
        "asset_class": "forward_charter",
        "plane1_validator": "validate_component_service_matrix.py",
        "plane2_sync_policy": "forward_charter",
        "plane2_emit_profile": "none",
        "canonical_registry_id": "component_service_matrix",
        "notes": "Forward-charter until DDL+emit; P95-GOV-7 optional",
    },
    "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/COUNTRY_WORK_CALENDAR.csv": {
        "plane1_validator": "validate_compliance_schema_drift.py",
        "plane1_in_validate_hlk": "false",
        "plane2_emit_profile": "gap_splice",
        "canonical_registry_id": "country_work_calendar",
        "notes": "Gap-splice OPS-86-15; schema-drift registry",
    },
    "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/ENGAGEMENT_REGISTRY.csv": {
        "plane1_validator": "validate_canonical_registry.py",
        "plane1_in_validate_hlk": "false",
        "plane2_emit_profile": "none",
        "canonical_registry_id": "engagement_registry",
        "notes": "DDL exists; emit unclear; P95-GOV-5 gap closure",
    },
    "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/KNOWLEDGE_PAIRING_REGISTRY.csv": {
        "asset_class": "git_only",
        "plane2_sync_policy": "git_only",
        "plane2_emit_profile": "none",
        "plane1_validator": "validate_knowledge_pairing_registry.py",
        "canonical_registry_id": "",
        "enum_parity_required": "false",
    },
    "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/BUILDOUT_BACKLOG.csv": {
        "asset_class": "git_only",
        "plane2_sync_policy": "git_only",
        "plane2_emit_profile": "none",
        "plane1_validator": "validate_buildout_backlog_registry.py",
        "canonical_registry_id": "",
        "enum_parity_required": "false",
    },
    "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/POC_TO_COMMERCIAL_MAP.csv": {
        "asset_class": "git_only",
        "plane2_sync_policy": "git_only",
        "plane1_validator": "validate_capability_registry.py",
        "plane1_in_validate_hlk": "true",
        "precedence_registered": "false",
        "canonical_registry_id": "poc_to_commercial_map",
        "enum_parity_required": "false",
        "notes": "Partial PRECEDENCE; via capability/use-case",
    },
    "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/MADEIRA_AIC_PER_TASK_REGISTRY.csv": {
        "asset_class": "git_only",
        "plane2_sync_policy": "git_only",
        "plane1_validator": "validate_madeira_aic_per_task.py",
        "canonical_registry_id": "",
        "enum_parity_required": "false",
    },
    "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/AIC_CAPABILITY_IMPLEMENTATION_MATRIX.csv": {
        "asset_class": "git_only",
        "plane2_sync_policy": "git_only",
        "plane1_validator": "validate_aic_capability_implementation_matrix.py",
        "enum_parity_required": "false",
    },
    "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/USE_CASE_ARCHIVE.csv": {
        "asset_class": "git_only",
        "plane2_sync_policy": "git_only",
        "plane1_validator": "validate_use_case_archive.py",
        "enum_parity_required": "false",
    },
    "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/OUTPUT_TYPE_REGISTRY.csv": {
        "plane1_validator": "validate_output_architecture_registries.py",
        "plane2_emit_profile": "none",
        "notes": "Mirror DDL; extend main/gap in P95-GOV-5",
    },
    "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/ARTIFACT_CLASS_REGISTRY.csv": {
        "plane1_validator": "validate_output_architecture_registries.py",
        "plane2_emit_profile": "none",
    },
    "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/COMPONENT_PRIMITIVE_REGISTRY.csv": {
        "plane1_validator": "validate_output_architecture_registries.py",
        "plane2_emit_profile": "none",
    },
    "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/CAPABILITY_REGISTRY.csv": {
        "plane2_emit_profile": "gap_splice",
        "plane1_validator": "validate_capability_registry.py",
    },
    "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/CAPABILITY_CONFIDENCE_REGISTRY.csv": {
        "plane2_emit_profile": "gap_splice",
        "plane1_validator": "validate_capability_confidence_registry.py",
    },
    "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/AIC_REGISTRY.csv": {
        "plane2_emit_profile": "gap_splice",
        "plane1_validator": "validate_aic_registry.py",
    },
    "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/AUDIENCE_REGISTRY.csv": {
        "plane2_emit_profile": "gap_splice",
        "plane1_validator": "validate_audience_registry.py",
    },
    # Data/Architecture HCAM pair
    "docs/references/hlk/v3.0/Admin/O5-1/Data/Architecture/canonicals/dimensions/ENTITY_CATALOG.csv": {
        "asset_class": "graph_projection",
        "plane1_validator": "validate_canonical_articulation.py",
        "plane2_sync_policy": "graph_projection",
        "plane2_emit_profile": "none",
        "precedence_registered": "false",
        "enum_parity_required": "false",
        "owning_area": "Data_Architecture",
        "owning_role": "Data Architect",
        "notes": "T1 git + T3 Neo4j; no T2 mirror per D-IH-95-B",
    },
    "docs/references/hlk/v3.0/Admin/O5-1/Data/Architecture/canonicals/dimensions/CANONICAL_RELATIONSHIP_REGISTRY.csv": {
        "asset_class": "graph_projection",
        "plane1_validator": "validate_canonical_articulation.py",
        "plane2_sync_policy": "graph_projection",
        "plane2_emit_profile": "none",
        "precedence_registered": "false",
        "enum_parity_required": "false",
        "owning_area": "Data_Architecture",
        "owning_role": "Data Architect",
        "notes": "Plus validate_fk_verb_coverage.py; P95-GOV-2 index backfill",
    },
    "docs/references/hlk/v3.0/Admin/O5-1/Data/Architecture/canonicals/dimensions/METRICS_REGISTRY.csv": {
        "asset_class": "git_only",
        "plane2_sync_policy": "git_only",
        "plane1_validator": "validate_metrics_registry.py",
        "enum_parity_required": "false",
        "owning_area": "Data_Architecture",
        "owning_role": "Data Architect",
    },
    "docs/references/hlk/v3.0/Admin/O5-1/Data/Architecture/canonicals/dimensions/SUPABASE_MODULE_REGISTRY.csv": {
        "asset_class": "git_only",
        "plane2_sync_policy": "git_only",
        "plane1_validator": "validate_supabase_module_registry.py",
        "precedence_registered": "false",
        "enum_parity_required": "false",
        "owning_area": "Data_Architecture",
        "owning_role": "Data Architect",
        "notes": "P95-GOV-2 PRECEDENCE backfill",
    },
    "docs/references/hlk/v3.0/Admin/O5-1/Data/Governance/canonicals/dimensions/DATA_CONTRACT_REGISTRY.csv": {
        "asset_class": "data_contract_mirror",
        "plane1_validator": "validate_data_contract_registry.py",
        "plane2_sync_policy": "forward_charter",
        "plane2_emit_profile": "none",
        "owning_area": "Data_Governance",
        "owning_role": "Data Governance Lead",
    },
    "docs/references/hlk/v3.0/Admin/O5-1/Data/Governance/canonicals/dimensions/RPA_ADAPTER_REGISTRY.csv": {
        "plane2_sync_policy": "forward_charter",
        "plane2_emit_profile": "none",
        "plane1_validator": "validate_adapter_registries.py",
        "notes": "9th adapter class; no mirror DDL; P95-GOV-7 optional",
    },
    "docs/references/hlk/v3.0/Admin/O5-1/Finance/Governance/canonicals/dimensions/PRICING_TIER_REGISTRY.csv": {
        "asset_class": "finops_mirror",
        "plane1_validator": "validate_pricing_tier_registry.py",
        "plane2_sync_policy": "forward_charter",
        "plane2_emit_profile": "none",
        "precedence_registered": "false",
        "owning_area": "Finance_Governance",
        "owning_role": "Business Controller",
        "notes": "P95-GOV-2 PRECEDENCE backfill",
    },
    "docs/references/hlk/v3.0/Admin/O5-1/Finance/Governance/canonicals/dimensions/FINOPS_TAX_CALENDAR.csv": {
        "asset_class": "finops_mirror",
        "plane1_validator": "validate_finops_tax_calendar.py",
        "plane2_sync_policy": "forward_charter",
        "plane2_emit_profile": "none",
        "precedence_registered": "false",
        "owning_area": "Finance_Governance",
        "owning_role": "Business Controller",
    },
    "docs/references/hlk/v3.0/Admin/O5-1/Finance/Governance/canonicals/dimensions/FINOPS_PERFORMANCE_OBLIGATION_REGISTRY.csv": {
        "asset_class": "finops_mirror",
        "plane1_validator": "validate_pricing_tier_registry.py",
        "plane1_in_validate_hlk": "false",
        "plane2_sync_policy": "forward_charter",
        "plane2_emit_profile": "none",
        "precedence_registered": "false",
        "owning_area": "Finance_Governance",
        "owning_role": "Business Controller",
        "notes": "Bundled with pricing tier validator",
    },
    # Marketing adapters — DDL exists, no emit
    "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Reach/canonicals/dimensions/EMAIL_ADAPTER_REGISTRY.csv": {
        "plane1_validator": "validate_adapter_registries.py",
        "plane2_emit_profile": "none",
        "notes": "Mirror DDL; emit missing; P95-GOV-5",
    },
    "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Reach/canonicals/dimensions/CRM_ADAPTER_REGISTRY.csv": {
        "plane1_validator": "validate_adapter_registries.py",
        "plane2_emit_profile": "none",
    },
    "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Reach/canonicals/dimensions/COMMUNICATION_ADAPTER_REGISTRY.csv": {
        "plane1_validator": "validate_adapter_registries.py",
        "plane2_emit_profile": "none",
    },
    "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Reach/canonicals/dimensions/SCHEDULING_ADAPTER_REGISTRY.csv": {
        "plane1_validator": "validate_adapter_registries.py",
        "plane2_emit_profile": "none",
    },
    "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Experimentation/canonicals/dimensions/ATTRIBUTION_ADAPTER_REGISTRY.csv": {
        "plane1_validator": "validate_adapter_registries.py",
        "plane2_emit_profile": "none",
        "owning_area": "Marketing_Experimentation",
    },
    "docs/references/hlk/v3.0/Admin/O5-1/Operations/RevOps/canonicals/dimensions/ENGAGEMENT_TEMPLATE_REGISTRY.csv": {
        "plane1_validator": "validate_engagement_template_registry.py",
        "plane2_emit_profile": "none",
        "owning_area": "Operations_RevOps",
        "owning_role": "RevOps Manager",
        "notes": "Mirror DDL; emit missing; P95-GOV-5",
    },
    "docs/references/hlk/v3.0/Admin/O5-1/Operations/RevOps/canonicals/dimensions/REVOPS_ADAPTER_REGISTRY.csv": {
        "plane1_validator": "validate_adapter_registries.py",
        "plane2_emit_profile": "none",
        "owning_area": "Operations_RevOps",
    },
    "docs/references/hlk/v3.0/Admin/O5-1/Operations/RevOps/canonicals/dimensions/BILLING_ADAPTER_REGISTRY.csv": {
        "plane1_validator": "validate_adapter_registries.py",
        "plane2_emit_profile": "none",
        "owning_area": "Operations_RevOps",
    },
    "docs/references/hlk/v3.0/Admin/O5-1/Operations/SMO/canonicals/dimensions/CONTRACT_ADAPTER_REGISTRY.csv": {
        "plane1_validator": "validate_adapter_registries.py",
        "plane2_emit_profile": "none",
        "owning_area": "Operations_SMO",
    },
    "docs/references/hlk/v3.0/Admin/O5-1/Operations/SMO/canonicals/SERVICE_CATALOG.csv": {
        "asset_class": "git_only",
        "plane1_validator": "validate_hlk.py",
        "plane1_in_validate_hlk": "false",
        "plane2_sync_policy": "git_only",
        "plane2_emit_profile": "none",
        "precedence_registered": "false",
        "enum_parity_required": "false",
        "owning_area": "Operations_SMO",
        "owning_role": "SMO Lead",
        "notes": "Validator mint forward-charter P95-GOV-4",
    },
    "docs/references/hlk/v3.0/Admin/O5-1/People/People Operations/canonicals/dimensions/ENGAGEMENT_MODEL_REGISTRY.csv": {
        "plane1_validator": "validate_engagement_model_registry.py",
        "plane2_emit_profile": "scoped_flag",
        "owning_area": "People_People_Operations",
        "owning_role": "People Operations",
    },
    "docs/references/hlk/v3.0/Admin/O5-1/People/People Operations/canonicals/dimensions/COLLABORATOR_SHARE_REGISTRY.csv": {
        "plane1_validator": "validate_collaborator_share.py",
        "plane2_emit_profile": "scoped_flag",
        "owning_area": "People_People_Operations",
    },
    "docs/references/hlk/v3.0/Admin/O5-1/People/People Operations/canonicals/dimensions/PARTNER_OVERLAP_EXCLUSION_CLAUSES.csv": {
        "plane1_validator": "validate_collaborator_share.py",
        "plane2_emit_profile": "scoped_flag",
        "owning_area": "People_People_Operations",
    },
    "docs/references/hlk/v3.0/Admin/O5-1/People/People Operations/canonicals/dimensions/COLLABORATOR_RATE_OVERRIDES.csv": {
        "plane1_validator": "validate_collaborator_share.py",
        "plane2_emit_profile": "scoped_flag",
        "owning_area": "People_People_Operations",
    },
    "docs/references/hlk/v3.0/Admin/O5-1/People/People Operations/canonicals/dimensions/COLLABORATOR_MARKET_RATE_REFERENCE.csv": {
        "plane1_validator": "validate_collaborator_share.py",
        "plane2_emit_profile": "scoped_flag",
        "owning_area": "People_People_Operations",
    },
    "docs/references/hlk/v3.0/Admin/O5-1/People/People Operations/canonicals/dimensions/HOLISTIKA_VENDOR_SERVICES_BILLED.csv": {
        "plane1_validator": "validate_collaborator_share.py",
        "plane2_emit_profile": "scoped_flag",
        "owning_area": "People_People_Operations",
    },
    "docs/references/hlk/v3.0/Admin/O5-1/People/Learning/canonicals/dimensions/LEARNING_OPS_BACKLOG.csv": {
        "asset_class": "git_only",
        "plane1_validator": "validate_hlk.py",
        "plane1_in_validate_hlk": "false",
        "plane2_sync_policy": "git_only",
        "plane2_emit_profile": "none",
        "precedence_registered": "false",
        "enum_parity_required": "false",
        "owning_area": "People_Learning",
        "owning_role": "Learning Lead",
        "notes": "Deferred I73; validator mint P95-GOV-4",
    },
    "docs/references/hlk/v3.0/Admin/O5-1/Research/Intelligence/canonicals/dimensions/INTELLIGENCEOPS_REGISTER.csv": {
        "plane1_validator": "validate_intelligenceops_register.py",
        "plane2_emit_profile": "main",
        "owning_area": "Research_Intelligence",
        "owning_role": "Holistik Researcher",
    },
    "docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/canonicals/dimensions/MADEIRA_TOOL_RBAC.csv": {
        "asset_class": "git_only",
        "plane1_validator": "validate_madeira_tool_rbac.py",
        "plane1_in_validate_hlk": "false",
        "plane2_sync_policy": "git_only",
        "plane2_emit_profile": "none",
        "enum_parity_required": "false",
        "owning_area": "Envoy_Tech_Lab",
        "owning_role": "System Owner",
        "notes": "release-gate strict; P95-GOV-6 HLK dispatch",
    },
    "docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/canonicals/dimensions/MADEIRA_PERSISTENCE_VEHICLE_REGISTRY.csv": {
        "asset_class": "git_only",
        "plane1_validator": "release-gate.py",
        "plane1_in_validate_hlk": "false",
        "plane2_sync_policy": "git_only",
        "plane2_emit_profile": "none",
        "enum_parity_required": "false",
        "owning_area": "Envoy_Tech_Lab",
        "owning_role": "System Owner",
    },
    "docs/references/hlk/v3.0/Envoy Tech Lab/canonicals/dimensions/RENDERING_PIPELINE_REGISTRY.csv": {
        "asset_class": "git_only",
        "plane1_validator": "validate_rendering_pipeline_registry.py",
        "plane2_sync_policy": "git_only",
        "plane2_emit_profile": "none",
        "precedence_registered": "false",
        "enum_parity_required": "false",
        "owning_area": "Envoy_Tech_Lab",
        "owning_role": "System Owner",
        "notes": "Non-O5-1 path split; P95-GOV-2 index backfill",
    },
}

# Default validator map by filename stem for compliance dimensions not explicitly listed.
_STEM_VALIDATORS: dict[str, str] = {
    "TOPIC_REGISTRY": "validate_topic_registry.py",
    "PROGRAM_REGISTRY": "validate_program_registry.py",
    "PERSONA_REGISTRY": "validate_persona_registry.py",
    "PERSONA_SCENARIO_REGISTRY": "validate_persona_scenario_registry.py",
    "CHANNEL_TOUCHPOINT_REGISTRY": "validate_channel_touchpoint_registry.py",
    "SOURCING_REGISTER": "validate_sourcing_register.py",
    "SKILL_REGISTRY": "validate_skill_registry.py",
    "TOUCHPOINT_KIT_CELL_REGISTRY": "validate_touchpoint_kit_cells.py",
    "POLICY_REGISTER": "validate_policy_register.py",
    "GOI_POI_REGISTER": "validate_goipoi_register.py",
    "SUBSTRATE_REGISTRY": "validate_substrate_registry.py",
    "PEOPLE_DESIGN_PATTERN_REGISTRY": "validate_design_pattern_registry.py",
    "ADVISER_ENGAGEMENT_DISCIPLINES": "validate_adviser_disciplines.py",
    "ADVISER_OPEN_QUESTIONS": "validate_adviser_questions.py",
    "FILED_INSTRUMENTS": "validate_filed_instruments.py",
    "BI_CONSUMER_REGISTRY": "validate_bi_consumer_registry.py",
    "AREA_BI_PROFILE": "validate_area_bi_profile.py",
}


def _load_canonical_registry_by_path() -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    if not CANONICAL_REGISTRY.is_file():
        return out
    with CANONICAL_REGISTRY.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            fp = (row.get("file_path") or "").strip()
            if fp.endswith(".csv"):
                out[fp] = row
    return out


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9_]+", "_", text.lower()).strip("_")


def _area_from_path(rel: str) -> str:
    parts = rel.split("/")
    try:
        idx = parts.index("O5-1")
        segs = parts[idx + 1 : idx + 3]
        if len(segs) >= 2 and segs[1] not in {"canonicals", "dimensions"}:
            return _slug("_".join(segs[:2]))
        return _slug(segs[0])
    except ValueError:
        if "Envoy Tech Lab" in rel:
            return "envoy_tech_lab"
        return "unknown"


def _gov_id(rel: str) -> str:
    stem = Path(rel).stem.lower()
    area = _area_from_path(rel)
    return f"gov_{area}_{_slug(stem)}"


def _workflow_path(rel: str) -> str:
    return rel


def _mirror_table_from_canonical(row: dict[str, str]) -> str:
    mt = (row.get("mirror_table") or "").strip()
    if mt and not mt.startswith("compliance."):
        return f"compliance.{mt}"
    return mt


def _build_row(rel: str, canon_rows: dict[str, dict[str, str]]) -> dict[str, str]:
    stem = Path(rel).stem
    ovr = CHARTER.get(rel, {})
    canon = canon_rows.get(rel, {})
    area = ovr.get("owning_area") or _area_from_path(rel)
    role = ovr.get("owning_role") or (canon.get("owning_role") or "System Owner")
    asset_class = ovr.get("asset_class") or "compliance_mirror"
    plane1 = ovr.get("plane1_validator") or _STEM_VALIDATORS.get(stem, "validate_hlk.py")
    in_hlk = ovr.get("plane1_in_validate_hlk") or (
        "false" if plane1 in {"none", "release-gate.py", "validate_compliance_schema_drift.py"} else "true"
    )
    mirror = ovr.get("plane2_mirror_table") or _mirror_table_from_canonical(canon)
    if asset_class == "graph_projection":
        p2_policy = "graph_projection"
    elif asset_class in {"git_only"}:
        p2_policy = "git_only"
    elif asset_class == "forward_charter":
        p2_policy = ovr.get("plane2_sync_policy", "forward_charter")
    elif asset_class == "data_contract_mirror":
        p2_policy = ovr.get("plane2_sync_policy", "forward_charter")
    elif asset_class == "finops_mirror":
        p2_policy = ovr.get("plane2_sync_policy", "forward_charter")
    else:
        p2_policy = ovr.get("plane2_sync_policy") or ("active" if mirror else "git_only")
    emit = ovr.get("plane2_emit_profile")
    if emit is None:
        if p2_policy == "active" and mirror:
            emit = "main"
        elif p2_policy == "graph_projection" or asset_class == "git_only":
            emit = "none"
        else:
            emit = "none"
    prec = ovr.get("precedence_registered") or ("true" if canon else "false")
    reg_id = ovr.get("canonical_registry_id")
    if reg_id is None:
        reg_id = (canon.get("canonical_id") or "").strip()
    enum_parity = ovr.get("enum_parity_required") or (
        "true" if p2_policy == "active" and mirror else "false"
    )
    pk = ovr.get("delete_reconcile_pk", "")
    if not pk and (stem.endswith("_REGISTRY") or stem.endswith("_REGISTER")):
        pk = stem.lower().replace("_registry", "_id").replace("_register", "_id")
        if stem == "baseline_organisation":
            pk = "org_id"
        if stem == "process_list":
            pk = "item_id"
    return {
        "governance_id": _gov_id(rel),
        "csv_path": rel,
        "owning_area": area,
        "owning_role": role,
        "asset_class": asset_class,
        "plane1_validator": plane1,
        "plane1_in_validate_hlk": in_hlk,
        "plane2_mirror_table": mirror,
        "plane2_sync_policy": p2_policy,
        "plane2_emit_profile": emit,
        "plane2_workflow_paths": _workflow_path(rel),
        "precedence_registered": prec,
        "canonical_registry_id": reg_id,
        "mirror_ddl_migration": ovr.get("mirror_ddl_migration", ""),
        "enum_parity_required": enum_parity,
        "delete_reconcile_pk": pk,
        "last_review": "2026-06-09",
        "last_review_decision_id": "D-IH-95-B",
        "status": "active",
        "notes": ovr.get("notes", ""),
    }


def main() -> int:
    canon_rows = _load_canonical_registry_by_path()
    vault_csvs = sorted(
        p.relative_to(REPO).as_posix()
        for p in VAULT_ROOT.rglob("canonicals/**/*.csv")
        if p.name != "CANONICAL_GOVERNANCE_REGISTRY.csv"
    )
    if len(vault_csvs) != EXPECTED_VAULT_CSV_COUNT:
        print(f"FAIL: expected {EXPECTED_VAULT_CSV_COUNT} vault CSVs, found {len(vault_csvs)}")
        return 1
    rows = [_build_row(rel, canon_rows) for rel in vault_csvs]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(CANONICAL_GOVERNANCE_REGISTRY_FIELDNAMES))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {OUT.relative_to(REPO).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
