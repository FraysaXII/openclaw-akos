-- Parity: scripts/sql/i31_phase1_staging/20260430_i31_goipoi_distance_extension_and_persona_registry_up.sql
-- Initiative 31 P2.2 + P2.1 — distance dimension on GOI/POI register + new persona_registry mirror.

-- =============================================================================
-- Part 1 — GOI/POI distance extension (D-IH-31-G)
-- =============================================================================

ALTER TABLE compliance.goipoi_register_mirror
  ADD COLUMN IF NOT EXISTS distance_band            TEXT,
  ADD COLUMN IF NOT EXISTS bridge_via               TEXT,
  ADD COLUMN IF NOT EXISTS distance_assessed_date   DATE;

-- Backfill the 6 existing rows to N1 (operator confirmed during Initiative 31 P2.2 review;
-- all current entries are direct operational contacts of the founder).
UPDATE compliance.goipoi_register_mirror
SET distance_band            = COALESCE(distance_band, 'N1'),
    distance_assessed_date   = COALESCE(distance_assessed_date, DATE '2026-04-30');

-- Distance band enum guard.
ALTER TABLE compliance.goipoi_register_mirror
  ADD CONSTRAINT goipoi_distance_band_enum
    CHECK (distance_band IN ('N1', 'N2', 'N3', 'N4'))
    NOT VALID;

ALTER TABLE compliance.goipoi_register_mirror
  VALIDATE CONSTRAINT goipoi_distance_band_enum;

-- bridge_via must be empty for N1 and present for N2-N4.
ALTER TABLE compliance.goipoi_register_mirror
  ADD CONSTRAINT goipoi_bridge_required_when_not_n1
    CHECK (
      (distance_band = 'N1' AND (bridge_via IS NULL OR bridge_via = '')) OR
      (distance_band IN ('N2', 'N3', 'N4') AND bridge_via IS NOT NULL AND bridge_via <> '')
    )
    NOT VALID;

ALTER TABLE compliance.goipoi_register_mirror
  VALIDATE CONSTRAINT goipoi_bridge_required_when_not_n1;

-- bridge_via cannot point at the row's own ref_id.
ALTER TABLE compliance.goipoi_register_mirror
  ADD CONSTRAINT goipoi_bridge_not_self
    CHECK (bridge_via IS NULL OR bridge_via = '' OR bridge_via <> ref_id)
    NOT VALID;

ALTER TABLE compliance.goipoi_register_mirror
  VALIDATE CONSTRAINT goipoi_bridge_not_self;

-- =============================================================================
-- Part 2 — persona_registry_mirror (D-IH-31 P2.1)
-- =============================================================================

