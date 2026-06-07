-- I95 D-IH-95-H capability schema pre-step: add capability_tier to the mirror (TEXT projection).
-- Applied to remote MasterData (swrmqpelgoblaquequzb) via MCP apply_migration on 2026-06-07.
-- Matches CAPABILITY_REGISTRY_FIELDNAMES; sync_compliance_mirrors_from_csv.py emits it dynamically.
ALTER TABLE compliance.capability_registry_mirror
  ADD COLUMN IF NOT EXISTS capability_tier TEXT;
