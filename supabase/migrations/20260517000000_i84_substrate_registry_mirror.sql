-- Initiative 84 P3c — compliance.substrate_registry_mirror (substrate doctrine mirror).
--
-- Per D-IH-84-A (mega charter) + D-IH-84-F (18-column schema + 8 enum frozensets)
-- + D-IH-84-G (paired Research-area SUBSTRATE_LANDSCAPE_DOCTRINE.md).
--
-- Mirror table for SUBSTRATE_REGISTRY.csv canonical at
-- docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/SUBSTRATE_REGISTRY.csv.
-- Receives upserts from the canonical CSV via the compliance_mirror_emit profile
-- (sync_compliance_mirrors_from_csv.py --substrate-registry-only) per the pattern
-- established by I59 P1.5, I72 P9, I73 P1, I79 P2.
--
-- Server-only (service_role) RLS posture per the existing compliance.* mirror
-- baseline. CHECK constraints mirror the 8 Pydantic Literal-typed enum columns
-- in akos/hlk_substrate_registry_csv.py.

BEGIN;

-- ============================================================================
-- compliance.substrate_registry_mirror
-- ============================================================================

CREATE TABLE IF NOT EXISTS compliance.substrate_registry_mirror (
    substrate_id                     text NOT NULL PRIMARY KEY,
    name                             text,
    vendor                           text,
    runtime_shape                    text,
    persistence_model                text,
    tool_protocol                    text,
    multi_tenant_ready               text,
    license_class                    text,
    status                           text,
    cost_class                       text,
    pricing_unit                     text,
    founder_principle_alignment      text,
    akos_integration_state           text,
    madeira_productization_role      text,
    aic_pattern_role                 text,
    last_audit_date                  date,
    audit_source_url                 text,
    notes                            text,
    source_git_sha                   text,
    synced_at                        timestamptz DEFAULT now(),
    CONSTRAINT substrate_registry_runtime_shape_chk
        CHECK (runtime_shape IN (
            'agent-sdk-typescript', 'agent-sdk-python', 'agent-sdk-rest',
            'framework-library-python', 'framework-library-typescript',
            'hosted-agent-platform', 'inference-provider', 'orchestration-engine'
        )),
    CONSTRAINT substrate_registry_persistence_model_chk
        CHECK (persistence_model IN (
            'ephemeral', 'session-scoped', 'persistent', 'cloud-managed'
        )),
    CONSTRAINT substrate_registry_tool_protocol_chk
        CHECK (tool_protocol IN (
            'mcp', 'openai-functions', 'anthropic-tools',
            'cursor-native', 'langchain-native', 'native-only'
        )),
    CONSTRAINT substrate_registry_license_class_chk
        CHECK (license_class IN (
            'proprietary-saas', 'open-weights-model',
            'open-source-mit', 'open-source-apache', 'open-source-other',
            'commercial-license'
        )),
    CONSTRAINT substrate_registry_status_chk
        CHECK (status IN (
            'active', 'candidate', 'experimental', 'deprecated', 'forecasted'
        )),
    CONSTRAINT substrate_registry_cost_class_chk
        CHECK (cost_class IN (
            'token-billed', 'seat-billed', 'gpu-hour-billed',
            'bring-your-own-key', 'free-tier-only', 'hybrid'
        )),
    CONSTRAINT substrate_registry_akos_integration_state_chk
        CHECK (akos_integration_state IN (
            'in-production', 'pilot', 'forecasted',
            'blocked', 'rejected', 'candidate'
        )),
    CONSTRAINT substrate_registry_madeira_role_chk
        CHECK (madeira_productization_role IN (
            'backend-only', 'library-import', 'agent-runtime',
            'not-applicable', 'forecasted'
        )),
    CONSTRAINT substrate_registry_aic_role_chk
        CHECK (aic_pattern_role IN (
            'supervisor', 'sub-agent', 'peer', 'dispatcher',
            'single-agent-rich-tools', 'not-applicable'
        ))
);

CREATE INDEX IF NOT EXISTS substrate_registry_status_idx
    ON compliance.substrate_registry_mirror (status);

CREATE INDEX IF NOT EXISTS substrate_registry_akos_state_idx
    ON compliance.substrate_registry_mirror (akos_integration_state);

CREATE INDEX IF NOT EXISTS substrate_registry_vendor_idx
    ON compliance.substrate_registry_mirror (vendor);

CREATE INDEX IF NOT EXISTS substrate_registry_last_audit_idx
    ON compliance.substrate_registry_mirror (last_audit_date DESC);

ALTER TABLE compliance.substrate_registry_mirror ENABLE ROW LEVEL SECURITY;

-- service_role-only: deny anon + authenticated explicitly.
-- (Compliance-mirror baseline per I59 P1.5; service_role can SELECT + INSERT +
-- UPDATE; anon/authenticated have no policies and thus inherit deny default.)
GRANT SELECT, INSERT, UPDATE ON compliance.substrate_registry_mirror TO service_role;
REVOKE ALL ON compliance.substrate_registry_mirror FROM anon, authenticated;

COMMENT ON TABLE compliance.substrate_registry_mirror IS
    'I84 P3 substrate doctrine mirror; mirrors SUBSTRATE_REGISTRY.csv canonical; sync via sync_compliance_mirrors_from_csv.py --substrate-registry-only';

COMMIT;
