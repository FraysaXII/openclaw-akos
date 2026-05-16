---
candidate_id: I81
title: Full-vault SOP body/addendum retrofit (DAMA-readiness scale-out)
status: candidate
authored: 2026-05-16
last_review: 2026-05-16
parent_initiative: 80 (I79 lessons-learned, P5+P6 forward-charter)
priority: 4
language: en
---

# I81 candidate — Full-vault SOP body/addendum retrofit

> **Candidate scaffold authored at I80 P6 per `D-IH-80-D` Option C forward-charter.** Promoted to `active` when (a) operator confirms the I80 paired-file pattern lands well across the 7 pilot pairs (2 from P4 + 5 from P5; ratification window: rolling), and (b) at least one I81 strand has a clear next-quarter execution priority (e.g., a hiring cohort that needs the People Operations addenda fully read; a Tech Lab framework refresh that needs the System Owner SOP addenda; a brand canon update that needs the Marketing addenda). The forward-charter language is deliberately *non-time-pressured*: full-vault retrofit can run as **a continuous initiative** OR be **absorbed into existing area review cadences** (one SOP retrofit per quarterly review per area).

## 1. Operating story

I80 minted `pattern_sop_addendum_split` and demonstrated it across 3 SOP families (8 paired files total: stakeholder lenses + 2 I79 People SOPs + 5 I73 engagement-lifecycle SOPs). The mechanical contract is operational (jargon-scan addendum exemption + Pydantic Literal extension + meta-SOP authoring contract + PRECEDENCE.md addendum-class registration). The remaining ~40 SOP body files across 11 areas have not yet been retrofitted.

I81 retrofits the remaining vault. The operator's framing ([D-IH-80-D Round-3 ratification](../80-i79-lessons-learned/decision-log.md)): *"option C... the goal of an SOP is to enable a person to execute the process e2e with relevant context and all, but all the supporting documentation can very well go into addendum, that way we can keep the extreme jargon weave in some SOPs out of the way, at least when it's jargon of another area. each area must speak their own jargon, that's ok. Data speaks data, tech speaks tech, finances the same, and people are plain terms because it's people"*.

The doctrinal cohering principle: **each area legitimately speaks its own jargon in its own SOPs; cross-area depth lives in addenda; people-area SOPs are the strictest plain-language register because people execute them**. This is *not* a policy of zero-jargon-everywhere; it is a policy of *register-discipline by area + cross-area depth in addenda*.

## 2. Scope

### 2a. SOPs in scope (full vault count as of 2026-05-16)

| Area / sub-area | SOP body count | Already paired (I80) | Remaining (I81) | Notes |
|:---|---:|---:|---:|:---|
| Operations / RevOps | 9 | 0 | 9 | Highest concentration; cross-area integration-heavy (FINOPS + Marketing + People) |
| Tech / System Owner | 8 | 0 | 8 | Tech jargon legitimately in body; addenda for cross-area integration only (e.g., Madeira UX review intersects People + Marketing) |
| People / People Operations | 6 | 5 | 1 | Almost fully retrofitted at I80 P5; only `SOP-RECRUITER_ONBOARDING_001` remains |
| Research / Intelligence | 4 | 0 | 4 | CORPINT register; addenda may carry classification-level routing |
| Marketing / Reach | 4 | 0 | 4 | Brand-voice + GTM register; addenda for cross-area handoffs (RevOps + Compliance) |
| People / Compliance | 3 | 0 | 3 | Compliance register; SOP-META is the meta-SOP itself + governance assets |
| People / (root canonicals) | 2 | 2 | 0 | Both retrofitted at I80 P4 |
| Operations / Engagement | 2 | 0 | 2 | Discovery + estimation discipline |
| Marketing / Brand | 2 | 0 | 2 | Brand canon register |
| Envoy Tech Lab | 1 | 0 | 1 | Tech Lab framework register |
| People / Ethics | 1 | 0 | 1 | Ethics register |
| People / Learning | 1 | 0 | 1 | Apprentice curriculum |
| Operations / PMO | 1 | 0 | 1 | Vault promotion gate |
| Operations / SMO | 1 | 0 | 1 | Service management |
| Marketing / Storytelling | 1 | 0 | 1 | Media onboarding |
| Finance / Business Controller | 1 | 0 | 1 | Founder funding |
| **Totals** | **47** | **7** | **40** | |

### 2b. Out-of-scope

