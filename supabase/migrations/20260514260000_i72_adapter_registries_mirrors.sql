-- Initiative 72 P9 — 8 adapter registry mirrors (Normalized Adapter Pattern).
--
-- Per D-IH-72-O (Normalized Adapter Pattern + status metadata) +
-- D-IH-72-T (MarTech adapter breadth: 8 sibling registries) +
-- D-IH-72-W (feature-flag pattern with TODO markers).
--
-- 8 mirror tables each receive upserts from their canonical CSV via the
-- compliance_mirror_emit profile (sync_compliance_mirrors_from_csv.py).
-- Server-only (service_role) RLS posture per the existing compliance.* mirror
-- baseline established by I59 P1.5 + I70 P8.1.

BEGIN;

-- ============================================================================
-- Generic adapter registry mirror schema (15 columns mirroring CSV header)
-- ============================================================================

-- 1) CRM_ADAPTER_REGISTRY
CREATE TABLE IF NOT EXISTS compliance.crm_adapter_registry_mirror (
    adapter_id                       text NOT NULL PRIMARY KEY,
    registry_class                   text NOT NULL DEFAULT 'CRM',
    vendor                           text,
    adapter_kind                     text,
    status                           text,
    owner_role                       text,
    linked_sop_path                  text,
    linked_runbook_path              text,
    linked_decision_id               text,
    feature_flag                     text,
    notes                            text,
    last_review_at                   text,
    last_review_by                   text,
    last_review_decision_id          text,
    methodology_version_at_review    text,
    source_git_sha                   text,
    synced_at                        timestamptz DEFAULT now(),
    CONSTRAINT crm_adapter_registry_class_chk CHECK (registry_class = 'CRM'),
    CONSTRAINT crm_adapter_kind_chk CHECK (adapter_kind IN ('first_party_internal', 'normalized_shim', 'direct_native')),
    CONSTRAINT crm_adapter_status_chk CHECK (status IN ('active', 'inactive', 'planned', 'experimental', 'deprecated')),
    CONSTRAINT crm_adapter_feature_flag_chk CHECK (feature_flag IN ('active', 'gated_operator', 'gated_release_gate', 'always_on'))
);
CREATE INDEX IF NOT EXISTS crm_adapter_registry_status_idx ON compliance.crm_adapter_registry_mirror (status);
CREATE INDEX IF NOT EXISTS crm_adapter_registry_owner_idx ON compliance.crm_adapter_registry_mirror (owner_role);
ALTER TABLE compliance.crm_adapter_registry_mirror ENABLE ROW LEVEL SECURITY;

-- 2) REVOPS_ADAPTER_REGISTRY
CREATE TABLE IF NOT EXISTS compliance.revops_adapter_registry_mirror (
    adapter_id                       text NOT NULL PRIMARY KEY,
    registry_class                   text NOT NULL DEFAULT 'REVOPS',
    vendor                           text,
    adapter_kind                     text,
    status                           text,
    owner_role                       text,
    linked_sop_path                  text,
    linked_runbook_path              text,
    linked_decision_id               text,
    feature_flag                     text,
    notes                            text,
    last_review_at                   text,
    last_review_by                   text,
    last_review_decision_id          text,
    methodology_version_at_review    text,
    source_git_sha                   text,
    synced_at                        timestamptz DEFAULT now(),
    CONSTRAINT revops_adapter_registry_class_chk CHECK (registry_class = 'REVOPS'),
    CONSTRAINT revops_adapter_kind_chk CHECK (adapter_kind IN ('first_party_internal', 'normalized_shim', 'direct_native')),
    CONSTRAINT revops_adapter_status_chk CHECK (status IN ('active', 'inactive', 'planned', 'experimental', 'deprecated')),
    CONSTRAINT revops_adapter_feature_flag_chk CHECK (feature_flag IN ('active', 'gated_operator', 'gated_release_gate', 'always_on'))
);
CREATE INDEX IF NOT EXISTS revops_adapter_registry_status_idx ON compliance.revops_adapter_registry_mirror (status);
ALTER TABLE compliance.revops_adapter_registry_mirror ENABLE ROW LEVEL SECURITY;

