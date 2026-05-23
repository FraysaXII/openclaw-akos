-- Parity: this is the canonical DDL — no staging file precedes it (Bundle B-2a is greenfield substrate per D-IH-81-V).
-- Ledger version: 20260524000000 (rename on apply if remote schema_migrations drifts).
-- Initiative 81 Phase 2 Bundle B-2a (substrate) — D-IH-81-V under D-IH-81-G umbrella, 2026-05-23.
-- Operator inline-ratify ratification 2026-05-23 (R1-a + R2-a + R3-a + R4-a + R5-triple per Bundle B-2 architecture report).
--
-- Purpose: stand up the FINOPS writer substrate so the Stripe → finops.registered_fact pipeline
-- can write monetary facts with industry-standard webhook idempotency (Layer 1 raw events) +
-- async DLQ worker (Layer 2 pgmq queue + dead-letter queue) + FX dual-source snapshot
-- (Layer 3 ECB-authoritative + Stripe FX Quote sidecar) + ENGAGEMENT_MODEL-aware counterparty
-- resolution. See docs/wip/planning/81-vault-integrity-layout-milestones-retrofit/reports/p2-bundle-b2-architecture-2026-05-23.md
-- §3 + §5 for the full architecture rationale + file inventory.
--
-- This migration is part of Bundle B-2 TRIPLE split (B-2a = DDL+Pydantic; B-2b = Edge Functions+worker; B-2c = CSV writes + governance close).
-- B-2b will add the Edge Functions (fx-rate-cache-refresh + finops-writer-worker + stripe-webhook-handler FINOPS branch).
-- B-2c will add the ENGAGEMENT_MODEL_REGISTRY rows (eng_model_saas_subscription + eng_model_rpp_vendor) + close governance.

-- =============================================================================
-- §1 — pgmq extension (per D-IH-81-V Recommendation 3; replaces ad-hoc DLQ table from initial design)
-- =============================================================================

CREATE EXTENSION IF NOT EXISTS pgmq;
COMMENT ON EXTENSION pgmq IS
  'Supabase pgmq extension — Postgres-native message queue used as FINOPS writer queue + dead-letter queue. Per I81 P2 B-2a (D-IH-81-V), industry-standard webhook idempotency pattern (Hookdeck / Smee / Stripe-recommended retry posture).';

-- Create the writer queue (idempotent — pgmq.create raises if exists; suppress via DO block).
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_class WHERE relname = 'q_finops_writer_queue') THEN
    PERFORM pgmq.create('finops_writer_queue');
  END IF;
END$$;

DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_class WHERE relname = 'q_finops_writer_dlq') THEN
    PERFORM pgmq.create('finops_writer_dlq');
  END IF;
END$$;

-- =============================================================================
-- §2 — holistika_ops.stripe_events (raw event log; idempotency Layer 1)
-- =============================================================================
-- Pattern: store the raw Stripe event payload immediately on webhook receipt + return 200 fast.
-- Idempotency key = stripe_event_id (unique). Async worker drains pgmq queue → writes to finops.
-- Survives webhook restarts, async processing failures, replay-from-DLQ scenarios.

CREATE SCHEMA IF NOT EXISTS holistika_ops;

CREATE TABLE IF NOT EXISTS holistika_ops.stripe_events (
  stripe_event_id   TEXT PRIMARY KEY,                          -- Stripe-assigned event id; idempotency key
  event_type        TEXT NOT NULL,                             -- e.g. invoice.paid, charge.succeeded, customer.subscription.created
  api_version       TEXT,                                      -- Stripe API version from event payload
  livemode          BOOLEAN NOT NULL DEFAULT false,            -- true = production Stripe, false = test/dev (Stripe AT)
  request_id        TEXT,                                      -- Stripe request idempotency id (if present)
  raw_payload       JSONB NOT NULL,                            -- full event payload (audit + replay)
  received_at       TIMESTAMPTZ NOT NULL DEFAULT now(),        -- webhook receipt timestamp
  processed_at      TIMESTAMPTZ,                               -- set when worker successfully writes to finops + dequeues
  process_attempts  INTEGER NOT NULL DEFAULT 0,                -- worker increments on each attempt
  last_error        TEXT,                                      -- last error message from worker (NULL on success)
  fx_rate_ecb       NUMERIC(18, 8),                            -- snapshot at receive time (per D-IH-81-V Recommendation 2)
  fx_rate_stripe    NUMERIC(18, 8),                            -- Stripe FX Quote API (audit sidecar)
  fx_source         TEXT                                       -- 'ecb_daily' / 'stripe_fx_quote' / 'previous_day_ecb' (fallback ladder)
);

