-- I95 D-IH-95-I: capability-registry collapse schema on the mirror. Applied to remote MasterData
-- (swrmqpelgoblaquequzb) via MCP 2026-06-08. De-densified capabilities are bearer-agnostic, so
-- bearer_class is dropped; l1_domain (the ~9-domain grouping) + definition are added. Matches
-- CAPABILITY_REGISTRY_FIELDNAMES; the dynamic emitter projects the new columns.
ALTER TABLE compliance.capability_registry_mirror DROP COLUMN IF EXISTS bearer_class;
ALTER TABLE compliance.capability_registry_mirror ADD COLUMN IF NOT EXISTS l1_domain TEXT;
ALTER TABLE compliance.capability_registry_mirror ADD COLUMN IF NOT EXISTS definition TEXT;
