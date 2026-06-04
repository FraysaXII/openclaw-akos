-- I93 P6 — OPS-86-15 mirror gap closure (MIRROR-2 ratification)
-- Five dimension CSVs: DDL + RLS service_role-only (CHANNEL mirror pattern)

-- =============================================================================
-- compliance.aic_registry_mirror
-- =============================================================================
CREATE TABLE IF NOT EXISTS compliance.aic_registry_mirror (
  aic_id                         TEXT PRIMARY KEY,
  aic_name                       TEXT NOT NULL,
  substrate_id                   TEXT,
  runtime_instance               TEXT,
  role_owner_class               TEXT,
  parent_doctrine_canonical      TEXT,
  status                         TEXT NOT NULL,
  notes                          TEXT,
  last_review_at                 TEXT,
  last_review_by                 TEXT,
  last_review_decision_id        TEXT,
  methodology_version_at_review  TEXT,
  source_git_sha                 TEXT,
  synced_at                      TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE compliance.aic_registry_mirror ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS aic_registry_mirror_service_role ON compliance.aic_registry_mirror;
CREATE POLICY aic_registry_mirror_service_role
  ON compliance.aic_registry_mirror FOR ALL TO service_role USING (true) WITH CHECK (true);
GRANT SELECT, INSERT, UPDATE, DELETE ON compliance.aic_registry_mirror TO service_role;
REVOKE ALL ON compliance.aic_registry_mirror FROM PUBLIC, anon, authenticated;

-- =============================================================================
-- compliance.audience_registry_mirror
-- =============================================================================
CREATE TABLE IF NOT EXISTS compliance.audience_registry_mirror (
  audience_code                  TEXT PRIMARY KEY,
  name                           TEXT NOT NULL,
  register_side                  TEXT NOT NULL,
  intent_summary                 TEXT,
  typical_surfaces               TEXT,
  bridge_anchor                  TEXT,
  status                         TEXT NOT NULL,
  added_at                       TEXT,
  last_review_at                 TEXT,
  last_review_by                 TEXT,
  last_review_decision_id        TEXT,
  methodology_version_at_review  TEXT,
  linked_decision_id             TEXT,
  notes                          TEXT,
  source_git_sha                 TEXT,
  synced_at                      TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE compliance.audience_registry_mirror ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS audience_registry_mirror_service_role ON compliance.audience_registry_mirror;
CREATE POLICY audience_registry_mirror_service_role
  ON compliance.audience_registry_mirror FOR ALL TO service_role USING (true) WITH CHECK (true);
GRANT SELECT, INSERT, UPDATE, DELETE ON compliance.audience_registry_mirror TO service_role;
REVOKE ALL ON compliance.audience_registry_mirror FROM PUBLIC, anon, authenticated;

-- =============================================================================
-- compliance.capability_registry_mirror
-- =============================================================================
CREATE TABLE IF NOT EXISTS compliance.capability_registry_mirror (
  capability_id                  TEXT PRIMARY KEY,
  capability_name                TEXT NOT NULL,
  bearer_class                   TEXT NOT NULL,
  area                           TEXT NOT NULL,
  role_owner                     TEXT NOT NULL,
  originating_process_ids        TEXT,
  substrate_id                   TEXT,
  skill_ids                      TEXT,
  lifecycle_status               TEXT NOT NULL,
  i81_verdict                    TEXT,
  i81_gap_summary                TEXT,
  external_register_summary      TEXT,
  last_review_at                 TEXT,
  last_review_by                 TEXT,
  last_review_decision_id        TEXT,
  methodology_version_at_review  TEXT,
  notes                          TEXT,
  source_git_sha                 TEXT,
  synced_at                      TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE compliance.capability_registry_mirror ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS capability_registry_mirror_service_role ON compliance.capability_registry_mirror;
CREATE POLICY capability_registry_mirror_service_role
  ON compliance.capability_registry_mirror FOR ALL TO service_role USING (true) WITH CHECK (true);
GRANT SELECT, INSERT, UPDATE, DELETE ON compliance.capability_registry_mirror TO service_role;
REVOKE ALL ON compliance.capability_registry_mirror FROM PUBLIC, anon, authenticated;

CREATE INDEX IF NOT EXISTS idx_capability_registry_mirror_area
  ON compliance.capability_registry_mirror (area);

-- =============================================================================
-- compliance.capability_confidence_registry_mirror
-- =============================================================================
CREATE TABLE IF NOT EXISTS compliance.capability_confidence_registry_mirror (
  confidence_id                  TEXT PRIMARY KEY,
  capability_id                  TEXT NOT NULL,
  substrate_score                TEXT NOT NULL,
  repeatability_score            TEXT NOT NULL,
  quality_score                  TEXT NOT NULL,
  translatability_score          TEXT NOT NULL,
  auditability_score             TEXT NOT NULL,
  aggregate_confidence           TEXT NOT NULL,
  rating_method                  TEXT NOT NULL,
  rated_at                       TEXT,
  rated_by                       TEXT,
  notes                          TEXT,
  last_review_at                 TEXT,
  last_review_by                 TEXT,
  last_review_decision_id        TEXT,
  methodology_version_at_review  TEXT,
  source_git_sha                 TEXT,
  synced_at                      TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE compliance.capability_confidence_registry_mirror ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS capability_confidence_registry_mirror_service_role
  ON compliance.capability_confidence_registry_mirror;
CREATE POLICY capability_confidence_registry_mirror_service_role
  ON compliance.capability_confidence_registry_mirror
  FOR ALL TO service_role USING (true) WITH CHECK (true);
GRANT SELECT, INSERT, UPDATE, DELETE ON compliance.capability_confidence_registry_mirror TO service_role;
REVOKE ALL ON compliance.capability_confidence_registry_mirror FROM PUBLIC, anon, authenticated;

CREATE INDEX IF NOT EXISTS idx_capability_confidence_registry_mirror_capability_id
  ON compliance.capability_confidence_registry_mirror (capability_id);

-- =============================================================================
-- compliance.country_work_calendar_mirror (OPS-86-18; no Pydantic SSOT yet)
-- =============================================================================
CREATE TABLE IF NOT EXISTS compliance.country_work_calendar_mirror (
  country_code                   TEXT PRIMARY KEY,
  country_name                   TEXT NOT NULL,
  legal_hours_per_day            TEXT NOT NULL,
  public_holidays_per_year_avg   TEXT,
  locale_uplift_pct              TEXT,
  notes                          TEXT,
  source_git_sha                 TEXT,
  synced_at                      TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE compliance.country_work_calendar_mirror ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS country_work_calendar_mirror_service_role ON compliance.country_work_calendar_mirror;
CREATE POLICY country_work_calendar_mirror_service_role
  ON compliance.country_work_calendar_mirror FOR ALL TO service_role USING (true) WITH CHECK (true);
GRANT SELECT, INSERT, UPDATE, DELETE ON compliance.country_work_calendar_mirror TO service_role;
REVOKE ALL ON compliance.country_work_calendar_mirror FROM PUBLIC, anon, authenticated;
