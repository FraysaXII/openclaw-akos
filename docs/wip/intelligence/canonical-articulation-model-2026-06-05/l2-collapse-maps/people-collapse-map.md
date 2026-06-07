---
intellectual_kind: capability_collapse_map
parent_initiative: INIT-OPENCLAW_AKOS-95
lane: L2 — Capability de-densify (R2-01) — per-area collapse map
area: People
authored: 2026-06-08
status: proposed
ratified_decision: D-IH-95-H   # keep-separate + de-densify (process-shadow → stable map)
language: en
audience: J-OP;J-AIC
register: internal   # docs/wip/intelligence/ — internal register permitted (CORPINT method terms allowed)
control_confidence_level: Euclid
method_source: docs/wip/intelligence/canonical-articulation-model-2026-06-05/l2-capability-densify-findings-2026-06-07.md
source_registry: docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/CAPABILITY_REGISTRY.csv
eviction_registry: docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/COMPONENT_PRIMITIVE_REGISTRY.csv
collapse: 93 -> 22 (+2 evicted)
note: >
  First per-area worked example of the L2 capability de-densify. Readonly research +
  one doc write. Proposes the stable People capability map; does NOT modify any canonical
  CSV (the 93→22 rewrite of CAPABILITY_REGISTRY is a gated canonical-CSV change requiring
  operator approval per akos-baseline-governance.mdc). Every one of the 93 People
  process-shadow rows is accounted for below (rolled up or evicted).
---

# L2 collapse map — People area (93 → 22)

> **One-line result:** The 93 People rows in `CAPABILITY_REGISTRY.csv` are a 1:1
> process-shadow (seeded `CAP-`+`process` id per D-IH-82-P). They collapse to **22 stable,
> bearer-agnostic People capabilities** — 91 rows roll up, 2 are evicted as mis-seeded
> non-capabilities. De-densification ratio ≈ **4.2 : 1**. Confidence: **Euclid** (direction
> settled by D-IH-95-H; the residual uncertainty is the legacy-methodology fold in §3, which
> is flagged for operator confirmation, not asserted).

This is the first per-area application of the 6-step collapse method ratified in the
[L2 method doc](../l2-capability-densify-findings-2026-06-07.md) §3.2 (D-IH-95-H). It inherits
that doc's external research base (capability-map sizing 40–100 / L1 7–10 / noun-gerund naming /
technology-neutral / differentiating-vs-utility tiering — [E-2][E-3][E-16][E-17][E-19][E-22]
there); the framing here is an **application**, not a novel position, so no new external sweep is
required per `akos-applied-research-discipline.mdc` RULE 2.

## Method recap (how this map was built)

1. **Strip non-capabilities (evict).** The L2 eviction target `COMPONENT_PRIMITIVE_REGISTRY.csv`
   holds *deliverable/UI* primitives (cover page, hook, CTA, evidence block…), **not** a
   code-symbol dump. People has **no** code symbols (unlike MADEIRA), so it yields **zero**
   `COMPONENT_PRIMITIVE` evictions; only 2 technology-named mis-seeds are evicted (§3).
2. **Normalize to (area, theme).** Projected each row onto `(People, theme)` using
   `role_owner` + the originating `process` id family (`gtm_team_dtp_*`, `gtm_cl_*`,
   `hol_peopl_dtp_*`, `tbi_peopl_dtp_*`).
3. **Merge across entity/convention.** Collapsed the `CAP-GTM-*` / `CAP-HOL-*` / `CAP-THI-*` /
   `CAP-TBI-*` variants of the same ability into one bearer-agnostic capability.
4. **Name as nouns/gerunds, outcome-oriented, technology-neutral.** Each gets a one-sentence
   definition.
5. **Assign L1 domain + tier.** Grouped under the 9 enterprise L1 domains (16 land in
   *People, Org Design & Quality Fabric*; 6 have a different primary domain — see §4). Tagged
   each `differentiating` vs `utility`.
6. **Wire, don't copy.** Each capability lists the originating `process` ids it is realized by
   (TRP-006, now N:N) in §2 — the *how* stays in `process_list.csv`.

