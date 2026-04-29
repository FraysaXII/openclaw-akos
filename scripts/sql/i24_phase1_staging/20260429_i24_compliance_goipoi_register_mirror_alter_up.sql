-- Initiative 24 P2 (D-IH-11) - Voice profile columns on goipoi_register_mirror (STAGING)
-- Parity: supabase/migrations/<ts>_i24_compliance_goipoi_register_mirror_alter.sql
-- CSV SSOT: docs/references/hlk/compliance/GOI_POI_REGISTER.csv

ALTER TABLE compliance.goipoi_register_mirror
  ADD COLUMN IF NOT EXISTS voice_register      TEXT,
  ADD COLUMN IF NOT EXISTS language_preference TEXT,
  ADD COLUMN IF NOT EXISTS pronoun_register    TEXT;
