---
language: en
status: active
initiative: 48-operator-dossier
report_kind: phase-report
phase: P1
program_id: shared
plane: ops
authority: System Owner
last_review: 2026-05-02
---

# I48 P1 — `akos/dossier/` package skeleton (D-IH-48-A)

## What shipped

### `akos/dossier/__init__.py` — public API

Re-exports the 4 P1 modules + 12 Section subclasses + helper constants. Mirrors the `akos/eval_harness/` package shape from I45.

### `akos/dossier/run.py` — `DossierRun` + `DossierFilter` + `DossierSectionResult`

| Public symbol | Purpose |
|:---|:---|
| `DossierRun` | One dossier render invocation; aggregates 12 sections + manifest |
| `DossierFilter` | Per-run filter for `--initiative` / `--persona` / `--since` (P6) |
| `DossierSectionResult` | One section's gather + render outputs (status / markdown / html / metrics / data_age) |
| `VALID_MODES` | `("snapshot", "live", "tier-b")` per D-IH-48-C |
| `VALID_FORMATS` | `("md", "pdf", "html", "all")` per D-IH-48-B |
| `DEFAULT_MAX_DOSSIER_USD` | $2/run per D-IH-48-L |
| `is_tier_b_opted_in()` | D-IH-48-L: `AKOS_DOSSIER_TIER_B=1` env opt-in |
| `resolve_max_dossier_usd()` | Reads `MAX_DOSSIER_USD` env with default + invalid-fallback |
| `resolve_run_dir(run, base)` | Computes UTC-stamped path `artifacts/uat-dossier/uat-dossier-<UTC>/` |
| `to_markdown()` | Renders all 12 sections in 1..12 order regardless of add() order (D-IH-48-D invariant) |
| `to_manifest()` | Builds sha256 + section_metrics + run config + file hashes |
| `to_json()` | Round-trippable scorecard JSON |

### `akos/dossier/sections.py` — `Section` ABC + 12 subclasses

| ID | Class | default_open_html | staleness_threshold_hours | status emitted |
|:--:|:---|:---:|:---:|:---:|
| 1 | `Section01ExecutiveSummary` | True | 0 (always re-aggregated) | PASS |
| 2 | `Section02SchemaGovernance` | True | 12 | SKIP (P1 placeholder) |
| 3 | `Section03EvalHealth` | True | 12 | SKIP |
| 4 | `Section04PersonaCalibration` | True | 24 | SKIP |
| 5 | `Section05Adversarial` | True | 24 | SKIP |
| 6 | `Section06Recovery` | False | None (NEVER auto-refresh) | SKIP |
| 7 | `Section07DriftCanaries` | True | 24 | SKIP |
| 8 | `Section08OperationalHealth` | False | 12 | SKIP |
| 9 | `Section09ExternalRepos` | False | 168 (weekly) | SKIP |
| 10 | `Section10GovernanceDebt` | True | 0 (always re-parse) | SKIP |
| 11 | `Section11TrendLines` | True | 0 (always re-query) | INFO + INSUFFICIENT-DATA |
| 12 | `Section12Appendix` | False | 0 (always emitted) | INFO |

`SECTION_CLASSES` tuple enforces the 1..12 ordering invariant (D-IH-48-D). Each subclass implements `gather() / render_markdown() / metrics_for_trend()` per the dossier-section-spec.md contract; `render_html()` defaults to `<details>` wrapping. P1 ships SKELETON gather() functions that emit PLACEHOLDER text per the contract — data sources land in P2.

### `akos/dossier/sparkline.py` — inline SVG generator

| Public symbol | Purpose |
|:---|:---|
| `INSUFFICIENT_DATA_PLACEHOLDER` | Returned when `len(values) < 2` |
| `render_sparkline_svg(values, label, width, height, ...)` | Deterministic SVG; no JS / external CDN |
| `SPARKLINE_STROKE_COLOR` | `BRAND_TOKENS_LIGHT["accent_primary"]` (teal) |
| `SPARKLINE_AXIS_COLOR` | `BRAND_TOKENS_LIGHT["border"]` (light grey) |

Validates as XML (`xml.etree.ElementTree.fromstring`); deterministic across runs (same input → identical bytes); brand-stroke matches `accent_primary` token (E9 single SSOT; sticky test asserts equality with `BRAND_TOKENS_LIGHT`); XML-escapes label for XSS hygiene (R-48-3).

### `akos/dossier/html_render.py` — markdown→HTML scaffold

| Public symbol | Purpose |
|:---|:---|
| `BRAND_CSS_VARS` | Derived `:root { --c-accent-primary: ...; ... }` block from `BRAND_TOKENS_LIGHT` (single SSOT) |
| `section_to_html_details(...)` | Emits `<details id="section-NN">` with `default_open` toggle |
| `BRAND_TOKENS_LIGHT/DARK` | Re-exported from `akos.hlk_pdf_render` for caller convenience |

P1 minimal: section body wrapped in `<pre>` + HTML-escape (R-48-3). P5 will replace `<pre>` with proper markdown library invocation + brand-CSS body styling. Standalone-file invariant (no external references) is the P5 closure check.

## R-47-9 / R-48-9 / E9 cross-cutting

The brand-token discipline established by I22 P6 + I27 P1 (single SSOT in `BRAND_VISUAL_PATTERNS.md`; mirrored to `BRAND_TOKENS_LIGHT/DARK` in `akos.hlk_pdf_render`; drift-checked by `tests/test_render_dossier.py::test_brand_tokens_light_match_pattern_doc`) is reused by I48 dossier WITHOUT re-declaring tokens:

- `sparkline.py` references `BRAND_TOKENS_LIGHT["accent_primary"]` (teal) for stroke
- `html_render.py` derives `:root { --c-* }` CSS variables programmatically from `BRAND_TOKENS_LIGHT`
- Sticky tests (`test_default_stroke_color_is_brand_accent_primary`, `test_brand_tokens_light_dark_re_exported`, `test_brand_css_vars_includes_all_light_tokens`) catch any future drift between dossier code and brand SSOT.

## Verification

- 117 new tests in 4 NEW suites:
  - `tests/test_dossier_run.py` — 22 tests (constants + dataclass shape + ordering + manifest + env helpers)
  - `tests/test_dossier_sections.py` — 56 tests (12 parametrized × 3 assertions + 20 special-case tests)
  - `tests/test_dossier_sparkline.py` — 19 tests (INSUFFICIENT-DATA + valid SVG + determinism + brand reuse + XSS hygiene + edge cases)
  - `tests/test_dossier_html_render.py` — 10 tests (BRAND_CSS_VARS derivation + section_to_html_details + HTML escape + no-script invariant)
- All 117 tests PASS in 0.43s (deterministic; no I/O dependencies in P1)

## Cross-references

- D-IH-48-A (package vs single file → package)
- D-IH-48-D (section ordering invariant 1..12)
- D-IH-48-I (HTML interactivity scope: native `<details>`; no JS framework)
- D-IH-48-L (cost discipline env vars: `MAX_DOSSIER_USD` + `AKOS_DOSSIER_TIER_B`)
- E9 (brand token reuse; single SSOT via `BRAND_TOKENS_LIGHT/DARK`)
- I27 P1 (`akos.hlk_pdf_render` BRAND_TOKENS source)
- I32 P10 (auto-render-with-markers pattern reference; will be used in P3)
- dossier-section-spec.md (P0 artifact; consumed by 12 Section subclasses)
