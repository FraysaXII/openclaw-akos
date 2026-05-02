---
language: en
status: active
initiative: 49-madeira-management-rollup
report_kind: asset-classification
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-03
---

# Initiative 49 — Asset classification

Per [`PRECEDENCE.md`](../../../references/hlk/compliance/PRECEDENCE.md).

## Canonical (planning)

| Path | Class | Validator |
|:-----|:------|:----------|
| `docs/wip/planning/49-madeira-management-rollup/master-roadmap.md` | canonical | planning traceability conventions |
| `docs/wip/planning/49-madeira-management-rollup/decision-log.md` | canonical | ditto |
| `docs/wip/planning/49-madeira-management-rollup/evidence-matrix.md` | canonical | prose |
| `docs/wip/planning/49-madeira-management-rollup/asset-classification.md` | canonical | ditto |
| `docs/wip/planning/49-madeira-management-rollup/risk-register.md` | canonical | ditto |
| `docs/wip/planning/49-madeira-management-rollup/scenario-taxonomy.md` | canonical | ditto |

## Canonical (registries)

| Path | Change | Validator |
|:-----|:-------|:-----------|
| `docs/references/hlk/compliance/process_list.csv` | P5 tranche | `validate_hlk.py` |
| `docs/references/hlk/compliance/dimensions/PERSONA_SCENARIO_REGISTRY.csv` | P2 and P10 columns / enum | `validate_persona_scenario_registry.py` |
| Vault SOP-MADEIRA_*.md (v3.0) | P6 | `validate_hlk_vault_links.py` |

## Canonical (policy and config)

| Path | Change |
|:-----|:-------|
| `config/verification-profiles.json` | P12 optional `brand_voice_lint_smoke` step |

## Mirrored / derived

| Artefact | Source |
|:---------|:-------|
| `compliance.process_list_mirror` sync | CSV after operator apply |
| `compliance.persona_scenario_registry_mirror` | Existing mirror path after PROMOTE-UPSERT tooling |

## Reference-only / repo (non-governance)

| Path | Notes |
|:-----|:------|
| `docs/guides/madeira_*.md` | Operator prose; cites SOPs |
| `static/madeira_control.html` | UI surface |
| `scripts/quarantine_scenario.py`, `scripts/promote_telemetry_to_scenario.py`, `scripts/lint_brand_voice_offline.py` | Tooling |

## Cursor rule

| Path |
|:-----|
| `.cursor/rules/akos-madeira-management.mdc` |

