-- I95 D-IH-95-H: retire legacy topic_class from the topic_registry mirror (superseded by the
-- subject_kind orthogonal facet). Applied to remote MasterData (swrmqpelgoblaquequzb) via MCP 2026-06-07.
-- Matches TOPIC_REGISTRY_FIELDNAMES (topic_class removed); the dynamic emitter no longer emits it.
ALTER TABLE compliance.topic_registry_mirror DROP COLUMN IF EXISTS topic_class;
