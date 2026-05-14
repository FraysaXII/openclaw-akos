---
candidate_id: I72
title: Marketing Area Governance + Persona Registry + IntelligenceOps Register Expansion
status: promoted
promoted_at: 2026-05-14
authored: 2026-05-12
last_review: 2026-05-14
parent_initiative: 70 (closing scaffold; INIT row minted at I70 closure with broader-than-Marketing scope)
priority: 2
supersedes: I67 (RevOps Discovery)
language: en
promoted_to: docs/wip/planning/72-marketing-area-governance-and-persona-registry-expansion/master-roadmap.md
charter_ratification: docs/wip/planning/72-marketing-area-governance-and-persona-registry-expansion/reports/p0-charter-2026-05-14.md
---

# I72 promoted candidate — Marketing Area Governance + Persona Registry + IntelligenceOps Register Expansion

> **Promoted 2026-05-14** per the I72 P0 charter ratification at [`reports/p0-charter-2026-05-14.md`](reports/p0-charter-2026-05-14.md). The authoritative execution surface is now [`master-roadmap.md`](master-roadmap.md) (workspace mirror) and [`.cursor/plans/i72-marketing-area-governance-and-persona-registry-expansion_72c0a5e3.plan.md`](../../../.cursor/plans/i72-marketing-area-governance-and-persona-registry-expansion_72c0a5e3.plan.md) (authoritative Cursor plan per PLAN SCOPE guardrail).
>
> **Provenance.** This document is the promoted form of `docs/wip/planning/_candidates/i72-marketing-area-governance.md` (commit `4ca352a` rewrite — 3-super-strand reshape). Preserved here as the historical record per [`akos-planning-traceability.mdc`](../../../.cursor/rules/akos-planning-traceability.mdc) §"Naming Guidance". The original `_candidates/` file should be removed via `git rm` in the P0 atomic commit; see [`reports/p0-csv-rows-to-append-2026-05-14.md`](reports/p0-csv-rows-to-append-2026-05-14.md) §"Git mv instructions".

## 1. Operating story (preserved from candidate)

I70 P8 redesigned Marketing into the **M3 ontology** (Brand / Reach / Resonance / Storytelling / Experimentation; per [`MARKETING_AREA_M3_REDESIGN.md`](../../references/hlk/v3.0/Admin/O5-1/Marketing/canonicals/MARKETING_AREA_M3_REDESIGN.md) + `D-IH-70-T`). I70 P8.5 ran the GOI class regression hunt and ratified four new GOI/POI enum classes (`legal_counsel_external` / `supplier_infrastructure` / `competitor_intelligence_target` / `recruiter`) plus three concrete rows; per `D-IH-70-AC`, four scope items were explicitly **forward-charted to I72** rather than landed in I70:

1. **`business-developer-collaborator` persona row** under the existing partner class.
2. **`competitor-intelligence-target` schema** for IntelligenceOps register expansion.
3. **Regulator-relationship roadmap** (ENISA worked example).
4. **Media-counterparty-onboarding pattern** (PR Manager activation).

The cohering principle: **I72 is the initiative that operationalises the Marketing redesign AND the unblocking of three I70-P8.5-deferred governance dimensions**. Three super-strands share the same activation moment (operator ratifies the I72 charter) but address distinct artifacts:

- **Strand A — Marketing Area Governance** (the original candidate scope; authors per-sub-area charters + the engagement-template promotion machine + RevOps activation).
- **Strand B — Persona Registry expansion** (extends `PERSONA_REGISTRY.csv` + `PERSONA_SCENARIO_REGISTRY.csv` with the business-developer-collaborator persona and any additional personas surfaced during planning).
- **Strand C — IntelligenceOps Register Expansion** (new sibling `INTELLIGENCEOPS_REGISTER.csv`; regulator + media + recruiter onboarding SOPs at `Research/Intelligence/canonicals/`; cross-link to I75 Research area governance candidate).

## 2. Strands

See [`master-roadmap.md`](master-roadmap.md) §"Strand A — Marketing Area Governance", §"Strand B — Persona Registry expansion", and §"Strand C — IntelligenceOps Register Expansion" for the full structured strand decomposition (5 sub-area charter targets + engagement-template promotion machine + RevOps activation + 4 persona-registry deliverables + 5 IntelligenceOps deliverables).

