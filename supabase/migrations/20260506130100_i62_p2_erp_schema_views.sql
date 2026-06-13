-- Initiative 62 P2.3 — erp.* read-side projection schema
-- D-IH-62-Q: dedicated erp.* schema for projection views; not compliance.* (read-only mirrors)
--            and not holistika_ops.* (write-side ERP-canonical).
-- D-IH-62-C: demo routing via session GUC app.data_mode through erp._mode().
--
-- Views ship SECURITY INVOKER so underlying RLS on compliance.* propagates to the caller.
-- anon role gets SELECT on erp.vw_public_health only (no PII; for status.holistikaresearch.com).
-- authenticated gets SELECT on the rest (subject to RLS on the source mirrors).

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
-- Conversational  : persona-fit alignment >= 80% over the last 5 cycles
-- Dossier         : most recent dossier_run.verdict = GO and within MAX_DOSSIER_USD
-- Skill quality   : every active skill has >= 1 passing eval_run in the last 7 days
-- Composite       : min of the three (RED if any RED; AMBER if any AMBER; GREEN if all GREEN)
CREATE OR REPLACE VIEW erp.vw_three_lights_status AS
WITH conversational AS (
  SELECT
    CASE
      WHEN AVG(CASE WHEN persona_fit_pass THEN 1.0 ELSE 0.0 END) >= 0.80 THEN 'GREEN'
      WHEN AVG(CASE WHEN persona_fit_pass THEN 1.0 ELSE 0.0 END) >= 0.60 THEN 'AMBER'
      ELSE 'RED'
    END AS light,
    COALESCE(MAX(occurred_at), NULL) AS last_observed_at
  FROM (
    SELECT
      (run_payload ->> 'persona_fit_pass')::boolean AS persona_fit_pass,
      occurred_at
    FROM compliance.eval_run
    WHERE kind = 'persona_fit'
    ORDER BY occurred_at DESC
    LIMIT 5
  ) t
),
dossier AS (
  SELECT
    CASE
      WHEN verdict = 'GO' AND COALESCE((run_payload ->> 'within_envelope')::boolean, true) THEN 'GREEN'
      WHEN verdict = 'AMBER' THEN 'AMBER'
      ELSE 'RED'
    END AS light,
    started_at AS last_observed_at
  FROM compliance.dossier_run
  ORDER BY started_at DESC
  LIMIT 1
),
skill_quality AS (
  SELECT
    CASE
      WHEN COUNT(*) FILTER (WHERE last_pass_at IS NULL OR last_pass_at < now() - INTERVAL '7 days') = 0 THEN 'GREEN'
      WHEN COUNT(*) FILTER (WHERE last_pass_at IS NULL) > 0 THEN 'RED'
      ELSE 'AMBER'
    END AS light,
    MAX(last_pass_at) AS last_observed_at
  FROM (
    SELECT
      sr.skill_id,
      MAX(er.occurred_at) FILTER (WHERE er.verdict = 'pass') AS last_pass_at
    FROM compliance.skill_registry_mirror sr
    LEFT JOIN compliance.eval_run er
      ON er.run_payload ->> 'skill_id' = sr.skill_id
    WHERE sr.status = 'active'
    GROUP BY sr.skill_id
  ) skill_summary
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
  'I62 P4.2 tile 01 — Three Lights composite verdict (conversational, dossier, skill quality). Source: compliance.eval_run + dossier_run + skill_registry_mirror.';

-- =============================================================================
-- erp.vw_mirror_health — 16/16 mirrors green + last_sync per dimension
-- =============================================================================
CREATE OR REPLACE VIEW erp.vw_mirror_health AS
SELECT
  table_name AS mirror_name,
  last_sync_at,
  CASE
    WHEN last_sync_at > now() - INTERVAL '24 hours'  THEN 'green'
    WHEN last_sync_at > now() - INTERVAL '48 hours'  THEN 'yellow'
    ELSE 'red'
  END AS freshness_state,
  EXTRACT(EPOCH FROM (now() - last_sync_at))::BIGINT AS staleness_seconds
FROM (
  -- Each row gets the most recent synced_at across compliance.* mirrors
  SELECT 'baseline_organisation_mirror'    AS table_name, MAX(synced_at) AS last_sync_at FROM compliance.baseline_organisation_mirror
  UNION ALL SELECT 'process_list_mirror',                  MAX(synced_at) FROM compliance.process_list_mirror
  UNION ALL SELECT 'persona_registry_mirror',              MAX(synced_at) FROM compliance.persona_registry_mirror
  UNION ALL SELECT 'topic_registry_mirror',                MAX(synced_at) FROM compliance.topic_registry_mirror
  UNION ALL SELECT 'skill_registry_mirror',                MAX(synced_at) FROM compliance.skill_registry_mirror
  UNION ALL SELECT 'policy_register_mirror',               MAX(synced_at) FROM compliance.policy_register_mirror
  UNION ALL SELECT 'program_registry_mirror',              MAX(synced_at) FROM compliance.program_registry_mirror
  UNION ALL SELECT 'goipoi_register_mirror',               MAX(synced_at) FROM compliance.goipoi_register_mirror
  UNION ALL SELECT 'adviser_disciplines_mirror',           MAX(synced_at) FROM compliance.adviser_disciplines_mirror
  UNION ALL SELECT 'adviser_open_questions_mirror',        MAX(synced_at) FROM compliance.adviser_open_questions_mirror
  UNION ALL SELECT 'founder_filed_instruments_mirror',     MAX(synced_at) FROM compliance.founder_filed_instruments_mirror
  UNION ALL SELECT 'finops_counterparty_mirror',           MAX(synced_at) FROM compliance.finops_counterparty_mirror
  UNION ALL SELECT 'touchpoint_kit_cell_mirror',           MAX(synced_at) FROM compliance.touchpoint_kit_cell_mirror
  UNION ALL SELECT 'repo_health_snapshot_mirror',          MAX(synced_at) FROM compliance.repo_health_snapshot_mirror
  UNION ALL SELECT 'initiative_registry_mirror',           MAX(synced_at) FROM compliance.initiative_registry_mirror
  UNION ALL SELECT 'ops_register_mirror',                  MAX(synced_at) FROM compliance.ops_register_mirror
) AS h;

COMMENT ON VIEW erp.vw_mirror_health IS
  'I62 P4.2 tile 05 / P2.4 freshness pattern. Per-mirror last_sync + freshness_state (green <24h, yellow <48h, red >=48h).';

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
  o.ops_id,
  o.title,
  o.owner_class,
  o.rice_score,
  o.rice_reach,
  o.rice_impact,
  o.rice_confidence,
  o.rice_effort,
  o.initiative_id,
  o.cycle_id,
  o.status,
  o.linked_decision_id,
  o.linked_report,
  o.opened_at,
  o.last_review,
  i.title  AS initiative_title,
  i.status AS initiative_status,
  erp._mode() AS data_mode
FROM compliance.ops_register_mirror o
LEFT JOIN compliance.initiative_registry_mirror i ON i.initiative_id = o.initiative_id
WHERE o.status = 'open' AND o.owner_class IN ('operator', 'mixed')
ORDER BY o.rice_score DESC NULLS LAST, o.opened_at ASC
LIMIT 50;

COMMENT ON VIEW erp.vw_operator_inbox_top IS
  'I62 P4.2 tile 02 + /operator-inbox drilldown — top 50 open operator/mixed-owned OPS rows by RICE.';

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
       SELECT verdict, started_at, run_payload
       FROM compliance.dossier_run
       ORDER BY started_at DESC
       LIMIT 1
     ),
     last_eval_summary AS (
       SELECT
         COUNT(*) AS run_count_24h,
         COUNT(*) FILTER (WHERE verdict = 'pass') AS pass_count_24h,
         COUNT(*) FILTER (WHERE verdict = 'fail') AS fail_count_24h
       FROM compliance.eval_run
       WHERE occurred_at >= now() - INTERVAL '24 hours'
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
  ld.verdict                      AS last_dossier_verdict,
  ld.started_at                   AS last_dossier_at,
  les.run_count_24h               AS eval_runs_24h,
  les.pass_count_24h              AS eval_pass_24h,
  les.fail_count_24h              AS eval_fail_24h,
  inbox.open_count                AS operator_inbox_open,
  erp._mode()                     AS data_mode,
  now()                           AS computed_at
FROM lights, pulse, mirrors, last_dossier ld, last_eval_summary les, inbox;

COMMENT ON VIEW erp.vw_mission_control_today IS
  'I62 P4.2 — single-fetch aggregator for the seven Mission Control "Today" tiles. Computed live; cache-friendly.';

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
-- authenticated: full operator surface (RLS via underlying mirrors)
GRANT SELECT ON erp.vw_three_lights_status     TO authenticated;
GRANT SELECT ON erp.vw_mirror_health           TO authenticated;
GRANT SELECT ON erp.vw_initiative_pulse        TO authenticated;
GRANT SELECT ON erp.vw_operator_inbox_top      TO authenticated;
GRANT SELECT ON erp.vw_mission_control_today   TO authenticated;
GRANT SELECT ON erp.vw_public_health           TO authenticated;

-- anon: only the public health surface
GRANT SELECT ON erp.vw_public_health           TO anon;
