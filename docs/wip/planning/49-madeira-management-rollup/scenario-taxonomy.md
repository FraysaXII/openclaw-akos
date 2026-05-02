---
language: en
status: active
initiative: 49-madeira-management-rollup
report_kind: scenario-taxonomy
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-03
---

# Initiative 49 — Scenario taxonomy extensions (PERSONA_SCENARIO_REGISTRY)

**Base taxonomy:** inherits all dimensions from Initiative 47 ([`scenario-taxonomy.md`](../47-user-centric-uat/scenario-taxonomy.md)): `persona_id`, `skill_id`, `scenario_class`, `difficulty_class`, `expected_outcome_class`, tenant axis, lifecycle.

This initiative adds **management dimensions** without changing persona scenario semantics:

| Field | Purpose | Allowed values |
|:------|:--------|:---------------|
| `priority_score` | Deterministic backlog sort | Non-negative float; computed by calibration (P2); operator may override with rationale in `decision-log` |
| `safety_lane` | Pins scenario to top regardless of score | `true`, `false` (empty treated as false) |
| `release_blocking` | Active scenarios that gate a GO verdict | `true`, `false` |
| `lifecycle_status` extended | Anti-flake quarantine | Adds `quarantined` (P10); quarantined rows excluded from normal verdict numerator |

**Relationship to MADEIRA UC-IDs:**

- UC rows in [`coverage-matrix.md`](../17-madeira-cursor-mode-parity/coverage-matrix.md) map to one or many registry rows via shared exemplar intents; coverage matrix carries a readable **priority** column aligned to `priority_score` order.

