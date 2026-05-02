# MADEIRA Langfuse saved-view walkthrough

**Audience:** operators monitoring MADEIRA conversational quality between weekly verdict cycles. Use alongside [`madeira_dossier_workflow.md`](madeira_dossier_workflow.md) for the rollup verdict, and [`madeira_operator_quickstart.md`](madeira_operator_quickstart.md) for the daily command strip.

Canonical cadence anchor: [SOP-MADEIRA_VERDICT_AND_CADENCE_001.md](../references/hlk/v3.0/Admin/O5-1/Tech/System%20Owner/SOP-MADEIRA_VERDICT_AND_CADENCE_001.md) §6.

## Local-first observability (no Langfuse keys required)

`scripts/log-watcher.py` mirrors every Madeira interaction's answer-quality envelope to `~/.openclaw/telemetry/madeira-answer-quality-<date>.jsonl`. The mirror is the source of truth for offline review and for `scripts/promote_telemetry_to_scenario.py` clustering. When Langfuse keys are absent the dashboard below is unavailable; the telemetry mirror remains complete.

To inspect locally without Langfuse:

```bash
py scripts/log-watcher.py --once
ls ~/.openclaw/telemetry/madeira-answer-quality-*.jsonl
```

## Saved-view JSON snippet (Langfuse Tracing)

Paste this snippet into Langfuse via *Tracing → Saved views → New saved view*. It cuts the same dimensions the MADEIRA dossier Section 8 surfaces (per-mode × per-persona × per-judge-axis × per-day) using only fields emitted by `akos/telemetry.py` and `scripts/log-watcher.py`:

```json
{
  "name": "MADEIRA — answer quality (cuts)",
  "description": "Initiative 49 P13 saved view: per-mode × per-persona × per-judge-axis × per-day for the MADEIRA agent.",
  "filters": {
    "type": "AND",
    "conditions": [
      { "field": "name", "operator": "equals", "value": "answer_quality" },
      { "field": "metadata.agent_role", "operator": "equals", "value": "madeira" }
    ]
  },
  "groupBy": [
    "metadata.madeira_interaction_mode",
    "metadata.persona_id",
    "metadata.judge_axis",
    "trace.start_time:day"
  ],
  "metrics": [
    "trace.count",
    "metadata.quality_score:avg",
    "metadata.cost_usd:sum"
  ],
  "sort": [{ "field": "trace.start_time", "direction": "desc" }]
}
```

Field provenance:

- `name=answer_quality` is set by [`akos/telemetry.py`](../../akos/telemetry.py) when emitting the per-interaction trace.
- `metadata.madeira_interaction_mode` is populated by `scripts/log-watcher.py` from the session jsonl line.
- `metadata.persona_id` is set by the per-persona scorecard pipeline (Initiative 47 P10) and propagates to traces tagged via Langfuse SDK calls in `akos/api.py`.
- `metadata.judge_axis` is set by the LLM-judge axes (Initiative 47 P12) when run.
- `metadata.cost_usd` is summed by `akos/eval_harness/cost_obs.py`.

## UI walkthrough

1. **Open Tracing.** In Langfuse, switch the project to the one whose `LANGFUSE_PUBLIC_KEY` matches `~/.openclaw/.env`.
2. **Filter.** Apply the saved view above. If the chart stays empty:
   - confirm `LANGFUSE_PUBLIC_KEY` / `LANGFUSE_SECRET_KEY` / `LANGFUSE_HOST` in `~/.openclaw/.env`;
   - run `py scripts/test-langfuse-trace.py` to verify connectivity (returns within seconds when configured).
3. **Read residual flags.** Drill into any trace with `quality_score < 1.0` to see the residual flag list emitted by the log watcher (for example `missing_citation_asset`, `internal_tool_leak`, `compaction_interference`).
4. **Promote insights.** Run `py scripts/promote_telemetry_to_scenario.py --since-days 7` to materialise JSON proposals; review and apply manually per [SOP-MADEIRA_SCENARIO_LIFECYCLE_001.md](../references/hlk/v3.0/Admin/O5-1/Tech/System%20Owner/SOP-MADEIRA_SCENARIO_LIFECYCLE_001.md) §5.4.
5. **Reconcile with dossier.** When MADEIRA flavour is enabled (`py scripts/render_uat_dossier.py --filter madeira`), Section 8's MADEIRA cost rollup mirrors the same per-mode / per-persona / per-judge-axis cuts; treat any divergence between Langfuse and dossier as a telemetry pipeline bug rather than a model regression.

## When the dashboard cannot be hosted in Langfuse

Some operators run AKOS without Langfuse keys for compliance reasons. In that case:

- The MADEIRA dossier Section 8 cost rollup remains computable from `artifacts/eval-history/eval-scorecard-*.json` produced by `scripts/eval.py --json`.
- The local jsonl mirror (`~/.openclaw/telemetry/`) remains the input for `scripts/promote_telemetry_to_scenario.py`.
- A static text snapshot of the latest cuts can be generated as evidence with:

  ```bash
  py scripts/eval.py --mode all --json | tee artifacts/eval-history/eval-scorecard-$(date -u +%Y%m%dT%H%M%SZ).json
  py scripts/render_uat_dossier.py --filter madeira --mode snapshot --format md
  ```

The dossier emit becomes the canonical operator narrative when the Langfuse panel is unavailable. The cadence SOP cites both pathways.
