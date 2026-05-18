# Persona-View Spec — `governance.initiative_program_rollup_view`

| Key | Value |
|:---|:---|
| Initiative | I86 P3 (initiative-cluster-execution-coordinator) |
| Authority | D-IH-86-K (persona-view rollup chartered Round 2) + D-IH-86-L (BBR drift-gate extension) |
| Authored | 2026-05-17 |
| View source | [`supabase/migrations/20260517163648_i86_p3_initiative_program_rollup_view.sql`](../../../../../supabase/migrations/20260517163648_i86_p3_initiative_program_rollup_view.sql) |
| Consumers | HLK-ERP panels (six routes; forward-chartered to I89 candidate for implementation) |

## 1. Why six personas, not one

The rollup view returns RAW initiative × program rows. Each persona reads a **different slice** with **different rendering rules**. Naming the personas up-front pre-commits the panel contract so a single rollup view powers all six panels without a parallel-tree explosion. Six is the minimum coverage to span the operator landscape revealed at the I86 Round 2 charter:

- **PMO** (portfolio orchestration)
- **Brand & Narrative Manager** (Marketing program slice)
- **IntelligenceOps** (Research program slice — forward-chartered to I75 active)
- **People** (Compliance + Talent + Founder + Madeira — the cross-cutting axis)
- **Founder** (meta-persona; reads every program)
- **Adviser-external** (REDACTED; external advisers per `akos-adviser-engagement.mdc`)

Two adjacencies that **do not** become their own persona (P3 acceptance):

- **DevOPS** and **System Owner** read the Tech program slice through the **People** persona (because in the post-I81 organisation those roles live under People-Compliance + Tech-System-Owner, sharing the same authentication scope). When the I81 People-DoD work activates a Tech persona, this row promotes to seven personas at the next P3-style review.
- **Investor** / **Cleared collaborator** / **Apprentice** read **public** rollup surfaces (none currently; reserved for forward initiatives). They are out of scope for I86 P3.

## 2. Per-persona contract

### 2.1 PMO

| Slot | Spec |
|:---|:---|
| Panel route | `/operator/operations/pmo/program-rollup/` |
| View slice | All rows from `governance.initiative_program_rollup_view` |
| Rendering | Raw — full `program_anchor_id` (e.g. `PRJ-HOL-PGF-2026`) + initiative metadata |
| Filters | By `status` (default: `active` + `continuous` + `program_line`); by `cycle_id`; by `owner_role`; by `program_lifecycle_status` |
| Sort | Default `program_anchor_id ASC, initiative_id ASC`; secondary `inception_date DESC` |
| Action handles | Open initiative master-roadmap (deep-link to `folder_path`); open program master-roadmap (deep-link via `program_id`); promote to D-IH-86-D cross-check; close initiative (forward-chartered) |
| Classification | Internal Use (level 4) |
| Auth | `authenticated` session with PMO role claim |

### 2.2 Brand & Narrative Manager

| Slot | Spec |
|:---|:---|
| Panel route | `/operator/marketing/brand/program-rollup/` |
| View slice | Rows where `program_anchor_id IN ('PRJ-HOL-MKT-2026', 'PRJ-HOL-BRAND-2026')` OR `owner_role = 'Brand & Narrative Manager'` |
| Rendering | Raw |
| Filters | By `status`; by initiative-author (cross-link to `BRAND_VOICE_FOUNDATION.md` authorship) |
| Sort | Default `program_anchor_id ASC, last_review DESC` |
| Action handles | Open BRAND program register; cross-link to BRAND_BASELINE_REALITY_MATRIX (drift-gate scope) |
| Classification | Internal Use (level 4) |
| Auth | `authenticated` with Marketing role claim |

### 2.3 IntelligenceOps

| Slot | Spec |
|:---|:---|
| Panel route | `/operator/research/intelligence/program-rollup/` |
| View slice | Rows where `program_anchor_id IN ('PRJ-HOL-RES-2026', 'PRJ-HOL-INT-2026')` OR `owner_role IN ('Intelligence', 'Holistik Researcher')` |
| Rendering | Raw |
| Filters | By `target_class` (forward-link to `INTELLIGENCEOPS_REGISTER.csv` — cross-canon read; gated on I75 active) |
| Sort | Default `program_anchor_id ASC, last_review DESC` |
| Action handles | Open IntelligenceOps register; cross-link to `INTELLIGENCEOPS_REGISTER.csv` |
| Classification | Restricted (level 5) — intelligence-collection metadata |
| Auth | `authenticated` with Research role claim; gated until I75 activates |

### 2.4 People (Compliance + Talent + Founder + Madeira)

| Slot | Spec |
|:---|:---|
| Panel route | `/operator/people/program-rollup/` |
| View slice | Rows where `program_anchor_id IN ('PRJ-HOL-PPL-2026', 'PRJ-HOL-FOUNDING-2026')` OR `owner_role IN ('Compliance', 'Talent', 'People Operations', 'Madeira', 'CPO')` |
| Rendering | Raw |
| Filters | By area (Compliance / Talent / People Operations / Founder-class / Madeira-class) |
| Sort | Default `program_anchor_id ASC, owner_role ASC` |
| Action handles | Open People design-pattern library; cross-link to baseline_organisation roles |
| Classification | Internal Use (level 4) — except Madeira-class rows (level 5) |
| Auth | `authenticated` with People role claim |

### 2.5 Founder (meta-persona)

