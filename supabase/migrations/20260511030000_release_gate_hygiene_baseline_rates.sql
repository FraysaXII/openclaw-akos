-- Parity: scripts/sql/release_gate_hygiene/20260511_release_gate_hygiene_baseline_rates_up.sql (none — direct apply per release-gate hygiene closure)
-- Release-gate hygiene 2026-05-11 — close the long-running baseline_organisation
-- column drift between canonical CSV and Supabase mirror.
--
-- Root cause (RCA, recorded in CHANGELOG release-gate hygiene entry): the canonical
-- docs/references/hlk/compliance/baseline_organisation.csv carried the role rate
-- trio (role_hourly_min_eur / role_hourly_par_eur / role_hourly_max_eur) since at
-- least the I12 P12 commit 8296512, but scripts/sync_compliance_mirrors_from_csv.py
-- hardcoded a 12-column BASELINE_FIELDNAMES tuple that pre-dated those columns.
-- The drift caused tests/test_sync_compliance_mirrors_from_csv.py to silently fail
-- and the mirror's SQL DDL never grew the columns. This migration adds them now.
--
-- Pattern follows P13.4 alter (related_party on goipoi_register_mirror) and the
-- earlier voice/distance alter patterns: nullable TEXT columns, no CHECK constraint
-- (numeric range policing remains an operator concern), backwards-compatible for
-- every existing row in the mirror.

ALTER TABLE compliance.baseline_organisation_mirror
  ADD COLUMN IF NOT EXISTS role_hourly_min_eur TEXT,
  ADD COLUMN IF NOT EXISTS role_hourly_par_eur TEXT,
  ADD COLUMN IF NOT EXISTS role_hourly_max_eur TEXT;