## Section 1 — Proposed capabilities (the stable map)

`proposed_capability_id` matches `^CAP-[A-Z0-9-]+$`. `L1_domain` is one of the 9 enterprise
strategy domains. `capability_tier` ∈ {differentiating, utility}.

| # | proposed_capability_id | capability_name | L1_domain | capability_tier | definition |
|:--|:--|:--|:--|:--|:--|
| 1 | CAP-TALENT-ACQUISITION | Talent Acquisition & Candidate Assessment | People, Org Design & Quality Fabric | utility | Sourcing, interviewing, and assessing internal hires and recruiters against role-fit criteria. |
| 2 | CAP-TALENT-ONBOARDING | Talent Onboarding & Enablement | People, Org Design & Quality Fabric | utility | Bringing new operators, cohorts, and external collaborators to productive capability via structured onboarding kits and the four-wall induction flow. |
| 3 | CAP-WORKFORCE-PLANNING | Workforce Planning & Role-Fit Design | People, Org Design & Quality Fabric | differentiating | Mapping required abilities onto the org chart, finding capability gaps, and prioritising role demand by phase and area strategy. |
| 4 | CAP-CAREER-PATHWAYS | Career Pathway & Progression Design | People, Org Design & Quality Fabric | utility | Designing role-based progression paths from current ability toward internal capability objectives. |
| 5 | CAP-LEARNING-DEVELOPMENT | Learning, Training & Curriculum Development | People, Org Design & Quality Fabric | differentiating | Building and coaching curricula that move people and apprentices from training to billable output, including formation-time estimation. |
| 6 | CAP-EXTERNAL-COLLABORATOR-MGMT | External / Outsourced Collaborator Sourcing & Engagement | People, Org Design & Quality Fabric | utility | Sourcing, comparing, contracting, and integrating freelance/outsourced collaborators, including SOC review and market-rate fit. |
| 7 | CAP-ACCESS-PROVISIONING | Workforce Access Provisioning & Security Tiering | People, Org Design & Quality Fabric | utility | Assigning tools, profiles, and security tiers to people by engagement and buyer sensitivity. |
| 8 | CAP-COMPENSATION-SETTLEMENT | Compensation, Payroll & Collaborator Settlement | Finance & Revenue Operations | utility | Running payroll, budget allocation, percentage-collaborator payouts, and collaborator-share settlement. |
| 9 | CAP-ENGAGEMENT-MODEL-GOVERNANCE | Engagement Model Governance & Intake Classification | Delivery & Client Engagement Operations | differentiating | Maintaining the engagement-model registry and classifying/routing each engagement at intake, including investor-advisor rounds. |
| 10 | CAP-CANONICAL-GOVERNANCE | Canonical Registry & Decision-Ratification Governance | People, Org Design & Quality Fabric | differentiating | Auditing canonical registries and ratifying decisions/policies that keep the governance SSOT trustworthy. |
| 11 | CAP-KNOWLEDGE-REGISTER-STEWARDSHIP | Knowledge & Source Register Stewardship | Corporate Intelligence & Research | differentiating | Stewarding knowledge/source registers (GOI/POI) and redacting adviser transcripts to access tier. |
| 12 | CAP-REGULATORY-READINESS | Regulatory Readiness & Evidence Packs | Legal, Compliance & Privacy | utility | Assembling regulatory readiness and evidence packs (e.g. ENISA) for external attestation. |
| 13 | CAP-COMPLIANCE-AUTOMATION | Compliance Workflow Automation | Legal, Compliance & Privacy | utility | Automating recurring compliance workflows end-to-end. |
| 14 | CAP-ETHICS-GOVERNANCE | Ethics & Responsible-AI Review | People, Org Design & Quality Fabric | differentiating | Reviewing ethical and responsible-AI boundaries, AI-overreach claims, and the allies/neutrals/enemies stakeholder-ethics frame. |
| 15 | CAP-PRECOMMIT-SYNTHESIS-DISCIPLINE | Pre-Commit Synthesis & Tranche Quality Discipline | People, Org Design & Quality Fabric | differentiating | Running tranche-level synthesis, charter authoring, closing-loop test design, and finding-disposition before any commit. |
| 16 | CAP-CLOSURE-ASSURANCE-GOVERNANCE | Closure Assurance & Verdict Governance | People, Org Design & Quality Fabric | differentiating | Enforcing the closure-UAT quality bar and PASS-WITH-FOLLOWUP rationale discipline at wave/initiative close. |
| 17 | CAP-REGRESSION-INDEX-ASSURANCE | Baseline Regression & Index-Integrity Assurance | People, Org Design & Quality Fabric | differentiating | Running inter-wave regression and baseline-index integrity sweeps to catch drift across the knowledge base. |
| 18 | CAP-EXPERIENCE-UX-QUALITY | Experience & UX Quality Design | People, Org Design & Quality Fabric | differentiating | Conducting UX research and the experience quality bar, including ERP-engagement-governance surface design. |
| 19 | CAP-CAPABILITY-CONFIDENCE-STEWARDSHIP | Capability-Map Confidence Stewardship | People, Org Design & Quality Fabric | differentiating | Rating and maintaining per-capability confidence across the de-densified capability map on a recurring cadence. |
| 20 | CAP-DESIGN-PATTERN-STEWARDSHIP | People Design-Pattern & Cross-Area Breakthrough Stewardship | People, Org Design & Quality Fabric | differentiating | Minting cross-area design patterns and propagating breakthroughs (incl. stakeholder-lenses review) to consuming areas. |
| 21 | CAP-AGENTIC-OPERATIONS | Agentic Operations & AIC Lifecycle Stewardship | Applied AI & MADEIRA | differentiating | Running the agentic operating cadence and stewarding AIC execution and per-task dispatch across the capability lifecycle. |
| 22 | CAP-DELIVERY-METHODOLOGY-STEWARDSHIP | Proprietary Delivery & Engagement Methodology Stewardship | People, Org Design & Quality Fabric | utility | Curating Holistika's proprietary delivery/engagement method primitives (four-wall, arrowhead, conceptualise→signify, tale-to-morale-to-analogy, root-cause/regression technique). |

