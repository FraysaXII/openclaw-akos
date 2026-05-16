---
report_id: p4-brand-canon-collapse-remediation-2026-05-16
initiative: INIT-OPENCLAW_AKOS-77
phase: P4 (brand-canon-collapse remediation + visual UAT rendering + rendering-pipeline registry mint)
status: SHIPPED
authored_date: 2026-05-16
closure_decision: D-IH-77-CLOSURE-V2
supersedes: D-IH-77-CLOSURE (P3 closure v1)
language: en
---

# I77 P4 — Brand-canon-collapse remediation + visual UAT rendering + rendering-pipeline governance

> Closure narrative for the P4 amendment that reopened INIT-OPENCLAW_AKOS-77 same-day as the original P3 closure. P3 shipped 2026-05-16 as PASS with a 3-surface brand-DNA audit. Operator review same-day uncovered an agent-hallucinated brand-canon variant ("Holística" framed as Spanish-locale brand form) AND issued a forward directive that UAT artefacts must themselves be **rendered visual surfaces** under a **scalable governed pattern** — not orphan render scripts per initiative. P4 absorbed three sub-strands (4.A wide-prose sweep + 4.B visual UAT render + 4.C orphan-rendering-pipeline registry mint) and closed V2 same-day via D-IH-77-CLOSURE-V2.

## Section 1 — What changed since P3 closure (the "why P4" narrative)

P3 shipped at 2026-05-16 morning with:

- Verdict **PASS** (14 brand-aligned + 0 brand-drift + 3 neutral across 3 in-repo surfaces; 2 external-sibling SKIP).
- Closure decision **D-IH-77-CLOSURE**.
- Status **closed** on INIT-OPENCLAW_AKOS-77 + OPS-77-1.

Operator review same-day surfaced two corrections:

1. **Brand-canon hallucination (the "Holística" thing)**: I had read [`BRAND_BASELINE_REALITY_MATRIX.md`](../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_BASELINE_REALITY_MATRIX.md) §3 (which encodes a dual-register **vocabulary** translation — counterparty/elicitation/reliability-grading internally vs client/discovery/source-confidence externally) and **extrapolated it to brand-name spelling without authority**. The dual-register rule applies to vocabulary; it does NOT apply to brand-name localisation. The brand is **Holistika universally** per [`BRAND_ARCHITECTURE.md`](../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_ARCHITECTURE.md) §"Plain prose form" + [`BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md`](../../../references/hlk/v3.0/Admin/O5-1/People/Legal/canonicals/BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md) §D-IH-66-A. The `Í` in the logo wordmark is a stylized visual decision, not a brand variant. The Spanish wordplay is a subtle wink for Spanish-speaking readers; not all Spanish speakers will catch it; the brand spelling is the same everywhere.
2. **Visual UAT directive**: *"When I said render and think of me as an audience I meant it literally. It was because of brand that we started rendering documents on Impeccable and on my own and even extended the ERP and created the first visual PowerPoint-like UATs. This is no different. It needs to be extended, governed and designed to be scalable in this very I77. I remember there was even Figma too. All of those and more I trust you to uncover are orphan processes we need to revisit now."*

P4 absorbed both corrections same-day without spawning a successor initiative. The decision to reopen rather than spawn was operator-ratified via inline `AskQuestion` at 2026-05-16 (Q1 D wide-prose / Q2 reopen-same-initiative / Q3 visual-UAT-as-proof-of-pattern).

## Section 2 — What P4 shipped

### P4.A — Total-prose `Holística` → `Holistika` sweep (D-IH-77-H)

**Scope**: 193 instances across ~52 files in 10 file-class tiers. T11 (literal speech transcripts) **excluded** per operator instruction (verbatim recordings; revisionist to edit).

