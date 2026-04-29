-- Initiative 21 — compliance.adviser_open_questions_mirror (STAGING)
-- Parity: supabase/migrations/*_i21_compliance_adviser_open_questions_mirror.sql
-- CSV SSOT: docs/references/hlk/compliance/ADVISER_OPEN_QUESTIONS.csv

CREATE SCHEMA IF NOT EXISTS compliance;

CREATE TABLE IF NOT EXISTS compliance.adviser_open_questions_mirror (
  question_id         TEXT NOT NULL,
  discipline_id       TEXT,
  program_id          TEXT,
  question_or_action  TEXT,
  owner_role          TEXT,
  target_date         TEXT,
  status              TEXT,
  poi_ref_id          TEXT,
  goi_ref_id          TEXT,
  evidence_pointer    TEXT,
  notes               TEXT,
  source_git_sha      TEXT NOT NULL,
  synced_at           TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (question_id)
);

CREATE INDEX IF NOT EXISTS adviser_open_questions_mirror_synced_at_idx
  ON compliance.adviser_open_questions_mirror (synced_at DESC);
CREATE INDEX IF NOT EXISTS adviser_open_questions_mirror_discipline_idx
  ON compliance.adviser_open_questions_mirror (discipline_id);
CREATE INDEX IF NOT EXISTS adviser_open_questions_mirror_program_idx
  ON compliance.adviser_open_questions_mirror (program_id);

ALTER TABLE compliance.adviser_open_questions_mirror ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS adviser_open_questions_mirror_deny_authenticated ON compliance.adviser_open_questions_mirror;
DROP POLICY IF EXISTS adviser_open_questions_mirror_deny_anon ON compliance.adviser_open_questions_mirror;
CREATE POLICY adviser_open_questions_mirror_deny_authenticated
  ON compliance.adviser_open_questions_mirror FOR ALL TO authenticated USING (false);
CREATE POLICY adviser_open_questions_mirror_deny_anon
  ON compliance.adviser_open_questions_mirror FOR ALL TO anon USING (false);

REVOKE ALL ON TABLE compliance.adviser_open_questions_mirror FROM PUBLIC;
GRANT ALL ON TABLE compliance.adviser_open_questions_mirror TO service_role;
