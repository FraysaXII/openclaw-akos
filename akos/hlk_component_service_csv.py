"""Canonical `COMPONENT_SERVICE_MATRIX.csv` column order (HLK compliance SSOT).

CTO chain maintains this inventory; validators enforce FKs to organisation and process_list.
"""

from __future__ import annotations

COMPONENT_SERVICE_FIELDNAMES: list[str] = [
    "component_id",
    "component_name",
    "component_kind",
    "lifecycle_status",
    "entity",
    "area",
    "primary_owner_role",
    "steward_ops_domain",
    "secondary_owner_role",
    "escalation_owner_role",
    "repo_slug",
    "github_url",
    "api_exposure",
    "api_spec_pointer",
    "integration_pattern",
    "depends_on_component_ids",
    "parent_component_id",
    "primary_process_item_id",
    "related_process_item_ids",
    "topic_ids",
    "access_level_data",
    "data_classification",
    "environment_scope",
    "slo_tier",
    "runbook_link",
    "doc_link",
    "legal_hold",
    "retention_policy_ref",
    "last_verified_date",
    "source_row",
    "notes",
]
