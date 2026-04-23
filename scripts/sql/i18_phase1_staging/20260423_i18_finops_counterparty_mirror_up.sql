-- Initiative 18 — compliance.finops_counterparty_register_mirror + cutover (STAGING)
-- Parity: supabase/migrations/*_i18_finops_counterparty_mirror_cutover.sql
-- Idempotent where practical. See sql-proposal-stack-20260417.md §7.

CREATE SCHEMA IF NOT EXISTS compliance;
COMMENT ON SCHEMA compliance IS 'HLK git-backed projections; SSOT remains docs/references/hlk/compliance/*.csv';

CREATE TABLE IF NOT EXISTS compliance.finops_counterparty_register_mirror (
  counterparty_id          TEXT NOT NULL,
  counterparty_type        TEXT,
  display_name             TEXT,
  service_category         TEXT,
  billing_model            TEXT,
  commercial_segment       TEXT,
  revenue_model            TEXT,
  role_owner               TEXT,
  process_item_id          TEXT,
  repo_slug                TEXT,
  component_id             TEXT,
  contract_doc_pointer     TEXT,
  renewal_review_due       TEXT,
  status                   TEXT,
  pci_phi_pii_scope        TEXT,
  confidence_level         TEXT,
  notes                    TEXT,
  source_git_sha           TEXT NOT NULL,
  synced_at                TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (counterparty_id)
);

CREATE INDEX IF NOT EXISTS finops_counterparty_register_mirror_synced_at_idx
  ON compliance.finops_counterparty_register_mirror (synced_at DESC);
CREATE INDEX IF NOT EXISTS finops_counterparty_register_mirror_process_idx
  ON compliance.finops_counterparty_register_mirror (process_item_id);

ALTER TABLE compliance.finops_counterparty_register_mirror ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS finops_counterparty_register_mirror_deny_authenticated ON compliance.finops_counterparty_register_mirror;
DROP POLICY IF EXISTS finops_counterparty_register_mirror_deny_anon ON compliance.finops_counterparty_register_mirror;
CREATE POLICY finops_counterparty_register_mirror_deny_authenticated
  ON compliance.finops_counterparty_register_mirror FOR ALL TO authenticated USING (false);
CREATE POLICY finops_counterparty_register_mirror_deny_anon
  ON compliance.finops_counterparty_register_mirror FOR ALL TO anon USING (false);

REVOKE ALL ON TABLE compliance.finops_counterparty_register_mirror FROM PUBLIC;
GRANT ALL ON TABLE compliance.finops_counterparty_register_mirror TO service_role;

-- One-step cutover from Initiative 16 vendor mirror (if present)
DO $$
BEGIN
  IF EXISTS (
    SELECT 1 FROM information_schema.tables
    WHERE table_schema = 'compliance' AND table_name = 'finops_vendor_register_mirror'
  ) THEN
    INSERT INTO compliance.finops_counterparty_register_mirror (
      counterparty_id, counterparty_type, display_name, service_category, billing_model,
      commercial_segment, revenue_model, role_owner, process_item_id, repo_slug, component_id,
      contract_doc_pointer, renewal_review_due, status, pci_phi_pii_scope, confidence_level,
      notes, source_git_sha, synced_at
    )
    SELECT
      vendor_id,
      'vendor',
      vendor_display_name,
      service_category,
      billing_model,
      'na',
      'na',
      role_owner,
      process_item_id,
      repo_slug,
      component_id,
      contract_doc_pointer,
      renewal_review_due,
      status,
      pci_phi_pii_scope,
      confidence_level,
      notes,
      source_git_sha,
      synced_at
    FROM compliance.finops_vendor_register_mirror
    ON CONFLICT (counterparty_id) DO NOTHING;
    DROP TABLE compliance.finops_vendor_register_mirror;
  END IF;
END $$;

ALTER TABLE holistika_ops.stripe_customer_link
  ADD COLUMN IF NOT EXISTS finops_counterparty_id TEXT;

COMMENT ON COLUMN holistika_ops.stripe_customer_link.finops_counterparty_id IS
  'Optional FINOPS_COUNTERPARTY_REGISTER.csv counterparty_id slug; git authoritative; not a FK to compliance mirror.';

-- Optional: privilege hardening when Stripe Wrapper schema exists (inventory-first; no secrets in git)
DO $$
BEGIN
  IF EXISTS (SELECT 1 FROM information_schema.schemata WHERE schema_name = 'stripe_gtm') THEN
    EXECUTE 'REVOKE ALL ON SCHEMA stripe_gtm FROM PUBLIC';
    EXECUTE 'GRANT USAGE ON SCHEMA stripe_gtm TO service_role';
    EXECUTE 'GRANT SELECT ON ALL TABLES IN SCHEMA stripe_gtm TO service_role';
    EXECUTE 'ALTER DEFAULT PRIVILEGES IN SCHEMA stripe_gtm GRANT SELECT ON TABLES TO service_role';
  END IF;
END $$;
