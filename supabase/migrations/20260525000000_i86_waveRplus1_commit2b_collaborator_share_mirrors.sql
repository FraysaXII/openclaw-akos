-- Initiative 86 Wave R+1 Commit 2b — compliance.collaborator_share_*_mirror (13th Quality Fabric specialty).
--
-- Per D-IH-86-CY-A (COLLABORATOR_SHARE_DOCTRINE mint + Combo C+D hybrid posture)
--   + D-IH-86-CY-B (formula-c-hybrid TRUE-MARGIN benefits formula)
--   + D-IH-86-CY-C (clause-c-recommended-table partner overlap exclusion pattern)
--   + D-IH-86-CY-D (market-rate-reference + governed overrides + Aisha-rate routing)
--   + D-IH-86-CY-EXT (Wave R+1 Commit 2b-ext: share_pattern enum extending the
--     schema to model three operationally observed economic shapes —
--     deep_partner_65_35 / orchestration_broker_thin_margin / custom).
--
-- Mirror tables for the 5 canonical CSVs under
-- docs/references/hlk/v3.0/Admin/O5-1/People/People Operations/canonicals/dimensions/.
-- Receives upserts from the canonical CSVs via the compliance_mirror_emit profile
-- (sync_compliance_mirrors_from_csv.py --collaborator-share-only forward; emit
-- helpers land at Commit 2c per the per-initiative sync-emit pattern established
-- by I59 P1.5, I72 P9, I73 P1, I79 P2, I84 P3).
--
-- Server-only (service_role) RLS posture per the existing compliance.* mirror
-- baseline. CHECK constraints mirror the Pydantic Literal-typed enum columns
-- in akos/hlk_collaborator_share.py + the doctrine §2 defaults (65/35 split,
-- bill_mode per service class, market-rate variance tolerance).
--
-- INFO ramp at mint per akos-collaborator-share.mdc RULE 5 (lands Commit 2c);
-- promotes to FAIL after the first non-trivial engagement settles + operator
-- ratifies. Mirror tables are populated immediately upon canonical CSV mint
-- regardless of ramp status (mirror parity is independent of strict-mode gate).

BEGIN;

-- ============================================================================
-- 1. compliance.collaborator_share_registry_mirror
-- ============================================================================

CREATE TABLE IF NOT EXISTS compliance.collaborator_share_registry_mirror (
    share_id                              text NOT NULL PRIMARY KEY,
    engagement_id                         text NOT NULL,
    collaborator_id                       text NOT NULL,
    engagement_model_id                   text NOT NULL,
    share_pattern                         text NOT NULL DEFAULT 'deep_partner_65_35',
    holistika_share_pct                   integer NOT NULL,
    collaborator_share_pct                integer NOT NULL,
    collaborator_billed_rate              numeric(18, 4) NOT NULL,
    collaborator_billed_rate_currency     text NOT NULL,
    collaborator_role_class               text NOT NULL,
    share_override_decision_id            text,
    status                                text NOT NULL,
    signed_at                             date,
    signed_by_collaborator                text,
    signed_by_holistika                   text,
    last_review_at                        date NOT NULL,
    notes                                 text,
    source_git_sha                        text,
    synced_at                             timestamptz DEFAULT now(),
    CONSTRAINT share_registry_share_id_format_chk
        CHECK (share_id ~ '^SHARE-[A-Z0-9-]+$'),
    -- D-IH-86-CY-EXT: enum membership mirrors VALID_SHARE_PATTERNS.
    CONSTRAINT share_registry_share_pattern_chk
        CHECK (share_pattern IN (
            'deep_partner_65_35',
            'orchestration_broker_thin_margin',
            'custom'
        )),
    CONSTRAINT share_registry_holistika_pct_chk
        CHECK (holistika_share_pct BETWEEN 0 AND 100),
    CONSTRAINT share_registry_collaborator_pct_chk
        CHECK (collaborator_share_pct BETWEEN 0 AND 100),
    -- D-IH-86-CY-EXT: per-row sum-to-100 invariant applies ONLY to
    -- deep_partner_65_35 rows. orchestration_broker_thin_margin spreads
    -- the 100% across multiple rows (across-rows invariant lives in CS-03);
    -- custom rows skip the automatic check (operator carries the math).
    CONSTRAINT share_registry_splits_sum_to_100_chk
        CHECK (
            share_pattern <> 'deep_partner_65_35'
            OR (holistika_share_pct + collaborator_share_pct = 100)
        ),
    CONSTRAINT share_registry_currency_chk
        CHECK (collaborator_billed_rate_currency ~ '^[A-Z]{3}$'),
    CONSTRAINT share_registry_status_chk
        CHECK (status IN (
            'draft', 'proposed', 'signed', 'active', 'settled', 'archived'
        )),
    -- D-IH-86-CY-EXT: per-pattern default-split + override audit (mirrors
    -- validator CS-04 branching).
    --
    -- deep_partner_65_35: default 65/35; any deviation MUST carry a
    --   ratifying decision FK (CS-04 row-local audit).
    -- orchestration_broker_thin_margin: per-row default = 6% Holistika +
    --   the row's collaborator slice. Across-row aggregate is checked by
    --   validator CS-04 (engagement-aggregate); the CHECK constraint here
    --   only enforces the row-local override-FK requirement when this row
    --   deviates from 6% Holistika.
    -- custom: every row MUST carry override FK.
    CONSTRAINT share_registry_default_split_or_override_chk
        CHECK (
            (share_pattern = 'deep_partner_65_35'
                AND (
                    (holistika_share_pct = 65 AND collaborator_share_pct = 35)
                    OR (share_override_decision_id IS NOT NULL
                        AND length(share_override_decision_id) > 0)
                ))
            OR (share_pattern = 'orchestration_broker_thin_margin'
                AND (
                    holistika_share_pct = 6
                    OR (share_override_decision_id IS NOT NULL
                        AND length(share_override_decision_id) > 0)
                ))
            OR (share_pattern = 'custom'
                AND share_override_decision_id IS NOT NULL
                AND length(share_override_decision_id) > 0)
        )
);

