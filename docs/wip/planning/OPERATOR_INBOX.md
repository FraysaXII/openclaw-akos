---
language: en
status: continuous
continuous_rationale: Auto-rendered Operator Action Inbox (I59 P4) — re-renders from OPS_REGISTER.csv on every status flip; never hand-edit between markers.
---

# Operator Action Inbox

> **SSOT** is `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/OPS_REGISTER.csv`. This file is
> auto-rendered by `scripts/render_operator_inbox.py` on every change to that
> CSV. Filter: `status='open'` AND `owner_class IN ('operator', 'mixed')`,
> ordered by `rice_score DESC`.
>
> Re-render: `py scripts/render_operator_inbox.py`. Determinism gate runs in
> release-gate.

<!-- BEGIN AUTO -->

_Rows: 35 (open · operator/mixed · ranked by RICE desc)._

| OPS ID | Initiative | Owner | RICE | What | Notes |
| --- | --- | --- | --- | --- | --- |
| `OPS-66-2` | INIT-OPENCLAW_AKOS-66 — Initiative 66 - Brand Vision Ops Sweep | operator (System Owner) | 2040 | Apply P6 governance Supabase migration | Fallback rows keep panels usable before apply |
| `OPS-67-1` | INIT-OPENCLAW_AKOS-66 — Initiative 66 - Brand Vision Ops Sweep | operator (Brand & Narrative Manager) | 1920 | Kick off I67 RevOps Discovery research | Launch gate for I67 |
| `OPS-66-1` | INIT-OPENCLAW_AKOS-66 — Initiative 66 - Brand Vision Ops Sweep | operator (Legal Counsel) | 840 | Submit trademark filings with counsel | Counsel and operator credentials required |
| `OPS-81-1` | INIT-OPENCLAW_AKOS-81 — I81 - Vault integrity sweep + Compliance layout reorganisation + named-milestone schema + full-vault SOP body/addendum retrofit | mixed (PMO) | 10 | I81 P1 vault integrity + DQ sprint + P2 layout-migration tranches coordination | Cluster wave-1 burndown sibling per I86 D-IH-86-A; D-IH-81-A absorbed mode allows parallel waves. |
| `OPS-82-1` | INIT-OPENCLAW_AKOS-82 — I82 - Holistika Capability Doctrine and Commercial Readiness (audience-aware capability surfacing) | mixed (PMO) | 9 | I82 doctrine mint + Talent activation + 3 facet-registry mints + live capability-surfacing UAT scheduling | Cluster wave-1 burndown sibling per I86 D-IH-86-A; consumes I81 P1 and I85 P1 outputs; forward-charters I83. |
| `OPS-14-1` | INIT-OPENCLAW_AKOS-14 — Initiative 14 — Holistika internal GTM and marketing operations (HLK-aligned) | operator (PMO) | — | (seed; needs operator triage) | seeded by I59 P3 audit pass; verify owner_class + RICE |
| `OPS-47-1` | INIT-OPENCLAW_AKOS-50 — Initiative 50 — Live cycle closure + cost SSOT truth-up | operator (PMO) | — | (seed; needs operator triage) | seeded by I59 P3 audit pass; verify owner_class + RICE |
| `OPS-47-2` | INIT-OPENCLAW_AKOS-50 — Initiative 50 — Live cycle closure + cost SSOT truth-up | operator (PMO) | — | (seed; needs operator triage) | seeded by I59 P3 audit pass; verify owner_class + RICE |
| `OPS-47-6` | INIT-OPENCLAW_AKOS-51 — Initiative 51 — Persona calibration cleanup | operator (PMO) | — | (seed; needs operator triage) | seeded by I59 P3 audit pass; verify owner_class + RICE |
| `OPS-47-8` | INIT-OPENCLAW_AKOS-52 — Initiative 52 — Multi-model judge roster + live calibration burn + endpoint cost truth-up | operator (PMO) | — | (seed; needs operator triage) | seeded by I59 P3 audit pass; verify owner_class + RICE |
| `OPS-47-9` | INIT-OPENCLAW_AKOS-50 — Initiative 50 — Live cycle closure + cost SSOT truth-up | operator (PMO) | — | (seed; needs operator triage) | seeded by I59 P3 audit pass; verify owner_class + RICE |
| `OPS-50-1` | INIT-OPENCLAW_AKOS-51 — Initiative 51 — Persona calibration cleanup | operator (PMO) | — | (seed; needs operator triage) | seeded by I59 P3 audit pass; verify owner_class + RICE |
| `OPS-51-1` | INIT-OPENCLAW_AKOS-51 — Initiative 51 — Persona calibration cleanup | operator (PMO) | — | (seed; needs operator triage) | seeded by I59 P3 audit pass; verify owner_class + RICE |
| `OPS-52-1` | INIT-OPENCLAW_AKOS-52 — Initiative 52 — Multi-model judge roster + live calibration burn + endpoint cost truth-up | operator (PMO) | — | (seed; needs operator triage) | seeded by I59 P3 audit pass; verify owner_class + RICE |
| `OPS-52-2` | INIT-OPENCLAW_AKOS-52 — Initiative 52 — Multi-model judge roster + live calibration burn + endpoint cost truth-up | operator (PMO) | — | (seed; needs operator triage) | seeded by I59 P3 audit pass; verify owner_class + RICE |
| `OPS-53-1` | INIT-OPENCLAW_AKOS-46 — Initiative 46 — Neo4j Strategic Posture: doctrine + GraphRAG PoC + agent memory ADR | operator (PMO) | — | (seed; needs operator triage) | seeded by I59 P3 audit pass; verify owner_class + RICE |
| `OPS-54-1` | INIT-OPENCLAW_AKOS-54 — Initiative 54 — Surface test hardening | operator (PMO) | — | (seed; needs operator triage) | seeded by I59 P3 audit pass; verify owner_class + RICE |
| `OPS-54-1.c` | INIT-OPENCLAW_AKOS-57 — Initiative 57 — Cycle closeout + live validation forward | operator (PMO) | — | (seed; needs operator triage) | seeded by I59 P3 audit pass; verify owner_class + RICE |
| `OPS-55-1` | INIT-OPENCLAW_AKOS-55 — Initiative 55 — Brand Ops Continuous Loop (Adviser updates -> regression gates) | operator (PMO) | — | (seed; needs operator triage) | seeded by I59 P3 audit pass; verify owner_class + RICE |
| `OPS-56-1` | INIT-OPENCLAW_AKOS-56 — Initiative 56 — First-response cycle (Adviser engagement operationalisation) | operator (PMO) | — | (seed; needs operator triage) | seeded by I59 P3 audit pass; verify owner_class + RICE |
| `OPS-57-1` | INIT-OPENCLAW_AKOS-57 — Initiative 57 — Cycle closeout + live validation forward | operator (PMO) | — | (seed; needs operator triage) | seeded by I59 P3 audit pass; verify owner_class + RICE |
| `OPS-57-2` | INIT-OPENCLAW_AKOS-57 — Initiative 57 — Cycle closeout + live validation forward | operator (PMO) | — | (seed; needs operator triage) | seeded by I59 P3 audit pass; verify owner_class + RICE |
| `OPS-58-1` | INIT-OPENCLAW_AKOS-58 — Initiative 58 — Cycle 2 multi-track forward | operator (PMO) | — | (seed; needs operator triage) | seeded by I59 P3 audit pass; verify owner_class + RICE |
| `OPS-58-2` | INIT-OPENCLAW_AKOS-58 — Initiative 58 — Cycle 2 multi-track forward | operator (PMO) | — | (seed; needs operator triage) | seeded by I59 P3 audit pass; verify owner_class + RICE |
| `OPS-58-4` | INIT-OPENCLAW_AKOS-58 — Initiative 58 — Cycle 2 multi-track forward | operator (PMO) | — | (seed; needs operator triage) | seeded by I59 P3 audit pass; verify owner_class + RICE |
| `OPS-59-1` | INIT-OPENCLAW_AKOS-59 — Initiative 59 — HLK governance promotion + clean slate cycle | operator (PMO) | — | Merge telemetry promotion proposals into PERSONA_SCENARIO_REGISTRY.csv | I59 P7; zero proposals at initial run (no telemetry data); re-run each cycle |
| `OPS-76-1` | INIT-OPENCLAW_AKOS-76 — I76 - MADEIRA elevation (operator-interaction quality at Cursor-grade) | operator (System Owner) | — | I76 P0 charter coordination - Wave A Lane 5 promotion under Option 5 default posture | Charter promotion ratified at A1 Option D novel framing (full P0..P6 charter + scope-overlap-tracker minted at P0). Inherits D-IH-84-C AICs F5 pre-ratification. P4 canonical-CSV gate mandatory pause-point per akos-agent-checkpoint-discipline.mdc. |
| `OPS-76-2` | INIT-OPENCLAW_AKOS-86 — I86 - Initiative Cluster Execution Coordinator (Waves 1-5 burndown) | operator (PMO) | — | Blocker-tracker review cadence - I74 candidate (TRIGGER-2 not met) | Quarterly review minimum even if no external trigger fires; ensures operator visibility of dormant candidate intent. Reverted-promotion lineage D-IH-86-F/G preserved in tracker. Will be relinked to forwarded_to_initiative_id at promotion time. |
| `OPS-76-3` | INIT-OPENCLAW_AKOS-86 — I86 - Initiative Cluster Execution Coordinator (Waves 1-5 burndown) | operator (PMO) | — | Blocker-tracker review cadence - I75 candidate (I72 P0 + I73 P0 + Research Director hire pending) | Most constraint-blocked of four Lane 5 candidates (3 of 6 conditions PENDING). Will be relinked to forwarded_to_initiative_id at promotion time. |
| `OPS-76-4` | INIT-OPENCLAW_AKOS-86 — I86 - Initiative Cluster Execution Coordinator (Waves 1-5 burndown) | operator (PMO) | — | Blocker-tracker review cadence - I83 candidate (I82 P4 USE_CASE_ARCHIVE not minted) | Two-stage unblock: I82 P4 first then I76 P3. Status flips from blocked-on-I82-P4 to blocked-on-I76-P3 at first stage. Will be relinked to forwarded_to_initiative_id at promotion time. |
| `OPS-86-1` | INIT-OPENCLAW_AKOS-86 — I86 - Initiative Cluster Execution Coordinator (Waves 1-5 burndown) | mixed (PMO) | — | I86 cluster coordination - Waves 1-5 nine-sibling burndown | Cadence event-driven per D-IH-86-B; spotlight facilitation per D-IH-86-A; sibling charters remain authoritative for scope. |
| `OPS-86-3` | INIT-OPENCLAW_AKOS-86 — I86 - Initiative Cluster Execution Coordinator (Waves 1-5 burndown) | operator (PMO) | — | I86 P2 — promote program_anchors to first-class column (Supabase DDL + Pydantic fieldnames + validator FK block) | Pause-record reports/p2-pause-record-<date>.md required before merge. |
| `OPS-86-8` | INIT-OPENCLAW_AKOS-86 — I86 - Initiative Cluster Execution Coordinator (Waves 1-5 burndown) | operator (PMO) | — | Wave N: refine inter_wave_regression_sweep probes (DIM-02 valid_statuses sync from canonical INITIATIVE_REGISTRY at load + DIM-04 forward-charter slot verification) | Wave M deferral per Cluster A sub-decision D-IH-86-BT. Forward-cadence: probe-refactor lands inside Wave N as P0 cleanup. |
| `OPS-86-9` | INIT-OPENCLAW_AKOS-86 — I86 - Initiative Cluster Execution Coordinator (Waves 1-5 burndown) | operator (PMO) | — | Wave N+: mint paired runbooks for the 4 Quality Fabric specialty canonicals (dataops + mktops + techops paired runbooks; UX SOP) | Wave M Cluster B engrave-properly deferral per D-IH-86-BU. Scope estimate: 3 person-weeks total across the 4 runbooks (Q3 2026 forward-charter). |
| `OPS-89-1` | INIT-OPENCLAW_AKOS-89 — I89 - HLK-ERP persona-rollup panel implementation (six routes incl Adviser-external REDACTED) | mixed (PMO) | — | I89 P0 charter coordination - tri-co-owned cross-cutting six-phase rollout | Cluster-coordination cost low (no sibling-coordination across the I86 ten-sibling list); higher operator-cycle cost on Adviser-external pause-point at P3. Closes when D-IH-89-CLOSURE mints. |

