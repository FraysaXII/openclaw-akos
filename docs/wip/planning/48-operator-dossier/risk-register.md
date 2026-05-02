---
language: en
status: active
initiative: 48-operator-dossier
report_kind: risk-register
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-02
---

# Initiative 48 — Risk Register

10 risks identified during planning. Severity is L / M / H; likelihood same scale.

## Active risks

### R-48-1 — Aggregator coupling: a CLI's stdout format changes silently breaks dossier section (M / M)
**Trigger:** A future eval.py / validate_hlk / drift canary refactor changes stdout shape; dossier section silently empty or garbled.

**Mitigation:** Per-section parser tested independently in `tests/test_dossier_sources.py`; PLACEHOLDER text emitted on parse failure (visible in dossier rather than crash); sticky integration test asserts each parser handles its CLI's actual current output (refresh-on-CLI-version-change pattern).

**Rollback:** Parser refactor in the affected section module only; format pinning via cassette comparison if necessary.

### R-48-2 — PDF rendering dependency: WeasyPrint not installed on operator laptop (M / L)
**Trigger:** Operator runs `--format pdf` without WeasyPrint; current chain falls through to fpdf2 → pandoc → markdown sidecar.

**Mitigation:** Soft-success markdown sidecar (existing `render_pdf_branded` fallback); operator UX clearly states sidecar is fallback in dossier manifest (`pdf_status: "sidecar_fallback"`); `requirements-export.txt` already documents the opt-in install (per I22 P6 pattern).

**Rollback:** Operator installs WeasyPrint; documented in USER_GUIDE.

### R-48-3 — HTML mode XSS surface (L / H)
**Trigger:** Embedded data (CLI stdout, persona names, scenario text, OPS-* follow-ups) contains malicious HTML/script that the renderer doesn't escape.

**Mitigation:** **NO JS framework** (D-IH-48-I); inline SVG sparklines only (no `<img src>` references); markdown library `markdown` already escapes user content; standalone-file invariant test asserts no external references; CSP-equivalent meta tag in HTML head (`Content-Security-Policy: default-src 'self' 'unsafe-inline'`); explicit HTML escape in section assembler.

**Rollback:** Disable HTML mode (--format md|pdf only); ship without HTML until escape audit complete.

### R-48-4 — `--mode tier-b` cost runaway (L / M)
**Trigger:** Operator runs `--mode tier-b` without env opt-in; dossier triggers full Tier B matrix; spend spikes.

**Mitigation:** `MAX_DOSSIER_USD` env cap (default $2/run; per D-IH-48-L); `AKOS_DOSSIER_TIER_B=1` env opt-in REQUIRED even when other Tier B keys (OPENAI/ANTHROPIC/etc.) are set; per-CLI cost roll-up reported in manifest; refuses to run with explicit error if cap exceeded.

**Rollback:** Operator lowers cap; reverts to `--mode live` or `--mode snapshot`.

### R-48-5 — Trend storage growth (`compliance.dossier_run` unbounded) (L / L)
**Trigger:** Mirror table grows unbounded over months/years; query cost climbs; dashboard render slows.

**Mitigation:** `POL-DOSSIER-RUN-RETENTION-V1` (180 days OR 1000 rows max; whichever hits first); operator-reviewed quarterly per policy cadence; partial index `(mode, started_at DESC)` keeps trend query cost flat regardless of total row count.

**Rollback:** Drop oldest rows via DELETE on retention exceedance; manual operator trigger; never automatic delete (audit trail).

### R-48-6 — Dossier becomes its own SSOT competing with UAT closure reports (M / M)
**Trigger:** Operator starts treating dossier as the canonical UAT output; ignores per-initiative phase reports + closure UAT; loss of per-initiative provenance.

**Mitigation:** Dossier explicitly CITES the UAT closure reports as SOURCE in every section (cross-link to `docs/wip/planning/<NN>/reports/uat-*.md`); never re-defines metrics; phase reports remain canonical and dossier reads them; cross-link in dossier executive summary explicitly says "this dossier aggregates reports; for per-initiative provenance see linked closure UAT".

