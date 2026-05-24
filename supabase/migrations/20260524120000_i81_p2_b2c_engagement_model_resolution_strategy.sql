-- Initiative 81 P2 Bundle B-2c (D-IH-81-X 2026-05-23) —
-- Extend compliance.engagement_model_registry_mirror with
-- counterparty_resolution_strategy (NOT NULL) + extend 4 enum CHECK
-- constraints (retribution_pattern, ip_clause_class, knowledge_access_level,
-- payment_cadence) to accommodate the 3 B-2c rows that extend the
-- people-taxonomy to a unified counterparty-routing taxonomy.
--
-- Operator ratifications (2026-05-23 inline-ratify batch):
--   b2c-enum-a   : NOT NULL col; 4 existing rows -> metadata_engagement_id,
--                  3 existing rows -> manual_review.
--   b2c-rows-c   : Mint 3 new rows — eng_model_saas_subscription (active),
--                  eng_model_rpp_vendor (planned),
--                  eng_model_one_off_invoice (planned).
--   b2c-did-a    : Single closure decision D-IH-81-X.
--   b2c-uat-c    : Live deploy + UAT (Stripe live audit DEFERRED pending
--                  mcp_auth user-stripe).
--   b2c-docs-c   : Full docs sync.
--
-- SSOT remains
--   docs/references/hlk/v3.0/Admin/O5-1/People/People Operations/canonicals/dimensions/ENGAGEMENT_MODEL_REGISTRY.csv
-- (now 17 cols / 10 rows; Pydantic at akos/hlk_engagement_model_csv.py).
--
-- Cross-doctrine: counterparty_resolution_strategy is the engagement-side
-- contract that the FINOPS resolver (supabase/functions/_shared/finops/
-- counterparty_resolver.ts; Pydantic VALID_RESOLUTION_STRATEGIES at
-- akos/hlk_finops_ledger.py L110-117) consumes when classifying a Stripe
-- event's counterparty resolution path. Per-row strategy lookup happens at
-- event-processing time via the engagement_model_id FK (Stripe metadata or
-- stripe_customer_link join).
--
-- Migration shape: ALTER ADD COLUMN with safe default -> per-row UPDATE/UPSERT
-- to backfill correct strategies -> ALTER DROP DEFAULT (NOT NULL invariant
-- preserved; future inserts MUST supply the column explicitly).

------------------------------------------------------------------------------
-- 1. ADD COLUMN with safe default (so existing 7 rows remain valid mid-ALTER)
------------------------------------------------------------------------------
ALTER TABLE compliance.engagement_model_registry_mirror
  ADD COLUMN IF NOT EXISTS counterparty_resolution_strategy TEXT
  NOT NULL DEFAULT 'manual_review';

------------------------------------------------------------------------------
-- 2. CHECK constraint on the new column
------------------------------------------------------------------------------
ALTER TABLE compliance.engagement_model_registry_mirror
  DROP CONSTRAINT IF EXISTS engagement_model_mirror_resolution_strategy_chk;
ALTER TABLE compliance.engagement_model_registry_mirror
  ADD CONSTRAINT engagement_model_mirror_resolution_strategy_chk
  CHECK (counterparty_resolution_strategy IN (
    'metadata_engagement_id',
    'metadata_billing_plane',
    'stripe_customer_link_lookup',
    'rpp_payout_attribution',
    'manual_review'
  ));

------------------------------------------------------------------------------
-- 3. Extend the 4 existing CHECK constraints to accommodate B-2c rows
--    (retribution_pattern +3 / ip_clause_class +3 /
--     knowledge_access_level +1 / payment_cadence +2). Pattern: DROP and
--    re-add with the extended frozenset.
------------------------------------------------------------------------------
ALTER TABLE compliance.engagement_model_registry_mirror
  DROP CONSTRAINT IF EXISTS engagement_model_mirror_retribution_pattern_chk;
ALTER TABLE compliance.engagement_model_registry_mirror
  ADD CONSTRAINT engagement_model_mirror_retribution_pattern_chk
  CHECK (retribution_pattern IN (
    'hourly',
    'milestone',
    'percentage',
    'barter_for_training',
    'equity_advisor',
    'hourly_low_trust',
    'operator_self',
    -- B-2c (D-IH-81-X) extensions:
    'subscription_recurring',
    'vendor_pass_through',
    'one_off_ad_hoc'
  ));

ALTER TABLE compliance.engagement_model_registry_mirror
  DROP CONSTRAINT IF EXISTS engagement_model_mirror_ip_clause_chk;
