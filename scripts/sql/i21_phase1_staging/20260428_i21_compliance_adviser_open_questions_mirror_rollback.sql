-- Initiative 21 — compliance.adviser_open_questions_mirror rollback (STAGING)

DROP POLICY IF EXISTS adviser_open_questions_mirror_deny_authenticated ON compliance.adviser_open_questions_mirror;
DROP POLICY IF EXISTS adviser_open_questions_mirror_deny_anon ON compliance.adviser_open_questions_mirror;

DROP INDEX IF EXISTS compliance.adviser_open_questions_mirror_synced_at_idx;
DROP INDEX IF EXISTS compliance.adviser_open_questions_mirror_discipline_idx;
DROP INDEX IF EXISTS compliance.adviser_open_questions_mirror_program_idx;

DROP TABLE IF EXISTS compliance.adviser_open_questions_mirror;
