-- Initiative 79 P6 — process_list_mirror schema migration: add inherited_pattern_id FK column
-- D-IH-79-E (charter mint of the FK lever) + D-IH-79-O (P5 cluster D ratification of the
-- as-shipped column placement at SSOT col 35; "8th col" in plan body refers to the 8th
-- new column added since the original 27-col baseline — I71 added 4, I72 added 7, I79
-- adds 1 = the 8th post-baseline addition).
-- Cross-references:
--   compliance.process_list_mirror (existing; mirrored from process_list.csv)
--   compliance.people_design_pattern_registry_mirror.pattern_id (FK target; minted I79 P2)
--   akos/hlk_process_csv.py PROCESS_LIST_FIELDNAMES (extended at this commit)
--   docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/process_list.csv (extended at this commit)
--   scripts/validate_hlk.py check_inherited_pattern_id_fk() (added at this commit)
--
-- The "process singularity" lever: when populated, makes the cross-area inheritance
-- lattice countable. SELECT COUNT(*) FROM compliance.process_list_mirror
-- WHERE inherited_pattern_id = '<X>' yields the adoption surface for any People design
-- pattern. Sparse population — existing 1166-row corpus stays NULL for all rows except
-- ~15-17 inline-ratify-seeded rows landed in the same I79 P6 commit. Future tranches grow
-- adoption organically per cross-area-breakthrough propagation SOP (I79 P4).

-- Single nullable column. No CHECK constraint at DDL level — application-level FK
-- resolution lives in scripts/validate_hlk.py check_inherited_pattern_id_fk(). Reasoning:
-- (a) Postgres cannot easily enforce a string-FK against a CSV-mirrored table without
-- introducing an actual foreign-key reference, and the pattern_id values are slug-style
-- strings authored at the People canonical layer (CSV-first authoring per the 2-plane
-- model in akos-holistika-operations.mdc); (b) compliance.people_design_pattern_registry_mirror
-- is itself a CSV mirror with its own resync cadence, and a hard FK would couple the
-- two mirrors' resync windows; (c) git-canonical CSV is the SSOT, and the validator
-- enforces FK resolution at every CI pre_commit run, which is the actual enforcement
-- surface that matters.
ALTER TABLE compliance.process_list_mirror
  ADD COLUMN IF NOT EXISTS inherited_pattern_id TEXT;

COMMENT ON COLUMN compliance.process_list_mirror.inherited_pattern_id IS
  'I79 P6 D-IH-79-E: nullable FK to compliance.people_design_pattern_registry_mirror.pattern_id; when populated, declares which People design pattern parents this process. Application-level FK resolution via scripts/validate_hlk.py check_inherited_pattern_id_fk(). Sparse population intent.';

-- Index for adoption-surface counting (the central use case: "how many processes inherit pattern X?").
CREATE INDEX IF NOT EXISTS process_list_mirror_inherited_pattern_id_idx
  ON compliance.process_list_mirror (inherited_pattern_id);
