"""Shared SSOT for the 9 adapter registries (Initiative 72 P9 + I93 P5b RPA).

Per `D-IH-72-O` (Normalized Adapter Pattern: AKOS-internal SSOT + per-vendor
adapter shim with active/inactive/planned/experimental/deprecated metadata
per Truto/Unified.to/Apideck consensus 2026) + `D-IH-72-T` (MarTech adapter
breadth: 6 sibling registries on top of CRM_ADAPTER_REGISTRY + REVOPS_-
ADAPTER_REGISTRY for 8 total registries).

The 8 adapter registries share an identical schema; this module is the
single SSOT they all reference. Each adapter registry file lives at the
canonical path appropriate to its area:

| Registry                                | Path                                                                                |
| :-------------------------------------- | :---------------------------------------------------------------------------------- |
| CRM_ADAPTER_REGISTRY.csv                | Marketing/Reach/canonicals/dimensions/                                              |
| REVOPS_ADAPTER_REGISTRY.csv             | Operations/RevOps/canonicals/dimensions/                                            |
| EMAIL_ADAPTER_REGISTRY.csv              | Marketing/Reach/canonicals/dimensions/                                              |
| ATTRIBUTION_ADAPTER_REGISTRY.csv        | Marketing/Experimentation/canonicals/dimensions/                                    |
| BILLING_ADAPTER_REGISTRY.csv            | Operations/RevOps/canonicals/dimensions/                                            |
| COMMUNICATION_ADAPTER_REGISTRY.csv      | Marketing/Reach/canonicals/dimensions/                                              |
| SCHEDULING_ADAPTER_REGISTRY.csv         | Marketing/Reach/canonicals/dimensions/                                              |
| CONTRACT_ADAPTER_REGISTRY.csv           | Operations/SMO/canonicals/dimensions/                                               |
| RPA_ADAPTER_REGISTRY.csv                | Data/Governance/canonicals/dimensions/ (I93 P5b)                                    |

Decision lineage:
- `D-IH-72-A` (P0 charter)
- `D-IH-72-O` (Normalized Adapter Pattern + status metadata)
- `D-IH-72-T` (MarTech adapter breadth — 6 sibling registries on top of CRM+REVOPS)
- `D-IH-72-U` (validate_process_list_pairing.py owned by I72 P9)
- `D-IH-72-W` (Feature-flag pattern with TODO markers for forward-references)
- `D-IH-93-I` (RPA adapter registry — Power Platform / Make / n8n / Edge / pg_net)
"""
from __future__ import annotations

# Keep in sync with each adapter registry CSV header row.
ADAPTER_REGISTRY_FIELDNAMES: tuple[str, ...] = (
    "adapter_id",                      # ^[a-z0-9_]{3,80}$ — stable identifier (vendor or internal slug)
    "registry_class",                  # one of REGISTRY_CLASSES (e.g. CRM, EMAIL); discriminates which file owns the row
    "vendor",                          # vendor display name (e.g. HubSpot)
    "adapter_kind",                    # enum first_party_internal | normalized_shim | direct_native
    "status",                          # enum active | inactive | planned | experimental | deprecated (per D-IH-72-O)
    "owner_role",                      # FK-by-convention to baseline_organisation.csv role_name
    "linked_sop_path",                 # path or TODO[I72-...] marker
    "linked_runbook_path",             # path or TODO[I72-...] marker (e.g. scripts/revops_dispatch.py)
    "linked_decision_id",              # FK-by-convention to DECISION_REGISTER.csv
    "feature_flag",                    # active | gated_operator | gated_release_gate | always_on (per D-IH-72-W)
    "notes",
    "last_review_at",
    "last_review_by",
    "last_review_decision_id",
    "methodology_version_at_review",
)


REGISTRY_CLASSES: frozenset[str] = frozenset({
    "CRM",
    "REVOPS",
    "EMAIL",
    "ATTRIBUTION",
    "BILLING",
    "COMMUNICATION",
    "SCHEDULING",
    "CONTRACT",
    "RPA",
})


VALID_ADAPTER_KINDS: frozenset[str] = frozenset({
    "first_party_internal",   # AKOS-internal SSOT (e.g. holistika_ops adapter)
    "normalized_shim",        # Normalized Adapter Pattern shim (e.g. HubSpot adapter via Unified.to-style abstraction)
    "direct_native",          # Direct vendor SDK call (no normalization layer)
})


VALID_STATUSES: frozenset[str] = frozenset({
    "active",        # adapter is live; events flow through it
    "inactive",      # adapter is mounted but disabled (operator can flip via feature_flag)
    "planned",       # adapter is on the roadmap but not yet implemented
    "experimental",  # adapter is implemented but behind release-gate / feature-flag
    "deprecated",    # adapter retired; historical record only
})


VALID_FEATURE_FLAGS: frozenset[str] = frozenset({
    "active",                 # always-on; no gate
    "gated_operator",         # operator must approve invocation per request
    "gated_release_gate",     # release-gate must pass before adapter activates in given env
    "always_on",              # explicitly always-on (used for first_party_internal adapters that never gate)
})


# Per-registry canonical paths (relative to repo root).
# Mirror table names for the 8 adapter classes with existing DDL (excludes RPA — P95-GOV-7).
ADAPTER_REGISTRY_CLASS_TO_MIRROR_TABLE: dict[str, str] = {
    "CRM": "compliance.crm_adapter_registry_mirror",
    "REVOPS": "compliance.revops_adapter_registry_mirror",
    "EMAIL": "compliance.email_adapter_registry_mirror",
    "ATTRIBUTION": "compliance.attribution_adapter_registry_mirror",
    "BILLING": "compliance.billing_adapter_registry_mirror",
    "COMMUNICATION": "compliance.communication_adapter_registry_mirror",
    "SCHEDULING": "compliance.scheduling_adapter_registry_mirror",
    "CONTRACT": "compliance.contract_adapter_registry_mirror",
}

ADAPTER_EMIT_REGISTRY_CLASSES: tuple[str, ...] = tuple(ADAPTER_REGISTRY_CLASS_TO_MIRROR_TABLE)

REGISTRY_PATHS: dict[str, str] = {
    "CRM": "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Reach/canonicals/dimensions/CRM_ADAPTER_REGISTRY.csv",
    "REVOPS": "docs/references/hlk/v3.0/Admin/O5-1/Operations/RevOps/canonicals/dimensions/REVOPS_ADAPTER_REGISTRY.csv",
    "EMAIL": "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Reach/canonicals/dimensions/EMAIL_ADAPTER_REGISTRY.csv",
    "ATTRIBUTION": "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Experimentation/canonicals/dimensions/ATTRIBUTION_ADAPTER_REGISTRY.csv",
    "BILLING": "docs/references/hlk/v3.0/Admin/O5-1/Operations/RevOps/canonicals/dimensions/BILLING_ADAPTER_REGISTRY.csv",
    "COMMUNICATION": "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Reach/canonicals/dimensions/COMMUNICATION_ADAPTER_REGISTRY.csv",
    "SCHEDULING": "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Reach/canonicals/dimensions/SCHEDULING_ADAPTER_REGISTRY.csv",
    "CONTRACT": "docs/references/hlk/v3.0/Admin/O5-1/Operations/SMO/canonicals/dimensions/CONTRACT_ADAPTER_REGISTRY.csv",
    "RPA": "docs/references/hlk/v3.0/Admin/O5-1/Data/Governance/canonicals/dimensions/RPA_ADAPTER_REGISTRY.csv",
}
