-- Initiative 24 P2 - Voice profile columns rollback (STAGING)

ALTER TABLE compliance.goipoi_register_mirror
  DROP COLUMN IF EXISTS pronoun_register,
  DROP COLUMN IF EXISTS language_preference,
  DROP COLUMN IF EXISTS voice_register;