CREATE INDEX IF NOT EXISTS share_registry_engagement_idx
    ON compliance.collaborator_share_registry_mirror (engagement_id);
CREATE INDEX IF NOT EXISTS share_registry_collaborator_idx
    ON compliance.collaborator_share_registry_mirror (collaborator_id);
CREATE INDEX IF NOT EXISTS share_registry_status_idx
    ON compliance.collaborator_share_registry_mirror (status);
CREATE INDEX IF NOT EXISTS share_registry_last_review_idx
    ON compliance.collaborator_share_registry_mirror (last_review_at DESC);
-- D-IH-86-CY-EXT: per-pattern slicing (orchestration_broker analytics, etc.).
CREATE INDEX IF NOT EXISTS share_registry_share_pattern_idx
    ON compliance.collaborator_share_registry_mirror (share_pattern);

ALTER TABLE compliance.collaborator_share_registry_mirror ENABLE ROW LEVEL SECURITY;
GRANT SELECT, INSERT, UPDATE ON compliance.collaborator_share_registry_mirror TO service_role;
REVOKE ALL ON compliance.collaborator_share_registry_mirror FROM anon, authenticated;

COMMENT ON TABLE compliance.collaborator_share_registry_mirror IS
    'I86 Wave R+1 Commit 2b: per-(engagement, collaborator) revenue-share row; mirrors COLLABORATOR_SHARE_REGISTRY.csv canonical per COLLABORATOR_SHARE_DOCTRINE.md §2.1 (D-IH-86-CY-A). D-IH-86-CY-EXT (Commit 2b-ext) adds share_pattern enum: deep_partner_65_35 (default; benefits formula; 65/35 row-local split) | orchestration_broker_thin_margin (Holistika ~6% per row; across-row aggregate = 100% revenue split; CS-03 across-rows audit) | custom (operator carries math; CS-03 skipped; CS-04 mandates override FK).';
COMMENT ON COLUMN compliance.collaborator_share_registry_mirror.share_pattern IS
    'D-IH-86-CY-EXT: which collaborator-share economic shape this row encodes. Enum values mirror VALID_SHARE_PATTERNS in akos/hlk_collaborator_share.py. Default deep_partner_65_35 preserves backward compatibility with all pre-ext rows.';


-- ============================================================================
-- 2. compliance.holistika_vendor_services_billed_mirror
-- ============================================================================