ALTER TABLE compliance.engagement_model_registry_mirror
  ADD CONSTRAINT engagement_model_mirror_ip_clause_chk
  CHECK (ip_clause_class IN (
    'standard_consultant',
    'milestone_handoff',
    'collaborator_share',
    'training_recipient',
    'advisor_nda',
    'outsourced_workproduct_only',
    'operator_owns_all',
    -- B-2c (D-IH-81-X) extensions:
    'saas_tos',
    'vendor_invoice_only',
    'none_required'
  ));

ALTER TABLE compliance.engagement_model_registry_mirror
  DROP CONSTRAINT IF EXISTS engagement_model_mirror_knowledge_access_chk;
ALTER TABLE compliance.engagement_model_registry_mirror
  ADD CONSTRAINT engagement_model_mirror_knowledge_access_chk
  CHECK (knowledge_access_level IN (
    'full_by_engagement',
    'partial_by_engagement',
    'training_curriculum_only',
    'work_product_scope_only',
    'full_internal',
    -- B-2c (D-IH-81-X) extensions:
    'none'
  ));

ALTER TABLE compliance.engagement_model_registry_mirror
  DROP CONSTRAINT IF EXISTS engagement_model_mirror_payment_cadence_chk;
ALTER TABLE compliance.engagement_model_registry_mirror
  ADD CONSTRAINT engagement_model_mirror_payment_cadence_chk
  CHECK (payment_cadence IN (
    'per_hour',
    'per_milestone',
    'per_deal_outcome',
    'barter_continuous',
    'per_round',
    'per_hour_capped',
    'none',
    -- B-2c (D-IH-81-X) extensions:
    'monthly_recurring',
    'per_invoice'
  ));

------------------------------------------------------------------------------
-- 4. Backfill the 7 existing rows per b2c-enum-a mapping
--    (4 -> metadata_engagement_id; 3 -> manual_review).
------------------------------------------------------------------------------
UPDATE compliance.engagement_model_registry_mirror
  SET counterparty_resolution_strategy = 'metadata_engagement_id'
  WHERE engagement_model_id IN (
    'eng_model_hourly_consultant',
    'eng_model_milestone_consultant',
    'eng_model_percentage_collaborator',
    'eng_model_outsourced_helper'
  );

UPDATE compliance.engagement_model_registry_mirror
  SET counterparty_resolution_strategy = 'manual_review'
  WHERE engagement_model_id IN (
    'eng_model_apprentice_learner',
    'eng_model_investor_advisor',
    'eng_model_operator_self'
  );

------------------------------------------------------------------------------
-- 5. UPSERT the 3 B-2c rows. UPSERT (not INSERT) because subsequent
--    sync_compliance_mirrors_from_csv.py runs are the canonical source-of-
--    truth refresh path; this seed makes the mirror immediately consistent
--    even before the first sync. source_git_sha is a placeholder; the sync
--    script overwrites it with the actual SHA of the row's source commit.
------------------------------------------------------------------------------
INSERT INTO compliance.engagement_model_registry_mirror (
  engagement_model_id,
  engagement_model_name,
  retribution_pattern,
  retribution_unit,
  typical_duration,
  access_level_default,
  soc_posture,
  ip_clause_class,
  knowledge_access_level,
  onboarding_pattern,
  offboarding_pattern,
  payment_cadence,
  legal_template_default,
  historical_examples,
  status,
  notes,
  counterparty_resolution_strategy,
  source_git_sha
)
VALUES
  (
    'eng_model_saas_subscription',
    'SaaS Subscription',
    'subscription_recurring',
    'subscription_period',
    'recurring_until_cancelled',
    0,
    'low_trust',
    'saas_tos',
    'none',
    'saas_signup_payment_method_capture',
    'subscription_cancellation_at_period_end',
    'monthly_recurring',
    'SaaS Terms of Service (no SoW)',
    'KiRBe product subscriptions (forward) + future Holistika SaaS surfaces',
    'active',
    'Counterparty is a SaaS customer (not a people-engagement); resolver routes via stripe_customer_link_lookup. Schema-extension row (B-2c / D-IH-81-X).',
    'stripe_customer_link_lookup',
    'b2c-migration-seed'
  ),
  (
    'eng_model_rpp_vendor',
    'Revenue Pass-Through Vendor',
    'vendor_pass_through',
    'vendor_invoice',
    'per_invoice_passed',
    0,
    'low_trust',
    'vendor_invoice_only',
    'none',
    'vendor_intake_per_invoice',
    'vendor_relationship_archive',
    'per_invoice',
    'vendor invoice acceptance (no SoW from Holistika side)',
    'Holistika receives vendor invoice + passes through to client (e.g. cloud infrastructure costs billed back to engagement client)',
    'planned',
    'Counterparty is a vendor whose invoice Holistika pays + bills through to a downstream client. Resolver=rpp_payout_attribution is FORWARD-CHARTER (not yet implemented in counterparty_resolver.ts); promote status=active when first real RPP invoice fires.',
    'rpp_payout_attribution',
    'b2c-migration-seed'
  ),
  (
    'eng_model_one_off_invoice',
    'One-off Ad-hoc Invoice',
    'one_off_ad_hoc',
    'invoice',
    'single_invoice_per_event',
    0,
    'low_trust',
    'none_required',
    'none',
    'minimal_intake_per_event',
    'event_archive',
    'per_invoice',
    'no template (ad-hoc free-form invoice)',
    'conference speaking fees / advisory honoraria outside formal investor_advisor / one-off product sales',
    'planned',
    'Counterparty is ad-hoc; resolver routes via metadata_billing_plane because no engagement context exists. Schema-extension row (B-2c / D-IH-81-X).',
    'metadata_billing_plane',
    'b2c-migration-seed'
  )
