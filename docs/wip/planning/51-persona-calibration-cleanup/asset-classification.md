---
language: en
status: active
initiative: 51-persona-calibration-cleanup
report_kind: asset-classification
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-03
---

# Initiative 51 — Asset classification

Per [`PRECEDENCE.md`](../../../references/hlk/compliance/PRECEDENCE.md).

## Canonical (planning)

| Path | Class | Validator |
|:-----|:------|:----------|
| `docs/wip/planning/51-persona-calibration-cleanup/master-roadmap.md` | canonical | planning traceability conventions |
| `docs/wip/planning/51-persona-calibration-cleanup/decision-log.md` | canonical | ditto |
| `docs/wip/planning/51-persona-calibration-cleanup/evidence-matrix.md` | canonical | prose |
| `docs/wip/planning/51-persona-calibration-cleanup/asset-classification.md` | canonical | ditto |
| `docs/wip/planning/51-persona-calibration-cleanup/risk-register.md` | canonical | ditto |

## Canonical (registries)

| Path | Change | Validator |
|:-----|:-------|:-----------|
| `docs/references/hlk/compliance/dimensions/PERSONA_SCENARIO_REGISTRY.csv` | P3 — D-IH-51-A default: new optional `target_difficulty_band` column on each persona row OR scenario rebalance | `validate_persona_scenario_registry.py`, `validate_hlk.py`; G-51-1 operator gate |
| `docs/references/hlk/compliance/dimensions/POLICY_REGISTER.csv` | P4 (conditional) — `POL-EVAL-FLAKE-THRESHOLD-V1` row | `validate_hlk.py`; G-51-2 operator gate |

## Canonical (code)

| Path | Change |
|:-----|:-------|
| `scripts/sync_compliance_mirrors_from_csv.py` | P1 — add `_emit_persona_scenario_registry_upserts()` |
| `scripts/quarantine_scenario.py` | P4 — add `--auto-from-flake-history` flag |
| `akos/hlk_persona_scenario_csv.py` | P3 (conditional) — add `target_difficulty_band` field if D-IH-51-A column path |
| `akos/hlk_policy_register_csv.py` | P4 (conditional) — extend `VALID_POLICY_CLASSES` with `flake_threshold` if D-IH-51-B formalize path |
| `scripts/eval.py` | P5 — add `--hard-fail-on-drift` flag |

## Canonical (config)

| Path | Change |
|:-----|:-------|
| `config/verification-profiles.json` | P5 — new `eval_calibration_hard_fail` step in `eval_tier_b_weekly` profile |

## Mirrored / derived

| Artefact | Source |
|:---------|:-------|
| `compliance.persona_scenario_registry_mirror` | P1 reseed via service_role; 329 rows expected at start (post-I50 P5) |
| `compliance.policy_register_mirror` | P4 (conditional) — flake-threshold POLICY row sync |

## Reference-only / repo (non-governance)

| Path | Notes |
|:-----|:------|
| `tests/test_persona_scenario_mirror_emit.py` | New test for P1 emitter |
| `tests/test_eval_persona_calibration.py` | Extension for `--hard-fail-on-drift` (P5) |
| `tests/test_scenario_quarantine.py` | Extension for auto-flake (P4) |
| `reports/calibration-audit-*.md` | P2 evidence |
| `reports/p1-mirror-reseed-*.md` | P1 evidence |
| `reports/uat-i51-persona-calibration-cleanup-*.md` | P6 closure |

## Doc/rule sync triggers

| Path | Trigger |
|:-----|:--------|
| `CHANGELOG.md` | P6 entry |
| `docs/wip/planning/README.md` | P0 row added; P6 status flipped to Closed |
| `docs/wip/planning/WIP_DASHBOARD.md` | P0 + P6 re-render |
| `docs/USER_GUIDE.md` | P3 (conditional) — document `target_difficulty_band` in HLK Operator Model section if column added |
| `SOP-HLK_PERSONA_SCENARIO_MIRROR_001.md` (new) OR `SOP-META_PROCESS_MGMT_001` follow-on | D-IH-51-D — mirror reseed cadence policy doc |
