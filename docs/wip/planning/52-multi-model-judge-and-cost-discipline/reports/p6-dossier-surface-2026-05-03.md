# I52 / P6 — Dossier surface for judge axes + endpoint cost subsection

**Date:** 2026-05-03
**Phase:** P6 (Dossier surface for multi-judge axes and endpoint cost)
**Initiative:** [I52 — Multi-model LLM-judge and cost discipline](../master-roadmap.md)
**Decisions referenced:** D-IH-52-A, D-IH-52-D, D-IH-52-E
**Gates touched:** none (this phase prepares the surface for P7 CI activation)

---

## Summary

This phase wires three new dossier surfaces against the multi-judge work
(P1-P3) and the endpoint cost surface (P5):

1. **Section 03 — MADEIRA judge-axis fail summary.**
   Per-axis FAIL count + worst-axis trend + judge member roster captured
   from the latest `eval-scorecard-*.json` artefact. Renders only on the
   `--filter madeira` path.
2. **Section 04 — Worst-axis cross-reference.**
   The same axis summary surfaces in the persona calibration section as
   a cross-reference, so an operator looking at a calibration outlier can
   see at a glance whether judge axes are also flagging the same persona
   slice.
3. **Section 08 — Endpoint cost subsection.**
   New "Endpoint cost surface" subsection with per-endpoint
   `runs / hours / $/hour / projected 24h / status / operator action`
   table, fed by `gather_madeira_endpoint_cost_summary()` reading the
   most recent `endpoint-cost-probe-*.json` sidecar.

The rendering is honest in both extremes: when no judge has run live
yet (the current state per E9), Section 03 says "no judge rows yet —
multi-judge not yet active in CI"; when no endpoint probe has run yet,
Section 08 says "no endpoint cost probe yet — run `…endpoint_cost_probe.py`"
with the exact command. Operators are never confused about whether a blank
section is a bug or a real "not yet exercised" state.

---

## Deliverables

### Code

| File | Status | Purpose |
|:--|:--|:--|
| `akos/dossier/sources.py` | edited | Added `gather_madeira_judge_axis_fail_summary` and `gather_madeira_endpoint_cost_summary` (≈170 LoC). Both honor the `latest_artifact` + `_safe_relative` patterns established in I49 P12. |
| `akos/dossier/sections.py` | edited | Section 03 madeira-flavor render extension; Section 04 worst-axis cross-reference; Section 08 endpoint cost subsection with per-row operator-action one-liner. `metrics_for_trend` augmented for all three sections. |
| `tests/test_dossier_judge_axes_endpoint.py` | new | 22 tests covering source functions, render-paths, metrics-for-trend keys, default-filter no-emission, and stub-vs-real probe detection. |

### Operator-facing one-liners

The Section 08 endpoint subsection emits a per-status one-liner so the
operator's "what happens if we deploy a huge model on RunPod?" question
has a deterministic, in-place answer:

| Envelope status | Operator action emitted |
|:--|:--|
| `PASS` | `OK; per-hour $X.XXXX, projected_24h=$YY.YY.` |
| `WARN` | `Investigate <eid>: per-hour $X.XXXX within 10-20% of ceiling; projected_24h=$YY.YY.` |
| `FAIL` | `Scale endpoint <eid> down NOW; per-hour $X.XXXX breaches POL ceiling >20% (alarm hard-fail band).` |
| `SKIP` | `No envelope verdict (missing ceiling row or zero metrics).` |

This satisfies the I52 success metric "Endpoint cost subsection answers
'what happens if we deploy a huge model on RunPod?' in <1 click".

---

## Verification

```text
py -m pytest tests/test_dossier_judge_axes_endpoint.py -q
22 passed in 0.27s

py -m pytest tests/test_dossier_madeira_flavor.py tests/test_dossier_judge_axes_endpoint.py -q
43 passed in 0.25s

py -m pytest -k "dossier" -q
299 passed, 1381 deselected in 29.26s

py scripts/check-drift.py
  No drift detected. Runtime matches repo state.
```

---

## Decisions executed (already recorded; this phase only wires the surface)

- **D-IH-52-A** (initial roster) — surfaced as the captured `judge_member_ids`
  list rendered alongside the axis summary, so the dossier reader sees
  exactly which models contributed to the judging.
- **D-IH-52-D** (unit discriminator) — Section 08 uses the per-GPU-hour
  surface exclusively (`config/eval/endpoint-prices.json`,
  `aggregate_endpoint_cost`, `evaluate_endpoint_envelope`); no token data
  leaks into the endpoint subsection.
- **D-IH-52-E** (no mixed-unit aggregation) — Section 08 keeps the
  pre-existing per-token `madeira_cost_rollup` subsection (with
  `per_judge_axis` token cost breakdown) physically separate from the
  new endpoint subsection. The two subsections are emitted side-by-side
  but never aggregate into a single number.

---

## Notes for the operator

1. **First multi-judge live dossier run (P8 closure target).**
   Once the operator runs
   `AKOS_RECORD_LIVE=1 AKOS_JUDGE_ROSTER='anthropic:…,openai:…'
   py scripts/render_uat_dossier.py --filter madeira --mode live`,
   Section 03's axis summary will populate from the live judges' axis
   verdicts. Today the rendered subsection honestly says "no judge rows yet"
   because no live judge has scored an eval row to date (E9).

2. **First endpoint probe run.**
   Section 08's endpoint subsection populates from
   `artifacts/endpoint-cost/endpoint-cost-probe-*.json`. A stub-mode probe
   (`py scripts/endpoint_cost_probe.py --stub`) is sufficient to see the
   subsection render with placeholder data; a real-data probe is bound to
   the next AKOS_RECORD_LIVE-triggered RunPod / Kalavai run (OPS-52-2).

3. **Stub-vs-real disambiguation.**
   `is_stub: true` in the probe sidecar surfaces in the rendered Section 8
   as "**STUB FIXTURE** (dispatcher validation only; no real RunPod/Kalavai
   data)". This mirrors the I52 P3 calibration burn convention so neither
   subsection can be misread as production evidence.

---

## Forward-carry

- **OPS-52-2** still bound to next AKOS_RECORD_LIVE cycle (first real
  RunPod or Kalavai run). The dossier surface is now ready to consume
  whatever it produces.
- **G-52-3 (CI activation)** is the next gate (P7), wiring the
  `endpoint_envelope_alarm.py` into `eval-tier-b.yml` alongside the
  multi-judge dispatcher.
