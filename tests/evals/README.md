# AKOS eval suites

Suites live under `suites/<suite_id>/`:

| File | Purpose |
|:-----|:--------|
| `manifest.json` | `suite_id`, `version`, optional `dimension_coverage` (D1–M2 ids). |
| `tasks.json` | Array of task objects (see schema below). |

## Task schema (rubric mode)

| Field | Required | Description |
|:------|:---------|:------------|
| `id` | yes | Stable task id. |
| `name` | yes | Short label. |
| `dimension_id` | no | Taxonomy id (e.g. `T1`, `D2`). |
| `prompt` | yes | Natural-language task stub (live runs). |
| `golden_answer` | rubric mode | Offline text scored against rubric. |
| `rubric` | rubric mode | `contains` (substrings) and `forbidden` (must not appear). |
| `max_tool_calls` | no | Trajectory bound (T3) for live runs. |
| `research_surface` | no | Categorical hint for Langfuse metadata (`hlk_registry`, `hlk_graph`, `browser`, `escalation`). |

## CLI

```bash
py scripts/run-evals.py list
py scripts/run-evals.py run --suite pathc-research-spine --dry-run
py scripts/run-evals.py run --suite pathc-research-spine --mode rubric
```

**Tier A (CI):** pytest `tests/test_eval_harness.py` + `run-evals.py run … --mode rubric --dry-run` via `release-gate` optional slice.

**Tier B:** Playwright / gateway-backed live runs when a worker has Ollama + gateway (see CONTRIBUTING).
