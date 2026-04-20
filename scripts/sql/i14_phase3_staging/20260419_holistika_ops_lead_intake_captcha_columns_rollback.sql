-- Rollback: captcha columns on holistika_ops.lead_intake (destructive to new columns only)

DROP INDEX IF EXISTS holistika_ops.lead_intake_captcha_verified_at_idx;

ALTER TABLE holistika_ops.lead_intake
  DROP COLUMN IF EXISTS captcha_verified_at,
  DROP COLUMN IF EXISTS captcha_provider;