COMMENT ON TABLE holistika_ops.stripe_events IS
  'Idempotency Layer 1 — raw Stripe webhook event log. Webhook handler MUST insert here first (ON CONFLICT DO NOTHING via stripe_event_id), then enqueue to pgmq.finops_writer_queue, then return 200. Worker drains queue + writes to finops.registered_fact. Pattern per D-IH-81-V Recommendation 3 (industry-standard webhook idempotency).';
COMMENT ON COLUMN holistika_ops.stripe_events.stripe_event_id IS
  'Stripe-assigned event id. PRIMARY KEY = idempotency lock. ON CONFLICT DO NOTHING on insert handles duplicate Stripe retries.';
COMMENT ON COLUMN holistika_ops.stripe_events.processed_at IS
  'NULL = pending or in-flight. NOT NULL = worker successfully wrote to finops.registered_fact AND dequeued from pgmq. Drives DLQ inspection: rows with processed_at IS NULL AND process_attempts >= N indicate stuck events.';
COMMENT ON COLUMN holistika_ops.stripe_events.fx_rate_ecb IS
  'Captured at receive time so worker can compute amount_minor_eur deterministically even if ECB cache refresh races. Set by webhook handler from holistika_ops.fx_rate_cache lookup; NULL on EUR-native events.';

CREATE INDEX IF NOT EXISTS stripe_events_event_type_idx
  ON holistika_ops.stripe_events (event_type);
CREATE INDEX IF NOT EXISTS stripe_events_pending_idx
  ON holistika_ops.stripe_events (received_at)
  WHERE processed_at IS NULL;
CREATE INDEX IF NOT EXISTS stripe_events_dlq_candidate_idx
  ON holistika_ops.stripe_events (process_attempts, received_at)
  WHERE processed_at IS NULL AND process_attempts >= 3;

ALTER TABLE holistika_ops.stripe_events ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS stripe_events_deny_authenticated ON holistika_ops.stripe_events;
DROP POLICY IF EXISTS stripe_events_deny_anon ON holistika_ops.stripe_events;
CREATE POLICY stripe_events_deny_authenticated
  ON holistika_ops.stripe_events FOR ALL TO authenticated USING (false);
CREATE POLICY stripe_events_deny_anon
  ON holistika_ops.stripe_events FOR ALL TO anon USING (false);
REVOKE ALL ON TABLE holistika_ops.stripe_events FROM PUBLIC;
GRANT ALL ON TABLE holistika_ops.stripe_events TO service_role;

-- =============================================================================
-- §3 — holistika_ops.fx_rate_cache (ECB daily rate cache; per D-IH-81-V Recommendation 2)
-- =============================================================================
-- Pattern: Edge Function fx-rate-cache-refresh runs daily at 17:00 CET (cron), fetches ECB XML,
-- upserts one row per currency pair per business day. Webhook handlers + worker look up by
-- (currency, effective_date) for deterministic EUR conversion. Authoritative source = ECB
-- (European Central Bank daily reference rates). Stripe FX Quote captured in sidecar column
-- on registered_fact for audit / divergence detection.

CREATE TABLE IF NOT EXISTS holistika_ops.fx_rate_cache (
  currency_pair     TEXT NOT NULL,                             -- e.g. 'USD/EUR' (always quote-to-base = source currency to EUR)
  effective_date    DATE NOT NULL,                             -- business day this rate is authoritative for
  rate              NUMERIC(18, 8) NOT NULL,                   -- ECB daily rate (1 unit source currency = N units EUR)
  source            TEXT NOT NULL DEFAULT 'ecb_daily',         -- 'ecb_daily' / 'ecb_previous_day_fallback' / 'manual_override' (operator)
  source_url        TEXT,                                      -- e.g. ECB XML feed URL at fetch time
  fetched_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (currency_pair, effective_date)
);

COMMENT ON TABLE holistika_ops.fx_rate_cache IS
  'ECB-authoritative daily FX cache. Refreshed by Edge Function fx-rate-cache-refresh (B-2b) on cron schedule 17:00 CET. Per D-IH-81-V Recommendation 2, correcting the initial assumption that Stripe Charge.exchange_rate was a reliable source — Stripe FX rates differ from ECB; only ECB is authoritative for finops.registered_fact.amount_minor_eur.';
COMMENT ON COLUMN holistika_ops.fx_rate_cache.currency_pair IS
  'Format: SRC/EUR — always source currency to EUR base. Examples: USD/EUR, GBP/EUR, CHF/EUR. EUR/EUR row exists at rate=1.0 for code path uniformity.';
COMMENT ON COLUMN holistika_ops.fx_rate_cache.source IS
  'Provenance: ecb_daily (normal path) / ecb_previous_day_fallback (ECB feed failed; use yesterday rate per fallback ladder Tier-2) / manual_override (operator-set; emits OPS_REGISTER alert).';