<!-- END AUTO -->

## Reading guide

- **OPS ID** is the canonical primary key in `OPS_REGISTER.csv`.
- **Initiative** is the originating initiative (linked via
  `originating_initiative_id`).
- **Owner** is `owner_class` followed by the labelled `owner_role`.
- **RICE** is the persisted `rice_score` (numeric). `impact=N` indicates a
  partial RICE (`rice_impact` set, full score not yet computed).
- **What** is the row's `title`; **Notes** is the row's `notes` field.

## How rows enter and leave this inbox

- **Enter:** a coding cycle mints a new row in `OPS_REGISTER.csv` with
  `status='open'` and `owner_class='operator'` or `'mixed'`. The next inbox
  re-render picks it up.
- **Leave:** the operator (or a follow-up cycle) flips the row's `status` to
  `closed` (or `forwarded`/`superseded`) in `OPS_REGISTER.csv`. The next inbox
  re-render drops it.
- Closed history lives in `OPS_REGISTER.csv` itself; the `closed_at` /
  `linked_decision_ids` fields preserve the audit trail without polluting this
  active surface.

## Cross-references

- Status taxonomy SSOT: `akos/planning/status_taxonomy.py`
- Initiative governance lifecycle SOP:
  `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/SOP-INITIATIVE_GOVERNANCE_001.md`
- Process harmonisation SOP (forward-looking):
  `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/SOP-INITIATIVE_PROCESS_HARMONISATION_001.md`
- I59 master roadmap (this surface's parent):
  `docs/wip/planning/59-hlk-governance-clean-slate/master-roadmap.md`
