# MADEIRA operator quickstart (nine o'clock card)

**Audience:** you need a ship-or-no-ship read in under thirty minutes without re-reading vault prose.

Canonical **what**: vault SOPs under `docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/`. Fast **how**: this guide only.

## Canonical SOP anchors (cite these in tickets)

| SOP | Covers |
|:----|:-------|
| [SOP-MADEIRA_VERDICT_AND_CADENCE_001.md](../references/hlk/v3.0/Admin/O5-1/Tech/System%20Owner/SOP-MADEIRA_VERDICT_AND_CADENCE_001.md) | Weekly verdict, dossier cadence (`env_tech_dtp_madeira_verdict`, `env_tech_dtp_madeira_dossier`) |
| [SOP-MADEIRA_INCIDENT_RESPONSE_001.md](../references/hlk/v3.0/Admin/O5-1/Tech/System%20Owner/SOP-MADEIRA_INCIDENT_RESPONSE_001.md) | Incident triage (`env_tech_dtp_madeira_incident`) |
| [SOP-MADEIRA_SCENARIO_LIFECYCLE_001.md](../references/hlk/v3.0/Admin/O5-1/Tech/System%20Owner/SOP-MADEIRA_SCENARIO_LIFECYCLE_001.md) | Lifecycle, telemetry proposals (`env_tech_dtp_madeira_lifecycle`, `env_tech_dtp_madeira_telemetry`) |
| [SOP-MADEIRA_UX_REVIEW_001.md](../references/hlk/v3.0/Admin/O5-1/Tech/System%20Owner/SOP-MADEIRA_UX_REVIEW_001.md) | Quarterly control-plane UX (`env_tech_dtp_madeira_uxreview`) |

Program index and initiative links: [`docs/wip/planning/49-madeira-management-rollup/madeira-program-index.md`](../wip/planning/49-madeira-management-rollup/madeira-program-index.md).

## One-screen command strip

Run from repo root (PowerShell-safe):

```bash
py scripts/doctor.py --docker-sandbox
py scripts/validate_persona_scenario_registry.py
py scripts/test.py madeira
```

Tier-3 or Playwright-heavy paths: optional strict Docker preflight via `AKOS_REQUIRE_DOCKER_PREFLIGHT=1` (see `docs/USER_GUIDE.md` Tier-3 UAT prerequisites).

Weekly MADEIRA dossier focus (three-light verdict in Section 1 when flavor is enabled):

```bash
py scripts/render_uat_dossier.py --filter madeira --mode live --format md
```

Deeper dossier semantics: [`madeira_dossier_workflow.md`](madeira_dossier_workflow.md).

Scenario hygiene (contributor-facing detail lives in [`madeira_contributor.md`](madeira_contributor.md)):

```bash
py scripts/quarantine_scenario.py --scenario-id SCN-... --reason "<short text>"
py scripts/promote_telemetry_to_scenario.py
```

Governance rubric thresholds and cadence table: [`docs/wip/planning/02-hlk-on-akos-madeira/MADEIRA_HARDENING_CONSOLIDATED_PLAN.md`](../wip/planning/02-hlk-on-akos-madeira/MADEIRA_HARDENING_CONSOLIDATED_PLAN.md) Part H.

Use-case rankings: [`docs/wip/planning/17-madeira-cursor-mode-parity/coverage-matrix.md`](../wip/planning/17-madeira-cursor-mode-parity/coverage-matrix.md) (`I49_review_order`, safety-first sort).
