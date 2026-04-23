# AKOS eval suites

Suites live under `suites/<suite_id>/`:

| File | Purpose |
|:-----|:--------|
| `manifest.json` | `suite_id`, `version`, `schema_version`, `last_reviewed`, optional `dimension_coverage` (D1–M2 ids). |
| `tasks.json` | Array of task objects (see schema below). |

## Task schema (rubric mode)

| Field | Required | Description |
|:------|:---------|:------------|
| `id` | yes | Stable task id. |
| `name` | yes | Short label. |
| `uc_id` | no | Madeira use-case id (e.g. `M-HLK-01`) for coverage-matrix traceability. |
| `dimension_id` | no | Taxonomy id (e.g. `T1`, `D2`). |
| `madeira_interaction_mode` | no | `ask` or `plan_draft`; forwarded to Langfuse metadata on `trace_eval_outcome`. |
| `prompt` | yes | Natural-language task stub (live runs). |
| `golden_answer` | rubric mode | Offline text scored against rubric. |
| `rubric` | rubric mode | `contains` (substrings) and `forbidden` (must not appear). |
| `max_tool_calls` | no | Trajectory bound (T3) for live runs. |
| `research_surface` | no | Categorical hint for Langfuse metadata (`hlk_registry`, `hlk_graph`, `browser`, `escalation`, `none`). |

## CLI

```bash
py scripts/run-evals.py list
py scripts/run-evals.py run --governance-rubric --dry-run
py scripts/run-evals.py run --governance-rubric --mode rubric
py scripts/run-evals.py run --suite pathc-research-spine --dry-run
py scripts/run-evals.py run --suite pathc-research-spine --mode rubric
```

Governance suite ids (`--governance-rubric`) are listed in [config/verification-profiles.json](../../config/verification-profiles.json) under `eval_rubric_governance_suites` (single source of truth with `scripts/release-gate.py` when `AKOS_EVAL_RUBRIC=1`).

## Tier A vs Tier B

| Tier | What runs | Purpose |
|:-----|:----------|:--------|
| **A (CI)** | `pytest tests/test_eval_harness.py`; `run-evals.py … --mode rubric --dry-run` optional in `release-gate` | Deterministic manifest + substring rubrics; no LLM. |
| **B (live regression)** | Gateway + tool-capable model; `run-evals.py … --mode live` when implemented | Contamination-resistant checks on real trajectories; opt-in per worker. Keep **Tier B** off default CI; document model + date per run. |

**AKOS_EVAL_RUBRIC=1:** `scripts/release-gate.py` runs rubric mode for every suite in **`eval_rubric_governance_suites`** in [config/verification-profiles.json](../../config/verification-profiles.json) (same as `py scripts/run-evals.py run --governance-rubric`).

**Manifest hygiene:** Set `schema_version` and `last_reviewed` (ISO date) when adding tasks or changing rubrics—mirrors LiveBench-style staleness awareness for **your** golden sets, not public benchmark scores.
