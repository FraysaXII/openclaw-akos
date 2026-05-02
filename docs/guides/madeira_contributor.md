# MADEIRA contributor guide

**Audience:** engineers changing prompts, persona registry rows, eval cassettes, or dossier renderers touching the MADEIRA lane.

Canonical lifecycle **what**: [SOP-MADEIRA_SCENARIO_LIFECYCLE_001.md](../references/hlk/v3.0/Admin/O5-1/Tech/System%20Owner/SOP-MADEIRA_SCENARIO_LIFECYCLE_001.md). This guide is **how** to stay inside that contract without copying SOP prose.

## Before you edit

1. Pick the persona and skill row in `docs/references/hlk/compliance/dimensions/PERSONA_SCENARIO_REGISTRY.csv`; note `scenario_id`, `lifecycle_status`, `priority_score`, `safety_lane`, `release_blocking`.
2. Map your change to a use-case id in [`docs/wip/planning/17-madeira-cursor-mode-parity/coverage-matrix.md`](../wip/planning/17-madeira-cursor-mode-parity/coverage-matrix.md) when the work is UAT-visible.
3. Run the narrow pytest group for fast feedback:

   ```bash
   py scripts/test.py madeira
   ```

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for `@pytest.mark.madeira` and other groups.

## Adding or adjusting a scenario row

1. Prefer **proposal-first** telemetry flow: [`scripts/promote_telemetry_to_scenario.py`](../../scripts/promote_telemetry_to_scenario.py) emits JSON for operator review — do not silently merge proposals into canonical CSV without review.
2. After CSV edits:

   ```bash
   py scripts/validate_persona_scenario_registry.py
   ```

3. For promotion/scaffold/active transitions, mirror the numbered gates in [SOP-MADEIRA_SCENARIO_LIFECYCLE_001.md](../references/hlk/v3.0/Admin/O5-1/Tech/System%20Owner/SOP-MADEIRA_SCENARIO_LIFECYCLE_001.md) section 5.

## Anti-flake: quarantine

When a scenario fails repeatedly without a fix landing, operators may quarantine instead of deleting stable ids:

```bash
py scripts/quarantine_scenario.py --scenario-id SCN-... --reason "<text>"
```

Quarantined rows stay in CSV for history; dossier renders call them out in the scenario-health slice when MADEIRA flavor is on.

## Cassettes and live capture

Tier-1 replay and cassette policy follow Initiative 47 conventions in `tests/evals/README.md`. If policy requires live capture for a tier, coordinate with operators before overwriting golden artefacts.

## When to escalate

- Registry **schema** or new `lifecycle_status` enum values → decision log gate in Initiative 49 folder, plus `scripts/validate_hlk.py`.
- **`process_list.csv`** edits → explicit operator alignment per `.cursor/rules/akos-governance-remediation.mdc`.