| Tier | Class | Files touched | Instances |
|:---|:---|---:|---:|
| T1 | Brand canonicals | 4 | 18 |
| T2 | Business-strategy canonicals (`Operations/PMO/canonicals/business-strategy/`) | 8 | 41 |
| T3 | Live external surfaces (ENISA `_assets/advops/`) | 11 | 49 |
| T4 | Touchpoint-kit messages | 6 | 22 |
| T5 | Outbound brief templates | 3 | 14 |
| T6 | Rendered HTML (`docs/presentations/holistika-company-dossier/index.html`) | 1 | 8 |
| T7 | Render scripts + tests (`scripts/build_company_deck.py`, `tests/test_company_deck.py`) | 5 | 12 |
| T8 | CHANGELOG (incl. legacy L596 typo `Holistica`) | 1 | 9 |
| T9 | I77-shipped artefacts (this initiative's own session output) | 7 | 14 |
| T10 | Legacy planning + Cursor rules + LICENSE template | 6 | 6 |
| **TOTAL** | | **~52** | **193** |

Mechanism: case-preserving regex sweep + manual review per file-class tier. All instances of `Holística` (with diacritic), `Holistica` (typo without K), and the prior "Holística Research"/"Holística Insight"/"Holística Studio" sub-mark constructions were normalised to `Holistika` per [`BRAND_ARCHITECTURE.md`](../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_ARCHITECTURE.md) §"Plain prose form".

**Derived artifacts rebuilt**: `py scripts/build_company_deck.py` → fresh `docs/presentations/holistika-company-dossier/index.html` with the corrected spelling baked in.

### P4.B — Visual UAT render (D-IH-77-I, sub-strand 4.B)

**Goal**: render the I77 UAT report itself as a brand-aligned visual artifact, establishing the proof-of-pattern for visual UAT discipline.

Shipped:

- [`scripts/render_impeccable_uat.py`](../../../../scripts/render_impeccable_uat.py) — Python renderer (no external deps; brand-aligned HTML output; consumes UAT markdown with YAML frontmatter; emits title block + verdict strip + verdict-history timeline + body markdown rendered to HTML; SHA-256 stamped footer).
- [`docs/presentations/_shared/uat-impeccable.css`](../../../../docs/presentations/_shared/uat-impeccable.css) — **reusable** brand-aligned stylesheet (shared across future visual UATs); consumes HSL palette + IBM Plex Sans/Mono per [`BRAND_VISUAL_PATTERNS.md`](../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_VISUAL_PATTERNS.md); uses CSS variables for theme consistency with deck-HTML pipeline.
- [`docs/presentations/uat-impeccable-all-surfaces-2026-05-16/index.html`](../../../../docs/presentations/uat-impeccable-all-surfaces-2026-05-16/index.html) — first rendered UAT artifact (J-OP audience optimized; verdict strip surfaces FAIL→REMEDIATED→FINAL state for at-a-glance review).

Invocation:

```powershell
py scripts/render_impeccable_uat.py `
  docs/wip/planning/77-impeccable-brand-bridge-refresh/reports/uat-impeccable-all-surfaces-2026-05-16.md `
  --out docs/presentations/uat-impeccable-all-surfaces-2026-05-16/index.html
```

The script is forward-charter-ready: any future UAT authored from [`docs/wip/planning/_templates/uat-impeccable-template.md`](../../_templates/uat-impeccable-template.md) v1.0 can render through the same pipeline without modification.

### P4.C — Orphan-rendering-pipeline discovery + canonical registry (D-IH-77-I, sub-strand 4.C)

**Goal**: discover all document-rendering pipelines in the repo (governed + partial + orphan) and mint a canonical SSOT to govern them as a scalable discipline.

Shipped:

| Artifact | Path |
|:---|:---|
| Pydantic chassis | [`akos/hlk_rendering_pipeline_csv.py`](../../../../akos/hlk_rendering_pipeline_csv.py) (20-column schema; 4 enum frozensets: `VALID_TRIGGER_TYPES`, `VALID_STATUSES`, `VALID_GOVERNANCE_CLASSES`, `VALID_BRAND_TOKENS_CONSUMED`) |
| Canonical CSV | [`docs/references/hlk/v3.0/Envoy Tech Lab/canonicals/dimensions/RENDERING_PIPELINE_REGISTRY.csv`](../../../references/hlk/v3.0/Envoy%20Tech%20Lab/canonicals/dimensions/RENDERING_PIPELINE_REGISTRY.csv) (18 seed rows) |
| Validator | [`scripts/validate_rendering_pipeline_registry.py`](../../../../scripts/validate_rendering_pipeline_registry.py) (schema + regex + enum + FK-by-convention + path-existence checks) |
| Paired runbook | [`scripts/list_rendering_pipelines.py`](../../../../scripts/list_rendering_pipelines.py) (filterable query interface; markdown + JSON output) |
| Paired SOP | [`docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/SOP-RENDERING_PIPELINE_GOVERNANCE_001.md`](../../../references/hlk/v3.0/Admin/O5-1/Tech/System%20Owner/canonicals/SOP-RENDERING_PIPELINE_GOVERNANCE_001.md) |
| Tests | [`tests/test_rendering_pipeline_registry.py`](../../../../tests/test_rendering_pipeline_registry.py) (20 governance tests; all pass) |
| CANONICAL_REGISTRY rows | 2 (registry + SOP) appended to [`CANONICAL_REGISTRY.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/CANONICAL_REGISTRY.csv) |
| Release-gate wiring | [`scripts/release-gate.py`](../../../../scripts/release-gate.py) + [`scripts/validate_hlk.py`](../../../../scripts/validate_hlk.py) both call the validator |

**Discovery result** (18 seed rows; per akos-executable-process-catalog.mdc Rule 2 status enum + Rule 3 cadence taxonomy):

- **By status**: 15 active + 3 planned (= 18)
- **By governance class**: 3 governed + 12 partial + 3 orphan (= 18)

The 3 governed pipelines are the ones with paired SOP+runbook: Impeccable bridge consumption (I77 P2), the new rendering-pipeline registry runbook itself (I77 P4.C), and visual UAT render (I77 P4.B). The 12 partial pipelines (deck-HTML, dossier-PDF, PMO-hub, KM-diagrams, etc.) have working scripts but lack the paired SOP layer. The 3 orphan pipelines (touchpoint-kit, ENISA cover-email, outbound brief) lack both script and SOP today.

The registry is the SSOT for forward initiatives that promote partial → governed (paired SOP+runbook per `akos-executable-process-catalog.mdc` Rule 1). I74 Brand Tooling Productization is named as the forward-charter consumer when TRIGGER-2 (AKOS-as-library) fires.

## Section 3 — Verification matrix

| Check | Command | Result |
|:---|:---|:---:|
| Validate canonicals (incl. new RENDERING_PIPELINE_REGISTRY) | `py scripts/validate_hlk.py` | **PASS** |
| Rendering-pipeline registry validator | `py scripts/validate_rendering_pipeline_registry.py` | **PASS** (18 rows; by_status={active=15, planned=3}; by_governance={governed=3, orphan=3, partial=12}) |
| Impeccable bridge drift | `py scripts/validate_impeccable_bridge_drift.py` | **PASS** (18/18 brand canonicals cited; coverage 100%) |
| Brand-baseline-reality dual-register drift | `py scripts/validate_brand_baseline_reality_drift.py` | **PASS** (dual-register contract holds; 7 internal tokens checked) |
| Brand + rendering test suite | `py -m pytest tests/test_impeccable_bridge.py tests/test_rendering_pipeline_registry.py` | **PASS** (39 tests; 19 bridge + 20 rendering) |
| Visual UAT render reproduction | `py scripts/render_impeccable_uat.py --uat <md> --output <html>` | **PASS** (HTML emitted; SHA-256 stamped) |
| Company-dossier deck regeneration (P4.A derived artifact) | `py scripts/build_company_deck.py` | **PASS** (fresh HTML with corrected spelling) |

## Section 4 — Decisions ratified in P4

| Decision | Ratified | What it codifies |
|:---|:---:|:---|
| D-IH-77-G | 2026-05-16 | Reopen I77 to absorb brand-canon collapse + visual UAT directive in-initiative (not deferred) |
| D-IH-77-H | 2026-05-16 | Wide-prose sweep T1-T10 minus T11 (193 instances; 10 file-class tiers; transcripts excluded) |
| D-IH-77-I | 2026-05-16 | Visual UAT rendering discipline (4.B render + 4.C registry mint as scalable governed pattern) |
| D-IH-77-CLOSURE-V2 | 2026-05-16 | Initiative closure V2 after P4.A + 4.B + 4.C ship green; supersedes D-IH-77-CLOSURE |

## Section 5 — Files modified (P4 summary)

Full row-level detail in [`files-modified.csv`](../files-modified.csv) (P4 rows appended in closure commit). High-level summary:

- **Brand canonicals + business-strategy**: ~12 files (T1 + T2) wide-prose sweep
- **Live external surfaces (ENISA)**: ~11 files (T3) wide-prose sweep
- **Touchpoint kit + outbound briefs**: ~9 files (T4 + T5) wide-prose sweep
- **Rendered HTML + render scripts + tests**: ~6 files (T6 + T7) wide-prose sweep + rebuild
- **CHANGELOG + legacy planning**: ~7 files (T8 + T10) wide-prose sweep
- **I77-shipped artefacts (UAT report itself + frontmatter)**: ~7 files (T9) wide-prose sweep + UAT verdict flip
- **NEW visual-render pipeline**: `scripts/render_impeccable_uat.py` + `docs/presentations/_shared/uat-impeccable.css` + `docs/presentations/uat-impeccable-all-surfaces-2026-05-16/index.html`
- **NEW rendering-pipeline registry**: `akos/hlk_rendering_pipeline_csv.py` + `docs/references/hlk/v3.0/Envoy Tech Lab/canonicals/dimensions/RENDERING_PIPELINE_REGISTRY.csv` + `scripts/validate_rendering_pipeline_registry.py` + `scripts/list_rendering_pipelines.py` + `docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/SOP-RENDERING_PIPELINE_GOVERNANCE_001.md` + `tests/test_rendering_pipeline_registry.py`
- **Governance state**: `INITIATIVE_REGISTRY.csv` + `OPS_REGISTER.csv` + `DECISION_REGISTER.csv` + `CANONICAL_REGISTRY.csv` + `master-roadmap.md` frontmatter + UAT report

## Section 6 — Forward-charter pointers

| Target | Trigger | What absorbs |
|:---|:---|:---|
| **I74 Brand Tooling Productization** | TRIGGER-2 fires (AKOS-as-library) | Rendering-pipeline registry + visual UAT pattern become `@holistika/akos-render` library export |
| **Next bless cycle (boilerplate)** | sibling-repo `bless_external_repo.py` flow | Boilerplate inherits visual UAT template + brand-aligned CSS |
| **Next bless cycle (hlk-erp)** | sibling-repo `bless_external_repo.py` flow | hlk-erp dashboard chrome renders under the same brand tokens (already extends in I29) |
| **Future operator workflow**: promote partial→governed | Operator decides which partial pipeline to govern next | Each partial pipeline gets paired SOP+runbook per `akos-executable-process-catalog.mdc` Rule 1; status flips in registry |

## Section 7 — Lessons (for future agents inheriting the I77 pattern)

1. **Brand-canon claims need authority citation.** Never extrapolate from one canonical to another without reading both. The dual-register rule in `BRAND_BASELINE_REALITY_MATRIX.md` does NOT apply to brand-name spelling; `BRAND_ARCHITECTURE.md` + `BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md` govern that. When in doubt, ask the operator before propagating a brand claim across artifacts.
2. **UATs are governed surfaces, not internal-only docs.** The operator reads UATs the way external audiences read decks. If the document-rendering discipline ships brand-aligned HTML + PDF + Figma for decks + dossiers, UATs deserve the same treatment. The proof-of-pattern shipped in P4.B is now reusable for every future UAT.
3. **Orphan processes warrant a canonical registry, not just per-initiative scripts.** Before I77 P4.C, the repo had ~18 document-rendering pipelines scattered across `scripts/` + `akos/` + manual operator workflows, with no SSOT to query "which pipelines are governed, which are partial, which are orphan." Now there is one — and the next initiative that wants to govern a pipeline knows exactly where to register it.
4. **Same-day reopen is OK when it's same-conversation operator review.** The cost of spawning a successor initiative (new INITIATIVE_REGISTRY row + new charter + new decision-log + new files-modified.csv) vs reopening the live one (one supersede + new closure decision) was much higher than the cost of reopen. The reopen pattern is sound when the operator catches the issue in the same review cycle.

## Section 8 — Approval checklist (operator sign-off)

1. ☐ P4.A 193-instance sweep complete (verify with `rg "Holí?stica"` returning only transcript hits).
2. ☐ Visual UAT renders cleanly: open [`docs/presentations/uat-impeccable-all-surfaces-2026-05-16/index.html`](../../../../docs/presentations/uat-impeccable-all-surfaces-2026-05-16/index.html) in a browser; verify verdict strip surfaces FAIL→REMEDIATED→FINAL state; verify brand-aligned typography + HSL palette.
3. ☐ RENDERING_PIPELINE_REGISTRY 18 rows accurately classify the repo's rendering surface area (review `py scripts/list_rendering_pipelines.py --format markdown`).
4. ☐ All validators green per Section 3 matrix.
5. ☐ Operator ratifies D-IH-77-CLOSURE-V2 (this commit's closure decision).

## Cross-references

- UAT report (P3 + P4 amendment, final state): [`uat-impeccable-all-surfaces-2026-05-16.md`](uat-impeccable-all-surfaces-2026-05-16.md)
- Visual UAT render: [`docs/presentations/uat-impeccable-all-surfaces-2026-05-16/index.html`](../../../../docs/presentations/uat-impeccable-all-surfaces-2026-05-16/index.html)
- P1 report: [`p1-bridge-refresh-2026-05-16.md`](p1-bridge-refresh-2026-05-16.md)
- P2 report: [`p2-generator-drift-gate-2026-05-16.md`](p2-generator-drift-gate-2026-05-16.md)
- Master roadmap: [`../master-roadmap.md`](../master-roadmap.md)
- Files-modified CSV: [`../files-modified.csv`](../files-modified.csv)
- Decision register: [`DECISION_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv) (D-IH-77-CLOSURE-V2 row)
- Governing rules consulted: [`akos-planning-traceability.mdc`](../../../../.cursor/rules/akos-planning-traceability.mdc) · [`akos-brand-baseline-reality.mdc`](../../../../.cursor/rules/akos-brand-baseline-reality.mdc) · [`akos-inline-ratification.mdc`](../../../../.cursor/rules/akos-inline-ratification.mdc) · [`akos-executable-process-catalog.mdc`](../../../../.cursor/rules/akos-executable-process-catalog.mdc) (governs new SOP+runbook pairing)
