---
language: en
phase: P10+R-A..R-F
initiative: INIT-OPENCLAW_AKOS-72
authored: 2026-05-14
authored_by: CMO
last_review: 2026-05-15
last_review_by: CMO
last_review_decision_id: D-IH-72-AP
methodology_version_at_review: v3.0
status: shipped
---

# I72 P10 — Initiative closing report (+ R-A..R-F regression amendment)

> Closes `INIT-OPENCLAW_AKOS-72` (Marketing Area Governance + Persona Registry + IntelligenceOps Register Expansion + RevOps Integration Spine + Process Catalog) after 11 phases (P0..P10) and 35 ratified `D-IH-72-*` decisions (A..AH + CLOSURE), plus a 6-phase regression amendment (R-A..R-F) ratifying 7 additional decisions (AI..AP) per the operator's "disciplines ≠ roles, no horizontal bloat" principle.

## Closure ratification

- **`D-IH-72-CLOSURE`** minted at this commit; appended to `DECISION_REGISTER.csv`.
- **`INITIATIVE_REGISTRY.csv`** row 58 flipped: `status: active` → `status: closed`; `closed_at: 2026-05-14`; `closure_decision_id: D-IH-72-CLOSURE`; `manifests_processes` populated with the 8 active cadence-bound process_list rows shipped under this initiative.
- **`OPS_REGISTER.csv`**: 10 OPS-72-* rows flipped to `status: closed` with `closed_at: 2026-05-14`.
- **`master-roadmap.md`** frontmatter `status: closed` (matches `INITIATIVE_REGISTRY` per `validate_initiative_registry_frontmatter_sync.py`).

## Phase-by-phase delivery summary

| Phase | Strand | Deliverable | Commit | Closes |
| :---: | :---: | :--- | :---: | :---: |
| P0 | charter | 34 D-IH rows + 10 OPS rows + new Cursor rule akos-executable-process-catalog.mdc + INIT-72 active flip + 17 file commit | `d8cb0db` + `f71f10b` | — |
| P1 | A.1 | 6 sub-area charters (Reach + Resonance + Account Management + Storytelling + Experimentation + Operations/RevOps) + GTM-to-Reach SOP migration + MARKETING_AREA_M3_REDESIGN cross-link update | `d6e89a5` | OPS-72-6 + OPS-72-10 |
| P2 | A.2 | ENGAGEMENT_TEMPLATE_REGISTRY canonical CSV + akos SSOT + validator + Supabase mirror + CANONICAL_REGISTRY + PRECEDENCE | `94afa3e` | OPS-72-1 |
| P3 | A.2 | SOP-ENGAGEMENT_TEMPLATE_PROMOTION_001.md + paired validator + process_list row tbi_mkt_dtp_revops_template_promotion_001 | `4b974b2` | OPS-72-2 |
| P4 | A.3 | RevOps activation: 7 baseline_organisation rows + process_list 7-col schema migration + SOP-REVOPS_QBR_001.md + Supabase migration + USER_GUIDE update | `48870b1` + `3e48d2c` | OPS-72-3 |
| P5 | B | 2 new personas + 4 PERSONA_SCENARIO_REGISTRY scenarios | `f967db3` + `bb64c74` | OPS-72-4 |
| P6 | C | INTELLIGENCEOPS_REGISTER canonical CSV + akos SSOT + validator + 4 seed rows + 2 SOPs (regulator + media) | `ee6af96` + `ba6bd63` | OPS-72-5 |
| P7 | D.1 | RevOps Integration Spine: finops FK migration + governance.engagement_revenue_view + akos SSOT + validator + tests + release-gate row | `6bc4d1b` + `575e01b` | OPS-72-7 |
| P8 | D.2 | REVOPS_PROCESS_CATALOG.yaml (8 seed processes) + revops_dispatch.py + scaffold_engagement.py + 6 process_list rows | `25ede2f` + `8743c80` | OPS-72-8 |
| P9 | D.3 | 8 adapter registries (CRM + REVOPS + EMAIL + ATTRIBUTION + BILLING + COMMUNICATION + SCHEDULING + CONTRACT) + 6 paired SOPs + 2 validators (validate_adapter_registries.py + validate_process_list_pairing.py) + Supabase mirror DDL (8 tables) + CANONICAL_REGISTRY + PRECEDENCE + CHANGELOG | `297d6b7` + `11f98cd` | OPS-72-9 |
| P10 | closure | D-IH-72-CLOSURE + 1 INIT closure + 10 OPS closures + master-roadmap status flip + this report + CHANGELOG closure entry | (this commit) | — |

