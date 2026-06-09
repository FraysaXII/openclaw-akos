-- P95-GOV-7 -- DATA_CONTRACT_REGISTRY mirror
BEGIN;
CREATE SCHEMA IF NOT EXISTS compliance;

CREATE TABLE IF NOT EXISTS compliance.data_contract_registry_mirror (
    contract_id TEXT NOT NULL PRIMARY KEY,
    producer_process_id TEXT,
    producer_area TEXT,
    consumer_area_ids TEXT,
    data_surface TEXT,
    schema_ref TEXT,
    semantics_ref TEXT,
    sla_freshness TEXT,
    sla_availability TEXT,
    quality_rules TEXT,
    classification TEXT,
    retention_policy_ref TEXT,
    version TEXT,
    status TEXT,
    owner_role TEXT,
    last_review_at TEXT,
    last_review_by TEXT,
    last_review_decision_id TEXT,
    methodology_version_at_review TEXT,
    notes TEXT,
    source_git_sha TEXT NOT NULL,
    synced_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT data_contract_registry_data_surface_chk CHECK (data_surface IN ('canonical_csv', 'mirror_table', 'fdw_projection', 'graph')),
    CONSTRAINT data_contract_registry_status_chk CHECK (status IN ('active', 'draft', 'deprecated'))
);

ALTER TABLE compliance.data_contract_registry_mirror ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS data_contract_registry_mirror_deny_authenticated ON compliance.data_contract_registry_mirror;
DROP POLICY IF EXISTS data_contract_registry_mirror_deny_anon ON compliance.data_contract_registry_mirror;
CREATE POLICY data_contract_registry_mirror_deny_authenticated ON compliance.data_contract_registry_mirror FOR ALL TO authenticated USING (false);
CREATE POLICY data_contract_registry_mirror_deny_anon ON compliance.data_contract_registry_mirror FOR ALL TO anon USING (false);
REVOKE ALL ON TABLE compliance.data_contract_registry_mirror FROM PUBLIC;
GRANT ALL ON TABLE compliance.data_contract_registry_mirror TO service_role;

COMMIT;