CREATE TABLE IF NOT EXISTS compliance.holistika_vendor_services_billed_mirror (
    vendor_billing_id                     text NOT NULL PRIMARY KEY,
    engagement_id                         text NOT NULL,
    holistika_service_class               text NOT NULL,
    bill_mode                             text NOT NULL,
    billed_hours                          numeric(18, 4),
    billed_rate                           numeric(18, 4),
    billed_amount_computed                numeric(18, 4),
    justification_clause_id               text,
    bill_mode_decision_id                 text,
    status                                text NOT NULL,
    last_review_at                        date NOT NULL,
    notes                                 text,
    source_git_sha                        text,
    synced_at                             timestamptz DEFAULT now(),
    CONSTRAINT vendor_billed_vbid_format_chk
        CHECK (vendor_billing_id ~ '^VBILL-[A-Z0-9-]+$'),
    CONSTRAINT vendor_billed_service_class_chk
        CHECK (holistika_service_class IN (
            'research_head_discipline',
            'mktops_marketing',
            'dataops_engineering',
            'madeira_ai_orchestration',
            'brand_render_machinery',
            'pmo_orchestration',
            'legal_template_handling',
            'front_end_engineering',
            'ai_engineering_bespoke',
            'external_research_pass'
        )),
    CONSTRAINT vendor_billed_bill_mode_chk
        CHECK (bill_mode IN ('billed', 'in_kind')),
    CONSTRAINT vendor_billed_status_chk
        CHECK (status IN ('draft', 'active', 'settled', 'archived')),
    -- Doctrine §2.2: 'billed' rows MUST have positive hours + rate; 'in_kind'
    -- rows have empty hours/rate. CS-05 audit surfaces deviations.
    CONSTRAINT vendor_billed_amounts_consistency_chk
        CHECK (
            (bill_mode = 'billed' AND billed_hours > 0 AND billed_rate > 0)
            OR (bill_mode = 'in_kind' AND billed_hours IS NULL AND billed_rate IS NULL)
        )
);

CREATE INDEX IF NOT EXISTS vendor_billed_engagement_idx
    ON compliance.holistika_vendor_services_billed_mirror (engagement_id);
CREATE INDEX IF NOT EXISTS vendor_billed_service_class_idx
    ON compliance.holistika_vendor_services_billed_mirror (holistika_service_class);
CREATE INDEX IF NOT EXISTS vendor_billed_bill_mode_idx
    ON compliance.holistika_vendor_services_billed_mirror (bill_mode);
CREATE INDEX IF NOT EXISTS vendor_billed_status_idx
    ON compliance.holistika_vendor_services_billed_mirror (status);

ALTER TABLE compliance.holistika_vendor_services_billed_mirror ENABLE ROW LEVEL SECURITY;
GRANT SELECT, INSERT, UPDATE ON compliance.holistika_vendor_services_billed_mirror TO service_role;
REVOKE ALL ON compliance.holistika_vendor_services_billed_mirror FROM anon, authenticated;

COMMENT ON TABLE compliance.holistika_vendor_services_billed_mirror IS
    'I86 Wave R+1 Commit 2b: per-engagement billed-vs-in-kind log for Holistika vendor services; mirrors HOLISTIKA_VENDOR_SERVICES_BILLED.csv canonical per COLLABORATOR_SHARE_DOCTRINE.md §2.2 (D-IH-86-CY-B formula-c-hybrid TRUE-MARGIN benefits formula). billed rows contribute to project_costs in benefits calculation; in_kind rows contribute 0 (Holistika absorbs).';


-- ============================================================================
-- 3. compliance.partner_overlap_exclusion_clauses_mirror
-- ============================================================================

CREATE TABLE IF NOT EXISTS compliance.partner_overlap_exclusion_clauses_mirror (
    clause_id                                  text NOT NULL PRIMARY KEY,
    clause_name                                text NOT NULL,
    applicable_holistika_service_classes       text NOT NULL,
    overlap_pattern_description                text NOT NULL,
    internal_precedent                         text,
    industry_precedent_citation                text,
    ratifying_decision_id                      text NOT NULL,
    last_review_at                             date NOT NULL,
    status                                     text NOT NULL,
    notes                                      text,
    source_git_sha                             text,
    synced_at                                  timestamptz DEFAULT now(),
    CONSTRAINT overlap_clauses_clause_id_format_chk
        CHECK (clause_id ~ '^clause_[a-z0-9_]+$'),
    CONSTRAINT overlap_clauses_status_chk
        CHECK (status IN ('active', 'planned', 'deprecated', 'archived'))
);