## What ships at closure

- **35 `D-IH-72-*` decisions ratified** (A..AH + CLOSURE) — 4 super-strands across Marketing area governance + Persona Registry + IntelligenceOps Register + RevOps Integration Spine + Process Catalog.
- **6 sub-area charters** (5 Marketing + 1 Operations/RevOps) under the Round 7 5-sub-area redesign.
- **2 new canonical sibling CSVs** (ENGAGEMENT_TEMPLATE_REGISTRY + INTELLIGENCEOPS_REGISTER) plus **8 adapter registries** (CRM + REVOPS + EMAIL + ATTRIBUTION + BILLING + COMMUNICATION + SCHEDULING + CONTRACT) — 10 net-new canonical CSVs total.
- **process_list.csv 7-column schema migration** (4 axis FKs + 3 revenue value cells per `D-IH-72-AF`) operationalising the multi-axis Marketing dimension ontology + value-mapping core function.
- **7 new baseline_organisation roles**: 2 active (RevOps Lead + RevOps Analyst) + 4 gated_ahead_of_growth_stage + 1 gated_ahead_of_executive_activation (CRO; COO already existed).
- **2 new personas + 4 UAT scenarios** in PERSONA_REGISTRY + PERSONA_SCENARIO_REGISTRY.
- **REVOPS_PROCESS_CATALOG.yaml** (8 seed processes) + **revops_dispatch.py** dispatcher + **scaffold_engagement.py** RPA scaffolder per `D-IH-72-N` + `D-IH-72-P`.
- **RevOps Integration Spine**: `engagement_id` + `template_id` FK columns on `finops.registered_fact` + `governance.engagement_revenue_view` joining mirrors per `D-IH-72-M`.
- **15 new SOPs** (1 promotion gate + 1 QBR + 2 IntelligenceOps + 5 P9 cross-area handoff + 1 CRM integration + 1 Research engagement trigger + 4 sub-area charter sister SOPs).
- **5 new validators**: `validate_engagement_template_registry.py` + `validate_engagement_template_promotion.py` + `validate_intelligenceops_register.py` + `validate_revops_spine.py` + `validate_adapter_registries.py` + `validate_process_list_pairing.py` (all wired into `validate_hlk.py` dispatcher; 4 wired into `release-gate.py`).
- **6 new Supabase migrations**: ENGAGEMENT_TEMPLATE_REGISTRY mirror + process_list 7-col extension + INTELLIGENCEOPS_REGISTER mirror + RevOps spine FK + adapter registries 8 mirrors + (P4 baseline org schema cascade implicit).
- **New Cursor rule** `.cursor/rules/akos-executable-process-catalog.mdc` (5 rules: SOP+runbook pairing + adapter status metadata + cadence taxonomy + DAMA-DMBOK 2.0 alignment + AC binary axis).

## UAT bands self-verification (operator blanket-trust posture aligned with I71 closure precedent)

- **Band A — HLK validators**: `py scripts/validate_hlk.py` PASS (18 dispatched). `py scripts/validate_decision_register.py` PASS (172 rows). `py scripts/validate_initiative_registry.py` PASS (58 rows). `py scripts/validate_ops_register.py` PASS (40 rows). `py scripts/validate_master_roadmap_frontmatter.py` PASS (58 folders).
- **Band B — Vault links**: `py scripts/validate_hlk_vault_links.py` PASS (no broken internal .md links; TODO markers per `D-IH-72-W` tolerated).
- **Band C — RevOps Spine** (P7 contract): `py scripts/validate_revops_spine.py` PASS (governance view + finops FK columns intact).
- **Band D — Adapter registries** (P9 contract): `py scripts/validate_adapter_registries.py` PASS (8 registries; all schema + enums + cross-class consistency green).
- **Band E — Process pairing** (P9 contract): `py scripts/validate_process_list_pairing.py` PASS (8 cadence-bound rows; 7 paired + 1 informational warning per `D-IH-72-W`).

