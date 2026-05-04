---
language: en
status: closed
initiative: 32-holistik-ops-maturation
report_kind: phase-report
phase: P12
program_id: shared
plane: ops
authority: AI Engineer
last_review: 2026-05-04
---

# I32 P12 — Madeira eval harness + 5 skill drift canaries (cross-reference; 2026-05-04)

> **Status retrospective.** P12 deliverables shipped 2026-04-30 as substrate work; the harness it delivered was promoted into [Initiative 45 — Live Eval Harness Modernisation](../../45-live-eval-harness/master-roadmap.md) which closed 2026-05-01 and was status-flipped to Closed under [I57 P2](../../57-cycle-closeout-live-validation/reports/p2-i45-closure-2026-05-04.md). This phase report records the cross-reference and closes I32 P12 as **superseded by I45**.

## Outcome (substrate from 2026-04-30; harness ownership transferred to I45)

I32 P12 shipped the per-skill scorecard + 5 baseline JSONs + 5 drift canaries. Two canaries (canary 2 + canary 4) were live; canaries 1, 3, 5 were documented for operator (required live runtime). A synthetic regression test trips canary 2 at -3pp drop. **Substrate stable; harness ownership has since transferred to [I45](../../45-live-eval-harness/master-roadmap.md).**

## Deliverables (substrate; preserved from 2026-04-30)

| Artefact | Path | Status |
|:---------|:-----|:-------|
| Per-skill scorecard generator | [`scripts/eval_per_skill.py`](../../../../scripts/eval_per_skill.py) | Active; back-compat shim per [I45 P1](../../45-live-eval-harness/master-roadmap.md) — calls `scripts/eval.py --mode canary` |
| 5 baseline JSONs | [`config/eval-baselines/`](../../../../config/eval-baselines/) | Active; consumed by the I45 harness |
| Canary 2 + canary 4 | (operational) | Active |
| Canaries 1 + 3 + 5 | (documented for operator) | Active; require live runtime per the I32 P9 phase report |
| Synthetic regression test | [`tests/test_madeira_eval_per_skill.py`](../../../../tests/test_madeira_eval_per_skill.py) | Active (9 tests, 2 trip canary 2 at -3pp drop); part of the 1764-test sweep |
| Original P9-named report | [`p9-madeira-eval-canaries-2026-04-30.md`](p9-madeira-eval-canaries-2026-04-30.md) | Existing; documents the substrate work in detail (note: numbered `p9` in the report file because the I32 closure UAT compressed the master-roadmap's P12 into UAT-section "P9 Madeira eval canaries") |

## Ownership transfer to I45

I45 P0 audit ([`docs/wip/planning/45-live-eval-harness/reports/audit-current-eval-surface-2026-05-01.md`](../../45-live-eval-harness/reports/audit-current-eval-surface-2026-05-01.md)) identified that the I32 P12 substrate (`scripts/eval_per_skill.py` + per-skill scorecard) was one of the 3 evaluation systems that needed to be unified into a single CLI surface. I45 P1 unified them: `scripts/eval_per_skill.py` is now a back-compat shim → `scripts/eval.py --mode canary`. The I45 closure UAT confirms 9 tests in `test_madeira_eval_per_skill.py` PASS unchanged.

**I57 P2 confirmation** — re-running the I45 verification matrix on 2026-05-04 returned 134/134 PASS in 21.11s; the I32 P12 substrate that I45 inherited continues to operate cleanly. This phase is closed as **superseded by I45 with no operational regression**.

## Acceptance criteria (from I32 master-roadmap)

| Criterion | Status | Evidence |
|:----------|:------:|:---------|
| Synthetic regression test trips canary 2 at -3pp drop | PASS | `test_madeira_eval_per_skill.py::test_canary2_trips_at_3pp_drop` (one of the 9 tests; PASS in the 1764-sweep) |
| Baselines committed | PASS | [`config/eval-baselines/`](../../../../config/eval-baselines/) directory with 5 baseline JSONs |
| Per-skill scorecard generator works against the canonical SKILL_REGISTRY rows | PASS | I45 P1 shim wraps the I32 substrate; harness is now I45-owned |

## Cross-references

- I32 closure UAT [`reports/uat-i32-holistik-ops-maturation-2026-04-30.md`](uat-i32-holistik-ops-maturation-2026-04-30.md) "P9 Madeira eval canaries (SUBSTRATE COMPLETE)" section (UAT phase numbering compressed; corresponds to master-roadmap P12).
- I45 master-roadmap [`docs/wip/planning/45-live-eval-harness/master-roadmap.md`](../../45-live-eval-harness/master-roadmap.md) — current owner of the harness.
- I45 P2 closeout [`docs/wip/planning/57-cycle-closeout-live-validation/reports/p2-i45-closure-2026-05-04.md`](../../57-cycle-closeout-live-validation/reports/p2-i45-closure-2026-05-04.md) — confirms substrate operates cleanly under I45 ownership.
- I57 P3 closeout: [`docs/wip/planning/57-cycle-closeout-live-validation/reports/p3-i32-closure-2026-05-04.md`](../../57-cycle-closeout-live-validation/reports/p3-i32-closure-2026-05-04.md).