CREATE INDEX IF NOT EXISTS overlap_clauses_status_idx
    ON compliance.partner_overlap_exclusion_clauses_mirror (status);
CREATE INDEX IF NOT EXISTS overlap_clauses_ratifying_decision_idx
    ON compliance.partner_overlap_exclusion_clauses_mirror (ratifying_decision_id);

ALTER TABLE compliance.partner_overlap_exclusion_clauses_mirror ENABLE ROW LEVEL SECURITY;
GRANT SELECT, INSERT, UPDATE ON compliance.partner_overlap_exclusion_clauses_mirror TO service_role;
REVOKE ALL ON compliance.partner_overlap_exclusion_clauses_mirror FROM anon, authenticated;

COMMENT ON TABLE compliance.partner_overlap_exclusion_clauses_mirror IS
    'I86 Wave R+1 Commit 2b: named overlap-clause pattern table for partner overlap exclusion; mirrors PARTNER_OVERLAP_EXCLUSION_CLAUSES.csv canonical per COLLABORATOR_SHARE_DOCTRINE.md §2.3 (D-IH-86-CY-C clause-c-recommended-table). When Holistika service class overlaps with partner capability (e.g., Websitz precedent: agency partner overlapping with MKTOPS), the named clause documents the in-kind contribution + exclusion rationale.';


-- ============================================================================
-- 4. compliance.collaborator_market_rate_reference_mirror
-- ============================================================================

CREATE TABLE IF NOT EXISTS compliance.collaborator_market_rate_reference_mirror (
    rate_id                       text NOT NULL PRIMARY KEY,
    role_class                    text NOT NULL,
    region_code                   text NOT NULL,
    experience_band               text NOT NULL,
    rate_currency                 text NOT NULL,
    rate_min_per_hour             numeric(18, 4) NOT NULL,
    rate_typical_per_hour         numeric(18, 4) NOT NULL,
    rate_max_per_hour             numeric(18, 4) NOT NULL,
    rate_source                   text NOT NULL,
    last_review_at                date NOT NULL,
    status                        text NOT NULL,
    notes                         text,
    source_git_sha                text,
    synced_at                     timestamptz DEFAULT now(),
    CONSTRAINT market_rate_rate_id_format_chk
        CHECK (rate_id ~ '^rate_[a-z0-9_]+$'),
    CONSTRAINT market_rate_region_code_chk
        CHECK (region_code ~ '^[A-Z]{2}$'),
    CONSTRAINT market_rate_currency_chk
        CHECK (rate_currency ~ '^[A-Z]{3}$'),
    CONSTRAINT market_rate_experience_band_chk
        CHECK (experience_band IN ('junior', 'mid', 'senior', 'lead', 'expert')),
    CONSTRAINT market_rate_status_chk
        CHECK (status IN ('active', 'planned', 'deprecated', 'archived')),
    CONSTRAINT market_rate_band_order_chk
        CHECK (rate_min_per_hour <= rate_typical_per_hour
               AND rate_typical_per_hour <= rate_max_per_hour),
    CONSTRAINT market_rate_positive_typical_chk
        CHECK (rate_typical_per_hour > 0)
);

CREATE INDEX IF NOT EXISTS market_rate_role_class_idx
    ON compliance.collaborator_market_rate_reference_mirror (role_class);
CREATE INDEX IF NOT EXISTS market_rate_region_idx
    ON compliance.collaborator_market_rate_reference_mirror (region_code);
CREATE INDEX IF NOT EXISTS market_rate_status_idx
    ON compliance.collaborator_market_rate_reference_mirror (status);

ALTER TABLE compliance.collaborator_market_rate_reference_mirror ENABLE ROW LEVEL SECURITY;
GRANT SELECT, INSERT, UPDATE ON compliance.collaborator_market_rate_reference_mirror TO service_role;
REVOKE ALL ON compliance.collaborator_market_rate_reference_mirror FROM anon, authenticated;

COMMENT ON TABLE compliance.collaborator_market_rate_reference_mirror IS
    'I86 Wave R+1 Commit 2b: role × region × experience-band market rate reference; mirrors COLLABORATOR_MARKET_RATE_REFERENCE.csv canonical per COLLABORATOR_SHARE_DOCTRINE.md §2.4 (D-IH-86-CY-D market-rate-reference-table-plus-governed-overrides). Aisha-rate-policy precedent; CS-04 audit (validate_collaborator_share.py) flags collaborator_billed_rate outside ±25% of rate_typical_per_hour.';


