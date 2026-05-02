---
language: en
status: active
initiative: 48-operator-dossier
report_kind: asset-classification
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-02
---

# Initiative 48 — Asset Classification

Per [`PRECEDENCE.md`](../../../references/hlk/compliance/PRECEDENCE.md): every artifact below is classified as **canonical** (authored, SSOT in git), **mirrored / derived** (rebuildable from canonical), or **reference-only** (not governed).

## New canonical (planning artifacts)

| Path | Class | Owner | Validator |
|:-----|:------|:------|:----------|
| `docs/wip/planning/48-operator-dossier/master-roadmap.md` | canonical | Founder + System Owner | `validate_planning_traceability` |
| `docs/wip/planning/48-operator-dossier/decision-log.md` | canonical | Founder + System Owner | `validate_planning_traceability` |
| `docs/wip/planning/48-operator-dossier/evidence-matrix.md` | canonical | Founder + System Owner | none (prose) |
| `docs/wip/planning/48-operator-dossier/asset-classification.md` (this file) | canonical | Founder + System Owner | `validate_planning_traceability` |
| `docs/wip/planning/48-operator-dossier/risk-register.md` | canonical | Founder + System Owner | `validate_planning_traceability` |
| `docs/wip/planning/48-operator-dossier/dossier-section-spec.md` (NEW per I48) | canonical | System Owner | none (prose; consumed by `akos/dossier/sections.py` at P1) |

## New canonical (Python package + scripts)

| Path | Class | Owner | Phase |
|:-----|:------|:------|:------|
| `akos/dossier/__init__.py` (NEW package) | canonical | System Owner | P1 |
| `akos/dossier/run.py` (NEW; `DossierRun` dataclass) | canonical | System Owner | P1 |
| `akos/dossier/sections.py` (NEW; `Section` ABC + 12 subclasses) | canonical | System Owner | P1 |
| `akos/dossier/sparkline.py` (NEW; SVG generator) | canonical | System Owner | P1 + P7 |
| `akos/dossier/html_render.py` (NEW; HTML mode) | canonical | System Owner | P1 + P5 |
| `akos/dossier/sources.py` (NEW; per-section data fetchers) | canonical | System Owner | P2 |
| `akos/dossier/runner.py` (NEW; subprocess CLI orchestrator) | canonical | System Owner | P3 |
| `akos/dossier/pdf_render.py` (NEW; thin wrapper around `render_pdf_branded`) | canonical | System Owner | P4 |
| `akos/dossier/dossier_run_writer.py` (NEW; mirror live writes) | canonical | System Owner | P7 |
| `scripts/render_uat_dossier.py` (NEW; operator entry point) | canonical | System Owner | P2 (skeleton) → P3-P8 (extensions) |

## New canonical (registry / policy)

| Path | Class | Owner | Phase |
|:-----|:------|:------|:------|
| `POL-DOSSIER-RUN-RETENTION-V1` row in `POLICY_REGISTER.csv` (`policy_class=retention`; encodes `min_days_kept=180; max_rows=1000`) | canonical | System Owner + Compliance | P7 |
| New `retention` value in `VALID_POLICY_CLASSES` enum (`akos/hlk_policy_register_csv.py`) | canonical | System Owner | P7 |

## New mirrored / derived (Supabase + filesystem)

| Path | Class | Source of truth | Mirror table / artifact |
|:-----|:------|:----------------|:------------------------|
| `supabase/migrations/<ts>_i48_dossier_run_mirror.sql` (P7) | canonical migration | the migration | `compliance.dossier_run_mirror` |
| `compliance.dossier_run_mirror` table | mirrored | live writes from `akos/dossier/dossier_run_writer.py` per dossier render invocation | RLS deny anon/auth; service_role only; `(mode, started_at DESC)` partial index for trend queries |
| `compliance.policy_register_mirror` 1 new row (`POL-DOSSIER-RUN-RETENTION-V1`) | mirrored | `POLICY_REGISTER.csv` | Reseeded via P9 |
| `artifacts/uat-dossier/uat-dossier-<UTC>/dossier.md` (per-run) | mirrored / derived | regenerable via `py scripts/render_uat_dossier.py` | gitignored |
| `artifacts/uat-dossier/uat-dossier-<UTC>/dossier.pdf` (per-run) | mirrored / derived | regenerable | gitignored |
| `artifacts/uat-dossier/uat-dossier-<UTC>/dossier.html` (per-run) | mirrored / derived | regenerable | gitignored |
| `artifacts/uat-dossier/uat-dossier-<UTC>/manifest.json` (per-run) | mirrored / derived | regenerable | gitignored |
| `artifacts/uat-dossier/uat-dossier-<UTC>/screenshots/*.png` (per-run; opt-in) | mirrored / derived | regenerable via Cursor browser MCP | gitignored |
| `artifacts/uat-dossier/index.json` (operator-local trend cache) | mirrored / derived | regenerable from `compliance.dossier_run_mirror` queries | gitignored |

