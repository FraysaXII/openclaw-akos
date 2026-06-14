-- I94 P3 / Tier 0 mirror sync (2026-06-13) — process_list.csv paired SOP + runbook paths
-- never mirrored to DDL. Full compliance_mirror_emit DML failed until break-glass:
--   ADD COLUMN sop_path, runbook_path on compliance.process_list_mirror.
--
-- Cross-references:
--   akos/hlk_process_csv.py PROCESS_LIST_FIELDNAMES (sop_path, runbook_path)
--   scripts/sync_compliance_mirrors_from_csv.py _emit_process_list_upserts
--   docs/wip/planning/94-area-architecture-and-completeness-v2/ (AREA-09 tranche)

ALTER TABLE compliance.process_list_mirror
  ADD COLUMN IF NOT EXISTS sop_path TEXT,
  ADD COLUMN IF NOT EXISTS runbook_path TEXT;

COMMENT ON COLUMN compliance.process_list_mirror.sop_path IS
  'Paired v3.0 SOP markdown path for validate_area_completeness scorer (I94 AREA-09); sparse.';
COMMENT ON COLUMN compliance.process_list_mirror.runbook_path IS
  'Paired executable runbook path (script or runbook markdown); sparse.';
