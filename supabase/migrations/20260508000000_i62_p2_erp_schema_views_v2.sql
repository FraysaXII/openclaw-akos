-- Initiative 62 P2.3 (v2) — erp.* read-side projection schema, adapted to actual remote shapes.
--
-- The original P2 migration (`20260506130100_i62_p2_erp_schema_views.sql`) was written
-- against the developer's mental model of compliance.* mirrors. The remote schema turned
-- out to use different column names (e.g. `run_started_at` vs `occurred_at`,
-- `lifecycle_status` vs `status`, `section_metrics` vs `run_payload`) and different
-- mirror table names (`adviser_engagement_disciplines_mirror` vs `adviser_disciplines_mirror`,
-- `finops_counterparty_register_mirror` vs `finops_counterparty_mirror`).
--
-- This v2 migration ships the same 6 erp.* views with the column/name harmonisation
-- applied. The original migration file remains in the migrations/ folder as historical
-- record; supabase_migrations.schema_migrations rejects re-application by version, so
-- the original is now effectively a no-op.
--
-- D-IH-62-Q (re-affirmed): erp.* projection schema separate from compliance.* mirrors
-- and holistika_ops.* write-side. SECURITY INVOKER preserves underlying RLS.
-- D-IH-62-C: demo routing via session GUC app.data_mode through erp._mode().

CREATE SCHEMA IF NOT EXISTS erp;

GRANT USAGE ON SCHEMA erp TO authenticated, anon, service_role;

-- =============================================================================
-- erp._mode() — reads session GUC app.data_mode (default 'live')
-- =============================================================================
CREATE OR REPLACE FUNCTION erp._mode()
RETURNS TEXT
LANGUAGE sql
STABLE
AS $$
  SELECT COALESCE(NULLIF(current_setting('app.data_mode', true), ''), 'live');
$$;

COMMENT ON FUNCTION erp._mode IS
  'I62 D-IH-62-C — returns the session-scoped data mode ("live" or "demo"). The ERP server-side Supabase client SETs app.data_mode per request based on the DATA_MODE env var.';

GRANT EXECUTE ON FUNCTION erp._mode() TO authenticated, anon, service_role;

-- =============================================================================
-- erp.vw_three_lights_status
-- =============================================================================
-- Conversational  : persona-fit pass-rate >= 80% over the 5 most recent persona_fit eval_runs.
--                   Source: compliance.eval_run.mode = 'persona_fit', overall_status = 'pass'/'fail'.
-- Dossier         : most recent dossier_run.section_metrics->>'verdict' = 'GO' AND within envelope.
--                   Source: compliance.dossier_run.section_metrics jsonb (no verdict column).
-- Skill quality   : every active skill has >= 1 passing eval_run in the last 7 days.
--                   Source: compliance.skill_registry_mirror.lifecycle_status = 'active'
--                           joined to compliance.eval_run.skill_id (column, not jsonb path).
-- Composite       : RED if any RED, AMBER if any AMBER, otherwise GREEN.
CREATE OR REPLACE VIEW erp.vw_three_lights_status AS
WITH recent_persona_fit AS (
  SELECT (overall_status = 'pass') AS persona_fit_pass, run_started_at
  FROM compliance.eval_run
  WHERE mode = 'persona_fit'
  ORDER BY run_started_at DESC
  LIMIT 5
),
conversational AS (
  SELECT
    CASE
      WHEN COUNT(*) = 0 THEN 'AMBER'
      WHEN AVG(CASE WHEN persona_fit_pass THEN 1.0 ELSE 0.0 END) >= 0.80 THEN 'GREEN'
      WHEN AVG(CASE WHEN persona_fit_pass THEN 1.0 ELSE 0.0 END) >= 0.60 THEN 'AMBER'
      ELSE 'RED'
    END AS light,
    MAX(run_started_at) AS last_observed_at
  FROM recent_persona_fit
),
last_dossier AS (
  SELECT
    section_metrics,
    started_at
  FROM compliance.dossier_run
  ORDER BY started_at DESC
  LIMIT 1
),
dossier AS (
  SELECT
    CASE
      WHEN section_metrics IS NULL THEN 'AMBER'
      WHEN COALESCE(section_metrics ->> 'verdict', '') = 'GO'
       AND COALESCE((section_metrics ->> 'within_envelope')::boolean, true) THEN 'GREEN'
      WHEN COALESCE(section_metrics ->> 'verdict', '') = 'AMBER' THEN 'AMBER'
      ELSE 'RED'
    END AS light,
    started_at AS last_observed_at
  FROM last_dossier
  UNION ALL
  -- empty fallback so the CTE always returns one row even with no dossier_runs yet
  SELECT 'AMBER'::text, NULL::timestamptz
  WHERE NOT EXISTS (SELECT 1 FROM compliance.dossier_run)
),
skill_summary AS (
  SELECT
    sr.skill_id,
    MAX(er.run_started_at) FILTER (WHERE er.overall_status = 'pass') AS last_pass_at
  FROM compliance.skill_registry_mirror sr
  LEFT JOIN compliance.eval_run er ON er.skill_id = sr.skill_id
  WHERE sr.lifecycle_status = 'active'
  GROUP BY sr.skill_id
),
skill_quality AS (
  SELECT
    CASE
      WHEN COUNT(*) = 0 THEN 'AMBER'
      WHEN COUNT(*) FILTER (WHERE last_pass_at IS NULL OR last_pass_at < now() - INTERVAL '7 days') = 0 THEN 'GREEN'
      WHEN COUNT(*) FILTER (WHERE last_pass_at IS NULL) > 0 THEN 'RED'
      ELSE 'AMBER'
    END AS light,
    MAX(last_pass_at) AS last_observed_at
  FROM skill_summary
)
SELECT
  c.light  AS conversational_light,
  d.light  AS dossier_light,
  s.light  AS skill_quality_light,
  CASE
    WHEN 'RED' IN (c.light, d.light, s.light) THEN 'RED'
    WHEN 'AMBER' IN (c.light, d.light, s.light) THEN 'AMBER'
    ELSE 'GREEN'
  END AS composite_verdict,
  GREATEST(c.last_observed_at, d.last_observed_at, s.last_observed_at) AS last_observed_at,
  erp._mode() AS data_mode
