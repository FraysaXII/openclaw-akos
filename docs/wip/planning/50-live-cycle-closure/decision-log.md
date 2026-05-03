---
language: en
status: active
initiative: 50-live-cycle-closure
report_kind: decision-log
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-03
---

# Initiative 50 — Decision log

Four decisions seeded with default positions per the cursor plan; operator-ratified at greenlight 2026-05-03.

## D-IH-50-A — Cost-ceiling formalization

**Decision (default):** Formalize cost ceilings as POLICY rows. Add a new `cost_ceiling` `policy_class` to `akos/hlk_policy_register_csv.py::VALID_POLICY_CLASSES` and seed three rows:

- `POL-EVAL-COST-CEILING-DOSSIER-V1` (`min_pass_score` re-purposed as `max_usd_per_run`; canonical `MAX_DOSSIER_USD` source)
- `POL-EVAL-COST-CEILING-PERSONA-V1` (canonical `MAX_PERSONA_USD` source)
- `POL-EVAL-COST-CEILING-JUDGE-V1` (canonical `--judge-cost-cap` source)

**Alternative considered:** Keep env-var pattern only (`MAX_DOSSIER_USD`, `MAX_PERSONA_USD`, `--judge-cost-cap`) and document in CHANGELOG/SOP without POLICY rows.

**Rationale:** Symmetry with I47 P12 `judge_threshold` POLICY rows. Auditability + dossier traceability + per-row operator approval cadence already exist for `judge_threshold`; `cost_ceiling` benefits from the same pattern. Env vars stay (operator override path) but POLICY rows are the canonical source.

**Reversibility:** High — POLICY rows can be deprecated; env vars stay as override.

**Operator answer (2026-05-03 plan iteration):** Formalize.

---

## D-IH-50-B — `MAX_DOSSIER_USD` for first live emit

**Decision:** $5 (default; can raise after first run). Sized to keep first emit safely below "operator wants to see this go through" envelope; matches the spend-cap in plan §"Initiative 50 P3".

**Reversibility:** High — env var per-run.

---

## D-IH-50-C — Tier-B smoke cell selection

**Decision:** 2 cells, picked from the highest-value-per-query persona × scenario_class slice. Default: `(OPERATOR, hard)` and `(PERSONA-INVESTOR-COLD, hard)` to exercise both internal-voice and external-cold paths under stress.

**Reversibility:** High — cells can be swapped per run.

---

## D-IH-50-D — Telemetry promotion merge cadence

**Decision:** 1–3 per cycle (default). Larger batches require explicit operator review. Per AKOS governance rule on `PERSONA_SCENARIO_REGISTRY.csv` edits, every merged scenario gets a per-row decision-log entry (G-50-2).

**Rationale:** Bounded operator review effort + traceability per row.

**Reversibility:** High — cadence tunable per cycle.

---

## Decisions deferred (out of I50 scope, candidates for I51+)

- **D-DEFER-50-α** — Mirror reseed for `compliance.persona_scenario_registry_mirror` (handled in I51 P1; OPS-47-9 closure).
- **D-DEFER-50-β** — Live judge activation (handled in I52).

---

## Decisions made during execution

- **2026-05-03 (D-IH-50-A execution)** — Formalize path taken. `cost_ceiling` `policy_class` was already present in `akos/hlk_policy_register_csv.py::VALID_POLICY_CLASSES` (added at I45 P4 for skill-level ceilings); no code change required to extend it for runtime ceilings. Three new POLICY rows shipped at the runtime envelope tier:
  - **`POL-EVAL-COST-CEILING-DOSSIER-V1`** — `max_usd_per_run=5.00` (anchors `MAX_DOSSIER_USD` env default; canonical for first-live MADEIRA dossier emit in P3).
  - **`POL-EVAL-COST-CEILING-PERSONA-V1`** — `max_usd_per_persona=5.00` (anchors `MAX_PERSONA_USD` env default; per-persona Tier-B envelope).
  - **`POL-EVAL-COST-CEILING-JUDGE-V1`** — `max_usd_per_scenario=0.01` (anchors `--judge-cost-cap` CLI default; pre-sized for I52 multi-judge consensus voting).

  Env vars + CLI flags **stay** as override paths; POLICY rows are the canonical source of truth (auditability + dossier traceability symmetry with I47 P12 `judge_threshold`). `validate_hlk.py` now reports **8 `cost_ceiling` rows** (5 skill-level pre-existing + 3 new runtime-envelope rows), all passing the POLICY_REGISTER validator. Post-write counts: 29 total POLICY rows.

- **2026-05-03 (D-IH-50-A execution, FINOPS counterparty alignment)** — **No-op**. `FINOPS_COUNTERPARTY_REGISTER.csv` currently contains 2 placeholder rows (`finops_example_cloud_platform`, `finops_example_customer`); no actual Anthropic / OpenAI / Ollama / RunPod / Kalavai counterparty rows exist yet. Adding real vendor rows is a substantive future tranche requiring operator approval (out of I50/P2 scope). The **alignment** clause of D-IH-50-A is therefore **closed as N/A** for this cycle; if operator stands up real counterparty rows later, P2 of the next cycle should align them with `model-prices.json` then.

- **2026-05-03 (D-IH-50-A execution, model-prices.json refresh)** — All five canonical model entries verified against published 2026-Q2 rates (web search 2026-05-03):
  - `anthropic:claude-3-5-sonnet-20241022`: $3/M input + $15/M output → unchanged.
  - `openai:gpt-4o`: $2.50/M input + $10/M output → unchanged. Annotated as **legacy** per OpenAI 2026-Q2 (superseded by gpt-5.x family); pricing retained for historical cassette reproducibility.
  - `openai:gpt-4o-mini`: $0.15/M input + $0.60/M output → unchanged.
  - `ollama:nomic-embed-text` + `deterministic:akos.intent.classify_request`: $0/$0 → unchanged.

  No new model entries added in I50/P2 — multi-model judge roster expansion is the I52/P1 deliverable. `_last_reviewed` bumped to `2026-05-03`; `_2026_q2_review_note` field documents the verification + legacy classification.

- **2026-05-03 (D-IH-50-A execution, schema test)** — `tests/test_model_prices.py` shipped (18 tests, all PASS): file existence, top-level keys, ISO date format, FinOps owner role, required per-model fields, valid tier enum, non-negative prices, output ≥ input invariant, cheap-tier strictly cheaper than flagship, deterministic/local zero-priced invariant, 2026-Q2 reference price hard-pin, review-note presence. Locks in the I50 P2 truth-up against silent regressions (R-50-1).

- **2026-05-03 (D-IH-50-C execution)** — 2-cell smoke ran as planned: `(OPERATOR, hard)` and `(PERSONA-INVESTOR-COLD, hard)`. Plus a Cell-0 baseline (no persona filter) for broader coverage. All three runs `overall_status: pass`; total spend **$0.00**; cost ceiling `$5.00` per run announced + honored via `POL-EVAL-COST-CEILING-PERSONA-V1`. Persona-filtered cells returned `rows_after_filter=0` because `tests/evals/cassettes/` is empty — a known I47-closure observation (4-D matrix infra wired; cassette population is the next prerequisite). Baseline (no filter) returned 14 PASS rows covering the 5 SKILL-* skills + CSV-load + module-level smoke probes. New OPS follow-up captured: **OPS-50-1 — Tier-B persona cassette population** (deferred to I51 P3, where the cassette generation work fits naturally with per-persona PASS-rate calculation for OPS-47-6/9 closure).
