-- Initiative 48 P7 — append-only dossier run history for trend / sparklines
--
-- Each invocation of scripts/render_uat_dossier.py may INSERT one row (best-effort
-- via service_role when SUPABASE_* env vars are set). Section 11 reads last N rows
-- for inline SVG sparklines (eval pass rate, calibration health, drift total, cost).

CREATE TABLE IF NOT EXISTS compliance.dossier_run (
  id BIGSERIAL PRIMARY KEY,
  run_id TEXT NOT NULL,
  started_at TIMESTAMPTZ NOT NULL,
  mode TEXT NOT NULL,
  git_sha TEXT NOT NULL DEFAULT 'unknown',
  section_metrics JSONB NOT NULL DEFAULT '{}'::jsonb,
  manifest_sha256 TEXT NOT NULL,
  emitted_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

COMMENT ON TABLE compliance.dossier_run IS
  'Initiative 48 P7: one row per dossier render; section_metrics mirrors manifest.section_metrics; queried for Section 11 sparklines.';

CREATE INDEX IF NOT EXISTS dossier_run_mode_started_idx
  ON compliance.dossier_run (mode, started_at DESC);

ALTER TABLE compliance.dossier_run ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS dossier_run_deny_authenticated ON compliance.dossier_run;
DROP POLICY IF EXISTS dossier_run_deny_anon ON compliance.dossier_run;
CREATE POLICY dossier_run_deny_authenticated
  ON compliance.dossier_run FOR ALL TO authenticated USING (false);
CREATE POLICY dossier_run_deny_anon
  ON compliance.dossier_run FOR ALL TO anon USING (false);
REVOKE ALL ON TABLE compliance.dossier_run FROM PUBLIC;
GRANT ALL ON TABLE compliance.dossier_run TO service_role;
