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

_Rows: 33 (open · operator/mixed · ranked by RICE desc)._

| OPS ID | Initiative | Owner | RICE | What | Notes |
| --- | --- | --- | --- | --- | --- |
| `OPS-66-2` | INIT-OPENCLAW_AKOS-66 — Initiative 66 - Brand Vision Ops Sweep | operator (System Owner) | 2040 | Apply P6 governance Supabase migration | Fallback rows keep panels usable before apply |
| `OPS-67-1` | INIT-OPENCLAW_AKOS-66 — Initiative 66 - Brand Vision Ops Sweep | operator (Brand & Narrative Manager) | 1920 | Kick off I67 RevOps Discovery research | Launch gate for I67 |
| `OPS-66-1` | INIT-OPENCLAW_AKOS-66 — Initiative 66 - Brand Vision Ops Sweep | operator (Legal Counsel) | 840 | Submit trademark filings with counsel | Counsel and operator credentials required |
| `OPS-77-1` | INIT-OPENCLAW_AKOS-77 — Initiative 77 - Impeccable Brand-Bridge Refresh + Drift Gate | operator (Brand & Narrative Manager) | 500 | Impeccable bridge refresh + drift gate execution (I77 P1-P3) | Opened at I77 P0 charter; closure targeted I77 P3 UAT. |
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
| `OPS-73-10` | INIT-OPENCLAW_AKOS-73 — I73 — People Operations + Engagement Models + Methodology IP (mega-initiative) | mixed (PMO) | — | P10 Cross-strand integration verification — all 8 strands cohere; SOPs reference Engagement Registry; IP minting flagged in advisor pipeline; Learning references registry for apprentice onboarding; Ethics quarterly review covers IP cadence | Closure target P10 (~1 day after P9 closes). Precedes P11 closure. |
| `OPS-73-3` | INIT-OPENCLAW_AKOS-73 — I73 — People Operations + Engagement Models + Methodology IP (mega-initiative) | mixed (People Operations Lead) | — | Strand C Engagement-lifecycle SOPs (hiring + onboarding + payroll + offboarding) parameterized by engagement_model_id + paired runbooks per akos-executable-process-catalog.mdc Rule 1 | Closure target P3 (~3-4 days). Inline-ratify gate C-73-4 SOP shape (default parameterized; split if >6 cases). |
| `OPS-73-4` | INIT-OPENCLAW_AKOS-73 — I73 — People Operations + Engagement Models + Methodology IP (mega-initiative) | operator (People Operations Lead) | — | Strand F HISTORICAL_ENGAGEMENT_CASE_LAW codification (Bâtard 2020 + Mark-II + Alias V + RCD Legal + L'Oréal arrangement; access_level=5 register=internal frontmatter) | Closure target P4 (~2 days). Inline-ratify gate C-73-8 anonymization scope (default anonymize counterparty names; preserve case codenames). akos-brand-baseline-reality.mdc forbidden contexts apply. |
| `OPS-73-5` | INIT-OPENCLAW_AKOS-73 — I73 — People Operations + Engagement Models + Methodology IP (mega-initiative) | mixed (Ethics Advisor) | — | Strand B SOP-ETHICS_LEARNING_REVIEW quarterly co-review SOP + BRAND_VOICE_FOUNDATION refresh with we-become-unethical-when-we-unlearn thesis | Closure target P5 (~1-2 days). Inline-ratify gate C-73-3 review owner (default Ethics-led with Learning co-reviewer per PEOPLE_AREA_RESTRUCTURE §3). |
| `OPS-73-6` | INIT-OPENCLAW_AKOS-73 — I73 — People Operations + Engagement Models + Methodology IP (mega-initiative) | mixed (CPO) | — | Strand D PEOPLE_COMPLIANCE_VS_ETHICS_BOUNDARY + process_list orphan reassignments (canonical-CSV gate) | Closure target P6 (~1-2 days). PAUSE POINT #2 - canonical-CSV gate (process_list tranche). Inline-ratify gate C-73-5 boundary edge cases (default Compliance owns regulatory; Ethics owns AI-overreach; joint AI-content-disclosure). |
| `OPS-73-7` | INIT-OPENCLAW_AKOS-73 — I73 — People Operations + Engagement Models + Methodology IP (mega-initiative) | mixed (PMO) | — | Strand G KB_HUMAN_READABILITY_CHARTER + 4 hlk-erp panel filter routes (operator-managed / cleared-collaborator / low-trust-outsourced / apprentice) mapped 1:1 to engagement classes | Closure target P7 (~2-3 days). Inline-ratify gate C-73-7 persona view technology (default role-tagged single surface with per-persona ERP panel filters). |
| `OPS-73-8` | INIT-OPENCLAW_AKOS-73 — I73 — People Operations + Engagement Models + Methodology IP (mega-initiative) | mixed (Brand & Narrative Manager) | — | Strand H METHODOLOGY_IP_MINTING_PATH brand-vs-name decision matrix (brand/legal PAUSE POINT) | Closure target P8 (~2 days). PAUSE POINT #3 - brand/legal gate. Inline-ratify gate C-73-6 licensing model (default decision-deferred-with-criteria-matrix per D-IH-73-F). |
| `OPS-73-9` | INIT-OPENCLAW_AKOS-73 — I73 — People Operations + Engagement Models + Methodology IP (mega-initiative) | operator (PMO) | — | P9 UAT - first engagement onboarded under new model (operator-self ratification option a OR first apprentice cohort option b) | Closure target P9 (~1 day after P7+P8 land). Operator-driven; agent does not block on it. |

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
