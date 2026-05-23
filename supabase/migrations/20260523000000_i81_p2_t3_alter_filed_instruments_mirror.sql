-- Initiative 81 P2 Tranche T3 — rename mirror table to drop FOUNDER_ prefix
-- (D-IH-81-S under D-IH-81-G umbrella, 2026-05-23).
--
-- The companion CSV moved + renamed in the same atomic commit:
--   canonicals/FOUNDER_FILED_INSTRUMENTS.csv → canonicals/advops/FILED_INSTRUMENTS.csv.
-- Pydantic chassis renamed:
--   akos/hlk_founder_filed_instruments_csv.py → akos/hlk_filed_instruments_csv.py
--   (with deprecation shim retained one initiative cycle).
-- Validator script renamed:
--   scripts/validate_founder_filed_instruments.py → scripts/validate_filed_instruments.py
--   (with deprecation shim retained one initiative cycle).
--
-- This migration is REVERSIBLE: the inverse migration would rename the
-- table back to founder_filed_instruments_mirror. Indexes + RLS policies
-- carry through the rename automatically per PostgreSQL DDL semantics.

-- Parity: staged at scripts/sql/i81_p2_t3_staging/ (none — direct forward migration per operator ratification 2026-05-23).
-- Operator gate: t3-shape Option A + t3-supabase-strategy Option 1 (full rename cascade with ALTER TABLE forward migration).

DO $$
BEGIN
  IF EXISTS (
    SELECT 1 FROM pg_class c
    JOIN pg_namespace n ON n.oid = c.relnamespace
    WHERE n.nspname = 'compliance'
      AND c.relname = 'founder_filed_instruments_mirror'
  ) THEN
    ALTER TABLE compliance.founder_filed_instruments_mirror
      RENAME TO filed_instruments_mirror;
  END IF;
END$$;

-- Rename indexes explicitly to keep their identifiers aligned with the new
-- table name. PostgreSQL does NOT auto-rename indexes on ALTER TABLE RENAME;
-- the underlying objects continue to exist but with the old name.
DO $$
BEGIN
  IF EXISTS (SELECT 1 FROM pg_indexes WHERE schemaname = 'compliance' AND indexname = 'founder_filed_instruments_mirror_synced_at_idx') THEN
    ALTER INDEX compliance.founder_filed_instruments_mirror_synced_at_idx
      RENAME TO filed_instruments_mirror_synced_at_idx;
  END IF;
  IF EXISTS (SELECT 1 FROM pg_indexes WHERE schemaname = 'compliance' AND indexname = 'founder_filed_instruments_mirror_discipline_idx') THEN
    ALTER INDEX compliance.founder_filed_instruments_mirror_discipline_idx
      RENAME TO filed_instruments_mirror_discipline_idx;
  END IF;
  IF EXISTS (SELECT 1 FROM pg_indexes WHERE schemaname = 'compliance' AND indexname = 'founder_filed_instruments_mirror_program_idx') THEN
    ALTER INDEX compliance.founder_filed_instruments_mirror_program_idx
      RENAME TO filed_instruments_mirror_program_idx;
  END IF;
  IF EXISTS (SELECT 1 FROM pg_indexes WHERE schemaname = 'compliance' AND indexname = 'founder_filed_instruments_mirror_status_idx') THEN
    ALTER INDEX compliance.founder_filed_instruments_mirror_status_idx
      RENAME TO filed_instruments_mirror_status_idx;
  END IF;
END$$;

-- RLS policies carry through the table rename automatically, but their
-- identifiers retain the old name. Recreate with aligned identifiers.
DROP POLICY IF EXISTS founder_filed_instruments_mirror_deny_authenticated ON compliance.filed_instruments_mirror;
DROP POLICY IF EXISTS founder_filed_instruments_mirror_deny_anon ON compliance.filed_instruments_mirror;
CREATE POLICY filed_instruments_mirror_deny_authenticated
  ON compliance.filed_instruments_mirror FOR ALL TO authenticated USING (false);
CREATE POLICY filed_instruments_mirror_deny_anon
  ON compliance.filed_instruments_mirror FOR ALL TO anon USING (false);

REVOKE ALL ON TABLE compliance.filed_instruments_mirror FROM PUBLIC;
GRANT ALL ON TABLE compliance.filed_instruments_mirror TO service_role;
