---
candidate_id: I81
title: Vault knowledge-base integrity + Compliance layout reorganisation + full-vault SOP body/addendum retrofit
status: candidate
authored: 2026-05-16
last_review: 2026-05-16
parent_initiative: 80 (I79 lessons-learned, P5+P6+P6.5 forward-charter)
priority: 4
language: en
---

# I81 candidate — Vault knowledge-base integrity, layout reorganisation, and full-vault SOP retrofit

> **Candidate scaffold authored at I80 P6 per `D-IH-80-D` Option C forward-charter.** **Expanded 2026-05-16 (operator directive):** one **dedicated end-to-end run** through `process_list.csv`, every referenced SOP (body + runbook paths), every addendum, [`KNOWLEDGE_PAIRING_REGISTRY.csv`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/KNOWLEDGE_PAIRING_REGISTRY.csv) completeness, validators, mirror emit coverage, artefact paths, and per-file metadata—so organisational confidence (“the knowledge base is robust”) rests on evidence, not hope. Separately execute **Compliance canonical layout reorganisation** (Initiative 22 forward layout—many registers historically landed under `canonicals/` root because area foundations post-dated minting; reorganise toward `advops/` / `finops/` / `techops/` / `dimensions/` per [`canonicals/README.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/README.md)) with path updates propagated to PRECEDENCE, validators, mirror sync scripts, and `hlk-erp` consumers—**operator-approved baseline/process tranches** apply.
>
> Promoted to `active` when (a) operator confirms the I80 paired-file pattern lands well across the pilot pairs (rolling ratification), (b) **P1 integrity baseline** backlog is prioritised or accepted as phased, (c) **P2 layout migration** hold-gates are explicit (baseline + process approval where CSV paths change validators), and (d) retrofit strands have clear next-quarter priority. Retrofit rhythm remains *non-time-pressured*: **continuous sprint** vs **absorbed into quarterly area review** ratified at P0.

## 1. Operating story

I80 minted `pattern_sop_addendum_split`, [`KNOWLEDGE_PAIRING_REGISTRY.csv`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/KNOWLEDGE_PAIRING_REGISTRY.csv), and validators so relationships are **machine-addressable**. The remaining work is triple:

1. **Integrity + data-quality (DQ)** — Prove that every executable process row in `process_list.csv` resolves cleanly to artefacts (SOP body, paired addendum where required, YAML/runbook/script per `validate_process_list_pairing.py`), paths exist on disk, frontmatter/metadata is coherent, and **pairing-registry rows stay in parity** (`KNOWLEDGE_PAIRING` + pairing validators—no orphaned bodies or dangling FKs).

2. **Layout reorganisation (Compliance canonicals)** — Move legacy flat files into the Initiative 22 **forward layout** documented in [`canonicals/README.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/README.md) so artefacts are grouped by plane (dimensions / advops / finops / techops / …), not **“everything cramped under Compliance root”**. This complements role/folder reorganisation elsewhere: vault layout becomes legible **per area**.

3. **SOP retrofit (body/addendum scale-out)** — The ~40 remaining SOP bodies across 11 areas (per §2a table).

I81 retrofits the remaining vault bodies **after** the integrity baseline and migration plan exist so refactors don't chase moving targets.

The doctrinal retrofit framing ([D-IH-80-D Round-3 ratification](../80-i79-lessons-learned/decision-log.md)): *"option C... the goal of an SOP is to enable a person to execute the process e2e with relevant context and all, but all the supporting documentation can very well go into addendum..."* plus per-area jargon legitimacy.

The doctrinal **integrity** framing (operator 2026-05-16): *inventory run through process_list, actual SOPs, addenda, mirrors, locations, metadata—everything about integrity and data quality—we need confidence the knowledge base is robust*.

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

### 2c. Knowledge-base integrity + data-quality sprint (FOUNDATION WORK)

**Purpose:** One governed pass producing a dated **inventory + DQ evidence pack** and a prioritized fix backlog—not ad-hoc grepping later.

Deliverables (minimal bar at P1 close):

| # | Artefact | What it proves |
|:-:|---|:---|
| 1 | **`reports/i81/kb-integrity-audit-<YYYY-MM-DD>.md`** (repo path under `docs/wip/planning/81-<slug>/reports/` once initiative folder promotes) | Human-readable synthesis: methodology, scope exclusions, totals, PASS/WARN/FAIL summary, remediation rows |
| 2 | **`reports/i81/kb-integrity-matrix-<YYYY-MM-DD>.csv`** (or equivalent machine table) | One row per `process_list.csv` executable row vs non-actionable meta rows: columns at minimum—`item_id`, `role_owner`, `area`, `sop_path`(s), `addendum_path`, `runbook_kind` (yaml/py/none), `pairing_registry_row`(s), `path_exists`(y/n), `pairing_validator`, `mirror_table`(if any), `notes` |
| 3 | **`KNOWLEDGE_PAIRING_REGISTRY` gap register** — either delta rows appended in dedicated commits OR appendix table in §1 referencing rows to mint | Every paired-body SOP instantiated through I81 has a `KNOWLEDGE_PAIRING` row (`D-IH-80-H` contract via `SOP-META_PROCESS_MGMT_001.md` §4.6) |

Mechanical gates to run/cite in P1 evidence pack (baseline set—extend during charter):

- `py scripts/validate_hlk.py` (umbrella: includes `DECISION_REGISTER`, `INITIATIVE_REGISTRY`, `OPS_REGISTER`, `process_list`, `KNOWLEDGE_PAIRING_REGISTRY`, etc.)
- `py scripts/validate_process_list_pairing.py`
- Per-area SOP scanners as needed (`validate_design_pattern_registry.py --jargon-scan` scope = People-area bodies where applicable)

**Mirrors posture:** Produce a **`compliance_mirror_emit` coverage checklist** aligned with [`akos-holistika-operations.mdc`](../../../.cursor/rules/akos-holistika-operations.mdc)—which CSVs mirror to which tables, which are intentionally non-mirrored yet, drift risk ranking. DDL/DML propagation remains operator SQL gate—not bulk commits of mirror data as migrations.

**Consumer posture:** Identify `hlk-erp` assumptions on paths (panels, dossiers)—note each row needing TypeScript/route update when layout migrations land (coordinate with cross-repo propagation SOP).

### 2d. Compliance vault layout reorganisation (Initiative 22 execution strand)

**Problem statement:** Canonical registers accrued under `People/Compliance/canonicals/` **root** before the forward three-axis layout was exercised; “everything cramped in compliance root” slows navigation and onboarding.

**Mechanism SSOT:** [`canonicals/README.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/README.md) **Forward layout (target)** + deprecation-alias paragraph.

**Deliverables:**

- Migrate legacy root CSV/Markdown to forward subfolders (**tranche commits**—not one mega-move) with deprecation-alias stubs or README redirects where required.
- Update **every** authoritative consumer in lockstep each tranche: `PRECEDENCE.md`; `scripts/validate_*.py` Path constants; [`scripts/sync_compliance_mirrors_from_csv.py`](../../../scripts/sync_compliance_mirrors_from_csv.py) mappings; KM manifest FK paths if touched; **`hlk-erp`** route strings + API contracts if surfaced there.
- Re-run **`py scripts/validate_hlk.py` + targeted mirror emit verification** (`py scripts/verify.py compliance_mirror_emit` profile when in scope).

**Gates:** `baseline_organisation.csv` + `process_list.csv` edits require **explicit operator approval** per [`akos-governance-remediation.mdc`](../../../.cursor/rules/akos-governance-remediation.mdc). Pure path moves affecting governance CSVs qualify as canonical gate if they redefine SSOT anchors—record D-IH-81-* decision per tranche.

**Cross-link Talent / capability work:** DQ matrix + cleaner layout unblock **Talent role activation + `CAPABILITY_REGISTRY` seed rows** handled in sibling **I82** (see [I82 candidate](i82-holistika-capability-doctrine-and-commercial-readiness.md) §Promotion criteria + phased dependency — **I82 P2 capability inventory should consume I81 P1 integrity artefacts** (I82 P1 = `baseline_organisation.csv` Talent tranche; the registry mint is P2).

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

**Recommended execution order:** **P1 integrity → P2 layout migration waves (operator-gated) → P3-P7 retrofit strands** so path moves settle before wholesale body/addendum churn. If operator accepts risk, **P2 waves may interleave** with retrofit *per-plane* once that plane's layout is stable.

| Phase | Strand | Scope | Closes |
|:---|:---:|:---|:---:|
| **P0** | — | Charter + INIT/DECISION/OPS mints + initiative `master-roadmap.md`; ratify retrofit mode (**continuous vs absorbed**); ratify migration strategy (**wave-by-plane** vs big-bang); confirm `hlk-erp` parity expectations | OPS-81-0 |
| **P1** | — | **Knowledge-base integrity + DQ baseline** (§2c): matrix CSV + audit markdown + `KNOWLEDGE_PAIRING` gap list + mirror-emit coverage checklist + validator run log; **no layout moves** in P1 except emergency fixes | OPS-81-1 |
| **P2** | — | **Compliance layout reorganisation** (§2d): Initiative 22 forward-layout moves in tranches; each tranche = git move + PRECEDENCE + validators + sync script + ERP notes; rerun `validate_hlk` GREEN | OPS-81-2 (possibly multiple OPS rows if phased by plane—split at charter) |
| **P3** | A (RevOps) | 9 RevOps SOPs retrofit | OPS-81-3 |
| **P4** | A (Marketing) | ~6 Marketing SOPs retrofit | OPS-81-4 |
| **P5** | B (Tech) | ~8 Tech Lab + System Owner SOPs retrofit | OPS-81-5 |
| **P6** | C (Research + Compliance + Ethics + Learning) | ~8 SOPs retrofit | OPS-81-6 |
| **P7** | D (Operations remainder + People Ops + Finance) | ~6 SOPs retrofit | OPS-81-7 |
| **P8** | — | Closing UAT (integrity regression + spot-check DQ rows + mirror smoke) + INITIATIVE closure + successor stub (**I-NN dimensional registry retrofit** optional) | OPS-81-8 |

**Effort estimate:**

- **P1 integrity sprint:** ~1-3 engineer-days (plus operator review).
- **P2 layout migration:** ~3-10 engineer-days total spread across **N tranches** (depends how many legacy root files migrate per wave).
- **P3-P7 retrofit (original I81 strands):** ~5-8 engineer-days continuous **or** absorbed into quarterly cadence (same as prior estimate).
- **Total when run continuously:** roughly **two weeks** inclusive of QA—often better absorbed as parallel tracks (**integrity + migrations** early; **retrofits** follow).

## 5. Conundrums (open at candidate stage)

1. **C-81-1 — Retrofit mode (continuous vs absorbed)**. Continuous = single-initiative ~5-8 days; absorbed = retrofit-per-quarterly-review per area. Default = absorbed (less context-switch; aligns with how each area already reviews its canonicals). Ratify at P0.
2. **C-81-2 — No-addendum-needed threshold**. When does an SOP legitimately not need an addendum? Default = body word-count + cross-area integration count. Ratify at P0.
3. **C-81-3 — Author posture**. Each area's role_owner authors its own retrofits OR a single agent batch-retrofits all? Default = each area's role_owner with agent assistance (preserves register-discipline expertise per area). Ratify at P0.
4. **C-81-4 — Forward-extension to non-SOP canonicals**. After I81 closes, should the same paired-file pattern extend to `*_REGISTRY.csv` companions OR `*_DOCTRINE.md` companions? Default = consider at I81 P8 closing-stub. Ratify at P8.
5. **C-81-5 — Linking validator integration**. Should `validate_design_pattern_registry.py --jargon-scan` be extended to also scan non-People area canonicals (Marketing brand register; Tech framework register) using their own register-specific forbidden-token lists? Default = out-of-scope for I81 retrofit strands (per-area register-jargon is legitimate); **optional line item in P1 integrity report** for “future gate” candidates. Ratify at P0.
6. **C-81-6 — Integrity matrix owner-of-record**. PMO runs the matrix vs each `role_owner` self-certifies per area? Default = **PMO + System Owner** produce matrix; **area role_owners** sign off rows for their area (lightweight inline-ratify batch). Ratify at P0.
7. **C-81-7 — Layout migration batching**. Big-bang path move (one painful day) vs wave-by-plane (many small PRs, less blast radius). Default = **wave-by-plane** per Initiative 22 README. Ratify at P0.

## 6. Decision preview (D-IH-81-* rows likely to mint)

| ID | Question | Owner | Status entering plan | Close-out phase |
|:---|:---|:---|:---:|:---:|
| D-IH-81-A | Retrofit mode (continuous vs absorbed) | People Operations Lead | open | P0 |
| D-IH-81-B | No-addendum-needed threshold | People Operations Lead | open | P0 |
| D-IH-81-C | Author posture (role_owner vs single-agent batch) | People Operations Lead | open | P0 |
| D-IH-81-D | Forward-extension to non-SOP canonicals | People Operations Lead | open | P8 |
| D-IH-81-E | Per-area register-specific jargon-scan extension | System Owner | open | P0 |
| **D-IH-81-F** | **Integrity matrix methodology + PASS threshold** — what constitutes “CLOSED-P1”? | PMO + System Owner | open | **P1** |
| **D-IH-81-G** | **Layout migration wave plan** — which root files move in which PR; deprecation-alias policy | Data Architect + Compliance Officer | open | **P2** |

## 7. Risks (preliminary)

| ID | Risk | Likelihood | Impact | Mitigation |
|:---|:---|:---:|:---:|:---|
| R-IH-81-1 | Retrofit fatigue if continuous mode chosen | M | M | Default to absorbed mode; allow operator-discretion mode-switch per phase |
| R-IH-81-2 | Per-area register-discipline expertise mis-applied (e.g., Tech Lab agent retrofits Marketing SOP without brand voice) | M | M | C-81-3 default routes retrofits via role_owner |
| R-IH-81-3 | Body-vs-addendum split judgement drift across areas | L | M | Meta-SOP §"Body and Addendum split" (minted at I80 P1) is the contract; retrofit author cites it |
| R-IH-81-4 | Net-new SOPs minted during I81 execution skip the paired-file contract | L | M | `SOP-META_PROCESS_MGMT_001.md` §"Body and Addendum split" is the binding contract for new SOPs; I81 reinforces enforcement |
| R-IH-81-5 | Cross-references break when bodies are trimmed | L | L | Mechanical: jargon-scan + frontmatter validators catch most; per-pair PR review catches rest |
| **R-IH-81-6** | **Integrity matrix becomes stale the day after P1** — drift returns without ownership | M | M | Assign **quarterly reconciliation** row to PMO or fold into `validate_hlk` release-gate already run on every PR |
| **R-IH-81-7** | **Layout migration breaks sibling repo `hlk-erp`** without coordinated PR | M | H | **Cross-repo schema propagation SOP** + explicit checklist row per tranche; never merge layout wave without consumer-path audit |

## 8. Forward-link to I80 + I82

This candidate absorbs the I80 P6 forward-charter (retrofit bodies) **and** formalises operator request (2026-05-16) for a **deterministic KB integrity baseline** plus **Compliance forward-layout reorganisation**.

- **I80** operationalised pairing at contract level (`SOP-META`, `KNOWLEDGE_PAIRING_REGISTRY`, validators). **I81** proves end-to-end **integrity** then **relocates cramped compliance artefacts** without losing SSOT.
- **[I82](i82-holistika-capability-doctrine-and-commercial-readiness.md)** consumes **I81 P1 outputs** (`kb-integrity-matrix-*`) when minting **`CAPABILITY_REGISTRY`** and activates **Talent** in `baseline_organisation.csv`. Recommended dependency: **I82 P2 (Capability registry mint) gates on I81 P1 integrity CLOSED OR explicit operator waiver** (`D-IH-82-PREREQ`); I82 P1 (Talent baseline tranche) is the canonical-CSV gate that unlocks downstream organisational work.

Until I81 promotes (or scoped slice lands), pairing contract remains binding for net-new SOPs; existing monolithic SOPs stay valid readers.

## 9. SOC posture

This candidate stub contains: zero secrets, zero API keys, zero raw GOI/POI mappings, zero PII. SOP filename slugs are public-naming-safe.

## 10. Cross-references

- Forward-charter origin: [I80 master roadmap](../80-i79-lessons-learned/master-roadmap.md) + [I80 P6 UAT](../80-i79-lessons-learned/reports/p6-uat-2026-05-16.md) + [I80 P6 integration verification](../80-i79-lessons-learned/reports/p6-integration-verification.md)
- Pattern doctrine: [`PEOPLE_DESIGN_PATTERN_LIBRARY.md` §pattern-sop-addendum-split](../../references/hlk/v3.0/Admin/O5-1/People/canonicals/PEOPLE_DESIGN_PATTERN_LIBRARY.md)
- Authoring contract: [`SOP-META_PROCESS_MGMT_001.md` §Body and Addendum split](../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/SOP-META_PROCESS_MGMT_001.md)
- [`KNOWLEDGE_PAIRING_REGISTRY.csv`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/KNOWLEDGE_PAIRING_REGISTRY.csv) + [`scripts/validate_knowledge_pairing_registry.py`](../../../scripts/validate_knowledge_pairing_registry.py) (I80 P6.5; D-IH-80-H)
- [`scripts/validate_process_list_pairing.py`](../../../scripts/validate_process_list_pairing.py)
- Compliance forward layout convention: [`canonicals/README.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/README.md) + [`PRECEDENCE.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md)
- DAMA-DMBOK 2.0 Metadata Management knowledge area (paired-file + registry granularity rationale)
