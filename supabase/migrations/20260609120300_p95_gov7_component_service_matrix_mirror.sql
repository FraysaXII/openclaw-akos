-- P95-GOV-7 -- COMPONENT_SERVICE_MATRIX mirror
BEGIN;
CREATE SCHEMA IF NOT EXISTS compliance;

CREATE TABLE IF NOT EXISTS compliance.component_service_matrix_mirror (
    component_id TEXT,
    component_name TEXT,
    component_kind TEXT,
    lifecycle_status TEXT,
    entity TEXT,
    area TEXT,
    primary_owner_role TEXT,
    steward_ops_domain TEXT,
    secondary_owner_role TEXT,
    escalation_owner_role TEXT,
    repo_slug TEXT,
    github_url TEXT,
    api_exposure TEXT,
    api_spec_pointer TEXT,
    integration_pattern TEXT,
    depends_on_component_ids TEXT,
    parent_component_id TEXT,
    primary_process_item_id TEXT,
    related_process_item_ids TEXT,
    topic_ids TEXT,
    access_level_data TEXT,
    data_classification TEXT,
    environment_scope TEXT,
    slo_tier TEXT,
    runbook_link TEXT,
    doc_link TEXT,
    legal_hold TEXT,
    retention_policy_ref TEXT,
    last_verified_date TEXT,
    source_row TEXT,
    notes TEXT,
    source_git_sha TEXT NOT NULL,
    synced_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (component_id),

    CONSTRAINT component_service_matrix_component_kind_chk CHECK (component_kind IN ('repository', 'saas', 'data_platform', 'integration', 'edge_function', 'library', 'infrastructure', 'observability', 'client_runtime', 'other')),
    CONSTRAINT component_service_matrix_lifecycle_status_chk CHECK (lifecycle_status IN ('experimental', 'active', 'constrained', 'sunset', 'retired')),
    CONSTRAINT component_service_matrix_steward_ops_domain_chk CHECK (steward_ops_domain IN ('MAROPS', 'DEVOPS', 'DATAOPS', 'PMSMO', 'LEGOPS', 'FINOPS', 'GTMOPS', 'SECOPS', 'other')),
    CONSTRAINT component_service_matrix_api_exposure_chk CHECK (api_exposure IN ('none', 'internal', 'partner', 'public')),
    CONSTRAINT component_service_matrix_integration_pattern_chk CHECK (integration_pattern IN ('push', 'pull', 'batch', 'stream', 'event', 'manual', 'n_a', 'edge_webhook', 'pgmq_worker', 'fdw_read', 'low_code_rpa', 'embedded_chart')),
    CONSTRAINT component_service_matrix_environment_scope_chk CHECK (environment_scope IN ('dev', 'staging', 'prod', 'multi', 'local_only')),
    CONSTRAINT component_service_matrix_slo_tier_chk CHECK (slo_tier IN ('best_effort', 'standard', 'critical'))

);
CREATE INDEX IF NOT EXISTS component_service_matrix_mirror_lifecycle_idx ON compliance.component_service_matrix_mirror (lifecycle_status);

ALTER TABLE compliance.component_service_matrix_mirror ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS component_service_matrix_mirror_deny_authenticated ON compliance.component_service_matrix_mirror;
DROP POLICY IF EXISTS component_service_matrix_mirror_deny_anon ON compliance.component_service_matrix_mirror;
CREATE POLICY component_service_matrix_mirror_deny_authenticated ON compliance.component_service_matrix_mirror FOR ALL TO authenticated USING (false);
CREATE POLICY component_service_matrix_mirror_deny_anon ON compliance.component_service_matrix_mirror FOR ALL TO anon USING (false);
REVOKE ALL ON TABLE compliance.component_service_matrix_mirror FROM PUBLIC;
GRANT ALL ON TABLE compliance.component_service_matrix_mirror TO service_role;

COMMIT;