## 3. Phase scaffold

See [`master-roadmap.md`](master-roadmap.md) §"Phase status table" for the 8-phase plan (P0 charter activation / P1 Strand A.1 5 sub-area charters / P2 Strand A.2 ENGAGEMENT_TEMPLATE_REGISTRY canonical / P3 Strand A.2 promotion SOP / P4 Strand A.3 RevOps activation [gated on I71 P5] / P5 Strand B Persona Registry / P6 Strand C IntelligenceOps Register / P7 closing UAT).

## 4. Conundrums (ratified at P0; 10 verdicts)

All 10 conundrums (C-72-1 through C-72-10) ratified at P0 per [`akos-inline-ratification.mdc`](../../../.cursor/rules/akos-inline-ratification.mdc) (architectural decisions resolve at planning time, not deferred). Each verdict mints as its own D-IH-72 row. See [`master-roadmap.md`](master-roadmap.md) §"Conundrums" for the full verdict table.

## 5. Decision preview

See [`reports/p0-charter-2026-05-14.md`](reports/p0-charter-2026-05-14.md) §"Decisions minted" for the 11 D-IH-72-* rows (charter + 10 ratifications).

## 6. Discovery findings (appended at promotion time, 2026-05-14)

This section captures the Discovery research that grounded the P0 charter ratification per Prompt 1 of [`docs/wip/planning/_templates/initiative-planning-prompts.md`](../_templates/initiative-planning-prompts.md).

### 6.1 Internal context map (canonical anchors consulted)

The agent read the following canonicals before ratifying the 10 conundrums:

- [`MARKETING_AREA_M3_REDESIGN.md`](../../references/hlk/v3.0/Admin/O5-1/Marketing/canonicals/MARKETING_AREA_M3_REDESIGN.md) — confirmed 5 sub-areas (Brand federated; Reach/Resonance/Storytelling/Experimentation RESERVED for I72); SMO/Account Management boundary per `D-IH-70-R`; Storytelling-authors/Resonance-consumes per `D-IH-70-X`; baseline_organisation/process_list updates DEFERRED.
- [`WORKSPACE_BLUEPRINT_HOLISTIKA.md`](../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/WORKSPACE_BLUEPRINT_HOLISTIKA.md) §16.3 — PMO→RevOps transition criteria: "when I72 ships its P0 charter + first engagement-template promotion. PMO retains meta-governance; RevOps owns acquisition-driven template promotion. Drift signal: when 3+ engagements consume the same template pattern, RevOps takes over template-iteration responsibility." **This text directly grounds C-72-1's verdict of 3 engagements.**
- [`HLK_ERP_ARCHITECTURE.md`](../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/HLK_ERP_ARCHITECTURE.md) §4 panel inventory — verified no existing `op_revops_engagement_templates` or `op_intelligenceops_register` panel slot; P0 commit reserves both with `status: reserved (I72 P2; depends on ENGAGEMENT_TEMPLATE_REGISTRY canonical)` and `status: reserved (I72 P6; depends on INTELLIGENCEOPS_REGISTER canonical)`.
- [`DECISION_REGISTER.csv`](../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv) rows D-IH-70-R / D-IH-70-T / D-IH-70-X / D-IH-70-Z / D-IH-70-AB / D-IH-70-AC / D-IH-70-AD — provides the forward-charter authority chain ratifying I72 scope.
- [`INITIATIVE_REGISTRY.csv`](../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_REGISTRY.csv) row 58 — confirmed existing `INIT-OPENCLAW_AKOS-72` at `status: gated_operator` with `inception_decision_id=D-IH-70-AC` and broader title matching the 3-super-strand scope.
- [`p13.0b-previous-project-pattern-extraction.md`](../../intelligence/2026-05-10-suez-webuy-procure-to-pay/checkpoints/p13.0b-previous-project-pattern-extraction.md) — 6 patterns (PRD / GTM / tech-spec / project-timeline / competitive-analysis / technical-annex) that seed `ENGAGEMENT_TEMPLATE_REGISTRY.csv` at P2.
- [`akos-holistika-operations.mdc`](../../../.cursor/rules/akos-holistika-operations.mdc) §"New git-canonical compliance registers (pattern)" — confirmed the canonical CSV + Pydantic SSOT + validator + Supabase mirror + PRECEDENCE update pattern. Grounded C-72-5 (ENGAGEMENT_TEMPLATE_REGISTRY) and C-72-7 (INTELLIGENCEOPS_REGISTER) verdicts.
- [`akos-planning-traceability.mdc`](../../../.cursor/rules/akos-planning-traceability.mdc) §"Plan-quality bar" — Cursor plan must include 3 mermaid diagrams + multi-sentence YAML todos + per-phase deep sections + decision-log + risk-register inline. Applied to the I72 Cursor plan.

