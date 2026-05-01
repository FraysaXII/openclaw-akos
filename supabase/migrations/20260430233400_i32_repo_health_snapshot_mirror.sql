-- Initiative 32 P7 — compliance.repo_health_snapshot_mirror
-- D-IH-32-L: pull-based snapshot of external repo state. Append-only history
-- (each weekly snapshot is one batch of rows; PK includes snapshot_date so
-- consecutive weeks are distinct rows for the same repo_slug).
-- Same governance posture as compliance.validation_runs (operational mirror;
-- not git SSOT). The CSV is the latest weekly snapshot; the mirror is the
-- audit history.

CREATE SCHEMA IF NOT EXISTS compliance;

CREATE TABLE IF NOT EXISTS compliance.repo_health_snapshot_mirror (
  repo_slug                              TEXT NOT NULL,
  snapshot_date                          DATE NOT NULL,
  commit_sha_at_snapshot                 TEXT,
  cursor_rule_count                      INT,
  has_external_repo_contract             BOOLEAN,
  has_akos_mirror_rule                   BOOLEAN,
  language_frontmatter_compliance_pct    NUMERIC,
  brand_jargon_violations                INT,
  embedded_obsidian_snapshot_present     BOOLEAN,
  notes                                  TEXT,
  source_git_sha                         TEXT NOT NULL,
  synced_at                              TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (repo_slug, snapshot_date)
);

COMMENT ON TABLE compliance.repo_health_snapshot_mirror IS
  'Initiative 32 P7 (D-IH-32-L) — append-only weekly snapshot of external Holistika repo health.';

CREATE INDEX IF NOT EXISTS repo_health_snapshot_synced_at_idx
  ON compliance.repo_health_snapshot_mirror (synced_at DESC);
CREATE INDEX IF NOT EXISTS repo_health_snapshot_date_idx
  ON compliance.repo_health_snapshot_mirror (snapshot_date DESC);
CREATE INDEX IF NOT EXISTS repo_health_snapshot_slug_idx
  ON compliance.repo_health_snapshot_mirror (repo_slug);
-- Partial index for "repos missing the EXTERNAL_REPO_CONTRACT" dashboard query.
CREATE INDEX IF NOT EXISTS repo_health_snapshot_missing_contract_idx
  ON compliance.repo_health_snapshot_mirror (snapshot_date DESC)
  WHERE has_external_repo_contract = false;

ALTER TABLE compliance.repo_health_snapshot_mirror ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS repo_health_snapshot_deny_authenticated ON compliance.repo_health_snapshot_mirror;
DROP POLICY IF EXISTS repo_health_snapshot_deny_anon ON compliance.repo_health_snapshot_mirror;
CREATE POLICY repo_health_snapshot_deny_authenticated
  ON compliance.repo_health_snapshot_mirror FOR ALL TO authenticated USING (false);
CREATE POLICY repo_health_snapshot_deny_anon
  ON compliance.repo_health_snapshot_mirror FOR ALL TO anon USING (false);

REVOKE ALL ON TABLE compliance.repo_health_snapshot_mirror FROM PUBLIC;
GRANT ALL ON TABLE compliance.repo_health_snapshot_mirror TO service_role;
