-- Parity: scripts/sql/i19_phase1_staging/20260423_i19_finops_ledger_phase1_up.sql
-- Ledger version: 20260423014326 (remote schema_migrations after MCP apply; rename if drift)
-- Initiative 19 Phase 1 — finops.registered_fact skeleton

CREATE SCHEMA IF NOT EXISTS finops;
COMMENT ON SCHEMA finops IS
  'Gated monetary/contract facts (Initiative 19). Joins to FINOPS_COUNTERPARTY_REGISTER counterparty_id slugs and optional Stripe ids. Not git CSV SSOT; Stripe API remains payment truth.';

CREATE TABLE IF NOT EXISTS finops.registered_fact (
  id                     UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  counterparty_id        TEXT NOT NULL,
  stripe_customer_id     TEXT,
  stripe_subscription_id TEXT,
  fact_type              TEXT NOT NULL,
  currency               TEXT NOT NULL DEFAULT 'USD',
  amount_minor           BIGINT,
  effective_date         DATE,
  metadata               JSONB NOT NULL DEFAULT '{}',
  source_reference       TEXT,
  created_at             TIMESTAMPTZ NOT NULL DEFAULT now()
);

COMMENT ON TABLE finops.registered_fact IS
  'Operator- or system-recorded facts (e.g. reconciliation snapshot, contract estimate). counterparty_id matches FINOPS_COUNTERPARTY_REGISTER.csv slug; no FK to compliance mirror.';
COMMENT ON COLUMN finops.registered_fact.amount_minor IS
  'Optional minor currency units (e.g. cents). Null when fact is non-amount metadata.';
COMMENT ON COLUMN finops.registered_fact.fact_type IS
  'Discriminator, e.g. reconciliation_snapshot, budget_line, contract_value_estimate.';

CREATE INDEX IF NOT EXISTS registered_fact_counterparty_idx
  ON finops.registered_fact (counterparty_id);
CREATE INDEX IF NOT EXISTS registered_fact_stripe_customer_idx
  ON finops.registered_fact (stripe_customer_id)
  WHERE stripe_customer_id IS NOT NULL;
CREATE INDEX IF NOT EXISTS registered_fact_fact_type_idx
  ON finops.registered_fact (fact_type);

ALTER TABLE finops.registered_fact ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS registered_fact_deny_authenticated ON finops.registered_fact;
DROP POLICY IF EXISTS registered_fact_deny_anon ON finops.registered_fact;
CREATE POLICY registered_fact_deny_authenticated
  ON finops.registered_fact FOR ALL TO authenticated USING (false);
CREATE POLICY registered_fact_deny_anon
  ON finops.registered_fact FOR ALL TO anon USING (false);

REVOKE ALL ON TABLE finops.registered_fact FROM PUBLIC;
GRANT ALL ON TABLE finops.registered_fact TO service_role;
