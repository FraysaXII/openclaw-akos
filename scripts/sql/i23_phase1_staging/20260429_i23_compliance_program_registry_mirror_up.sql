-- Initiative 23 P2 — compliance.program_registry_mirror (STAGING)
-- Parity: supabase/migrations/<ts>_i23_compliance_program_registry_mirror.sql
-- CSV SSOT: docs/references/hlk/compliance/dimensions/PROGRAM_REGISTRY.csv

CREATE SCHEMA IF NOT EXISTS compliance;

CREATE TABLE IF NOT EXISTS compliance.program_registry_mirror (
  program_id                  TEXT NOT NULL,
  process_item_id             TEXT,
  program_name                TEXT,
  program_code                TEXT,
  lifecycle_status            TEXT,
  parent_program_id           TEXT,
  consumes_program_ids        TEXT,
  produces_for_program_ids    TEXT,
  subsumes_program_ids        TEXT,
  primary_owner_role          TEXT,
  default_plane               TEXT,
  start_date                  TEXT,
  target_close_date           TEXT,
  risk_class                  TEXT,
  notes                       TEXT,
  source_git_sha              TEXT NOT NULL,
  synced_at                   TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (program_id)
);

CREATE INDEX IF NOT EXISTS program_registry_mirror_synced_at_idx
  ON compliance.program_registry_mirror (synced_at DESC);
CREATE INDEX IF NOT EXISTS program_registry_mirror_lifecycle_idx
  ON compliance.program_registry_mirror (lifecycle_status);
CREATE INDEX IF NOT EXISTS program_registry_mirror_plane_idx
  ON compliance.program_registry_mirror (default_plane);
CREATE INDEX IF NOT EXISTS program_registry_mirror_code_idx
  ON compliance.program_registry_mirror (program_code);

ALTER TABLE compliance.program_registry_mirror ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS program_registry_mirror_deny_authenticated ON compliance.program_registry_mirror;
DROP POLICY IF EXISTS program_registry_mirror_deny_anon ON compliance.program_registry_mirror;
CREATE POLICY program_registry_mirror_deny_authenticated
  ON compliance.program_registry_mirror FOR ALL TO authenticated USING (false);
CREATE POLICY program_registry_mirror_deny_anon
  ON compliance.program_registry_mirror FOR ALL TO anon USING (false);

REVOKE ALL ON TABLE compliance.program_registry_mirror FROM PUBLIC;
GRANT ALL ON TABLE compliance.program_registry_mirror TO service_role;
