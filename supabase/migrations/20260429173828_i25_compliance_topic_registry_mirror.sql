-- Parity: scripts/sql/i25_phase1_staging/20260429_i25_compliance_topic_registry_mirror_up.sql
-- Initiative 25 P2 - compliance.topic_registry_mirror

CREATE SCHEMA IF NOT EXISTS compliance;

CREATE TABLE IF NOT EXISTS compliance.topic_registry_mirror (
  topic_id              TEXT NOT NULL,
  title                 TEXT,
  topic_class           TEXT,
  lifecycle_status      TEXT,
  primary_owner_role    TEXT,
  program_id            TEXT,
  plane                 TEXT,
  parent_topic          TEXT,
  related_topics        TEXT,
  depends_on            TEXT,
  subsumes              TEXT,
  subsumed_by           TEXT,
  manifest_path         TEXT,
  notes                 TEXT,
  source_git_sha        TEXT NOT NULL,
  synced_at             TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (topic_id)
);

CREATE INDEX IF NOT EXISTS topic_registry_mirror_synced_at_idx ON compliance.topic_registry_mirror (synced_at DESC);
CREATE INDEX IF NOT EXISTS topic_registry_mirror_program_idx ON compliance.topic_registry_mirror (program_id);
CREATE INDEX IF NOT EXISTS topic_registry_mirror_plane_idx ON compliance.topic_registry_mirror (plane);
CREATE INDEX IF NOT EXISTS topic_registry_mirror_class_idx ON compliance.topic_registry_mirror (topic_class);

ALTER TABLE compliance.topic_registry_mirror ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS topic_registry_mirror_deny_authenticated ON compliance.topic_registry_mirror;
DROP POLICY IF EXISTS topic_registry_mirror_deny_anon ON compliance.topic_registry_mirror;
CREATE POLICY topic_registry_mirror_deny_authenticated ON compliance.topic_registry_mirror FOR ALL TO authenticated USING (false);
CREATE POLICY topic_registry_mirror_deny_anon ON compliance.topic_registry_mirror FOR ALL TO anon USING (false);

REVOKE ALL ON TABLE compliance.topic_registry_mirror FROM PUBLIC;
GRANT ALL ON TABLE compliance.topic_registry_mirror TO service_role;
