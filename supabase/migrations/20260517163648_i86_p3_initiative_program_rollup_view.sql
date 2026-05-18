-- I86 P3 — governance.initiative_program_rollup_view
--
-- Cross-area persona-view rollup joining INITIATIVE_REGISTRY x PROGRAM_REGISTRY mirrors
-- on the post-P2 `program_anchors` first-class column (D-IH-86-J), surfacing one row per
-- (initiative, program_anchor) pair so consumer panels can render initiative portfolios
-- partitioned by program.
--
-- Authority: D-IH-86-K (P0 → P3 closure) — persona-view rollup chartered at I86 Round 2;
--            D-IH-86-J (P2 column promotion) — depends on program_anchors column existing
--            on compliance.initiative_registry_mirror (preceding migration 20260517163635);
--            D-IH-86-L (BBR drift-gate extension) — REDACTED rendering is enforced at the
--            consumer-panel layer (forward-chartered to I89 candidate), not in this view.
--
-- Per akos-holistika-operations.mdc §"Operator SQL gate" + I66 P6 precedent
-- (governance.brand_template_registry + governance.engagement_intelligence_view at
-- supabase/migrations/20260509213000_i66_p6_brand_template_and_intelligence_views.sql):
--   - Discovery: governance schema already exists (I64 P1 governance_canonical_change_log
--     2026-05-08 + I65 P1 governance_planning_workspace 2026-05-08 + I66 P6 brand_template
--     2026-05-09 + I66 P6 engagement_intelligence 2026-05-09). USAGE granted to
--     authenticated + anon + service_role at I66 P6 L13.
--   - Proposal: read-only view; no DML; rollup query joins two existing mirrors only;
--     no PII (initiative + program metadata + governance ids); RLS posture inherits from
--     view-level GRANT (Postgres views do not carry their own RLS).
--   - Execute: operator applies via MCP apply_migration after the I86 P2 migration lands;
--     this migration is idempotent (CREATE OR REPLACE VIEW).
--   - Pre-push parity: `supabase migration list` shows both timestamps land in order
--     (20260517163635 P2 column, then 20260517163648 P3 view).
--
-- Pattern: I66 P6 view pattern (CREATE OR REPLACE VIEW + COMMENT ON VIEW + GRANT SELECT
--          to authenticated + service_role + NOTIFY pgrst). Adapted from VALUES-tabled
--          static-data views to a JOIN-tabled mirror-join view because P3 data is
--          dynamically derived from the canonical CSVs (not a frozen registry snapshot).
--
-- Rollback plan: DROP VIEW IF EXISTS governance.initiative_program_rollup_view; idempotent
--                because of OR REPLACE; safe to recreate.
--
-- Redaction posture: This view returns RAW initiative + program rows (`PRJ-HOL-*` literal
-- program ids in the result set). External-facing redaction (e.g. for Adviser-external
-- persona panels) is enforced at the consumer-panel layer per `akos-brand-baseline-reality.mdc`
-- §"Translation table" + `scripts/validate_brand_baseline_reality_drift.py` extended scope
-- (I86 P3 adviser-surface extension). Authoring-time leakage is caught by the drift gate;
-- runtime rendering substitutes `[INTERNAL-PROGRAM]` per consumer-panel TSX (forward-chartered
-- to I89 candidate).
--
-- RLS: Postgres views inherit access from the underlying tables AND the view-level GRANT.
-- - `compliance.initiative_registry_mirror` denies anon + authenticated (service_role only) per
--   I59 P1.2 + I86 P2 inheritance.
-- - `compliance.program_registry_mirror` carries the same posture.
-- - The view itself GRANTs SELECT to `authenticated` + `service_role` so panel consumers
--   reading via Supabase JS client with an authenticated session can query the view.
-- - The underlying-table RLS posture **also** filters: an authenticated session reading
--   the view goes through SECURITY DEFINER not by default; this view uses default
--   SECURITY INVOKER so the rows surfacing to authenticated readers depend on the
--   underlying-table RLS. Per D-IH-86-K Stage-A acceptance, anonymous and unauthenticated
--   access are denied at the underlying table layer. The view-GRANT SELECT to authenticated
--   surfaces the view name in PostgREST schema cache; actual row return is governed by
--   underlying RLS. Operators consuming via service_role bypass RLS (intended for sync
--   jobs and authoring-side ERP).

CREATE OR REPLACE VIEW governance.initiative_program_rollup_view AS
SELECT
    init.initiative_id,
    init.repo_slug,
    init.folder_path,
    init.title,
    init.status,
    init.cycle_id,
    init.owner_role,
    init.inception_date,
    init.last_review,
    init.closed_at,
    init.archived_at,
    init.continuous_rationale,
    init.cadence,
    init.gated_on,
    init.operator_action,
    -- Anchor unspooled from the semicolon-list column (one row per (initiative, anchor) pair).
    btrim(anchor_token) AS program_anchor_id,
    -- Joined program metadata (LEFT JOIN so initiatives without anchors still surface).
    prog.program_name,
    prog.program_code,
    prog.lifecycle_status AS program_lifecycle_status,
    prog.parent_program_id,
    prog.primary_owner_role AS program_owner_role,
    prog.default_plane AS program_default_plane,
    prog.start_date AS program_start_date,
    prog.target_close_date AS program_target_close_date,
    prog.risk_class AS program_risk_class,
    -- I86 review-stamp dimension (D-IH-71-E columns inherited from both mirrors).
    init.last_review_at AS initiative_last_review_at,
    init.last_review_by AS initiative_last_review_by,
    init.last_review_decision_id AS initiative_last_review_decision_id,
    init.methodology_version_at_review AS initiative_methodology_version_at_review,
    prog.last_review_at AS program_last_review_at,
    prog.last_review_by AS program_last_review_by,
    prog.last_review_decision_id AS program_last_review_decision_id,
    prog.methodology_version_at_review AS program_methodology_version_at_review
FROM compliance.initiative_registry_mirror AS init
LEFT JOIN LATERAL unnest(
    CASE
        WHEN init.program_anchors IS NULL OR init.program_anchors = ''
        THEN ARRAY[NULL]::TEXT[]
        ELSE string_to_array(init.program_anchors, ';')
    END
) AS anchor_token ON true
LEFT JOIN compliance.program_registry_mirror AS prog
    ON prog.program_id = btrim(anchor_token);

COMMENT ON VIEW governance.initiative_program_rollup_view IS
  'I86 P3 (D-IH-86-K) — cross-area persona-view rollup. One row per (initiative, program_anchor). Initiatives without program_anchors surface as one row with NULL anchor/program columns. RAW rows (no redaction); consumer panels enforce REDACTED rendering for Adviser-external persona per D-IH-86-L + akos-brand-baseline-reality.mdc.';

GRANT SELECT ON governance.initiative_program_rollup_view TO authenticated, service_role;

NOTIFY pgrst, 'reload schema';