-- 3) EMAIL_ADAPTER_REGISTRY
CREATE TABLE IF NOT EXISTS compliance.email_adapter_registry_mirror (
    adapter_id                       text NOT NULL PRIMARY KEY,
    registry_class                   text NOT NULL DEFAULT 'EMAIL',
    vendor                           text,
    adapter_kind                     text,
    status                           text,
    owner_role                       text,
    linked_sop_path                  text,
    linked_runbook_path              text,
    linked_decision_id               text,
    feature_flag                     text,
    notes                            text,
    last_review_at                   text,
    last_review_by                   text,
    last_review_decision_id          text,
    methodology_version_at_review    text,
    source_git_sha                   text,
    synced_at                        timestamptz DEFAULT now(),
    CONSTRAINT email_adapter_registry_class_chk CHECK (registry_class = 'EMAIL'),
    CONSTRAINT email_adapter_kind_chk CHECK (adapter_kind IN ('first_party_internal', 'normalized_shim', 'direct_native')),
    CONSTRAINT email_adapter_status_chk CHECK (status IN ('active', 'inactive', 'planned', 'experimental', 'deprecated')),
    CONSTRAINT email_adapter_feature_flag_chk CHECK (feature_flag IN ('active', 'gated_operator', 'gated_release_gate', 'always_on'))
);
CREATE INDEX IF NOT EXISTS email_adapter_registry_status_idx ON compliance.email_adapter_registry_mirror (status);
ALTER TABLE compliance.email_adapter_registry_mirror ENABLE ROW LEVEL SECURITY;

-- 4) ATTRIBUTION_ADAPTER_REGISTRY
CREATE TABLE IF NOT EXISTS compliance.attribution_adapter_registry_mirror (
    adapter_id                       text NOT NULL PRIMARY KEY,
    registry_class                   text NOT NULL DEFAULT 'ATTRIBUTION',
    vendor                           text,
    adapter_kind                     text,
    status                           text,
    owner_role                       text,
    linked_sop_path                  text,
    linked_runbook_path              text,
    linked_decision_id               text,
    feature_flag                     text,
    notes                            text,
    last_review_at                   text,
    last_review_by                   text,
    last_review_decision_id          text,
    methodology_version_at_review    text,
    source_git_sha                   text,
    synced_at                        timestamptz DEFAULT now(),
    CONSTRAINT attribution_adapter_registry_class_chk CHECK (registry_class = 'ATTRIBUTION'),
    CONSTRAINT attribution_adapter_kind_chk CHECK (adapter_kind IN ('first_party_internal', 'normalized_shim', 'direct_native')),
    CONSTRAINT attribution_adapter_status_chk CHECK (status IN ('active', 'inactive', 'planned', 'experimental', 'deprecated')),
    CONSTRAINT attribution_adapter_feature_flag_chk CHECK (feature_flag IN ('active', 'gated_operator', 'gated_release_gate', 'always_on'))
);
ALTER TABLE compliance.attribution_adapter_registry_mirror ENABLE ROW LEVEL SECURITY;

-- 5) BILLING_ADAPTER_REGISTRY
CREATE TABLE IF NOT EXISTS compliance.billing_adapter_registry_mirror (
    adapter_id                       text NOT NULL PRIMARY KEY,
    registry_class                   text NOT NULL DEFAULT 'BILLING',
    vendor                           text,
    adapter_kind                     text,
    status                           text,
    owner_role                       text,
    linked_sop_path                  text,
    linked_runbook_path              text,
    linked_decision_id               text,
    feature_flag                     text,
    notes                            text,
    last_review_at                   text,
    last_review_by                   text,
    last_review_decision_id          text,
    methodology_version_at_review    text,
    source_git_sha                   text,
    synced_at                        timestamptz DEFAULT now(),
    CONSTRAINT billing_adapter_registry_class_chk CHECK (registry_class = 'BILLING'),
    CONSTRAINT billing_adapter_kind_chk CHECK (adapter_kind IN ('first_party_internal', 'normalized_shim', 'direct_native')),
    CONSTRAINT billing_adapter_status_chk CHECK (status IN ('active', 'inactive', 'planned', 'experimental', 'deprecated')),
    CONSTRAINT billing_adapter_feature_flag_chk CHECK (feature_flag IN ('active', 'gated_operator', 'gated_release_gate', 'always_on'))
);
ALTER TABLE compliance.billing_adapter_registry_mirror ENABLE ROW LEVEL SECURITY;

-- 6) COMMUNICATION_ADAPTER_REGISTRY
CREATE TABLE IF NOT EXISTS compliance.communication_adapter_registry_mirror (
    adapter_id                       text NOT NULL PRIMARY KEY,
    registry_class                   text NOT NULL DEFAULT 'COMMUNICATION',
    vendor                           text,
    adapter_kind                     text,
    status                           text,
    owner_role                       text,
    linked_sop_path                  text,
    linked_runbook_path              text,
    linked_decision_id               text,
    feature_flag                     text,
    notes                            text,
    last_review_at                   text,
    last_review_by                   text,
    last_review_decision_id          text,
    methodology_version_at_review    text,
    source_git_sha                   text,
    synced_at                        timestamptz DEFAULT now(),
    CONSTRAINT communication_adapter_registry_class_chk CHECK (registry_class = 'COMMUNICATION'),
    CONSTRAINT communication_adapter_kind_chk CHECK (adapter_kind IN ('first_party_internal', 'normalized_shim', 'direct_native')),
    CONSTRAINT communication_adapter_status_chk CHECK (status IN ('active', 'inactive', 'planned', 'experimental', 'deprecated')),
    CONSTRAINT communication_adapter_feature_flag_chk CHECK (feature_flag IN ('active', 'gated_operator', 'gated_release_gate', 'always_on'))
);
ALTER TABLE compliance.communication_adapter_registry_mirror ENABLE ROW LEVEL SECURITY;