## Section 2 — Rollup (which old rows realize each capability)

Each proposed capability lists the old `CAPABILITY_REGISTRY` rows it absorbs, by source
`process` id family. These ids become the N:N `originating_process_ids` (TRP-006) on the new
capability — the *how* stays in `process_list.csv`; the capability row carries only the stable
*what*. **91 of 93 rows roll up here; the remaining 2 are evicted in §3.**

| proposed_capability_id | absorbs (old capability rows → originating process ids) | n |
|:--|:--|:--|
| CAP-TALENT-ACQUISITION | B2E Candidate Interview (`thi_peopl_dtp_98`); Recruiter onboarding brief (`tbi_peopl_dtp_recruiter_onboarding_001`) | 2 |
| CAP-TALENT-ONBOARDING | Employee Onboarding Kit (`hol_peopl_dtp_284`); Operator & Cohort Onboarding Cycle (`hol_peopl_dtp_314`); 4th Wall Phases (`hol_peopl_dtp_147`); flujo cuarta pared onboarding (`gtm_team_dtp_1`); categorizar doc por role (`gtm_team_dtp_2`); categorizar info admin externos (`gtm_team_dtp_3`); investigación hacia cliente onboarding (`gtm_team_dtp_5`); carpeta de onboarding (`gtm_team_dtp_21`) | 8 |
| CAP-WORKFORCE-PLANNING | Team growth (`gtm_cl_04ec26ad9a99ef`); role-fit roles prioritarios (`gtm_cl_2ae952ae94b393`); role-fit hijack externos (`gtm_cl_98d7a76562651a`); capacidades faltantes del mapa (`gtm_team_dtp_11`); priorizar por fases G2M (`gtm_team_dtp_12`); prioridades por áreas (`gtm_team_dtp_13`); huecos de capacidades (`gtm_team_dtp_25`) | 7 |
| CAP-CAREER-PATHWAYS | Career planning (`gtm_cl_38e95efc220bcd`); plan de carrera por rol (`gtm_team_dtp_23`); plan de carrera (`gtm_team_dtp_26`) | 3 |
| CAP-LEARNING-DEVELOPMENT | estimar tiempos formación→producción (`gtm_cl_0730efdd3b8cab`); estandarizar fases nuevas entradas (`gtm_cl_1cd52c451097c9`); research/ofimática para output (`gtm_cl_1e813f8c8570a5`); estimar tiempos de formación (`gtm_team_dtp_4`); procesos de formación y output (`gtm_team_dtp_24`); Curriculum Drafting & Methodology Coaching (`hol_peopl_dtp_313`); Consult Hard-Skillers for Estimation (`thi_peopl_dtp_131`); Apprentice curriculum assignment (`tbi_peopl_dtp_apprentice_curriculum_assignment_001`) | 8 |
| CAP-EXTERNAL-COLLABORATOR-MGMT | ETL info a proyectos (`gtm_team_dtp_6`); comparar perfiles fiverr (`gtm_team_dtp_7`); separar responsabilidad org externa (`gtm_team_dtp_10`); investigación Vinc precio/calidad (`gtm_team_dtp_14`); ETL externos/clientes (`gtm_team_dtp_15`); negociar estilo de trabajo (`gtm_team_dtp_16`); acordar entregables (`gtm_team_dtp_17`); reunión a quién contratar fiverr (`gtm_team_dtp_18`); excel de perfiles fiverr (`gtm_team_dtp_19`); Outsourced helper SOC review (`tbi_peopl_dtp_outsourced_helper_soc_review_001`) | 10 |
| CAP-ACCESS-PROVISIONING | niveles de seguridad por buyer (`gtm_team_dtp_8`); herramientas de acceso (`gtm_team_dtp_9`); accesos y perfiles (`gtm_team_dtp_22`) | 3 |
| CAP-COMPENSATION-SETTLEMENT | reparto de presupuesto (`gtm_team_dtp_20`); Payroll Cycle Operations (`hol_peopl_dtp_315`); Percentage collaborator payout reconciliation (`tbi_peopl_dtp_percentage_collaborator_payout_001`); Collaborator share kit + settlement (`hol_peopl_dtp_collaborator_share_001`) | 4 |
| CAP-ENGAGEMENT-MODEL-GOVERNANCE | Engagement Model Registry maintenance (`tbi_peopl_dtp_engagement_model_registry_mtnce_001`); Per-engagement classification at intake (`tbi_peopl_dtp_engagement_model_classification_001`); Engagement lifecycle routing at intake (`tbi_peopl_dtp_engagement_lifecycle_routing_001`); Investor advisor round review (`tbi_peopl_dtp_investor_advisor_round_review_001`) | 4 |
| CAP-CANONICAL-GOVERNANCE | Canonical Registry Audit Cycle (`hol_peopl_dtp_310`); DECISION_REGISTER Ratification Review (`hol_peopl_dtp_311`); Apply Policy Framework (`hol_peopl_dtp_101`); Rant Policy (`hol_peopl_dtp_102`) | 4 |
| CAP-KNOWLEDGE-REGISTER-STEWARDSHIP | GOI/POI register maintenance (`hol_peopl_dtp_303`); Adviser transcript redaction (`hol_peopl_dtp_304`) | 2 |
| CAP-REGULATORY-READINESS | ENISA Readiness and Evidence Pack (`hol_peopl_dtp_302`) | 1 |
| CAP-COMPLIANCE-AUTOMATION | FlowMaker Compliance Automation (`SOP-FLOWMAKER_COMPLIANCE_AUTOMATION_003`) | 1 |
| CAP-ETHICS-GOVERNANCE | Allies, Neutrals & Enemies — NPS+CORPINT ethics frame (`hol_peopl_dtp_139`); AI-Overreach Claim Review (`hol_peopl_dtp_312`); Quarterly Ethics & Learning co-review (`hol_peopl_dtp_316`); Agentic ethics boundaries review (`tbi_peopl_dtp_agentic_ethics_boundaries_001`) | 4 |
| CAP-PRECOMMIT-SYNTHESIS-DISCIPLINE | Synthesis before tranche; Tranche charter authoring; Closing-loop test design; Disposition via inline-ratify enum (all 4 → `hol_peopl_dtp_synthesis_before_tranche_001`) | 4 |
| CAP-CLOSURE-ASSURANCE-GOVERNANCE | UAT governance bar enforcement (`hol_peopl_dtp_uat_governance_001`); PASS-WITH-FOLLOWUP rationale authoring (`hol_peopl_dtp_pwf_governance_001`) | 2 |
| CAP-REGRESSION-INDEX-ASSURANCE | Inter-wave regression sweep (`hol_peopl_dtp_inter_wave_regression_001`); Baseline index integrity sweep (`hol_peopl_dtp_index_integrity_001`) | 2 |
| CAP-EXPERIENCE-UX-QUALITY | UX research + quality bar (`hol_peopl_dtp_ux_research_001`); ERP-engagement-governance UX design (`hol_peopl_dtp_synthesis_before_tranche_001`) | 2 |
| CAP-CAPABILITY-CONFIDENCE-STEWARDSHIP | Per-capability confidence rating review (`hol_peopl_talent_h_capability_confidence_001`) | 1 |
| CAP-DESIGN-PATTERN-STEWARDSHIP | People cross-area breakthrough propagation (`tbi_peopl_dtp_cross_area_breakthrough_001`); Stakeholder lenses canonical review (`tbi_peopl_dtp_stakeholder_lenses_review_001`) | 2 |
| CAP-AGENTIC-OPERATIONS | People agentic operations cadence (`tbi_peopl_dtp_agentic_ops_mtnce_001`); AIC capability execution & lifecycle stewardship (`hol_peopl_talent_a_capability_execution_001`); Per-task AIC dispatcher routing (`hol_peopl_talent_a_aic_dispatcher_001`) | 3 |
| CAP-DELIVERY-METHODOLOGY-STEWARDSHIP | Isolate Concept (`hol_peopl_dtp_104`); Declare Signifier (`hol_peopl_dtp_105`); Regression Definition & Techniques (`hol_peopl_dtp_106`); Design MO (`thi_peopl_dtp_111`); Sell (`hol_peopl_dtp_115`); Normalize (`hol_peopl_dtp_116`); Pacify (`hol_peopl_dtp_117`); Engage — Holistika Project Lifecycle (`hol_peopl_dtp_118`); Hijack (`hol_peopl_dtp_119`); Arrowhead Strategy (`hol_peopl_dtp_140`); Conceptualize (`hol_peopl_dtp_141`); Output 1 Framework Design (`hol_peopl_dtp_158`); Tale to Morale to Analogy (`hol_peopl_dtp_159`); Root Cause Analysis (`hol_peopl_dtp_160`) | 14 |
| **Rolled-up subtotal** | | **91** |

