---
language: en
report_kind: phase_closure
phase: P6
status: closed
closed_at: 2026-05-06
initiative: I59 — HLK governance promotion + clean slate cycle
---

# I59 P6 — OPS-58-3 rubric fix (closure)

## Root cause

`_heuristic_persona_fit` in `akos/eval_harness/judge.py` returned a flat 3
whenever `persona is None`, which was the common case because
`score_response_offline` received `persona=None` from most callers even when
the scenario carried a `persona_id`. The I58 calibration burns showed 0%
alignment on persona_fit for exactly this reason.

## Fix (Path A from I59 plan)

1. Added `PERSONA_CSV` path constant and `_PERSONA_CACHE` dict at module level.
2. Added `_load_persona_registry()` → `{persona_id: row_dict}` (cached on first
   call; reads `docs/references/hlk/compliance/dimensions/PERSONA_REGISTRY.csv`).
3. Added `resolve_persona(scenario, persona)` — returns `persona` when not
   `None`; otherwise looks up `scenario["persona_id"]` in the registry.
4. `score_response_offline` now calls `resolve_persona(scenario, persona)` to
   obtain a real persona dict before passing it to `_heuristic_persona_fit`.
5. The heuristic logic itself is unchanged — it already handled persona dicts
   correctly. The bug was exclusively that it never received one.

## OPS_REGISTER flip

`OPS-58-3` row in `docs/references/hlk/compliance/OPS_REGISTER.csv` flipped
from `status=open` to `status=closed`, `closed_at=2026-05-06`, with
`evidence_path` pointing to this report and `rice_score=149`.

## Tests

`tests/test_judge_persona_fit_offline.py` — 14 tests:

- `TestHeuristicPersonaFit` (7): None persona → 3, empty response → 1,
  qualification_gate match → 5, qualification_gate miss → 3, cold persona
  escalate → 5, cold persona no-escalate → 3, warm persona → 4.
- `TestResolvePersona` (4): passed persona wins, no persona_id → None,
  resolves from registry, unknown id → None.
- `TestScoreResponseOfflineWithResolve` (3): persona resolved from scenario
  produces correct score, no persona_id falls back to neutral 3, explicit
  persona overrides registry.

All pass.

## Cross-references

- I58 calibration burns: `docs/wip/planning/58-cycle-2-multi-track-forward/reports/ops-58-1-2026-05-06.md`
- Decision: `D-IH-58-J` (forwarded as engineering follow-up)
- Decision: `D-IH-59-J` (OPS-58-3 lands in I59 P6 scope)