## Forward-charters retained

- **I73** People Operations Lead activation + recruiter onboarding SOP (per `D-IH-72-K` + `D-IH-72-W`).
- **I75** Research/Intelligence cross-coordination follow-on (per `D-IH-72-W`).
- **I76** AIC (Agent in Charge) `role_owner` activation (per `D-IH-72-S`).
- **Tech/Data successor initiative**: SOP-TECH_REVOPS_OBSERVABILITY_001 + SOP-DATA_REVOPS_GOVERNANCE_001 + dedicated tech adapter registry expansion.
- **CRO + COO executive layer activation**: gated rows in `baseline_organisation.csv` per `D-IH-72-AD` await growth-stage trigger.
- **6 RevOps expansion roles** (RevOps Systems Specialist + RevOps Process Architect + RevOps Enablement Lead + RevOps Data Engineer + 2 more): gated_ahead_of_growth_stage rows per `D-IH-72-AC`.
- **TODO[I72-FOLLOWUP-MADEIRA-RUNBOOK]** in `SOP-MADEIRA_REVOPS_HANDOFF_001.md` §3.2 — actual MADEIRA invocation surface specification.

## Cross-references

- Authoritative plan: [`.cursor/plans/i72-marketing-area-governance-and-persona-registry-expansion_72c0a5e3.plan.md`](../../../.cursor/plans/i72-marketing-area-governance-and-persona-registry-expansion_72c0a5e3.plan.md).
- Phase reports: `reports/p0-charter-2026-05-14.md` + `reports/p9-cross-area-integration-2026-05-14.md` + this `p72-closing.md`.
- Files-modified history: `files-modified.csv` (92 rows across P0..P9; P10 rows + R-A..R-F rows appended; ~150 rows total at R-F close).
- Inception decision: `D-IH-70-AC` (forward-charter source from I70 P8.5 GOI hunt).
- Precedent closure pattern: I71 P6 closing (`D-IH-71-CLOSURE`; same blanket-trust UAT posture).

---

## Regression amendment R-A..R-F (post-P10)

After P10 closure, an end-to-end regression review was launched (subagent sweep
2026-05-14 evening) covering all 35 D-IH-72-* decisions, the new Cursor rule,
canonical CSVs, sub-area folder hygiene, and YAML companion pointers. Nine
evidence-grounded questions were surfaced via inline-ratify; the operator's
responses crystallized one architectural principle and triggered a 6-phase
amendment cycle:

> **"Disciplines ≠ roles. New roles should do lots of things; do not bloat the
> org horizontally."**

