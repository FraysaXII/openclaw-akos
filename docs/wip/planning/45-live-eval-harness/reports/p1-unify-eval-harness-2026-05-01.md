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

# I45 P1 — Unified eval harness landing

**Phase:** P1 (unify into `akos/eval_harness/v2`)
**Closes:** I45 P1 entry criteria; resolves evidence-matrix E1 (3 drifting eval surfaces).
**Date:** 2026-05-01

## Actions

1. Converted `akos/eval_harness.py` (single file, 42 lines from I10) into the package `akos/eval_harness/__init__.py`. **Public API preserved exactly** — `load_suite`, `score_rubric_task`, `list_suite_ids`, plus module-level `EVALS_DIR` / `SUITES_DIR` constants. All existing imports keep working.
2. New module `akos/eval_harness/v2.py` with:
   - `Scorecard` and `ScoreRow` dataclasses (unified result schema across all modes)
   - 4 mode runners: `run_smoke`, `run_canary`, `run_rubric`, `run_replay` (replay is P2 stub)
   - `run_modes()` top-level dispatcher; `--mode all` collapses to `smoke + canary + rubric` (replay opt-in)
3. New CLI `scripts/eval.py` with subcommands `list`, `record` (P2 stub), `promote` (P7 stub) and `--mode {rubric,canary,replay,smoke,all}` modes. JSON + markdown output. Standard `--exit-on-fail` semantics.
4. Added deprecation notices to:
   - `scripts/eval_per_skill.py` (header + stderr at runtime; silenced via `AKOS_EVAL_NO_DEPRECATION_WARN=1`)
   - `scripts/run-evals.py` (same)
   - Both shims continue to work for one release cycle (per asset-classification policy).
5. Promoted the `madeira_uat_inproc.py` pattern (D-IH-32-Q9) from `%TEMP%` into `--mode smoke`. The 7 in-process probes now live as canonical code in `akos/eval_harness/v2.py:run_smoke()`.
6. New test suite `tests/test_eval_harness_v2.py` with 22 tests covering:
   - Backward compatibility (4 tests)
   - v2 module surface (8 tests, including synthetic regression injection for canary 2)
   - CLI surface (5 tests, including JSON parse + exit code semantics)
   - Shim back-compat at CLI level (2 tests)
   - Drift detectors (3 tests — package-vs-file check + v2-module-exists check + VALID_MODES contract)

## Verification

- `py scripts/eval.py list` shows 2 suites + 5 skills + 0 cassettes (cassettes land in P2). Exit 0.
- `py scripts/eval.py --mode all` runs 14 rows (7 smoke + 5 canary + 2 rubric), all PASS, overall PASS, ~3.7s.
- `py scripts/eval.py --mode all --json` emits valid JSON with `schema_version=1.0`, `overall_status=pass`, `modes_run=[smoke,canary,rubric]`.
- `py scripts/eval.py --mode canary --current SKILL-MADEIRA-LOOKUP-V1=80.0` correctly returns exit 1, JSON `overall_status=fail`, `canary_2_tripped=true` for the Madeira row. Synthetic regression detection works.
- `py scripts/eval.py record --skill SKILL-MADEIRA-LOOKUP-V1` correctly returns exit 2 ("AKOS_RECORD_LIVE=1 required") — the P2 guard works.
- Shims: `py scripts/eval_per_skill.py --json` exit 0, output unchanged from I32 P9 baseline (operator-pasteable JSON). `py scripts/run-evals.py list` exit 0, output unchanged from I10 baseline.
- Pytest: `tests/test_eval_harness.py` (5 tests, I10) + `tests/test_madeira_eval_per_skill.py` (9 tests, I32 P9) + `tests/test_eval_harness_v2.py` (22 tests, NEW) = **36 tests, 36/36 PASS**, 4.0s.

## Surface contract (for downstream phases)

The v2 surface is the canonical entry point for all subsequent I45 phases:

- **P2 (cassettes)** will fill in `run_replay()` and the `record` CLI subcommand. Cassette format: JSONL under `tests/evals/cassettes/<skill_id>/*.jsonl`. Recording requires `AKOS_RECORD_LIVE=1`.
- **P3 (router-registry gap)** will add a 5th smoke probe: "intent.py consults SKILL_REGISTRY before exemplars".
- **P4 (cost+latency)** will populate `ScoreRow.cost_usd`, `latency_ms_p50`, `latency_ms_p95` from a Langfuse scrape.
- **P5 (adversarial)** will add `tests/evals/cassettes/adversarial/<skill_id>/*.jsonl`; cassette runner reuses `run_replay()`.
- **P6 (Tier B weekly)** will add a `--tier {A,B}` flag and the GitHub Action that wraps `--mode all --tier B`.
- **P7 (promotion gate)** will fill in the `promote` CLI subcommand with the 4-criteria check.

## Artifacts changed/added

**Added:**
- `akos/eval_harness/__init__.py` (62 lines; converted from old `eval_harness.py`)
- `akos/eval_harness/v2.py` (~310 lines)
- `scripts/eval.py` (~205 lines)
- `tests/test_eval_harness_v2.py` (22 tests)

**Removed:**
- `akos/eval_harness.py` (old single file; replaced by package)

**Modified:**
- `scripts/eval_per_skill.py` (deprecation notice + comment header; behavior unchanged)
- `scripts/run-evals.py` (same)

## Risks not yet realized

- R-45-2 (test count drops as duplicates collapse): Did NOT realize — we ADDED 22 tests on top of the existing 14, net +22. The merge will happen naturally as cassettes (P2) replace per-test live calls.
- R-45-12 (shims hide migration): mitigation in place via deprecation warnings; will track shim usage in P8 closure.

## Next phase

P2 — Trace Record and Replay. Will populate `tests/evals/cassettes/<skill_id>/` with seed cassettes (one per existing skill, deterministic JSONL shape), wire `record` and `replay` subcommands to real I/O, and add the `last_recorded` staleness alarm.
