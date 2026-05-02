---
language: en
status: active
initiative: 47-user-centric-uat
report_kind: scenario-taxonomy
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-02
---

# Initiative 47 — Scenario taxonomy + difficulty calibration framework

> Per D-IH-47-A, every scenario in PERSONA_SCENARIO_REGISTRY.csv carries 5 typed dimensions. Per D-IH-47-C, difficulty is auto-classified from observed AKOS behavior (not assigned by feel). This file defines the taxonomy + calibration framework that drives P0-P10.

## The 5 scenario dimensions

Every row in `PERSONA_SCENARIO_REGISTRY.csv` carries these 5 typed fields:

| Dimension | Type | Source | Purpose |
|:----------|:-----|:-------|:--------|
| **persona_id** | FK to PERSONA_REGISTRY.csv (16 archetypes) | I31 P2 registry | Who is asking? Drives expected register, language, distance band |
| **skill_id** | FK to SKILL_REGISTRY.csv (5 skills today) | I32 P2 + I45 P3 + I46 P5 | What capability is being exercised? |
| **scenario_class** | enum (lookup, multihop, adversarial, recovery, benchmark, cross_axis, cannot_answer) | I47 P0 | What kind of scenario? Drives test surface (cassette dir, evaluator path) |
| **difficulty_class** | enum (trivial, moderate, hard, impossible) | I47 P0 + auto-classified by P10 calibration | How hard is it? Drives the 40/40/10/10 distribution target |
| **expected_outcome_class** | enum (PASS, GROUND, ESCALATE, REFUSE) | I47 P0 | What SHOULD the system do? Distinct from difficulty |

The 4 expected_outcome_classes:
- **PASS** — system answers correctly with adequate citation/register/persona-fit
- **GROUND** — system answers BUT must cite a canonical path (citation discipline gate)
- **ESCALATE** — system MUST route to admin_escalate or execution_escalate (cannot answer in-band)
- **REFUSE** — system MUST refuse (cannot-answer or out-of-scope; tested by impossible-by-design scenarios)

## The 7 scenario classes

| Class | Description | Phase | Cassette directory |
|:------|:------------|:------|:-------------------|
| **lookup** | Single-fact lookup ("who is the System Owner") | P2-P5 | `tests/evals/cassettes/persona/<persona_id>/` |
| **multihop** | Multi-step retrieval ("find the role that owns the FinOps process under the founding program") | P2-P5 | same as above |
| **adversarial** | Persona impersonation, indirect injection, persona-context jargon, tier-jumping, cross-persona leakage | P7 | `tests/evals/cassettes/adversarial_persona/<persona_id>/` |
| **recovery** | Degraded-state scenarios (Neo4j down, Aura auth fail, mirror stale, cost breach, etc.) | P9 | `tests/evals/cassettes/recovery/` |
| **benchmark** | LongMemEval-LIGHT + MASEval-LIGHT + Promptfoo curated subset | P8 | `tests/evals/cassettes/benchmark/<adapter>/` |
| **cross_axis** | Queries spanning ≥3 of the 6 Holistik Ops axes | P6 | `tests/evals/cassettes/cross_axis/` |
| **cannot_answer** | Out-of-scope queries ("what's the weather in Madrid"); MUST refuse not hallucinate | P6, P9 | `tests/evals/cassettes/cross_axis/` (subset) |

## The 4 difficulty classes (calibrated by P10 meta-eval)

Difficulty is **auto-classified by `scripts/calibrate_scenarios.py`** based on observed AKOS behavior at P0 + P10 + P15. Operator can override via CSV edit but must log rationale in decision-log.

| Class | Auto-classification rule | Distribution target (per D-IH-47-C) |
|:------|:-------------------------|:------------------------------------|
| **trivial** | First naive `classify_request(prompt)` returns the expected_route within 1 attempt; no persona context needed | 10% (sanity floor) |
| **moderate** | First naive call returns wrong route OR insufficient grounding; passes after persona context applied | 40% |
| **hard** | Requires multi-step retrieval OR cross-axis reasoning OR multi-hop graph traversal; first call almost always wrong; passes only with grounding | 40% |
| **impossible** | System MUST refuse / escalate; passing means correct refusal (the response says "I can't answer that" or routes to admin_escalate / execution_escalate appropriately) | 10% (refusal discipline floor) |

**Tolerance:** ±5% on each bucket. If P10 calibration reports outside tolerance, operator either (a) edits scenarios to rebalance OR (b) updates the target with rationale.

## The 16 persona archetypes (Tier classification per D-IH-47-B)

