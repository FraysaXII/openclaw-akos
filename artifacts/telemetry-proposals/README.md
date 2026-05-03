# `artifacts/telemetry-proposals/`

Operator-local artifact directory for **`scripts/promote_telemetry_to_scenario.py`** output.

## What lives here

JSON files named `telemetry-proposals-<UTC>.json`, each emitted by a single run of the promotion script over the operator's `~/.openclaw/telemetry/madeira-answer-quality-*.jsonl` files. Each file contains a list of cluster-keyed proposals with suggested `PERSONA_SCENARIO_REGISTRY` row fields (persona_id, skill_id, scenario_class, difficulty_class, expected_route, expected_outcome_class, lifecycle_status=scaffold, sample, rationale, match_count).

## Why these are gitignored

- Operator-local: telemetry feed is per-machine.
- Transient: regenerated on every run; no value in versioning.
- Privacy: telemetry samples can carry user prompts that may include incidental PII fragments not covered by the operator's redaction pipeline.

## Operator workflow (Initiative 49 P11 + Initiative 50 P5)

1. **Emit proposals** — `py scripts/promote_telemetry_to_scenario.py --since-days 30`
2. **Triage** — review the JSON; pick 1–3 highest-leverage clusters.
3. **Merge** — append rows to `docs/references/hlk/compliance/dimensions/PERSONA_SCENARIO_REGISTRY.csv` with `lifecycle_status=scaffold` and `notes` citing the proposal_id + telemetry source.
4. **Validate** — `py scripts/validate_persona_scenario_registry.py` and `py scripts/validate_hlk.py` must pass.
5. **Decision-log** — per-row entry in the active initiative's decision-log per the `G-50-2`-style operator-merge gate.

**Auto-merge is forbidden.** The promotion script never writes to the canonical CSV; it only emits proposals.

## Cross-references

- [`SOP-MADEIRA_SCENARIO_LIFECYCLE_001.md`](../../docs/references/hlk/v3.0/Admin/O5-1/Tech/System%20Owner/SOP-MADEIRA_SCENARIO_LIFECYCLE_001.md) §5.4 (operator-merge policy).
- [`PERSONA_SCENARIO_REGISTRY.csv`](../../docs/references/hlk/compliance/dimensions/PERSONA_SCENARIO_REGISTRY.csv) (canonical destination).
- [`scripts/promote_telemetry_to_scenario.py`](../../scripts/promote_telemetry_to_scenario.py) (emitter).
