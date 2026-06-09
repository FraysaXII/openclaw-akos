-- P95-GOV-7 -- RPA adapter registry mirror (9th adapter class)
BEGIN;
CREATE SCHEMA IF NOT EXISTS compliance;

CREATE TABLE IF NOT EXISTS compliance.rpa_adapter_registry_mirror (
    adapter_id TEXT NOT NULL PRIMARY KEY,
    registry_class TEXT NOT NULL DEFAULT 'RPA',
    vendor TEXT,
    adapter_kind TEXT,
    status TEXT,
    owner_role TEXT,
    linked_sop_path TEXT,
    linked_runbook_path TEXT,
    linked_decision_id TEXT,
    feature_flag TEXT,
    notes TEXT,
    last_review_at TEXT,
    last_review_by TEXT,
    last_review_decision_id TEXT,
    methodology_version_at_review TEXT,
    source_git_sha TEXT NOT NULL,
    synced_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT rpa_adapter_registry_class_chk CHECK (registry_class = 'RPA'),
    CONSTRAINT rpa_adapter_kind_chk CHECK (adapter_kind IN ('first_party_internal', 'normalized_shim', 'direct_native')),
    CONSTRAINT rpa_adapter_status_chk CHECK (status IN ('active', 'inactive', 'planned', 'experimental', 'deprecated')),
    CONSTRAINT rpa_adapter_feature_flag_chk CHECK (feature_flag IN ('active', 'gated_operator', 'gated_release_gate', 'always_on'))
);

ALTER TABLE compliance.rpa_adapter_registry_mirror ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS rpa_adapter_registry_mirror_deny_authenticated ON compliance.rpa_adapter_registry_mirror;
DROP POLICY IF EXISTS rpa_adapter_registry_mirror_deny_anon ON compliance.rpa_adapter_registry_mirror;
CREATE POLICY rpa_adapter_registry_mirror_deny_authenticated ON compliance.rpa_adapter_registry_mirror FOR ALL TO authenticated USING (false);
CREATE POLICY rpa_adapter_registry_mirror_deny_anon ON compliance.rpa_adapter_registry_mirror FOR ALL TO anon USING (false);
REVOKE ALL ON TABLE compliance.rpa_adapter_registry_mirror FROM PUBLIC;
GRANT ALL ON TABLE compliance.rpa_adapter_registry_mirror TO service_role;

COMMIT;