-- ============================================================================
-- 5. compliance.collaborator_rate_overrides_mirror
-- ============================================================================

CREATE TABLE IF NOT EXISTS compliance.collaborator_rate_overrides_mirror (
    override_id                       text NOT NULL PRIMARY KEY,
    override_kind                     text NOT NULL,
    engagement_id                     text NOT NULL,
    collaborator_id                   text NOT NULL,
    reference_rate_id                 text,
    reference_rate_value              numeric(18, 4),
    actual_value                      numeric(18, 4) NOT NULL,
    variance_pct                      numeric(8, 4) NOT NULL,
    justification_narrative           text NOT NULL,
    ratifying_decision_id             text NOT NULL,
    commercial_strategy_rationale     text NOT NULL,
    expires_at                        date,
    last_review_at                    date NOT NULL,
    status                            text NOT NULL,
    notes                             text,
    source_git_sha                    text,
    synced_at                         timestamptz DEFAULT now(),
    CONSTRAINT rate_overrides_override_id_format_chk
        CHECK (override_id ~ '^OVERRIDE-[A-Z0-9-]+$'),
    CONSTRAINT rate_overrides_override_kind_chk
        CHECK (override_kind IN ('market_rate_excursion', 'share_split_deviation')),
    CONSTRAINT rate_overrides_status_chk
        CHECK (status IN ('draft', 'active', 'expired', 'archived')),
    -- Doctrine §2.4: expired overrides MUST be reflected in status; CS-07
    -- audit surfaces overdue active rows where expires_at < CURRENT_DATE.
    CONSTRAINT rate_overrides_expiry_status_consistency_chk
        CHECK (
            expires_at IS NULL
            OR status IN ('expired', 'archived', 'draft')
            OR expires_at >= CURRENT_DATE
        )
);

CREATE INDEX IF NOT EXISTS rate_overrides_engagement_idx
    ON compliance.collaborator_rate_overrides_mirror (engagement_id);
CREATE INDEX IF NOT EXISTS rate_overrides_collaborator_idx
    ON compliance.collaborator_rate_overrides_mirror (collaborator_id);
CREATE INDEX IF NOT EXISTS rate_overrides_ref_rate_idx
    ON compliance.collaborator_rate_overrides_mirror (reference_rate_id);
CREATE INDEX IF NOT EXISTS rate_overrides_status_idx
    ON compliance.collaborator_rate_overrides_mirror (status);
CREATE INDEX IF NOT EXISTS rate_overrides_expires_at_idx
    ON compliance.collaborator_rate_overrides_mirror (expires_at);

ALTER TABLE compliance.collaborator_rate_overrides_mirror ENABLE ROW LEVEL SECURITY;
GRANT SELECT, INSERT, UPDATE ON compliance.collaborator_rate_overrides_mirror TO service_role;
REVOKE ALL ON compliance.collaborator_rate_overrides_mirror FROM anon, authenticated;

COMMENT ON TABLE compliance.collaborator_rate_overrides_mirror IS
    'I86 Wave R+1 Commit 2b: governed commercial deviations from market-rate-reference or default-split; mirrors COLLABORATOR_RATE_OVERRIDES.csv canonical per COLLABORATOR_SHARE_DOCTRINE.md §2.4 (D-IH-86-CY-D). Two override_kinds: market_rate_excursion (rate outside ±25% band; covers CS-04) + share_split_deviation (non-65/35 split; covers CS-03). Both require ratifying_decision_id FK to DECISION_REGISTER + commercial_strategy_rationale narrative + optional expires_at for time-boxed deviations.';


COMMIT;

-- ============================================================================
-- Rollback (per supabase/migrations/README.md operator runbook)
-- ============================================================================
-- BEGIN;
-- DROP TABLE IF EXISTS compliance.collaborator_rate_overrides_mirror;
-- DROP TABLE IF EXISTS compliance.collaborator_market_rate_reference_mirror;
-- DROP TABLE IF EXISTS compliance.partner_overlap_exclusion_clauses_mirror;
-- DROP TABLE IF EXISTS compliance.holistika_vendor_services_billed_mirror;
-- DROP TABLE IF EXISTS compliance.collaborator_share_registry_mirror;
-- COMMIT;
