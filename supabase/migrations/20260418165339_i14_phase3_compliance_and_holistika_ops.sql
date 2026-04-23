-- Parity: scripts/sql/i14_phase3_staging/20260417_i14_phase3_up.sql
-- Initiative 14 Phase 3 — compliance mirrors + holistika_ops (operator-approved)
-- Idempotent where practical. See sql-proposal-stack-20260417.md §4–§6.

CREATE SCHEMA IF NOT EXISTS compliance;
COMMENT ON SCHEMA compliance IS 'HLK git-backed projections; SSOT remains docs/references/hlk/compliance/*.csv';

CREATE TABLE IF NOT EXISTS compliance.process_list_mirror (
  type                    TEXT,
  orientation             TEXT,
  entity                  TEXT,
  area                    TEXT,
  role_parent_1           TEXT,
  role_owner              TEXT,
  item_parent_2           TEXT,
  item_parent_2_id        TEXT,
  item_parent_1           TEXT,
  item_parent_1_id        TEXT,
  item_name               TEXT,
  item_id                 TEXT NOT NULL,
  item_granularity        TEXT,
  time_hours_par          TEXT,
  description             TEXT,
  instructions            TEXT,
  addundum_extras         TEXT,
  confidence              TEXT,
  count_name              TEXT,
  frequency               TEXT,
  quality                 TEXT,
  source_git_sha          TEXT NOT NULL,
  synced_at               TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (item_id)
);

CREATE INDEX IF NOT EXISTS process_list_mirror_parent1_idx
  ON compliance.process_list_mirror (item_parent_1_id);
CREATE INDEX IF NOT EXISTS process_list_mirror_synced_at_idx
  ON compliance.process_list_mirror (synced_at DESC);

CREATE TABLE IF NOT EXISTS compliance.baseline_organisation_mirror (
  org_uuid                TEXT NOT NULL,
  role_name               TEXT,
  role_description        TEXT,
  role_full_description   TEXT,
  access_level            TEXT,
  reports_to              TEXT,
  area                    TEXT,
  entity                  TEXT,
  org_id                  TEXT,
  sop_url                 TEXT,
  responsible_processes   TEXT,
  components_used         TEXT,
  source_git_sha          TEXT NOT NULL,
  synced_at               TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (org_uuid)
);

CREATE INDEX IF NOT EXISTS baseline_org_mirror_synced_at_idx
  ON compliance.baseline_organisation_mirror (synced_at DESC);

CREATE SCHEMA IF NOT EXISTS holistika_ops;
COMMENT ON SCHEMA holistika_ops IS 'Holistika company CRM/billing; distinct from kirbe SaaS product schema';

CREATE TABLE IF NOT EXISTS holistika_ops.stripe_customer_link (
  id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  org_label               TEXT NOT NULL,
  stripe_customer_id      TEXT NOT NULL UNIQUE,
  livemode                BOOLEAN NOT NULL DEFAULT false,
  created_at              TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at              TIMESTAMPTZ NOT NULL DEFAULT now(),
  notes                   TEXT
);

CREATE TABLE IF NOT EXISTS holistika_ops.billing_account (
  id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  legal_entity_name       TEXT NOT NULL,
  currency                TEXT NOT NULL DEFAULT 'usd',
  stripe_customer_link_id UUID REFERENCES holistika_ops.stripe_customer_link(id),
  created_at              TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at              TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS billing_account_stripe_fk_idx
  ON holistika_ops.billing_account (stripe_customer_link_id);

-- RLS
ALTER TABLE compliance.process_list_mirror ENABLE ROW LEVEL SECURITY;
ALTER TABLE compliance.baseline_organisation_mirror ENABLE ROW LEVEL SECURITY;
ALTER TABLE holistika_ops.stripe_customer_link ENABLE ROW LEVEL SECURITY;
ALTER TABLE holistika_ops.billing_account ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS process_list_mirror_deny_authenticated ON compliance.process_list_mirror;
DROP POLICY IF EXISTS process_list_mirror_deny_anon ON compliance.process_list_mirror;
CREATE POLICY process_list_mirror_deny_authenticated
  ON compliance.process_list_mirror FOR ALL TO authenticated USING (false);
CREATE POLICY process_list_mirror_deny_anon
  ON compliance.process_list_mirror FOR ALL TO anon USING (false);

DROP POLICY IF EXISTS baseline_org_mirror_deny_authenticated ON compliance.baseline_organisation_mirror;
DROP POLICY IF EXISTS baseline_org_mirror_deny_anon ON compliance.baseline_organisation_mirror;
CREATE POLICY baseline_org_mirror_deny_authenticated
  ON compliance.baseline_organisation_mirror FOR ALL TO authenticated USING (false);
CREATE POLICY baseline_org_mirror_deny_anon
  ON compliance.baseline_organisation_mirror FOR ALL TO anon USING (false);

DROP POLICY IF EXISTS holistika_stripe_link_deny_authenticated ON holistika_ops.stripe_customer_link;
DROP POLICY IF EXISTS holistika_stripe_link_deny_anon ON holistika_ops.stripe_customer_link;
CREATE POLICY holistika_stripe_link_deny_authenticated
  ON holistika_ops.stripe_customer_link FOR ALL TO authenticated USING (false);
CREATE POLICY holistika_stripe_link_deny_anon
  ON holistika_ops.stripe_customer_link FOR ALL TO anon USING (false);

DROP POLICY IF EXISTS holistika_billing_deny_authenticated ON holistika_ops.billing_account;
DROP POLICY IF EXISTS holistika_billing_deny_anon ON holistika_ops.billing_account;
CREATE POLICY holistika_billing_deny_authenticated
  ON holistika_ops.billing_account FOR ALL TO authenticated USING (false);
CREATE POLICY holistika_billing_deny_anon
  ON holistika_ops.billing_account FOR ALL TO anon USING (false);

-- Grants (sync jobs use service_role; it bypasses RLS on Supabase)
GRANT USAGE ON SCHEMA compliance TO service_role;
GRANT ALL ON ALL TABLES IN SCHEMA compliance TO service_role;
GRANT USAGE ON SCHEMA holistika_ops TO service_role;
GRANT ALL ON ALL TABLES IN SCHEMA holistika_ops TO service_role;
