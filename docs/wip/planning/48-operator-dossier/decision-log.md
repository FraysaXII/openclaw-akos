---
language: en
status: active
initiative: 48-operator-dossier
report_kind: decision-log
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-02
---

# Initiative 48 — Decision Log

12 decisions seeded with default positions per the cursor plan. Operator pre-ratified at greenlight (2026-05-02 05:46 CET).

## D-IH-48-A — Module location: package vs single file

**Decision:** New `akos/dossier/` Python package (not single-file `akos/dossier.py`).

**Alternatives considered:**
- Single-file `akos/dossier.py` (~600 lines; simpler import; harder to test in isolation)

**Rationale:** Package mirrors `akos/eval_harness/` shape from I45 (which now has 7 modules: `__init__`, `v2`, `cassette`, `cost_obs`, `adversarial`, `promotion`, `persona`, `judge`, `eval_run_writer`). Package gives room for `run.py` (DossierRun) + `sections.py` (12 Section subclasses) + `sparkline.py` (SVG generator) + `html_render.py` (HTML mode) + `runner.py` (live mode CLI orchestrator) + `pdf_render.py` (PDF mode thin wrapper) + `dossier_run_writer.py` (P7 trend storage). Each ~100-200 lines; testable in isolation.

**Reversibility:** Med (consolidation back to single-file would need to update all imports).

---

## D-IH-48-B — Output formats day 1

**Decision:** All 3 formats day 1 (md + pdf + html); per-format flag `--format md|pdf|html|all`; `all` is default.