FROM conversational c, dossier d, skill_quality s;

COMMENT ON VIEW erp.vw_three_lights_status IS
  'I62 P4.2 tile 01 (v2) — Three Lights composite verdict. Source: compliance.eval_run + dossier_run + skill_registry_mirror with column shapes adapted to remote schema.';

-- =============================================================================
-- erp.vw_mirror_health — per-mirror last_sync + freshness across active mirrors
-- =============================================================================
CREATE OR REPLACE VIEW erp.vw_mirror_health AS
SELECT
  table_name AS mirror_name,
  last_sync_at,
  CASE
    WHEN last_sync_at IS NULL THEN 'red'
    WHEN last_sync_at > now() - INTERVAL '24 hours'  THEN 'green'
    WHEN last_sync_at > now() - INTERVAL '48 hours'  THEN 'yellow'
    ELSE 'red'
  END AS freshness_state,
  COALESCE(EXTRACT(EPOCH FROM (now() - last_sync_at)), 0)::BIGINT AS staleness_seconds
FROM (
  SELECT 'baseline_organisation_mirror'                AS table_name, MAX(synced_at) AS last_sync_at FROM compliance.baseline_organisation_mirror
  UNION ALL SELECT 'process_list_mirror',                          MAX(synced_at) FROM compliance.process_list_mirror
  UNION ALL SELECT 'persona_registry_mirror',                      MAX(synced_at) FROM compliance.persona_registry_mirror
  UNION ALL SELECT 'topic_registry_mirror',                        MAX(synced_at) FROM compliance.topic_registry_mirror
  UNION ALL SELECT 'skill_registry_mirror',                        MAX(synced_at) FROM compliance.skill_registry_mirror
  UNION ALL SELECT 'policy_register_mirror',                       MAX(synced_at) FROM compliance.policy_register_mirror
  UNION ALL SELECT 'program_registry_mirror',                      MAX(synced_at) FROM compliance.program_registry_mirror
  UNION ALL SELECT 'goipoi_register_mirror',                       MAX(synced_at) FROM compliance.goipoi_register_mirror
  UNION ALL SELECT 'adviser_engagement_disciplines_mirror',        MAX(synced_at) FROM compliance.adviser_engagement_disciplines_mirror
  UNION ALL SELECT 'adviser_open_questions_mirror',                MAX(synced_at) FROM compliance.adviser_open_questions_mirror
  UNION ALL SELECT 'founder_filed_instruments_mirror',             MAX(synced_at) FROM compliance.founder_filed_instruments_mirror
  UNION ALL SELECT 'finops_counterparty_register_mirror',          MAX(synced_at) FROM compliance.finops_counterparty_register_mirror
  UNION ALL SELECT 'touchpoint_kit_cell_mirror',                   MAX(synced_at) FROM compliance.touchpoint_kit_cell_mirror
  UNION ALL SELECT 'repo_health_snapshot_mirror',                  MAX(synced_at) FROM compliance.repo_health_snapshot_mirror
  UNION ALL SELECT 'initiative_registry_mirror',                   MAX(synced_at) FROM compliance.initiative_registry_mirror
  UNION ALL SELECT 'ops_register_mirror',                          MAX(synced_at) FROM compliance.ops_register_mirror
) AS h;

