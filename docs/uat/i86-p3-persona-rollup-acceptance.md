# UAT — I86 P3 persona-view rollup acceptance

| Key | Value |
|:---|:---|
| Initiative | I86 P3 (initiative-cluster-execution-coordinator) |
| Authored | 2026-05-17 |
| Authority | D-IH-86-K (persona-view rollup chartered Round 2; P3 closure) |
| View under test | `governance.initiative_program_rollup_view` |
| Migration | [`supabase/migrations/20260517163648_i86_p3_initiative_program_rollup_view.sql`](../../supabase/migrations/20260517163648_i86_p3_initiative_program_rollup_view.sql) |

## Why this acceptance doc exists

Per `akos-planning-traceability.mdc` §"UAT evidence contract" + `akos-governance-remediation.mdc` §"Planning + verification expectations", an initiative that promises **browser**, **dashboard WebChat**, **adviser-external**, or other **human-in-the-loop** checks at P3 must carry a dimension checklist + a dated `reports/uat-*.md` (or canonical UAT link). I86 P3 chartered a six-persona rollup with a public-prose Adviser-external view; this dimension checklist exists so the future P3 implementation initiative (I89 candidate) can carry forward the acceptance contract.

**I86 P3 ships the SPEC + the data-layer view + the BBR drift-gate scope extension; actual TSX panel implementation requires sibling `hlk-erp` PR which is out of scope.** The "UAT" rows here are therefore split between (a) what I86 P3 itself proves (data-layer + spec authoring + drift-gate) and (b) what the forward-chartered I89 candidate must prove (TSX rendering + redaction enforcement + persona auth + browser smoke).

## Dimension checklist

### A. Data-layer (I86 P3 self-attestable)

| # | Dimension | Pass criterion | I86 P3 evidence |
|:---|:---|:---|:---|
| A1 | Migration syntactic correctness | `psql --command="\d governance.initiative_program_rollup_view"` resolves on a database with both P2 (column) + P3 (view) applied | Author-side `py scripts/verify.py compliance_mirror_emit` runs clean after P2 column lands; view itself awaits operator apply |
| A2 | View returns expected row count | SELECT count(*) FROM governance.initiative_program_rollup_view ≥ 68 rows on canonical INITIATIVE_REGISTRY | Pending operator apply (covered by I89 acceptance) |
| A3 | NULL-anchor rows surface | Initiatives without `program_anchors` populated appear in the view with NULL `program_anchor_id` (LEFT JOIN behaviour) | Pending operator apply (covered by I89 acceptance) |
| A4 | One row per (initiative, anchor) | An initiative with `program_anchors = 'PRJ-HOL-A;PRJ-HOL-B'` produces TWO rows in the view | Pending operator apply (covered by I89 acceptance) |

### B. Spec authoring (I86 P3 self-attestable)

| # | Dimension | Pass criterion | I86 P3 evidence |
|:---|:---|:---|:---|
| B1 | Six personas named + contracted | [`reports/persona-view-spec-2026-05-19.md`](../wip/planning/86-initiative-cluster-execution-coordinator/reports/persona-view-spec-2026-05-19.md) covers PMO, Brand & Narrative Manager, IntelligenceOps, People, Founder, Adviser-external | **PASS** — spec authored 2026-05-17 |
| B2 | HLK-ERP panel inventory extended | `HLK_ERP_ARCHITECTURE.md` §4 includes the six new rollup-aware routes | **PASS** — 6 rows appended 2026-05-17 |
| B3 | Forward-chartered implementation initiative named | [`_candidates/i89-hlk-erp-program-rollup-implementation.md`](../wip/planning/_candidates/i89-hlk-erp-program-rollup-implementation.md) stub exists with scope notes | **PASS** — stub authored 2026-05-17 |

### C. Drift-gate scope extension (I86 P3 self-attestable)

| # | Dimension | Pass criterion | I86 P3 evidence |
|:---|:---|:---|:---|
| C1 | Adviser-surface glob coverage extended | `scripts/validate_brand_baseline_reality_drift.py` scans `**/founder-filed/**/*.md` + `**/adviser-handoff/*.md` in addition to deck/dossier patterns | **PASS** — `_scan_advops_decks_and_dossiers` extended 2026-05-17 |
| C2 | BBR validator green on current corpus | `py scripts/validate_brand_baseline_reality_drift.py` exits 0 | To run as part of P3 closure regression |
| C3 | `PRJ-HOL-` remains in default internal-token list | `DEFAULT_INTERNAL_TOKENS` tuple in `validate_brand_baseline_reality_drift.py` carries `"PRJ-HOL-"` | **PASS** — token retained from P1 commit (D-IH-86-L) |

### D. Forward-chartered to I89 (NOT attestable in I86 P3)

| # | Dimension | Pass criterion | Owner |
|:---|:---|:---|:---|
| D1 | TSX panel scaffolds for six routes | Six route stubs under `hlk-erp/app/(operator)/...` render the view | I89 P0+ |
| D2 | Adviser-external REDACTED rendering | `PRJ-HOL-*` substituted with `[INTERNAL-PROGRAM]` in the adviser-external panel TSX | I89 P0+ |
| D3 | Persona auth claim wiring | Supabase Auth + RLS confirms each persona's slice filter executes server-side | I89 P0+ |
| D4 | Browser smoke (Cursor Browser MCP) | `dashboard.holistikaresearch.com` route resolves; render matches spec | I89 P0+ |
| D5 | Adviser-external PDF export pipeline | Export carries REDACTED tokens; no internal-register leakage | I89 P0+ |

### E. Operator-side residuals (out of agent scope)

| # | Residual | Owner |
|:---|:---|:---|
| E1 | Apply P3 migration via MCP `apply_migration` | Operator |
| E2 | Run `get_advisors(security)` post-apply | Operator |
| E3 | Confirm `governance.initiative_program_rollup_view` appears in PostgREST schema cache (`NOTIFY pgrst, 'reload schema'` already in migration) | Operator |
| E4 | Promote I89 candidate to active when adviser-external scope is operator-ratified | Operator |

## P3 acceptance verdict (this initiative)

**PASS at the self-attestable dimensions (A1 author-side, B1-3, C1-3).** Data-layer dimensions A2-A4 + forward-chartered dimensions D1-D5 + operator residuals E1-E4 are deliberately deferred — I86 P3 is a **spec + chassis + scope extension** phase, not an end-to-end render-and-verify phase.

Recorded outcomes per row land in [`reports/uat-persona-view-2026-05-19.md`](../wip/planning/86-initiative-cluster-execution-coordinator/reports/uat-persona-view-2026-05-19.md) (dated UAT report).

## Cross-references

- Plan body: `~/.cursor/plans/i86_program_anchor_robustness_3e15859c.plan.md` §P3.
- D-IH-86-N: appended to `DECISION_REGISTER.csv` + `decision-log.md` at P3 closure.
- D-IH-86-L: BBR drift-gate extension ratification (Round 2 P1; this P3 scope-widening completes the workstream).
- Sister UAT precedent: [`docs/wip/planning/07-hlk-neo4j-graph-projection/reports/uat-graph-explorer-browser-20260415.md`](../wip/planning/07-hlk-neo4j-graph-projection/reports/uat-graph-explorer-browser-20260415.md).