ON CONFLICT (engagement_model_id) DO UPDATE
  SET engagement_model_name             = EXCLUDED.engagement_model_name,
      retribution_pattern               = EXCLUDED.retribution_pattern,
      retribution_unit                  = EXCLUDED.retribution_unit,
      typical_duration                  = EXCLUDED.typical_duration,
      access_level_default              = EXCLUDED.access_level_default,
      soc_posture                       = EXCLUDED.soc_posture,
      ip_clause_class                   = EXCLUDED.ip_clause_class,
      knowledge_access_level            = EXCLUDED.knowledge_access_level,
      onboarding_pattern                = EXCLUDED.onboarding_pattern,
      offboarding_pattern               = EXCLUDED.offboarding_pattern,
      payment_cadence                   = EXCLUDED.payment_cadence,
      legal_template_default            = EXCLUDED.legal_template_default,
      historical_examples               = EXCLUDED.historical_examples,
      status                            = EXCLUDED.status,
      notes                             = EXCLUDED.notes,
      counterparty_resolution_strategy  = EXCLUDED.counterparty_resolution_strategy,
      source_git_sha                    = EXCLUDED.source_git_sha,
      synced_at                         = now();

------------------------------------------------------------------------------
-- 6. DROP DEFAULT — future inserts MUST supply the column explicitly.
--    NOT NULL invariant preserved by step 1 (already enforced).
------------------------------------------------------------------------------
ALTER TABLE compliance.engagement_model_registry_mirror
  ALTER COLUMN counterparty_resolution_strategy DROP DEFAULT;

------------------------------------------------------------------------------
-- 7. Index on the new column (resolver lookups filter by strategy class).
------------------------------------------------------------------------------
CREATE INDEX IF NOT EXISTS engagement_model_mirror_resolution_strategy_idx
  ON compliance.engagement_model_registry_mirror (counterparty_resolution_strategy);

------------------------------------------------------------------------------
-- 8. Update governance.engagement_model_registry_view to surface the new col.
--    Postgres CREATE OR REPLACE VIEW only allows appending columns at the END
--    (column-order changes raise SQLSTATE 42P16). So we append
--    counterparty_resolution_strategy AFTER synced_at — view-column ordering
--    is cosmetic; consumers reference by name not position.
------------------------------------------------------------------------------
CREATE OR REPLACE VIEW governance.engagement_model_registry_view AS
SELECT
  engagement_model_id,
  engagement_model_name,
  retribution_pattern,
  retribution_unit,
  typical_duration,
  access_level_default,
  soc_posture,
  ip_clause_class,
  knowledge_access_level,
  onboarding_pattern,
  offboarding_pattern,
  payment_cadence,
  legal_template_default,
  historical_examples,
  status,
  notes,
  synced_at,
  counterparty_resolution_strategy
FROM compliance.engagement_model_registry_mirror
WHERE status = 'active';

COMMENT ON VIEW governance.engagement_model_registry_view IS
  'Initiative 73 P1 + I81 P2 B-2c (D-IH-81-X) — operator-facing engagement-model taxonomy view (status=active only). Adds counterparty_resolution_strategy column to support FINOPS resolver lookups (akos/hlk_finops_ledger.py VALID_RESOLUTION_STRATEGIES). Consumed by P7 hlk-erp KB-view panel filter routes (operator-managed / cleared-collaborator / low-trust-outsourced / apprentice / saas-subscription).';

COMMENT ON COLUMN compliance.engagement_model_registry_mirror.counterparty_resolution_strategy IS
  'B-2c (D-IH-81-X) — per-engagement-model contract that the FINOPS counterparty resolver consumes when classifying a Stripe event. Values: metadata_engagement_id (HIGH confidence) / metadata_billing_plane (MEDIUM) / stripe_customer_link_lookup (LOW) / rpp_payout_attribution (FORWARD-CHARTER) / manual_review. Lockstep with akos/hlk_finops_ledger.py VALID_RESOLUTION_STRATEGIES + supabase/functions/_shared/finops/counterparty_resolver.ts.';
