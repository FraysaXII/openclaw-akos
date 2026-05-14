"""Field contract for ENGAGEMENT_TEMPLATE_REGISTRY.csv (Initiative 72 P2).

Canonical CSV lives under
``docs/references/hlk/v3.0/Admin/O5-1/Operations/RevOps/canonicals/dimensions/``
per `D-IH-72-Y` Round 7 path migration (RevOps area canonicals live under
``Operations/RevOps/canonicals/`` rather than the legacy
``People/Compliance/canonicals/dimensions/`` location used by sibling registries
like SKILL_REGISTRY + PERSONA_REGISTRY).

Mirrored to ``compliance.engagement_template_registry_mirror`` on Supabase per
the pattern established by Initiative 32 P2 (skill_registry_mirror).

ENGAGEMENT_TEMPLATE_REGISTRY = a versioned bundle of repeatable engagement
patterns (counterparty class + value band + duration target + discipline mix +
billing cadence + contract kind + lifecycle status). Sibling to
ENGAGEMENT_REGISTRY.csv (which holds ACTIVE engagement instances); a TEMPLATE
codifies the shape an engagement instance assumes when promoted via
SOP-ENGAGEMENT_TEMPLATE_PROMOTION_001.md (P3 deliverable).

Per `D-IH-72-F` the template registry is a SIBLING canonical (not a
column-extension on ENGAGEMENT_REGISTRY.csv) — engagement instances and
engagement templates have distinct lifecycles, distinct ownership, and distinct
mirror tables.

Decision lineage:
- `D-IH-72-A` (P0 charter)
- `D-IH-72-F` (sibling registry, not extension)
- `D-IH-72-Y` (Round 7 path migration to Operations/RevOps/canonicals/)
- `D-IH-72-AH` (Round 8 Operations/RevOps area charter at P1)
"""

from __future__ import annotations

# Keep in sync with the canonical CSV header row at
# docs/references/hlk/v3.0/Admin/O5-1/Operations/RevOps/canonicals/dimensions/ENGAGEMENT_TEMPLATE_REGISTRY.csv
ENGAGEMENT_TEMPLATE_REGISTRY_FIELDNAMES: tuple[str, ...] = (
    "template_id",                     # ^tmpl_[a-z0-9_]{4,80}_v\d+$ — stable, semver-suffixed
    "name",                            # human-readable
    "engagement_class",                # FK to ENGAGEMENT_CLASSES (see VALID_ENGAGEMENT_CLASSES)
    "owner_role",                      # FK to baseline_organisation.csv role_name
    "discipline_mix",                  # semicolon-list; subset of VALID_MARKETING_DISCIPLINES
    "duration_target_days",            # integer; typical engagement duration
    "value_band_eur",                  # FK to VALID_VALUE_BANDS
    "billing_cadence",                 # FK to VALID_BILLING_CADENCES
    "contract_kind",                   # FK to VALID_CONTRACT_KINDS
    "counterparty_class",              # FK to VALID_COUNTERPARTY_CLASSES
    "artifact_path_pattern",           # glob; engagement folder structure pattern
    "supabase_mirror",                 # mirror table name (default: compliance.engagement_template_registry_mirror)
    "panel_slot",                      # HLK-ERP panel slot id (per HLK_ERP_ARCHITECTURE.md §4)
    "lifecycle_status",                # FK to VALID_LIFECYCLE_STATUSES
    "promotion_decision_id",           # FK to DECISION_REGISTER.csv decision_id; the decision that promoted this template
    "ssot_path",                       # repo-relative path to the canonical authoring doc (the SOP or charter that owns this template)
    "version",                         # semver-like
    "notes",
    "last_review_at",                  # I71 P4 audit-trail (DATE; ISO YYYY-MM-DD)
    "last_review_by",                  # FK-by-convention to baseline_organisation.csv role_name
    "last_review_decision_id",         # FK-by-convention to DECISION_REGISTER.csv decision_id; nullable
    "methodology_version_at_review",   # vMAJOR.MINOR per LOGIC_CHANGE_LOG.md
)

# Cross-canonical enums

VALID_ENGAGEMENT_CLASSES: frozenset[str] = frozenset({
    # Mirrors ENGAGEMENT_REGISTRY.csv engagement_class column values.
    "customer-outbound",
    "partner-outbound",
    "sister-business-outbound-internal",
    "collaborator-inbound",
    "internal",
})

VALID_MARKETING_DISCIPLINES: frozenset[str] = frozenset({
    # Mirrors MARKETING_AREA_M3_REDESIGN.md §2 sub-area names.
    "Brand", "Reach", "Resonance", "Storytelling", "Experimentation",
    # Operations sibling areas commonly involved in templates.
    "RevOps", "PMO", "SMO", "IntelligenceOps",
    # Cross-area collaborators.
    "Account Management", "Finance", "Legal", "Compliance", "Tech",
})

VALID_VALUE_BANDS: frozenset[str] = frozenset({
    "under_10k", "10k_50k", "50k_250k", "250k_1m", "over_1m",
})

VALID_BILLING_CADENCES: frozenset[str] = frozenset({
    "one_time",
    "milestone",
    "monthly_subscription",
    "quarterly_subscription",
    "annual_subscription",
})

VALID_CONTRACT_KINDS: frozenset[str] = frozenset({
    "msa_sow",          # Master Services Agreement + Statement of Work
    "single_sow",       # Standalone SoW (no MSA)
    "partner_agreement", # Partner / cobranding agreement
    "dpa_only",         # DPA-only (data-processing) for collaborator-inbound
    "internal",         # Internal SSOT engagement (no external contract)
})

VALID_COUNTERPARTY_CLASSES: frozenset[str] = frozenset({
    "enterprise",
    "sme",
    "sister_business",
    "collaborator",
    "internal",
    "regulator",
})

VALID_LIFECYCLE_STATUSES: frozenset[str] = frozenset({
    "active",       # Promoted; available for engagement-instance assignment
    "deprecated",   # Retired; preserved for historical reference
    "scaffold",     # Authored but not yet promoted (per SOP-ENGAGEMENT_TEMPLATE_PROMOTION_001.md)
})