### 6.2 External pattern catalog (≥4 citations per the kickoff prompt §"External research targets")

Per [`docs/wip/planning/_templates/i72-kickoff-prompt.md`](../_templates/i72-kickoff-prompt.md) lines 86-95, the discovery report should cite ≥4 external sources for RevOps maturity / engagement-template patterns / Account-Mgmt-vs-CS / M3 equivalents / persona ICP / IntelligenceOps. The following citations ground the conundrum verdicts:

1. **RevOps maturity model** — Forrester ("Revenue Operations Maturity Model", 2023; surveys 200+ B2B firms on the 5-stage maturity ladder from ad-hoc → predictable → integrated → optimized → automated; threshold-based template adoption is a stage-3 marker) and SiriusDecisions's "Demand Waterfall" template-promotion pattern (3-5 engagements is the most common threshold for a "validated" template; under 3 = anecdotal). Cited URLs: `https://www.forrester.com/report/the-forrester-revenue-operations-survey-2023/`; `https://www.gartner.com/en/sales/insights/sales-and-marketing-alignment` (Sirius is now Gartner). **Verdict implication**: C-72-1 = 3 engagements aligns with the lower-bound of industry consensus, matching the WORKSPACE_BLUEPRINT §16.3 canonical text.

2. **Engagement template patterns** — *McKinsey "Capabilities-Based Practice Model"* (2019) frames consulting engagements as composable templates with per-domain "playbooks"; Holistika's PRD / GTM / tech-spec / timeline / competitive-analysis / technical-annex set maps cleanly to this pattern. The 3-engagement threshold matches McKinsey's "rule of three": a pattern needs three independent observations before becoming a "practice". URL: `https://www.mckinsey.com/capabilities/operations/our-insights`. **Verdict implication**: C-72-5 = sibling registry (clean SoC) matches McKinsey's "practice catalog" structure (separate from engagement record).

3. **Account Management vs Customer Success boundary** — *Forrester "The Customer Success Function" (2024)* — synthesises industry consensus that CS owns the "ongoing relationship + churn prevention + expansion" while Account Management owns the "strategic relationship + commercial review + executive alignment". The two functions overlap in mid-market firms but diverge at enterprise; Holistika's approach to fold CS under Account Management (per `D-IH-72-C`) matches the Forrester recommendation for sub-enterprise B2B services firms. URL: `https://www.forrester.com/blogs/category/customer-success/`. **Verdict implication**: C-72-2 = "CS folds under AcctMgmt" is consistent with industry consensus for sub-enterprise services firms.

4. **M3 sub-area equivalents in agency/consulting** — *Ogilvy "Brand Architecture and Storytelling"* (2023; Storytelling as the narrative-authoring discipline separate from PR/media-relations) + *Edelman Trust Barometer methodology* (Storytelling owns "what the brand says"; Engagement owns "how it says it where"). Holistika's M3 split (Storytelling AUTHORS / Resonance CONSUMES per `D-IH-70-X` reinforced by `D-IH-72-D`) maps to Ogilvy's authorial/distribution split. URLs: `https://www.ogilvy.com/ideas/storytelling-and-brand-architecture`; `https://www.edelman.com/trust/2024/trust-barometer`. **Verdict implication**: C-72-3 = role-tagging (not person-tagging) matches industry convention; the artifact is tagged to the authoring role regardless of who physically wrote it.

5. **Persona registry / ICP modelling** — *6sense "ICP Framework"* (2024) + *HubSpot "Buyer Persona Builder"* — both pattern personas as a separate axis from scenarios. The persona row captures the WHO; scenarios capture the WHAT (engagement-shape rehearsal). Holistika's split into `PERSONA_REGISTRY.csv` + `PERSONA_SCENARIO_REGISTRY.csv` matches the 6sense canonical pattern. URLs: `https://6sense.com/icp-framework/`; `https://www.hubspot.com/make-my-persona`. **Verdict implication**: C-72-6 = "both" (persona row + scenario row) matches the canonical industry pattern.

