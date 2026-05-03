---
language: en
status: closed
initiative: 50-live-cycle-closure
report_kind: phase-report
phase: P2
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-03
---

# I50 P2 — Cost SSOT truth-up + cost-ceiling formalization

## Outcome

D-IH-50-A executed with **default formalize path**. Three new runtime-envelope POLICY rows shipped, `model-prices.json` refreshed for 2026-Q2, schema test added (18 cases, all green).

## Web-search evidence (2026-Q2 published prices, 2026-05-03)

| Model | Input/M | Output/M | Input/1k | Output/1k | Source |
|:------|:------:|:------:|:------:|:------:|:------|
| anthropic:claude-3-5-sonnet-20241022 | $3.00 | $15.00 | 0.003 | 0.015 | aicostcheck.com 2026 + pricepertoken.com + kickllm.com (3 concordant sources) |
| openai:gpt-4o | $2.50 | $10.00 | 0.0025 | 0.01 | platform.openai.com/docs/pricing (note: gpt-4o now classified legacy) |
| openai:gpt-4o-mini | $0.15 | $0.60 | 0.00015 | 0.0006 | platform.openai.com/docs/pricing + GPT-4o-mini model page |

All three entries match the existing values in `config/eval/model-prices.json` → **no price change needed**, only metadata refresh.

## File changes

### `config/eval/model-prices.json`
- `_last_reviewed`: `2026-05-01` → **`2026-05-03`**
- New top-level key: **`_2026_q2_review_note`** documenting the verification + GPT-4o legacy classification + I52 deferment for new entries.
- New per-model `_note` on `openai:gpt-4o`: legacy classification per OpenAI (superseded by gpt-5.x; pricing retained for cassette reproducibility).
- All five model entries unchanged (prices verified accurate).

### `docs/references/hlk/compliance/dimensions/POLICY_REGISTER.csv`
- New rows (3): `POL-EVAL-COST-CEILING-DOSSIER-V1`, `POL-EVAL-COST-CEILING-PERSONA-V1`, `POL-EVAL-COST-CEILING-JUDGE-V1`.
- All `policy_class=cost_ceiling`; `applies_to_schema=*`; `applies_to_table=*`; `cadence=continuous`; owners: Business Controller (DOSSIER, PERSONA), System Owner (JUDGE).
- Anchors: `max_usd_per_run=5.00` (DOSSIER), `max_usd_per_persona=5.00` (PERSONA), `max_usd_per_scenario=0.01` (JUDGE).
- Env vars + CLI flags retained as override paths (`MAX_DOSSIER_USD`, `MAX_PERSONA_USD`, `--judge-cost-cap`).

### `tests/test_model_prices.py` (NEW)
- 18 tests covering: file existence, top-level key set, ISO date format on `_last_reviewed`, FinOps owner discipline, required per-model fields, valid tier enum (deterministic/cheap/mid/flagship), non-negative prices, **output ≥ input invariant** (commercial provider sanity), **cheap-tier strictly cheaper than flagship-tier** (catches accidental tier swap), **deterministic/local zero-priced** (catches accidental LLM substitution per POL-EVAL-COST-CEILING-SHARED-LOCALE-DETECT pattern), **2026-Q2 reference price hard-pin** for the three commercial entries, review-note presence.

## Verification

```text
$ py -m pytest tests/test_model_prices.py -v --tb=short
============================= 18 passed in 0.17s ==============================

$ py scripts/validate_hlk.py
...
  POLICY_REGISTER Validator
  ========================================
  Rows validated:     29
  Policies:           29
  By class:
    cost_ceiling             8
    judge_threshold          3
    rls                      9
    ...
  PASS
  POLICY_REGISTER: PASS
  OVERALL: PASS
```

`cost_ceiling` count: 5 (skill-level, I45 P4) → **8** (skill-level + 3 new runtime-envelope). Total POLICY rows: 26 → 29.

## D-IH-50-A — closure

- **Formalize cost ceilings as POLICY rows** (default path): **DONE**.
- **FINOPS counterparty alignment**: **N/A this cycle** — `FINOPS_COUNTERPARTY_REGISTER.csv` carries only 2 placeholder rows; no actual Anthropic/OpenAI/Ollama/RunPod/Kalavai vendor rows exist. Standing up real counterparty rows is out of I50/P2 scope (operator-approved tranche).
- **`tests/test_model_prices.py`**: shipped, 18/18 green.

## Cross-references

- E2 in [`evidence-matrix.md`](../evidence-matrix.md) (stale `_last_reviewed` cleared).
- E3 in [`evidence-matrix.md`](../evidence-matrix.md) (no `POL-EVAL-COST-CEILING-*` runtime rows existed; now 3 added).
- E5 in [`evidence-matrix.md`](../evidence-matrix.md) (FINOPS alignment closed N/A).
- E8 in [`evidence-matrix.md`](../evidence-matrix.md) (`tests/test_model_prices.py` did not exist; now ships).
- R-50-1 in [`risk-register.md`](../risk-register.md) (price regression; mitigation now active via 2026-Q2 reference hard-pin test).

## Operator gate

**G-50-1** (cost-ceiling formalization) — **closed at default formalize path**. Operator may revisit if env-var-only path becomes preferred; deprecation cadence is per-row standard POLICY lifecycle.
