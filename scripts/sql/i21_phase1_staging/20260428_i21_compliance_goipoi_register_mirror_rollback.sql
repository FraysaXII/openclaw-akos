-- Initiative 21 — compliance.goipoi_register_mirror rollback (STAGING)
-- Drop policies, indexes, table.

DROP POLICY IF EXISTS goipoi_register_mirror_deny_authenticated ON compliance.goipoi_register_mirror;
DROP POLICY IF EXISTS goipoi_register_mirror_deny_anon ON compliance.goipoi_register_mirror;

DROP INDEX IF EXISTS compliance.goipoi_register_mirror_synced_at_idx;
DROP INDEX IF EXISTS compliance.goipoi_register_mirror_program_idx;
DROP INDEX IF EXISTS compliance.goipoi_register_mirror_class_idx;

DROP TABLE IF EXISTS compliance.goipoi_register_mirror;
