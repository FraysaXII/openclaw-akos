-- I65 P1.2 — governance schema + planning_workspace_view + workspace_markdown_cache
--
-- Per docs/wip/planning/65-akos-planning-workspace-panel/reports/data-model-2026-05-07.md.
--
-- D-IH-65-A: governance.* schema separate from compliance.* mirrors and erp.*
--   read-side projections. governance.* contains views/tables that join
--   registry mirrors with operational metadata (markdown cache, search index).
-- D-IH-65-B: GitHub is canonical for markdown bodies; governance.workspace_markdown_cache
--   is a 5-minute lossy fallback only. Cache eviction is best-effort, not transactional.
-- D-IH-65-C: planning_workspace_view is computed live (not materialised) — registry
--   mirrors land via the I63 sync cadence; freshness flags are computed from the row's
--   last_review against the current date.
-- D-IH-65-D: SECURITY INVOKER — server-side hlk-erp uses the service_role client to
--   read the view (consistent with existing erp.* projection pattern). Operator
--   access-level gating happens at the route layer
--   (holistika_ops.current_access_level() >= 4).

CREATE SCHEMA IF NOT EXISTS governance;

GRANT USAGE ON SCHEMA governance TO authenticated, anon, service_role;

-- =============================================================================
-- governance.planning_workspace_view
--   One row per initiative; joined ops + decision counts.
-- =============================================================================

CREATE OR REPLACE VIEW governance.planning_workspace_view AS
WITH ops_per_initiative AS (
  SELECT
    originating_initiative_id AS initiative_id,
    COUNT(*) FILTER (WHERE status = 'open')   AS open_ops,
    COUNT(*) FILTER (WHERE status = 'closed') AS closed_ops,
    COUNT(*)                                  AS total_ops,
    MAX(rice_score)                           AS top_rice
  FROM compliance.ops_register_mirror
  GROUP BY originating_initiative_id
),
decisions_per_initiative AS (
  SELECT
    initiating_initiative_id AS initiative_id,
    COUNT(*)                                       AS total_decisions,
    COUNT(*) FILTER (WHERE status = 'active')      AS active_decisions,
    COUNT(*) FILTER (WHERE status = 'superseded')  AS superseded_decisions,
    MAX(decided_at)                                AS last_decision_at
  FROM compliance.decision_register_mirror
  GROUP BY initiating_initiative_id
)
SELECT
  i.initiative_id,
  i.repo_slug,
  i.folder_path,
  i.title,
  i.status,
  i.cycle_id,
  i.owner_role,
  i.inception_date,
  i.last_review,
  i.closed_at,
  i.archived_at,
  i.cadence,
  i.gated_on,
  i.operator_action,
  i.inception_decision_id,
  i.closure_decision_id,
  i.continuous_rationale,
  i.linked_topic_ids,
  i.notes AS initiative_notes,
  CASE
    WHEN i.status NOT IN ('active', 'continuous', 'gated_external', 'gated_operator') THEN 'fresh'
    WHEN i.last_review IS NULL                                                        THEN 'stale'
    WHEN i.last_review < CURRENT_DATE - INTERVAL '21 days'                            THEN 'stale'
    WHEN i.last_review < CURRENT_DATE - INTERVAL '14 days'                            THEN 'aging'
    ELSE 'fresh'
  END AS freshness_state,
  COALESCE(o.open_ops, 0)              AS open_ops_count,
  COALESCE(o.closed_ops, 0)            AS closed_ops_count,
  COALESCE(o.total_ops, 0)             AS total_ops_count,
  COALESCE(o.top_rice, 0)              AS top_ops_rice,
  COALESCE(d.total_decisions, 0)       AS total_decisions,
  COALESCE(d.active_decisions, 0)      AS active_decisions,
  COALESCE(d.superseded_decisions, 0)  AS superseded_decisions,
  d.last_decision_at,
  i.synced_at AS registry_synced_at
FROM compliance.initiative_registry_mirror i
LEFT JOIN ops_per_initiative o      ON o.initiative_id = i.initiative_id
LEFT JOIN decisions_per_initiative d ON d.initiative_id = i.initiative_id;

COMMENT ON VIEW governance.planning_workspace_view IS
  'I65 P1.2 — joined registry state per initiative for /operator/planning/. Live computed; freshness derived from last_review vs CURRENT_DATE.';

GRANT SELECT ON governance.planning_workspace_view TO authenticated, service_role;

-- =============================================================================
-- governance.workspace_markdown_cache
--   5-minute fallback for GitHub Contents API (D-IH-65-B). Lossy and rebuildable.
-- =============================================================================

CREATE TABLE IF NOT EXISTS governance.workspace_markdown_cache (
  cache_key      TEXT PRIMARY KEY,
  ref            TEXT NOT NULL,                                                     -- 'main' or commit SHA
  path           TEXT NOT NULL,                                                     -- 'docs/wip/planning/65-.../master-roadmap.md'
  body           TEXT NOT NULL,
  size_bytes     INTEGER NOT NULL,
  fetched_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
  expires_at     TIMESTAMPTZ NOT NULL DEFAULT (now() + INTERVAL '5 minutes')
);

COMMENT ON TABLE governance.workspace_markdown_cache IS
  'I65 P1.2 — 5-minute lossy fallback for GitHub Contents API responses. NOT canonical (markdown lives at github.com/FraysaXII/openclaw-akos).';

CREATE INDEX IF NOT EXISTS workspace_markdown_cache_expires_idx
  ON governance.workspace_markdown_cache (expires_at);
CREATE INDEX IF NOT EXISTS workspace_markdown_cache_ref_path_idx
  ON governance.workspace_markdown_cache (ref, path);

ALTER TABLE governance.workspace_markdown_cache ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS workspace_markdown_cache_read_authenticated ON governance.workspace_markdown_cache;
DROP POLICY IF EXISTS workspace_markdown_cache_service_role_all   ON governance.workspace_markdown_cache;
CREATE POLICY workspace_markdown_cache_read_authenticated
  ON governance.workspace_markdown_cache FOR SELECT TO authenticated USING (true);
CREATE POLICY workspace_markdown_cache_service_role_all
  ON governance.workspace_markdown_cache FOR ALL TO service_role USING (true) WITH CHECK (true);

GRANT SELECT ON governance.workspace_markdown_cache TO authenticated;
GRANT ALL    ON governance.workspace_markdown_cache TO service_role;

-- =============================================================================
-- governance.purge_expired_workspace_cache()
--   Idempotent eviction. Called by the markdown reader on cache miss; can also
--   be wired to pg_cron later if needed (D-IH-65-B: best-effort eviction).
-- =============================================================================

CREATE OR REPLACE FUNCTION governance.purge_expired_workspace_cache()
RETURNS INTEGER
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = governance, pg_temp
AS $$
DECLARE
  deleted_count INTEGER;
BEGIN
  DELETE FROM governance.workspace_markdown_cache WHERE expires_at < now();
  GET DIAGNOSTICS deleted_count = ROW_COUNT;
  RETURN deleted_count;
END;
$$;

COMMENT ON FUNCTION governance.purge_expired_workspace_cache IS
  'I65 P1.2 — best-effort eviction of expired markdown cache rows. Returns count deleted.';

GRANT EXECUTE ON FUNCTION governance.purge_expired_workspace_cache() TO authenticated, service_role;

NOTIFY pgrst, 'reload schema';
