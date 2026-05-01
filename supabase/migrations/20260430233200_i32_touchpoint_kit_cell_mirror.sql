-- Initiative 32 P3 — compliance.touchpoint_kit_cell_mirror
-- D-IH-32-C: Touchpoint-kit cell registry as canonical dimension. Each row
-- mirrors one (persona x channel x language) template file under
-- docs/references/hlk/v3.0/_assets/touchpoint-kit/. Same governance pattern
-- as compliance.persona_registry_mirror. The validator's FS-vs-CSV drift
-- detector enforces 1:1 parity with the filesystem.

CREATE SCHEMA IF NOT EXISTS compliance;
COMMENT ON SCHEMA compliance IS 'HLK git-backed projections; SSOT remains docs/references/hlk/compliance/*.csv';

CREATE TABLE IF NOT EXISTS compliance.touchpoint_kit_cell_mirror (
  cell_id                       TEXT NOT NULL,
  persona_id                    TEXT,    -- FK to PERSONA_REGISTRY (informational, no SQL FK)
  channel_id                    TEXT,    -- FK to CHANNEL_TOUCHPOINT_REGISTRY
  language                      TEXT,    -- en | es | fr
  topic_ids                     TEXT,    -- semicolon-list TEXT
  template_path                 TEXT,    -- repo-relative
  distance_variants_in_file     TEXT,    -- semicolon-list of N1;N2;N3;N4
  lifecycle_status              TEXT,
  last_review                   DATE,
  notes                         TEXT,
  source_git_sha                TEXT NOT NULL,
  synced_at                     TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (cell_id)
);

COMMENT ON TABLE compliance.touchpoint_kit_cell_mirror IS
  'Initiative 32 P3 — projection of TOUCHPOINT_KIT_CELL_REGISTRY.csv. SSOT is the git CSV.';

CREATE INDEX IF NOT EXISTS touchpoint_kit_cell_mirror_synced_at_idx
  ON compliance.touchpoint_kit_cell_mirror (synced_at DESC);
CREATE INDEX IF NOT EXISTS touchpoint_kit_cell_mirror_persona_idx
  ON compliance.touchpoint_kit_cell_mirror (persona_id);
CREATE INDEX IF NOT EXISTS touchpoint_kit_cell_mirror_channel_idx
  ON compliance.touchpoint_kit_cell_mirror (channel_id);
CREATE INDEX IF NOT EXISTS touchpoint_kit_cell_mirror_language_idx
  ON compliance.touchpoint_kit_cell_mirror (language);
CREATE INDEX IF NOT EXISTS touchpoint_kit_cell_mirror_lifecycle_idx
  ON compliance.touchpoint_kit_cell_mirror (lifecycle_status);

ALTER TABLE compliance.touchpoint_kit_cell_mirror ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS touchpoint_kit_cell_mirror_deny_authenticated ON compliance.touchpoint_kit_cell_mirror;
DROP POLICY IF EXISTS touchpoint_kit_cell_mirror_deny_anon ON compliance.touchpoint_kit_cell_mirror;
CREATE POLICY touchpoint_kit_cell_mirror_deny_authenticated
  ON compliance.touchpoint_kit_cell_mirror FOR ALL TO authenticated USING (false);
CREATE POLICY touchpoint_kit_cell_mirror_deny_anon
  ON compliance.touchpoint_kit_cell_mirror FOR ALL TO anon USING (false);

REVOKE ALL ON TABLE compliance.touchpoint_kit_cell_mirror FROM PUBLIC;
GRANT ALL ON TABLE compliance.touchpoint_kit_cell_mirror TO service_role;
