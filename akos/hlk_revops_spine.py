"""RevOps Spine query-shape SSOT (Initiative 72 P7).

Per `D-IH-72-A` (P0 charter), `D-IH-72-L` (Strand D charter), `D-IH-72-M`
(option D both: engagement_id + template_id FK columns AND
governance.engagement_revenue_view), and `D-IH-72-AC` (RevOps role activation
gating).

The RevOps Spine is the cross-area join surface that wires Marketing
demand-side activity (engagements) to Finance revenue facts via a uniform
query shape. This module is the Pydantic-style SSOT for that query shape;
the validator at `scripts/validate_revops_spine.py` enforces:

1. Migration ``20260514250000_i72_revops_spine_finops_fk_columns.sql`` exists
   and adds the two FK columns + view definition.
2. The view definition matches ``EXPECTED_VIEW_COLUMNS`` (column-set check;
   used at release-gate to detect drift between SSOT and migration body).
3. Engagement-template join semantics match ``DOCUMENTED_JOIN_SEMANTICS``
   (LEFT JOIN compliance.engagement_template_registry_mirror via the latest
   non-null template_id observed in finops.registered_fact for that
   engagement; chosen because templates may evolve over an engagement
   lifetime and the most-recent template is the one active for revenue
   recognition).

The HLK-ERP panel ``/operator/operations/revops/engagement-revenue/`` (panel
slot ``op_revops_engagement_revenue`` reserved at I72 P0 in
``HLK_ERP_ARCHITECTURE.md`` §4) consumes ``governance.engagement_revenue_view``
read-only; UI implementation lives in the sibling repo (per
``akos-mirror-template.mdc``).
"""

from __future__ import annotations

# Migration filename + view name pinned for release-gate drift detection.
SPINE_MIGRATION_FILENAME: str = "20260514250000_i72_revops_spine_finops_fk_columns.sql"
SPINE_VIEW_NAME: str = "governance.engagement_revenue_view"
# NOTE: HLK_ERP_ARCHITECTURE.md tables use the route as the slot identifier
# (e.g., the route is the primary key in the panel-slot table). The
# ``op_revops_engagement_revenue`` short-id is used in master-roadmap +
# CANONICAL_REGISTRY references. The validator accepts EITHER.
SPINE_PANEL_SLOT: str = "op_revops_engagement_revenue"
SPINE_PANEL_ROUTE: str = "/operator/operations/revops/engagement-revenue/"

# FK columns added to finops.registered_fact at I72 P7.
SPINE_FK_COLUMNS: tuple[str, ...] = (
    "engagement_id",
    "template_id",
)

# Column-set the view exposes — pinned for release-gate drift detection.
# The validator parses the migration body and compares the parsed SELECT
# column list to this tuple (order not enforced beyond exact membership).
EXPECTED_VIEW_COLUMNS: tuple[str, ...] = (
    # Engagement metadata (from compliance.engagement_registry_mirror).
    "engagement_id",
    "engagement_name",
    "engagement_class",
    "counterparty_org_id",
    "engagement_owner_role",
    "engagement_status",
    "engagement_started_at",
    "engagement_ended_at",
    "language_primary",
    # Template metadata (from compliance.engagement_template_registry_mirror).
    "template_id",
    "template_name",
    "template_engagement_class",
    "template_value_band_eur",
    "template_duration_target_days",
    "template_billing_cadence",
    "template_contract_kind",
    "template_lifecycle_status",
    # Aggregated revenue facts (from finops.registered_fact).
    "revenue_amount_minor_total",
    "revenue_fact_count",
    "revenue_first_effective_date",
    "revenue_last_effective_date",
    "revenue_currency_min",
    "revenue_currency_max",
)


DOCUMENTED_JOIN_SEMANTICS: str = (
    "LEFT JOIN compliance.engagement_template_registry_mirror via the latest "
    "non-null template_id observed in finops.registered_fact for that engagement; "
    "templates may evolve over an engagement lifetime and the most-recent template "
    "is the one active for revenue recognition. LEFT JOIN finops.registered_fact "
    "via engagement_id; aggregates SUM/COUNT/MIN/MAX per engagement."
)
