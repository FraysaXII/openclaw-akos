-- Initiative 86 Wave R+2 Commit 6 — compliance.collaborator_share_*_mirror
-- enum amendment: 3-shape → 4-base + 1-overlay model + methodology-readiness
-- gating axis + parallel_invoice_stream_indicator + overlay_pct_deviation.
--
-- Per D-IH-86-EJ (4-base + 1-overlay share_pattern model; supersedes D-IH-86-DE)
--   + D-IH-86-EK (parallel_invoice_stream_indicator axis)
--   + D-IH-86-EL (CS-09 overlay-base + methodology-pattern coherence;
--     supersedes D-IH-86-EG)
--   + D-IH-86-EM (CS-03 unified across-rows sum-to-100 invariant +
--     CS-04 composition-branching defaults)
--   + D-IH-86-EN (methodology-readiness 4-value axis gating per-pattern
--     eligibility).
--
-- Forward-migration: this is an ALTER TABLE pass, NOT a fresh CREATE TABLE.
-- The pre-rewrite mirror DDL (20260525000000_i86_waveRplus1_commit2b_
-- collaborator_share_mirrors.sql) stays in the migration ledger; this
-- migration mutates it in place.
--
-- Sequencing contract: this migration MUST land BEFORE the next
-- sync_compliance_mirrors_from_csv.py --collaborator-share-only invocation
-- because Wave R+2 Commit 5 (sha 17a5db7) already migrated the canonical
-- COLLABORATOR_SHARE_REGISTRY.csv rows to the new 20-column shape (added
-- columns share_overlay + methodology_readiness +
-- parallel_invoice_stream_indicator + retired
-- orchestration_broker_thin_margin enum value) AND the
-- COLLABORATOR_RATE_OVERRIDES.csv to the 3-value override_kind enum.
-- Without this DDL pass, the sync emit will fail on UNDEFINED column /
-- CHECK constraint violation.
--
-- Pre-existing rows: the AISHA-CONTINUITY SHARE_REGISTRY row authored at
-- D-IH-86-DA mint already lives in the mirror at share_pattern =
-- deep_partner_65_35 (preserved in the new enum) with no overlay and
-- methodology_readiness defaulting to 'methodology_trained' (Aïsha is
-- internal-pool partner per D-IH-86-EH framing). The 3 retired SUEZ
-- orchestration_broker rows have ALREADY been deleted from the canonical
-- CSV at Commit 5; the next sync_compliance_mirrors invocation will
-- DELETE the corresponding mirror rows via the standard upsert protocol.
--
-- Server-only (service_role) RLS posture preserved; CHECK constraints
-- mirror the Pydantic Literal enums in akos/hlk_collaborator_share.py +
-- the rewritten doctrine §2.3 + §2.4 + §6 (D-IH-86-EJ..EN).
--
-- INFO ramp continues at Wave R+2; FAIL promotion gated on 3 worked
-- examples per doctrine §9 Stage 2 (1 already PASS = AISHA-CONTINUITY;
-- pending: SUEZ recommercialised settlement at engagement-close +
-- Websitz engagement deep_partner_65_35 first settlement).

BEGIN;

-- ============================================================================
-- 1. compliance.collaborator_share_registry_mirror
--    Drop superseded CHECK constraints; add 3 new columns; add new CHECKs
--    mirroring the 4-base + 1-overlay model + methodology-readiness axis.
-- ============================================================================

-- ---- 1.1 Drop pre-rewrite CHECK constraints ---------------------------------

-- D-IH-86-DE 3-value enum → superseded by D-IH-86-EJ 4-value enum.
ALTER TABLE compliance.collaborator_share_registry_mirror
    DROP CONSTRAINT IF EXISTS share_registry_share_pattern_chk;

-- D-IH-86-DE per-pattern sum-to-100 invariant → superseded by D-IH-86-EM
-- unified across-rows CS-03 invariant (cannot be expressed as row-local
-- CHECK because it requires aggregation over all rows in an engagement).
-- The row-local sanity (0..100 per column) is retained via the surviving
-- share_registry_holistika_pct_chk + share_registry_collaborator_pct_chk.
ALTER TABLE compliance.collaborator_share_registry_mirror
    DROP CONSTRAINT IF EXISTS share_registry_splits_sum_to_100_chk;

