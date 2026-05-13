-- Parity: scripts/sql/i70/20260513_p82_baseline_sub_area_status_up.sql (none — direct apply per I70 P8.2 atomic discipline)
-- I70 P8 §8.14 (P8.2) — extend baseline_organisation_mirror with sub_area + status columns
--
-- Rationale (D-IH-70-Z, operator ratification 2026-05-13):
--   When P8.2 surfaced a schema/intent gap between the I70 plan (which assumed
--   sub_area + status columns existed) and the live canonical schema (which
--   only had area + role_hourly_*_eur), operator chose Option C: extend the
--   schema rather than backfit the plan to legacy structure. This is the v3.1
--   methodology versioning rework — earlier intent for sub-area + soft-state
--   tracking was never crystallised into columns; this migration crystallises
--   it as part of the Marketing M3 redesign landing.
--
--   sub_area: hierarchical encoding within an area (e.g. Marketing/Reach,
--             People/Compliance, Operations/SMO). NULL/empty allowed for
--             rows where an area has no sub-division.
--
--   status:   soft-state enum-ish. Allowed values via CHECK constraint:
--             active, deprecated, pending. Default 'active'. Enables future
--             soft-deprecations without hard-removing rows mid-design-cycle.
--
-- Pattern follows 20260511030000_release_gate_hygiene_baseline_rates.sql:
-- nullable TEXT columns with backwards-compatible IF NOT EXISTS guards.

ALTER TABLE compliance.baseline_organisation_mirror
  ADD COLUMN IF NOT EXISTS sub_area TEXT,
  ADD COLUMN IF NOT EXISTS status TEXT;

-- CHECK constraint on status (allow only the documented enum values; NULL or
-- empty stays permitted for rows that pre-date the v3.1 default).
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_constraint
    WHERE conname = 'baseline_organisation_mirror_status_check'
  ) THEN
    ALTER TABLE compliance.baseline_organisation_mirror
      ADD CONSTRAINT baseline_organisation_mirror_status_check
      CHECK (status IS NULL OR status = '' OR status IN ('active', 'deprecated', 'pending'));
  END IF;
END $$;

-- Helpful covering index for "all active roles in an area" queries that the
-- governance.baseline_organisation_view downstream consumers (ERP People
-- panels, role-owner audit reports) will hit frequently once sub_area is
-- populated for the M3 redesign roles.
CREATE INDEX IF NOT EXISTS baseline_organisation_mirror_area_sub_area_status_idx
  ON compliance.baseline_organisation_mirror (area, sub_area, status);
