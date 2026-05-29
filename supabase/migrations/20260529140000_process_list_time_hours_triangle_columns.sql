-- SUEZ engagement estimation triangle (2026-05-10) — process_list.csv columns never mirrored to DDL.
-- akos/hlk_process_csv.py PROCESS_LIST_FIELDNAMES includes time_hours_min + time_hours_max after
-- time_hours_par; prod-resync DML failed 2026-05-29 with:
--   column "time_hours_min" of relation "process_list_mirror" does not exist
--
-- Cross-references:
--   docs/wip/intelligence/2026-05-10-suez-webuy-procure-to-pay/checkpoints/p3b-csv-extensions-2026-05-10.md
--   docs/references/hlk/v3.0/Admin/O5-1/Operations/Engagement/canonicals/SOP-ENG_ESTIMATION_DISCIPLINE_001.md
--   compliance.process_list_mirror (time_hours_par is TEXT per I14 baseline; keep triangle cols TEXT)

ALTER TABLE compliance.process_list_mirror
  ADD COLUMN IF NOT EXISTS time_hours_min TEXT,
  ADD COLUMN IF NOT EXISTS time_hours_max TEXT;

COMMENT ON COLUMN compliance.process_list_mirror.time_hours_min IS
  'Engagement estimation triangle lower bound (hours); sparse population per SOP-ENG_ESTIMATION_DISCIPLINE_001.';
COMMENT ON COLUMN compliance.process_list_mirror.time_hours_max IS
  'Engagement estimation triangle upper bound (hours); sparse population per SOP-ENG_ESTIMATION_DISCIPLINE_001.';