The amendment did NOT spin up a new initiative (per operator framing: "this is
nothing but a regression, a big one"). It is treated as a post-shipment regression
amendment to I72 itself, with all decisions minted under the same `D-IH-72-*`
namespace and without a v3.2.0 SemVer cut (operator: v3.1 is still being built).

### R-A — Cursor rule hardening (commit `93f82db`, 6 files +18/-11)

Decisions: `D-IH-72-AI` (path corrections) + `D-IH-72-AJ` (alwaysApply audit).

- `akos-executable-process-catalog.mdc`: added missing YAML frontmatter
  (`description` + `alwaysApply: true`); corrected 4 adapter-registry paths in
  Rule 2 (REVOPS, BILLING, COMMUNICATION, CONTRACT) to match where they actually
  shipped during P9 (not where the planning draft predicted).
- 4 additional Cursor rules elevated to `alwaysApply: true` per the operator's
  "be generous" guidance: `akos-planning-traceability`,
  `akos-agent-checkpoint-discipline`, `akos-holistika-operations`,
  `akos-brand-baseline-reality`.

### R-B — Folder cleanup + SOP backfill (commit `16f08ae`, 9 files +327/-4)

Decisions: `D-IH-72-AK` (catalog SOP backfill) + `D-IH-72-AL` (Social/Growth removal).

- Deleted dead `Marketing/Social/` and `Marketing/Growth/` folder shells (only
  `.gitkeep` placeholders remained from a never-activated v3.0 plan; obsolesced
  by the M3 5-sub-area redesign per `D-IH-72-D` + `D-IH-72-E`).
- Authored 3 missing SOPs referenced by `REVOPS_PROCESS_CATALOG.yaml`:
  `SOP-REVENUE_ROLLUP_001.md`, `SOP-PERSONA_AUDIT_001.md`,
  `SOP-ENGAGEMENT_SCAFFOLDING_001.md`. Replaced 3 `TODO[I72-...]` pointers in
  the YAML catalog with concrete paths; fixed 1 stale `crm_sync.runbook_pointer`.
- Added 3 new `CANONICAL_REGISTRY.csv` rows for the new SOPs.

### R-C — RevOps role slim (commit `dd86b22`, 4 files +14/-17; baseline 82→78)

Decision: `D-IH-72-AM` (RevOps role consolidation).

- Deleted 4 `gated_ahead_of_growth_stage` rows from `baseline_organisation.csv`
  (RevOps Systems Specialist + RevOps Process Architect + RevOps Enablement Lead
  + RevOps Data Engineer). These were the operator's primary horizontal-bloat
  example: 4 forward-chartered specialist roles for what should be 4 disciplines
  inside one role's headcount expansion pattern.
- `RevOps Lead` role description now explicitly absorbs all 4 disciplines
  (systems, process, enablement, data engineering) as growth-stage scaling vectors
  rather than separate role lines.
- `REVOPS_AREA_CHARTER.md` §2 table updated to reflect the slim 2-role active
  structure (RevOps Lead + RevOps Analyst); `SOP-REVENUE_ROLLUP_001.md` §4
  failure-mode escalation rerouted from the deleted Data Engineer to RevOps Lead.

### R-D — Marketing sub-role selective collapse (commit `ccbf87d`, 11 files +52/-57; baseline 78→72)

Decision: `D-IH-72-AN` (Marketing sub-role consolidation, selective).

- Deleted 6 sub-role rows from `baseline_organisation.csv`: Demand Generation
  Manager, Paid Media Manager (both absorbed by Reach Manager); Community
  Manager (absorbed by Resonance Manager); Thought Leadership Editor + Corporate
  Marketing (both absorbed by Storytelling Manager); Growth Hacker (absorbed by
  Experimentation Manager).
- Retained 3 sub-roles with distinct external mandates: Account Management
  Manager (client-facing distinct from internal RevOps), PR Manager
  (regulator/media-facing distinct from brand work), Marketing Analytics Manager
  (cross-sub-area horizontal capability).
- Cascade rewrites: 17 `process_list.csv` rows rerouted role_owner to the parent
  Sub-Area Manager; `POL-RLS-HOLISTIKA-OPS-LEAD-INTAKE` policy owner updated.
- 4 sub-area charters + `MARKETING_AREA_M3_REDESIGN.md` + `BRAND_DISCIPLINE_ONTOLOGY.md`
  + `ACCOUNT_MANAGEMENT_CHARTER.md` updated with the new generalist-manager
  taxonomy and absorbed-discipline notes.

### R-E — Brand+Storytelling → "Brand & Narrative" merger (commit `a09fbe6`, 38 files +123/-90; baseline 72→67)

Decision: `D-IH-72-AO` (Brand+Storytelling merger).

The deepest cut. Per the operator's reframed Q1b answer, Brand and Storytelling
were not just peer sub-areas — they were the same sub-area split twice. Merger
rationale: visual identity + voice + narrative arc + thought leadership + AV +
copywriting + UX writing all serve one mandate (how Holistika sounds and looks
to the outside world). PR sits naturally under Brand & Narrative as the
counterparty-facing wing of the same discipline cluster.

- Deleted 5 baseline rows: AV, Copywriter, Design, UX Designer (Brand sub-roles)
  + Storytelling Manager (collapsed into the merged manager).
- Renamed `Brand Manager` → `Brand & Narrative Manager`; new role description
  absorbs visual identity + voice + copywriting + AV production + UX design +
  thought leadership editorial + corporate marketing as scaling-vector
  disciplines (not new role lines).
- `PR Manager.reports_to` rerouted to `Brand & Narrative Manager`;
  `PR Manager.sub_area` updated to `Brand & Narrative`.
- `CMO` description rewritten to list the new 4-sub-area structure
  (Brand & Narrative + Reach + Resonance + Experimentation) — collapsed from 5
  per `D-IH-72-AO`.
- Cascade rewrites (FK columns only; narrative bodies untouched as historical
  record): 40 `process_list.csv` rows + `PERSONA-PRESS` handoff_role + 5
  `POLICY_REGISTER.csv` rows + 1 `TOPIC_REGISTRY.csv` row + 1
  `CHANNEL_TOUCHPOINT_REGISTRY.csv` row + 1 `SKILL_REGISTRY.csv` row +
  `boilerplate` `REPOSITORY_REGISTRY.csv` row + 3 `INITIATIVE_REGISTRY.csv` rows
  (66/67/77) + 2 `OPS_REGISTER.csv` rows (67-1, 77-1) + 1
  `INTELLIGENCEOPS_REGISTER.csv` row (IO-MED-PLACEHOLDER-001) + 25 markdown
  YAML frontmatter rewrites under `Marketing/Brand/`, `Marketing/Storytelling/`,
  `Operations/Engagement/`.

**Filesystem strategy (deliberate)**: `Marketing/Brand/` and
`Marketing/Storytelling/` folders kept in place to preserve cross-reference
stability. The conceptual merger lives in role descriptions, charters,
frontmatter, and the registry. A future filesystem-only pass may consolidate
the two folders under `Marketing/Brand & Narrative/` once cross-link debt is
quantified — but R-E does NOT take that step (minimum-disruption).

### R-F — Closing amendment report + D-IH-72-AP (this commit)

Decision: `D-IH-72-AP` (regression amendment R-A..R-E closure ratification).

- This report (`p72-closing.md`) amended with the R-A..R-F section above.
- `CHANGELOG.md` `[Unreleased]` band updated with R-A..R-F entries (no v3.2.0
  cut per operator: v3.1 is still being built).
- `files-modified.csv` backfilled with R-F closure rows.
- `INITIATIVE_REGISTRY.csv` row 58 `last_review_at` + `last_review_decision_id`
  updated to `D-IH-72-AP`.

### Net regression amendment delta

| Metric | Before R-A | After R-F | Delta |
| :--- | ---: | ---: | ---: |
| `baseline_organisation.csv` rows | 82 | 67 | **−15** |
| Active Marketing sub-areas | 5 | 4 | **−1** (Brand+Storytelling merged) |
| RevOps active roles | 2 | 2 | 0 (4 forward-chartered specialists deleted) |
| Marketing sub-roles below sub-area manager | 9 | 3 | **−6** (selective collapse) |
| `D-IH-72-*` decisions ratified | 35 (A..AH + CLOSURE) | 42 (A..AP + CLOSURE) | **+7** |
| `Marketing/Social/` + `Marketing/Growth/` shells | present (dead) | deleted | cleanup |
| Cursor rules with `alwaysApply: true` | 0 of 5 net-new | 5 of 5 | hardened |
| `REVOPS_PROCESS_CATALOG.yaml` `TODO[...]` pointers | 4 | 0 | resolved |

### UAT bands re-verification at R-F

- **Band A — HLK validators**: `py scripts/validate_hlk.py` PASS (0 errors;
  12 advisory warnings unchanged, all pre-existing).
- **Band B — Vault links**: PASS (no broken internal links introduced by R-A..R-E).
- **Band C — RevOps Spine** (P7 contract): PASS (slim role taxonomy doesn't
  affect the FK schema or governance view).
- **Band D — Adapter registries** (P9 contract): PASS (path corrections in R-A
  match where the registries actually shipped).
- **Band E — Process pairing** (P9 contract): PASS (3 backfilled SOPs in R-B
  resolved 3 of 4 informational warnings; 1 warning remains as
  `tbi_ops_dtp_revops_media_review_001` per `D-IH-72-W` design tolerance).

### Closure posture at R-F

`INIT-OPENCLAW_AKOS-72` remains `status: closed`. The R-A..R-F amendment is
NOT a re-opening. It is documented under the same initiative ID as a
regression-amend cycle (mirroring how a software release ships patch-band
bugfixes without bumping the major version). All work shipped on `main` per
the operator's "regression, a big one" framing.
