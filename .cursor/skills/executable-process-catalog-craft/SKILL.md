---
name: executable-process-catalog-craft
description: Use when authoring a process catalog, automation playbook, adapter or integration registry, or any canonical that registers executable actions (human-run, agent-run, or hybrid) in this AKOS workspace. Codifies the craft for paired SOP+runbook pairing (RULE 1), adapter status metadata (RULE 2), cadence taxonomy (RULE 3), and DAMA-DMBOK 2.0 alignment posture (RULE 4). Triggers on process catalog, paired SOP+runbook, adapter registry, integration registry, cadence taxonomy, on_demand, scheduled, event_triggered, gated_operator, AC-HUMAN, AC-AUTOMATION, Normalized Adapter Pattern, status enum. Pairs with .cursor/rules/akos-executable-process-catalog.mdc (the WHEN); this skill is the HOW.
version: 1.0.0
ratifying_decisions: D-IH-86-CT; D-IH-72-N; D-IH-72-S
authored: 2026-05-24
---

# Executable-Process-Catalog Craft

> Codified at I86 Wave R close (drain7) to operationalise the I72 P8 + P9 precedents. The craft turns process catalog authoring from "ship the YAML" into "every entry has AI route AND human route AND status metadata AND cadence." Ratified by D-IH-86-CT alongside the parent rule.

## When to use this skill

Read this skill when:

- Authoring or extending a process catalog under any owning role (Marketing/Resonance/RevOps, Operations/PMO, People/People Operations, etc.).
- Adding a new entry to an existing process catalog.
- Authoring a new adapter / integration registry (CRM, billing, email, attribution, communication, scheduling, contract).
- Authoring a new SOP at `docs/references/hlk/v3.0/<area>/<role>/canonicals/SOP-*.md` that codifies an executable action.
- Authoring a new automation script under `scripts/` that operationalises a `process_list.csv` row.

This skill assumes you have already read [`akos-executable-process-catalog.mdc`](../../../.cursor/rules/akos-executable-process-catalog.mdc).

## Core principles

### Principle 1 — Every executable process is paired (SOP + runbook)

Both surfaces. Always. The SOP is the operator-facing readable contract; the runbook is the agent-facing executable contract. Neither supersedes the other. AICs (Agents in Charge) consume SOPs as instructions just like humans do — the SOP is for "anyone wearing the role_owner hat."

The pairing guarantees Holistika is never locked into "AI-only" or "human-only" execution for any governed process. This is the load-bearing property.

### Principle 2 — Bidirectional cross-references

The SOP cites the runbook path in its frontmatter (`linked_runbooks:`) + body §"Automation"; the runbook docstring/header cites the SOP path. When you mint one, mint both + wire the cross-refs in the same commit. Asymmetric authoring (SOP without runbook + later "we'll add the runbook in a follow-up") almost always produces orphans.

### Principle 3 — Per-catalog-entry: BOTH acceptance criteria

Every entry in a process catalog (e.g., `REVOPS_PROCESS_CATALOG.yaml`) MUST declare:

- `acceptance_criteria_human`: A human or AIC role_owner can run via paired SOP without invoking the runbook.
- `acceptance_criteria_automation`: The runbook fires unattended.

Both AC fields. Validator `validate_process_list_pairing.py` enforces this when it ships (I72 P9 deliverable). Until then, operator-discipline + reviewer rejection.

### Principle 4 — Adapter status metadata is mandatory

Every adapter / integration registry row carries a `status:` column with the 5-value enum:

- **active** — wired up, tested, in production use.
- **inactive** — exists but not currently wired.
- **planned** — spec-only; no implementation yet.
- **deprecated** — phased out; do not extend; replace with successor.
- **experimental** — proof-of-concept; may promote to active or roll back.

Pydantic models declare `status: Literal[...]`. Operator-facing surfaces filter / surface by status (active in primary view; planned in roadmap view; deprecated with strikethrough).

### Principle 5 — Cadence taxonomy is non-negotiable

Every executable process catalog entry declares its activation cadence as one of:

- **on_demand** — operator (or agent on operator instruction) triggers ad-hoc.
- **scheduled** — cron-like deterministic schedule.
- **event_triggered** — fires on specific system event.
- **gated_operator** — runs after explicit operator approval (each invocation requires AskQuestion ratification gate).

When a process supports multiple cadences, record the primary + use `cadence_secondary` for the alternate. Encoded in `process_list.csv` `cadence` column AND mirrored into sibling YAML catalog as `cadence_type`.

### Principle 6 — DAMA-DMBOK 2.0 alignment posture

Process catalogs + adapter registries inherit Holistika's DAMA-DMBOK 2.0 alignment posture per D-IH-72-M Strand D charter:

- **RMDM**: every catalog references canonical CSVs as SSOT (don't duplicate the data).
- **Metadata Management**: status + cadence + cross-reference + last-review metadata are mandatory.
- **Data Integration & Interoperability**: cross-area integrations use the Normalised Adapter Pattern (Truto / Unified.to / Apideck industry consensus 2026) — NOT point-to-point integrations.

Data Owner is named in the catalog frontmatter. For RevOps catalogs, Data Owner = PMO interim until CRO activation (D-IH-72-AD).

## Per-area authoring craft

### Process catalog YAML entry shape

```yaml
- item_id: <area>_<workstream>_dtp_<purpose>_<seq>
  process_name: <human-readable name>
  area: <area-tag>
  workstream: <workstream-tag>
  owner_role: <role from baseline_organisation.csv>
  cadence_type: on_demand | scheduled | event_triggered | gated_operator
  cadence_schedule: <cron-expression or "weekly" | null>
  paired_sop: docs/references/hlk/v3.0/<area>/<role>/canonicals/SOP-<purpose>_<NNN>.md
  paired_runbook: scripts/<purpose>.py | <yaml-catalog-entry-id> | <orchestrator-workflow-id>
  acceptance_criteria_human: "<one-sentence AC for SOP-only path>"
  acceptance_criteria_automation: "<one-sentence AC for runbook-only path>"
  inherited_pattern_id: <FK to PEOPLE_DESIGN_PATTERN_REGISTRY.pattern_id or null>
  status: active | inactive | planned | deprecated | experimental
  last_review: <YYYY-MM-DD>
  notes: <free-text or null>
```

### Adapter registry CSV row shape

```
adapter_id,adapter_name,vendor,area,owner_role,status,version,linked_runbook,linked_sop,supabase_mirror,last_review,notes
crm_adapter_hubspot,HubSpot CRM Adapter,HubSpot,Marketing/Reach,Marketing Director,active,1.2.0,scripts/crm_adapter_hubspot.py,SOP-MARKETING_CRM_HUBSPOT_001.md,compliance.crm_adapter_hubspot_mirror,2026-05-24,"Multi-CRM normalised adapter pattern; FK to PERSONA_REGISTRY"
```

## Pre-flight checklist

1. Both surfaces (SOP + runbook) authored in the same commit.
2. Cross-references wired (SOP frontmatter `linked_runbooks:` + runbook docstring).
3. Both AC fields populated (AC-HUMAN + AC-AUTOMATION).
4. Adapter status enum value selected from the 5-value list.
5. Cadence taxonomy value selected from the 4-value list.
6. DAMA Data Owner named in catalog frontmatter.
7. Adapter Pydantic model declares `status: Literal[...]`.
8. Mirror DDL minted in `supabase/migrations/` if mirrored to Postgres.
9. PRECEDENCE.md updated with canonical + mirror rows.
10. `inherited_pattern_id` FK populated when the entry inherits a People pattern.

## Anti-patterns

- **AP1 — SOP without runbook.** Locks Holistika into human-only execution.
- **AP2 — Runbook without SOP.** Locks Holistika into agent-only execution; operator can't debug.
- **AP3 — Cross-references absent.** Both surfaces drift independently; rediscovery cost.
- **AP4 — Missing acceptance criteria.** Cannot verify the AI-route-OR-human-route doctrine measurably.
- **AP5 — Missing status metadata on adapter rows.** Operator + agent decision-making breaks.
- **AP6 — Missing cadence.** Schedulers can't schedule; on-demand work gets cron'd; production breakage.
- **AP7 — Point-to-point integrations bypassing Normalised Adapter Pattern.** Cross-area integration spine breaks.
- **AP8 — Duplicate data in catalog instead of FK to canonical CSV.** RMDM violation; drift.

## Cross-references

- Parent rule: [`akos-executable-process-catalog.mdc`](../../../.cursor/rules/akos-executable-process-catalog.mdc).
- Sister rules: [`akos-holistika-operations.mdc`](../../../.cursor/rules/akos-holistika-operations.mdc) (canonical CSV mint pattern), [`akos-governance-remediation.mdc`](../../../.cursor/rules/akos-governance-remediation.mdc) (process_list.csv tranche approvals).
- Worked examples: I72 P8 (process catalog) + I72 P9 (multi-CRM adapter pattern).
- External research: DAMA-DMBOK 2.0 (2024 revision) + Truto/Unified.to/Apideck Normalised Adapter Pattern consensus (2026).
- Ratifying decisions: D-IH-86-CT (this skill mint), D-IH-72-N (process catalog architecture), D-IH-72-S (binary AC axis).
