-- Parity: scripts/sql/i21_phase1_staging/20260428_i21_compliance_founder_filed_instruments_mirror_up.sql
-- Initiative 21 — Founder filed instruments register mirror

CREATE SCHEMA IF NOT EXISTS compliance;

CREATE TABLE IF NOT EXISTS compliance.founder_filed_instruments_mirror (
  instrument_id              TEXT NOT NULL,
  discipline_id              TEXT,
  program_id                 TEXT,
  instrument_type            TEXT,
  jurisdiction               TEXT,
  status                     TEXT,
  effective_or_filing_date   TEXT,
  storage_location           TEXT,
  vault_link                 TEXT,
  primary_owner_role         TEXT,
  counterparty_goi_ref_id    TEXT,
  supersedes_instrument_id   TEXT,
  notes                      TEXT,
  source_git_sha             TEXT NOT NULL,
  synced_at                  TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (instrument_id)
);

CREATE INDEX IF NOT EXISTS founder_filed_instruments_mirror_synced_at_idx
  ON compliance.founder_filed_instruments_mirror (synced_at DESC);
CREATE INDEX IF NOT EXISTS founder_filed_instruments_mirror_discipline_idx
  ON compliance.founder_filed_instruments_mirror (discipline_id);
CREATE INDEX IF NOT EXISTS founder_filed_instruments_mirror_program_idx
  ON compliance.founder_filed_instruments_mirror (program_id);
CREATE INDEX IF NOT EXISTS founder_filed_instruments_mirror_status_idx
  ON compliance.founder_filed_instruments_mirror (status);

ALTER TABLE compliance.founder_filed_instruments_mirror ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS founder_filed_instruments_mirror_deny_authenticated ON compliance.founder_filed_instruments_mirror;
DROP POLICY IF EXISTS founder_filed_instruments_mirror_deny_anon ON compliance.founder_filed_instruments_mirror;
CREATE POLICY founder_filed_instruments_mirror_deny_authenticated
  ON compliance.founder_filed_instruments_mirror FOR ALL TO authenticated USING (false);
CREATE POLICY founder_filed_instruments_mirror_deny_anon
  ON compliance.founder_filed_instruments_mirror FOR ALL TO anon USING (false);

REVOKE ALL ON TABLE compliance.founder_filed_instruments_mirror FROM PUBLIC;
GRANT ALL ON TABLE compliance.founder_filed_instruments_mirror TO service_role;
