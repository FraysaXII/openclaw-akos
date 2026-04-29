-- Initiative 23 P2 — compliance.program_registry_mirror rollback (STAGING)

DROP POLICY IF EXISTS program_registry_mirror_deny_authenticated ON compliance.program_registry_mirror;
DROP POLICY IF EXISTS program_registry_mirror_deny_anon ON compliance.program_registry_mirror;

DROP INDEX IF EXISTS compliance.program_registry_mirror_synced_at_idx;
DROP INDEX IF EXISTS compliance.program_registry_mirror_lifecycle_idx;
DROP INDEX IF EXISTS compliance.program_registry_mirror_plane_idx;
DROP INDEX IF EXISTS compliance.program_registry_mirror_code_idx;

DROP TABLE IF EXISTS compliance.program_registry_mirror;