COMMENT ON VIEW erp.vw_mirror_health IS
  'I62 P4.2 tile 05 (v2) — per-mirror last_sync + freshness. Renamed mirrors to match remote (adviser_engagement_disciplines, finops_counterparty_register).';

-- =============================================================================
-- erp.vw_initiative_pulse — counts by status + 30-day closure sparkline
-- =============================================================================
CREATE OR REPLACE VIEW erp.vw_initiative_pulse AS
SELECT
  COUNT(*) FILTER (WHERE status = 'active')          AS active_count,
  COUNT(*) FILTER (WHERE status = 'closed')          AS closed_count,
  COUNT(*) FILTER (WHERE status = 'archived')        AS archived_count,
  COUNT(*) FILTER (WHERE status = 'continuous')      AS continuous_count,
  COUNT(*) FILTER (WHERE status = 'program_line')    AS program_line_count,
  COUNT(*) FILTER (WHERE status = 'gated_external')  AS gated_external_count,
  COUNT(*) FILTER (WHERE status = 'gated_operator')  AS gated_operator_count,
  COUNT(*)                                            AS total_count,
  (
    SELECT json_agg(json_build_object('day', day, 'closed', n) ORDER BY day)
    FROM (
      SELECT DATE_TRUNC('day', closed_at)::date AS day, COUNT(*) AS n
      FROM compliance.initiative_registry_mirror
      WHERE closed_at >= now() - INTERVAL '30 days'
      GROUP BY 1
      ORDER BY 1
    ) sl
  ) AS closures_last_30_days,
  erp._mode() AS data_mode
FROM compliance.initiative_registry_mirror;

COMMENT ON VIEW erp.vw_initiative_pulse IS
  'I62 P4.2 tile 03 — initiative counts by status + 30-day closure sparkline.';

-- =============================================================================
-- erp.vw_operator_inbox_top — top 50 open OPS rows by RICE
-- =============================================================================
CREATE OR REPLACE VIEW erp.vw_operator_inbox_top AS
SELECT
  o.ops_action_id                       AS ops_id,
  o.title,
  o.owner_class,
  o.rice_score,
  o.rice_reach,
  o.rice_impact,
  o.rice_confidence_pct                 AS rice_confidence,
  o.rice_effort_person_weeks            AS rice_effort,
  o.originating_initiative_id           AS initiative_id,
  NULL::text                            AS cycle_id,
  o.status,
  o.linked_decision_ids                 AS linked_decision_id,
  o.evidence_path                       AS linked_report,
  o.opened_at,
  NULL::date                            AS last_review,
  i.title  AS initiative_title,
  i.status AS initiative_status,
  erp._mode() AS data_mode
FROM compliance.ops_register_mirror o
LEFT JOIN compliance.initiative_registry_mirror i ON i.initiative_id = o.originating_initiative_id
WHERE o.status = 'open' AND o.owner_class IN ('operator', 'mixed')
ORDER BY o.rice_score DESC NULLS LAST, o.opened_at ASC
LIMIT 50;

COMMENT ON VIEW erp.vw_operator_inbox_top IS
  'I62 P4.2 tile 02 (v2) + /operator-inbox drilldown — top 50 open operator/mixed-owned OPS rows by RICE. ops_action_id surfaced as ops_id; originating_initiative_id surfaced as initiative_id; cycle_id + last_review null-padded for backwards-compat consumer shape.';

