---
language: en
status: active
intellectual_kind: phase_evidence
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

# I45 P0 — Audit of the current eval surface

**Audit id:** AUDIT-EVAL-SURFACE-2026-05-01
**Closes:** I45 P0 entry criteria; feeds evidence-matrix rows E1-E13.
**Method:** Read-only walk of `akos/eval_harness.py`, `scripts/run-evals.py`, `scripts/eval_per_skill.py`, `tests/evals/`, `config/eval/`, `config/eval-baselines/`, `config/verification-profiles.json`, plus grep for cross-references.

## TL;DR

We have **three distinct eval surfaces** that together do less than what one well-named, unified surface could do.

| Surface | Built in | Schema | CLI | Result format | Consumers |
|:--------|:---------|:-------|:----|:--------------|:----------|
| `akos/eval_harness.py` + `scripts/run-evals.py` | I10 (closed 2026-04-15) | manifest.json + tasks.json (`tests/evals/suites/<id>/`) | `py scripts/run-evals.py {list,run}` | stdout text + optional Langfuse score | `scripts/release-gate.py` (when `AKOS_EVAL_RUBRIC=1`); `tests/test_eval_harness.py` |
| `scripts/eval_per_skill.py` | I32 P9 (2026-04-30) | per-skill JSON in `config/eval-baselines/skill_*.json` | `py scripts/eval_per_skill.py [--json]` | stdout text or stdout JSON | `tests/test_madeira_eval_per_skill.py` |
| `madeira_uat_inproc.py` (lives in `%TEMP%`) | I32 D-IH-32-Q9 (2026-05-01) | hard-coded probe list | `py %TEMP%/madeira_uat_inproc.py` | stdout text | none (one-off; lost to TEMP cleanup) |

**Total:** 3 entry points, 3 schemas, 3 result formats, near-zero shared code.

## Surface 1 — `akos/eval_harness.py` + `scripts/run-evals.py`

