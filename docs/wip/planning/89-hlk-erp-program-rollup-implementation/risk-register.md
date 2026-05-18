# I89 — Risk Register

> Risk rows for I89 (HLK-ERP persona-rollup panel implementation). Phase-anchored summary in [`master-roadmap.md`](master-roadmap.md) §"Risk register preview (inline)".

## R-IH-89-1 — BBR FAIL state blocks CI until ADVOPS triage closes

- **Risk**: Per D-IH-89-E, `scripts/validate_brand_baseline_reality_drift.py` flips from `INFO` to `FAIL` at I89 P0. The 7 pre-existing `PRJ-HOL-FOUNDING-2026` leaks in `_assets/advops/**/founder-filed/**/*.md` will FAIL the CI gate until ADVOPS triage (OPS-86-5) closes them. If ADVOPS slips beyond 5 days AND a blocking I89 commit is urgent, every CI run fails.
- **Likelihood**: High (the 7 leaks are pre-existing; until triage closes, every run hits them).
- **Impact**: High (CI-block prevents merge of subsequent I89 phase commits; could stall execution mid-week).
- **Mitigation**:
 - Operator accepted as feature not bug (D-IH-89-E). The CI-block surfaces ADVOPS triage urgency.
 - ADVOPS triage prioritised same-week (OPS-86-5 assigned to Brand & Narrative Manager + ADVOPS engagement co-owner).
 - Hot-fix lane: temporarily revert BBR gate to `INFO` if ADVOPS slips >5d AND a blocking I89 commit is urgent. Revert is one-line in `release-gate.py`. Re-flip immediately after the blocking commit lands. Document the revert + re-flip in CHANGELOG.md.
- **Owner**: PMO (gate flip) + Brand & Narrative Manager (ADVOPS triage).

## R-IH-89-2 — Adviser-external panel accidentally imports internal RollupTable

- **Risk**: A future refactor or auto-import (VSCode IntelliSense suggestion, Cursor AI suggestion, manual edit) accidentally imports `RollupTable.tsx` inside `app/(public-advops)/program-rollup/page.tsx` — silently breaking the security-by-isolation pattern.
- **Likelihood**: Medium (auto-import tooling is the most common refactor source).
- **Impact**: Critical (would surface internal-register tokens to Adviser-external audience; potential reputation damage; breaches the I66 BBR doctrine).
- **Mitigation**:
 - Component isolation by directory (`components/program-rollup/RollupTable.tsx` vs `components/program-rollup/RedactedRollupTable.tsx`).
 - ESLint custom rule `no-restricted-imports` in `hlk-erp/.eslintrc.json`:
 ```json
 "no-restricted-imports": ["error", {
   "patterns": [{
     "group": ["**/RollupTable", "**/RollupTable.tsx"],
     "message": "Adviser-external routes must use RedactedRollupTable, not RollupTable."
   }]
 }]
 ```
 (scoped via `overrides` to `app/(public-advops)/**`).
 - CI in `hlk-erp` runs `pnpm lint` on every PR — the ESLint rule fires at PR-time, blocking merge.
- **Owner**: System Owner (ESLint rule) + Brand & Narrative Manager (rule rationale doctrine ownership).

## R-IH-89-3 — Redaction matrix in TS drifts from BBR canonical Markdown

- **Risk**: The TypeScript `bbr-redaction-matrix.ts` is a sibling-repo translation of `BRAND_BASELINE_REALITY_MATRIX.md`. If the canonical Markdown matrix is extended (new internal-register token added) and the TS table is not synced, the new token leaks to Adviser-external rendering.
- **Likelihood**: Medium (cross-repo sync is the most fragile coordination point).
- **Impact**: High (new internal-register token leaks; partially defeats the redaction discipline).
- **Mitigation**:
 - Unit test `bbr-redaction-matrix.test.ts` in `hlk-erp` parses the canonical Markdown matrix at test time (via cross-repo include or vendored snapshot updated by `SOP-CROSS_REPO_SCHEMA_PROPAGATION_001`) and asserts every internal-register token has a corresponding TS table entry.
 - CI in `hlk-erp` fails the test if drift detected.
 - Schema propagation SOP (`SOP-CROSS_REPO_SCHEMA_PROPAGATION_001.md`) covers the cross-repo coordination — when the AKOS canonical changes, an automated PR opens against `hlk-erp` to update the TS table.
- **Owner**: Brand & Narrative Manager (matrix doctrine) + System Owner (sync automation).

## R-IH-89-4 — I75 not active at P2 — Research route renders 'Coming when I75 actives'

- **Risk**: I75 (Research-area governance) is candidate; P2 ships a Research route placeholder. If operator browses Research route before I75 actives, they see a coming-soon component rather than data.
- **Likelihood**: Low (operator informed at P2 demo).
- **Impact**: Low (UX friction; no security or correctness risk).
- **Mitigation**: Coming-soon component renders a link to I75 candidate at `docs/wip/planning/_candidates/i75-research-area-governance.md` so operator sees inception path. When I75 actives, the route auto-switches to live data (driven by an I75-status flag).
- **Owner**: PMO (status flag) + Research Lead / interim KM Officer (I75 inception).

