---
language: en
status: promoted
promoted_to: docs/wip/planning/89-hlk-erp-program-rollup-implementation/master-roadmap.md
promoted_date: 2026-05-17
promotion_decision: D-IH-89-A (I86 P3 close inline-ratify batch)
candidate_for: I89 (hlk-erp persona-rollup panel implementation)
forward_charter_authority: D-IH-86-K + D-IH-86-N (I86 P3 ratification + I89 forward-charter handoff)
authored: 2026-05-17
last_review: 2026-05-17
owner_role: PMO (primary; tri-co-owned with System Owner + Brand & Narrative Manager per D-IH-89-D)
cross_area_impact: People (Compliance/Founder/Madeira/Talent personas); Marketing (Brand & Narrative Manager persona); Research (IntelligenceOps persona forward-link); Operations (PMO persona); Adviser-external (REDACTED rendering — MANDATORY pause-point per public-prose)
---

> **PROMOTED 2026-05-17 → [`docs/wip/planning/89-hlk-erp-program-rollup-implementation/master-roadmap.md`](../89-hlk-erp-program-rollup-implementation/master-roadmap.md).** Per operator inline-ratify batch in I86 P3 close chat (answers `i89-q1-now` + `i89-q2-all-six` + `i89-q3-cross-cutting-phases` + `i89-q4-tri-co-own` + `i89-q5-flip-now`), I89 is now an **active initiative** with five decisions D-IH-89-A..E ratified. This stub is preserved for archival reference; the active roadmap is the source of truth for phase ordering + decisions + risks + files.

# I89 candidate — HLK-ERP persona-rollup panel implementation (PROMOTED 2026-05-17)

**Forward-chartered from I86 P3 (D-IH-86-K).** I86 P3 ships the data-layer view + the persona-view spec + the BBR drift-gate scope extension. The actual TSX panel implementation across six routes — and especially the Adviser-external REDACTED rendering — lives in this follow-up candidate.

## Context (carried forward from I86)

- **Data layer ready**: `governance.initiative_program_rollup_view` ([supabase/migrations/20260517163648_*.sql](../../../../supabase/migrations/20260517163648_i86_p3_initiative_program_rollup_view.sql)) joins `compliance.initiative_registry_mirror` × `compliance.program_registry_mirror` on the post-P2 `program_anchors` semicolon-list column. Returns one row per (initiative, anchor) pair; LEFT JOIN so unanchored initiatives still surface.
- **Spec ready**: [`docs/wip/planning/86-initiative-cluster-execution-coordinator/reports/persona-view-spec-2026-05-19.md`](../86-initiative-cluster-execution-coordinator/reports/persona-view-spec-2026-05-19.md) covers six persona contracts.
- **Drift gate ready**: [`scripts/validate_brand_baseline_reality_drift.py`](../../../../scripts/validate_brand_baseline_reality_drift.py) scans `_assets/advops/**/founder-filed/**/*.md` + `**/adviser-handoff/*.md` for `PRJ-HOL-` leakage. Authoring-time hardening lives here; render-time substitution lives in I89.
- **HLK-ERP architecture pre-registered**: [`HLK_ERP_ARCHITECTURE.md`](../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/HLK_ERP_ARCHITECTURE.md) §4 carries six new rollup-aware routes (rows 17-22).

## Why this is a separate initiative (not part of I86)

I86 is an **operational coordinator** ("mints no SSOT" charter per master-roadmap preamble). The Adviser-external view, especially, is **MANDATORY pause-point** territory per `akos-agent-checkpoint-discipline.mdc` §"Pause-point depth heuristic" → public-prose category. That deserves a dedicated initiative with proper P0 operator ratification, not a P3 stretch goal of an operational coordinator.

Additionally, the **TSX implementation belongs in `hlk-erp`** (a sibling repo per `REPOSITORY_REGISTRY.csv`), not in `openclaw-akos`. Cross-repo bless pattern requires its own coordination per `SOP-EXTERNAL_REPO_BLESSING_001.md` + `SOP-CROSS_REPO_SCHEMA_PROPAGATION_001.md`.

## Forward-charter scope

When promoted from candidate to active, I89 should ship:

### Six panel routes (TSX scaffolds under `hlk-erp/app/(operator)/...`)

1. `/operator/operations/pmo/program-rollup/` — full PMO slice
2. `/operator/marketing/brand/program-rollup/` — Marketing slice
3. `/operator/research/intelligence/program-rollup/` — Research slice (gated until I75 active)
4. `/operator/people/program-rollup/` — People cross-cutting slice
5. `/operator/people/founder/program-rollup/` — Founder meta-persona (CPO L6)
6. `/operator/(public-advops)/program-rollup/` — Adviser-external REDACTED

### REDACTED rendering enforcement (Adviser-external panel)

- At-the-render TSX substitution: `program_anchor_id.startsWith('PRJ-HOL-') ? '[INTERNAL-PROGRAM]' : program_anchor_id`.
- `program_name` column rendered via BRAND_BASELINE_REALITY_MATRIX translation (external-register name).
- `initiative_id` rendered as `[INTERNAL-INITIATIVE]`.
- Only `title` (already external-register per BBR) + `inception_date` + `status` surface.

### Supabase Auth + RLS wiring

- Each persona panel reads `governance.initiative_program_rollup_view` with the appropriate `authenticated` JWT claim.
- Persona slicing applied as `WHERE` clause + RLS policy.
- Adviser-external role claim TBD — likely a separate authentication scope per `akos-adviser-engagement.mdc`; carries no `service_role` privilege.

### Browser smoke (Cursor Browser MCP)

- Six routes resolve at `dashboard.holistikaresearch.com` (or per-environment domain).
- Render matches spec.
- Adviser-external panel passes BBR review (no `PRJ-HOL-` visible in rendered DOM).

### UAT acceptance

- Dimensions D1-D5 + E1-E4 from [`docs/uat/i86-p3-persona-rollup-acceptance.md`](../../../uat/i86-p3-persona-rollup-acceptance.md) carry forward as I89 acceptance criteria.
- Browser MCP-verified screenshots for each persona; PDF export of Adviser-external panel attached.

### Adviser-external PDF export pipeline

- Sibling export pipeline per `akos-adviser-engagement.mdc` consumes the same REDACTED rendering.
- Operator handoff carries no internal-register tokens.

## Cross-references

- Inception decision: D-IH-86-K (I86 P3 ratification, 2026-05-17).
- Forward-charter decision: D-IH-86-N (I86 P3 closure → I89 implementation handoff, 2026-05-17).
- Closure decision (when I89 ships): TBD.
- I86 closure record: [`docs/wip/planning/86-initiative-cluster-execution-coordinator/reports/p3-closure-pause-record-2026-05-17.md`](../86-initiative-cluster-execution-coordinator/reports/p3-closure-pause-record-2026-05-17.md) (this commit).
- I86 P3 OPS row: OPS-86-4 closes when I89 candidate promotes.
- ADVOPS dossier triage OPS row: OPS-86-5 (ENISA evidence prose carries `PRJ-HOL-FOUNDING-2026` literally; needs BBR external-register translation; owner: Brand & Narrative Manager + ADVOPS engagement co-owner).