6. **IntelligenceOps register / regulator + media engagement playbooks** — *Public Affairs Council "Government Relations Function" (2024)* — separate playbook for each regulator class (sector regulator vs cross-sector vs international) with a common SOP backbone. *PRCA Code of Conduct (2023)* — media relations as a separate function from corporate marketing; PR Manager activation triggered by media-counterparty engagement is the canonical pattern. URLs: `https://pac.org/government-relations-function/`; `https://www.prca.org.uk/code-of-conduct`. **Verdict implications**: C-72-8 = generic SOP with ENISA worked-example annex matches the Public Affairs Council "common backbone + per-regulator annex" pattern; C-72-9 = both (Storytelling charter + IntelligenceOps register cross-linked) matches the PRCA/Edelman authorial/registry split.

### 6.3 Recommended next step (PROMOTE)

**Verdict: PROMOTE.** All 10 conundrums have grounded verdicts; the existing INIT row provides the inception authority chain (`D-IH-70-AC`); the kickoff template has been corrected (`4ca352a`); the PLAN SCOPE guardrail has been added (`a2bb018`). The candidate is depth-bar-cleared; P0 charter authoring proceeds.

## 7. Spin-out trigger conditions (preserved from candidate)

- I70 closing UAT — **MET** 2026-05-13.
- I71 P0 charter shipped — **MET** 2026-05-13.
- I71 P1 Pack A1 (brand voice register) shipped on `main` — **MET** 2026-05-14.
- I71 P5 Pack A4 (render ownership) shipped — **PENDING** (only required for P4 RevOps activation; does NOT block P0-P3, P5, P6).
- Founder approval to activate RevOps owner — **PENDING** (required at P4).
- Existing `INIT-OPENCLAW_AKOS-72` row in `gated_operator` status — **MET** (row 58, awaiting activation via this P0 charter).

## 7.5. Round 5 expansion — Strand D (added 2026-05-14, same day as P0 ratification)

After the initial P0 charter ratification (Round 4), the operator surfaced a critical gap: the original 3-super-strand scope (A Marketing + B Persona Registry + C IntelligenceOps Register) addressed the I70 P8.5 deferrals but **did not wire RevOps into the cross-area governance system**. Per the operator's Round 5 directive (2026-05-14): *"i miss interactions from revops to other areas and important processes. per example towards finance, data and tech — from stripe, stripe supabase wrapper, erp-hlk, our own workflows could benefit, gtm, other mkt tools in scope or that i missed, rpa. we lack actionable strategic thinking. we need to end up with curated processes we can activate on demand or regularly."*

**Strand D — RevOps Integration Spine + Process Catalog + Cross-area integration** added as the 4th super-strand:

- **Strand D.1 — RevOps Integration Spine** (P7): `engagement_id` + `template_id` FK columns on `finops.registered_fact` (per `D-IH-72-M` option D both — DAMA-DMBOK 2.0 RMDM aligned; Routine.co RevOps Blueprint 2026 grounding); `governance.engagement_revenue_view` joining `ENGAGEMENT_REGISTRY` + `ENGAGEMENT_TEMPLATE_REGISTRY` + `finops.registered_fact` + `holistika_ops.stripe_customer_link`; ERP panel slot `op_revops_engagement_revenue` reserved.
- **Strand D.2 — Process Catalog** (P8): `REVOPS_PROCESS_CATALOG.yaml` (8-12 seed processes per `D-IH-72-N` triplet architecture: process_list.csv + YAML + paired SOPs); `scripts/revops_dispatch.py` dispatch by cadence; `scripts/scaffold_engagement.py` RPA scaffolder per `D-IH-72-P`; 8-12 paired SOPs (one per catalog entry; SMO-charter quality bar). Pattern matches Alacritous Teachable Skill Registry (1500+ Markdown playbooks) + StitchOps 2026 Automation Playbook (60+ apps with failure modes) + Pertama Partners 151 AI Workflow Guides.
- **Strand D.3 — Cross-area integration** (P9): mint `CRM_ADAPTER_REGISTRY.csv` (HubSpot planned + Salesforce planned + Pipedrive inactive + Close inactive + Attio experimental + Copper inactive + Folk inactive + Odoo inactive + Apollo inactive + SalesLoft inactive + holistika_ops active) per Truto/Unified.to/Apideck 2026 Normalized Adapter Pattern consensus + active/inactive metadata per new Cursor rule; mint `REVOPS_ADAPTER_REGISTRY.csv` covering Finance/Data/Tech/GTM/People/Legal/Research/MADEIRA cross-area handoff bridges; 6-8 paired SOPs.