> **N:N note (TRP-006):** `hol_peopl_dtp_synthesis_before_tranche_001` realizes **two** proposed
> capabilities (CAP-PRECOMMIT-SYNTHESIS-DISCIPLINE + CAP-EXPERIENCE-UX-QUALITY) — exactly the
> many-to-many the de-densify is designed to express (5 seeded `…METHOD-*` capability rows
> against 1 process). This is impossible in a fused single-table model and is the worked proof
> of the keep-separate decision (L2 §1.3).

## Section 3 — Evictions (rows that are NOT People capabilities)

| old capability_id | name | originating process | disposition | rationale |
|:--|:--|:--|:--|:--|
| CAP-HOL-PEOPL-DTP-114 | Terraform | `hol_peopl_dtp_114` | **EVICT** — not a capability | Technology/tool name (infrastructure-as-code). Naming a capability after a system "tells the enterprise nothing" (L2 [E-19]). If a real dependency, it belongs in `SUBSTRATE_REGISTRY` / component-service matrix — **not** People capabilities, and **not** `COMPONENT_PRIMITIVE_REGISTRY` (which holds deliverable/UI primitives only). |
| CAP-HOL-PEOPL-DTP-157 | CUDA Framework | `hol_peopl_dtp_157` | **EVICT** — not a capability | Technology/vendor framework name. Same rationale as Terraform — substrate, not a People ability. |

