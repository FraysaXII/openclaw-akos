-- P95-GOV-7 -- Finance Plane-2 registry mirrors (pricing tier + performance obligation + tax calendar)
-- D-IH-95-B forward-charter DDL activation; enum CHECK parity with akos/hlk_pricing_tier_registry_csv.py + hlk_finops_tax_calendar_csv.py

BEGIN;
CREATE SCHEMA IF NOT EXISTS compliance;

CREATE TABLE IF NOT EXISTS compliance.pricing_tier_registry_mirror (
    pricing_tier_id TEXT NOT NULL PRIMARY KEY,
    tier_slug TEXT,
    display_name TEXT,
    product_surface TEXT,
    performance_obligation_id TEXT,
    pmo_pricing_model_ref TEXT,
    billing_cadence TEXT,
    status TEXT,
    last_review_at TEXT,
    last_review_by TEXT,
    last_review_decision_id TEXT,
    methodology_version_at_review TEXT,
    notes TEXT,
    source_git_sha TEXT NOT NULL,
    synced_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT pricing_tier_registry_product_surface_chk CHECK (product_surface IN ('kirbe_saas', 'service_engagement', 'partner_channel', 'internal_trial')),
    CONSTRAINT pricing_tier_registry_billing_cadence_chk CHECK (billing_cadence IN ('monthly', 'annual_prepay', 'one_time', 'usage_metered', 'n_a')),
    CONSTRAINT pricing_tier_registry_status_chk CHECK (status IN ('active', 'draft', 'deprecated'))
);
CREATE INDEX IF NOT EXISTS pricing_tier_registry_mirror_status_idx ON compliance.pricing_tier_registry_mirror (status);

ALTER TABLE compliance.pricing_tier_registry_mirror ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS pricing_tier_registry_mirror_deny_authenticated ON compliance.pricing_tier_registry_mirror;
DROP POLICY IF EXISTS pricing_tier_registry_mirror_deny_anon ON compliance.pricing_tier_registry_mirror;
CREATE POLICY pricing_tier_registry_mirror_deny_authenticated ON compliance.pricing_tier_registry_mirror FOR ALL TO authenticated USING (false);
CREATE POLICY pricing_tier_registry_mirror_deny_anon ON compliance.pricing_tier_registry_mirror FOR ALL TO anon USING (false);
REVOKE ALL ON TABLE compliance.pricing_tier_registry_mirror FROM PUBLIC;
GRANT ALL ON TABLE compliance.pricing_tier_registry_mirror TO service_role;


CREATE TABLE IF NOT EXISTS compliance.finops_performance_obligation_registry_mirror (
    obligation_id TEXT NOT NULL PRIMARY KEY,
    obligation_name TEXT,
    ifrs15_pattern TEXT,
    recognition_trigger TEXT,
    policy_section_ref TEXT,
    status TEXT,
    last_review_at TEXT,
    last_review_by TEXT,
    last_review_decision_id TEXT,
    methodology_version_at_review TEXT,
    notes TEXT,
    source_git_sha TEXT NOT NULL,
    synced_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT finops_perf_obligation_ifrs15_pattern_chk CHECK (ifrs15_pattern IN ('over_time', 'point_in_time')),
    CONSTRAINT finops_perf_obligation_status_chk CHECK (status IN ('active', 'draft', 'deprecated'))
);

ALTER TABLE compliance.finops_performance_obligation_registry_mirror ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS finops_performance_obligation_registry_mirror_deny_authenticated ON compliance.finops_performance_obligation_registry_mirror;
DROP POLICY IF EXISTS finops_performance_obligation_registry_mirror_deny_anon ON compliance.finops_performance_obligation_registry_mirror;
CREATE POLICY finops_performance_obligation_registry_mirror_deny_authenticated ON compliance.finops_performance_obligation_registry_mirror FOR ALL TO authenticated USING (false);
CREATE POLICY finops_performance_obligation_registry_mirror_deny_anon ON compliance.finops_performance_obligation_registry_mirror FOR ALL TO anon USING (false);
REVOKE ALL ON TABLE compliance.finops_performance_obligation_registry_mirror FROM PUBLIC;
GRANT ALL ON TABLE compliance.finops_performance_obligation_registry_mirror TO service_role;


CREATE TABLE IF NOT EXISTS compliance.finops_tax_calendar_mirror (
    obligation_id TEXT NOT NULL PRIMARY KEY,
    modelo_code TEXT,
    obligation_name TEXT,
    cadence_type TEXT,
    cadence_rule TEXT,
    hacienda_authority TEXT,
    applicability_gate TEXT,
    responsible_role TEXT,
    executor_party TEXT,
    paired_sop_path TEXT,
    paired_runbook_path TEXT,
    last_filed_at TEXT,
    next_due_at TEXT,
    source_ref TEXT,
    status TEXT,
    last_review_at TEXT,
    last_review_by TEXT,
    last_review_decision_id TEXT,
    methodology_version_at_review TEXT,
    notes TEXT,
    source_git_sha TEXT NOT NULL,
    synced_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT finops_tax_calendar_cadence_type_chk CHECK (cadence_type IN ('monthly', 'quarterly', 'annual', 'event_triggered', 'on_demand')),
    CONSTRAINT finops_tax_calendar_hacienda_authority_chk CHECK (hacienda_authority IN ('AEAT_common', 'foral_deferred')),
    CONSTRAINT finops_tax_calendar_applicability_gate_chk CHECK (applicability_gate IN ('always', 'at_incorporation', 'if_autonomo_path', 'if_foreign_assets_gt_50k_eur', 'post_first_fiscal_year')),
    CONSTRAINT finops_tax_calendar_status_chk CHECK (status IN ('active', 'draft', 'not_applicable_yet'))
);

ALTER TABLE compliance.finops_tax_calendar_mirror ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS finops_tax_calendar_mirror_deny_authenticated ON compliance.finops_tax_calendar_mirror;
DROP POLICY IF EXISTS finops_tax_calendar_mirror_deny_anon ON compliance.finops_tax_calendar_mirror;
CREATE POLICY finops_tax_calendar_mirror_deny_authenticated ON compliance.finops_tax_calendar_mirror FOR ALL TO authenticated USING (false);
CREATE POLICY finops_tax_calendar_mirror_deny_anon ON compliance.finops_tax_calendar_mirror FOR ALL TO anon USING (false);
REVOKE ALL ON TABLE compliance.finops_tax_calendar_mirror FROM PUBLIC;
GRANT ALL ON TABLE compliance.finops_tax_calendar_mirror TO service_role;

COMMIT;