**Rollback:** Operator marks dossier sections AUTO-RENDER-ONLY (no hand-edits); dossier loses its competing-SSOT role; closure reports stay primary.

### R-48-7 — Markdown→PDF chain fallback loses styling (M / M)
**Trigger:** WeasyPrint→fpdf2→pandoc→sidecar fallback fires on operator laptop; PDF mode degrades from brand-aligned to plain-text sidecar.

**Mitigation:** Same chain ENISA dossier already uses (proven; tested in `tests/test_render_dossier.py`); operator-visible sidecar warning in manifest (`pdf_status: "sidecar_fallback"`); HTML mode independently produces brand-aligned output (no WeasyPrint dependency); dossier executive summary cell reports which formats succeeded.

**Rollback:** Install WeasyPrint at operator-side; docs/CONTRIBUTING.md already documents this per I22 P6.

### R-48-8 — Operator confusion when dossier shows different state than live system (M / M)
**Trigger:** Operator runs `--mode snapshot` (reads cache) and sees data older than what's in the live system; dossier looks "wrong" relative to a fresh `validate_hlk` run.

**Mitigation:** Manifest shows per-section `data_age_seconds`; sections older than configured staleness threshold (D-IH-48-E; default 24h) carry visible STALE badge in markdown ("⚠ stale: last refreshed 36h ago"); `--mode live` always re-runs critical sections; per-section spec lists each section's staleness budget.

**Rollback:** Operator runs `--mode live` (forces re-run regardless of cache age).

### R-48-9 — Per-initiative scoping breaks when WIP_DASHBOARD format evolves (L / L)
**Trigger:** A future change to `WIP_DASHBOARD.md` BEGIN_AUTO/END_AUTO marker contract; dossier `--initiative <NN>` filter breaks because it can't parse the dashboard.

**Mitigation:** Dossier WIP_DASHBOARD parser uses the SAME marker contract as `render_wip_dashboard.py` (single SSOT for marker syntax); changes to that contract caught by `tests/test_wip_dashboard_render.py` (existing); dossier `tests/test_dossier_sources.py::test_wip_dashboard_marker_parse_stable` adds a sticky-test safeguard.

**Rollback:** Update parser; pin marker contract in WIP_DASHBOARD comments.

### R-48-10 — Brand drift: dossier ships independently and brand tokens evolve in BRAND_VISUAL_PATTERNS.md without dossier update (L / L)
**Trigger:** Brand Manager updates `BRAND_VISUAL_PATTERNS.md` `BRAND_TOKENS_LIGHT/DARK`; `akos/hlk_pdf_render.py` lags; dossier renders with stale brand colors.

**Mitigation:** Dossier reuses `BRAND_TOKENS_LIGHT/DARK` from `akos/hlk_pdf_render.py` (single SSOT; no token re-declaration in `akos/dossier/`); existing test `test_brand_tokens_light_match_pattern_doc` already enforces sync between markdown spec and Python constants; if test fails, both PDF + HTML mode regen automatically when tokens fix; dossier inherits the existing drift safeguard for free.

**Rollback:** Token sync via existing process; existing test catches drift; no I48-specific remediation needed.

## Risks closed before P0

(None — initiative just opened.)

## Cross-references

- I22 P6 PDF chain (R-48-2 + R-48-7 mitigation lineage)
- I26 service_role rotation pattern → R-48-4 cost ceiling enforcement model + RLS posture for new mirror
- I27 P4 ENISA dossier → R-48-7 fallback chain proof
- I32 P10 WIP_DASHBOARD → R-48-9 marker contract (existing test suite catches drift)
- I45 P4 cost ceiling pattern → R-48-4 spend cap + R-48-5 retention pattern
- I46 P2 drift canary → R-48-1 graceful-degradation pattern (PLACEHOLDER on parse failure)
- I47 P9 D-IH-47-L real-chaos opt-in env-gate → R-48-4 same env-opt-in posture for cost-bearing operations
- I47 P11 R-47-9 OVERLAY_HLK_GRAPH swap → analogous architectural decision (swap a heavy element when a contextual feature is active; here: drop sparklines from PDF if cumulative size approaches font-rendering limit)
