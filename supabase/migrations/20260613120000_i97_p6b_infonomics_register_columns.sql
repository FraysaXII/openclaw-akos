-- I97 P6b-CSV — Infonomics register economic columns on compliance mirrors (D-IH-97-E).
BEGIN;

ALTER TABLE compliance.data_contract_registry_mirror
    ADD COLUMN IF NOT EXISTS economic_value_class TEXT,
    ADD COLUMN IF NOT EXISTS carrying_cost_band TEXT,
    ADD COLUMN IF NOT EXISTS monetization_status TEXT;

ALTER TABLE compliance.finops_counterparty_register_mirror
    ADD COLUMN IF NOT EXISTS information_asset_ref TEXT;

ALTER TABLE compliance.finops_performance_obligation_registry_mirror
    ADD COLUMN IF NOT EXISTS information_asset_ref TEXT;

-- All 9 adapter registry mirrors share the post-I97 hook columns.
ALTER TABLE compliance.crm_adapter_registry_mirror
    ADD COLUMN IF NOT EXISTS handoff_cost_band TEXT,
    ADD COLUMN IF NOT EXISTS value_stream_id TEXT;
ALTER TABLE compliance.revops_adapter_registry_mirror
    ADD COLUMN IF NOT EXISTS handoff_cost_band TEXT,
    ADD COLUMN IF NOT EXISTS value_stream_id TEXT;
ALTER TABLE compliance.email_adapter_registry_mirror
    ADD COLUMN IF NOT EXISTS handoff_cost_band TEXT,
    ADD COLUMN IF NOT EXISTS value_stream_id TEXT;
ALTER TABLE compliance.attribution_adapter_registry_mirror
    ADD COLUMN IF NOT EXISTS handoff_cost_band TEXT,
    ADD COLUMN IF NOT EXISTS value_stream_id TEXT;
ALTER TABLE compliance.billing_adapter_registry_mirror
    ADD COLUMN IF NOT EXISTS handoff_cost_band TEXT,
    ADD COLUMN IF NOT EXISTS value_stream_id TEXT;
ALTER TABLE compliance.communication_adapter_registry_mirror
    ADD COLUMN IF NOT EXISTS handoff_cost_band TEXT,
    ADD COLUMN IF NOT EXISTS value_stream_id TEXT;
ALTER TABLE compliance.scheduling_adapter_registry_mirror
    ADD COLUMN IF NOT EXISTS handoff_cost_band TEXT,
    ADD COLUMN IF NOT EXISTS value_stream_id TEXT;
ALTER TABLE compliance.contract_adapter_registry_mirror
    ADD COLUMN IF NOT EXISTS handoff_cost_band TEXT,
    ADD COLUMN IF NOT EXISTS value_stream_id TEXT;
ALTER TABLE compliance.rpa_adapter_registry_mirror
    ADD COLUMN IF NOT EXISTS handoff_cost_band TEXT,
    ADD COLUMN IF NOT EXISTS value_stream_id TEXT;

COMMIT;
