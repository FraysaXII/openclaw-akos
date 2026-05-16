---
candidate_id: I85
title: Audience-tag canonicalization (J-* codes from brand matrix prose → canonical CSV register + frontmatter migration + drift gate)
status: candidate
authored: 2026-05-16
last_review: 2026-05-16
parent_initiatives: [77, 81]
related_initiatives: [66, 71]
priority: 5
language: en
---

# I85 candidate — Audience-tag canonicalization

> **Spawned by I77 P4 follow-up.** Surfaced as a vague forward-charter item in [`uat-impeccable-all-surfaces-2026-05-16.md`](../77-impeccable-brand-bridge-refresh/reports/uat-impeccable-all-surfaces-2026-05-16.md) §7 item #1 *"Audience-tagging migration (informal labels → J-* codes on `_assets/advops/**`) — candidate for I-NN micro OR absorbable by I81 vault-sweep. Not P4 scope (it's a different governance dimension: persona-audience tagging, not brand-canon)."* and re-confirmed as a concrete gap by the real Impeccable audit on `BASELINE_REALITY.md` at [`impeccable-audit-baseline-reality-2026-05-16.md`](../77-impeccable-brand-bridge-refresh/reports/impeccable-audit-baseline-reality-2026-05-16.md) §3 findings #7+#8+#9 (3 neutral findings collapse into this single governed workstream).
>
> Operator directive at I77 P4 closure (2026-05-16 evening): *"brand needs to rework how to address these things, I rather have them in this initiative wired up with other jobs and initiatives properly like we did earlier"* — i.e., the same wiring discipline that I77 P4.C applied to the rendering-pipeline registry (canonical CSV + Pydantic chassis + validator + SOP + runbook + tests + release-gate wiring) should apply to audience-tagging. This candidate is the concrete wiring.

## 1. Operating story

