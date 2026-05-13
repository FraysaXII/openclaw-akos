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

_Rows: 25 (open · operator/mixed · ranked by RICE desc)._

| OPS ID | Initiative | Owner | RICE | What | Notes |
| --- | --- | --- | --- | --- | --- |
| `OPS-66-2` | INIT-OPENCLAW_AKOS-66 — Initiative 66 - Brand Vision Ops Sweep | operator (System Owner) | 2040 | Apply P6 governance Supabase migration | Fallback rows keep panels usable before apply |
| `OPS-67-1` | INIT-OPENCLAW_AKOS-66 — Initiative 66 - Brand Vision Ops Sweep | operator (Brand Manager) | 1920 | Kick off I67 RevOps Discovery research | Launch gate for I67 |
| `OPS-66-1` | INIT-OPENCLAW_AKOS-66 — Initiative 66 - Brand Vision Ops Sweep | operator (Legal Counsel) | 840 | Submit trademark filings with counsel | Counsel and operator credentials required |
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
| `OPS-71-1` | INIT-OPENCLAW_AKOS-71 — CI/CD Discipline and AIOps Baseline Maturity | operator (PMO) | — | Validator pack productization (I71 Strand A) | Opened at I71 P0 charter; closure targeted I71 P6. |

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