**Why only 2 evictions (and none to `COMPONENT_PRIMITIVE_REGISTRY`):** the L2 method's
`COMPONENT_PRIMITIVE_REGISTRY` eviction channel exists for *code symbols* (MADEIRA's
`LLMConfig`, `Sentiment Analyzer`, etc.). The People area has no code symbols. Its only
non-capabilities are two technology-named rows, which are substrate, so they are dropped from
the capability registry rather than re-homed in the deliverable-primitive registry.

> **Eviction-vs-fold flag (operator confirmation needed):** CAP-DELIVERY-METHODOLOGY-STEWARDSHIP
> (§1 #22) is a **holding capability** for 14 legacy `hol_peopl_dtp_101–160` / `thi_peopl_dtp_111`
> rows that read like the *previous-project example-only* R&L corpus (single-verb / concept-fragment
> names: Sell, Normalize, Pacify, Hijack, Conceptualize…). They are **folded, not evicted**, on the
> conservative L2 rule "task-grain micro-steps stay as realizing processes, not capabilities."
> Some may be genuine proprietary-method primitives (four-wall, arrowhead, CORPINT engagement
> phases — internal register per `akos-brand-baseline-reality.mdc`); others may be noise. **This is
> the one residual judgment in this map** — surfaced for operator inline-ratify (keep-as-one /
> split / evict-subset), not asserted.

## Section 4 — Cross-area flags

Capabilities **seeded under the People area** whose stable strategy-layer home is another L1
domain, or which carry shared ownership. Capabilities are org-agnostic (L2 [E-2][E-3]); the
*area* a row was seeded in does not bind its *domain*. Flags below drive future cross-area dedup
(e.g. a Finance collapse map may already hold the settlement ability).

| proposed_capability_id | primary L1_domain | cross-area flag | governing doctrine |
|:--|:--|:--|:--|
| CAP-COMPENSATION-SETTLEMENT | Finance & Revenue Operations | People owns people-side comp policy; **Finance owns ledger + reconciliation**; collaborator-share settlement overlaps the collaborator-share discipline. | `akos-finance-ops.mdc`; `akos-collaborator-share.mdc` |
| CAP-ENGAGEMENT-MODEL-GOVERNANCE | Delivery & Client Engagement Operations | **People mints the engagement-model registry pattern** (People-as-DoD RULE 1); Delivery/Client-Engagement consumes it at intake. Shared owner. | `akos-people-discipline-of-disciplines.mdc` RULE 1 |
| CAP-KNOWLEDGE-REGISTER-STEWARDSHIP | Corporate Intelligence & Research | GOI/POI is the CORPINT knowledge dimension; **People/Compliance stewards** the register; Legal owns transcript-redaction policy. | `akos-research-area.mdc`; `akos-adviser-engagement.mdc` |
| CAP-REGULATORY-READINESS | Legal, Compliance & Privacy | ENISA evidence is a Legal/Privacy attestation; **People/Compliance assembles** the pack. | `akos-baseline-governance.mdc` (HLK compliance) |
| CAP-COMPLIANCE-AUTOMATION | Legal, Compliance & Privacy | Compliance owns the workflow; **Tech Lab builds** the automation (FlowMaker). | `akos-holistika-operations.mdc` |
| CAP-AGENTIC-OPERATIONS | Applied AI & MADEIRA | AIC execution + per-task dispatch is MADEIRA's; **People owns the agentic doctrine + cadence** (People-as-DoD RULE 3); Tech Lab owns infra. | `akos-people-discipline-of-disciplines.mdc` RULE 3; `akos-aic-delegation.mdc` |
| CAP-ACCESS-PROVISIONING | People, Org Design & Quality Fabric | People sets people-side tiers; **Tech Lab / System Owner owns** the access-control implementation + buyer-security model. | `akos-holistika-operations.mdc` (SOC) |
| CAP-EXTERNAL-COLLABORATOR-MGMT | People, Org Design & Quality Fabric | People sources/contracts; **Delivery scopes deliverables; Finance sets market-rate/budget; CORPINT (Vinc) supplies vendor intel.** | `akos-collaborator-share.mdc` |
| CAP-EXPERIENCE-UX-QUALITY | People, Org Design & Quality Fabric | People owns the UX quality bar; **Marketing/Brand owns brand surfaces; Tech Lab builds.** | `akos-quality-fabric.mdc` |
| CAP-DELIVERY-METHODOLOGY-STEWARDSHIP | People, Org Design & Quality Fabric | Engagement-phase method terms (engage/pacify/hijack, allies-neutrals-enemies) overlap **Research/CORPINT methodology**; internal register only. | `akos-brand-baseline-reality.mdc`; `akos-research-area.mdc` |

The other **12** capabilities (CAP-TALENT-ACQUISITION, -ONBOARDING, -WORKFORCE-PLANNING,
-CAREER-PATHWAYS, -LEARNING-DEVELOPMENT, -CANONICAL-GOVERNANCE, -ETHICS-GOVERNANCE,
-PRECOMMIT-SYNTHESIS-DISCIPLINE, -CLOSURE-ASSURANCE-GOVERNANCE, -REGRESSION-INDEX-ASSURANCE,
-CAPABILITY-CONFIDENCE-STEWARDSHIP, -DESIGN-PATTERN-STEWARDSHIP) are **cleanly People-domain**,
no cross-area pull.

## Section 5 — Count summary (93 → 22)

| Metric | Value |
|:--|:--|
| Source rows (`CAPABILITY_REGISTRY.csv`, `area=People`) | **93** |
| Rolled up into stable capabilities (§2) | 91 |
| Evicted as non-capabilities (§3) | 2 |
| **Proposed stable capabilities** | **22** |
| De-densification ratio | ≈ **4.2 : 1** (91 ÷ 22) |
| Reconciliation | 91 rolled + 2 evicted = **93** ✓ (every old row accounted for) |
| Tier split | 13 differentiating · 9 utility |
| L1-domain split | 16 *People, Org Design & Quality Fabric* · 2 *Legal, Compliance & Privacy* · 1 each *Finance & Revenue Ops* / *Delivery & Client Engagement Ops* / *Corporate Intelligence & Research* / *Applied AI & MADEIRA* |
| `COMPONENT_PRIMITIVE_REGISTRY` evictions | **0** (no code symbols in People) |

**Sizing sanity (L2 [E-17]):** 22 capabilities for the People steward area is organic — People
is the "discipline of disciplines," so it legitimately carries more abilities than a stream-aligned
area, while staying well inside the strategic band (the enterprise target is ~60–110 across the 9
L1 domains). The 16 People-domain capabilities are the area's own; the 6 cross-domain ones (§4)
are candidates for relocation/shared-ownership when the Finance / Delivery / Legal / CorpIntel /
Applied-AI collapse maps are built.

## Cross-references

- **Method** (the WHAT this applies): [`l2-capability-densify-findings-2026-06-07.md`](../l2-capability-densify-findings-2026-06-07.md) §3.2 (6-step collapse), ratified **D-IH-95-H**.
- **Source registry**: [`CAPABILITY_REGISTRY.csv`](../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/CAPABILITY_REGISTRY.csv) (`area=People`, 93 rows).
- **Eviction registry inspected**: [`COMPONENT_PRIMITIVE_REGISTRY.csv`](../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/COMPONENT_PRIMITIVE_REGISTRY.csv) (deliverable/UI primitives; 0 People evictions).
- **Governing rules**: `akos-people-discipline-of-disciplines.mdc` (People-as-DoD ownership), `akos-quality-fabric.mdc` (the Quality-Fabric capabilities #15–20), `akos-baseline-governance.mdc` (the 93→22 rewrite is a **gated canonical-CSV change** — this doc is a proposal only).
- **Open gate for execution**: the legacy-methodology fold (§3 flag) + the 6 cross-domain relocations (§4) are inline-ratify decisions when L2 executes the canonical-CSV tranche.
