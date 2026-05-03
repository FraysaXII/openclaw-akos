---
language: en
status: active
initiative: 50-live-cycle-closure
report_kind: asset-classification
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-03
---

# Initiative 50 — Asset classification

Per [`PRECEDENCE.md`](../../../references/hlk/compliance/PRECEDENCE.md).

## Canonical (planning)

| Path | Class | Validator |
|:-----|:------|:----------|
| `docs/wip/planning/50-live-cycle-closure/master-roadmap.md` | canonical | planning traceability conventions |
| `docs/wip/planning/50-live-cycle-closure/decision-log.md` | canonical | ditto |
| `docs/wip/planning/50-live-cycle-closure/evidence-matrix.md` | canonical | prose |
| `docs/wip/planning/50-live-cycle-closure/asset-classification.md` | canonical | ditto |
| `docs/wip/planning/50-live-cycle-closure/risk-register.md` | canonical | ditto |

## Canonical (config)

| Path | Change | Validator |
|:-----|:-------|:-----------|
| `config/eval/model-prices.json` | P2 — refresh per-model prices for 2026-Q2; bump `_last_reviewed` | `tests/test_model_prices.py` (new in P2) |

## Canonical (registries)

| Path | Change | Validator |
|:-----|:-------|:-----------|
| `docs/references/hlk/compliance/dimensions/POLICY_REGISTER.csv` | P2 (conditional) — three new `cost_ceiling` rows if D-IH-50-A formalize path | `validate_policy_register.py`, `validate_hlk.py` |
| `docs/references/hlk/compliance/FINOPS_COUNTERPARTY_REGISTER.csv` | P2 (conditional) — counterparty notes alignment if eval suppliers map | `validate_finops_counterparty_register.py`, `validate_hlk.py` |
| `docs/references/hlk/compliance/dimensions/PERSONA_SCENARIO_REGISTRY.csv` | P5 — append 1–3 scaffold rows from telemetry proposals (operator-merge only) | `validate_persona_scenario_registry.py`, `validate_hlk.py` |

## Canonical (code)

| Path | Change | Validator |
|:-----|:-------|:-----------|
| `akos/hlk_policy_register_csv.py` | P2 (conditional) — extend `VALID_POLICY_CLASSES` with `cost_ceiling` if D-IH-50-A formalize path | unit tests |

## Mirrored / derived

| Artefact | Source |
|:---------|:-------|
| `compliance.policy_register_mirror` | POLICY rows after operator apply |
| `compliance.dossier_run` | First live MADEIRA dossier emit (P3) writes a row |
| `compliance.eval_run` | First Tier-B smoke (P4) writes 2 rows (one per cell) |

## Reference-only / repo (non-governance)

| Path | Notes |
|:-----|:------|
| `tests/test_model_prices.py` | New schema/sanity test for `config/eval/model-prices.json` |
| `reports/dossier-first-live-emit-*.md` | P3 evidence |
| `reports/p4-tier-b-smoke-*.md` | P4 evidence |
| `reports/uat-i50-live-cycle-closure-*.md` | P6 closure |

## Doc/rule sync triggers

| Path | Trigger |
|:-----|:--------|
| `CHANGELOG.md` | P6 entry |
| `docs/wip/planning/README.md` | P0 row added; P6 status flipped to Closed |
| `docs/wip/planning/WIP_DASHBOARD.md` | P0 + P6 re-render |

