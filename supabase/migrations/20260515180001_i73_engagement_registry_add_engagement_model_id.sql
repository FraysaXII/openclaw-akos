-- Initiative 73 P1 — compliance.engagement_registry_mirror: add engagement_model_id FK column
-- Sibling D-IH-73-N ratification: the existing 16-column ENGAGEMENT_REGISTRY.csv is extended
-- with a 17th column `engagement_model_id` that FKs into compliance.engagement_model_registry_mirror
-- (created at 20260515180000_i73_compliance_engagement_model_mirror.sql).
--
-- Backwards compatibility: existing 6 ENGAGEMENT_REGISTRY rows have NO engagement_model_id today
-- (they predate the I73 taxonomy). The new column is NULLABLE so existing rows remain valid
-- without backfill; the FK constraint validates only non-NULL values. Backfill is deferred to
-- P9 UAT per D-IH-73-B charter-satisfies-gate posture.

ALTER TABLE compliance.engagement_registry_mirror
  ADD COLUMN IF NOT EXISTS engagement_model_id TEXT NULL;

COMMENT ON COLUMN compliance.engagement_registry_mirror.engagement_model_id IS
  'I73 P1 (D-IH-73-N): FK to compliance.engagement_model_registry_mirror.engagement_model_id. NULL for engagements that predate the I73 7-class taxonomy; backfilled at P9 UAT per D-IH-73-B charter-satisfies-gate.';

-- FK constraint with NOT VALID so existing NULL-bearing rows don't block the migration.
-- New rows / backfilled rows MUST satisfy the FK; the operator runs VALIDATE CONSTRAINT
-- after P9 backfill closes (forward-charter for I73-followup).
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1
    FROM pg_constraint
    WHERE conname = 'engagement_registry_mirror_engagement_model_id_fk'
      AND conrelid = 'compliance.engagement_registry_mirror'::regclass
  ) THEN
    ALTER TABLE compliance.engagement_registry_mirror
      ADD CONSTRAINT engagement_registry_mirror_engagement_model_id_fk
      FOREIGN KEY (engagement_model_id)
      REFERENCES compliance.engagement_model_registry_mirror (engagement_model_id)
      ON UPDATE CASCADE
      ON DELETE RESTRICT
      NOT VALID;
  END IF;
END$$;

CREATE INDEX IF NOT EXISTS engagement_registry_mirror_engagement_model_id_idx
  ON compliance.engagement_registry_mirror (engagement_model_id);