CREATE TABLE IF NOT EXISTS compliance.persona_registry_mirror (
  persona_id              TEXT PRIMARY KEY,
  name                    TEXT NOT NULL,
  direction               TEXT NOT NULL CHECK (direction IN ('inbound', 'outbound', 'bidirectional')),
  intent_summary          TEXT NOT NULL,
  value_band              TEXT NOT NULL CHECK (value_band IN ('high', 'medium', 'low', 'depends_on_qualification')),
  typical_languages       TEXT NOT NULL,
  typical_channels        TEXT,
  typical_distance_band   TEXT NOT NULL CHECK (typical_distance_band ~ '^N[1-4](-N[1-4])?$'),
  qualification_gate      TEXT,
  intro_artifact_path     TEXT,
  handoff_role            TEXT,
  linked_topic_ids        TEXT,
  notes                   TEXT,
  source_git_sha          TEXT,
  synced_at               TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE compliance.persona_registry_mirror ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS persona_registry_mirror_anon_deny      ON compliance.persona_registry_mirror;
DROP POLICY IF EXISTS persona_registry_mirror_auth_deny      ON compliance.persona_registry_mirror;
DROP POLICY IF EXISTS persona_registry_mirror_service_role   ON compliance.persona_registry_mirror;

CREATE POLICY persona_registry_mirror_anon_deny
  ON compliance.persona_registry_mirror
  FOR ALL TO anon
  USING (false) WITH CHECK (false);

CREATE POLICY persona_registry_mirror_auth_deny
  ON compliance.persona_registry_mirror
  FOR ALL TO authenticated
  USING (false) WITH CHECK (false);

CREATE POLICY persona_registry_mirror_service_role
  ON compliance.persona_registry_mirror
  FOR ALL TO service_role
  USING (true) WITH CHECK (true);

GRANT SELECT, INSERT, UPDATE, DELETE ON compliance.persona_registry_mirror TO service_role;
REVOKE ALL ON compliance.persona_registry_mirror FROM PUBLIC;
REVOKE ALL ON compliance.persona_registry_mirror FROM anon, authenticated;

CREATE INDEX IF NOT EXISTS idx_persona_registry_mirror_direction
  ON compliance.persona_registry_mirror (direction);

CREATE INDEX IF NOT EXISTS idx_persona_registry_mirror_value_band
  ON compliance.persona_registry_mirror (value_band);

CREATE INDEX IF NOT EXISTS idx_persona_registry_mirror_typical_distance_band
  ON compliance.persona_registry_mirror (typical_distance_band);

-- =============================================================================
-- Part 3 — channel_touchpoint_registry_mirror (Initiative 31 P3)
-- =============================================================================

CREATE TABLE IF NOT EXISTS compliance.channel_touchpoint_registry_mirror (
  channel_id                       TEXT PRIMARY KEY,
  name                             TEXT NOT NULL,
  direction                        TEXT NOT NULL CHECK (direction IN ('inbound', 'outbound', 'bidirectional')),
  supported_languages              TEXT NOT NULL,
  typical_personas                 TEXT,
  typical_distance_band_inbound    TEXT NOT NULL CHECK (typical_distance_band_inbound ~ '^N[1-4](-N[1-4])?$'),
  triage_rule                      TEXT,
  response_sla_band                TEXT,
  response_owner_role              TEXT,
  linked_topic_ids                 TEXT,
  notes                            TEXT,
  source_git_sha                   TEXT,
  synced_at                        TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE compliance.channel_touchpoint_registry_mirror ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS channel_touchpoint_registry_mirror_anon_deny    ON compliance.channel_touchpoint_registry_mirror;
DROP POLICY IF EXISTS channel_touchpoint_registry_mirror_auth_deny    ON compliance.channel_touchpoint_registry_mirror;
DROP POLICY IF EXISTS channel_touchpoint_registry_mirror_service_role ON compliance.channel_touchpoint_registry_mirror;

CREATE POLICY channel_touchpoint_registry_mirror_anon_deny
  ON compliance.channel_touchpoint_registry_mirror
  FOR ALL TO anon
  USING (false) WITH CHECK (false);

CREATE POLICY channel_touchpoint_registry_mirror_auth_deny
  ON compliance.channel_touchpoint_registry_mirror
  FOR ALL TO authenticated
  USING (false) WITH CHECK (false);

CREATE POLICY channel_touchpoint_registry_mirror_service_role
  ON compliance.channel_touchpoint_registry_mirror
  FOR ALL TO service_role
  USING (true) WITH CHECK (true);

GRANT SELECT, INSERT, UPDATE, DELETE ON compliance.channel_touchpoint_registry_mirror TO service_role;
REVOKE ALL ON compliance.channel_touchpoint_registry_mirror FROM PUBLIC;
REVOKE ALL ON compliance.channel_touchpoint_registry_mirror FROM anon, authenticated;

CREATE INDEX IF NOT EXISTS idx_channel_touchpoint_registry_mirror_direction
  ON compliance.channel_touchpoint_registry_mirror (direction);

CREATE INDEX IF NOT EXISTS idx_channel_touchpoint_registry_mirror_typical_distance_band_inbound
  ON compliance.channel_touchpoint_registry_mirror (typical_distance_band_inbound);

-- =============================================================================
-- Part 4 — sourcing_register_mirror (Initiative 31 P5.2)
-- =============================================================================

CREATE TABLE IF NOT EXISTS compliance.sourcing_register_mirror (
  vendor_id                          TEXT PRIMARY KEY,
  discipline                         TEXT NOT NULL,
  engagement_type                    TEXT NOT NULL CHECK (engagement_type IN ('one_off', 'recurring', 'retainer', 'pilot')),
  languages_supported                TEXT,
  timezone_band                      TEXT,
  hourly_rate_band                   TEXT,
  quality_band                       TEXT CHECK (quality_band IS NULL OR quality_band IN ('a', 'b', 'c', '')),
  distance_band_at_first_contact     TEXT NOT NULL CHECK (distance_band_at_first_contact IN ('N1', 'N2', 'N3', 'N4')),
  current_distance_band              TEXT NOT NULL CHECK (current_distance_band IN ('N1', 'N2', 'N3', 'N4')),
  last_engagement_date               DATE,
  linked_topic_ids                   TEXT,
  notes                              TEXT,
  source_git_sha                     TEXT,
  synced_at                          TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE compliance.sourcing_register_mirror ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS sourcing_register_mirror_anon_deny    ON compliance.sourcing_register_mirror;
DROP POLICY IF EXISTS sourcing_register_mirror_auth_deny    ON compliance.sourcing_register_mirror;
DROP POLICY IF EXISTS sourcing_register_mirror_service_role ON compliance.sourcing_register_mirror;

CREATE POLICY sourcing_register_mirror_anon_deny
  ON compliance.sourcing_register_mirror
  FOR ALL TO anon
  USING (false) WITH CHECK (false);

CREATE POLICY sourcing_register_mirror_auth_deny
  ON compliance.sourcing_register_mirror
  FOR ALL TO authenticated
  USING (false) WITH CHECK (false);

CREATE POLICY sourcing_register_mirror_service_role
  ON compliance.sourcing_register_mirror
  FOR ALL TO service_role
  USING (true) WITH CHECK (true);

GRANT SELECT, INSERT, UPDATE, DELETE ON compliance.sourcing_register_mirror TO service_role;
REVOKE ALL ON compliance.sourcing_register_mirror FROM PUBLIC;
REVOKE ALL ON compliance.sourcing_register_mirror FROM anon, authenticated;

CREATE INDEX IF NOT EXISTS idx_sourcing_register_mirror_discipline
  ON compliance.sourcing_register_mirror (discipline);

CREATE INDEX IF NOT EXISTS idx_sourcing_register_mirror_current_distance_band
  ON compliance.sourcing_register_mirror (current_distance_band);

CREATE INDEX IF NOT EXISTS idx_sourcing_register_mirror_quality_band
  ON compliance.sourcing_register_mirror (quality_band);
