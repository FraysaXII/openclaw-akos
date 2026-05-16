---
candidate_id: I81
title: Knowledge-base integrity sweep (vault + planning surface) + Compliance layout reorganisation + named-milestone migration + full-vault SOP body/addendum retrofit
status: candidate
authored: 2026-05-16
last_review: 2026-05-16
parent_initiative: 80 (I79 lessons-learned, P5+P6+P6.5 forward-charter; expanded 2026-05-16)
priority: 4
language: en
---

# I81 candidate — Knowledge-base integrity sweep, Compliance layout reorganisation, named-milestone migration, and full-vault SOP retrofit

> **Candidate scaffold authored at I80 P6 per `D-IH-80-D` Option C forward-charter.** **Expanded 2026-05-16 in two waves:**
>
> **Wave 1 (operator directive 2026-05-16 morning):** one **dedicated end-to-end run** through `process_list.csv`, every referenced SOP (body + runbook paths), every addendum, [`KNOWLEDGE_PAIRING_REGISTRY.csv`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/KNOWLEDGE_PAIRING_REGISTRY.csv) completeness, validators, mirror emit coverage, artefact paths, and per-file metadata — so organisational confidence ("the knowledge base is robust") rests on evidence, not hope. Separately execute **Compliance canonical layout reorganisation** (Initiative 22 forward layout — many registers historically landed under `canonicals/` root because area foundations post-dated minting; reorganise toward `advops/` / `finops/` / `techops/` / `dimensions/` per [`canonicals/README.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/README.md)) with path updates propagated to PRECEDENCE, validators, mirror sync scripts, and `hlk-erp` consumers — **operator-approved baseline/process tranches** apply.
>
> **Wave 2 (operator directive 2026-05-16 evening, response to inline-ratify on next-action sequencing):** absorb a fourth foundation strand — **planning-surface integrity** — that mirrors vault-surface integrity for the **planning artefacts themselves** (candidate stubs, dep maps, master-roadmaps, decision logs). Drives a **named-milestone schema** ([`I82-CAPABILITY-REGISTRY-MINT`] replacing magic-number `I82 P2`-style references) so phase renumbering inside one initiative does not silently break references in sibling initiatives. Mints a Class B drift validator (`scripts/validate_planning_cross_refs.py`) and ships the one-shot historical regression sweep that gives "previous rounds clean" confidence empirically — both as long-term targets, not band-aids.
>
> Promoted to `active` when (a) operator confirms the I80 paired-file pattern lands well across the pilot pairs (rolling ratification), (b) **P1 integrity baseline** backlog is prioritised or accepted as phased, (c) **P2 layout migration** hold-gates are explicit (baseline + process approval where CSV paths change validators), (d) **P3 planning-surface integrity + named-milestone schema** has a ratified vocabulary (D-IH-81-H), and (e) retrofit strands have clear next-quarter priority. Retrofit rhythm remains *non-time-pressured*: **continuous sprint** vs **absorbed into quarterly area review** ratified at P0.

## 1. Operating story

I80 minted `pattern_sop_addendum_split`, [`KNOWLEDGE_PAIRING_REGISTRY.csv`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/KNOWLEDGE_PAIRING_REGISTRY.csv), and validators so relationships are **machine-addressable**. The remaining work is **quadruple**:

1. **Vault integrity + data-quality (DQ)** — Prove that every executable process row in `process_list.csv` resolves cleanly to artefacts (SOP body, paired addendum where required, YAML/runbook/script per `validate_process_list_pairing.py`), paths exist on disk, frontmatter/metadata is coherent, and **pairing-registry rows stay in parity** (`KNOWLEDGE_PAIRING` + pairing validators — no orphaned bodies or dangling FKs).

2. **Layout reorganisation (Compliance canonicals)** — Move legacy flat files into the Initiative 22 **forward layout** documented in [`canonicals/README.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/README.md) so artefacts are grouped by plane (dimensions / advops / finops / techops / …), not **"everything cramped under Compliance root"**. This complements role/folder reorganisation elsewhere: vault layout becomes legible **per area**.

3. **Planning-surface integrity + named-milestone schema (NEW Wave 2 strand)** — Replace **magic-number cross-references** (`I82 P2`-style) between sibling initiatives with **named milestones** (`I82-CAPABILITY-REGISTRY-MINT`-style) anchored in each initiative's frontmatter `milestones:` array. Mint `scripts/validate_planning_cross_refs.py` (`akos/hlk_planning_milestone.py` Pydantic SSOT + tests) so this drift class becomes a **mechanical gate** alongside `validate_hlk` + `release-gate`. File a one-shot **Class B regression sweep report** as the historical baseline. Migration scope = **active candidates + dep map + active master-roadmaps**; closed-initiative roadmaps + reports are **frozen historical records** (out of scope; documented as policy in D-IH-81-J).

4. **SOP retrofit (body/addendum scale-out)** — The ~40 remaining SOP bodies across 11 areas (per §2a table).

I81 retrofits the remaining vault bodies **after** the integrity baselines (vault + planning-surface) and migration plans exist so refactors don't chase moving targets.

The doctrinal retrofit framing ([D-IH-80-D Round-3 ratification](../80-i79-lessons-learned/decision-log.md)): *"option C... the goal of an SOP is to enable a person to execute the process e2e with relevant context and all, but all the supporting documentation can very well go into addendum..."* plus per-area jargon legitimacy.

The doctrinal **vault integrity** framing (operator 2026-05-16 morning): *inventory run through process_list, actual SOPs, addenda, mirrors, locations, metadata — everything about integrity and data quality — we need confidence the knowledge base is robust*.

The doctrinal **planning-surface integrity** framing (operator 2026-05-16 evening, response to inline-ratify): *option F (named milestones) folded into existing initiatives where it belongs, combined with C (sweep + validator), designed for long-term target, properly governed and well designed*. Together: **Class B drift becomes structurally impossible** when references are FK-resolved, not free-text.

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

**Cross-link Talent / capability work:** DQ matrix + cleaner layout unblock **Talent role activation + `CAPABILITY_REGISTRY` seed rows** handled in sibling **I82** (see [I82 candidate](i82-holistika-capability-doctrine-and-commercial-readiness.md) §Promotion criteria + phased dependency — **I82-CAPABILITY-REGISTRY-MINT (currently I82 P2) should consume I81 P1 integrity artefacts** (I82-TALENT-ACTIVATION (currently I82 P1) is the canonical-CSV gate; the registry mint is the next milestone).

**Cross-link audience-tag canonicalization:** Sibling **[I85 candidate](i85-audience-tag-canonicalization.md)** mints `AUDIENCE_REGISTRY.csv` + drift gate for `_assets/advops/**` + `_assets/touchpoint-kit/**` frontmatter `audience: <J-*>` tagging. **Forward link**: I81 P1 evidence pack `kb-integrity-matrix-<date>.csv` should add an `audience_tags_coverage` column once I85 P1 ships (per I85 §5 wiring). I85 runs as sibling (different governance axis — persona-audience tagging, not vault-integrity); I81 P1 evidence pack consumes I85 P1 registry output as a column extension.

### 2e. Planning-surface integrity + named-milestone schema + Class B validator (Wave 2 strand)

**Problem statement:** Phase numbers in cross-references between sibling initiatives are **magic numbers**. When initiative *X* renumbers its own phases (e.g., I82 inserted Talent activation as P1, shifting Capability registry from P1 → P2), every sibling reference to "I82 P1" goes silently stale. **The 2026-05-16 regression sweep that this candidate's headline preface now references caught 4 phase-numbering drifts and 1 typo — empirical evidence the gap exists.** Closing the gap structurally requires three coordinated artefacts: a **schema** (named milestones), a **validator** (FK resolution), and a **historical baseline** (one-shot sweep).

**Mechanism SSOT (proposed; ratified at P0/P3 charter):**

- **Milestone ID format**: `<INITIATIVE_ID>-<PURPOSE_SLUG>` — e.g., `I82-CAPABILITY-REGISTRY-MINT`, `I82-TALENT-ACTIVATION`, `I82-USE-CASE-ARCHIVE`, `I83-INGESTOR-QUERY-LAYER`. `INITIATIVE_ID` matches `^I\d{2,3}$`; `PURPOSE_SLUG` is `UPPER-KEBAB-CASE`, ≤ 6 hyphenated tokens, semantically meaningful (not "PHASE-2"). Schema decision **D-IH-81-H** (close-out P3).
- **Definition home**: each initiative's frontmatter `milestones:` YAML array — same pattern as existing Cursor-plan `todos:` arrays. Each entry: `id`, `phase` (informational `P\d+(\.\d+)?` mapping), `purpose` (1 sentence), `status` (`planned` / `in_progress` / `closed` / `cancelled`).
- **Body convention**: phase headers retain `## P<N> — <name>` for human readability AND add `(milestone: I<NN>-<PURPOSE-SLUG>)` parenthetical on first occurrence.
- **Cross-reference convention**: between sibling initiatives use named milestones with informational phase parenthetical: `I82-CAPABILITY-REGISTRY-MINT (currently P2)`. The named ID is canonical; the `(currently P2)` parenthetical is informational and **may go stale** without breaking anything (only the canonical ID is FK-resolved).

**Deliverables (P3 close):**

| # | Artefact | Purpose |
|:-:|---|:---|
| 1 | [`akos/hlk_planning_milestone.py`](../../../akos/hlk_planning_milestone.py) | Pydantic SSOT for milestone schema; `Literal['planned','in_progress','closed','cancelled']` status enum; `MILESTONE_ID_PATTERN` regex constant |
| 2 | [`scripts/validate_planning_cross_refs.py`](../../../scripts/validate_planning_cross_refs.py) | Class B drift validator: walks `_candidates/*.md` + `_templates/*.md` + active `<NN-slug>/master-roadmap.md`; loads each frontmatter `milestones:`; resolves every `I<NN>-<SLUG>` reference in body; fails loudly on unresolved IDs, mismatched phase parenthetical drift (warn-only), or schema violations |
| 3 | [`tests/test_planning_cross_refs.py`](../../../tests/test_planning_cross_refs.py) | `@pytest.mark.governance` valid + invalid input pairs; registered under `scripts/test.py` group list |
| 4 | `reports/p3-class-b-regression-sweep-<YYYY-MM-DD>.md` (filed under `docs/wip/planning/81-<slug>/reports/`) | One-shot historical baseline: every active surface scanned with date, methodology, PASS/WARN/FAIL summary, remediation list. Findings inform the validator's rule set retroactively |
| 5 | Migration commits (Wave 1 = active candidates I74/I75/I76/I78/I81/I82/I83 + I60/I61/I69; Wave 2 = `INITIATIVE_DEPENDENCIES.md` + `_templates/README.md`; Wave 3 = active master-roadmaps — currently I77 only) | Net references migrated to named-milestone canonical form |
| 6 | `validate_hlk.py` umbrella + `release-gate.py` wiring + `config/verification-profiles.json` `pre_commit` profile entry | Validator runs on every commit; mechanical gate replaces human discipline |
| 7 | Cursor-rule extension to [`akos-planning-traceability.mdc`](../../../.cursor/rules/akos-planning-traceability.mdc) §"Plan-quality bar" | Codifies named-milestone convention so future plan authors inherit it by default |

**Migration policy (closed-initiative posture, D-IH-81-J):** Closed initiative master-roadmaps + reports are **frozen historical records** — they capture state at closure and **must not be retroactively migrated** to named-milestone form. The validator's allowlist excludes `<NN-slug>/` paths where the initiative's `INITIATIVE_REGISTRY.csv` row has `status=closed`. Active candidates + dep map + active master-roadmaps are **in scope**.

**CONTRIBUTING.md adherence:** validator + Pydantic + tests follow [`CONTRIBUTING.md`](../../../CONTRIBUTING.md) §"Python Code Standards" — Pydantic in `akos/<module>.py`, type hints, structured logging via `akos.log.setup_logging`, `pathlib.Path`, `@pytest.mark.governance`, wired into `scripts/test.py` group list + `scripts/release-gate.py` + `config/verification-profiles.json` `pre_commit`.

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

**Recommended execution order:** **P1 vault integrity → P2 layout migration waves (operator-gated) → P3 planning-surface integrity + named-milestone migration + Class B validator → P4-P8 retrofit strands → P9 closing UAT** so all foundational integrity (vault + planning) and layout reorganisation settle before wholesale body/addendum churn. If operator accepts risk, **P2 waves may interleave** with retrofit *per-plane* once that plane's layout is stable; **P3 ships before retrofit** so retrofit phases can use named-milestone references natively.

| Phase | Strand | Scope | Closes |
|:---|:---:|:---|:---:|
| **P0** | — | Charter + INIT/DECISION/OPS mints + initiative `master-roadmap.md`; ratify retrofit mode (**continuous vs absorbed**); ratify migration strategy (**wave-by-plane** vs big-bang); ratify named-milestone schema (D-IH-81-H); confirm `hlk-erp` parity expectations | OPS-81-0 |
| **P1** | — | **Vault integrity + DQ baseline** (§2c): matrix CSV + audit markdown + `KNOWLEDGE_PAIRING` gap list + mirror-emit coverage checklist + validator run log; **no layout moves** in P1 except emergency fixes | OPS-81-1 |
| **P2** | — | **Compliance layout reorganisation** (§2d): Initiative 22 forward-layout moves in tranches; each tranche = git move + PRECEDENCE + validators + sync script + ERP notes; rerun `validate_hlk` GREEN | OPS-81-2 (possibly multiple OPS rows if phased by plane — split at charter) |
| **P3** | — | **Planning-surface integrity + named-milestone migration + Class B validator** (§2e): mint `akos/hlk_planning_milestone.py` + `scripts/validate_planning_cross_refs.py` + tests; file Class B regression sweep report; migrate active candidates + dep map + active master-roadmaps to named milestones; wire validator into `validate_hlk.py` + `release-gate.py` + `pre_commit` profile; extend `akos-planning-traceability.mdc` §"Plan-quality bar"; ratify D-IH-81-H/I/J | OPS-81-3 |
| **P4** | A (RevOps) | 9 RevOps SOPs retrofit | OPS-81-4 |
| **P5** | A (Marketing) | ~6 Marketing SOPs retrofit | OPS-81-5 |
| **P6** | B (Tech) | ~8 Tech Lab + System Owner SOPs retrofit | OPS-81-6 |
| **P7** | C (Research + Compliance + Ethics + Learning) | ~8 SOPs retrofit | OPS-81-7 |
| **P8** | D (Operations remainder + People Ops + Finance) | ~6 SOPs retrofit | OPS-81-8 |
| **P9** | — | Closing UAT (integrity regression + spot-check DQ rows + mirror smoke + named-milestone validator GREEN on full active surface) + INITIATIVE closure + successor stub (**I-NN dimensional registry retrofit** optional) | OPS-81-9 |

**Effort estimate:**

- **P1 vault integrity sprint:** ~1-3 engineer-days (plus operator review).
- **P2 layout migration:** ~3-10 engineer-days total spread across **N tranches** (depends how many legacy root files migrate per wave).
- **P3 planning-surface + validator + sweep:** ~0.5-1 engineer-day (Pydantic + validator + tests + migration of ~10 active surfaces; mostly mechanical once schema is ratified).
- **P4-P8 retrofit (original I81 strands):** ~5-8 engineer-days continuous **or** absorbed into quarterly cadence (same as prior estimate).
- **Total when run continuously:** roughly **two weeks** inclusive of QA — often better absorbed as parallel tracks (**P1+P2+P3 integrity + migration foundation** early; **P4-P8 retrofits** follow).

## 5. Conundrums (open at candidate stage)

1. **C-81-1 — Retrofit mode (continuous vs absorbed)**. Continuous = single-initiative ~5-8 days; absorbed = retrofit-per-quarterly-review per area. Default = absorbed (less context-switch; aligns with how each area already reviews its canonicals). Ratify at P0.
2. **C-81-2 — No-addendum-needed threshold**. When does an SOP legitimately not need an addendum? Default = body word-count + cross-area integration count. Ratify at P0.
3. **C-81-3 — Author posture**. Each area's role_owner authors its own retrofits OR a single agent batch-retrofits all? Default = each area's role_owner with agent assistance (preserves register-discipline expertise per area). Ratify at P0.
4. **C-81-4 — Forward-extension to non-SOP canonicals**. After I81 closes, should the same paired-file pattern extend to `*_REGISTRY.csv` companions OR `*_DOCTRINE.md` companions? Default = consider at I81 P9 closing-stub. Ratify at P9.
5. **C-81-5 — Linking validator integration**. Should `validate_design_pattern_registry.py --jargon-scan` be extended to also scan non-People area canonicals (Marketing brand register; Tech framework register) using their own register-specific forbidden-token lists? Default = out-of-scope for I81 retrofit strands (per-area register-jargon is legitimate); **optional line item in P1 integrity report** for "future gate" candidates. Ratify at P0.
6. **C-81-6 — Integrity matrix owner-of-record**. PMO runs the matrix vs each `role_owner` self-certifies per area? Default = **PMO + System Owner** produce matrix; **area role_owners** sign off rows for their area (lightweight inline-ratify batch). Ratify at P0.
7. **C-81-7 — Layout migration batching**. Big-bang path move (one painful day) vs wave-by-plane (many small PRs, less blast radius). Default = **wave-by-plane** per Initiative 22 README. Ratify at P0.
8. **C-81-8 — Named-milestone schema design** (Wave 2 strand). `<I_ID>-<PURPOSE_SLUG>` (no embedded sequence number; YAML frontmatter carries phase position) **vs** `<I_ID>-M<NN>-<PURPOSE_SLUG>` (orderable but reintroduces magic numbers) **vs** `<I_ID>:<PURPOSE_SLUG>` (colon separator awkward in markdown anchors). Default = `<I_ID>-<PURPOSE_SLUG>` (the simplest stable form). Ratify at **P0** with finalisation at P3 once first migration wave reveals corner cases.
9. **C-81-9 — Validator strictness on first rollout**. Fail-on-unresolved (default) **vs** warn-only-first-pass for 1-2 weeks **vs** allowlist mode (specific files exempt during transition). Default = **fail-on-unresolved** with an **explicit allowlist** for cross-initiative-not-yet-migrated references during the migration wave only; the allowlist must be empty at P3 close. Ratify at **P3**.
10. **C-81-10 — Closed-initiative migration policy**. Migrate closed-initiative roadmaps to named milestones too (treats them as live cross-references) **vs** treat closed initiatives as **frozen historical records** never retroactively edited (default; matches `files-modified.csv` precedent). Default = **frozen**: validator allowlist excludes `<NN-slug>/` paths where `INITIATIVE_REGISTRY.csv` row carries `status=closed`. Ratify at **P3** as **D-IH-81-J**.

## 6. Decision preview (D-IH-81-* rows likely to mint)

| ID | Question | Owner | Status entering plan | Close-out phase |
|:---|:---|:---|:---:|:---:|
| D-IH-81-A | Retrofit mode (continuous vs absorbed) | People Operations Lead | open | P0 |
| D-IH-81-B | No-addendum-needed threshold | People Operations Lead | open | P0 |
| D-IH-81-C | Author posture (role_owner vs single-agent batch) | People Operations Lead | open | P0 |
| D-IH-81-D | Forward-extension to non-SOP canonicals | People Operations Lead | open | P9 |
| D-IH-81-E | Per-area register-specific jargon-scan extension | System Owner | open | P0 |
| **D-IH-81-F** | **Integrity matrix methodology + PASS threshold** — what constitutes "CLOSED-P1"? | PMO + System Owner | open | **P1** |
| **D-IH-81-G** | **Layout migration wave plan** — which root files move in which PR; deprecation-alias policy | Data Architect + Compliance Officer | open | **P2** |
| **D-IH-81-H** | **Named-milestone schema vocabulary** — final ID format + frontmatter `milestones:` array shape + body parenthetical convention | System Owner + PMO | open | **P0** charter (finalised P3 if migration reveals corner cases) |
| **D-IH-81-I** | **Validator wiring scope + strictness** — `validate_hlk.py` umbrella + `release-gate.py` + `pre_commit` profile + allowlist policy for transition window | System Owner | open | **P3** |
| **D-IH-81-J** | **Closed-initiative frozen-reference policy** — closed roadmaps never retroactively migrated; validator allowlist excludes them | PMO | open | **P3** |

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
| **R-IH-81-8** | **Named-milestone migration mid-flight breakage** — references go stale during the transition window if retrofit phases reach for milestones not yet migrated | M | M | C-81-9 default = explicit transition allowlist with hard P3-close empty-allowlist check; **P3 ships ahead of P4-P8** so retrofit phases use named milestones natively |
| **R-IH-81-9** | **Validator over-strict** — false positives on legitimate prose mentions (e.g., "I82 P2" in a discussion paragraph not intended as cross-ref) block unrelated commits | L | M | Validator scopes only **markdown link targets** + **frontmatter `milestones:` arrays** + **explicit cross-reference paragraphs** (heuristic: in lists or bold-emphasis markers); free prose `I82 P2` mentions are warn-only with allowlist override |
| **R-IH-81-10** | **Closed-initiative frozen-reference policy mis-applied** — agents migrate closed roadmaps in well-meaning sweeps, polluting historical record | L | M | D-IH-81-J ratifies the policy; validator's allowlist mechanically enforces it; cursor-rule extension to `akos-planning-traceability.mdc` codifies it for future plan authors |

## 8. Forward-link to I80 + I82 + I83

This candidate absorbs the I80 P6 forward-charter (retrofit bodies) **and** formalises two operator requests on 2026-05-16: (a) a **deterministic vault KB integrity baseline** + **Compliance forward-layout reorganisation**; (b) **planning-surface integrity** via **named milestones** + **Class B drift validator** + **historical regression sweep** as a long-term governance pattern.

- **I80** operationalised pairing at contract level (`SOP-META`, `KNOWLEDGE_PAIRING_REGISTRY`, validators). **I81** proves end-to-end **vault + planning-surface integrity**, **relocates cramped compliance artefacts** without losing SSOT, and **structurally eliminates Class B drift** by replacing magic-number cross-references with FK-resolved named milestones.
- **[I82](i82-holistika-capability-doctrine-and-commercial-readiness.md)** consumes **I81 P1 outputs** (`kb-integrity-matrix-*`) when minting **`CAPABILITY_REGISTRY`** and activates **Talent** in `baseline_organisation.csv`. Recommended dependency: **I82-CAPABILITY-REGISTRY-MINT (currently I82 P2) gates on I81 P1 integrity CLOSED OR explicit operator waiver** (`D-IH-82-PREREQ`); **I82-TALENT-ACTIVATION (currently I82 P1)** is the canonical-CSV gate that unlocks downstream organisational work. Once I81 P3 ships, all I82 + I83 cross-references migrate to named-milestone form (Wave 1 of the migration deliverable).
- **[I83](i83-ai-archivist-and-kirbe-ingestor.md)** depends on **I82-USE-CASE-ARCHIVE (currently I82 P4)** closed before I83 P0 charter — references will use the named form post I81 P3.

**Long-term pattern**: named milestones are a permanent vocabulary across **all future initiatives**, not a one-shot I81 deliverable. Cursor rule extension (`akos-planning-traceability.mdc` §"Plan-quality bar") locks this in so future plan authors inherit it by default.

Until I81 promotes (or scoped slice lands), pairing contract remains binding for net-new SOPs; existing monolithic SOPs stay valid readers; magic-number cross-references remain operator-discipline-gated rather than mechanically validated.

## 9. SOC posture

This candidate stub contains: zero secrets, zero API keys, zero raw GOI/POI mappings, zero PII. SOP filename slugs are public-naming-safe.

## 10. Cross-references

- Forward-charter origin: [I80 master roadmap](../80-i79-lessons-learned/master-roadmap.md) + [I80 P6 UAT](../80-i79-lessons-learned/reports/p6-uat-2026-05-16.md) + [I80 P6 integration verification](../80-i79-lessons-learned/reports/p6-integration-verification.md)
- Pattern doctrine: [`PEOPLE_DESIGN_PATTERN_LIBRARY.md` §pattern-sop-addendum-split](../../references/hlk/v3.0/Admin/O5-1/People/canonicals/PEOPLE_DESIGN_PATTERN_LIBRARY.md)
- Authoring contract: [`SOP-META_PROCESS_MGMT_001.md` §Body and Addendum split](../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/SOP-META_PROCESS_MGMT_001.md)
- [`KNOWLEDGE_PAIRING_REGISTRY.csv`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/KNOWLEDGE_PAIRING_REGISTRY.csv) + [`scripts/validate_knowledge_pairing_registry.py`](../../../scripts/validate_knowledge_pairing_registry.py) (I80 P6.5; D-IH-80-H)
- [`scripts/validate_process_list_pairing.py`](../../../scripts/validate_process_list_pairing.py)
- Compliance forward layout convention: [`canonicals/README.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/README.md) + [`PRECEDENCE.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md)
- Planning-surface artefacts to mint at P3: `akos/hlk_planning_milestone.py` + `scripts/validate_planning_cross_refs.py` + `tests/test_planning_cross_refs.py` + `reports/p3-class-b-regression-sweep-<YYYY-MM-DD>.md`. Cursor-rule extension target: [`akos-planning-traceability.mdc`](../../../.cursor/rules/akos-planning-traceability.mdc) §"Plan-quality bar".
- Class B regression sweep precedent (one-shot historical baseline shipped 2026-05-16 as the inline-ratify response that proved the gap): `INITIATIVE_DEPENDENCIES.md` §5 history line dated 2026-05-16 evening; commit `76838d3` (regression-fix wave) is the empirical evidence informing the validator's rule set.
- DAMA-DMBOK 2.0 Metadata Management knowledge area (paired-file + registry granularity rationale; named-milestone schema is "metadata about cross-references" — same knowledge area).
