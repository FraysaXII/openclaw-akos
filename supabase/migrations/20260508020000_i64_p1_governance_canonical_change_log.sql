-- I64 P1 — governance.canonical_change_log + governance.repo_health_view
--
-- I64 master-roadmap.md §P1: append-only log of canonical CSV changes that
-- the I63 broadcast loop fans out to consumer repos. Mirrored shape lets
-- the Mission Control "Recent canonical changes" panel render the last 7
-- days at a glance.
--
-- D-IH-64-A: governance.* schema is the read-side projection home for
-- external-repo governance (consistent with I65's planning view that
-- already lives there).

CREATE SCHEMA IF NOT EXISTS governance;

-- =============================================================================
-- governance.canonical_change_log
--   Append-only history of canonical CSV broadcasts and their consumer status.
-- =============================================================================

CREATE TABLE IF NOT EXISTS governance.canonical_change_log (
  change_id        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  changed_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
  csv_name         TEXT NOT NULL,
  source_git_sha   TEXT NOT NULL,
  changed_by       TEXT,
  rows_changed     INTEGER,
  consumers        JSONB NOT NULL DEFAULT '[]'::jsonb,
  broadcast_status TEXT NOT NULL DEFAULT 'pending'
                   CHECK (broadcast_status IN ('pending', 'posted', 'regen-pr', 'ack', 'failed')),
  thread_url       TEXT,
  notes            TEXT
);

COMMENT ON TABLE governance.canonical_change_log IS
  'I64 P1 - append-only log of canonical CSV broadcasts. Backs the "Recent canonical changes" panel on /governance/external-repos.';
COMMENT ON COLUMN governance.canonical_change_log.consumers IS
  'JSONB array of {slug:string, status:"posted"|"regen-pr"|"ack"|"failed"} entries.';

CREATE INDEX IF NOT EXISTS canonical_change_log_changed_at_idx
  ON governance.canonical_change_log (changed_at DESC);
CREATE INDEX IF NOT EXISTS canonical_change_log_csv_name_idx
  ON governance.canonical_change_log (csv_name);
CREATE INDEX IF NOT EXISTS canonical_change_log_broadcast_status_idx
  ON governance.canonical_change_log (broadcast_status);

ALTER TABLE governance.canonical_change_log ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS canonical_change_log_read_authenticated ON governance.canonical_change_log;
DROP POLICY IF EXISTS canonical_change_log_service_role_all   ON governance.canonical_change_log;
CREATE POLICY canonical_change_log_read_authenticated
  ON governance.canonical_change_log FOR SELECT TO authenticated USING (true);
CREATE POLICY canonical_change_log_service_role_all
  ON governance.canonical_change_log FOR ALL TO service_role USING (true) WITH CHECK (true);

GRANT SELECT ON governance.canonical_change_log TO authenticated;
GRANT ALL    ON governance.canonical_change_log TO service_role;

-- =============================================================================
-- governance.repo_health_view
--   Joined registry + latest health-snapshot for the "Repos at a glance" grid.
--   One row per repo, with the most recent snapshot_date prevailing.
-- =============================================================================

CREATE OR REPLACE VIEW governance.repo_health_view AS
WITH latest_snapshot AS (
  SELECT DISTINCT ON (repo_slug)
    repo_slug,
    snapshot_date,
    commit_sha_at_snapshot,
    cursor_rule_count,
    has_external_repo_contract,
    has_akos_mirror_rule,
    language_frontmatter_compliance_pct,
    brand_jargon_violations,
    embedded_obsidian_snapshot_present
  FROM compliance.repo_health_snapshot_mirror
  ORDER BY repo_slug, snapshot_date DESC
)
SELECT
  r.repo_slug,
  r.github_url,
  r.class,
  r.primary_owner_role,
  r.lifecycle_status,
  r.topic_ids,
  r.notes AS registry_notes,
  s.snapshot_date AS last_snapshot_date,
  s.commit_sha_at_snapshot,
  s.cursor_rule_count,
  s.has_external_repo_contract,
  s.has_akos_mirror_rule,
  s.language_frontmatter_compliance_pct,
  s.brand_jargon_violations,
  s.embedded_obsidian_snapshot_present,
  CASE
    WHEN r.lifecycle_status = 'reference' THEN 'reference'
    WHEN s.snapshot_date IS NULL THEN 'unknown'
    WHEN s.snapshot_date < CURRENT_DATE - INTERVAL '30 days' THEN 'stale'
    WHEN COALESCE(s.brand_jargon_violations, 0) > 0
      AND r.class IN ('platform', 'client-delivery') THEN 'attention'
    WHEN s.has_external_repo_contract IS DISTINCT FROM TRUE
      AND r.class IN ('platform', 'client-delivery', 'internal') THEN 'attention'
    WHEN COALESCE(s.language_frontmatter_compliance_pct, 0) < 0.8
      AND r.class IN ('platform', 'client-delivery') THEN 'attention'
    ELSE 'blessed'
  END AS status_dot,
  CASE
    WHEN s.snapshot_date IS NULL THEN NULL
    ELSE (CURRENT_DATE - s.snapshot_date)::INTEGER
  END AS blessed_age_days,
  r.synced_at AS registry_synced_at
FROM compliance.repository_registry_mirror r
LEFT JOIN latest_snapshot s ON s.repo_slug = r.repo_slug;

COMMENT ON VIEW governance.repo_health_view IS
  'I64 P1 - joined view of compliance.repository_registry_mirror + latest compliance.repo_health_snapshot_mirror per repo. Backs the "Repos at a glance" panel. Computed status_dot maps to GREEN/AMBER/RED logic in the page spec.';

GRANT SELECT ON governance.repo_health_view TO authenticated, service_role;

-- =============================================================================
-- governance.canonical_change_log_recent_view
--   Convenience wrapper: last 7 days of the change log, broadcast-status sorted.
-- =============================================================================

CREATE OR REPLACE VIEW governance.canonical_change_log_recent_view AS
SELECT
  change_id,
  changed_at,
  csv_name,
  source_git_sha,
  changed_by,
  rows_changed,
  consumers,
  broadcast_status,
  thread_url,
  notes
FROM governance.canonical_change_log
WHERE changed_at >= now() - INTERVAL '7 days'
ORDER BY changed_at DESC;

COMMENT ON VIEW governance.canonical_change_log_recent_view IS
  'I64 P1 - last 7 days of canonical change broadcasts. Used by the "Recent canonical changes" panel.';

GRANT SELECT ON governance.canonical_change_log_recent_view TO authenticated, service_role;

NOTIFY pgrst, 'reload schema';
