-- Rollback: holistika_ops.lead_intake (destructive — drops table and policies)

DROP POLICY IF EXISTS holistika_lead_intake_deny_authenticated ON holistika_ops.lead_intake;
DROP POLICY IF EXISTS holistika_lead_intake_deny_anon ON holistika_ops.lead_intake;

DROP TABLE IF EXISTS holistika_ops.lead_intake CASCADE;
