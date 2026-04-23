-- Parity: scripts/sql/i14_phase3_staging/20260419_holistika_ops_lead_intake_captcha_columns_up.sql
-- Initiative 14 — holistika_ops.lead_intake — CAPTCHA audit columns (Phase B / MAROPS)

ALTER TABLE holistika_ops.lead_intake
  ADD COLUMN IF NOT EXISTS captcha_provider TEXT,
  ADD COLUMN IF NOT EXISTS captcha_verified_at TIMESTAMPTZ;

COMMENT ON COLUMN holistika_ops.lead_intake.captcha_provider IS
  'Server-set only after successful Turnstile siteverify; e.g. turnstile. Never accept from client JSON.';
COMMENT ON COLUMN holistika_ops.lead_intake.captcha_verified_at IS
  'Server clock (UTC) immediately after successful siteverify; NULL if CAPTCHA not used or pre-migration rows.';

CREATE INDEX IF NOT EXISTS lead_intake_captcha_verified_at_idx
  ON holistika_ops.lead_intake (captcha_verified_at DESC)
  WHERE captcha_verified_at IS NOT NULL;
