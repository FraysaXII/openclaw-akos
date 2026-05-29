-- I68 Track G / bless-pattern CI posture columns for repo_health_snapshot (CHANGELOG 2026-05).
-- REPO_HEALTH_SNAPSHOT.csv + akos/hlk_repo_health_csv.py gained 6 columns when external-repo
-- CI posture checks landed; mirror DDL was never extended. Prod-resync DML failed 2026-05-29:
--   column "ci_workflow_present" of relation "repo_health_snapshot_mirror" does not exist.
--
-- Cross-references:
--   docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/REPO_HEALTH_SNAPSHOT.csv
--   akos/hlk_repo_health_csv.py REPO_HEALTH_SNAPSHOT_FIELDNAMES
--   supabase/migrations/20260430233400_i32_repo_health_snapshot_mirror.sql (original table)

ALTER TABLE compliance.repo_health_snapshot_mirror
  ADD COLUMN IF NOT EXISTS ci_workflow_present BOOLEAN,
  ADD COLUMN IF NOT EXISTS dependabot_present BOOLEAN,
  ADD COLUMN IF NOT EXISTS codeowners_present BOOLEAN,
  ADD COLUMN IF NOT EXISTS license_present BOOLEAN,
  ADD COLUMN IF NOT EXISTS akos_mirror_sha256_match BOOLEAN,
  ADD COLUMN IF NOT EXISTS secret_rotation_oldest_age_days INT;

COMMENT ON COLUMN compliance.repo_health_snapshot_mirror.ci_workflow_present IS
  'Bless-pattern CI posture — .github/workflows/ci.yml present at snapshot time.';
COMMENT ON COLUMN compliance.repo_health_snapshot_mirror.dependabot_present IS
  'Bless-pattern CI posture — .github/dependabot.yml present at snapshot time.';
COMMENT ON COLUMN compliance.repo_health_snapshot_mirror.codeowners_present IS
  'Bless-pattern CI posture — .github/CODEOWNERS present at snapshot time.';
COMMENT ON COLUMN compliance.repo_health_snapshot_mirror.license_present IS
  'Bless-pattern CI posture — LICENSE file present at repo root at snapshot time.';
COMMENT ON COLUMN compliance.repo_health_snapshot_mirror.akos_mirror_sha256_match IS
  'Bless-pattern drift — akos-mirror.mdc sha256 matches AKOS template; NULL when N/A.';
COMMENT ON COLUMN compliance.repo_health_snapshot_mirror.secret_rotation_oldest_age_days IS
  'Oldest secret rotation age in days at snapshot time; -1 when unknown; NULL when not scanned.';
