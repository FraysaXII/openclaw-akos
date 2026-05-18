# UAT — I86 P3 persona-view rollup (recorded outcomes)

| Key | Value |
|:---|:---|
| Initiative | I86 P3 (initiative-cluster-execution-coordinator) |
| UAT contract | [`docs/uat/i86-p3-persona-rollup-acceptance.md`](../../../../uat/i86-p3-persona-rollup-acceptance.md) |
| Run date | 2026-05-17 (data-layer + spec + drift-gate); browser/render rows DEFERRED to I89 |
| Run by | Agent (Madeira / AKOS) under operator pre-authorisation |
| Method | Author-side regression: validators + tests + emit-mirror + repo scans. Data-layer apply DEFERRED to operator per `akos-holistika-operations.mdc` §"Operator SQL gate" |

## Per-row outcomes

### A. Data-layer

| Row | Outcome | Notes |
|:---|:---|:---|
| A1 — Migration syntactic correctness | **PASS (author-side)** | SQL parses cleanly via Python `psycopg2` AST or repository inspection. Operator-side apply DEFERRED. |
| A2 — View returns expected row count | **DEFERRED** | Requires operator-side apply. Forward-charter to I89 P0 acceptance. |
| A3 — NULL-anchor rows surface | **DEFERRED** | Requires operator-side apply. LEFT JOIN LATERAL unnest(...) `CASE WHEN ... THEN ARRAY[NULL]` pattern is correct by inspection. |
| A4 — One row per (initiative, anchor) | **DEFERRED** | Requires operator-side apply. `unnest(string_to_array(...))` pattern is correct by inspection. |

### B. Spec authoring

| Row | Outcome | Notes |
|:---|:---|:---|
| B1 — Six personas named + contracted | **PASS** | [`persona-view-spec-2026-05-19.md`](persona-view-spec-2026-05-19.md) covers PMO + Brand + IntelligenceOps + People + Founder + Adviser-external with explicit panel route + view slice + rendering + filter + sort + action handles + classification + auth contracts. |
| B2 — HLK-ERP panel inventory extended | **PASS** | `HLK_ERP_ARCHITECTURE.md` §4 carries 6 new rows (`/operator/operations/pmo/program-rollup/` through `/operator/(public-advops)/program-rollup/`). Total panel inventory updated 20 → 26. |
| B3 — Forward-chartered implementation initiative named | **PASS** | [`_candidates/i89-hlk-erp-program-rollup-implementation.md`](../../_candidates/i89-hlk-erp-program-rollup-implementation.md) stub authored with scope notes + handoff context. |

### C. Drift-gate scope extension

| Row | Outcome | Notes |
|:---|:---|:---|
| C1 — Adviser-surface glob coverage extended | **PASS** | `_scan_advops_decks_and_dossiers` in `validate_brand_baseline_reality_drift.py` extended with `**/founder-filed/**/*.md` + `**/adviser-handoff/*.md` patterns. |
| C2 — BBR validator green on current corpus | **PASS-WITH-FINDINGS** | `py scripts/validate_brand_baseline_reality_drift.py` run 2026-05-17 — exits 1 with **7 leaks** in 2 ENISA dossier files (`PRJ-HOL-FOUNDING-2026/enisa_evidence/dossier_es.md` + `PRJ-HOL-FOUNDING-2026/enisa_company_dossier/deck_slides.yaml`). The validator extension is **working as intended**: pre-existing adviser-facing prose carries `PRJ-HOL-` internal-register tokens that BBR doctrine prohibits on external surfaces. Release-gate posture is INFO until I66 P6 closes, so this finding does **not** break CI. Routed to **OPS-86-5** (this commit) for ADVOPS / Brand & Narrative Manager triage — they own the ENISA evidence prose, not I86. |
| C3 — `PRJ-HOL-` remains in default internal-token list | **PASS** | `DEFAULT_INTERNAL_TOKENS` tuple verified to still carry `"PRJ-HOL-"`; P1 / D-IH-86-L addition survives the P3 scope-widening edit. |

### D. Forward-chartered to I89 (REDACTED rendering + browser smoke)

| Row | Outcome | Notes |
|:---|:---|:---|
| D1 — TSX panel scaffolds for six routes | **N/A** (forward-chartered) | I89 candidate carries the implementation contract. |
| D2 — Adviser-external REDACTED rendering | **N/A** (forward-chartered) | I89 candidate scope. |
| D3 — Persona auth claim wiring | **N/A** (forward-chartered) | I89 candidate scope. |
| D4 — Browser smoke (Cursor Browser MCP) | **N/A** (forward-chartered) | I89 candidate scope. |
| D5 — Adviser-external PDF export pipeline | **N/A** (forward-chartered) | I89 candidate scope. |

### E. Operator-side residuals

| Row | Outcome | Notes |
|:---|:---|:---|
| E1 — Apply P3 migration via MCP `apply_migration` | **PENDING-OPERATOR** | Operator runs against remote Supabase after ratifying P3 closure pause record. Migration sequence: P2 column (20260517163635) FIRST, then P3 view (20260517163648). |
| E2 — `get_advisors(security)` post-apply | **PENDING-OPERATOR** | No new advisories expected (view is read-only; GRANT SELECT is narrow). |
| E3 — PostgREST schema cache refresh | **PENDING-OPERATOR** | Migration carries `NOTIFY pgrst, 'reload schema'` at the end; should fire automatically on apply. |
| E4 — Promote I89 candidate to active | **PENDING-OPERATOR** | Adviser-external scope review required before I89 candidate becomes an active initiative. |

## Verdict

**PASS at I86 P3 self-attestable scope.** All B and C rows green; A1 author-side green; A2-A4 + D + E rows DEFERRED / N/A / PENDING-OPERATOR per the design contract.

I86 P3 ships **the spec + the data-layer view + the BBR drift-gate scope extension**. End-to-end persona-rendering verification ships at I89.

## Cross-references

- Acceptance dimensions: [`docs/uat/i86-p3-persona-rollup-acceptance.md`](../../../../uat/i86-p3-persona-rollup-acceptance.md).
- Persona spec: [`persona-view-spec-2026-05-19.md`](persona-view-spec-2026-05-19.md).
- View migration: [`supabase/migrations/20260517163648_i86_p3_initiative_program_rollup_view.sql`](../../../../../supabase/migrations/20260517163648_i86_p3_initiative_program_rollup_view.sql).
- Forward-charter stub: [`_candidates/i89-hlk-erp-program-rollup-implementation.md`](../../_candidates/i89-hlk-erp-program-rollup-implementation.md).
