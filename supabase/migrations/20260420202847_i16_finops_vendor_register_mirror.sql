-- Parity: scripts/sql/i16_phase3_staging/20260420_i16_finops_vendor_mirror_up.sql
-- Dashboard migration version name: i16_finops_vendor_register_mirror (Initiative 16)
-- Initiative 16 — compliance.finops_vendor_register_mirror

CREATE SCHEMA IF NOT EXISTS compliance;
COMMENT ON SCHEMA compliance IS 'HLK git-backed projections; SSOT remains docs/references/hlk/compliance/*.csv';

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

CREATE INDEX IF NOT EXISTS finops_vendor_register_mirror_synced_at_idx
  ON compliance.finops_vendor_register_mirror (synced_at DESC);
CREATE INDEX IF NOT EXISTS finops_vendor_register_mirror_process_idx
  ON compliance.finops_vendor_register_mirror (process_item_id);

ALTER TABLE compliance.finops_vendor_register_mirror ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS finops_vendor_register_mirror_deny_authenticated ON compliance.finops_vendor_register_mirror;
DROP POLICY IF EXISTS finops_vendor_register_mirror_deny_anon ON compliance.finops_vendor_register_mirror;
CREATE POLICY finops_vendor_register_mirror_deny_authenticated
  ON compliance.finops_vendor_register_mirror FOR ALL TO authenticated USING (false);
CREATE POLICY finops_vendor_register_mirror_deny_anon
  ON compliance.finops_vendor_register_mirror FOR ALL TO anon USING (false);

REVOKE ALL ON TABLE compliance.finops_vendor_register_mirror FROM PUBLIC;
GRANT ALL ON TABLE compliance.finops_vendor_register_mirror TO service_role;
