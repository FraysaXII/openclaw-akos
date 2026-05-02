-- Initiative 47 P10 — extend compliance.eval_run with persona/difficulty/judge columns
--
-- D-IH-47-F: persona_id + difficulty_class + scenario_class + judge_scores
-- on ScoreRow are mirrored to compliance.eval_run for cross-time analytics
-- across runs (same governance pattern as I45 P4).
--
-- D-IH-47-J: judge_scores JSONB stores the LLM-judge 3-axis dict
-- (brand_voice / citation / persona_fit) per scenario row.

-- Defensive: extension table may not yet exist on environments that haven't
-- pushed I45 P4. The IF NOT EXISTS prevents that from breaking.
CREATE TABLE IF NOT EXISTS compliance.eval_run (
  id BIGSERIAL PRIMARY KEY,
  run_id TEXT NOT NULL,
  emitted_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  schema_version TEXT NOT NULL DEFAULT '1.0',
  mode TEXT NOT NULL,
  skill_id TEXT NOT NULL,
  status TEXT NOT NULL,
  current_pct DOUBLE PRECISION,
  baseline_pct DOUBLE PRECISION,
  delta_pp DOUBLE PRECISION,
  cost_usd DOUBLE PRECISION,
  latency_ms_p50 DOUBLE PRECISION,
  latency_ms_p95 DOUBLE PRECISION,
  failures TEXT,
  notes TEXT,
  source_git_sha TEXT NOT NULL DEFAULT 'unknown'
);

ALTER TABLE compliance.eval_run
  ADD COLUMN IF NOT EXISTS persona_id TEXT,
  ADD COLUMN IF NOT EXISTS difficulty_class TEXT,
  ADD COLUMN IF NOT EXISTS scenario_class TEXT,
  ADD COLUMN IF NOT EXISTS judge_scores JSONB;

COMMENT ON COLUMN compliance.eval_run.persona_id IS
  'Initiative 47 P10 (D-IH-47-F): FK PERSONA_REGISTRY (or OPERATOR pseudo); NULL for non-persona rows.';
COMMENT ON COLUMN compliance.eval_run.difficulty_class IS
  'Initiative 47 P10 (D-IH-47-C): trivial|moderate|hard|impossible.';
COMMENT ON COLUMN compliance.eval_run.scenario_class IS
  'Initiative 47 P10: lookup|multihop|adversarial|recovery|benchmark|cross_axis|cannot_answer.';
COMMENT ON COLUMN compliance.eval_run.judge_scores IS
  'Initiative 47 P12 (D-IH-47-J): LLM-judge 3-axis JSON: {brand_voice: 1-5, citation: 1-5, persona_fit: 1-5}.';

CREATE INDEX IF NOT EXISTS eval_run_persona_id_idx
  ON compliance.eval_run (persona_id) WHERE persona_id IS NOT NULL;
CREATE INDEX IF NOT EXISTS eval_run_difficulty_class_idx
  ON compliance.eval_run (difficulty_class) WHERE difficulty_class IS NOT NULL;
CREATE INDEX IF NOT EXISTS eval_run_scenario_class_idx
  ON compliance.eval_run (scenario_class) WHERE scenario_class IS NOT NULL;
CREATE INDEX IF NOT EXISTS eval_run_persona_difficulty_idx
  ON compliance.eval_run (persona_id, difficulty_class)
  WHERE persona_id IS NOT NULL AND difficulty_class IS NOT NULL;

-- Re-assert RLS posture (idempotent; same as I45 P4 base table).
ALTER TABLE compliance.eval_run ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS eval_run_deny_authenticated ON compliance.eval_run;
DROP POLICY IF EXISTS eval_run_deny_anon ON compliance.eval_run;
CREATE POLICY eval_run_deny_authenticated
  ON compliance.eval_run FOR ALL TO authenticated USING (false);
CREATE POLICY eval_run_deny_anon
  ON compliance.eval_run FOR ALL TO anon USING (false);
REVOKE ALL ON TABLE compliance.eval_run FROM PUBLIC;
GRANT ALL ON TABLE compliance.eval_run TO service_role;