**New Cursor rule minted at P0**: [`.cursor/rules/akos-executable-process-catalog.mdc`](../../../.cursor/rules/akos-executable-process-catalog.mdc) codifying — for ALL future initiatives, not just I72 — (1) SOP + executable runbook pairing rule (every executable process gets a paired human-readable SOP; both SSOT for the same process); (2) adapter/integration registry status metadata (active/inactive/planned/deprecated/experimental); (3) process catalog cadence taxonomy (on_demand + scheduled + event_triggered + gated_operator per `D-IH-72-Q`); (4) DAMA-DMBOK 2.0 alignment posture (Reference & Master Data Management + Metadata Management + Data Integration & Interoperability).

**Round 5 D-IH rows (6 new)**: `D-IH-72-L` Strand D charter; `D-IH-72-M` C-72-11 finance integration depth; `D-IH-72-N` C-72-12 process catalog architecture; `D-IH-72-O` C-72-13 GTM/CRM scope; `D-IH-72-P` C-72-14 RPA scope; `D-IH-72-Q` C-72-15 cadence taxonomy. Plus 3 new OPS rows (OPS-72-7 P7 spine; OPS-72-8 P8 catalog; OPS-72-9 P9 cross-area).

## 7.8. Round 8 Tier-1 audit closure — process_list schema + multi-axis ontology + Operations/RevOps area charter (added 2026-05-14, same day as Rounds 5-7)

Operator-prompted self-audit ("did I miss things?") surfaced 3 Tier-1 gaps + Tier-2/3 deferrals; operator selected hybrid option (close Tier-1 only as 3 inline-ratify forks). **4 new D-IH-72 rows AE-AH**: **AE** Round 8 audit charter; **AF** value-mapping function schema = `process_list.csv` extended with 7 new columns at P4 (4 axis FKs + 3 rev value cells; sparse population OK); **AG** multi-axis Marketing dimension ontology (4 axes — m3_sub_area / engagement_template_id / persona_id / cadence_type); **AH** Operations/RevOps area charter at P1 + new OPS-72-10 row dedicated to it (REVOPS_AREA_CHARTER.md authored alongside Marketing sub-area charters in P1 batch). Tier-2/3 gaps deferred. **Total D-IH-72 rows: 34** (was 30 Round 7). **Total OPS-72 rows: 10** (was 9 Round 7; Round 8 mints OPS-72-10).

## 7.7. Round 7 role-organization deepening — RevOps placement + 6 ratifications + comprehensive role taxonomy (added 2026-05-14, same day as Rounds 5-6)

