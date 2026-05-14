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
| `OPS-67-1` | INIT-OPENCLAW_AKOS-66 — Initiative 66 - Brand Vision Ops Sweep | operator (Brand Manager) | 1920 | Kick off I67 RevOps Discovery research | Launch gate for I67 |
| `OPS-66-1` | INIT-OPENCLAW_AKOS-66 — Initiative 66 - Brand Vision Ops Sweep | operator (Legal Counsel) | 840 | Submit trademark filings with counsel | Counsel and operator credentials required |
| `OPS-77-1` | INIT-OPENCLAW_AKOS-77 — Initiative 77 - Impeccable Brand-Bridge Refresh + Drift Gate | operator (Brand Manager) | 500 | Impeccable bridge refresh + drift gate execution (I77 P1-P3) | Opened at I77 P0 charter; closure targeted I77 P3 UAT. |
| `OPS-72-3` | INIT-OPENCLAW_AKOS-72 — Initiative 72 - Marketing Area Governance + Persona Registry + IntelligenceOps Register Expansion + RevOps Integration Spine + Process Catalog (Operations/RevOps area minted Round 7; process_list schema 7-col extension + multi-axis Marketing dimension ontology + Operations/RevOps area charter at P1 added Round 8) | mixed (CMO) | 350 | Strand A.3 RevOps owner activation (baseline + QBR SOP + PMO->RevOps handoff + process_list 7-col extension at P4) | Closure target P4 (~2-3 days). HARD EXTERNAL DEP: I71 P5 Pack A4. MANDATORY canonical-CSV gate (baseline + process_list). |
| `OPS-72-10` | INIT-OPENCLAW_AKOS-72 — Initiative 72 - Marketing Area Governance + Persona Registry + IntelligenceOps Register Expansion + RevOps Integration Spine + Process Catalog (Operations/RevOps area minted Round 7; process_list schema 7-col extension + multi-axis Marketing dimension ontology + Operations/RevOps area charter at P1 added Round 8) | mixed (PMO) | 320 | Operations/RevOps area charter authoring (REVOPS_AREA_CHARTER.md at Operations/RevOps/canonicals/) — alongside Marketing sub-area charters in P1 batch | Closure target P1 (~1-2 days within P1's 3-5 day range). Per-charter inline-ratify gate. NOT a canonical-CSV gate (charter is markdown). Cross-references: D-IH-72-Y placement; D-IH-72-AC sub-role taxonomy; D-IH-72-AD executive layer; Round 7 Role Taxonomy section in p0-charter as content seed. owner_role originally drafted as 'PMO (interim until CRO activation per D-IH-72-AD)' to capture interim-until-CRO-activation context; collapsed to clean FK PMO per validator constraint; interim context preserved here + in D-IH-72-AD notes. |
| `OPS-72-2` | INIT-OPENCLAW_AKOS-72 — Initiative 72 - Marketing Area Governance + Persona Registry + IntelligenceOps Register Expansion + RevOps Integration Spine + Process Catalog (Operations/RevOps area minted Round 7; process_list schema 7-col extension + multi-axis Marketing dimension ontology + Operations/RevOps area charter at P1 added Round 8) | mixed (CMO) | 240 | Strand A.2 SOP-ENGAGEMENT_TEMPLATE_PROMOTION_001 + promotion-rule validator + process_list row | Closure target P3 (~2-3 days). MANDATORY canonical-CSV gate. |
| `OPS-72-7` | INIT-OPENCLAW_AKOS-72 — Initiative 72 - Marketing Area Governance + Persona Registry + IntelligenceOps Register Expansion + RevOps Integration Spine + Process Catalog (Operations/RevOps area minted Round 7; process_list schema 7-col extension + multi-axis Marketing dimension ontology + Operations/RevOps area charter at P1 added Round 8) | mixed (CMO) | 214 | Strand D.1 RevOps Integration Spine (engagement_id + template_id FKs on finops.registered_fact + governance.engagement_revenue_view + ERP panel op_revops_engagement_revenue) | Closure target P7 (~3-4 days). MANDATORY canonical-CSV gate (finops schema change is high-blast-radius). DAMA-DMBOK 2.0 RMDM + Data Integration & Interoperability aligned. Cross-references: I19 finops ledger Phase 1 + I18 FINOPS counterparty register + I14 holistika_ops.stripe_customer_link. |
| `OPS-72-6` | INIT-OPENCLAW_AKOS-72 — Initiative 72 - Marketing Area Governance + Persona Registry + IntelligenceOps Register Expansion + RevOps Integration Spine + Process Catalog (Operations/RevOps area minted Round 7; process_list schema 7-col extension + multi-axis Marketing dimension ontology + Operations/RevOps area charter at P1 added Round 8) | mixed (CMO) | 194 | Strand A.1 sub-area charter authoring (5 charters: Reach + Resonance + Storytelling + Experimentation + Account Management) | Closure target P1 (~3-5 days; Round 7 +1-2 days for quality-pass). Per-charter inline-ratify gate. |
| `OPS-72-1` | INIT-OPENCLAW_AKOS-72 — Initiative 72 - Marketing Area Governance + Persona Registry + IntelligenceOps Register Expansion + RevOps Integration Spine + Process Catalog (Operations/RevOps area minted Round 7; process_list schema 7-col extension + multi-axis Marketing dimension ontology + Operations/RevOps area charter at P1 added Round 8) | mixed (CMO) | 192 | Strand A.2 ENGAGEMENT_TEMPLATE_REGISTRY canonical CSV + Supabase mirror + ERP panel slot wiring | Closure target P2 (~3-4 days). MANDATORY canonical-CSV gate. |
| `OPS-72-8` | INIT-OPENCLAW_AKOS-72 — Initiative 72 - Marketing Area Governance + Persona Registry + IntelligenceOps Register Expansion + RevOps Integration Spine + Process Catalog (Operations/RevOps area minted Round 7; process_list schema 7-col extension + multi-axis Marketing dimension ontology + Operations/RevOps area charter at P1 added Round 8) | mixed (CMO) | 117 | Strand D.2 Process Catalog (REVOPS_PROCESS_CATALOG.yaml + 8-12 paired SOPs + revops_dispatch.py + scaffold_engagement.py RPA scaffolder + process_list.csv tranche + 8 adapter registry shells) | Closure target P8 (~4-6 days). MANDATORY canonical-CSV gate. Per new Cursor rule akos-executable-process-catalog.mdc: every catalog entry has SOP path + runbook path (pairing rule). Per-catalog-entry inline-ratify (8-12 gates batched). |
| `OPS-72-4` | INIT-OPENCLAW_AKOS-72 — Initiative 72 - Marketing Area Governance + Persona Registry + IntelligenceOps Register Expansion + RevOps Integration Spine + Process Catalog (Operations/RevOps area minted Round 7; process_list schema 7-col extension + multi-axis Marketing dimension ontology + Operations/RevOps area charter at P1 added Round 8) | mixed (CMO) | 85 | Strand B Persona Registry expansion (business-developer-collaborator + surfaced personas) | Closure target P5 (~2-3 days). MANDATORY canonical-CSV gate. Independent of Strand A. |
| `OPS-72-9` | INIT-OPENCLAW_AKOS-72 — Initiative 72 - Marketing Area Governance + Persona Registry + IntelligenceOps Register Expansion + RevOps Integration Spine + Process Catalog (Operations/RevOps area minted Round 7; process_list schema 7-col extension + multi-axis Marketing dimension ontology + Operations/RevOps area charter at P1 added Round 8) | mixed (CMO) | 65 | Strand D.3 Cross-area integration (8 adapter registries CRM + REVOPS + EMAIL + ATTRIBUTION + BILLING + COMMUNICATION + SCHEDULING + CONTRACT + 6-8 paired SOPs covering Finance/Data/Tech/GTM/People/Legal/Research/MADEIRA + full validate_process_list_pairing.py validator) | Closure target P9 (~7-10 days; Round 6 effort revised from 5-7 days due to MarTech breadth). MANDATORY canonical-CSV gate. Multi-area touchpoints: requires coordination check with I73 People Operations + I75 Research + I77 Brand candidate states. DAMA-DMBOK 2.0 Metadata Management + Data Integration & Interoperability aligned. Cost-of-no-action: $12.9-15M/yr + 10-30% duplication per Truto 2026. Multi-area cross-coordination targets (originally drafted in forwarded_to_initiative_id; moved to notes per validator FK constraint): INIT-OPENCLAW_AKOS-14;INIT-OPENCLAW_AKOS-18;INIT-OPENCLAW_AKOS-19;INIT-OPENCLAW_AKOS-62;INIT-OPENCLAW_AKOS-68. |
| `OPS-72-5` | INIT-OPENCLAW_AKOS-72 — Initiative 72 - Marketing Area Governance + Persona Registry + IntelligenceOps Register Expansion + RevOps Integration Spine + Process Catalog (Operations/RevOps area minted Round 7; process_list schema 7-col extension + multi-axis Marketing dimension ontology + Operations/RevOps area charter at P1 added Round 8) | mixed (CMO) | 63 | Strand C IntelligenceOps Register Expansion (canonical CSV + 3 SOPs + I73 recruiter cross-link) | Closure target P6 (~4-6 days). MANDATORY canonical-CSV gate. Independent of Strand A. |
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
