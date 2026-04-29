-- Parity: scripts/sql/i24_phase1_staging/20260429_i24_compliance_goipoi_register_mirror_alter_up.sql
-- Initiative 24 P2 (D-IH-11) - Voice profile columns on goipoi_register_mirror

ALTER TABLE compliance.goipoi_register_mirror
  ADD COLUMN IF NOT EXISTS voice_register      TEXT,
  ADD COLUMN IF NOT EXISTS language_preference TEXT,
  ADD COLUMN IF NOT EXISTS pronoun_register    TEXT;
