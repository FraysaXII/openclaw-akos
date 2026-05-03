# Endpoint cost probe outputs

This directory holds outputs of `scripts/endpoint_cost_probe.py` and (by
convention) the operator-curated JSONL run logs that feed it.

## What lives here

- `endpoint-cost-probe-<UTC-timestamp>.md` — human-readable per-endpoint
  cost report (markdown).
- `endpoint-cost-probe-<UTC-timestamp>.json` — machine-readable sidecar
  with the same data; consumed by `scripts/endpoint_envelope_alarm.py`
  for the G-52-4 hard-fail gate.
- (operator) `*.jsonl` — observed RunPod / Kalavai run logs. One JSON
  object per line with at least `endpoint_id` and `duration_hours` keys.

## Gitignore posture

`*.json` and `*.md` outputs are gitignored (regenerable). This README is
the only tracked file.

## Operator workflow

Stub-mode validation (no real data; dispatcher smoke):

```
py scripts/endpoint_cost_probe.py --stub
py scripts/endpoint_envelope_alarm.py --stub
```

Real-data run (after the operator collects observed RunPod / Kalavai run
logs into a JSONL file):

```
py scripts/endpoint_cost_probe.py --runs-jsonl artifacts/endpoint-cost/observed-runs-2026-05-XX.jsonl
py scripts/endpoint_envelope_alarm.py --probe-json artifacts/endpoint-cost/endpoint-cost-probe-<ts>.json
```

The alarm exits code 2 on any hard-fail-band breach (per
`POL-EVAL-COST-CEILING-ENDPOINT-{RUNPOD,KALAVAI}-V1`); operator
investigates, scales down the endpoint manually, and only then reruns.

## Pricing source contract

Per D-IH-52-E, this directory consumes data from
`config/eval/endpoint-prices.json` exclusively. It does NOT read
`config/eval/model-prices.json`. Mixing units in a single computation is
a governance violation; the two files are physically separate to make
that violation impossible.
