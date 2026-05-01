-- Initiative 45 P4 — compliance.eval_run mirror
--
-- Symmetric to compliance.validation_runs (I32 P1) but for eval results.
-- Append-only event log: one row per scripts/eval.py invocation with the
-- aggregated scorecard. Enables historical regression queries (cost trend per
-- skill, latency p95 over time, canary-2 trip rate, adversarial pass rate).
--
-- Same governance posture as other compliance.* mirrors:
-- - Deny anon and authenticated; service_role only
-- - Append-only via INSERT grant (no UPDATE/DELETE policy)
-- - Indexes for the 3 most likely query patterns: by skill, by time, by status

CREATE SCHEMA IF NOT EXISTS compliance;

CREATE TABLE IF NOT EXISTS compliance.eval_run (
  eval_run_id              BIGSERIAL PRIMARY KEY,
  run_started_at           TIMESTAMPTZ NOT NULL DEFAULT now(),
  run_elapsed_ms           INTEGER NOT NULL DEFAULT 0,
  modes_run                TEXT[] NOT NULL DEFAULT '{}',  -- e.g., ['smoke','canary','rubric']
  overall_status           TEXT NOT NULL,                 -- 'pass' | 'fail'
  -- Per-skill aggregates from the unified Scorecard
  skill_id                 TEXT,                          -- nullable: row-level skill or NULL for run-summary
  mode                     TEXT,                          -- 'smoke' | 'canary' | 'rubric' | 'replay' | 'smoke'
  status                   TEXT,                          -- 'PASS' | 'FAIL' | 'SKIP' | 'WARN'
  baseline_pct             NUMERIC,
  current_pct              NUMERIC,
  delta_pp                 NUMERIC,
  canary_2_tripped         BOOLEAN NOT NULL DEFAULT false,
  cost_usd                 NUMERIC,
  latency_ms_p50           NUMERIC,
  latency_ms_p95           NUMERIC,
  failures                 TEXT[] NOT NULL DEFAULT '{}',
  notes                    TEXT,
  source_git_sha           TEXT NOT NULL,
  recorded_by              TEXT NOT NULL DEFAULT 'unknown',
  -- For row-level archiving of all 14 ScoreRow modes from one run
  schema_version           TEXT NOT NULL DEFAULT '1.0'
);

COMMENT ON TABLE compliance.eval_run IS
  'Initiative 45 P4 — append-only eval run history. Symmetric to compliance.validation_runs.';
COMMENT ON COLUMN compliance.eval_run.skill_id IS
  'Per-row skill_id (or NULL for run-level summary). Mirrors ScoreRow.skill_id.';
COMMENT ON COLUMN compliance.eval_run.cost_usd IS
  'I45 P4: per-skill avg cost USD per run. Compared against POLICY_REGISTER cost_ceiling rows.';

CREATE INDEX IF NOT EXISTS eval_run_started_at_idx
  ON compliance.eval_run (run_started_at DESC);
CREATE INDEX IF NOT EXISTS eval_run_skill_id_idx
  ON compliance.eval_run (skill_id) WHERE skill_id IS NOT NULL;
CREATE INDEX IF NOT EXISTS eval_run_status_idx
  ON compliance.eval_run (status);
CREATE INDEX IF NOT EXISTS eval_run_mode_idx
  ON compliance.eval_run (mode);
-- Cost regression queries hit (skill_id, run_started_at) most often
CREATE INDEX IF NOT EXISTS eval_run_skill_time_cost_idx
  ON compliance.eval_run (skill_id, run_started_at DESC) WHERE cost_usd IS NOT NULL;

ALTER TABLE compliance.eval_run ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS eval_run_deny_authenticated ON compliance.eval_run;
DROP POLICY IF EXISTS eval_run_deny_anon ON compliance.eval_run;
CREATE POLICY eval_run_deny_authenticated
  ON compliance.eval_run FOR ALL TO authenticated USING (false);
CREATE POLICY eval_run_deny_anon
  ON compliance.eval_run FOR ALL TO anon USING (false);

REVOKE ALL ON TABLE compliance.eval_run FROM PUBLIC;
GRANT SELECT, INSERT ON TABLE compliance.eval_run TO service_role;
GRANT USAGE, SELECT ON SEQUENCE compliance.eval_run_eval_run_id_seq TO service_role;
