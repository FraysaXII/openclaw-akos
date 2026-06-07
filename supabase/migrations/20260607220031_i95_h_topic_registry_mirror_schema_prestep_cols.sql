-- I95 D-IH-95-H L5 schema tranche: add the 5 new TOPIC_REGISTRY columns to the mirror (TEXT projection).
-- Applied to remote MasterData (swrmqpelgoblaquequzb) via MCP apply_migration on 2026-06-07.
-- Matches TOPIC_REGISTRY_FIELDNAMES; sync_compliance_mirrors_from_csv.py emits these dynamically.
ALTER TABLE compliance.topic_registry_mirror
  ADD COLUMN IF NOT EXISTS subject_kind TEXT,
  ADD COLUMN IF NOT EXISTS steward_role TEXT,
  ADD COLUMN IF NOT EXISTS working_area_path TEXT,
  ADD COLUMN IF NOT EXISTS knowledge_index_path TEXT,
  ADD COLUMN IF NOT EXISTS physical_model TEXT;
