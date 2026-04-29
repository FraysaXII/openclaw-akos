-- Initiative 21 — compliance.goipoi_register_mirror (STAGING)
-- Parity: supabase/migrations/*_i21_compliance_goipoi_register_mirror.sql
-- Idempotent where practical. CSV SSOT: docs/references/hlk/compliance/GOI_POI_REGISTER.csv.

CREATE SCHEMA IF NOT EXISTS compliance;
COMMENT ON SCHEMA compliance IS 'HLK git-backed projections; SSOT remains docs/references/hlk/compliance/*.csv';

CREATE TABLE IF NOT EXISTS compliance.goipoi_register_mirror (
  ref_id            TEXT NOT NULL,
  entity_kind       TEXT,
  class             TEXT,
  is_public_entity  TEXT,
  display_name      TEXT,
  lens              TEXT,
  sensitivity       TEXT,
  program_id        TEXT,
  role_owner        TEXT,
  process_item_id   TEXT,
  primary_link      TEXT,
  notes             TEXT,
  source_git_sha    TEXT NOT NULL,
  synced_at         TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (ref_id)
);

CREATE INDEX IF NOT EXISTS goipoi_register_mirror_synced_at_idx
  ON compliance.goipoi_register_mirror (synced_at DESC);
CREATE INDEX IF NOT EXISTS goipoi_register_mirror_program_idx
  ON compliance.goipoi_register_mirror (program_id);
CREATE INDEX IF NOT EXISTS goipoi_register_mirror_class_idx
  ON compliance.goipoi_register_mirror (class);

ALTER TABLE compliance.goipoi_register_mirror ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS goipoi_register_mirror_deny_authenticated ON compliance.goipoi_register_mirror;
DROP POLICY IF EXISTS goipoi_register_mirror_deny_anon ON compliance.goipoi_register_mirror;
CREATE POLICY goipoi_register_mirror_deny_authenticated
  ON compliance.goipoi_register_mirror FOR ALL TO authenticated USING (false);
CREATE POLICY goipoi_register_mirror_deny_anon
  ON compliance.goipoi_register_mirror FOR ALL TO anon USING (false);

REVOKE ALL ON TABLE compliance.goipoi_register_mirror FROM PUBLIC;
GRANT ALL ON TABLE compliance.goipoi_register_mirror TO service_role;