-- D-IH-86-DE per-pattern default-split + override audit → superseded by
-- D-IH-86-EM composition-branching defaults (4 base patterns + overlay).
ALTER TABLE compliance.collaborator_share_registry_mirror
    DROP CONSTRAINT IF EXISTS share_registry_default_split_or_override_chk;

-- ---- 1.2 Add 3 new columns --------------------------------------------------

-- D-IH-86-EJ: overlay tag (nullable; only bd_commission_overlay enum value
-- supported at Wave R+2). When non-null, the row is a stackable overlay
-- sitting beside a base-pattern sibling row at the same engagement_id.
ALTER TABLE compliance.collaborator_share_registry_mirror
    ADD COLUMN IF NOT EXISTS share_overlay text;

-- D-IH-86-EN: methodology-readiness state of the collaborator. Gates
-- which share_pattern values are eligible per
-- METHODOLOGY_READINESS_PERMISSIBLE_PATTERNS in akos/hlk_collaborator_share.py.
-- NOT NULL with a defensive default of 'methodology_not_applicable' for
-- back-fill of pre-rewrite rows; operator should re-classify in the next
-- review cycle. CS-09 audit fires WARN on pre-rewrite rows still carrying
-- the default after Wave R+3 close (forward-charter).
ALTER TABLE compliance.collaborator_share_registry_mirror
    ADD COLUMN IF NOT EXISTS methodology_readiness text
        NOT NULL DEFAULT 'methodology_not_applicable';