## R-IH-89-5 — RLS policy on base tables breaks existing read patterns

- **Risk**: P1 ships six RLS policies on `compliance.initiative_registry_mirror` + `compliance.program_registry_mirror`. If existing `hlk-erp` pages read these tables under a different JWT claim (or no claim), they break.
- **Likelihood**: Medium (existing pages exist — `hlk-erp/app/(operator)/operations/pmo/initiatives/` is one).
- **Impact**: High (a previously-working operator surface goes blank or 403s).
- **Mitigation**:
 - P1 §P1.7 inline-ratify gate surfaces all six RLS policies + their exclusion sets BEFORE apply.
 - Mid-P1 self-checkpoint runs a SELECT-survey of existing consumers (every `hlk-erp` page currently reading `initiative_registry_mirror`) and confirms persona claims cover them.
 - Default-allow fallback policy for `authenticated` role with no specific persona claim — preserves backward compatibility until all consumers migrate. Documented in the P1 RLS migration SQL.
- **Owner**: System Owner (RLS migration) + PMO (consumer survey).

## R-IH-89-6 — PDF export Playwright Chromium crash on Windows Python 3.14+

- **Risk**: Per [`akos-planning-traceability.mdc`](../../../../.cursor/rules/akos-planning-traceability.mdc) §"UAT evidence contract" footnote: Playwright on Windows + Python 3.14+ preview interpreters may crash bundled Chromium (`0xC0000005`).
- **Likelihood**: Low (operator runs CPython 3.12.x; AKOS standard interpreter).
- **Impact**: Medium (PDF export runbook fails; advisor handoff blocked).
- **Mitigation**:
 - Pin Python 3.12.x in `scripts/export_adviser_program_rollup_pdf.py` docstring.
 - If 3.14+ is required by other tooling, document alternative: run the export via Cursor IDE Browser MCP against the live `/program-rollup` Adviser-external panel + manually save-as-PDF.
- **Owner**: System Owner.

## R-IH-89-7 — MANDATORY public-prose pause at P3 + P4 stalls if reviewer unavailable

- **Risk**: P3 + P4 are MANDATORY pause-points per `akos-agent-checkpoint-discipline.mdc` (public-prose category). If Brand & Narrative Manager unavailable for multi-day window, execution stalls.
- **Likelihood**: Medium (single-reviewer dependency).
- **Impact**: Medium (delay, not failure).
- **Mitigation**:
 - Pre-schedule operator review windows at P0 (Brand & Narrative Manager committed to a P3 + P4 review slot).
 - Pause-records skimmable per `akos-agent-checkpoint-discipline.mdc` — mechanical evidence first (10 lines).
 - Soft-clear NOT applicable (public-prose category is non-skippable per the rule).
 - Backup reviewer: Founder may stand in for Brand & Narrative Manager during prolonged absence (founder has BBR doctrine authority).
- **Owner**: PMO (scheduling) + Brand & Narrative Manager (primary reviewer).

## R-IH-89-8 — Adviser-external panel discovers BBR matrix coverage gap

- **Risk**: At P3 implementation time, the Adviser-external panel may surface internal-register tokens NOT yet in the BBR matrix (e.g. a new column name, a new persona-alignment value).
- **Likelihood**: Medium (real-world rendering surfaces edge cases the static matrix didn't anticipate).
- **Impact**: Medium (one or two tokens may need translation patch; not a doctrine failure).
- **Mitigation**:
 - P3 mid-checkpoint surfaces uncovered token list via DOM scrape.
 - BBR matrix extended via I66 follow-up commit (not blocking I89 — extend matrix + extend matrix unit test).
 - If Adviser-external rendering would surface an uncovered token, the redaction matrix has a default-redact fallback: any token matching `/^PRJ-HOL-/` or `/^INIT-OPENCLAW_AKOS-/` or `/^D-IH-\d+-[A-Z]+$/` regex auto-redacts to `[INTERNAL]` even without an explicit matrix entry. Documented in `bbr-redaction-matrix.ts`.
- **Owner**: Brand & Narrative Manager.

## Cross-references

- [`master-roadmap.md`](master-roadmap.md) §"Risk register preview (inline)".
- [`decision-log.md`](decision-log.md) §"D-IH-89-E" (R-IH-89-1 hot-fix lane reference).
- [`akos-brand-baseline-reality.mdc`](../../../../.cursor/rules/akos-brand-baseline-reality.mdc) §"Drift gate" — R-IH-89-3 mitigation rationale.
- [`akos-agent-checkpoint-discipline.mdc`](../../../../.cursor/rules/akos-agent-checkpoint-discipline.mdc) §"Pause-point depth heuristic" — R-IH-89-7 non-skippable rationale.
