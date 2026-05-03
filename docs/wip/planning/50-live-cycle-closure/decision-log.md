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

_Append phased ratifications below as they land._