-- D-IH-86-EK: parallel-invoice-stream indicator. TRUE when the row's
-- collaborator invoices the end-customer directly (parallel to
-- Holistika's invoice stream); FALSE when revenue flows through
-- Holistika first and is then re-distributed per the share_pattern.
-- Used by settlement runbook to skip TRUE-MARGIN benefits computation
-- for parallel-stream rows (the collaborator carries their own
-- counterparty risk + tax-treatment). Defensive default FALSE
-- preserves pre-rewrite semantics.
ALTER TABLE compliance.collaborator_share_registry_mirror
    ADD COLUMN IF NOT EXISTS parallel_invoice_stream_indicator boolean
        NOT NULL DEFAULT FALSE;

-- ---- 1.3 Add new CHECK constraints (4-base + 1-overlay model) ---------------

-- D-IH-86-EJ: 4-value base enum (3-value pre-rewrite enum superseded).
-- 'orchestration_broker_thin_margin' AND 'custom' are no longer valid;
-- pre-rewrite rows authored under either value MUST be migrated via the
-- Commit-5 supersede SQL (sha 17a5db7 already migrated the SUEZ rows;
-- the AISHA-CONTINUITY row stays at deep_partner_65_35 which is preserved).
ALTER TABLE compliance.collaborator_share_registry_mirror
    ADD CONSTRAINT share_registry_share_pattern_chk
        CHECK (share_pattern IN (
            'deep_partner_65_35',
            'bd_intro_only',
            'joint_venture_aventure',
            'consulting_direct'
        ));

-- D-IH-86-EJ: share_overlay enum membership. NULL = base row (no
-- overlay); non-NULL = stackable overlay row. Only 'bd_commission_overlay'
-- enum value supported at Wave R+2; future overlays (e.g.,
-- methodology_licensing_overlay; equity_kicker_overlay) would extend this
-- enum via successor decision rows.
ALTER TABLE compliance.collaborator_share_registry_mirror
    ADD CONSTRAINT share_registry_share_overlay_chk
        CHECK (
            share_overlay IS NULL
            OR share_overlay IN ('bd_commission_overlay')
        );

-- D-IH-86-EL CS-09 row-local mirror: when share_overlay is non-null, the
-- row's share_pattern must be in the valid base-pattern set for that
-- overlay (VALID_OVERLAY_BASE_PAIRINGS in
-- akos/hlk_collaborator_share.py). bd_commission_overlay pairs with
-- consulting_direct OR deep_partner_65_35 (not bd_intro_only, which
-- already has commission baked into its base; not joint_venture_aventure,
-- which is symmetric-bench by definition).
-- The engagement-level pairing audit (BASE row + OVERLAY row co-presence)
-- is enforced by validator CS-09 because SQL CHECK cannot express
-- across-rows aggregation.
ALTER TABLE compliance.collaborator_share_registry_mirror
    ADD CONSTRAINT share_registry_overlay_base_pairing_chk
        CHECK (
            share_overlay IS NULL
            OR (share_overlay = 'bd_commission_overlay'
                AND share_pattern IN ('consulting_direct', 'deep_partner_65_35'))
        );

-- D-IH-86-EN: methodology_readiness 4-value enum (mirrors
-- VALID_METHODOLOGY_READINESS in akos/hlk_collaborator_share.py).
ALTER TABLE compliance.collaborator_share_registry_mirror
    ADD CONSTRAINT share_registry_methodology_readiness_chk
        CHECK (methodology_readiness IN (
            'methodology_trained',
            'methodology_in_progress',
            'methodology_naive',
            'methodology_not_applicable'
        ));

-- D-IH-86-EN: methodology_readiness × share_pattern eligibility matrix
-- (mirrors METHODOLOGY_READINESS_PERMISSIBLE_PATTERNS in
-- akos/hlk_collaborator_share.py). Prevents "35% compromise to bridge a
-- methodology gap" failure mode operator named explicitly 2026-05-26.
--   - methodology_trained: all 4 base patterns
--   - methodology_in_progress: excludes joint_venture_aventure (symmetric
--     framing requires equal bench)
--   - methodology_naive: excludes deep_partner_65_35 (35% share requires
--     methodology contribution) AND joint_venture_aventure
--   - methodology_not_applicable: same restriction as naive (one-time
--     BD-only introducers; not expected to learn methodology)
ALTER TABLE compliance.collaborator_share_registry_mirror
    ADD CONSTRAINT share_registry_methodology_pattern_compat_chk
        CHECK (
            (methodology_readiness = 'methodology_trained')
            OR (methodology_readiness = 'methodology_in_progress'
                AND share_pattern IN (
                    'deep_partner_65_35',
                    'bd_intro_only',
                    'consulting_direct'
                ))
            OR (methodology_readiness IN ('methodology_naive', 'methodology_not_applicable')
                AND share_pattern IN (
                    'bd_intro_only',
                    'consulting_direct'
                ))
        );

-- D-IH-86-EM CS-04 row-local mirror: per-pattern default anchor with
-- override-FK fallback. The across-rows aggregate audit (CS-03 unified
-- sum-to-100) lives in the validator because SQL CHECK cannot express it.
--
-- Per-row anchors per the rewritten doctrine §3 worked examples:
--   - deep_partner_65_35: (Hol 65, Col 35) per-row OR override FK (Websitz)
--   - bd_intro_only: (Hol 85, Col 0) BASE row OR (Hol 0, Col 15) BD row
--     OR override FK (forward-charter)
--   - joint_venture_aventure: (Hol 50, Col 0) Hol row OR (Hol 0, Col 50)
--     partner row OR override FK (forward-charter)
--   - consulting_direct: (Hol 100, Col 0) solo OR (Hol 85, Col 0) base
--     with overlay sibling OR (Hol 0, Col 15) overlay row (must carry
--     share_overlay = 'bd_commission_overlay') OR override FK (SUEZ
--     instantiates this pattern's base + overlay at C5)
ALTER TABLE compliance.collaborator_share_registry_mirror
    ADD CONSTRAINT share_registry_default_split_or_override_chk
        CHECK (
            (share_pattern = 'deep_partner_65_35'
                AND (
                    (holistika_share_pct = 65 AND collaborator_share_pct = 35)
                    OR (share_override_decision_id IS NOT NULL
                        AND length(share_override_decision_id) > 0)
                ))
            OR (share_pattern = 'bd_intro_only'
                AND (
                    (holistika_share_pct = 85 AND collaborator_share_pct = 0)
                    OR (holistika_share_pct = 0 AND collaborator_share_pct = 15)
                    OR (share_override_decision_id IS NOT NULL
                        AND length(share_override_decision_id) > 0)
                ))
            OR (share_pattern = 'joint_venture_aventure'
                AND (
                    (holistika_share_pct = 50 AND collaborator_share_pct = 0)
                    OR (holistika_share_pct = 0 AND collaborator_share_pct = 50)
                    OR (share_override_decision_id IS NOT NULL
                        AND length(share_override_decision_id) > 0)
                ))
            OR (share_pattern = 'consulting_direct'
                AND (
                    -- solo: 100/0
                    (holistika_share_pct = 100 AND collaborator_share_pct = 0)
                    -- base with overlay sibling: 85/0
                    OR (holistika_share_pct = 85 AND collaborator_share_pct = 0
                        AND share_overlay IS NULL)
                    -- overlay row: 0/15 (must carry share_overlay tag)
                    OR (holistika_share_pct = 0 AND collaborator_share_pct = 15
                        AND share_overlay = 'bd_commission_overlay')
                    OR (share_override_decision_id IS NOT NULL
                        AND length(share_override_decision_id) > 0)
                ))
        );

-- ---- 1.4 Add new indexes for the 3 new columns ------------------------------

CREATE INDEX IF NOT EXISTS share_registry_share_overlay_idx
    ON compliance.collaborator_share_registry_mirror (share_overlay)
    WHERE share_overlay IS NOT NULL;

CREATE INDEX IF NOT EXISTS share_registry_methodology_readiness_idx
    ON compliance.collaborator_share_registry_mirror (methodology_readiness);

CREATE INDEX IF NOT EXISTS share_registry_parallel_invoice_idx
    ON compliance.collaborator_share_registry_mirror (parallel_invoice_stream_indicator)
    WHERE parallel_invoice_stream_indicator = TRUE;

-- ---- 1.5 Update column + table comments to reflect Wave R+2 doctrine --------

COMMENT ON TABLE compliance.collaborator_share_registry_mirror IS
    'I86 Wave R+2 Commit 6 (D-IH-86-EJ..EN): per-(engagement, collaborator) revenue-share row; mirrors COLLABORATOR_SHARE_REGISTRY.csv canonical per COLLABORATOR_SHARE_DOCTRINE.md §2.3 (rewritten). 4-base + 1-overlay model: deep_partner_65_35 (Websitz; 65/35 per-row) | bd_intro_only (BD commission 15% across 2 rows; 85/15 aggregate) | joint_venture_aventure (50/50 symmetric across 2 rows) | consulting_direct (100/0 solo OR 85/0 base + 0/15 bd_commission_overlay row across 2 rows; SUEZ instantiates this with overlay). Methodology-readiness axis (D-IH-86-EN) gates per-pattern eligibility. CS-03 unified across-rows sum-to-100 invariant lives in validator; per-row anchors enforced by share_registry_default_split_or_override_chk.';

COMMENT ON COLUMN compliance.collaborator_share_registry_mirror.share_pattern IS
    'D-IH-86-EJ (supersedes D-IH-86-DE): top-level economic-model classifier. 4-value enum mirrors VALID_SHARE_PATTERNS in akos/hlk_collaborator_share.py. Pre-rewrite values orchestration_broker_thin_margin AND custom RETIRED; consulting_direct + bd_commission_overlay overlay replaces orchestration_broker; custom-shape engagements forward-chartered to a future share_pattern enum extension.';

COMMENT ON COLUMN compliance.collaborator_share_registry_mirror.share_overlay IS
    'D-IH-86-EJ: stackable overlay tag. NULL = base row (most rows); non-NULL = stackable overlay sitting beside a base-pattern sibling at the same engagement_id. Only bd_commission_overlay supported at Wave R+2; future overlays (methodology_licensing / equity_kicker) would extend the enum via successor decision rows. CS-09 audit (validator) enforces engagement-level base+overlay co-presence + pairing-table compatibility.';

COMMENT ON COLUMN compliance.collaborator_share_registry_mirror.methodology_readiness IS
    'D-IH-86-EN: collaborator''s methodology-readiness state. Gates which share_pattern values are eligible per METHODOLOGY_READINESS_PERMISSIBLE_PATTERNS in akos/hlk_collaborator_share.py. Defensive default ''methodology_not_applicable'' for back-fill of pre-rewrite rows; operator re-classifies in next review cycle. CS-09 row-local CHECK (share_registry_methodology_pattern_compat_chk) prevents committing to share_patterns the collaborator structurally cannot fulfil. Forward-charter: D-IH-86-EO will audit pre-rewrite rows still carrying the default after Wave R+3 close.';

COMMENT ON COLUMN compliance.collaborator_share_registry_mirror.parallel_invoice_stream_indicator IS
    'D-IH-86-EK: TRUE when collaborator invoices end-customer directly (parallel to Holistika''s invoice stream); FALSE when revenue flows through Holistika first and is then re-distributed per the share_pattern. Used by settlement runbook (scripts/collaborator_share_calculate.py) to skip TRUE-MARGIN benefits computation for parallel-stream rows (collaborator carries own counterparty risk + tax treatment). Defensive default FALSE preserves pre-rewrite semantics; operator flips to TRUE on new rows that match the SUEZ → EFA invoice topology.';


-- ============================================================================
-- 2. compliance.collaborator_rate_overrides_mirror
--    Update override_kind enum: 2-value → 3-value (add overlay_pct_deviation).
-- ============================================================================

-- D-IH-86-DE 2-value enum → superseded by D-IH-86-EJ 3-value enum.
ALTER TABLE compliance.collaborator_rate_overrides_mirror
    DROP CONSTRAINT IF EXISTS rate_overrides_override_kind_chk;

-- D-IH-86-EJ: 3-value override_kind enum (mirrors VALID_OVERRIDE_KINDS in
-- akos/hlk_collaborator_share.py). overlay_pct_deviation is NEW at Wave
-- R+2: when a bd_commission_overlay row deviates from its
-- DEFAULT_BD_COMMISSION_OVERLAY_PCT (15) anchor, the override row carries
-- this kind to make the deviation auditable separately from the base row's
-- share_split_deviation. Allows independent audit + commercial-rationale
-- tracking for overlay-side commission excursions.
ALTER TABLE compliance.collaborator_rate_overrides_mirror
    ADD CONSTRAINT rate_overrides_override_kind_chk
        CHECK (override_kind IN (
            'market_rate_excursion',
            'share_split_deviation',
            'overlay_pct_deviation'
        ));

COMMENT ON TABLE compliance.collaborator_rate_overrides_mirror IS
    'I86 Wave R+2 Commit 6 (D-IH-86-EJ): governed commercial deviations from market-rate-reference, default-split, or overlay-pct anchor; mirrors COLLABORATOR_RATE_OVERRIDES.csv canonical per the rewritten COLLABORATOR_SHARE_DOCTRINE.md §2.4. THREE override_kinds: market_rate_excursion (rate outside ±25% market-rate band; covers CS-04) + share_split_deviation (base-row split deviates from per-pattern default anchor; covers CS-03/CS-04) + overlay_pct_deviation (NEW per D-IH-86-EJ: bd_commission_overlay row deviates from 15% anchor; covers CS-09 overlay-side audit). All three require ratifying_decision_id FK to DECISION_REGISTER + commercial_strategy_rationale narrative + optional expires_at for time-boxed deviations.';


COMMIT;

-- ============================================================================
-- Rollback (per supabase/migrations/README.md operator runbook)
-- ============================================================================
-- This rollback reverts compliance.collaborator_share_registry_mirror +
-- compliance.collaborator_rate_overrides_mirror to their Wave R+1 Commit 2b
-- shape (3-value share_pattern enum + 2-value override_kind enum + no
-- share_overlay/methodology_readiness/parallel_invoice_stream_indicator
-- columns). Only run AFTER:
--   (a) Reverting CSV rows back to pre-Commit 5 shape (revert sha 17a5db7).
--   (b) Truncating any rows that depend on the new columns (verify no
--       overlay rows exist; verify no overlay_pct_deviation overrides exist;
--       verify no methodology_readiness != 'methodology_not_applicable' rows).
-- Operator runs sync_compliance_mirrors_from_csv.py --collaborator-share-only
-- AFTER rollback to refresh mirror state from CSV.
--
-- BEGIN;
-- -- 1. collaborator_share_registry_mirror rollback
-- ALTER TABLE compliance.collaborator_share_registry_mirror
--     DROP CONSTRAINT IF EXISTS share_registry_default_split_or_override_chk;
-- ALTER TABLE compliance.collaborator_share_registry_mirror
--     DROP CONSTRAINT IF EXISTS share_registry_methodology_pattern_compat_chk;
-- ALTER TABLE compliance.collaborator_share_registry_mirror
--     DROP CONSTRAINT IF EXISTS share_registry_methodology_readiness_chk;
-- ALTER TABLE compliance.collaborator_share_registry_mirror
--     DROP CONSTRAINT IF EXISTS share_registry_overlay_base_pairing_chk;
-- ALTER TABLE compliance.collaborator_share_registry_mirror
--     DROP CONSTRAINT IF EXISTS share_registry_share_overlay_chk;
-- ALTER TABLE compliance.collaborator_share_registry_mirror
--     DROP CONSTRAINT IF EXISTS share_registry_share_pattern_chk;
-- DROP INDEX IF EXISTS share_registry_share_overlay_idx;
-- DROP INDEX IF EXISTS share_registry_methodology_readiness_idx;
-- DROP INDEX IF EXISTS share_registry_parallel_invoice_idx;
-- ALTER TABLE compliance.collaborator_share_registry_mirror
--     DROP COLUMN IF EXISTS parallel_invoice_stream_indicator;
-- ALTER TABLE compliance.collaborator_share_registry_mirror
--     DROP COLUMN IF EXISTS methodology_readiness;
-- ALTER TABLE compliance.collaborator_share_registry_mirror
--     DROP COLUMN IF EXISTS share_overlay;
-- -- Recreate pre-rewrite CHECKs
-- ALTER TABLE compliance.collaborator_share_registry_mirror
--     ADD CONSTRAINT share_registry_share_pattern_chk
--         CHECK (share_pattern IN (
--             'deep_partner_65_35',
--             'orchestration_broker_thin_margin',
--             'custom'
--         ));
-- ALTER TABLE compliance.collaborator_share_registry_mirror
--     ADD CONSTRAINT share_registry_splits_sum_to_100_chk
--         CHECK (
--             share_pattern <> 'deep_partner_65_35'
--             OR (holistika_share_pct + collaborator_share_pct = 100)
--         );
-- ALTER TABLE compliance.collaborator_share_registry_mirror
--     ADD CONSTRAINT share_registry_default_split_or_override_chk
--         CHECK (
--             (share_pattern = 'deep_partner_65_35'
--                 AND (
--                     (holistika_share_pct = 65 AND collaborator_share_pct = 35)
--                     OR (share_override_decision_id IS NOT NULL
--                         AND length(share_override_decision_id) > 0)
--                 ))
--             OR (share_pattern = 'orchestration_broker_thin_margin'
--                 AND (
--                     holistika_share_pct = 6
--                     OR (share_override_decision_id IS NOT NULL
--                         AND length(share_override_decision_id) > 0)
--                 ))
--             OR (share_pattern = 'custom'
--                 AND share_override_decision_id IS NOT NULL
--                 AND length(share_override_decision_id) > 0)
--         );
--
-- -- 2. collaborator_rate_overrides_mirror rollback
-- ALTER TABLE compliance.collaborator_rate_overrides_mirror
--     DROP CONSTRAINT IF EXISTS rate_overrides_override_kind_chk;
-- ALTER TABLE compliance.collaborator_rate_overrides_mirror
--     ADD CONSTRAINT rate_overrides_override_kind_chk
--         CHECK (override_kind IN ('market_rate_excursion', 'share_split_deviation'));
-- COMMIT;
