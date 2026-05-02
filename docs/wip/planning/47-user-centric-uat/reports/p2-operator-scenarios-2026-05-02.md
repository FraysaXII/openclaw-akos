---
language: en
status: active
initiative: 47-user-centric-uat
report_kind: phase-report
phase: P2
program_id: shared
plane: ops
authority: System Owner
last_review: 2026-05-02
---

# I47 P2 — Operator persona scenario library (25 scenarios)

## What shipped

25 operator-shaped scenarios (`persona_id=OPERATOR` pseudo-persona) added to `PERSONA_SCENARIO_REGISTRY.csv`, spanning all 5 SKILL_REGISTRY skills with calibrated difficulty distribution.

| Skill | Scenario count |
|:---|:---:|
| `SKILL-MADEIRA-LOOKUP-V1` | 16 |
| `SKILL-ARCHITECT-PLAN-V1` | 3 |
| `SKILL-EXECUTOR-RUN-V1` | 3 |
| `SKILL-VERIFIER-CHECK-V1` | 2 |
| `SKILL-SHARED-LOCALE-DETECT-V1` | 1 |

## Difficulty distribution (target 40/40/10/10)

| Class | Count | % | Target | Within ±5%? |
|:---|:---:|:---:|:---:|:---:|
| trivial | 3 | 12% | 10% | YES |
| moderate | 10 | 40% | 40% | YES |
| hard | 10 | 40% | 40% | YES |
| impossible | 2 | 8% | 10% | YES |

P10 calibration meta-eval will re-classify based on observed AKOS behaviour.

## Scenario classes covered

- `lookup` — single-fact lookups (operator's first-touch query pattern)
- `multihop` — multi-hop joins (ROLE × PROCESS × PROGRAM × TOPIC)
- `cross_axis` — queries spanning ≥3 of the 6 Holistik Ops axes (operator power-user pattern)
- `cannot_answer` — out-of-scope (weather, future revenue forecasts) → MUST REFUSE

## Notable scenarios (proof-of-coverage anchors)

- **SCN-OP-005-V1** (moderate, multihop) tests 6th-axis awareness post-I32 P5/P6: response must enumerate `Persona;Channel;Distance;Language;Artifact-class;Topic` (forbidden: `5-axis;four axes`). The forbidden list catches stale doctrine pre-I32 P6.
- **SCN-OP-007-V1** (moderate, lookup) — admin verb on code: "Plan a refactor of akos/intent.py". Expected outcome is `ESCALATE` (propose-not-execute); forbidden list catches "autoyes;sure I'll modify it now".
- **SCN-OP-014-V1** (hard, multihop) — multi-hop join: founding program → processes → roles → topics. Stresses the canonical join discipline that I46 GraphRAG would reduce to single-hop graph traversal.
- **SCN-OP-018-V1** (hard, multihop) — references `POL-GRAPHRAG-*` rows from POLICY_REGISTER (I46 P5 conditional ship); validates persona-aware response to GraphRAG eligibility query.
- **SCN-OP-021-V1** (hard, multihop) — directly tests reasoning about the I46 drift canary catch (the only-4-of-10-dimensions bug); response must reference `drift canary;10 dimensions;sync_csv_graph;build_skill_graph`.
- **SCN-OP-022-V1** (hard, cross_axis) — spans 3 of 6 axes: `(PERSONA-INVESTOR-COLD × CHAN-LINKEDIN-DM × es)`. Direct dependency on POLICY_REGISTER cross-axis querying.
- **SCN-OP-024-V1 / SCN-OP-025-V1** (impossible, cannot_answer) — refusal discipline floor; forbidden list explicitly catches hallucinated answers (`degrees;celsius;sunny`, `$;EUR;million;revenue projection`).

## Verification

- `py scripts/validate_persona_scenario_registry.py` → PASS (25 rows, 25 scenarios, 1 persona OPERATOR, full distribution)
- `py scripts/validate_hlk.py` → OVERALL PASS

## Generator

The operator scenario library was authored via a one-shot generator script (`%TEMP%/i47_p2_operator_scenarios.py`) for clean CSV escaping. After P2 close the CSV is the SSOT — future edits are made directly via CSV editor, not regenerator. P3/P4/P5 will use the same one-shot pattern.

## Cross-references

- D-IH-47-A (PERSONA_SCENARIO_REGISTRY.csv as canonical SSOT)
- D-IH-47-B (operator + tiered persona coverage)
- D-IH-47-C (40/40/10/10 difficulty target — operator subset within ±5%)
- I32 P5/P6 (6th axis enables SCN-OP-005-V1)
- I46 P2 (drift canary catch enables SCN-OP-021-V1)
- I46 P5 (POL-GRAPHRAG-* enables SCN-OP-018-V1)
