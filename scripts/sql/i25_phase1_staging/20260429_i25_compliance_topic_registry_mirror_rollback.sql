-- Initiative 25 P2 - rollback (STAGING)

DROP POLICY IF EXISTS topic_registry_mirror_deny_authenticated ON compliance.topic_registry_mirror;
DROP POLICY IF EXISTS topic_registry_mirror_deny_anon ON compliance.topic_registry_mirror;

DROP INDEX IF EXISTS compliance.topic_registry_mirror_synced_at_idx;
DROP INDEX IF EXISTS compliance.topic_registry_mirror_program_idx;
DROP INDEX IF EXISTS compliance.topic_registry_mirror_plane_idx;
DROP INDEX IF EXISTS compliance.topic_registry_mirror_class_idx;

DROP TABLE IF EXISTS compliance.topic_registry_mirror;
