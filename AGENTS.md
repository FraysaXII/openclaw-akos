# AKOS — agent workspace index

Holistika knowledge + control plane in this repo. This file is the **durable**
entry point for every Cursor session — not tied to a single planning initiative.

## Load order

1. **This file** — tier model + verification golden path.
2. **Always-on rules** (≤4; enforced mechanically) — see table below.
3. **Task router** — [`akos-rule-router.mdc`](.cursor/rules/akos-rule-router.mdc) maps work class → domain rule + skill.
4. **Domain rules** — load by glob or agent-request when the task matches (see router).

Policy SSOT: [`config/cursor-rule-tiers.json`](config/cursor-rule-tiers.json) (change the core trio or cap there; run the tier validator after edits).

## Always-on rules (repo default)

| File | Purpose |
|:---|:---|
| [`akos-operator-communication.mdc`](.cursor/rules/akos-operator-communication.mdc) | Plain language for the operator; codes travel with functional names |
| [`akos-baseline-governance.mdc`](.cursor/rules/akos-baseline-governance.mdc) | Runtime inventory, HLK SSOT, canonical CSV gates, phase commits |
| [`akos-rule-router.mdc`](.cursor/rules/akos-rule-router.mdc) | Pointer-only index of domain rules (no duplicate doctrine) |

## Tier model (all initiatives)

| Tier | Mechanism | When it applies |
|:---|:---|:---|
| **Always-on** | `alwaysApply: true` on ≤4 rules | Every session |
| **Glob-scoped** | `alwaysApply: false` + `globs:` | Editing matching paths (planning, vault, UAT reports, etc.) |
| **Agent-requested** | `description:` only, no globs | Cursor pulls when task matches rule description |
| **Hooks** | [`.cursor/hooks.json`](.cursor/hooks.json) | Canonical CSV commit gate, schema drift reminder, secret scan, seat handoff on stop |

**Changing the bar:** edit [`config/cursor-rule-tiers.json`](config/cursor-rule-tiers.json), then:

```powershell
py scripts/validate_cursor_rule_tiers.py
```

## Verification golden path

```powershell
py scripts/validate_hlk.py
py scripts/verify.py pre_commit
py scripts/release-gate.py
```

## Two-seat routing (optional pattern)

When judgment-heavy work is separated from mechanical execution:

| Seat | Agent | Typical model | Role |
|:---|:---|:---|:---|
| Thinking | [`.cursor/agents/planner.md`](.cursor/agents/planner.md) | Opus-class | Charter, gates, evidence packets (`readonly`) |
| Execution | [`.cursor/agents/executor.md`](.cursor/agents/executor.md) | Composer-class | Validators, CSV tranches, scoped edits |
| Review | [`.cursor/agents/reviewer.md`](.cursor/agents/reviewer.md) | inherit | Readonly diff + validator evidence |

Full guide: [`docs/guides/cursor-two-seat-routing.md`](docs/guides/cursor-two-seat-routing.md)

Handoff markers (any initiative): `=== OPUS DONE -> SWITCH TO COMPOSER ===` / `=== THINKING DONE — operator review ===`

## Active planning work

Initiatives live under [`docs/wip/planning/`](docs/wip/planning/) — see the index in [`docs/wip/planning/README.md`](docs/wip/planning/README.md) for **current** charters, not this file.

Each initiative carries its own `master-roadmap.md`, decision log, and closure UAT under `reports/`. This workspace index does **not** list initiative numbers so new work does not require editing `AGENTS.md`.

## Where doctrine lives

| Need | Go to |
|:---|:---|
| Planning + UAT shape | [`akos-planning-traceability.mdc`](.cursor/rules/akos-planning-traceability.mdc) + [`docs/wip/planning/_templates/uat-closure-template.md`](docs/wip/planning/_templates/uat-closure-template.md) |
| Holistika ops / Supabase | [`akos-holistika-operations.mdc`](.cursor/rules/akos-holistika-operations.mdc) · mirror DML [`holistika-mirror-dml-apply.md`](docs/guides/holistika-mirror-dml-apply.md) · Data/Ops lattice [`holistika-ops-governance-lattice.md`](docs/guides/holistika-ops-governance-lattice.md) · vault SOP `SOP-HOLISTIKA_COMPLIANCE_MIRROR_DML_001` |
| Quality-bound artifacts | [`akos-quality-fabric.mdc`](.cursor/rules/akos-quality-fabric.mdc) |
| Initiative registry | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_REGISTRY.csv` |