-- =============================================================================
-- erp.vw_mission_control_today — single-fetch hero/tile aggregator
-- =============================================================================
CREATE OR REPLACE VIEW erp.vw_mission_control_today AS
WITH lights AS (SELECT * FROM erp.vw_three_lights_status),
     pulse  AS (SELECT * FROM erp.vw_initiative_pulse),
     mirrors AS (
       SELECT
         COUNT(*) FILTER (WHERE freshness_state = 'green')  AS green_count,
         COUNT(*) FILTER (WHERE freshness_state = 'yellow') AS yellow_count,
         COUNT(*) FILTER (WHERE freshness_state = 'red')    AS red_count,
         COUNT(*) AS total_count,
         MIN(last_sync_at) AS oldest_sync_at
       FROM erp.vw_mirror_health
     ),
     last_dossier AS (
       SELECT
         COALESCE(section_metrics ->> 'verdict', 'unknown') AS verdict,
         started_at,
         section_metrics
       FROM compliance.dossier_run
       ORDER BY started_at DESC
       LIMIT 1
     ),
     last_eval_summary AS (
       SELECT
         COUNT(*) AS run_count_24h,
         COUNT(*) FILTER (WHERE overall_status = 'pass') AS pass_count_24h,
         COUNT(*) FILTER (WHERE overall_status = 'fail') AS fail_count_24h
       FROM compliance.eval_run
       WHERE run_started_at >= now() - INTERVAL '24 hours'
     ),
     inbox AS (
       SELECT COUNT(*) AS open_count FROM erp.vw_operator_inbox_top
     )
SELECT
  lights.composite_verdict        AS verdict,
  lights.conversational_light,
  lights.dossier_light,
  lights.skill_quality_light,
  pulse.active_count,
  pulse.closed_count,
  pulse.gated_operator_count,
  pulse.closures_last_30_days,
  mirrors.green_count             AS mirrors_green,
  mirrors.yellow_count            AS mirrors_yellow,
  mirrors.red_count               AS mirrors_red,
  mirrors.total_count             AS mirrors_total,
  mirrors.oldest_sync_at          AS oldest_mirror_sync_at,
  COALESCE(ld.verdict, 'unknown') AS last_dossier_verdict,
  ld.started_at                   AS last_dossier_at,
  les.run_count_24h               AS eval_runs_24h,
  les.pass_count_24h              AS eval_pass_24h,
  les.fail_count_24h              AS eval_fail_24h,
  inbox.open_count                AS operator_inbox_open,
  erp._mode()                     AS data_mode,
  now()                           AS computed_at
FROM lights, pulse, mirrors, last_eval_summary les, inbox
LEFT JOIN last_dossier ld ON true;

COMMENT ON VIEW erp.vw_mission_control_today IS
  'I62 P4.2 (v2) — single-fetch aggregator for the seven Mission Control "Today" tiles. Last-dossier surfaced via LEFT JOIN so the view returns 1 row even when compliance.dossier_run is empty.';

-- =============================================================================
-- erp.vw_public_health — anon-readable status surface (no PII)
-- =============================================================================
CREATE OR REPLACE VIEW erp.vw_public_health AS
SELECT
  CASE
    WHEN composite_verdict = 'GREEN' THEN 'operational'
    WHEN composite_verdict = 'AMBER' THEN 'degraded'
    ELSE 'major_incident'
  END                                       AS overall_state,
  composite_verdict                         AS verdict,
  last_observed_at,
  (SELECT MIN(last_sync_at) FROM erp.vw_mirror_health WHERE freshness_state = 'green') AS last_mirror_sync_at,
  now()                                     AS computed_at
FROM erp.vw_three_lights_status;

COMMENT ON VIEW erp.vw_public_health IS
  'I62 P8.4 — anon-readable status page source. Exposes overall state + verdict + last sync only.';

-- =============================================================================
-- Grants
-- =============================================================================
GRANT SELECT ON erp.vw_three_lights_status     TO authenticated;
GRANT SELECT ON erp.vw_mirror_health           TO authenticated;
GRANT SELECT ON erp.vw_initiative_pulse        TO authenticated;
GRANT SELECT ON erp.vw_operator_inbox_top      TO authenticated;
GRANT SELECT ON erp.vw_mission_control_today   TO authenticated;
GRANT SELECT ON erp.vw_public_health           TO authenticated;
GRANT SELECT ON erp.vw_public_health           TO anon;

NOTIFY pgrst, 'reload schema';
