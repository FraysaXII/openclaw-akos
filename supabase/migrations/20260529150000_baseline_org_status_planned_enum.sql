-- I86 Wave P (D-IH-86-CL) — extend baseline_organisation_mirror.status CHECK for `planned`.
-- 22 ghost-role rows in baseline_organisation.csv carry status=planned (CHANGELOG 2026-05-22).
-- Prod-resync DML failed 2026-05-29:
--   baseline_organisation_mirror_status_check rejects `planned` (I70 migration allowed only
--   active / deprecated / pending).
--
-- Cross-references:
--   docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/baseline_organisation.csv
--   akos/hlk_baseline_org_csv.py BASELINE_ORGANISATION_FIELDNAMES (status column)
--   supabase/migrations/20260513140000_i70_p82_baseline_sub_area_status.sql (original CHECK)

ALTER TABLE compliance.baseline_organisation_mirror
  DROP CONSTRAINT IF EXISTS baseline_organisation_mirror_status_check;

ALTER TABLE compliance.baseline_organisation_mirror
  ADD CONSTRAINT baseline_organisation_mirror_status_check
  CHECK (
    status IS NULL
    OR status = ''
    OR status IN ('active', 'deprecated', 'pending', 'planned')
  );

COMMENT ON COLUMN compliance.baseline_organisation_mirror.status IS
  'Soft-state: active | deprecated | pending | planned (D-IH-86-CL ghost-role batch). NULL/empty allowed for legacy rows.';