- **Net-new SOPs** that other initiatives mint during I81 execution — those should ship paired at minting time (per `SOP-META_PROCESS_MGMT_001.md` §"Body and Addendum split" contract minted at I80 P1).
- **Bodies that legitimately need no addendum** — some SOPs are short enough or single-area enough that an addendum would be empty. The retrofit author judges per-pair; a "no addendum needed; body alone is sufficient" outcome is acceptable and recorded as `addendum_needed: false` in the retrofit log. **Expected outcome rate: 10-30% of SOPs end up body-only**, narrowing the actual paired-file count to **~28-36** of the 40 remaining.

## 3. Strands

### Strand A — RevOps + Marketing retrofit (cross-area-heaviest)

The RevOps SOPs intersect FINOPS + Marketing + People + Legal + Tech most heavily. Their addenda will be the densest. Marketing SOPs (Reach + Brand + Storytelling) carry brand-voice register; cross-area depth (Compliance routing for media releases; RevOps integration for GTM) lives in addendum.

| SOP | Likely addendum content |
|:---|:---|
| `SOP-ENGAGEMENT_SCAFFOLDING_001` | Workspace blueprint cross-references + per-engagement folder shape detail |
| `SOP-ENGAGEMENT_TEMPLATE_PROMOTION_001` | RevOps QBR cadence detail + template-class taxonomy + Marketing brand-voice cross-check |
| `SOP-PERSONA_AUDIT_001` | Persona-registry FK posture + Tech CRM-integration impact + Research persona-research input |
| `SOP-LEGAL_TEMPLATE_FIRE_001` | Legal Counsel handoff posture + IP-clause routing + Compliance access-level routing |
| `SOP-MADEIRA_REVOPS_HANDOFF_001` | Madeira Tech Lab posture + UX review cadence + RevOps verdict-and-cadence cross-references |
| `SOP-PEOPLE_ENGAGEMENT_HANDOFF_001` | People-to-RevOps handoff mechanics + workspace-blueprint folder co-creation |
| `SOP-FINOPS_BRIDGE_001` | FINOPS no-second-SSOT architecture detail + Stripe metadata routing + counterparty FK posture |
| `SOP-REVOPS_QBR_001` | Quarterly business review depth + cross-area roll-up mechanics |
| Marketing: `SOP-GTM_QUALIFICATION_001` + `SOP-GTM_INBOUND_SLA_001` + `SOP-CRM_INTEGRATION_001` | RevOps cross-area integration + persona-registry FK |
| Marketing: `SOP-BRAND_TEMPLATE_REGISTRY_MTNCE_001` + `SOP-BRAND_VOICE_DRIFT_TRIAGE_001` | Drift-gate validator detail + LLM-judge posture (cross-link I78 candidate) |
| `SOP-MEDIA_ONBOARDING_001` | Compliance access-level routing + Storytelling brand-voice cross-check |

**~12 SOPs · ~10-12 addenda likely.**

### Strand B — Tech Lab + System Owner retrofit (Tech jargon legitimate; cross-area depth only)

