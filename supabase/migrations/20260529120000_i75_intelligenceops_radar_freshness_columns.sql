-- I75 Wave R+5 C1 — INTELLIGENCEOPS_REGISTER radar freshness columns (D-IH-86-FH)
-- Extends compliance.intelligenceops_register_mirror to match CSV SSOT
-- akos/hlk_research_radar.INTELLIGENCEOPS_REGISTER_FIELDNAMES

ALTER TABLE compliance.intelligenceops_register_mirror
  ADD COLUMN IF NOT EXISTS volatility_class TEXT,
  ADD COLUMN IF NOT EXISTS staleness_days INTEGER,
  ADD COLUMN IF NOT EXISTS staleness_posture TEXT,
  ADD COLUMN IF NOT EXISTS next_verify_by DATE;

COMMENT ON COLUMN compliance.intelligenceops_register_mirror.volatility_class IS
  'D-IH-86-FH: per-row volatility default hint (fast|medium|slow|static); staleness_days overrides.';
COMMENT ON COLUMN compliance.intelligenceops_register_mirror.staleness_days IS
  'D-IH-86-FH: per-row integer decay window; never a global constant in code.';
COMMENT ON COLUMN compliance.intelligenceops_register_mirror.staleness_posture IS
  'D-IH-86-FH: cite_and_flag | block_govern | none when stale at Research Action govern stage.';
COMMENT ON COLUMN compliance.intelligenceops_register_mirror.next_verify_by IS
  'D-IH-86-FH: date alarm; sweep surfaces when today > next_verify_by.';

ALTER TABLE compliance.intelligenceops_register_mirror
  DROP CONSTRAINT IF EXISTS intelligenceops_register_mirror_volatility_class_check;
ALTER TABLE compliance.intelligenceops_register_mirror
  ADD CONSTRAINT intelligenceops_register_mirror_volatility_class_check
  CHECK (volatility_class IS NULL OR volatility_class IN ('fast', 'medium', 'slow', 'static'));

ALTER TABLE compliance.intelligenceops_register_mirror
  DROP CONSTRAINT IF EXISTS intelligenceops_register_mirror_staleness_posture_check;
ALTER TABLE compliance.intelligenceops_register_mirror
  ADD CONSTRAINT intelligenceops_register_mirror_staleness_posture_check
  CHECK (staleness_posture IS NULL OR staleness_posture IN ('cite_and_flag', 'block_govern', 'none'));