### What it does
- Loads suite manifests under `tests/evals/suites/<id>/{manifest,tasks}.json`. Two suites today: `pathc-research-spine` and `madeira-operator-coverage`.
- Provides `score_rubric_task(task, answer)` — substring-based scoring (`contains` and `forbidden` lists in the task's `rubric` block).
- `scripts/run-evals.py` exposes `list`, `run --suite <id>`, `run --governance-rubric` subcommands.
- Optional Langfuse v4 scoring via `akos.telemetry.LangfuseReporter`.

### Strengths
- Well-defined manifest schema (`suite_id`, `version`, `schema_version`, `last_reviewed`, `dimension_coverage`).
- Tier A vs Tier B split documented in `tests/evals/README.md` (Tier A = no LLM, Tier B = live regression opt-in).
- `eval_rubric_governance_suites` in `config/verification-profiles.json` ties to `release-gate.py` for production gating.

### Weaknesses
- No replay; every run that wants real LLM behavior must call live LLMs.
- No per-skill traceability — suites are coverage-shaped, not skill-shaped.
- Tier B is effectively dormant ("opt-in per worker") — no scheduled runs, no model-tier matrix.
- No cost observability (no per-task `tokens_in/out`, `usd_estimate`).
- `scripts/run-evals.py` has dead code paths (`_load_legacy_tasks`, `LEGACY_TASKS = EVALS_DIR / "tasks.json"`) — pre-suite migration debris.

### Evidence pointers
- `akos/eval_harness.py` lines 1-42 (entire module — minimal surface)
- `scripts/run-evals.py` lines 1-31 (header + imports)
- `tests/evals/README.md` Tier A/B section
- `tests/evals/suites/pathc-research-spine/manifest.json` (4 fields + dimension_coverage)
- `tests/evals/suites/madeira-operator-coverage/` (parallel structure)

## Surface 2 — `scripts/eval_per_skill.py`

### What it does
- Loads `SKILL_REGISTRY.csv` rows + per-skill baseline JSON (`config/eval-baselines/skill_*.json`).
- For each skill, computes `delta_pp = current_pct - baseline_pct`.
- Trips canary 2 (`eval regression > 2pp`) when `delta < -threshold`.
- Emits human-readable scorecard or JSON.
- Synthetic regression test (`tests/test_madeira_eval_per_skill.py`) injects a 3pp drop and asserts canary 2 trips.

### Strengths
- Skill-shaped (matches `SKILL_REGISTRY.csv` row structure).
- JSON output mode for machine consumption.
- Has a `--current` override flag for testing.
- Per-skill baseline JSONs carry `langfuse_trace_pattern` + `lifecycle_status` + ownership.

### Weaknesses
- No actual live runtime — `current` defaults to baseline (placeholder echo); only injected via `--current` overrides for tests.
- Canary 2 is the only exercised canary (1, 3, 4, 5 are documented in the I32 P9 plan but unbuilt as runners).
- No record/replay — purely metric comparison.
- Result format diverges from `scripts/run-evals.py` (no manifest concept; no rubric scoring).

### Evidence pointers
- `scripts/eval_per_skill.py` (entire 165-line file)
- `config/eval-baselines/skill_*.json` (5 baseline JSONs, one per current skill)
- `tests/test_madeira_eval_per_skill.py` (9 tests; canary-2 synthetic regression on lines TBD)

## Surface 3 — `madeira_uat_inproc.py` (lost to `%TEMP%`)

### What it does
- 8 in-process probes for the post-I32-SKILL_REGISTRY landing UAT (D-IH-32-Q9):
  1. env bootstrap
  2-5. SKILL/CELL/POLICY/REPO_HEALTH CSV loads with field count assertions
  6. `classify_request` smoke
  7. 5 intent probes (orchestrator-fallback count = 0/5)
  8. `validate_hlk` dispatcher full vault
- Reported 8/8 green; D-IH-32-Q9 PASS.

### Strengths
- Concrete, fast, no LLM needed (in-process).
- 5 intent probes are the closest thing we have to canary 5 ("UAT smoke detects orchestrator fallback") in code.

### Weaknesses
- **Lives in `%TEMP%`. Gone on next cleanup.** Pattern not captured.
- No JSON output.
- Hard-coded probes; not extensible.
- Not registered in any verification profile.

### Evidence pointers
- `docs/wip/planning/32-holistik-ops-maturation/reports/madeira-runtime-uat-2026-05-01.md` (the report; the script itself is in TEMP)

## Cross-cutting findings

### Drift between `SKILL_REGISTRY.tools_required` and `agent-capabilities.json`

`SKILL_REGISTRY.csv` row for `SKILL-EXECUTOR-RUN-V1` declares `tools_required=Shell;Read;Write` (Cursor-style names).
`config/agent-capabilities.json` `executor` role declares `shell_exec`, `write_file`, `read_file` (gateway ids).

**Two parallel naming systems for the same concept.** I32 P2 report flagged this; I45 P3 will reconcile via a per-skill waiver column.

### `intent.py` does not consult `SKILL_REGISTRY.csv`

`grep -n SKILL_REGISTRY akos/intent.py` returns zero hits. The router knows nothing about the registry.

`config/intent-exemplars.json` is the current routing data source (parallel to but disconnected from `SKILL_REGISTRY.csv`'s `axes_consumed`, `tools_required`, `agents_supported`).

I45 P3 closes this gap: `intent.py` consults `SKILL_REGISTRY.csv` first; falls back to exemplars.

### `config/eval/alerts.json` has un-exercised alerts

```
madeira_internal_tool_leak       — fires when MADEIRA mentions internal tool ids (akos_*, mcp_*)
madeira_pseudo_hlk_path_leak     — fires on fabricated HLK paths
madeira_suspect_uuid_hallucination — fires on uuid-shaped hallucinations
```

No probes test these. They fire on production traces (Langfuse-side), but if they regress in a code change, we find out at customer-report time.

I45 P5 builds adversarial cassettes to exercise each.

### `config/eval/baselines.json` is SOP-shaped, not skill-shaped

Per the read of `config/eval/baselines.json`:
- `completion_rate` / `containment_rate` / `pr_throughput_increase` / `prompt_injection_vuln_rate`
- Each has `target`, `comparator`, `window`, `sop_reference`.
- Surfaced via `GET /metrics` endpoint.

This file is **operational SOP-baseline tracking**, distinct from `config/eval-baselines/` (per-skill accuracy baselines). They share the word "baseline" but are different concepts. Worth a future doctrine note (out of I45 scope; document for I47).

### Verification profiles surface

`config/verification-profiles.json` has 11 profiles. Eval-relevant ones:
- `pre_commit` — bundles drift + full pytest + `browser-smoke.py --playwright` + `test_madeira_interaction` + `release-gate.py`. Heavy.
- `eval_rubric_governance_suites` — list of 2 suite ids; consumed by `run-evals.py --governance-rubric` and `release-gate.py` when `AKOS_EVAL_RUBRIC=1`.
- `wip_dashboard_render_smoke` — added in I32 P10.

No profile gates the per-skill canary scorecard or any replay/cassette path. I45 P1 + P6 add them.

## Recommended P1 unification surface

```
py scripts/eval.py [--mode {rubric,replay,canary,smoke}] [--suite <id>] [--skill <id>] [--json]
py scripts/eval.py record --skill <id> [--mode {default,adversarial}]
py scripts/eval.py replay --skill <id> [--cassette <path>]
py scripts/eval.py promote --skill <id> [--override --reason <text>]
py scripts/eval.py scorecard [--cost] [--enforce]
```

Backward-compat shims:
- `scripts/run-evals.py` → calls `scripts/eval.py --mode rubric` after deprecation warning.
- `scripts/eval_per_skill.py` → calls `scripts/eval.py --mode canary` after deprecation warning.
- `madeira_uat_inproc.py` pattern promoted as `scripts/eval.py --mode smoke`.

Each mode reads from / writes to a unified scorecard schema (JSON + markdown). Operator can mix modes (`--mode rubric,canary,smoke`).

## Risks not yet on register

- **R-AUDIT-01** — `tests/evals/tasks.json` (legacy file at root of `tests/evals/`, not under `suites/`) is loaded by `_load_legacy_tasks()` in `scripts/run-evals.py` but no current command uses it. Either migrate to a suite or delete in P1. **(Add to risk register R-45-13.)**
- **R-AUDIT-02** — `config/eval/baselines.json` and `config/eval-baselines/` share a confusing name. P1 should rename one for clarity. Suggested: `config/eval/sop-targets.json` for the I10 file. **(Defer to I47; non-blocking.)**

## Closure assertion

I45 P0 audit complete. Evidence-matrix rows E1-E13 are sourced from this file. No code changes; this is observation-only.