CREATE INDEX IF NOT EXISTS fx_rate_cache_fetched_idx
  ON holistika_ops.fx_rate_cache (fetched_at DESC);

ALTER TABLE holistika_ops.fx_rate_cache ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS fx_rate_cache_deny_authenticated ON holistika_ops.fx_rate_cache;
DROP POLICY IF EXISTS fx_rate_cache_deny_anon ON holistika_ops.fx_rate_cache;
CREATE POLICY fx_rate_cache_deny_authenticated
  ON holistika_ops.fx_rate_cache FOR ALL TO authenticated USING (false);
CREATE POLICY fx_rate_cache_deny_anon
  ON holistika_ops.fx_rate_cache FOR ALL TO anon USING (false);
REVOKE ALL ON TABLE holistika_ops.fx_rate_cache FROM PUBLIC;
GRANT ALL ON TABLE holistika_ops.fx_rate_cache TO service_role;

-- Seed EUR/EUR row at rate 1.0 (every FX conversion needs the identity entry for code uniformity).
INSERT INTO holistika_ops.fx_rate_cache (currency_pair, effective_date, rate, source, source_url)
VALUES ('EUR/EUR', CURRENT_DATE, 1.00000000, 'identity_seed', NULL)
ON CONFLICT (currency_pair, effective_date) DO NOTHING;

-- =============================================================================
-- §4 — finops.registered_fact column extensions (FX dual-source + EUR amount)
-- =============================================================================
-- Extends the I19 Phase 1 finops.registered_fact table with 4 new columns to support the FX
-- snapshot pattern. Idempotent (ADD COLUMN IF NOT EXISTS); safe on re-apply. Worker fills these
-- columns when writing facts; ECB rate is authoritative for amount_minor_eur, Stripe FX Quote
-- is captured as audit sidecar to detect divergence (R3 risk in p2-bundle-b2-architecture report).

ALTER TABLE finops.registered_fact
  ADD COLUMN IF NOT EXISTS amount_minor_eur BIGINT,
  ADD COLUMN IF NOT EXISTS fx_rate_ecb      NUMERIC(18, 8),
  ADD COLUMN IF NOT EXISTS fx_rate_stripe   NUMERIC(18, 8),
  ADD COLUMN IF NOT EXISTS fx_source        TEXT;

COMMENT ON COLUMN finops.registered_fact.amount_minor_eur IS
  'EUR-equivalent of amount_minor at effective_date, computed using fx_rate_ecb (authoritative). NULL when fact is non-amount metadata OR when currency = EUR (in which case = amount_minor by identity). Per D-IH-81-V Recommendation 2.';
COMMENT ON COLUMN finops.registered_fact.fx_rate_ecb IS
  'ECB daily reference rate at effective_date used to compute amount_minor_eur. Sourced from holistika_ops.fx_rate_cache lookup at worker write-time. NULL when currency = EUR.';
COMMENT ON COLUMN finops.registered_fact.fx_rate_stripe IS
  'Stripe FX Quote API rate at effective_date (audit sidecar; per D-IH-81-V Recommendation 2). Divergence from fx_rate_ecb beyond tolerance emits OPS_REGISTER row for operator review (per Recommendation 4 HLK-ERP convergence).';
COMMENT ON COLUMN finops.registered_fact.fx_source IS
  'Provenance enum: ecb_daily (normal) / ecb_previous_day_fallback (ECB feed stale) / stripe_fx_quote (ECB unavailable) / manual_override (operator). Drives DLQ observability.';

-- =============================================================================
-- §5 — Service-role grant on compliance.ops_register_mirror (HLK-ERP convergence per R4)
-- =============================================================================
-- Per D-IH-81-V Recommendation 4 (HLK-ERP convergence): finops-writer-worker emits OPS_REGISTER
-- rows on DLQ alert + FX divergence + counterparty resolution failure. The compliance mirror
-- table already exists (I21 P4); this grants service_role INSERT capability so the worker
-- can append rows. Operator-facing OPERATOR_INBOX.md auto-renders from OPS_REGISTER.csv per
-- existing scripts/render_operator_inbox.py pipeline.

DO $$
BEGIN
  IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'compliance' AND table_name = 'ops_register_mirror') THEN
    EXECUTE 'GRANT INSERT ON TABLE compliance.ops_register_mirror TO service_role';
    EXECUTE 'GRANT SELECT ON TABLE compliance.ops_register_mirror TO service_role';
  END IF;
END$$;

-- =============================================================================
-- Migration end — Bundle B-2a substrate complete.
-- Next: Bundle B-2b (Edge Functions + worker) per D-IH-81-W. See architecture report §5.
-- =============================================================================
