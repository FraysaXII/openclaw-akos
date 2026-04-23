-- Parity: scripts/sql/i14_phase3_staging/20260418_holistika_ops_lead_intake_up.sql
-- Initiative 14 — holistika_ops.lead_intake (company marketing / CRM leads)

CREATE TABLE IF NOT EXISTS holistika_ops.lead_intake (
  id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at              TIMESTAMPTZ NOT NULL DEFAULT now(),
  form_type               TEXT NOT NULL DEFAULT 'contact',
  contact_name            TEXT NOT NULL,
  contact_email           TEXT NOT NULL,
  company_name            TEXT,
  service_interest        TEXT,
  message_body            TEXT NOT NULL,
  source                  TEXT,
  qualification_status    TEXT NOT NULL DEFAULT 'new',
  session_metadata        JSONB,
  CONSTRAINT lead_intake_form_type_chk
    CHECK (form_type IN ('contact', 'project_intake', 'other')),
  CONSTRAINT lead_intake_email_len_chk
    CHECK (char_length(contact_email) <= 320)
);

CREATE INDEX IF NOT EXISTS lead_intake_created_at_idx
  ON holistika_ops.lead_intake (created_at DESC);

COMMENT ON TABLE holistika_ops.lead_intake IS 'Holistika company inbound leads; inserts via service_role from Next API only';

ALTER TABLE holistika_ops.lead_intake ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS holistika_lead_intake_deny_authenticated ON holistika_ops.lead_intake;
DROP POLICY IF EXISTS holistika_lead_intake_deny_anon ON holistika_ops.lead_intake;

CREATE POLICY holistika_lead_intake_deny_authenticated
  ON holistika_ops.lead_intake FOR ALL TO authenticated USING (false);

CREATE POLICY holistika_lead_intake_deny_anon
  ON holistika_ops.lead_intake FOR ALL TO anon USING (false);

GRANT ALL ON TABLE holistika_ops.lead_intake TO service_role;