**Alternatives considered:**
- MD only first; PDF + HTML later (3-day initiative; smaller scope; doesn't extract full value of the existing PDF chain)
- MD + PDF only (skips HTML; HTML is the most operator-accessible format on a laptop)

**Rationale:** "Extract full value out of our capabilities" (operator language). The PDF chain (`akos.hlk_pdf_render.render_pdf_branded`) is proven via ENISA dossier; HTML adds no new infrastructure (markdown library already in repo + brand CSS variables derived from existing `BRAND_TOKENS_LIGHT/DARK`). Shipping all 3 day 1 makes the dossier immediately useful in any operator context.

**Reversibility:** Trivial (just change default flag value).

---

## D-IH-48-C — Aggregation modes: snapshot / live / tier-b

**Decision:** 3 modes (snapshot | live | tier-b); snapshot default; tier-b env-gated `AKOS_DOSSIER_TIER_B=1`.

**Alternatives considered:**
- 2 modes (snapshot + live; defer tier-b to I49)
- 1 mode (always live; simpler but slow + expensive default; bad operator UX for quick checks)

**Rationale:** Snapshot is ~10s and CI-safe (default); live is ~5min and full-coverage (operator opt-in); tier-b extends with Tier B model regression (env-gated cost discipline; same posture as I47 P9 real-chaos `AKOS_REAL_CHAOS_OK=1`).

**Reversibility:** Trivial (modes are independent code paths).

---

## D-IH-48-D — Section ordering

**Decision:** Executive summary first → schema/governance → eval health → persona library → adversarial → recovery → drift → operational health → external repos → open follow-ups → trend lines → appendix.

**Alternatives considered:**
- Drift / operational health first (operations-led ordering; less operator-friendly for a non-debugging read)
- Appendix first (data-first; useless for a "dossier" presentation context)

**Rationale:** Executive summary first matches dossier convention (ENISA P4 dossier opens the same way); appendix last keeps raw provenance available without polluting the read flow. Per-section spec details in [`dossier-section-spec.md`](dossier-section-spec.md).

**Reversibility:** Trivial (per-section spec config-driven).

---

## D-IH-48-E — Per-section data-source policy

**Decision:** Read existing artifact when fresh (≤24h); re-run CLI otherwise. Configurable per section via `dossier-section-spec.md`.

**Alternatives considered:**
- Always re-run (slow; expensive; defeats snapshot mode)
- Always read (fast but stale; defeats live mode)

**Rationale:** Hybrid policy gives operator control: snapshot mode reads cache (fast); live mode forces re-run regardless of staleness; tier-b runs full Tier B cells. Per-section configurability handles cost asymmetry (validate_hlk cheap to re-run; Tier B expensive).

**Reversibility:** Med (operator can override staleness threshold via env var or per-section spec edit).

---

## D-IH-48-F — Trend storage substrate

**Decision:** New `compliance.dossier_run` Supabase mirror table (BIGSERIAL run_id + JSONB section_metrics + git_sha + manifest_sha256). Plus operator-local `artifacts/uat-dossier/index.json` for offline mode.

**Alternatives considered:**
- Just operator-local JSON (no Supabase dependency; loses cross-machine queryability)
- Reuse `compliance.eval_run` (semantic conflation: eval_run is per-eval-row; dossier_run is per-dossier-render-invocation; different cardinality)

**Rationale:** Mirror provides the cross-time / cross-machine aggregation surface needed for sparklines + Tier B PR comments. Operator-local index handles offline mode (no SUPABASE_URL set).

**Reversibility:** Med (drop column; existing artifacts still queryable from operator-local index).

---

## D-IH-48-G — Dossier artifact retention

**Decision:** Operator-local + gitignored (regenerable per run). CHANGELOG references closure-cycle dossier sha256 only.

**Alternatives considered:**
- Git-tracked dossiers (size bloat; markdown is regenerable; PDF binary diff noise)
- Cloud blob storage (operator-local already serves the use case; cross-machine via mirror per D-IH-48-F)

**Rationale:** Same posture as `artifacts/calibration/`, `artifacts/chaos/`, `artifacts/agent-memory-triggers/` (all regenerable; gitignored except README).

**Reversibility:** Trivial (.gitignore line).

---

## D-IH-48-H — PDF rendering chain

**Decision:** Reuse `akos.hlk_pdf_render.render_pdf_branded` unchanged. Same WeasyPrint → fpdf2 → pandoc fallback chain.

**Sub-decision D-IH-48-H1 (deferred to P4):** Reuse `profile="dossier"` enum value vs add new `profile="uat_dossier"` value. Default tentative: extend with `"uat_dossier"` (cover layout differs slightly from ENISA — UTC timestamp + UAT mode label vs ENISA program id + issue date).

**Alternatives considered:**
- New PDF pipeline (Playwright-based / wkhtmltopdf / etc.) — rejected; current chain is proven + fallback-safe
- Always reuse `"dossier"` profile (cover may not match UAT context)

**Rationale:** The hard work is done; no new dependency added; WeasyPrint→fpdf2→pandoc fallback chain handles operator environment variance gracefully.

**Reversibility:** Trivial (delete `pdf_render.py` thin wrapper; revert PDF flag).

---

## D-IH-48-I — HTML interactivity scope

**Decision:** Static + native `<details>` collapsible (no JavaScript framework / Alpine.js / htmx). Inline SVG sparklines (no `<img src>` references).

**Alternatives considered:**
- Alpine.js for collapsible / search (~10kb; adds dependency; XSS surface)
- htmx for live-reload (~14kb; adds server requirement; not standalone)
- Vega-Lite charts (richer than SVG sparklines; CDN dependency; deferred to D-DEFER-48-α)

**Rationale:** R-48-3 mitigation: no JS = no XSS surface; standalone-file invariant; operator can email the HTML to anyone without security review. Native `<details>` is browser-native and accessibility-friendly.

**Reversibility:** Trivial (HTML mode is self-contained; can add JS later if operator wants interactivity).

---

## D-IH-48-J — CI integration timing

**Decision:** Ship in P8 (this initiative).

**Alternatives considered:**
- Defer to I49 (cleaner I48 closure; loses the natural pairing of "dossier ships" + "Tier B emits dossier")

**Rationale:** `eval-tier-b.yml` already exists from I45 P6 + I47 P14 (4-D matrix). Adding a trailing dossier-render step is additive (no matrix change). Bundling CI integration with the dossier ship gives operator a complete workflow at I48 close (vs partial workflow + manual follow-up).

**Reversibility:** Med (revert eval-tier-b.yml step; delete dossier-on-pr.yml).

---

## D-IH-48-K — Operator-facing CLI surface

**Decision:** New `scripts/render_uat_dossier.py` (vs extending `scripts/eval.py`).

**Alternatives considered:**
- Extend `scripts/eval.py` with `--dossier` mode (existing CLI; familiar; but eval.py already grew flags in I45/I47; further growth dilutes its purpose)
- Subcommand `scripts/eval.py dossier` (cleaner than flag; still in eval.py)

**Rationale:** "One script per concern" cursor convention. The dossier orchestrates ~10 CLIs (eval.py is just one of them); making the dossier renderer ITS OWN script keeps eval.py focused on eval. Mirrors the I27 P4 `scripts/render_dossier.py` exemplar (program-specific dossier got its own script).

**Reversibility:** Trivial (add flag/subcommand to eval.py later if operator changes mind).

---

## D-IH-48-L — Cost discipline for `--mode tier-b`

**Decision:** Per-mode cost cap `MAX_DOSSIER_USD` env (default $2/run). `AKOS_DOSSIER_TIER_B=1` env opt-in required even when other Tier B keys (OPENAI/ANTHROPIC/etc.) are set.

**Alternatives considered:**
- No cap (relies on per-CLI caps; risk of compound spend)
- Higher cap ($10/run; matches Tier B budget but defeats snapshot-mode operator discipline)

**Rationale:** R-48-4 mitigation. Same env-gate posture as I47 D-IH-47-L real-chaos: explicit operator opt-in for cost-bearing operations; default-safe.

**Reversibility:** Trivial (env var; operator override).

---

## Decisions deferred (out of I48 scope)

- **D-DEFER-48-α** — Vega-Lite interactive charts (richer than SVG sparklines). Defer to I49 if operator wants drill-down.
- **D-DEFER-48-β** — Multi-language dossier (es / fr). Defer until first non-en operator audience requests it.
- **D-DEFER-48-γ** — Live MCP-tool-call traces in dossier. Needs Langfuse plumbing; revisit in I49.
- **D-DEFER-48-δ** — Dossier-as-SaaS endpoint (web service that emits dossier on POST). Product scope; not internal tooling.
- **D-DEFER-48-ε** — KiRBe / hlk-erp side dossier (cross-repo). Tracked separately under `EXTERNAL_REPO_CONTRACT.md` extension if those repos want the same pattern.