## Modified canonical

| Path | Change | Phase |
|:-----|:-------|:------|
| `akos/hlk_policy_register_csv.py` | Add `retention` to `VALID_POLICY_CLASSES` | P7 |
| `akos/hlk_pdf_render.py` | Maybe extend `render_pdf_branded` `profile` enum with `"uat_dossier"` (D-IH-48-H1 sub-decision deferred to P4) | P4 (conditional) |
| `docs/references/hlk/compliance/dimensions/POLICY_REGISTER.csv` | 1 new row `POL-DOSSIER-RUN-RETENTION-V1` | P7 |
| `.github/workflows/eval-tier-b.yml` | Add trailing dossier-render + artifact-upload step per matrix cell | P8 |
| `.github/workflows/dossier-on-pr.yml` | NEW; opt-in workflow gated by `vars.AKOS_DOSSIER_ON_PR == 'true'` repo var | P8 |
| `config/verification-profiles.json` | Add `dossier_smoke` profile (`py scripts/render_uat_dossier.py --mode snapshot --format md`) | P9 |
| `docs/wip/planning/README.md` | New row for I48 | P0 |
| `docs/wip/planning/WIP_DASHBOARD.md` | Re-rendered | P0 + P9 |
| `docs/ARCHITECTURE.md` | Operator Scripts table + Orchestration Library `akos/` table | P9 |
| `docs/USER_GUIDE.md` | New section: "Operator-facing UAT Dossier" | P9 |
| `docs/DEVELOPER_CHECKLIST.md` | New line: `py scripts/render_uat_dossier.py --mode snapshot` as part of pre-PR checklist | P9 |
| `docs/reference/DEV_VERIFICATION_REFERENCE.md` | New `dossier_smoke` profile description | P9 |
| `CHANGELOG.md` | Closure entry under `[Unreleased]` | P9 |
| `.gitignore` | `artifacts/uat-dossier/*.md`, `*.pdf`, `*.html`, `*.json` (preserve README.md) | P2 |

## Reference-only / external (cited but not authored)

| Source | Citation use |
|:-------|:-------------|
| WeasyPrint (https://weasyprint.org) | P4 PDF rendering primary path; cited in PDF mode docs |
| fpdf2 (https://pyfpdf.github.io) | P4 PDF rendering fallback path |
| pandoc | P4 PDF rendering second fallback |
| Python `markdown` library | P5 markdown→HTML conversion (already in repo deps) |
| `Inter` typography (Google Fonts) | P4 + P5 brand token |
| BRAND_VISUAL_PATTERNS.md `BRAND_TOKENS_LIGHT/DARK` (canonical SSOT) | Single token source for both PDF + HTML modes (E9) |

These are **not** copied into the repo. They are referenced inline in evidence-matrix and the dossier output.

## Drift handling rule

If canonical and mirrored assets disagree:

1. **Canonical wins.** `POLICY_REGISTER.csv` is SSOT for `POL-DOSSIER-RUN-RETENTION-V1`. `BRAND_VISUAL_PATTERNS.md` is SSOT for brand tokens (mirrored to `BRAND_TOKENS_LIGHT/DARK` in `akos/hlk_pdf_render.py`; drift caught by `tests/test_render_dossier.py::test_brand_tokens_light_match_pattern_doc`).
2. **Investigate translation or propagation drift.** P9 doc-sync matrix per `akos-docs-config-sync.mdc`; mirror reseed via the existing `scripts/sync_compliance_mirrors_from_csv.py` + `npx supabase db push` flow (per I47 P13 item 2 boolean fix).
3. **Resync runtime/mirror from canonical.** Reseed mirrors; re-render dossier (which queries the mirror); operator verifies sparklines still render correctly.
4. **Document the incident in the remediation report.** Per `akos-governance-remediation.mdc` (existing rule).

## What is explicitly NOT changed

- `Scorecard.to_markdown()` (I47 P10) — embedded verbatim; never re-rendered
- `validate_hlk.py` core dispatcher (I32 P1) — invoked via subprocess; never altered
- `scripts/eval.py` (I45 P1) — orchestrated as a child process; flags untouched
- `akos.hlk_pdf_render` core functions (I22 P6 + I27 P1) — only `profile` enum potentially extended (D-IH-48-H1)
- `BRAND_VISUAL_PATTERNS.md` (Brand Manager owns; we read tokens, never edit)
- I46 P5 conditional GraphRAG ship state — dossier reads it; never alters
- I47 P14 Tier B 4-D matrix — dossier ships AS a trailing step; matrix dimensions unchanged
