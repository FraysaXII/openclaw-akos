---
initiative_id: I85
language: en
last_review: 2026-05-16
---

# I85 — Asset classification

Per [`PRECEDENCE.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md). Mirrors I77 P4.C precedent.

## Canonical (edit-here-first; canonical-CSV gates apply)

| Asset | Phase | Gate | Notes |
|:---|:---|:---|:---|
| `docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/dimensions/AUDIENCE_REGISTRY.csv` (NEW; 8 seed rows) | P1 | operator approval (canonical CSV gate) | New dimensional canonical; narrow FK index per D-IH-85-A |
| `docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/SOP-AUDIENCE_TAG_GOVERNANCE_001.md` (NEW; `status: review` at P1; `status: active` at P4) | P1 → P4 | operator approval at P1 and P4 | Paired SOP per [`akos-executable-process-catalog.mdc`](../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 1 |
| `docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_BASELINE_REALITY_MATRIX.md` (MODIFIED; §"Multi-audience composition recipe" added) | P3 | inline-ratify | Addresses Impeccable audit finding #9 |
| `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/CANONICAL_REGISTRY.csv` (NEW 2 rows: registry + SOP) | P1 | operator approval (canonical CSV gate) | Mirrors I77 P4.C pattern |
| `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_REGISTRY.csv` (NEW row `INIT-OPENCLAW_AKOS-85`) | P0 | operator approval | Promotes candidate to active |
| `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv` (NEW 5 rows: D-IH-85-A..E) | P0 | operator approval | Charter decisions |
| `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/OPS_REGISTER.csv` (NEW row `OPS-85-1`) | P0 | operator approval | Open action: P2 sweep coordination |

## Mirrored / derived (auto-rendered or synced)

| Asset | Source | Renderer/Sync |
|:---|:---|:---|
| Supabase `compliance.audience_registry_mirror` | `AUDIENCE_REGISTRY.csv` | `scripts/sync_compliance_mirrors_from_csv.py` (post P1) |
| `docs/wip/planning/WIP_DASHBOARD.md` | per-initiative `master-roadmap.md` frontmatter | `scripts/render_wip_dashboard.py` |
| `docs/wip/planning/OPERATOR_INBOX.md` | `OPS_REGISTER.csv` | `scripts/render_operator_inbox.py` |

## Reference-only / consumer surfaces (operator-batch-approve per tranche at P2)

| Asset class | Surface | Action |
|:---|:---|:---|
| `BASELINE_REALITY.md` | repo root | Add `audience: [J-OP]` frontmatter + concrete example (P3 — not P2 since it's the bridge, not an asset surface) |
| `docs/references/hlk/v3.0/_assets/advops/**/*.md` (decks) | ~20-30 surfaces | P2-a tranche; operator-batch-approve dry-run |
| `docs/references/hlk/v3.0/_assets/advops/**/dossier_*.md` (dossiers) | ~10-15 surfaces | P2-b tranche; operator-batch-approve dry-run |
| `docs/references/hlk/v3.0/_assets/touchpoint-kit/**/*.md` (emails + onboarding) | ~20-30 surfaces | P2-c tranche; operator-batch-approve dry-run |

## Engineering surface (governed by [`CONTRIBUTING.md`](../../../CONTRIBUTING.md); not compliance-canonical)

| Asset | Phase | Compliance contract |
|:---|:---|:---|
| `akos/hlk_audience_csv.py` (Pydantic chassis) | P1 | Fieldname tuple matches CSV header exactly; same shape as `akos/hlk_rendering_pipeline_csv.py` |
| `scripts/validate_audience_registry.py` (registry-level) | P1 | Schema + enum + cross-link to matrix; wired into `validate_hlk.py` + `release-gate.py` |
| `scripts/validate_audience_tags.py` (drift gate) | P2 | Asserts every governed-root prose surface carries valid `audience:` value FK-resolved |
| `scripts/audience_tag_assets.py` (paired runbook) | P2 | `--dry-run` default; `--apply` interactive; cited from SOP-AUDIENCE_TAG_GOVERNANCE_001.md |
| `tests/test_audience_registry.py` | P1 | ~15-20 governance tests; same shape as `tests/test_rendering_pipeline_registry.py` |