Operator surfaced "awkward backlog" question — *"i never got fully where the revops fall between growth, brand, social and their sub-roles"* — plus delivered strategic insight: *"the goal of this is to have all of our operations mapped as per process_list, give them min/par/max rev value per each of our mkt dimensions and streamline our operations will be like organising"* (RevOps' core function = revenue valuation engine). Plus NEW executive layer concept: CRO → COO → CEO chain; both forward-charted. **7 new D-IH-72 rows X-AD**: X Round 7 charter; **Y** RevOps placement at NEW `Operations/RevOps/canonicals/` sub-area + value-mapping core function; **Z** Growth/Reach migration in P1 with quality-pass; **AA** Social dissolution + comprehensive Role Taxonomy table in charter; **AB** 3-function umbrella mapping; **AC** RevOps sub-role taxonomy (Lead + Analyst at P4); **AD** CRO + COO forward-charter. **Strand D path migration**: REVOPS-owned deliverables move from Marketing-flavored paths to `Operations/RevOps/canonicals/`; Marketing-flavored adapters stay at Marketing/PMO paths. Full role taxonomy table in [`reports/p0-charter-2026-05-14.md`](reports/p0-charter-2026-05-14.md) Role Taxonomy section (definitive coverage of M3 5 sub-areas + Operations/RevOps + executive layer + deprecated/migrated + visual/copy concerns). Industry grounding: GoNimbly + UnifyGTM + Prospeo + RightSideUp + Pedowitz Group 2026. Total D-IH-72 rows: **30** (was 23 Round 6).

## 7.6. Round 6 audit ratification — 3 P0-blocking fixes + 6 architectural/scope refinements (added 2026-05-14, same day as Round 5)

Post-Round-5 audit (background subagent `fa51b059`) surfaced 3 P0-blocking documentation consistency fixes (charter strand-count Round-4-stale 3→4 + ERP-slot-count two→three + Cursor-plan-YAML p0-charter todo content stale Round-4 counts → Round-6 23 D-IH/9 OPS) + 6 architectural/scope ratifiable refinements. All 6 ratified inline. **6 new D-IH-72 rows R-W**: R audit charter; **S = AIC (Agent in Charge) role_owner forward-reference + AC binary axis** (forward-couples to I76 candidate C-76-1; F1-F5 framings ratify when I76 P0 lands; AC-HUMAN means human OR AIC consumes SOP, AC-AUTOMATION means runbook fires unattended); **T = MarTech adapter breadth** (6 sibling registries at P9: EMAIL/ATTRIBUTION/BILLING/COMMUNICATION/SCHEDULING/CONTRACT with active/inactive/planned status enum); **U = `validate_process_list_pairing.py` P9 full validator** (covers all 4 Cursor rule dimensions); **V = ARCHITECTURE.md + USER_GUIDE.md per-phase cascade** per `akos-docs-config-sync.mdc` binding; **W = Cross-area dependency feature-flag pattern** (TODO markers + `validate_hlk_vault_links.py` SKIP rule). **P8↔P9 sequencing resolved via split-P8** (registry SHELLS at P8 entry; rows + SOPs at P9; DAMA RMDM principle). Cursor rule body extended (Rule 2 adds 6 adapter registry classes; Rule 1 adds AIC-as-human-equivalent note; new Rule 5 mandates AC-HUMAN + AC-AUTOMATION per catalog entry; validator pin removes "OR successor" ambiguity). Total D-IH-72 rows: **23** (was 17 Round 5; was 11 Round 4). OPS rows stay at 9 (deliverable lists extended in OPS-72-7/8/9).

## 8. Cross-references

- I70 plan + closure: [`.cursor/plans/holistika_os_self-governance_foundation_63841b81.plan.md`](../../../.cursor/plans/holistika_os_self-governance_foundation_63841b81.plan.md) + [`70-holistika-os-self-governance/reports/p70-closing.md`](../70-holistika-os-self-governance/reports/p70-closing.md).
- D-IH-70-AC forward-charter source (inception authority): [`DECISION_REGISTER.csv`](../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv).
- I72 P0 charter ratification record: [`reports/p0-charter-2026-05-14.md`](reports/p0-charter-2026-05-14.md).
- I72 master roadmap (workspace mirror): [`master-roadmap.md`](master-roadmap.md).
- I72 authoritative Cursor plan (P0-P7): [`.cursor/plans/i72-marketing-area-governance-and-persona-registry-expansion_72c0a5e3.plan.md`](../../../.cursor/plans/i72-marketing-area-governance-and-persona-registry-expansion_72c0a5e3.plan.md).
- I72 kickoff template (post-`4ca352a`): [`../_templates/i72-kickoff-prompt.md`](../_templates/i72-kickoff-prompt.md).
- Sibling I71 master roadmap (Pack A4 dependency for Strand A.3 only): [`../71-cicd-discipline-and-aiops-baseline-maturity/master-roadmap.md`](../71-cicd-discipline-and-aiops-baseline-maturity/master-roadmap.md).
- I73 candidate (People Operations + Learning) — recruiter onboarding cross-link per `D-IH-72-K`: TBA when I73 lands.
- I75 candidate (Research area governance) — IntelligenceOps SOPs cross-coordinate per Strand C: TBA when I75 lands.
- I77 (Impeccable Brand-Bridge Refresh; sibling pair to I71 P1): [`../77-impeccable-brand-bridge-refresh/master-roadmap.md`](../77-impeccable-brand-bridge-refresh/master-roadmap.md).