-- 7) SCHEDULING_ADAPTER_REGISTRY
CREATE TABLE IF NOT EXISTS compliance.scheduling_adapter_registry_mirror (
    adapter_id                       text NOT NULL PRIMARY KEY,
    registry_class                   text NOT NULL DEFAULT 'SCHEDULING',
    vendor                           text,
    adapter_kind                     text,
    status                           text,
    owner_role                       text,
    linked_sop_path                  text,
    linked_runbook_path              text,
    linked_decision_id               text,
    feature_flag                     text,
    notes                            text,
    last_review_at                   text,
    last_review_by                   text,
    last_review_decision_id          text,
    methodology_version_at_review    text,
    source_git_sha                   text,
    synced_at                        timestamptz DEFAULT now(),
    CONSTRAINT scheduling_adapter_registry_class_chk CHECK (registry_class = 'SCHEDULING'),
    CONSTRAINT scheduling_adapter_kind_chk CHECK (adapter_kind IN ('first_party_internal', 'normalized_shim', 'direct_native')),
    CONSTRAINT scheduling_adapter_status_chk CHECK (status IN ('active', 'inactive', 'planned', 'experimental', 'deprecated')),
    CONSTRAINT scheduling_adapter_feature_flag_chk CHECK (feature_flag IN ('active', 'gated_operator', 'gated_release_gate', 'always_on'))
);
ALTER TABLE compliance.scheduling_adapter_registry_mirror ENABLE ROW LEVEL SECURITY;

-- 8) CONTRACT_ADAPTER_REGISTRY
CREATE TABLE IF NOT EXISTS compliance.contract_adapter_registry_mirror (
    adapter_id                       text NOT NULL PRIMARY KEY,
    registry_class                   text NOT NULL DEFAULT 'CONTRACT',
    vendor                           text,
    adapter_kind                     text,
    status                           text,
    owner_role                       text,
    linked_sop_path                  text,
    linked_runbook_path              text,
    linked_decision_id               text,
    feature_flag                     text,
    notes                            text,
    last_review_at                   text,
    last_review_by                   text,
    last_review_decision_id          text,
    methodology_version_at_review    text,
    source_git_sha                   text,
    synced_at                        timestamptz DEFAULT now(),
    CONSTRAINT contract_adapter_registry_class_chk CHECK (registry_class = 'CONTRACT'),
    CONSTRAINT contract_adapter_kind_chk CHECK (adapter_kind IN ('first_party_internal', 'normalized_shim', 'direct_native')),
    CONSTRAINT contract_adapter_status_chk CHECK (status IN ('active', 'inactive', 'planned', 'experimental', 'deprecated')),
    CONSTRAINT contract_adapter_feature_flag_chk CHECK (feature_flag IN ('active', 'gated_operator', 'gated_release_gate', 'always_on'))
);
ALTER TABLE compliance.contract_adapter_registry_mirror ENABLE ROW LEVEL SECURITY;

-- ============================================================================
-- Comments documenting the I72 P9 contract
-- ============================================================================

COMMENT ON TABLE compliance.crm_adapter_registry_mirror IS
    'I72 P9 D-IH-72-O — CRM adapter registry mirror. Normalized Adapter Pattern (Truto/Unified.to/Apideck consensus 2026). Server-only (service_role).';
COMMENT ON TABLE compliance.revops_adapter_registry_mirror IS
    'I72 P9 D-IH-72-O — RevOps adapter registry mirror (cross-area handoff bridges: finops_bridge, people_engagement_handoff, legal_template_fire, madeira_revops_handoff). Server-only (service_role).';
COMMENT ON TABLE compliance.email_adapter_registry_mirror IS
    'I72 P9 D-IH-72-T — Email adapter registry mirror.';
COMMENT ON TABLE compliance.attribution_adapter_registry_mirror IS
    'I72 P9 D-IH-72-T — Attribution adapter registry mirror.';
COMMENT ON TABLE compliance.billing_adapter_registry_mirror IS
    'I72 P9 D-IH-72-T — Billing adapter registry mirror (Stripe + alternates).';
COMMENT ON TABLE compliance.communication_adapter_registry_mirror IS
    'I72 P9 D-IH-72-T — Communication adapter registry mirror.';
COMMENT ON TABLE compliance.scheduling_adapter_registry_mirror IS
    'I72 P9 D-IH-72-T — Scheduling adapter registry mirror.';
COMMENT ON TABLE compliance.contract_adapter_registry_mirror IS
    'I72 P9 D-IH-72-T — Contract adapter registry mirror (NDA/MSA/SOW signing platforms).';

COMMIT;
