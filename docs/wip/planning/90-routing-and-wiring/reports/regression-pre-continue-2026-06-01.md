---
intellectual_kind: regression_report
sharing_label: internal_only
initiative_id: INIT-OPENCLAW_AKOS-90
authored: 2026-06-01
language: en
linked_decisions:
  - D-IH-90-R
  - D-IH-90-H
---

# Regression sweep — pre-continue (2026-06-01)

Scope: validate I90 P2/P3 surfaces before GATE #2 sign-off and I91 execution.

## I90-specific (PASS)

| Check | Command | Result |
|:---|:---|:---|
| Rule tiers self-test | `py scripts/validate_cursor_rule_tiers.py --self-test` | **PASS** (core=3 max=4) |
| Rule tiers full scan | `py scripts/validate_cursor_rule_tiers.py` | **PASS** (34 rules, 3 always-on) |
| Rule×skill self-test | `py scripts/validate_rule_skill_pairing.py --self-test` | **PASS** |
| Rule×skill full scan | `py scripts/validate_rule_skill_pairing.py` | **PASS** (21/21 paired) |
| HLK umbrella | `py scripts/validate_hlk.py` | **PASS** |
| I90 unit tests | `pytest tests/test_validate_cursor_rule_tiers.py tests/test_validate_rule_skill_pairing.py` | **PASS** (8 tests) |
| Hook scripts syntax | `py -m py_compile .cursor/hooks/*.py` | **PASS** |
| Inter-wave self-test | `py scripts/inter_wave_regression_sweep.py --self-test` | **PASS** |

## Pre-commit profile (`py scripts/verify.py pre_commit`)

**Stopped at `test_all`:** 3497 passed, **7 failed**, 17 skipped (~6m15s).

### Failures tied to I90 (fixed in working tree, not yet committed)

| Test | Cause | Fix |
|:---|:---|:---|
| `test_validate_review_stamps` (4 tests) | OPS-86-23 `last_review_decision_id` had semicolon list `D-IH-86-CZ;D-IH-90-H` | Single ID `D-IH-90-H` + `D-IH-90-H` in `linked_decision_ids` |
| `test_repo_health_snapshot::test_akos_mirror_*` | Test expected `alwaysApply: true`; I90 P2 set template to `false` in AKOS | Test updated to match D-IH-90-R posture |

### Failures **not** attributed to I90 (pre-existing / environmental)

| Test | Notes |
|:---|:---|
| `test_company_deck::test_slide_11_*` | Deck content assertion — unrelated to rule tiers |
| `test_release_gate_external_repo_check::*` | 2 external repo contract issues (41 repos skipped) — sibling-repo drift |
| `test_validate_review_stamps` expanded class | Same OPS stamp class; fixed by OPS row correction |

## Advisory (non-blocking)

- `validate_hlk.py`: 18 process_list pairing WARNs (deferred SOP/runbook; D-IH-72-W pattern)
- Initiative frontmatter: 3 `last_review` mismatches (17, 81, 86)
- Master-roadmap: I65 missing `closed_at` companion (pre-existing)

## Verdict

| Lane | Status |
|:---|:---|
| **I90 mechanical bar** | **PASS** — safe to continue I91 charter / GATE #2 review |
| **Full repo pre_commit** | **FAIL** until OPS stamp fix + test fix committed; 2 unrelated test failures remain |

## Re-verify after fix commit

```powershell
py scripts/validate_review_stamps.py
py -m pytest tests/test_validate_review_stamps.py::TestRealCanonicalsSmoke tests/test_repo_health_snapshot.py::test_akos_mirror_cursor_rule_template_exists_and_loads_always -q
```
