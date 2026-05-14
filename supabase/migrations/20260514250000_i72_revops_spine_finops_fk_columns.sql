-- Initiative 72 P7 — RevOps Spine: finops.registered_fact engagement + template FK columns
-- D-IH-72-A (P0 charter); D-IH-72-L (Strand D charter); D-IH-72-M (option D both:
-- engagement_id + template_id FK columns AND governance.engagement_revenue_view).
--
-- DAMA-DMBOK 2.0 RMDM principle: one consistent revenue story from engagement
-- creation through revenue recognition. Per Routine.co RevOps Blueprint 2026:
-- "one consistent revenue story from deal creation through recognition".
--
-- Cross-references:
--   compliance.engagement_registry_mirror (existing; mirrored from ENGAGEMENT_REGISTRY.csv)
--   compliance.engagement_template_registry_mirror (I72 P2; mirrored from ENGAGEMENT_TEMPLATE_REGISTRY.csv)
--   finops.registered_fact (existing; I19 P1)
--   akos/hlk_revops_spine.py (Pydantic-style SSOT for spine query shapes)
--   scripts/validate_revops_spine.py (validator for spine integrity)

-- 1) Add FK columns to finops.registered_fact (nullable for backwards compat)
ALTER TABLE finops.registered_fact
  ADD COLUMN IF NOT EXISTS engagement_id TEXT,
  ADD COLUMN IF NOT EXISTS template_id   TEXT;

COMMENT ON COLUMN finops.registered_fact.engagement_id IS
  'D-IH-72-M: FK-by-convention to compliance.engagement_registry_mirror.engagement_id. Nullable: pre-spine facts (I19+I20 era) carry NULL; post-spine facts populate when registered. RevOps Spine queries join via this column.';
COMMENT ON COLUMN finops.registered_fact.template_id IS
  'D-IH-72-M: FK-by-convention to compliance.engagement_template_registry_mirror.template_id. Nullable: pre-promotion engagements may carry NULL; post-promotion engagements populate via SOP-ENGAGEMENT_TEMPLATE_PROMOTION_001. RevOps Spine queries derive per-template revenue rollups.';

CREATE INDEX IF NOT EXISTS registered_fact_engagement_id_idx
  ON finops.registered_fact (engagement_id)
  WHERE engagement_id IS NOT NULL;
CREATE INDEX IF NOT EXISTS registered_fact_template_id_idx
  ON finops.registered_fact (template_id)
  WHERE template_id IS NOT NULL;

-- 2) governance.engagement_revenue_view: cross-area join surface for the RevOps spine
-- Per D-IH-72-M option D: governance.engagement_revenue_view joins:
--   compliance.engagement_registry_mirror (engagement metadata + status + dates)
--   compliance.engagement_template_registry_mirror (template per-engagement)
--   finops.registered_fact (revenue + budget + reconciliation facts)
-- View is read-only; consumers query via the operator-facing HLK-ERP panel
-- /operator/operations/revops/engagement-revenue/ (panel slot
-- op_revops_engagement_revenue per HLK_ERP_ARCHITECTURE.md §4 reserved at I72 P0).

CREATE OR REPLACE VIEW governance.engagement_revenue_view AS
SELECT
  e.engagement_id,
  e.engagement_name,
  e.engagement_class,
  e.counterparty_org_id,
  e.owner_role                         AS engagement_owner_role,
  e.status                             AS engagement_status,
  e.started_at                         AS engagement_started_at,
  e.ended_at                           AS engagement_ended_at,
  e.language_primary,
  t.template_id,
  t.name                               AS template_name,
  t.engagement_class                   AS template_engagement_class,
  t.value_band_eur                     AS template_value_band_eur,
  t.duration_target_days               AS template_duration_target_days,
  t.billing_cadence                    AS template_billing_cadence,
  t.contract_kind                      AS template_contract_kind,
  t.lifecycle_status                   AS template_lifecycle_status,
  COALESCE(SUM(f.amount_minor), 0)     AS revenue_amount_minor_total,
  COUNT(f.id)                          AS revenue_fact_count,
  MIN(f.effective_date)                AS revenue_first_effective_date,
  MAX(f.effective_date)                AS revenue_last_effective_date,
  COALESCE(MIN(f.currency), 'EUR')     AS revenue_currency_min,
  COALESCE(MAX(f.currency), 'EUR')     AS revenue_currency_max
FROM compliance.engagement_registry_mirror e
LEFT JOIN compliance.engagement_template_registry_mirror t
  ON t.template_id = (
    SELECT MAX(rf.template_id)
    FROM finops.registered_fact rf
    WHERE rf.engagement_id = e.engagement_id
  )
LEFT JOIN finops.registered_fact f
  ON f.engagement_id = e.engagement_id
GROUP BY
  e.engagement_id,
  e.engagement_name,
  e.engagement_class,
  e.counterparty_org_id,
  e.owner_role,
  e.status,
  e.started_at,
  e.ended_at,
  e.language_primary,
  t.template_id,
  t.name,
  t.engagement_class,
  t.value_band_eur,
  t.duration_target_days,
  t.billing_cadence,
  t.contract_kind,
  t.lifecycle_status;

COMMENT ON VIEW governance.engagement_revenue_view IS
  'D-IH-72-M: RevOps Spine cross-area join. One row per engagement_id with template metadata and aggregated revenue facts. Consumers: HLK-ERP /operator/operations/revops/engagement-revenue/ panel (op_revops_engagement_revenue slot per HLK_ERP_ARCHITECTURE.md §4); RevOps QBR cycle (SOP-REVOPS_QBR_001.md); RevOps Analyst per-quarter portfolio reconciliation. Read-only; deny-by-default RLS inherited from source tables.';

-- View RLS inherits from underlying tables; no separate policy needed.
GRANT SELECT ON governance.engagement_revenue_view TO service_role;