The Tech Lab + System Owner SOPs legitimately speak tech jargon in their bodies (the operator's framing: *"tech speaks tech"*). Addenda only carry cross-area depth where Tech intersects People + Marketing + Operations.

| SOP | Likely addendum content |
|:---|:---|
| `SOP-TECH_AGENTIC_INFRA_001` | **No-op per I80 P4 decision** — Tech Lab speaks tech in body legitimately; cross-area depth (KB tier integration) already lives in `SOP-PEOPLE_AGENTIC_OPERATIONS_001.addendum.md` |
| `SOP-RELEASE_TAXONOMY_001` | Release taxonomy + cross-area release-cadence mechanics (Marketing + People impact) |
| `SOP-CICD_BASELINE_001` | CI/CD framework register + cross-area release-gate routing |
| `SOP-MADEIRA_VERDICT_AND_CADENCE_001` | Madeira UX cadence detail + cross-link to RevOps Madeira-handoff SOP |
| `SOP-MADEIRA_SCENARIO_LIFECYCLE_001` | Test bank scenario depth + UX review cross-references |
| `SOP-MADEIRA_UX_REVIEW_001` | UX-review framework register + Marketing brand-voice cross-check |
| `SOP-MCP_SERVER_DEFINITION` | MCP framework register + cross-area MCP discoverability mechanics |
| `SOP-HLK_TOOLING_STANDARDS_001` | Tooling framework register + cross-area dev-experience mechanics |

**~8 SOPs · ~5-7 addenda likely (1 no-op confirmed; 2-3 may end body-only).**

### Strand C — Research + Compliance + Ethics + Learning retrofit (CORPINT + classification register)

These SOPs carry CORPINT register (Intelligence) or classification-level routing (Compliance + Ethics) or apprentice-curriculum mechanics (Learning). Addenda may carry classification routing detail or curriculum integration detail.

| SOP | Likely addendum content |
|:---|:---|
| Intelligence: `SOP-IO_INTELLIGENCE_REPORT_001` + `SOP-IO_ELICITATION_DISCIPLINE_001` + `SOP-RESEARCH_ENGAGEMENT_TRIGGER_001` + `SOP-SOURCE_RELIABILITY_REGISTRY_MTNCE_001` | CORPINT classification routing + cross-area handoff (RevOps engagement-trigger) + Compliance access-level routing |
| Compliance: `SOP-META_PROCESS_MGMT_001` + `SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001` + `SOP-HLK_TRANSCRIPT_REDACTION_001` | Meta-SOP authoring contract is itself the meta; addenda carry validator integration depth + GOI/POI obfuscation mechanics + transcript-redaction technical specifics |
| Ethics: `SOP-ETHICS_LEARNING_REVIEW_001` | Ethics review framework + cross-link Learning curriculum cadence |
| Learning: `SOP-LEARNING_APPRENTICE_CURRICULUM_ASSIGNMENT_001` | Apprentice curriculum framework register + Tech Lab knowledge-test integration |

**~8 SOPs · ~6-8 addenda likely.**

### Strand D — Operations remainder + People Operations recruiter + Finance retrofit

The smaller remainder spans PMO + Engagement + SMO + People-Ops-recruiter + Finance.

| SOP | Likely addendum content |
|:---|:---|
| `SOP-RECRUITER_ONBOARDING_001` (People Ops) | Cross-link to engagement-lifecycle SOP family + recruiter-specific access-level routing |
| Engagement: `SOP-ENG_ESTIMATION_DISCIPLINE_001` + `SOP-ENG_DISCOVERY_QUESTIONNAIRE_001` | Discovery framework register + estimation rubric depth |
| `SOP-PMO_VAULT_PROMOTION_GATE_001` | Vault promotion mechanics depth + cross-area decision-register integration |
| `SOP-SMO_<...>` (SMO; 1 SOP) | Service management framework register |
| `SOP-FOUNDER_COMPANY_FUNDING_001` (Finance) | FINOPS architecture cross-link + cap-table mechanics + investor-advisor lifecycle cross-link |

**~6 SOPs · ~4-5 addenda likely.**

## 4. Phase scaffold (preliminary; refine at promotion-time P0 charter)

| Phase | Strand | Scope | Closes |
|:---|:---:|:---|:---:|
| **P0** | — | Charter + INITIATIVE / DECISION / OPS rows + master-roadmap; ratify retrofit-mode ([continuous] vs [absorbed-into-quarterly-review]) | — |
| **P1** | A (RevOps) | 9 RevOps SOPs retrofit | OPS-81-1 |
| **P2** | A (Marketing) | ~6 Marketing SOPs retrofit | OPS-81-2 |
| **P3** | B (Tech) | ~8 Tech Lab + System Owner SOPs retrofit | OPS-81-3 |
| **P4** | C (Research + Compliance + Ethics + Learning) | ~8 SOPs retrofit | OPS-81-4 |
| **P5** | D (Operations remainder + People Ops + Finance) | ~6 SOPs retrofit | OPS-81-5 |
| **P6** | — | Closing UAT + INITIATIVE_REGISTRY closure + I-NN candidate stub for next-vault-class retrofit (templates + dimensions + canonicals beyond SOPs) | — |

**Effort estimate: 5-8 engineer-days at continuous-execution pace**, OR **1-2 retrofits per area per quarter** absorbed into existing review cadences (4-6 quarters to complete).

## 5. Conundrums (open at candidate stage)

1. **C-81-1 — Retrofit mode (continuous vs absorbed)**. Continuous = single-initiative ~5-8 days; absorbed = retrofit-per-quarterly-review per area. Default = absorbed (less context-switch; aligns with how each area already reviews its canonicals). Ratify at P0.
2. **C-81-2 — No-addendum-needed threshold**. When does an SOP legitimately not need an addendum? Default = body word-count + cross-area integration count. Ratify at P0.
3. **C-81-3 — Author posture**. Each area's role_owner authors its own retrofits OR a single agent batch-retrofits all? Default = each area's role_owner with agent assistance (preserves register-discipline expertise per area). Ratify at P0.
4. **C-81-4 — Forward-extension to non-SOP canonicals**. After I81 closes, should the same paired-file pattern extend to `*_REGISTRY.csv` companions OR `*_DOCTRINE.md` companions? Default = consider at I81 P6 closing-stub. Ratify at P6.
5. **C-81-5 — Linking validator integration**. Should `validate_design_pattern_registry.py --jargon-scan` be extended to also scan non-People area canonicals (Marketing brand register; Tech framework register) using their own register-specific forbidden-token lists? Default = out-of-scope for I81 (per-area register-jargon is legitimate); revisit at I82 candidate. Ratify at P0.

## 6. Decision preview (D-IH-81-* rows likely to mint)

| ID | Question | Owner | Status entering plan | Close-out phase |
|:---|:---|:---|:---:|:---:|
| D-IH-81-A | Retrofit mode (continuous vs absorbed) | People Operations Lead | open | P0 |
| D-IH-81-B | No-addendum-needed threshold | People Operations Lead | open | P0 |
| D-IH-81-C | Author posture (role_owner vs single-agent batch) | People Operations Lead | open | P0 |
| D-IH-81-D | Forward-extension to non-SOP canonicals | People Operations Lead | open | P6 |
| D-IH-81-E | Per-area register-specific jargon-scan extension | System Owner | open | P0 |

## 7. Risks (preliminary)

| ID | Risk | Likelihood | Impact | Mitigation |
|:---|:---|:---:|:---:|:---|
| R-IH-81-1 | Retrofit fatigue if continuous mode chosen | M | M | Default to absorbed mode; allow operator-discretion mode-switch per phase |
| R-IH-81-2 | Per-area register-discipline expertise mis-applied (e.g., Tech Lab agent retrofits Marketing SOP without brand voice) | M | M | C-81-3 default routes retrofits via role_owner |
| R-IH-81-3 | Body-vs-addendum split judgement drift across areas | L | M | Meta-SOP §"Body and Addendum split" (minted at I80 P1) is the contract; retrofit author cites it |
| R-IH-81-4 | Net-new SOPs minted during I81 execution skip the paired-file contract | L | M | `SOP-META_PROCESS_MGMT_001.md` §"Body and Addendum split" is the binding contract for new SOPs; I81 reinforces enforcement |
| R-IH-81-5 | Cross-references break when bodies are trimmed | L | L | Mechanical: jargon-scan + frontmatter validators catch most; per-pair PR review catches rest |

## 8. Forward-link to I80

This candidate's existence satisfies the I80 P6 forward-charter. I80 closes (at P7) with the operator's framing operationalised at *contract level*; I81 closes the loop by retrofitting the remaining ~40 bodies to *demonstration level*. Until I81 promotes, the contract holds and net-new SOPs honor it; existing SOPs retain their pre-I80 monolithic form (legitimate; no breaking change to existing readers).

## 9. SOC posture

This candidate stub contains: zero secrets, zero API keys, zero raw GOI/POI mappings, zero PII. SOP filename slugs are public-naming-safe.

## 10. Cross-references

- Forward-charter origin: [I80 master roadmap](../80-i79-lessons-learned/master-roadmap.md) + [I80 P6 UAT](../80-i79-lessons-learned/reports/p6-uat-2026-05-16.md) + [I80 P6 integration verification](../80-i79-lessons-learned/reports/p6-integration-verification.md)
- Pattern doctrine: [`PEOPLE_DESIGN_PATTERN_LIBRARY.md` §pattern-sop-addendum-split](../../references/hlk/v3.0/Admin/O5-1/People/canonicals/PEOPLE_DESIGN_PATTERN_LIBRARY.md)
- Authoring contract: [`SOP-META_PROCESS_MGMT_001.md` §Body and Addendum split](../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/SOP-META_PROCESS_MGMT_001.md)
- Validator: [`scripts/validate_design_pattern_registry.py`](../../../scripts/validate_design_pattern_registry.py) (`--jargon-scan` mode with addendum exemption per `D-IH-80-F`)
- DAMA-DMBOK 2.0 Metadata Management knowledge area (paired-file metadata granularity rationale)
