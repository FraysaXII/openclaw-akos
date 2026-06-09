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


VALID_COMPONENT_KINDS: frozenset[str] = frozenset({
    "repository", "saas", "data_platform", "integration", "edge_function", "library",
    "infrastructure", "observability", "client_runtime", "other",
})
VALID_LIFECYCLE_STATUSES: frozenset[str] = frozenset({
    "experimental", "active", "constrained", "sunset", "retired",
})
VALID_STEWARD_OPS_DOMAINS: frozenset[str] = frozenset({
    "MAROPS", "DEVOPS", "DATAOPS", "PMSMO", "LEGOPS", "FINOPS", "GTMOPS", "SECOPS", "other",
})
VALID_API_EXPOSURES: frozenset[str] = frozenset({"none", "internal", "partner", "public"})
VALID_INTEGRATION_PATTERNS: frozenset[str] = frozenset({
    "push", "pull", "batch", "stream", "event", "manual", "n_a", "edge_webhook",
    "pgmq_worker", "fdw_read", "low_code_rpa", "embedded_chart",
})
VALID_ENVIRONMENT_SCOPES: frozenset[str] = frozenset({"dev", "staging", "prod", "multi", "local_only"})
VALID_SLO_TIERS: frozenset[str] = frozenset({"best_effort", "standard", "critical"})

CSV_PATH_RELATIVE: str = (
    "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/techops/COMPONENT_SERVICE_MATRIX.csv"
)
