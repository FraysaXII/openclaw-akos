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

# I45 P2 — Trace Record and Replay (cassettes)

**Phase:** P2 (record-and-replay cassettes; AgentEval pattern)
**Closes:** I45 P2 entry criteria; resolves evidence-matrix E9 (replay-based eval not adopted at AKOS).
**Date:** 2026-05-01

## Actions

1. New module `akos/eval_harness/cassette.py` (~265 lines) implementing the cassette format:
   - `CassetteHeader` dataclass (schema v1.0): skill_id, probe_id, probe_kind, recorded_at, recorded_by, model_id, model_tier, golden_assertion, last_recorded
   - JSONL format: header line, N event lines (prompt/tool_call/tool_response/final), summary line
   - 2 probe kinds: `classify_request` (deterministic, no LLM, safe to record without env guard) and `live_llm` (real LLM trajectory; requires `AKOS_RECORD_LIVE=1`)
   - Staleness policy: fresh < 60d, warn 60-89d, fail >= 90d (mirrors LiveBench-style awareness from `tests/evals/README.md`)
   - 4 public functions: `record_classify_request_cassette`, `record_live_llm_cassette`, `replay_classify_request_cassette`, `replay_live_llm_cassette`, plus `replay_cassette` dispatcher

2. Wired `akos.eval_harness.v2.run_replay()` to use the cassette module. `--mode replay` now executes real cassette replays (not the P1 stub).

3. Extended `scripts/eval.py record` subcommand with full args:
   - `--skill <id>`, `--probe <id>`, `--prompt <text>` (required)
   - `--kind {classify_request|live_llm}` (default classify_request)
   - `--by`, `--model-id`, `--model-tier` (provenance)
   - `--contains`, `--forbidden` (live_llm rubric)
   - `live_llm` kind enforces `AKOS_RECORD_LIVE=1` guard

4. Seeded **6 cassettes** (one per current SKILL_REGISTRY row, plus a 2nd Madeira lookup):
   - `tests/evals/cassettes/SKILL-MADEIRA-LOOKUP-V1/lookup_role.jsonl`
   - `tests/evals/cassettes/SKILL-MADEIRA-LOOKUP-V1/hlk_search.jsonl`
   - `tests/evals/cassettes/SKILL-ARCHITECT-PLAN-V1/plan_migration.jsonl`
   - `tests/evals/cassettes/SKILL-EXECUTOR-RUN-V1/run_pytest.jsonl`
   - `tests/evals/cassettes/SKILL-VERIFIER-CHECK-V1/verify_governance.jsonl`
   - `tests/evals/cassettes/SKILL-SHARED-LOCALE-DETECT-V1/detect_french.jsonl`

5. Added `tests/evals/cassettes/.gitattributes` documenting cassette discipline (synthetic data only, no real PII; per R-45-4).

6. New test suite `tests/test_eval_cassette.py` (16 tests):
   - Format round-trip (3 tests): write -> read symmetry, malformed-file detection
   - Deterministic record + replay (3 tests): record creates cassette; replay passes; tampered golden_assertion fails
   - Staleness (3 tests): fresh / warn at 60d / fail at 90d
   - Live LLM guard (2 tests): blocked without env var; allowed with
   - List + adversarial isolation (1 test): `list_cassettes` excludes `adversarial/`
   - Seeded cassettes (3 tests): all 5 skills present; all replay PASS; v2 dispatcher row count matches

## Verification

- `py scripts/eval.py --mode replay` runs all 6 cassettes; all PASS, fresh, ~1.6s.
- `py scripts/eval.py record --skill X --probe Y --prompt "..."` writes a deterministic cassette without any env var (classify_request kind).
- `py scripts/eval.py record --kind live_llm --skill X --probe Y --prompt "..."` correctly returns exit 2 ("AKOS_RECORD_LIVE=1 required") without the env var.
- `tests/test_eval_cassette.py`: **16/16 PASS** in 1.7s.
- Combined eval-related test count: 5 + 9 + 22 + 16 = **52 tests, 52/52 PASS**.

## What this gives us

- **Cost-controlled regression detection on the routing layer**: every commit's `--mode replay` runs all 6 cassettes against the in-process `classify_request` and asserts route stability. Zero LLM cost.
- **A pattern that scales to real LLM trajectories**: when P6 lands the live LLM recorder, the cassette format already supports `live_llm` cassettes with rubric-based replay (no LLM call at replay time, per the AgentEval pattern).
- **A staleness policy that catches drift**: any cassette older than 90 days fails; warns at 60. Operator can override via `--allow-stale` flag (TODO: wire to `--mode replay`; deferred to P6).

## What this does NOT do (deferred)

- No actual LLM trajectories yet — the 6 seeds are deterministic classify_request cassettes. The `live_llm` kind is a stub that lands in P6 when Tier B recording is wired.
- No adversarial cassettes yet — those are P5 territory (`tests/evals/cassettes/adversarial/<skill_id>/`).
- No PII linter — `scripts/validate_cassette_no_pii.py` is a P5 deliverable.
- No `--allow-stale` CLI flag for `--mode replay` — deferred to P6 when staleness becomes a real concern.

## Risks resolved or deferred

- **R-45-1 (cassettes go stale silently)**: mitigated. `last_recorded` field is populated; staleness_status() function works; replay surfaces age in row notes. P6 will wire the WARN/FAIL gating into the dispatcher (`--allow-stale` flag).
- **R-45-4 (PII leak)**: documented via `.gitattributes` marker. Linter is P5 deliverable.

## Next phase

P3 — Close the Registry-Router gap. Refactor `akos/intent.py` to consult `SKILL_REGISTRY.csv` first (via axes_consumed + tools_required + agents_supported); add `routing_condition` column; reconcile drift between `SKILL_REGISTRY.tools_required` (Cursor names) and `agent-capabilities.json` (gateway ids). Cassettes recorded today will catch any routing regression introduced by P3.
