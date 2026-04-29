-- Parity: scripts/sql/i21_phase1_staging/20260428_i21_compliance_adviser_disciplines_mirror_up.sql
-- Initiative 21 — ADVOPS plane disciplines lookup (compliance.adviser_engagement_disciplines_mirror)

CREATE SCHEMA IF NOT EXISTS compliance;

CREATE TABLE IF NOT EXISTS compliance.adviser_engagement_disciplines_mirror (
  discipline_id              TEXT NOT NULL,
  discipline_code            TEXT,
  display_name               TEXT,
  canonical_role             TEXT,
  default_process_item_id    TEXT,
  default_program_id         TEXT,
  description                TEXT,
  notes                      TEXT,
  source_git_sha             TEXT NOT NULL,
  synced_at                  TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (discipline_id)
);

CREATE INDEX IF NOT EXISTS adviser_engagement_disciplines_mirror_synced_at_idx
  ON compliance.adviser_engagement_disciplines_mirror (synced_at DESC);
CREATE INDEX IF NOT EXISTS adviser_engagement_disciplines_mirror_program_idx
  ON compliance.adviser_engagement_disciplines_mirror (default_program_id);

ALTER TABLE compliance.adviser_engagement_disciplines_mirror ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS adviser_engagement_disciplines_mirror_deny_authenticated ON compliance.adviser_engagement_disciplines_mirror;
DROP POLICY IF EXISTS adviser_engagement_disciplines_mirror_deny_anon ON compliance.adviser_engagement_disciplines_mirror;
CREATE POLICY adviser_engagement_disciplines_mirror_deny_authenticated
  ON compliance.adviser_engagement_disciplines_mirror FOR ALL TO authenticated USING (false);
CREATE POLICY adviser_engagement_disciplines_mirror_deny_anon
  ON compliance.adviser_engagement_disciplines_mirror FOR ALL TO anon USING (false);

REVOKE ALL ON TABLE compliance.adviser_engagement_disciplines_mirror FROM PUBLIC;
GRANT ALL ON TABLE compliance.adviser_engagement_disciplines_mirror TO service_role;
