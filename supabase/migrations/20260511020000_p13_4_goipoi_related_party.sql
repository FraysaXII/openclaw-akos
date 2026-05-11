-- Parity: scripts/sql/p13_phase4_staging/20260511_p13_4_goipoi_related_party_up.sql (none — direct apply per P13.4 pause record)
-- P13.4 (D-W13-D) — related-party disclosure column on compliance.goipoi_register_mirror.
--
-- Pattern follows I24 P2 alter (voice_register / language_preference / pronoun_register)
-- and I31 P2.2 alter (distance_band / bridge_via / distance_assessed_date): single new
-- nullable TEXT column with no CHECK constraint to keep enum policing in the validator.
-- Empty default (NULL in SQL; "" in CSV) is backwards-compatible for every existing row.

ALTER TABLE compliance.goipoi_register_mirror
  ADD COLUMN IF NOT EXISTS related_party TEXT;

-- Optional partial index for queries that scan related-party rows specifically
-- (e.g., audit dossiers, SOC-disclosure reports). Cheap: indexes only the small
-- minority of rows with related_party='true'.
CREATE INDEX IF NOT EXISTS goipoi_register_mirror_related_party_idx
  ON compliance.goipoi_register_mirror (related_party)
  WHERE related_party = 'true';
