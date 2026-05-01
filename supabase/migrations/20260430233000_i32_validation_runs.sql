-- Initiative 32 P1 — compliance.validation_runs operational mirror
-- D-IH-32-F: validator graph dispatcher emits structured per-run rows; this is
-- audit history, not git-canonical SSOT. Same governance posture as
-- finops.registered_fact (Initiative 19): server-only writes, deny anon and
-- authenticated, no FK to canonical CSVs.

CREATE SCHEMA IF NOT EXISTS compliance;
COMMENT ON SCHEMA compliance IS 'HLK git-backed projections; SSOT remains docs/references/hlk/compliance/*.csv';

CREATE TABLE IF NOT EXISTS compliance.validation_runs (
  run_id            UUID NOT NULL,
  validator_name    TEXT NOT NULL,
  started_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
  duration_ms       INT NOT NULL DEFAULT 0,
  status            TEXT NOT NULL,
  exit_code         INT NOT NULL DEFAULT 0,
  row_count         INT NOT NULL DEFAULT 0,
  error_count       INT NOT NULL DEFAULT 0,
  drift_detected    BOOLEAN NOT NULL DEFAULT false,
  git_sha           TEXT,
  host              TEXT,
  notes             TEXT,
  PRIMARY KEY (run_id, validator_name)
);

COMMENT ON TABLE compliance.validation_runs IS
  'Initiative 32 P1 — operational mirror of validator runs (audit history). NOT git SSOT.';
COMMENT ON COLUMN compliance.validation_runs.run_id IS
  'UUID v4 generated per dispatcher invocation; same run_id across all validator rows in one dispatch.';
COMMENT ON COLUMN compliance.validation_runs.status IS
  'One of: pass | fail | error | skipped.';
COMMENT ON COLUMN compliance.validation_runs.drift_detected IS
  'True when a drift incident was recorded by the validator (e.g., mirror parity break).';

CREATE INDEX IF NOT EXISTS validation_runs_started_at_idx
  ON compliance.validation_runs (started_at DESC);
CREATE INDEX IF NOT EXISTS validation_runs_validator_name_idx
  ON compliance.validation_runs (validator_name);
CREATE INDEX IF NOT EXISTS validation_runs_status_idx
  ON compliance.validation_runs (status)
  WHERE status <> 'pass';

ALTER TABLE compliance.validation_runs ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS validation_runs_deny_authenticated ON compliance.validation_runs;
DROP POLICY IF EXISTS validation_runs_deny_anon ON compliance.validation_runs;
CREATE POLICY validation_runs_deny_authenticated
  ON compliance.validation_runs FOR ALL TO authenticated USING (false);
CREATE POLICY validation_runs_deny_anon
  ON compliance.validation_runs FOR ALL TO anon USING (false);

REVOKE ALL ON TABLE compliance.validation_runs FROM PUBLIC;
GRANT ALL ON TABLE compliance.validation_runs TO service_role;