The J-* audience codes (J-IN investor, J-CU customer-SME, J-PT partner, J-ENISA reviewer, J-AD advisor, J-RC recruiter/hire, J-CO collaborator, J-OP operator-internal) live as **prose-only** rows inside [`BRAND_BASELINE_REALITY_MATRIX.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_BASELINE_REALITY_MATRIX.md). Every surface under `docs/references/hlk/v3.0/_assets/advops/**` and `docs/references/hlk/v3.0/_assets/touchpoint-kit/**` could carry an `audience: <J-*>` frontmatter for FK-resolvability — but there is no canonical CSV to FK-resolve against, no validator to enforce it, and no migration to populate the frontmatter on existing surfaces.

The Impeccable `/impeccable critique`, `/polish`, `/craft`, and `/audit` commands consume the bridge file [`BASELINE_REALITY.md`](../../../BASELINE_REALITY.md) to identify audience(s) per surface. Today the identification is **inferred from prose** (PRODUCT.md `register` field + matrix prose-rows). Mechanical identification via frontmatter `audience: <J-*>` would let Impeccable hard-fail on `craft` for explicit `audience: <multi>` surfaces (per [`SKILL.md`](../../../.cursor/skills/impeccable/SKILL.md) line 20) AND let CI detect drift (e.g., a surface tagged `audience: J-IN` containing J-CU vocabulary).

I85 closes the gap with the same wiring pattern I77 P4.C applied to rendering pipelines:

1. **Canonical CSV** at `docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/dimensions/AUDIENCE_REGISTRY.csv` (8 seed rows: 7 external J-* + 1 internal J-OP).
2. **Pydantic chassis** at `akos/hlk_audience_csv.py` (same shape as `akos/hlk_rendering_pipeline_csv.py`).
3. **Validator** at `scripts/validate_audience_registry.py` (registry-level: schema + enum + cross-link to matrix).
4. **Tag-migration runbook** at `scripts/audience_tag_assets.py` (scans `_assets/advops/**/*.md` + `_assets/touchpoint-kit/**/*.md`; reports surfaces missing `audience:` frontmatter; optional `--apply` mode adds it interactively).
5. **Drift gate** at `scripts/validate_audience_tags.py` (asserts every prose surface under the governed roots carries a valid `audience:` value FK-resolved against `AUDIENCE_REGISTRY.csv`).
6. **Paired SOP** at `docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/SOP-AUDIENCE_TAG_GOVERNANCE_001.md` (per [`akos-executable-process-catalog.mdc`](../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 1 SOP+runbook pairing).
7. **CANONICAL_REGISTRY rows** (registry + SOP).
8. **Tests** at `tests/test_audience_registry.py` (~15-20 governance tests; same shape as `tests/test_rendering_pipeline_registry.py`).
9. **Multi-audience composition recipe** added to `BRAND_BASELINE_REALITY_MATRIX.md` (worked pattern for J-IN+J-AD simultaneous-reach surfaces — addresses Impeccable audit finding #9).
10. **Bridge update**: [`BASELINE_REALITY.md`](../../../BASELINE_REALITY.md) gets a concrete `audience: <J-*>` frontmatter example (addresses Impeccable audit finding #7).

## 2. Scope

### 2a. In scope

- Canonical CSV mint + Pydantic chassis + validator + runbook + SOP + tests + CANONICAL_REGISTRY rows (mirrors I77 P4.C wiring pattern row-for-row).
- Tag-migration sweep across `_assets/advops/**/*.md` + `_assets/touchpoint-kit/**/*.md` (~50-100 surfaces).
- Bridge update to `BASELINE_REALITY.md` (concrete frontmatter example + multi-audience composition recipe link).
- Matrix update to `BRAND_BASELINE_REALITY_MATRIX.md` (multi-audience composition recipe section).
- Drift gate wired into [`scripts/validate_hlk.py`](../../../scripts/validate_hlk.py) + [`scripts/release-gate.py`](../../../scripts/release-gate.py).

### 2b. Out of scope (forward-charter)

- **Sibling-repo audience tags** (`boilerplate/messages/*.json` audience routing; `hlk-erp/app/(public)/**` audience-aware rendering) — deferred to next bless cycle per [`SOP-EXTERNAL_REPO_BLESSING_001.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/Envoy%20Tech%20Lab/External%20Repos/SOP-EXTERNAL_REPO_BLESSING_001.md).
- **Audience-aware rendering** in the visual UAT pipeline (I77 P4.B output) — the rendered HTML stays J-OP-optimized; multi-audience render variants are I74 Brand Tooling Productization scope.
- **J-* code additions/renames** — frozen at the 8 seed rows unless `BRAND_BASELINE_REALITY_MATRIX.md` adds a new row first per AKOS precedence rule.

### 2c. Cross-area touchpoints

- **Brand** (owner): canonical CSV + SOP + matrix update.
- **Tech / System Owner** (co-owner): validators + drift gate + release-gate wiring.
- **Marketing / Reach** (consumer): touchpoint-kit surfaces gain `audience:` frontmatter.
- **Operations / RevOps** (consumer): advops-engagement surfaces gain `audience:` frontmatter.

## 3. Phase shape (provisional; ratify at P0 charter)

| Phase | Effort | Deliverable | Gate |
|:---|:---|:---|:---|
| P0 — Charter | 0.5d | Inline-ratify open conundrums (CSV column count; multi-audience encoding `audience: J-IN+J-AD` vs `audience: [J-IN, J-AD]`; tag-migration sweep strategy auto vs interactive); mint INITIATIVE_REGISTRY + DECISION_REGISTER rows | operator approval |
| P1 — Canonical mint | 1d | AUDIENCE_REGISTRY.csv + Pydantic chassis + validator + tests + CANONICAL_REGISTRY rows; SOP authored | operator approval (canonical CSV gate) |
| P2 — Tag-migration sweep | 1d | scripts/audience_tag_assets.py runbook + scripts/validate_audience_tags.py drift gate; sweep `_assets/**` surfaces | operator approval per tranche (no surprise frontmatter changes) |
| P3 — Bridge + matrix update | 0.5d | BASELINE_REALITY.md frontmatter example + BRAND_BASELINE_REALITY_MATRIX.md multi-audience composition recipe; impeccable-bridge-drift re-runs green | inline-ratify |
| P4 — Closure | 0.5d | release-gate + validate_hlk wired; closure report; CHANGELOG entry; files-modified.csv | operator approval |
| **Total** | **~3.5d** | | |

## 4. Open conundrums (resolve at P0 charter via inline-ratify)

| ID | Question | Default verdict | Decision target |
|:---|:---|:---|:---|
| C-85-1 | Should `AUDIENCE_REGISTRY.csv` carry the full per-audience matrix content (bridge frame + objection patterns + first-doubt trigger), or stay narrow (code + name + register-side + surface examples)? | Narrow (matrix stays SSOT for deep content; CSV is FK index only) | D-IH-85-A |
| C-85-2 | Multi-audience frontmatter encoding: `audience: J-IN+J-AD` (string) vs `audience: [J-IN, J-AD]` (list)? | List (YAML-native; easier to FK-resolve) | D-IH-85-B |
| C-85-3 | Tag-migration sweep posture: auto-apply per agent inference vs interactive per surface vs operator-batch-approve? | Operator-batch-approve per file-class tranche | D-IH-85-C |
| C-85-4 | Should `BASELINE_REALITY.md` itself gain `audience: J-OP` frontmatter (it's an internal bridge consumed by Impeccable / agents)? | Yes — consistency with the new convention | D-IH-85-D |
| C-85-5 | I81 absorption posture: does I85 run as a sibling I-NN OR get absorbed as an I81 sub-strand? | Sibling I-NN (different governance axis; less coupling) — but I81 vault-sweep evidence pack can include audience-tag coverage as a column in `kb-integrity-matrix-<date>.csv` | D-IH-85-E |

## 5. Cross-references + wiring (the "wired up with other jobs" requirement)

- **Origin**: [I77 P4 follow-up](../77-impeccable-brand-bridge-refresh/reports/p4-brand-canon-collapse-remediation-2026-05-16.md) + UAT §7 item #1 + Impeccable audit finding #8.
- **Sibling absorbing related foundation work**: [I81 — Knowledge-base integrity sweep](i81-full-vault-sop-addendum-retrofit.md). I81 P1 evidence pack (`kb-integrity-matrix-<date>.csv`) should add an `audience_tags_coverage` column once I85 ships — this is the concrete inter-initiative wiring beyond a vague "or absorbable by I81". Sequencing: **I85 P1 mints registry → I81 P1 evidence pack consumes audience_tags_coverage column** (forward link in INITIATIVE_DEPENDENCIES.md).
- **Brand canonical home**: [`BRAND_BASELINE_REALITY_MATRIX.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_BASELINE_REALITY_MATRIX.md) gains §"Multi-audience composition recipe" addressing Impeccable audit finding #9.
- **Brand voice canonical sibling**: I71 P1 Pack A1 (BRAND_ENGLISH_PATTERNS + BRAND_LLM_TONE_TELLS) is the foundation for per-audience prose voice; I85 layers FK-resolvable audience tags on top.
- **Pattern precedent (must mirror)**: I77 P4.C [`RENDERING_PIPELINE_REGISTRY.csv`](../../../docs/references/hlk/v3.0/Envoy%20Tech%20Lab/canonicals/dimensions/RENDERING_PIPELINE_REGISTRY.csv) — same wiring pattern (canonical + Pydantic + validator + SOP + runbook + tests + CANONICAL_REGISTRY rows + release-gate wiring). Apply row-for-row.
- **Forward-charter consumer**: [I74 Brand Tooling Productization](i74-brand-tooling-productization.md) absorbs audience-tag aware rendering when TRIGGER-2 fires.
- **Governing rules**: [`akos-executable-process-catalog.mdc`](../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 1 (SOP+runbook pairing) + Rule 2 (status enum) · [`akos-holistika-operations.mdc`](../../../.cursor/rules/akos-holistika-operations.mdc) §"New git-canonical compliance registers (pattern)" · [`akos-brand-baseline-reality.mdc`](../../../.cursor/rules/akos-brand-baseline-reality.mdc) · [`akos-planning-traceability.mdc`](../../../.cursor/rules/akos-planning-traceability.mdc).

## 6. Promotion criteria (to `active` initiative folder)

1. Operator ratifies C-85-1..5 via P0 inline-ratify AskQuestion.
2. Operator confirms ~3.5d effort allocation slot (likely Q3 2026 after I81 P1 evidence pack lands; can run earlier if operator prioritizes).
3. No conflict with I81 layout reorganisation tranches in flight (P0 charter coordinates).

## 7. Files this candidate will mint (when promoted)

- **NEW canonical**: `docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/dimensions/AUDIENCE_REGISTRY.csv`
- **NEW Pydantic chassis**: `akos/hlk_audience_csv.py`
- **NEW validator**: `scripts/validate_audience_registry.py`
- **NEW drift gate**: `scripts/validate_audience_tags.py`
- **NEW runbook**: `scripts/audience_tag_assets.py`
- **NEW SOP**: `docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/SOP-AUDIENCE_TAG_GOVERNANCE_001.md`
- **NEW tests**: `tests/test_audience_registry.py`
- **MODIFIED**: `BASELINE_REALITY.md` (frontmatter example), `BRAND_BASELINE_REALITY_MATRIX.md` (multi-audience composition recipe), `CANONICAL_REGISTRY.csv` (2 rows), `scripts/validate_hlk.py` (validator entry), `scripts/release-gate.py` (validator row), `scripts/INITIATIVE_DEPENDENCIES.md` (i85 node + edges), ~50-100 surfaces under `_assets/advops/**` + `_assets/touchpoint-kit/**` (frontmatter `audience:` addition per operator-batch-approve tranche).
