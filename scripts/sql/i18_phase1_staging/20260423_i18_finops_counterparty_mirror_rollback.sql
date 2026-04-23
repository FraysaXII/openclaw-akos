-- Initiative 18 — BREAK-GLASS rollback (staging reference only)
-- Recreates empty Initiative 16 vendor mirror shape; drops counterparty mirror.
-- Data loss unless restored from backup or re-sync from CSV.

DROP POLICY IF EXISTS finops_counterparty_register_mirror_deny_authenticated ON compliance.finops_counterparty_register_mirror;
DROP POLICY IF EXISTS finops_counterparty_register_mirror_deny_anon ON compliance.finops_counterparty_register_mirror;
DROP TABLE IF EXISTS compliance.finops_counterparty_register_mirror;

CREATE TABLE IF NOT EXISTS compliance.finops_vendor_register_mirror (
  vendor_id               TEXT NOT NULL,
  vendor_display_name     TEXT,
  service_category        TEXT,
  billing_model           TEXT,
  role_owner              TEXT,
  process_item_id         TEXT,
  repo_slug               TEXT,
  component_id            TEXT,
  contract_doc_pointer    TEXT,
  renewal_review_due      TEXT,
  status                  TEXT,
  pci_phi_pii_scope       TEXT,
  confidence_level        TEXT,
  notes                   TEXT,
  source_git_sha          TEXT NOT NULL,
  synced_at               TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (vendor_id)
);

ALTER TABLE compliance.finops_vendor_register_mirror ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS finops_vendor_register_mirror_deny_authenticated ON compliance.finops_vendor_register_mirror;
DROP POLICY IF EXISTS finops_vendor_register_mirror_deny_anon ON compliance.finops_vendor_register_mirror;
CREATE POLICY finops_vendor_register_mirror_deny_authenticated
  ON compliance.finops_vendor_register_mirror FOR ALL TO authenticated USING (false);
CREATE POLICY finops_vendor_register_mirror_deny_anon
  ON compliance.finops_vendor_register_mirror FOR ALL TO anon USING (false);
REVOKE ALL ON TABLE compliance.finops_vendor_register_mirror FROM PUBLIC;
GRANT ALL ON TABLE compliance.finops_vendor_register_mirror TO service_role;

ALTER TABLE holistika_ops.stripe_customer_link DROP COLUMN IF EXISTS finops_counterparty_id;