| Slot | Spec |
|:---|:---|
| Panel route | `/operator/people/founder/program-rollup/` |
| View slice | All rows (Founder reads every program slice) |
| Rendering | Raw |
| Filters | By program (multi-select); by area (multi-select); by `status`; by `risk_class` |
| Sort | Default `program_anchor_id ASC, status ASC, last_review DESC` |
| Action handles | All PMO + Brand + IntelligenceOps + People action handles; plus closure-cross-check (D-IH-86-D) trigger; plus methodology-version filter (`methodology_version_at_review = vN`) |
| Classification | Restricted (level 6) — CPO-class read; carries the highest access |
| Auth | `authenticated` with Founder role claim (single-occupant; carries CPO scope) |

### 2.6 Adviser-external (REDACTED)

| Slot | Spec |
|:---|:---|
| Panel route | `/operator/(public-advops)/program-rollup/` |
| View slice | Rows where `status IN ('active', 'continuous', 'program_line')` AND `program_anchor_id IS NOT NULL` (only currently-tracked work) |
| Rendering | **REDACTED** — `program_anchor_id` substituted with `[INTERNAL-PROGRAM]` at render time; `program_name` rendered as `<external-translation-name>` from BRAND_BASELINE_REALITY_MATRIX translation; `initiative_id` substituted with `[INTERNAL-INITIATIVE]`; only `title` (already external-register per BBR) + `inception_date` + `status` surface |
| Filters | By `status` only |
| Sort | Default `inception_date DESC` |
| Action handles | None (read-only); print-to-PDF for adviser handoff (sibling export pipeline) |
| Classification | Public (level 1) — for adviser eyes; REDACTED so no internal token leaks |
| Auth | `authenticated` with Adviser-external role claim (forward-chartered; not yet a real role) |
| **MANDATORY pause-point** | Per `akos-agent-checkpoint-discipline.mdc` §"Pause-point depth heuristic": public-prose category. **This panel is forward-chartered to I89 candidate, NOT implemented in I86 P3.** I86 P3 ships the SPEC + the data-layer view + the BBR drift-gate scope extension; actual TSX panel implementation requires sibling `hlk-erp` PR which is out of scope for this initiative |

## 3. Authoring-time + render-time redaction matrix

| Layer | Internal-register token | External-register translation | Enforcement |
|:---|:---|:---|:---|
| Authoring (markdown / yaml / panel TSX source) | `PRJ-HOL-*` | `[INTERNAL-PROGRAM]` | `scripts/validate_brand_baseline_reality_drift.py` — extended at P3 (this commit) |
| Database (SQL view) | `program_anchor_id = 'PRJ-HOL-PGF-2026'` | (unchanged — view returns raw) | n/a (data layer is RAW) |
| Render (panel TSX) | column reads `program_anchor_id` | for Adviser-external persona: `program_anchor_id.startsWith('PRJ-HOL-') ? '[INTERNAL-PROGRAM]' : program_anchor_id` | TSX adviser-panel component (forward-chartered to I89) |
| Export (PDF) | embedded `PRJ-HOL-*` text | same redaction as render | sibling export pipeline per `akos-adviser-engagement.mdc` |

## 4. UAT acceptance dimensions

Six dimensions for P3 acceptance, mirrored in [`docs/uat/i86-p3-persona-rollup-acceptance.md`](../../../../uat/i86-p3-persona-rollup-acceptance.md):

1. **Migration applies cleanly** — `supabase/migrations/20260517163648_*.sql` runs against a fresh + P2-applied database with no errors. Idempotent on re-apply.
2. **View returns expected rows** — `SELECT count(*) FROM governance.initiative_program_rollup_view` returns at least 68 rows (current INITIATIVE_REGISTRY row count) with the 24 anchored initiatives producing one row per anchor (≈40 rollup rows from anchored + 44 unanchored single-rows = ~84 expected).
3. **NULL-anchor rows surface** — initiatives without `program_anchors` populated still appear in the view with NULL anchor columns (LEFT JOIN behaviour preserved).
4. **Persona slice filters work** — each persona's filter expression returns a non-empty subset matching the contract above.
5. **BBR drift-gate adviser scope green** — `scripts/validate_brand_baseline_reality_drift.py` scans the extended adviser-surface set and reports no `PRJ-HOL-` leakage (PASS).
6. **Redaction rendering verified** — synthetic adviser-panel render (markdown-only mock — actual TSX deferred to I89) shows `[INTERNAL-PROGRAM]` substitution in place of `PRJ-HOL-*` ids.

## 5. References

- View source: [`supabase/migrations/20260517163648_i86_p3_initiative_program_rollup_view.sql`](../../../../../supabase/migrations/20260517163648_i86_p3_initiative_program_rollup_view.sql)
- Stage B column source: [`supabase/migrations/20260517163635_i86_p2_program_anchors_column.sql`](../../../../../supabase/migrations/20260517163635_i86_p2_program_anchors_column.sql)
- Sibling I66 P6 views (precedent): [`supabase/migrations/20260509213000_i66_p6_brand_template_and_intelligence_views.sql`](../../../../../supabase/migrations/20260509213000_i66_p6_brand_template_and_intelligence_views.sql)
- BBR contract: [`docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_BASELINE_REALITY_MATRIX.md`](../../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_BASELINE_REALITY_MATRIX.md)
- HLK-ERP panel inventory: [`docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/HLK_ERP_ARCHITECTURE.md`](../../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/HLK_ERP_ARCHITECTURE.md) §4 (rows 17-22, this commit)
- Forward-chartered implementation initiative: [`docs/wip/planning/_candidates/i89-hlk-erp-program-rollup-implementation.md`](../../../_candidates/i89-hlk-erp-program-rollup-implementation.md) (stub, this commit)
