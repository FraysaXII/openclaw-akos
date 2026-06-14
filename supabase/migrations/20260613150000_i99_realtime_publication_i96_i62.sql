-- I99 P5 follow-up (D-IH-99-J) — Realtime publication for I96 freshness strip + I62 notifications drawer
-- Registry: SUPA-RT-17, SUPA-RT-02, SUPA-RT-03
-- Operator SQL gate: apply via supabase db push / holistika operator-sql-gate (not auto-applied by this commit alone)

-- Option A: public security-invoker view for ERP Realtime client (matches I62 notifications pattern)
CREATE OR REPLACE VIEW public.intelligenceops_register_mirror
  WITH (security_invoker = true) AS
SELECT *
FROM compliance.intelligenceops_register_mirror;

COMMENT ON VIEW public.intelligenceops_register_mirror IS
  'I96 Research Center Realtime + BFF read surface; SSOT table compliance.intelligenceops_register_mirror';

GRANT SELECT ON public.intelligenceops_register_mirror TO authenticated, service_role;

-- Publication membership (idempotent)
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_publication_tables
    WHERE pubname = 'supabase_realtime'
      AND schemaname = 'compliance'
      AND tablename = 'intelligenceops_register_mirror'
  ) THEN
    ALTER PUBLICATION supabase_realtime ADD TABLE compliance.intelligenceops_register_mirror;
  END IF;

  IF NOT EXISTS (
    SELECT 1 FROM pg_publication_tables
    WHERE pubname = 'supabase_realtime'
      AND schemaname = 'holistika_ops'
      AND tablename = 'notifications'
  ) THEN
    ALTER PUBLICATION supabase_realtime ADD TABLE holistika_ops.notifications;
  END IF;
END $$;

ALTER TABLE compliance.intelligenceops_register_mirror REPLICA IDENTITY FULL;
ALTER TABLE holistika_ops.notifications REPLICA IDENTITY FULL;
