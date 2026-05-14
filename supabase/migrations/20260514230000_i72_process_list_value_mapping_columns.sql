-- Initiative 72 P4 — process_list_mirror schema migration: add 7 value-mapping columns
-- D-IH-72-AF: value-mapping function schema (4 axis FKs + 3 revenue value cells).
-- D-IH-72-AG: multi-axis Marketing dimension ontology (sparse population per row).
-- D-IH-72-V: schema cascade (akos SSOT module + Pydantic + Supabase mirror DDL + release-gate).
--
-- Sparse population: existing 1144+ rows backwards-compatible (NULL for all 7 cells).
-- Rows authored by RevOps Lead/Analyst (post-P4 activation per D-IH-72-AC) populate the
-- relevant axis cells.
--
-- Cross-references:
--   compliance.process_list_mirror (existing; mirrored from process_list.csv)
--   akos/hlk_process_csv.py PROCESS_LIST_FIELDNAMES (extended at this commit)
--   docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/process_list.csv (extended at this commit)

-- 4 axis FK columns (nullable; sparse population intent).
ALTER TABLE compliance.process_list_mirror
  ADD COLUMN IF NOT EXISTS m3_sub_area              TEXT,    -- enum brand|reach|resonance|storytelling|experimentation per MARKETING_AREA_M3_REDESIGN.md
  ADD COLUMN IF NOT EXISTS engagement_template_id   TEXT,    -- FK to compliance.engagement_template_registry_mirror.template_id
  ADD COLUMN IF NOT EXISTS persona_id               TEXT,    -- FK to compliance.persona_registry_mirror.persona_id
  ADD COLUMN IF NOT EXISTS cadence_type             TEXT,    -- enum on_demand|scheduled|event_triggered|gated_operator per D-IH-72-Q
  -- 3 revenue value cells (NUMERIC; nullable; populated by RevOps Analyst at QBR cadence).
  ADD COLUMN IF NOT EXISTS min_rev_value_eur        NUMERIC,
  ADD COLUMN IF NOT EXISTS par_rev_value_eur        NUMERIC,
  ADD COLUMN IF NOT EXISTS max_rev_value_eur        NUMERIC;

COMMENT ON COLUMN compliance.process_list_mirror.m3_sub_area IS
  'D-IH-72-AF: Marketing M3 sub-area axis FK; nullable; enum brand|reach|resonance|storytelling|experimentation per MARKETING_AREA_M3_REDESIGN.md.';
COMMENT ON COLUMN compliance.process_list_mirror.engagement_template_id IS
  'D-IH-72-AF: Engagement template axis FK to compliance.engagement_template_registry_mirror.template_id; nullable; resolves at I72 P2.';
COMMENT ON COLUMN compliance.process_list_mirror.persona_id IS
  'D-IH-72-AF: Persona axis FK to compliance.persona_registry_mirror.persona_id; nullable; expands at I72 P5.';
COMMENT ON COLUMN compliance.process_list_mirror.cadence_type IS
  'D-IH-72-AF + D-IH-72-Q: cadence axis enum on_demand|scheduled|event_triggered|gated_operator.';
COMMENT ON COLUMN compliance.process_list_mirror.min_rev_value_eur IS
  'D-IH-72-AF: declared minimum revenue value attributable to this process under the specified axis combination; populated at QBR cadence.';
COMMENT ON COLUMN compliance.process_list_mirror.par_rev_value_eur IS
  'D-IH-72-AF: declared par/expected revenue value; populated at QBR cadence.';
COMMENT ON COLUMN compliance.process_list_mirror.max_rev_value_eur IS
  'D-IH-72-AF: declared maximum revenue value; populated at QBR cadence.';

-- Indexes for axis-slicing queries (per RevOps Analyst access pattern).
CREATE INDEX IF NOT EXISTS process_list_mirror_m3_sub_area_idx
  ON compliance.process_list_mirror (m3_sub_area);
CREATE INDEX IF NOT EXISTS process_list_mirror_engagement_template_id_idx
  ON compliance.process_list_mirror (engagement_template_id);
CREATE INDEX IF NOT EXISTS process_list_mirror_persona_id_idx
  ON compliance.process_list_mirror (persona_id);
CREATE INDEX IF NOT EXISTS process_list_mirror_cadence_type_idx
  ON compliance.process_list_mirror (cadence_type);