| Tier | Persona archetype | Scenario count | Notes |
|:----:|:------------------|:--------------:|:------|
| Op | (operator; you the founder) | 25 | Power user; spans all 5 skills + cross-axis |
| 1 | PERSONA-INVESTOR-COLD | 25 | LinkedIn DM origin; Spanish/English; cap-table-friendly intro deferred |
| 1 | PERSONA-INVESTOR-WARM | 25 | Warm referral; tighter SLA; bridge person referenced |
| 1 | PERSONA-ADVISOR-REFERRAL | 25 | Spanish dominant; ENISA / CNAE / instruments scope |
| 1 | PERSONA-CUSTOMER-KIRBE-PROSPECT | 25 | KiRBe trial flow; data residency; pricing |
| 2 | PERSONA-ADVISOR-COLD | 10 | Default low-priority; acknowledge-and-defer |
| 2 | PERSONA-PARTNER-JOINT-EQUITY | 10 | 3-of-3 gate per CHANNEL_STRATEGY Channel 6 |
| 2 | PERSONA-PARTNER-SUBCONTRACT | 10 | Existing partner pattern; SoW expected |
| 2 | PERSONA-TALENT-INBOUND | 10 | Portfolio + 1 reference required before call |
| 2 | PERSONA-VENDOR-OUTBOUND | 10 | Holistika sources externally; TEMPLATE_OUTBOUND_BRIEF |
| 2 | PERSONA-VENDOR-INBOUND | 10 | Low priority; sourcing register alignment check |
| 2 | PERSONA-EXISTING-CUSTOMER | 10 | Default-N1; renewals + expansion + support |
| 2 | PERSONA-EXISTING-PARTNER | 10 | Default-N1; ongoing collaboration |
| 3 | PERSONA-PRESS | 5 | Brand Manager handles; Founder vetoes if sensitive |
| 3 | PERSONA-IDEA-PROPOSER | 5 | Known person with project idea; informal first |
| 3 | PERSONA-RANDOM-INBOUND | 5 | Catch-all; re-bucket after 1-2 exchanges |
| 3 | PERSONA-CUSTOMER-SERVICE-PROSPECT | 5 | 30-min discovery call; scope-shaping doc |
| | **TOTAL persona scenarios** | **225** | |

Plus ~125 cross-cutting scenarios (cross_axis 25 + adversarial 30 + benchmark 30 + recovery 16) = **~350 scenarios total**.

## Calibration framework (P0 establishes; P10 validates)

`scripts/calibrate_scenarios.py` runs each scenario through current AKOS and emits per-scenario classification. Pseudocode:

```
for scenario in PERSONA_SCENARIO_REGISTRY:
    result = classify_request(scenario.prompt_text, agent=...)
    actual_route = result.route
    expected_route = scenario.expected_route

    if actual_route == expected_route:
        if result.confidence >= 0.9:
            difficulty = "trivial"
        else:
            difficulty = "moderate"
    elif scenario.expected_outcome_class == "ESCALATE" and actual_route in escalation_routes:
        difficulty = "moderate"  # got the right escalation; not trivially correct
    elif scenario.expected_outcome_class == "REFUSE" and actual_route == "other":
        difficulty = "moderate"  # appropriate non-action
    else:
        difficulty = "hard"  # requires grounding/multi-step beyond classify_request
    # Special: cassette replay attempts grounding; if grounding still fails → impossible-or-bug
```

The auto-classified `difficulty_class` is written back to PERSONA_SCENARIO_REGISTRY.csv at P10 close. Operator can override manually with rationale in decision-log.

## Difficulty distribution dashboard

P10 produces `reports/calibration-baseline-2026-05-XX.md` with:

```
Persona            Trivial  Moderate  Hard  Impossible  Target met?
operator             3 (12%)  10 (40%) 11 (44%)  1 (4%)     YES
PERSONA-INVESTOR-COLD 2 (8%)   9 (36%) 12 (48%)  2 (8%)     YES (within ±5%)
...
TOTAL              35 (10%) 140 (40%) 140 (40%) 35 (10%)    YES
```

If any persona is outside ±5%, operator either rebalances scenarios or accepts with rationale.

## Cross-references

- D-IH-47-A (PERSONA_SCENARIO_REGISTRY.csv as canonical SSOT)
- D-IH-47-B (tiered persona coverage)
- D-IH-47-C (40/40/10/10 difficulty target)
- I31 P2 (PERSONA_REGISTRY.csv source)
- I32 P2 (SKILL_REGISTRY.csv source)
- I45 P1 (eval harness Scorecard pattern that P10 extends)
- I45 P5 (adversarial cassette pattern that P7 extends with persona context)
- I46 P5 (retrieval_mode column will be tested per persona × per skill)
- I46 P4 ADR (agent memory deferred — informs P8 LongMemEval-LIGHT REFUSE behavior)
