-- I63 + I86 Wave H schema catch-up for compliance.repository_registry_mirror.
-- Prod-resync failure (2026-05-29): line 1816
--   column "consumes_compliance_types" of relation "repository_registry_mirror" does not exist
--
-- Cross-references:
--   docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/REPOSITORY_REGISTRY.csv
--   akos/hlk_repository_registry_csv.py (29-column field contract)
--   scripts/sync_compliance_mirrors_from_csv.py (_emit_repository_registry_upserts)

ALTER TABLE compliance.repository_registry_mirror
  ADD COLUMN IF NOT EXISTS consumes_compliance_types TEXT,
  ADD COLUMN IF NOT EXISTS consumes_mirrors TEXT,
  ADD COLUMN IF NOT EXISTS local_path TEXT,
  ADD COLUMN IF NOT EXISTS app_class TEXT,
  ADD COLUMN IF NOT EXISTS metadata_tags TEXT,
  ADD COLUMN IF NOT EXISTS github_topics TEXT,
  ADD COLUMN IF NOT EXISTS github_visibility TEXT,
  ADD COLUMN IF NOT EXISTS primary_language TEXT,
  ADD COLUMN IF NOT EXISTS created_at DATE,
  ADD COLUMN IF NOT EXISTS pushed_at DATE,
  ADD COLUMN IF NOT EXISTS last_inventory_at DATE,
  ADD COLUMN IF NOT EXISTS governance_status TEXT,
  ADD COLUMN IF NOT EXISTS related_initiative_ids TEXT,
  ADD COLUMN IF NOT EXISTS codeowners_present BOOLEAN,
  ADD COLUMN IF NOT EXISTS branch_protection_enabled BOOLEAN;

ALTER TABLE compliance.repository_registry_mirror
  DROP CONSTRAINT IF EXISTS repository_registry_mirror_consumes_compliance_types_check;
ALTER TABLE compliance.repository_registry_mirror
  ADD CONSTRAINT repository_registry_mirror_consumes_compliance_types_check
  CHECK (
    consumes_compliance_types IS NULL
    OR consumes_compliance_types = ''
    OR consumes_compliance_types IN ('yes', 'no')
  );

ALTER TABLE compliance.repository_registry_mirror
  DROP CONSTRAINT IF EXISTS repository_registry_mirror_app_class_check;
ALTER TABLE compliance.repository_registry_mirror
  ADD CONSTRAINT repository_registry_mirror_app_class_check
  CHECK (
    app_class IS NULL
    OR app_class = ''
    OR app_class IN (
      'production',
      'research',
      'experiment',
      'template',
      'fork',
      'archive',
      'uncategorized'
    )
  );

ALTER TABLE compliance.repository_registry_mirror
  DROP CONSTRAINT IF EXISTS repository_registry_mirror_github_visibility_check;
ALTER TABLE compliance.repository_registry_mirror
  ADD CONSTRAINT repository_registry_mirror_github_visibility_check
  CHECK (
    github_visibility IS NULL
    OR github_visibility = ''
    OR github_visibility IN ('PUBLIC', 'PRIVATE', 'INTERNAL')
  );

ALTER TABLE compliance.repository_registry_mirror
  DROP CONSTRAINT IF EXISTS repository_registry_mirror_governance_status_check;
ALTER TABLE compliance.repository_registry_mirror
  ADD CONSTRAINT repository_registry_mirror_governance_status_check
  CHECK (
    governance_status IS NULL
    OR governance_status = ''
    OR governance_status IN ('governed', 'inventoried', 'unmanaged', 'archived')
  );

