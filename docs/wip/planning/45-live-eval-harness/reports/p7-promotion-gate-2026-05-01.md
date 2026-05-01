---
language: en
status: active
intellectual_kind: phase_report
role_owner: System Owner
area: Tech / Holistik Ops
entity: Holistika Research
authority: Founder + System Owner
last_review: 2026-05-01
artifact_role: governed_evidence
topic_ids:
  - topic_skill_registry
parent_topic: topic_skill_registry
---

# I45 P7 — Skill promotion gate

**Phase:** P7 (4-criteria graduation gate; tooling-enforced)
**Closes:** I45 P7 + evidence-matrix E6 (skill promotion is honour-based) + R-45-9 mitigation operationalized.
**Date:** 2026-05-01

## Actions

1. **`akos/eval_harness/promotion.py`** (~165 lines) — promotion evaluator:
   - `CriterionResult` and `PromotionVerdict` dataclasses (JSON-serializable)
   - 4 per-criterion check functions:
     - `check_tier_a_green(skill_id)` — runs `--mode all`; PASS if all skill rows pass
     - `check_tier_b_recent(skill_id, within_days=14)` — currently SKIPs with explicit reason (compliance.eval_run not yet populated; activates when P6 weekly workflow runs)
     - `check_adversarial_pass(skill_id)` — at least 1 adversarial cassette exists AND replays PASS
     - `check_routing_condition_non_empty(skill_id)` — SKILL_REGISTRY row has non-empty routing_condition
   - `evaluate_promotion(skill_id, override=False, override_reason="")` — aggregator; FAIL if any criterion fails; PASS if all pass or skip (SKIP is "data not yet available" — operator-readable)
   - Operator override path returns `OVERRIDE` verdict with audit-trailed reason

2. **`scripts/eval.py promote` subcommand** wired with full args:
   - `--skill <id>` (required)
   - `--override` (bypass; requires `--reason`)
   - `--reason <text>` (mandatory with `--override`; audit trail per R-45-9)
   - `--json` (machine-readable verdict)
   - Exit codes: 0 = PASS or OVERRIDE; 1 = FAIL; 2 = bad args (override without reason)

3. **POLICY_REGISTER row**: `POL-EVAL-PROMOTION-GATE` (`policy_class=promotion_gate`):
   - States the 4 criteria
   - Names the enforcer: `py scripts/eval.py promote --skill <id>`
   - Override path documented (operator override + reason → audit row in compliance.eval_run + quarterly review)

4. **17 new tests** in `tests/test_eval_promotion.py`:
   - Per-criterion checks (7 tests): pass/fail for routing_condition, adversarial_pass, tier_a, tier_b SKIP semantics
   - Aggregate verdict (4 tests): MADEIRA passes (3 PASS + 1 SKIP); SHARED-LOCALE fails on routing_condition; unknown skill fails on >=2 criteria; override returns OVERRIDE
   - CLI surface (5 tests): exit 0 for pass; exit 1 for fail; exit 2 for override-without-reason; override+reason exits 0; --json emits structured verdict
   - Policy register coupling (1 test): POL-EVAL-PROMOTION-GATE row present

## Verification

- `py scripts/eval.py promote --skill SKILL-MADEIRA-LOOKUP-V1`: OVERALL: PASS (Tier A green + adversarial pass + non-empty routing_condition; Tier B SKIP with operator-readable reason)
- `py scripts/eval.py promote --skill SKILL-SHARED-LOCALE-DETECT-V1`: OVERALL: FAIL (empty routing_condition — by design, since SHARED-LOCALE is intentionally always-eligible). This is the correct behavior: a "shared utility skill" should not graduate to tenant-scope without an explicit policy decision.
- `py scripts/eval.py promote --skill X --override --reason "test"`: OVERALL: OVERRIDE; audit-trailed.
- `py scripts/eval.py promote --skill X --override` (no reason): exits 2 with "audit trail" error.
- `tests/test_eval_promotion.py`: **17/17 PASS** in 6.3s.

## Sample verdict output (markdown mode)

```text
  Promotion verdict: SKILL-MADEIRA-LOOKUP-V1
  ============================================================
 [+] tier_a_green                     [PASS] all 1 Tier A rows for SKILL-MADEIRA-LOOKUP-V1 passed
 [~] tier_b_recent                    [SKIP] compliance.eval_run not yet populated with live runs for SKILL-MADEIRA-LOOKUP-V1; check against last 14d will activate when P6 weekly workflow has executed at least once with AKOS_TIER_B_ENABLED=true.
 [+] adversarial_pass                 [PASS] all 7 adversarial cassettes for SKILL-MADEIRA-LOOKUP-V1 passed
 [+] routing_condition_non_empty      [PASS] routing_condition='intent_in=hlk_lookup;hlk_search'

  OVERALL: PASS
```

## What this does NOT do (deferred)

- **`compliance.eval_run` query path NOT YET wired** — `check_tier_b_recent` returns SKIP with explanatory reason. Once P6 weekly workflow runs and the mirror has data, this becomes a real Postgres query. P8 closure documents the operator-side wire-up SQL.
- **No automatic promotion** — promotion is operator-triggered (`promote --skill X`); the gate enforces, doesn't auto-execute. Per D-IH-45-F default position (rejected fully-automated alternative).
- **No quarterly override review automation** — operator-side cadence per R-45-9; no automated reminder shipped.

## Risks resolved

- **R-45-9 (promotion gate blocks urgent ship)**: explicitly handled via `--override --reason` audit trail; no rigid blocker. The gate enforces the 4 criteria but provides the escape valve with high-visibility audit.
- **D-IH-45-F honour-vs-tooling decision**: operationalized. No skill can promote without `py scripts/eval.py promote` returning exit 0 (or operator override).

## Operator-applied steps

1. **Test the gate today**: `py scripts/eval.py promote --skill SKILL-MADEIRA-LOOKUP-V1` returns 0; `--skill SKILL-SHARED-LOCALE-DETECT-V1` returns 1.
2. **Apply POLICY_REGISTER reseed** (the new promotion_gate row): `py scripts/sync_compliance_mirrors_from_csv.py --policy-only`.
3. **Wire to release-gate** (optional): add a step to `scripts/release-gate.py` that calls `eval.py promote --skill <each_changed_skill>` when SKILL_REGISTRY.csv has changed.

## Next phase

P8 — Tests + UAT + closure. Full pytest sweep + UAT report covering all 9 phases + CHANGELOG entry + WIP_DASHBOARD re-render + I45 closure assertion.
