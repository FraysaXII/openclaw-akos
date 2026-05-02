---
language: en
status: active
initiative: 48-operator-dossier
report_kind: evidence-matrix
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-02
---

# Initiative 48 — Evidence Matrix

| ID | Observation | Source | Impact | Resolved by |
|:---|:------------|:-------|:-------|:------------|
| **E1** | Operator runs 4-5 CLIs to verify I47 closure (`validate_hlk` + `eval --mode all` + `eval --calibrate` + visit dashboard + read UAT report). No single front door. | Direct operator question (post-I47 P15 close, 2026-05-02 05:31 CET): *"if i, as an human operator want to run the full UAT suite and have a report of everything that happened in a really really well presented manner, like a dossier, can i do that? or is it all cli?"* | Operator-UX gap; verification cycles longer than necessary; risk of missing one CLI in a hurry | P3 (live mode orchestrates all 10 CLIs) + P4 (PDF) + P5 (HTML) |
| **E2** | `scripts/render_dossier.py` (I27 P4) proves the brand-aligned PDF pattern works for the ENISA program dossier. The pipeline (`akos.hlk_pdf_render.render_pdf_branded`) is tested + has WeasyPrint→fpdf2→pandoc fallback chain. Tests at `tests/test_render_dossier.py`. | Read of `scripts/render_dossier.py` lines 1-94 + `akos/hlk_pdf_render.py` lines 1-40 | The HARD work (brand-aligned PDF chain + token system + fallback chain + test discipline) is already done. I48 only needs to AGGREGATE not reinvent. | P4 (reuse `render_pdf_branded`); D-IH-48-H |
| **E3** | `scripts/render_wip_dashboard.py` (I32 P10) proves the auto-render-with-markers pattern (BEGIN_AUTO / END_AUTO + deterministic sha256). Hand-edits above/below markers are preserved. | Read of `scripts/render_wip_dashboard.py` lines 1-50 | Same pattern fits dossier sections that should be ops-editable (e.g. operator commentary above an auto-table). Dossier markdown body adopts the same marker convention. | P2 + P3 (per-section markers) |
| **E4** | I47 P15 closure UAT report (`uat-i47-user-centric-uat-2026-05-02.md`) is dossier-shaped (executive summary → what we built → verification stack → lessons → 9 OPS-* follow-ups). Operator authored it once, end-of-initiative. | Read of `docs/wip/planning/47-user-centric-uat/reports/uat-i47-user-centric-uat-2026-05-02.md` | The closure UAT IS what the dossier should look like — but on-demand at any time, not only at initiative close. The 12-section dossier-section-spec.md derives from this template. | All phases (the closure UAT is the section template) |
| **E5** | I46 P2 drift canary catches real drift today (csv=N neo4j=0 [DRIFT] for 6 axis-6 dimensions before I47 P13 item 1 fix). Output is plain stdout. Without aggregation it's invisible to ops between checks. | I46 P7 closure UAT terminal output | Important signals are emitted but not surfaced. Aggregator + sparkline (P7) make trend visible week-over-week. | P2 (Section 7: Drift canaries) + P7 (sparkline per drift count) |
| **E6** | `compliance.eval_run` table now receives live writes (I47 P13 item 4). 30+ days of operator usage will populate it. Today the mirror is queryable but empty. | Read of `akos/eval_harness/eval_run_writer.py` | The trend-storage substrate exists. Dossier P7 reads it for sparklines (eval pass rate + cost trend). Without dossier the data has no consumer. | P7 (sparkline source from `compliance.eval_run`) |
| **E7** | `Scorecard.to_markdown()` already emits per-persona breakdown + LLM-judge axis sections when those rows exist (I47 P10 + P12). | Read of `akos/eval_harness/v2.py` lines 86-145 | Scorecard markdown is a self-contained section; dossier just embeds it verbatim. No re-rendering needed. | P2 + P3 (embed `Scorecard.to_markdown()` output verbatim into Section 3: Eval health) |
| **E8** | Cursor browser MCP is available in this environment (`cursor-ide-browser` server). I46 P7 + I47 P15 used it to capture OpenClaw Control SPA screenshots during live UAT. | I46 + I47 closure UAT artifacts (screenshots taken during browser-tabs / browser-navigate / browser-take-screenshot calls) | Live screenshots embedded in dossier give operator visual confirmation alongside data tables. Especially valuable for stakeholder reviews where the data alone doesn't convey "we tested it live." | P3 (`--screenshots` opt-in flag; best-effort) |
| **E9** | `BRAND_VISUAL_PATTERNS.md` is the canonical brand token SSOT; `BRAND_TOKENS_LIGHT/DARK` in `akos/hlk_pdf_render.py` mirrors it; `tests/test_render_dossier.py::test_brand_tokens_light_match_pattern_doc` enforces drift-free sync. | Read of `.cursor/rules/akos-docs-config-sync.mdc` line 110 | I48 stays brand-token-clean by reusing `render_pdf_branded` + `BRAND_TOKENS_*` (no token re-declaration in dossier code). HTML mode derives CSS variables from the same Python tokens. R-48-10 mitigation. | P4 (PDF mode) + P5 (HTML mode shares same tokens via CSS variable map) |
| **E10** | Per-section staleness is configurable per `dossier-section-spec.md` (P0 artifact); some sections (validate_hlk) cheap to re-run; others (Tier B) expensive. Default policy: read artifact ≤24h fresh; otherwise re-run. | Section-spec design (P0) + cost asymmetry observed in I45 P4 cost ceiling rows | Operator gets fast snapshot mode by default; live mode upgrades freshness; tier-b mode pulls Tier B latest. Hybrid posture matches I45 P4 + I47 P12 cost discipline. | D-IH-48-E + P2/P3/P5 |
| **E11** | The `eval-tier-b.yml` workflow (I45 P6 + I47 P14 4-D matrix) already produces per-cell scorecard artifacts. Adding a trailing dossier step is additive (no matrix change). | Read of `.github/workflows/eval-tier-b.yml` | P8 ships dossier-as-artifact for every Tier B weekly run with zero matrix risk. The 4-D matrix produces 10 cells = 10 dossier artifacts per weekly run. | P8 |
| **E12** | The `validate_configs.py::TestOpenclawConfig` 2 pre-existing failures (operator-local `openclaw.json` schema mismatch `sandbox.mode='all'` vs allowed `'off'\|'strict'`) currently surface only when running pytest. Dossier surfaces them prominently in Section 2 (schema/governance) under "Known operator-local config issues". | I47 P15 pytest run (1180 passed / 5 skipped / 0 failed excl. these 2) | Operator-local issues become visible without scrolling pytest output. Dossier highlights them as operator-actionable. | P2 (Section 2: schema/governance) |

## Cross-references to other initiatives

- **Initiative 27 P4** — built `scripts/render_dossier.py` for ENISA (E2 source: brand-aligned PDF chain proven; the exemplar)
- **Initiative 32 P10** — built `scripts/render_wip_dashboard.py` (E3 source: auto-render-with-markers pattern reference)
- **Initiative 45 P4 + P6** — built `compliance.eval_run` mirror table + Tier B GitHub Action (E6 + E11 sources for trend storage + CI integration)
- **Initiative 46 P2** — built drift canary (E5 source: signal-without-aggregation example)
- **Initiative 47 P10 + P12 + P13 item 4** — extended `Scorecard.to_markdown()` for per-persona + LLM-judge sections + wired `compliance.eval_run` live writes (E7 + E6 dependencies)
- **Initiative 47 P14** — extended Tier B to 4-D matrix (E11 dependency for per-cell dossier artifact in P8)
- **Initiative 47 P15** — closure UAT report shape (E4 source: section template)
- **Initiative 49 (future)** — multi-judge consensus + benchmark scoring; potential consumer of dossier trend lines for cross-judge variance analysis (D-DEFER-48-α target)
