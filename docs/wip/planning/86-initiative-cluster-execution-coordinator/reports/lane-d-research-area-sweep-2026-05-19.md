---
intellectual_kind: lane_findings_and_design_report
parent_initiative: INIT-OPENCLAW_AKOS-86
parent_wave: Wave H — I86 cluster burndown
lane: Lane D — Research Area sweep + Combo C+D design
sharing_label: internal_only
authored: 2026-05-19
last_review: 2026-05-19
linked_decisions:
  - D-IH-86-T  # cluster burndown plan
  - D-IH-86-O  # Option 5 default posture (conflict surfacing)
  - D-IH-79-A  # People mega-charter
  - D-IH-79-H  # akos-people-discipline-of-disciplines.mdc mint
  - D-IH-70-S  # Research as top-level area
  - D-IH-70-Q  # Talent monolith split → People restructure
  - D-IH-84-G  # Research = meta-discipline that audits substrates
  - D-IH-80-E  # inline-ratify-craft skill canonicalisation
  - D-IH-71-CLOSURE  # baseline_organisation + process_list latest tranche
linked_runbooks: []
status: draft
role_owner: Founder (Research Head) + System Owner
co_owner_role: People Operations Manager
language: en
purpose: |
  Single deliverable for Lane D of Wave H: a read-only sweep of the Research
  area (internal + external) + a fully drafted design for the operator-ratified
  COMBO C+D disposition: NEW People canonical RESEARCH_HEAD_DISCIPLINE.md +
  NEW cursor rule akos-applied-research-discipline.mdc + EXTENSION to the
  inline-ratify-craft skill. NOT a master-roadmap; NOT a phased plan; a
  ratify-bait artifact that the parent coordinator will use to author the
  final three files after operator approval.
---

# Lane D — Research Area Sweep + Combo C+D Design (Wave H)

## 0. One-paragraph executive summary

Holistika's Research area is **structurally well-developed** but **doctrinally under-codified for the Research-Head-as-operator scenario the operator named**. The area exists at `v3.0/Research/` as a top-level area with four discipline charters (Methodology / Intelligence / Diagnosis / Validation per D-IH-70-S); eight Research roles exist in `baseline_organisation.csv` (Holistik Researcher as Research Area Head + Lead/Senior/Private + Intelligence/OSINT/HUMINT analysts + Trainee); 30+ `hol_resea_*` process rows exist in `process_list.csv`; a Trello research-playlist registry maps directly to the operator's mentioned "playlist of researches"; `SUBSTRATE_LANDSCAPE_DOCTRINE.md` already names Research as the **meta-discipline that audits which substrates earn canonical status** (D-IH-84-G); and `docs/wip/intelligence/` is Research-owned Tier-1 WIP. What is **missing** is a single canonical that codifies **how the operator (and AICs after them) does research-first canonical authoring as a daily discipline** — the meta-discipline of "research-backing every canonical/rule/decision rather than authoring from first principles or repo state alone". The Combo C+D disposition fills exactly that gap: a People canonical (pattern-shaped, since People mints patterns for other areas to author against per `akos-people-discipline-of-disciplines.mdc`), a cursor rule (always-applied; mechanically enforces research-first), and a skill extension (the inline-ratify-craft Principle 1.5 distinguishing evidence-sweep from research-sweep). The operator's framing "I don't think it's that new" is **structurally correct** — the proposed artifacts are a `last_review`-style polish layer over an already-existing area, not a greenfield invention.

## 1. Operator framing (verbatim)

> *you need to sweep the research area to propose the solution, it's a best effort combo of C and D but I don't think it's that new. I literally single-handedly created everything you see here at Holistika by researching. I noted some of them but never had a proper governance nor continuity. Trello has research, I have playlist of researches. I even created IRE at first to store research material I had and when I saw we had so many sources I had to govern that. We have tons of opportunities in research area that have not been [much] explored. So I trust you to research internally and externally and help me take this Research Area to true v3.1 level and properly ensure all areas are covered in their manifesto/baseline processes.*
> — operator, 2026-05-19, Wave H Lane D dispatch.

Two anchors derived from this framing:

1. **The operator IS the Research Head today.** Per `baseline_organisation.csv` L12, the **Holistik Researcher** role is "Research Area Head" and reports to O5-1 — and the operator is the only individual filling this role today. Every canonical, every cursor rule, every doctrine in this repo passed through the operator's research-then-author pattern. The Combo C+D artifacts codify this existing practice; they do not invent it.
2. **Continuity is the unmet need, not the practice.** The operator named that they "noted some of them but never had a proper governance nor continuity". The Combo C+D artifacts close exactly this gap: they make the operator's tacit research discipline **transmissible** to AICs (per I76 candidate; Madeira-as-method) and **enforceable** mechanically (cursor rule + validator surface, future-tracked).

The scratchpad entry (`operator-scratchpad.md` L64) that triggered this lane reinforces both anchors: *"We're doing an excellent research job to justify and back our decisions up. Please ensure we are continuously using and properly enriching and backfilling canonicals and relevant artifacts with research material, thinking as a Researcher Head. This is an espectacular case of using applied research, which is a hot topic today and a competitive advantage if properly industrialized."*

## 2. Internal sweep — what already exists in the Research area

### 2.1 Research area at v3.0/Research/ (4 disciplines)

Promoted from `Admin/O5-1/Research/` sub-area to `v3.0/Research/` top-level area per D-IH-70-S (2026-05-12). Four discipline charters:

| Discipline | File | Status | Role owner | Mission (one-sentence) |
|:---|:---|:---|:---|:---|
| **Methodology** | `v3.0/Research/Methodology/canonicals/METHODOLOGY_DISCIPLINE_CHARTER.md` | active | KM Officer + Research Analyst | *How we research* — pillars + technique catalog + deep-research apparatus. |
| **Intelligence** | `v3.0/Research/Intelligence/canonicals/INTELLIGENCE_DISCIPLINE_CHARTER.md` | active | Research Analyst + KM Officer | *What we collect* — HUMINT + OSINT + Intelligence Matrix + per-engagement cadence. |
| **Diagnosis** | `v3.0/Research/Diagnosis/canonicals/DIAGNOSIS_DISCIPLINE_CHARTER.md` | active | Research Director + Research Analyst | *What's wrong* — engagement / system / methodology diagnostic surfaces (F-51 codified). |
| **Validation** | `v3.0/Research/Validation/canonicals/VALIDATION_DISCIPLINE_CHARTER.md` | active | KM Officer + Research Director | *What's true* — source-reliability grading + cross-source corroboration + evidence-confidence scoring. |

Parent canonical: `v3.0/Research/canonicals/RESEARCH_AREA_CHARTER.md` (also active). Four-discipline ontology **mirrors** the Brand sub-discipline ontology (Brand: AV / Copywriter / Design / UX-Designer), per RESEARCH_AREA_CHARTER §2.

**Key load-bearing claim** (RESEARCH_AREA_CHARTER §6 *"Authoring vs consuming rule"*): Research **AUTHORS** investigative artifacts (intelligence reports, methodology pillars, diagnostic templates, validation rubrics); other areas **CONSUME** those artifacts as inputs to their own work. The Combo C+D artifacts respect this boundary — they codify the Research-Head's research-first authoring discipline, they do not push Research into consuming-area territory.

### 2.2 Research roles in baseline_organisation.csv (8 rows)

From `baseline_organisation.csv` grep against `Research`:

| row | role_name | description (one-line) | reports_to | access_level |
|:---|:---|:---|:---|:---|
| 12 | Holistik Researcher | Research Area Head; peer to CFO/CPO/COO/CMO/CDO/CTO; governs R&L, HUMINT, OSINT, Intelligence Matrix, deep-research, 4 methodology pillars | O5-1 | 4 |
| 13 | Lead Researcher | Research Team Lead; supervises Senior/Private/HUMINT | Holistik Researcher | 3 |
| 14 | Senior Researcher | Experienced researcher with Private-level access | Lead Researcher | 2 |
| 15 | Private Researcher | Entry-level Community-access | Lead Researcher | 1 |
| 16 | Intelligence Analyst | Operates the Intelligence Matrix | Holistik Researcher | 4 |
| 17 | OSINT Analyst | Open-source intelligence | Holistik Researcher | 3 |
| 18 | HUMINT Specialist | Human-source intelligence | Lead Researcher | 3 |
| 56 | Holistik Researcher Trainee | Apprentice tier added P13.4 | Holistik Researcher | 2 |

Plus **Research Director** named in RESEARCH_AREA_CHARTER §3 + DIAGNOSIS_DISCIPLINE_CHARTER §3 as a **planned baseline_organisation row** deferred to P8 §8.5 (People restructure tranche) — **not yet in the CSV**.

The Holistik Researcher (Research Area Head) row L12 is the canonical anchor for the operator-as-Research-Head framing. The proposed canonical's `role_owner` frontmatter is **Founder (acting as Holistik Researcher) + System Owner co-steward** — consistent with this row's authority.

### 2.3 Research processes in process_list.csv (30+ rows)

Sample (from `grep ,Research, process_list.csv | head -15`):

- `hol_resea_prj_1` — Holistika Research and Methodology (project-grain, role_owner=Holistik Researcher).
- `hol_resea_ws_1..5` — workstreams: HUMINT Techniques, Intelligence Matrix Operations, Methodology Pillars, Deep Research, Research Techniques.
- `hol_resea_dtp_94..200+` — concrete processes: Enriched Interview, Focus group, HxPESTAL, Create Analogy, 6 Ws, Place in Intelligence Matrix, Classify Intel, Output 1, etc.

`grep -c "research" process_list.csv` → **579 matches** across the file (across many areas' processes that consume research outputs). The Research area is dense in `process_list.csv`.

**Gap relative to the proposed canonical**: there is no `hol_resea_dtp_*` row for **"research_canonical_authoring"** (the meta-process of authoring a canonical / rule / doctrine using research-first discipline) nor for **"applied_research_audit"** (the meta-process of auditing whether canonical assets carry sufficient research backing). These are forward-charter C-NN-B candidates (§7); they are not authored today because per SOP-META order, canonical-doctrine landing precedes `process_list.csv` row mint for net-new item_ids.

### 2.4 Existing Research-area canonicals beyond the 4 charters

- **`v3.0/Admin/O5-1/Research/Methodology/canonicals/SUBSTRATE_LANDSCAPE_DOCTRINE.md`** — minted I84 P3 per D-IH-84-G. Codifies Research as the **meta-discipline that audits which substrates earn canonical status**. Directly relevant precedent for the proposed canonical: the discipline-of-disciplines pattern applied recursively to Research-area is already a ratified doctrine. The proposed `RESEARCH_HEAD_DISCIPLINE.md` extends this pattern from "substrate audit" to "general research-first canonical authoring".
- **`v3.0/Admin/O5-1/Research/Methodology/canonicals/SOP-RESEARCH_SUBSTRATE_AUDIT_CADENCE_001.md`** — paired SOP (cadence: quarterly + event-triggered); reference SOP shape the proposed canonical's anti-patterns section will cite.
- **`v3.0/Admin/O5-1/Research/Intelligence/canonicals/SOP-IO_ELICITATION_DISCIPLINE_001.md`** + **`SOP-IO_INTELLIGENCE_REPORT_001.md`** + **`SOP-REGULATOR_RELATIONSHIP_001.md`** + **`SOP-RESEARCH_ENGAGEMENT_TRIGGER_001.md`** — Intelligence-discipline SOPs (migrated from `Admin/O5-1/Operations/IntelligenceOps/` per D-IH-70-W).
- **`v3.0/Research/Intelligence/canonicals/GOI_POI_STANCE_DOCTRINE.md`** — GOI/POI stance doctrine (I21 lineage).
- **`v3.0/Admin/O5-1/Research/Intelligence/canonicals/dimensions/INTELLIGENCEOPS_REGISTER.csv`** — register canonical.
- **`v3.0/Admin/O5-1/Research/RESEARCH_VS_TECH_LAB_ENTITY_RATIONALE_2026-04.md`** — Research-vs-Tech-Lab entity-formation rationale; sets the precedent that Research leads first and Tech Lab represents productization. Cited in the proposed canonical's §1 Purpose.
- Empty technique folders (kept via `.gitkeep`): `Research Techniques/`, `Methodology Pillars/`, `OSINT Operations/`, `HUMINT Techniques/`, `Intelligence Matrix/`, `Deep Research/`. These are P4.5-wave-3 migration targets per RESEARCH_AREA_CHARTER §4.

### 2.5 Research-related WIP topology

- **Tier 1 WIP**: `docs/wip/intelligence/` (Research-owned per WORKSPACE_BLUEPRINT §17). Currently holds:
  - `2026-05-10-suez-webuy-procure-to-pay/` — per-engagement intelligence-collection working space.
  - `substrate-audit-2026-Q2/` — quarterly substrate-audit folder per SOP-RESEARCH_SUBSTRATE_AUDIT_CADENCE_001.
  - Root `README.md` declaring promotion-ladder semantics.
- **Trello backlog registry**: `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/RESEARCH_BACKLOG_TRELLO_REGISTRY.md` — canonical mapping from external Trello board `67697e19c67277de7ae1a85c` to topic_id candidates. **This is the registry surface for the operator's "playlist of researches" mention.** 16 rows; covers Office Automation, People, Security & Intelligence, Design, System Design, Content & Channel Strategy, Macro Investment, AI, Politics, Social, Logic, Legal, UX/CRM, plus MADEIRA-research-radar. The registry frames Trello as **not SSOT** — Trello is the upstream candidate surface, the v3.0 vault is canonical. This is exactly the operator's lived practice.

### 2.6 Research mentions across other v3.0 area canonicals (coverage scoring)

| Canonical | `grep -c research` | Quality of mention | Verdict |
|:---|---:|:---|:---|
| `People/canonicals/HOLISTIKA_ORGANISING_DOCTRINE.md` | ~14 | Operator's verbatim: *"We are not research, but we manage the human way of approaching anything."* + multiple operational references (process singularity examples cite Research) | **Adequate** — People explicitly differentiates from Research; Research consumers cited by example. |
| `People/canonicals/HOLISTIKA_AGENTIC_DOCTRINE.md` | 3 | Cross-area substrate-audit cross-references | **Thin** — Agentic doctrine mentions Research only as a substrate audit cross-link, not as a research-discipline pillar of agentic operations. |
| `People/canonicals/PEOPLE_DESIGN_PATTERN_LIBRARY.md` | ~10 (instance-level) | Research cited as an example consumer of patterns (Pattern: Persona Registry, IntelligenceOps Register, etc.) | **Adequate at instance-level**; **missing the meta-pattern** of "research-first canonical authoring" as a People design pattern row. |
| `Operations/PMO/canonicals/KB_HUMAN_READABILITY_CHARTER.md` | **0** | No mention of research backing for the readability discipline | **Gap** — KB readability decisions are based on operator tacit knowledge, not cited research; should reference Nielsen Norman Group / readability research. |
| `Envoy Tech Lab/canonicals/AGENTIC_FRAMEWORK_LANDSCAPE.md` | 1 | Probably the SUBSTRATE_LANDSCAPE cross-link | **Thin** — framework selection lacks explicit research-comparison-matrix backing. |
| `Marketing/Brand/canonicals/BRAND_BASELINE_REALITY_MATRIX.md` | 0 hits on "research backing" / "evidence base" / "research-backed" patterns | The matrix is grounded in HUMINT tradecraft (US Army FM 2-22.3) but the citation is a single footnote in cursor rule `akos-brand-baseline-reality.mdc`; the matrix doctrine itself doesn't explicitly carry an "Evidence base" section | **Partial** — research grounding exists implicitly (FM 2-22.3) but is not surfaced as a maintained "Evidence base" structure that future revisions can append to. |
| `Admin/O5-1/Research/Methodology/canonicals/SUBSTRATE_LANDSCAPE_DOCTRINE.md` | dense | Full research-grounded doctrine; quarterly cadence; cross-references industry sources | **Exemplary** — the proposed canonical inherits this shape. |

**Pattern**: research-grounding density is **high in Research-area canonicals**, **moderate in People doctrine + brand**, **thin in Tech + Operations**, **absent in KB readability**. This maps cleanly to the per-area gap analysis in §6.

### 2.7 Existing cursor rules touching research discipline (closest analogs)

- **`akos-inline-ratification.mdc`** Principle 1 ("Run the evidence sweep first") — closest analog. The skill extension proposed in §7.C distinguishes evidence-sweep (already covered) from research-sweep (new).
- **`akos-planning-traceability.mdc`** §"Plan-quality bar" — requires "Inline decision-log preview" and "Inline risk register" but does **not** require an Evidence-base / Research-citation row.
- **`akos-people-discipline-of-disciplines.mdc`** Rule 1 — People mints patterns + Rule 4 anti-jargon discipline. The proposed cursor rule respects Rule 1 explicitly (the People-canonical home is the right place per pattern-mint; the cursor rule is the always-applied operationalisation).
- **`akos-governance-remediation.mdc`** — names HLK compliance governance + asset classification but does not require research-backing in decisions.
- **`akos-executable-process-catalog.mdc`** Rule 1 — paired SOP + runbook discipline. The proposed canonical follows this (paired with a future runbook; deferred to forward-charter as the canonical sit on operator-discipline-enforced posture until a `validate_research_backing.py` validator earns its place).

**No existing rule** mechanically enforces "research-first authoring of new canonicals" or "external-source citation in decision rows". The proposed `akos-applied-research-discipline.mdc` fills this gap.

### 2.8 Existing skills touching research craft (closest analogs)

- **`.cursor/skills/inline-ratify-craft/SKILL.md`** Principle 1 (evidence sweep). Extension proposed in §7.C.
- **`.cursor/skills/hlk-planning-system/SKILL.md`** (in personal skills). Roadmap-authoring skill; cross-references DAMA + SSOT but does not explicitly carry research-craft as a principle.
- **`.cursor/skills/archivist/SKILL.md`** — doc-quality maintenance.

The proposed extension to `inline-ratify-craft` is the highest-leverage placement because every inline-ratify gate is a candidate for research-sweep.

### 2.9 IRE archaeology — operator's mention not found in repo

The operator named *"I even created IRE at first to store research material I had"*. Repo-wide `grep -i "IRE\|Information Research Engine"` returns no IRE-specific hits — only `external-render-discipline.mdc` (unrelated string match). This is consistent with operator framing: IRE was the **pre-vault** Drive-folder artifact (predates v3.0). Not chased further; the proposed canonical's §6 Backfill protocol mentions the IRE precedent as folkloric origin without requiring a verifiable repo trace.

The `docs/references/hlk/previous-project-for-product-owner-example-only/` folder is a **Shopify Plugin Project**, not the IRE — confirmed by reading `product-requirements.md`. Not the IRE.

### 2.10 Summary of what already works + what's missing

**Already works**:

- 4-discipline Research area at v3.0/Research/ (Methodology/Intelligence/Diagnosis/Validation).
- 8 Research roles in baseline_organisation.csv.
- 30+ hol_resea_* process rows.
- 8 Research-area SOPs (4 IntelligenceOps SOPs + Substrate Audit Cadence + Intelligence Discipline charters + GOI/POI Stance + Engagement Trigger).
- Tier 1 WIP at `docs/wip/intelligence/` (Research-owned).
- Trello backlog registry as the operator's "playlist" surface.
- SUBSTRATE_LANDSCAPE_DOCTRINE as the discipline-of-disciplines precedent.
- Inline-ratify-craft Principle 1 (evidence sweep) as the closest authoring-discipline analog.

**Missing** (the gaps the Combo C+D artifacts fill):

1. A **single canonical** that frames the Research Head as a **doctrine-author discipline** — i.e., HOW the operator (and AICs after them) does research-first canonical authoring, applied at every canonical / rule / doctrine / decision mint.
2. A **cursor rule** that mechanically calls out research-first authoring as always-applied discipline (instead of relying on inline-ratify Principle 1 to be invoked at every gate).
3. A **skill extension** that names the **evidence-sweep vs research-sweep** distinction explicitly (closest existing language collapses both into "evidence sweep").
4. A **maintained Evidence-base section** structure on existing doctrine canonicals — so revisions can append research material without inventing schema each time.
5. **process_list.csv rows** for the meta-processes (research_canonical_authoring, applied_research_audit) — forward-charter; not minted today per SOP-META order.

The Combo C+D artifacts address gaps 1-3 directly; gap 4 is addressed by the canonical's §6 Backfill protocol; gap 5 is flagged as forward-charter C-NN-B in §7.

## 3. External research findings

### 3.1 ResearchOps Community of Practice — 8 Pillars (canonical 2018+)

The ResearchOps Community (founded by Kate Towsey via the `#WhatisResearchOps` 2018 global workshops; Brigette Metzler, Emma Boulton, Holly Cole, Tomomi Sasaki as named co-contributors) canonicalised an **8-Pillar framework** for research operations:

1. **Environment** — the physical + digital infrastructure that hosts research activity.
2. **Scope** — the boundaries of what research the org does and does not do.
3. **People** — who can conduct research; how non-researchers are supported.
4. **Organisational context** — research's relationship with adjacent functions (product, eng, design).
5. **Recruitment and admin** — participant pipelines + scheduling + incentive logistics.
6. **Data and knowledge management** — capture, storage, retrieval, synthesis of research outputs.
7. **Governance** — consent, retention, privacy, ethics, IP.
8. **Tools and infrastructure** — software and platforms for recruiting, interviewing, analysis, repository.

Source: ResearchOps Community "About" + Medium republications by Atlantic Building team. The 8-Pillar framework is the **single most-cited canonicalisation of ResearchOps as a discipline**.

### 3.2 Dovetail's commercial 8-Pillar variation

Dovetail (the commercial ResearchOps platform) publishes an 8-pillar variant emphasising the repository-tooling layer:

1. People
2. Scope and culture
3. Participant management
4. **Asset management** — raw materials (recordings, transcripts, notes) for storage / retrieval.
5. **Knowledge management** — synthesised findings + searchable repository.
6. Tools
7. Governance
8. [Eighth pillar not surfaced in cached excerpt]

Notable: Dovetail explicitly **separates asset management (raw) from knowledge management (synthesised)**. This separation is structurally similar to Holistika's Tier 1 WIP (raw + synthesis-in-progress) vs canonical (synthesised + ratified). Holistika's `docs/wip/intelligence/` is the **raw + WIP-synthesis** surface; `docs/references/hlk/v3.0/Research/` is the **canonical synthesised surface**. The pattern is well-precedented.

### 3.3 Kate Towsey — *Research That Scales: The Research Operations Handbook* (Rosenfeld Media, 2024)

Book canonicalises the 8 Pillars + introduces the "ResearchOps Venn diagram" + names "eight elements of research operations" as the practitioner-facing taxonomy. Author founded the ResearchOps Community + the `#WhatisResearchOps` movement.

**Relevance to Holistika**: the book frames ResearchOps as **the discipline that scales the impact of research across an organisation by minting roles, tools, and processes**. This is precisely the operator's framing — "applied research as competitive advantage **if properly industrialised**". The proposed canonical's §3 5-Pillar adaptation is a Holistika-fit translation of the 8 Pillars (not a blind copy — see §7.A §3 for the reduction rationale).

### 3.4 Applied research as competitive moat — Bell Labs / Xerox PARC / OpenAI / Anthropic lineage

Industry consensus 2025-2026 (per the WebSearch sweep): **innovation is no longer the differentiator; the speed of converting research breakthrough → commercialisation is**. Bell Labs and Xerox PARC failed not from research quality (Bell Labs alone filed ~503 patents/year; PARC invented the GUI + Ethernet) but from the transformation gap — the lag between breakthrough and product. The 2026 AI-lab landscape (OpenAI / Anthropic / DeepMind) inherits this lesson: their moat is **research → product velocity + governance of mission as capital scales**, not raw research output.

**Relevance to Holistika**: the operator's "applied research as competitive advantage **if properly industrialised**" framing maps to this lineage. The proposed canonical's §1 Purpose names this anchor explicitly. The cursor rule's RULE 1 + RULE 2 mechanise the "industrialisation" half — every canonical / doctrine / rule mint cites its research backing, so the gap between breakthrough (in the operator's Cursor-session researching) and codification (in v3.0 canonical) shrinks to one commit.

### 3.5 DAMA-DMBOK 3.0 — no dedicated Research Management knowledge area; Metadata Management as proxy

DAMA-DMBOK 3.0 (in active development as of Q1 2026; quarterly town-halls; Triple Helix governance: 11-member Editorial Board + 7-member CDMP Review Panel + global community) maintains **11 core knowledge areas**. None of them is explicitly "Research Management". The closest proxies:

- **Metadata Management** — "data about data" for understanding / governance / accessibility; catalogs tracking lineage / definitions / usage.
- **Data Governance** (renamed "data governance function" in 3.0; now includes AI governance + ethics).

**Relevance**: the proposed canonical's §3.4 "Source-and-Provenance Metadata" pillar inherits DAMA-DMBOK Metadata Management semantics — every research-backed claim in a canonical carries a `source_taxonomy` + `confidence_level` annotation (FK into Holistika's existing `compliance/source_taxonomy.md` + `confidence_levels.md` canonicals). DAMA-alignment is preserved.

### 3.6 Engineering-side research-repository patterns

Survey of engineering-research-repo conventions (taclab-research/science-repo-practices; the-turing-way/reproducible-project-template; PPLS Open Research):

- Directory structure: `analysis/` + `code/` + `workflows/` + `data/` + `input/` + `output/` (latter two excluded from VC).
- Lab notebook format: Title + one-sentence summary / Motivation-Aims / Methods overview with actionable items / Main conclusions / Data input-output / Key parameters / Markdown narrative between code chunks.
- READMEs: Vision/Mission + Roadmap/Milestones + Team roles + Contributing + Licensing.
- 2026 practices: type hints + ruff + basedpyright + Hydra configs + uv builds + pre-commit + GitHub Actions + AGENTS.md for LLM tools.

**Relevance**: most of these are already in Holistika (Python type hints + ruff + pre-commit + GitHub Actions runners + per-repo READMEs). The lab-notebook format maps to the **synthesis docs** Holistika already authors under `docs/wip/intelligence/<engagement>/checkpoints/`. No new tooling required for the Combo C+D scope; the gap is doctrinal (how to author + cite + backfill), not infrastructural.

### 3.7 What the external sweep does NOT find

- No industry doctrine that maps cleanly to the operator's specific scenario: **"founder is single-person research-head + future AIC inheritor + writing canonical doctrine, not customer-facing UX research"**. The closest is Kate Towsey's framing + Bell Labs lineage, but neither codifies the AIC-continuity dimension. **The Combo C+D artifacts are partly novel-framing** in this dimension — Holistika is contributing to the industry conversation, not merely consuming it.
- No mature consensus on **research-backed-by-default doctrine authoring** as an engineering practice. ADRs (Architecture Decision Records, Michael Nygard / ThoughtWorks 2011 lineage) come closest; they recommend "decision drivers" and "considered alternatives" sections but stop short of mandating external-source citation. **Holistika's proposed RULE 2** (external source citation on novel-framing canonical / rule mints) is **stronger than ADR practice** as conventionally applied.

## 4. Synthesis — per-area gap analysis

Operator's scratchpad framing (L65): *"Same with People, Marketing, Tech, Data, and of course OPS, remember to check everytime what artifacts and canonicals need to be enriched per wave."*

Per-area research-coverage assessment:

| Area | Coverage today | Gap | Backfill priority |
|:---|:---|:---|:---|
| **Research** (the area) | Exemplary at SUBSTRATE_LANDSCAPE_DOCTRINE level; 4-discipline charters carry stubs but consistent shape; Trello registry tracks playlist | **Meta-discipline gap**: no canonical frames Research Head as doctrine-author discipline | **Highest** — this is the Combo C+D primary fill. |
| **People** | HOLISTIKA_ORGANISING_DOCTRINE carries operator's verbatim voice; cites Research as a peer area; PEOPLE_DESIGN_PATTERN_LIBRARY lacks a "Research-first canonical authoring" pattern row | Pattern-row gap: PEOPLE_DESIGN_PATTERN_REGISTRY.csv should carry a `research_first_canonical_authoring` row; HOLISTIKA_AGENTIC_DOCTRINE thin on Research-as-pillar-of-agentic-ops | **High** — pattern-row mint can ride a future People tranche; agentic doctrine extension is a follow-up. |
| **Marketing** | BRAND_BASELINE_REALITY_MATRIX is grounded in HUMINT tradecraft (FM 2-22.3) but lacks explicit Evidence-base section that downstream revisions can append to; BRAND_VISION grounded but lacks `evidence_base` slot | Evidence-base structural gap on brand canonicals; trivial to add (frontmatter pattern) | **Medium** — backfill in next BBR revision wave. |
| **Tech** | AGENTIC_FRAMEWORK_LANDSCAPE has 1 research mention (cross-link); framework selection lacks visible comparison-matrix backing in-doc (the matrix lives in I84 substrate audit reports under wip/intelligence) | **Medium gap**: framework rows lack inline citation to the substrate-audit evidence base; should add `audit_source_url` per row (already in SUBSTRATE_REGISTRY.csv schema but not consistently surfaced in framework-landscape canonical) | **Medium** — easy to fold into next tech-canonical revision. |
| **Data** | PRECEDENCE.md classifies canonical/mirror/reference but does not declare a meta-research process for how the precedence ladder is maintained; HLK_KM_TOPIC_FACT_SOURCE.md is research-grounded by construction (fact-source contract) but does not link to source-taxonomy decision history | **Medium gap**: data-governance research backing is implicit in HLK_KM_TOPIC_FACT_SOURCE but not surfaced as Evidence-base; PRECEDENCE.md should cite the DAMA-DMBOK 3.0 alignment posture explicitly | **Medium** — fold into a future I27-class doctrine wave. |
| **Operations** | KB_HUMAN_READABILITY_CHARTER has **0** research mentions; readability decisions are operator-tacit-knowledge based; should cite Nielsen Norman Group readability research + plain-language standards | **High gap**: a charter named "human readability" with no research backing reads as authority-by-fiat | **High** — easy fix; one Evidence-base section addition. |

The proposed canonical's §6 Backfill protocol gives a uniform shape for closing all these gaps over successive waves, without authoring everything at once today.

## 5. Decisions surfaced (for parent coordinator to ratify after operator review)

| ID (suggested) | Question | Recommended option | Rationale |
|:---|:---|:---|:---|
| D-IH-86-RH-A | Where does the new canonical live: People/canonicals/ or Research/canonicals/? | **People/canonicals/** (per akos-people-discipline-of-disciplines.mdc Rule 1: People mints patterns; Research authors their own processes from those patterns) | The canonical codifies a **meta-pattern** — research-first authoring — that every area instantiates. That is People's stewardship territory. |
| D-IH-86-RH-B | Pillar count for §3: 5, 7, or 8? | **5** (Inventory / Sourcing / Synthesis / Governance / Propagation) | Holistika-fit reduction of the ResearchOps Community 8 Pillars; environment / org-context are absorbed into Inventory; people / tools are absorbed into Governance + Sourcing. Operator's "not that new" framing favors compact. |
| D-IH-86-RH-C | Should the cursor rule be `always-applied` or `selectively-applied`? | **always-applied** | Research-first authoring is a foundational posture, not a conditional one; matches the precedent of `akos-people-discipline-of-disciplines.mdc` always-applied posture. |
| D-IH-86-RH-D | Should the skill extension introduce a new Principle (1.5) or replace Principle 1? | **NEW Principle 1.5** | Principle 1 (evidence sweep) is established + ratified by D-IH-80-E; adding 1.5 distinguishes evidence-sweep from research-sweep without invalidating prior ratification. |
| D-IH-86-RH-E | Should the cursor rule include a validator hook today? | **NO** (operator-discipline-enforced at v1; flag forward-charter for `validate_research_backing.py`) | Validator design needs evidence about which canonical fields a future automated check should scan; not-yet-mature; honor operator's "not overengineered" directive. |
| D-IH-86-RH-F | Should the canonical claim a paired runbook today? | **NO** (deferred to forward-charter; status:review until paired) | Per akos-executable-process-catalog.mdc Rule 1, executable processes need pairs. The canonical itself is doctrine, not an executable process; the paired runbook would be the validator (D-IH-86-RH-E above), which is deferred. |
| D-IH-86-RH-G | Do we mint a process_list.csv row for `research_canonical_authoring` today? | **NO** (forward-charter C-NN-B) | Operator-CSV-gate discipline; net-new item_id without operator ratification of the tranche shape is out of scope for Lane D. |
| D-IH-86-RH-H | Do we add a `research_first_canonical_authoring` row to PEOPLE_DESIGN_PATTERN_REGISTRY.csv today? | **NO** (forward-charter; ride next People design pattern tranche) | Same canonical-CSV-gate discipline. |

All decisions are **recommended defaults**; parent coordinator surfaces as inline-ratify gate at operator handoff per inline-ratify-craft Principle 3.

## 6. Risks

| ID | Risk | Likelihood | Impact | Mitigation |
|:---|:---|:---|:---|:---|
| R-IH-86-RH-1 | Operator perceives Combo C+D as over-engineered ("I don't think it's that new") | **Medium** | **Medium** | §1 anchors directly cite operator's framing; canonical §1 Purpose explicitly says "codifies existing practice, doesn't invent it"; total LoC budget kept lean (canonical ~250 lines, rule ~120 lines, skill extension ~60 lines). |
| R-IH-86-RH-2 | Cursor rule causes false-positive friction on legitimate non-novel commits (bugfixes, refactors) | **Medium** | **Medium** | Rule §"When this rule does NOT apply" carves explicit exemptions for mechanical authoring, bugfix commits, refactors of already-researched canonicals, doc-only typo fixes. |
| R-IH-86-RH-3 | Skill extension dilutes Principle 1's evidence-sweep mandate by introducing optional-feeling research-sweep | **Low** | **Medium** | Principle 1.5 explicitly frames research-sweep as **conditional on novelty** (not optional); cross-references RULE 2 of the cursor rule which mechanically enforces external citation when novel framing. |
| R-IH-86-RH-4 | Folding canonical into People area creates "another People canonical" fatigue | **Low** | **Low** | The canonical is small + pattern-shaped + frontmatter-tagged for People area; PEOPLE_DESIGN_PATTERN_LIBRARY remains the human-readable pattern hub; the new canonical reads as a methodology pillar inside People's existing structure. |
| R-IH-86-RH-5 | RULE 3 (wave-closure reports require "Research enrichment" subsection) creates retroactive backfill demand on already-closed waves | **Medium** | **Low** | Rule applies prospectively only; operator can choose to backfill or not on a per-wave basis. Soft-clause language. |
| R-IH-86-RH-6 | The "operator IS the Research Head" frame becomes brittle when AICs are productionised | **Low** | **Medium** | Canonical §1 Purpose explicitly names AIC continuity as the second motivation; the canonical reads-the-same whether the executor is the human operator or a future AIC. |

## 7. Proposed designs — full draft content

### 7.A NEW People canonical: `RESEARCH_HEAD_DISCIPLINE.md`

**Target path**: `docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/RESEARCH_HEAD_DISCIPLINE.md`

**Frontmatter** (proposed):

```yaml
---
title: Research Head Discipline
language: en
intellectual_kind: people-canonical
access_level: 4
audience: J-OP;J-CO
confidence_level: A1
source_taxonomy: holistika-internal-doctrine
authors:
  - Founder (acting as Holistik Researcher / Research Area Head)
  - System Owner
co_authors:
  - People Operations Manager
  - KM Officer
last_review: 2026-05-19
last_review_by: Founder
ratifying_decisions:
  - D-IH-86-RH-A  # canonical home = People (suggested)
  - D-IH-86-RH-B  # 5-pillar shape (suggested)
status: review
register: internal
linked_canonicals:
  - HOLISTIKA_ORGANISING_DOCTRINE.md
  - HOLISTIKA_AGENTIC_DOCTRINE.md
  - PEOPLE_DESIGN_PATTERN_LIBRARY.md
  - ../../Research/canonicals/RESEARCH_AREA_CHARTER.md
  - ../../Research/Methodology/canonicals/METHODOLOGY_DISCIPLINE_CHARTER.md
  - ../../Research/Methodology/canonicals/SUBSTRATE_LANDSCAPE_DOCTRINE.md
  - ../Compliance/canonicals/source_taxonomy.md
  - ../Compliance/canonicals/confidence_levels.md
linked_cursor_rules:
  - .cursor/rules/akos-applied-research-discipline.mdc
linked_skills:
  - .cursor/skills/inline-ratify-craft/SKILL.md
companion_to:
  - HOLISTIKA_ORGANISING_DOCTRINE.md
  - ../../Research/canonicals/RESEARCH_AREA_CHARTER.md
---
```

**Body** (5 numbered sections + anti-patterns + cross-references; target ~250 lines):

```markdown
# Research Head Discipline

> The People-area pattern that names how the **Research Head** authors canonical
> doctrine, cursor rules, decision rows, and skills — research-first, by
> default, every time. Codified at I86 Wave H from the operator's framing:
> *"I literally single-handedly created everything you see here at Holistika
> by researching. I noted some of them but never had a proper governance nor
> continuity."* This canonical IS that governance and continuity.

## 1. Purpose

Holistika's canonical doctrine — every v3.0 area charter, every cursor rule,
every doctrine canonical, every load-bearing decision-register row — has been
authored single-handedly by the operator (acting as Research Area Head per
`baseline_organisation.csv` Holistik Researcher row L12) through a tacit
discipline of research-first authoring: read the repo state, sweep the
relevant industry precedent, distil to a structured option set, ratify, then
write. This canonical names that discipline so it survives two transitions:

1. **Continuity** — the operator's existing practice becomes legible to
   future-self-reading-cold and to collaborators who join the area.
2. **AIC continuity** (per [`i76-madeira-elevation.md`](../../../../../wip/planning/_candidates/i76-madeira-elevation.md))
   — when a future AIC acts as Research Head (or as Research-Head co-steward),
   the discipline transmits without operator re-explanation. AICs read this
   canonical as a doctrine and inherit the pattern.

The discipline is grounded in the industry consensus that **applied research,
properly industrialised, is a competitive moat** (per the Bell Labs / Xerox
PARC / OpenAI lineage — innovation is abundant; the differentiator is the
transformation velocity from research to commercialised governance). This
canonical industrialises Holistika's applied-research practice.

## 2. Scope (when this canonical fires)

This canonical fires whenever any of the following surfaces are authored
or revised:

- A net-new **canonical CSV** is minted (per `akos-holistika-operations.mdc`
  §"New git-canonical compliance registers" pattern).
- A net-new **doctrine canonical** is authored (any `.md` under
  `docs/references/hlk/v3.0/**/canonicals/` carrying `intellectual_kind:
  doctrine|area_charter|discipline_charter|people-canonical|
  research-area-canonical|tech-canonical|brand-canonical`).
- A net-new **cursor rule** is minted at `.cursor/rules/akos-*.mdc`.
- A net-new **skill** is minted at `.cursor/skills/*/SKILL.md`.
- A **decision-register row** is appended to `DECISION_REGISTER.csv` that
  carries `novel_framing: yes` (forward-charter field; not yet in schema).
- Any of the above is **revised** in a non-mechanical way (i.e., not a typo
  fix, not a link-rot fix, not a formatting normalisation).

This canonical does NOT fire for:

- Mechanical authoring (typo fixes, link-rot, formatting).
- Bugfix commits.
- Refactors of already-researched canonicals (when the underlying research
  base does not change).
- Per-engagement WIP synthesis (covered by Research/Intelligence discipline
  charters + Tier 1 WIP rules at `docs/wip/intelligence/`).
- Code-only changes that do not touch canonical doctrine.

When fired, the canonical guides the authoring through the 5-pillar discipline
below + the cursor rule [`akos-applied-research-discipline.mdc`](../../../../../../.cursor/rules/akos-applied-research-discipline.mdc)
mechanically enforces the minimum bar.

## 3. The 5 Research-Head pillars

Holistika-fit reduction of the ResearchOps Community 8 Pillars (Environment /
Scope / People / Organisational context / Recruitment&admin / Data&knowledge /
Governance / Tools&infrastructure — Kate Towsey + ResearchOps Community 2018):
Holistika's substrate already covers Environment, People, Tools, Recruitment
via existing canonicals (WORKSPACE_BLUEPRINT, baseline_organisation, agentic
substrate registry, engagement model registry), so the 5 pillars below name
the **operator-Research-Head-specific discipline** that does not collapse into
those existing canonicals.

### 3.1 Inventory — what does the corpus already say?

Before authoring anything new, the Research Head sweeps the existing corpus
to find what the repo already commits to. Concretely:

- `Grep` + `Glob` + `Read` over `docs/references/hlk/v3.0/**/canonicals/`
  for the topic being authored.
- `Read` of all `linked_canonicals` named in the closest sibling canonical's
  frontmatter (these are pre-curated entry points).
- `Read` of `DECISION_REGISTER.csv` for any prior ratification on the topic.
- `Read` of the relevant `process_list.csv` rows.
- `Read` of `docs/wip/intelligence/` for any in-flight synthesis on the topic.

The inventory pass is **non-negotiable** — it is the Research Head equivalent
of the inline-ratify-craft Principle 1 "Run the evidence sweep first"
(`.cursor/skills/inline-ratify-craft/SKILL.md`).

Outcome: a short Inventory paragraph in the planning notes (or the canonical's
forward Evidence-base section) naming what the corpus already commits to,
what's deliberately silent, and what would conflict if the new authoring goes
forward as drafted. The Inventory pass typically collapses 2-3 plausible
authoring directions into 1 obvious one (per inline-ratify-craft Principle 1
quantitative claim).

### 3.2 Sourcing — what does the industry already say?

When the inventory surfaces a novel framing (something the repo does not
yet commit to), the Research Head opens a sourcing pass against external
industry precedent. Concretely:

- 3-10 `WebSearch` queries on the topic, scoped to the year the decision is
  being made (2026 today; future-dated for AIC continuity).
- 1-5 `WebFetch` calls on the most authoritative sources surfaced.
- Optional: targeted reads of named precedent documents (DAMA-DMBOK 3.0,
  ResearchOps Community publications, Kate Towsey *Research That Scales*,
  Allyson Berri's writing, McKinsey / Bain / DT consulting taxonomies, etc.).

The sourcing pass is **conditional on novelty** — if the inventory pass
already converged on an obvious authoring direction, sourcing can be light
(1-2 confirmatory queries). If the inventory surfaced genuine novelty,
sourcing is heavier (5-10 queries, multiple precedent sources).

Outcome: a Sourcing paragraph naming what the industry consensus is, where
Holistika converges with it, where Holistika diverges and why. The
divergence narrative is the load-bearing claim — when Holistika diverges
from industry consensus, the canonical names the divergence + the rationale
+ the conditions under which the divergence might be revisited.

### 3.3 Synthesis — what is Holistika's lived position?

Inventory + Sourcing feed Synthesis. Synthesis is the act of distilling:

- The corpus's pre-existing commitments (Inventory).
- The industry's precedent + best practice (Sourcing).
- The operator's lived experience and tacit knowledge (Founder corpus
  per `FOUNDER_CORPUS_INVENTORY` section paths; AIC inheritors read this
  FK-only per `D-IH-76-K` access posture).
- The engagement-as-org-diagnostic feedback loop (per
  [`DIAGNOSIS_DISCIPLINE_CHARTER.md`](../../Research/Diagnosis/canonicals/DIAGNOSIS_DISCIPLINE_CHARTER.md)
  §4 — every customer engagement stress-tests Holistika's own governance).

Into a **single Holistika-position statement** that the new canonical /
rule / skill / decision codifies. The Synthesis position is the canonical's
load-bearing claim — its `intellectual_kind: doctrine` core.

Synthesis output: the canonical's body itself; the cursor rule's body itself;
the skill's principles; or the decision-register row's rationale. The
Inventory + Sourcing passes' outputs are preserved in the canonical's
**Evidence base** section per §6 Backfill protocol below.

### 3.4 Governance — provenance, classification, access

Every research-backed claim in a Holistika canonical carries provenance
metadata so future readers (and validators) can audit the claim. Concretely:

- **`source_taxonomy`** annotation per claim (FK into
  [`source_taxonomy.md`](../Compliance/canonicals/source_taxonomy.md)):
  HUMINT / OSINT / internal-doctrine / vendor-doc / academic-paper /
  industry-publication / regulatory-text / etc.
- **`confidence_level`** annotation per claim (FK into
  [`confidence_levels.md`](../Compliance/canonicals/confidence_levels.md)):
  A1-F6 reliability + confidence scale.
- **`access_level`** annotation per canonical (FK into
  [`access_levels.md`](../Compliance/canonicals/access_levels.md)):
  the source-reading clearance required to verify the claim.
- **Audit URL or repo-path citation** per external source: every external
  source surfaces as a citeable URL (or repo-path if Holistika-internal).

This pillar inherits DAMA-DMBOK 3.0 Metadata Management semantics + Holistika's
existing source / confidence / access compliance canonicals. No new schema —
the existing compliance scaffolding is the surface.

### 3.5 Propagation — does the new claim trigger sister-canonical revision?

When a new canonical / rule / skill / decision lands, the Research Head
asks: does this trigger revision elsewhere? Concretely:

- Does a sibling canonical now carry a claim that contradicts the new one?
  (If so, surface as inline-ratify gate per
  [`akos-inline-ratification.mdc`](../../../../../../.cursor/rules/akos-inline-ratification.mdc).)
- Does a cross-area canonical now need to cite the new one as `linked_canonicals`
  in its frontmatter? (If so, mint the cross-link in the same commit batch.)
- Does the cross-area breakthrough propagation SOP need to fire? (Per
  [`SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.md`](SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.md)
  — applies when the new claim is itself a People pattern that other areas
  inherit.)
- Does the substrate-audit cadence need an off-cycle update? (Per
  [`SOP-RESEARCH_SUBSTRATE_AUDIT_CADENCE_001.md`](../../Research/Methodology/canonicals/SOP-RESEARCH_SUBSTRATE_AUDIT_CADENCE_001.md)
  — applies when the new claim materially changes substrate posture.)

The propagation pillar is what distinguishes research-first authoring from
research-as-citation-decoration: research-first claims **change the
sibling-canonical surface**; decoration claims do not. If the new claim does
not propagate, the Research Head asks whether the claim is load-bearing or
ornamental — load-bearing claims propagate by construction; ornamental
claims are anti-pattern (§7 below).

## 4. Internal-research checklist (the inventory pass operationalised)

When opening a research-first authoring session, the Research Head walks this
checklist:

1. **Closest sibling canonical**: identify the existing canonical(s) in the
   same area + adjacent areas whose scope is closest to the new authoring.
   Read it / them fully.
2. **Linked canonicals**: read every canonical named in the sibling's
   `linked_canonicals` frontmatter.
3. **Decision-register lineage**: `grep` `DECISION_REGISTER.csv` for the topic
   + adjacent decision IDs; read the relevant rows.
4. **Process_list rows**: `grep` `process_list.csv` for the relevant area + topic.
5. **Baseline_organisation rows**: `grep` `baseline_organisation.csv` for the
   relevant role(s).
6. **Cursor rules**: `Glob .cursor/rules/akos-*.mdc` and read those whose names
   surface in the topic space.
7. **Skills**: `Glob .cursor/skills/*/SKILL.md` and read those relevant.
8. **WIP synthesis**: `Glob docs/wip/intelligence/**/*.md` for any in-flight
   work on the topic.
9. **Planning history**: `Glob docs/wip/planning/**/master-roadmap.md` for any
   initiative-level prior treatment.
10. **CHANGELOG**: `grep` CHANGELOG.md for the topic — what's already shipped.

This checklist is the operationalisation of pillar §3.1 Inventory. The output
is captured in the Inventory paragraph of the planning notes or the canonical's
Evidence-base section (§6).

## 5. External-research checklist (the sourcing pass operationalised)

When the inventory pass surfaces a novel framing, the Research Head walks the
external checklist:

1. **WebSearch with year-scoping**: 3-10 queries; always include the year
   (current = 2026) to filter for current consensus. Avoid pre-2024 searches
   when the topic is fast-moving (AI / agentic / ResearchOps tooling).
2. **WebFetch authoritative sources**: 1-5 fetches of the top results from
   WebSearch; prefer first-party (vendor docs, standard bodies, named
   practitioners) over second-party.
3. **Named precedent corpus**: read the relevant chapter / section of any
   standard reference (DAMA-DMBOK 3.0; ResearchOps Community publications;
   Kate Towsey *Research That Scales*; McKinsey / Bain / Deloitte / KPMG /
   Forrester / Gartner / IDC industry analyst notes; academic papers via
   arXiv / Google Scholar for technical claims).
4. **Citation discipline**: every external source surfaced is cited inline
   in the canonical's Evidence-base section with URL + retrieval date + a
   one-clause summary of the relevance.
5. **Divergence narrative**: when Holistika's drafted position diverges from
   the industry consensus, the canonical names the divergence + the rationale
   + the conditions under which it might be revisited. Divergence-without-
   rationale is the most-common research-as-ornament failure mode (§7).

## 6. Backfill protocol — Evidence-base section on existing canonicals

When revising an existing canonical that was authored before this discipline
was codified, the Research Head opens an Evidence-base section (frontmatter
slot + body section):

**Frontmatter slot** (added on revision):

```yaml
evidence_base:
  internal_sources:
    - path: <repo-relative path>
      relevance: <one-clause summary>
  external_sources:
    - url: <https://...>
      retrieved: YYYY-MM-DD
      relevance: <one-clause summary>
  inventory_pass_completed: YYYY-MM-DD
  sourcing_pass_completed: YYYY-MM-DD
  research_head: <name or role e.g. "Founder (acting as Holistik Researcher)">
```

**Body section** (added at end of canonical, before final `## Cross-references`):

```markdown
## Evidence base

This canonical's load-bearing claims are grounded in the following sources
(per the Research Head Discipline §6 Backfill protocol).

### Internal sources
- [`path/to/canonical.md`](path/to/canonical.md) — <one-clause>
- ...

### External sources
- [Source title](URL) (retrieved YYYY-MM-DD) — <one-clause>
- ...

### Provenance
- Inventory pass: YYYY-MM-DD by <role>
- Sourcing pass: YYYY-MM-DD by <role>
- Synthesis: this canonical body
- Last review: see frontmatter
```

The Evidence-base structure is **append-only by default** — revisions add
sources rather than rewriting. Removals are governance events that surface
in the decision register.

Backfill priority order (per §4 per-area gap analysis):

1. `Operations/PMO/canonicals/KB_HUMAN_READABILITY_CHARTER.md` (currently 0 research mentions).
2. `Envoy Tech Lab/canonicals/AGENTIC_FRAMEWORK_LANDSCAPE.md` (link to SUBSTRATE_REGISTRY audit_source_url).
3. `Marketing/Brand/canonicals/BRAND_BASELINE_REALITY_MATRIX.md` (HUMINT tradecraft grounding made explicit).
4. `People/canonicals/HOLISTIKA_AGENTIC_DOCTRINE.md` (Research-as-pillar mention upgraded from footnote).
5. `Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md` (DAMA-DMBOK 3.0 alignment posture).

Backfill is incremental, not big-bang. One canonical per wave is sustainable.

## 7. Anti-patterns

The Research Head Discipline is unforgiving on four anti-patterns:

### 7.1 Research-as-ornament

Citing a source that does not actually load-bear on the canonical's claims —
"according to McKinsey, X is important" without naming what McKinsey actually
said about X or how Holistika's claim relates. Anti-pattern because it
trains future readers to ignore citations as decoration.

Counter-test: remove the citation. Does the canonical's claim weaken? If no,
the citation was ornament. Remove it.

### 7.2 Research-after-the-fact-to-justify

Authoring a position from operator intuition + then sweeping the industry to
find supporting citations + adding them as if they motivated the position.
Anti-pattern because it inverts the discipline (justification → research)
which produces selection bias.

Counter-test: would the operator's position have changed had the sourcing
pass surfaced contradicting evidence? If no (i.e., the position was always
going to be ratified regardless), the sourcing was theater. Either the
position is genuinely operator-tacit-knowledge-derived (in which case name
that explicitly + skip sourcing claim) or surface the contradicting evidence
and address it.

### 7.3 Research-as-procrastination

Extending the inventory + sourcing passes indefinitely to defer the synthesis
write-up. Anti-pattern because perfect is the enemy of done; Holistika
canonicals are revisable (see Backfill protocol §6) — version 1 with thin
sourcing is more valuable than version 0 with planned-deep sourcing.

Counter-test: has the inventory pass converged on a stable picture (no new
sweep adds material claims)? If yes, write the synthesis. Has the sourcing
pass surfaced the dominant industry-consensus position + the major dissenting
positions? If yes, write the synthesis. Do not chase exhaustiveness.

### 7.4 Copy-paste-citations

Citing the same source across many canonicals without re-reading it on each
cite. Anti-pattern because cited claims drift from what the source actually
says as the citing canonicals proliferate.

Counter-test: when a source is cited for the third time, re-read the relevant
section of the source. Does the cite still hold? If yes, continue. If not,
correct all three cites in the same commit batch.

## 8. Cross-references

- [`HOLISTIKA_ORGANISING_DOCTRINE.md`](HOLISTIKA_ORGANISING_DOCTRINE.md) §2
  (People is the discipline of disciplines) — the parent doctrine this
  canonical inherits from.
- [`HOLISTIKA_AGENTIC_DOCTRINE.md`](HOLISTIKA_AGENTIC_DOCTRINE.md) — agentic
  is a discipline of disciplines, recursive; this canonical is the recursive
  application to research-first authoring.
- [`PEOPLE_DESIGN_PATTERN_LIBRARY.md`](PEOPLE_DESIGN_PATTERN_LIBRARY.md) —
  the human-readable pattern hub; a `research_first_canonical_authoring`
  pattern row should be added in a future People design pattern tranche
  (forward-charter C-NN-B).
- [`../../Research/canonicals/RESEARCH_AREA_CHARTER.md`](../../Research/canonicals/RESEARCH_AREA_CHARTER.md) —
  the Research area's 4-discipline charter; this canonical names the
  meta-discipline that operates above the four (the Research Head's
  doctrine-author discipline).
- [`../../Research/Methodology/canonicals/SUBSTRATE_LANDSCAPE_DOCTRINE.md`](../../Research/Methodology/canonicals/SUBSTRATE_LANDSCAPE_DOCTRINE.md) —
  the discipline-of-disciplines-applied-to-Research precedent
  (D-IH-84-G); this canonical extends the pattern from substrate audit
  to general canonical authoring.
- [`.cursor/rules/akos-applied-research-discipline.mdc`](../../../../../../.cursor/rules/akos-applied-research-discipline.mdc) —
  the always-applied cursor rule that mechanically enforces this discipline.
- [`.cursor/skills/inline-ratify-craft/SKILL.md`](../../../../../../.cursor/skills/inline-ratify-craft/SKILL.md)
  Principle 1.5 — the skill extension that distinguishes evidence-sweep
  from research-sweep.
- [`.cursor/rules/akos-people-discipline-of-disciplines.mdc`](../../../../../../.cursor/rules/akos-people-discipline-of-disciplines.mdc) —
  the always-applied People rule that justifies this canonical's home in
  People (People mints patterns; Research authors processes from those
  patterns).
- ResearchOps Community 8 Pillars (https://researchops.community/about/) —
  industry-precedent for the discipline shape.
- Kate Towsey, *Research That Scales: The Research Operations Handbook*
  (Rosenfeld Media, 2024) — book canonicalisation of ResearchOps.
- D-IH-86-RH-A through D-IH-86-RH-H in `DECISION_REGISTER.csv`
  (ratify gate at parent coordinator handoff).
```

### 7.B NEW cursor rule: `akos-applied-research-discipline.mdc`

**Target path**: `.cursor/rules/akos-applied-research-discipline.mdc`

**Frontmatter** (proposed):

```yaml
---
description: Always-applied rule that mechanically calls out research-first authoring discipline on every canonical / cursor rule / skill / decision mint. Pairs with RESEARCH_HEAD_DISCIPLINE.md canonical + inline-ratify-craft skill Principle 1.5.
globs:
  - docs/references/hlk/v3.0/**/canonicals/*.md
  - docs/references/hlk/v3.0/**/canonicals/dimensions/*.csv
  - .cursor/rules/akos-*.mdc
  - .cursor/skills/*/SKILL.md
  - docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv
alwaysApply: true
---
```

**Body** (proposed; target ~120 lines):

```markdown
# AKOS Applied Research Discipline

Use this rule whenever authoring or revising **canonicals**, **cursor rules**,
**skills**, or **decision-register rows** in this workspace. Codifies operator
ratification at I86 Wave H of D-IH-86-T cluster burndown + the Combo C+D
disposition for the Research Head discipline (operator's framing 2026-05-19:
*"applied research is a hot topic today and a competitive advantage if
properly industrialized"*).

This rule is the mechanically-enforced layer of the
[`RESEARCH_HEAD_DISCIPLINE.md`](../../docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/RESEARCH_HEAD_DISCIPLINE.md)
canonical. The canonical describes the discipline; this rule names when it
fires. Read both together.

## RULE 1 — Canonical-CSV mints require internal + external research backing (binding)

Whenever a net-new canonical CSV is minted (per
[`akos-holistika-operations.mdc`](akos-holistika-operations.mdc) §"New
git-canonical compliance registers"), the authoring discipline must include:

1. **Internal research pass**: documented inventory of which existing
   canonicals, decision-register rows, process_list rows, and
   baseline_organisation rows bear on the new register. Output captured in
   the ratifying decision row's rationale or in a planning-notes file
   referenced from the decision row.
2. **External research pass**: at least one external industry source cited
   in the ratifying decision row when the register introduces a novel
   framing not yet seen in Holistika or industry. (If the register is a
   pure clone of an existing pattern — e.g., a new sibling adapter registry
   following the established Normalised Adapter Pattern — external citation
   is optional; the cite-by-existing-pattern is sufficient.)

The two passes' outputs are documented in:

- The ratifying decision row's `rationale` cell (or a short pointer to a
  planning-notes file).
- The canonical's `linked_canonicals` frontmatter (for internal links).
- The canonical's body (or its companion Evidence-base section per the
  RESEARCH_HEAD_DISCIPLINE §6 Backfill protocol).

## RULE 2 — Doctrine canonicals and rule mints cite at least one external source when novel framing (binding)

Whenever a net-new doctrine canonical (any `intellectual_kind: doctrine`,
`area_charter`, `discipline_charter`, `people-canonical`,
`research-area-canonical`, `tech-canonical`, or `brand-canonical` file under
`docs/references/hlk/v3.0/**/canonicals/`) is minted, OR a net-new cursor
rule under `.cursor/rules/akos-*.mdc`, OR a net-new skill under
`.cursor/skills/*/SKILL.md`:

If the new canonical / rule / skill introduces a **novel framing** (a
position Holistika has not previously committed to), the authoring must
cite at least one external industry source. Cited inline in the body OR in
the Evidence-base section.

If the canonical / rule / skill is a **refinement** of an already-ratified
Holistika position (e.g., a v2 extension of a v1 doctrine, a tightening of
an existing rule), external citation is optional; the prior Holistika
ratification IS the precedent.

The novelty test: would a future reader, reading this canonical / rule /
skill cold, encounter a position they could not derive from prior Holistika
doctrine + first-principles thinking? If yes, the framing is novel and an
external citation is mandatory. If no, refinement-only and external citation
is optional.

## RULE 3 — Wave-closure reports include a "Research enrichment" subsection (binding)

Whenever a wave (per the I86 cluster burndown lineage; also any future
analogous coordination structure) closes via a closure report at
`docs/wip/planning/<NN>/reports/<YYYY-MM-DD>-wave-<X>-*-closure.md`, the
closure report includes a `## Research enrichment` subsection naming:

- **Which canonicals were enriched** with new research material during the
  wave (with Evidence-base section additions or `linked_canonicals`
  frontmatter additions).
- **Which canonicals were identified as needing enrichment** but deferred
  to a future wave (forward-charter forward-pointer).
- **Which external sources were newly surfaced** during the wave that should
  inform future authoring (a short list of authoritative URLs).

This subsection makes the operator's lived research practice **trackable
across waves** — closing the continuity gap the operator named verbatim in
the I86 Wave H Lane D dispatch.

The subsection can be brief (5-15 lines per wave). It is not a deep
research narrative; it is a research-state-of-the-wave snapshot.

## When this rule does NOT apply

This rule does NOT fire for:

- **Mechanical authoring** — typo fixes, link-rot fixes, formatting
  normalisations, markdown lint fixes, YAML-frontmatter normalisations.
- **Bugfix commits** — code-level bug fixes that do not touch canonical
  doctrine.
- **Refactors of already-researched canonicals** — when the underlying
  research base does not change; e.g., splitting a section into two for
  readability, renaming a heading.
- **Test additions** — adding tests that exercise existing code or
  canonical contracts without introducing new doctrine.
- **Per-engagement WIP synthesis** — covered by Research/Intelligence
  discipline charters + Tier 1 WIP rules at `docs/wip/intelligence/`.
- **Operator-discretion exemption** — when the operator explicitly invokes
  the exemption in a commit message ("rule-exempt-research-discipline:
  <one-clause reason>") for time-pressed or scope-limited work. The
  exemption surfaces in the next wave's "Research enrichment" subsection
  as a deferred-backfill flag.

## Self-discipline rules for agents

When generating prose under the rule's globs:

1. **Default to the inventory pass.** Before authoring, sweep the closest
   sibling canonical + linked canonicals + decision-register lineage. The
   sweep is operationalised in the
   [RESEARCH_HEAD_DISCIPLINE §4 internal-research checklist](../../docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/RESEARCH_HEAD_DISCIPLINE.md).
2. **Distinguish evidence-sweep from research-sweep.** Evidence-sweep is
   `Grep / Read / Glob` over repo state (covered by `akos-inline-ratification.mdc`
   Principle 1 + skill-craft Principle 1). Research-sweep is `WebSearch /
   WebFetch` over industry precedent (this rule's RULE 2). The two are not
   substitutes; novel framings require both.
3. **Cite inline.** External citations belong in the canonical's body or
   its Evidence-base section, not in a separate dossier. The citation is
   half of the load-bearing claim.
4. **Honour the anti-patterns.** Research-as-ornament, research-after-the-
   fact-to-justify, research-as-procrastination, copy-paste-citations are
   anti-pattern per RESEARCH_HEAD_DISCIPLINE §7. Counter-tests applied
   before commit.

## Cross-references

- [`RESEARCH_HEAD_DISCIPLINE.md`](../../docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/RESEARCH_HEAD_DISCIPLINE.md)
  — the canonical this rule operationalises.
- [`akos-people-discipline-of-disciplines.mdc`](akos-people-discipline-of-disciplines.mdc)
  — parent rule; the canonical's home in People follows that rule's
  Rule 1.
- [`akos-inline-ratification.mdc`](akos-inline-ratification.mdc) — sister
  rule; Principle 1 evidence-sweep is the closest analog to RULE 1 here.
- [`akos-planning-traceability.mdc`](akos-planning-traceability.mdc) — the
  plan-quality bar that wave-closure reports inherit (RULE 3 extends it
  with the Research enrichment subsection).
- [`akos-holistika-operations.mdc`](akos-holistika-operations.mdc)
  §"New git-canonical compliance registers" — the canonical-CSV mint
  pattern RULE 1 attaches to.
- [`.cursor/skills/inline-ratify-craft/SKILL.md`](../skills/inline-ratify-craft/SKILL.md)
  Principle 1.5 — the skill craft that operationalises research-sweep at
  inline-ratify gates.
- D-IH-86-T (cluster burndown plan) + D-IH-86-RH-A through D-IH-86-RH-H
  (Combo C+D Lane D ratification gate; parent coordinator surfaces).

@docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/RESEARCH_HEAD_DISCIPLINE.md
```

### 7.C EXTEND `inline-ratify-craft` skill with Principle 1.5

**Target file**: `.cursor/skills/inline-ratify-craft/SKILL.md`

**Insertion point**: after the existing Principle 1 section ("Run the
evidence sweep first") and before Principle 2 ("Distil to ranked options
with rationale embedded inline"). Estimated ~60 lines.

**Proposed body**:

```markdown
### Principle 1.5 — Research-sweep when the question is novel

Principle 1 names the evidence sweep — `Grep`, `Read`, `Glob`,
`SemanticSearch` over **repo state**. This is the right move for most
inline-ratify gates because most decisions can be ratified from what the
repo already commits to.

But some inline-ratify gates pose questions the repo has no prior
commitment on. The operator's framing is genuinely novel; the closest
sibling canonical does not yet take a position; no decision-register row
ratifies the relevant axis. For these gates, the evidence sweep collapses
to "the repo is silent" and the agent needs a second sweep: the
**research sweep** over industry precedent.

The research sweep is `WebSearch` + `WebFetch` + (optionally) reads of
named precedent corpus (DAMA-DMBOK 3.0; ResearchOps Community publications;
Kate Towsey *Research That Scales*; industry analyst notes; academic
papers). The sweep is **conditional on novelty** — if the evidence sweep
already converged on an obvious authoring direction, research sweep is
light (1-2 confirmatory queries). If the evidence sweep surfaced genuine
silence, research sweep is heavier (5-10 queries; multiple precedent
sources).

How to know when novelty fires:

- The inline-ratify gate's options that the agent can draft from repo state
  alone all carry low-confidence rationales (every option boils down to
  "the operator should pick because we don't know"). That is the signal
  that the repo cannot make the call alone.
- The closest sibling canonical's `last_review` predates the topic the gate
  poses (e.g., posing a 2026 LLM substrate question against a canonical
  whose last review was 2025).
- The topic appears in `RESEARCH_BACKLOG_TRELLO_REGISTRY.md` as a
  `candidate` (i.e., the operator has flagged it for research but has not
  yet written the synthesis).
- The topic surfaces in `docs/wip/intelligence/` as in-flight WIP without
  yet a canonical home.

When novelty fires, the agent runs the research sweep BEFORE posing the
inline-ratify gate. The sweep's output enriches the option set with
industry-precedent framings the agent could not have generated from repo
state alone. This is responsible for the "third path" emergence Principle
6 names — many of those third paths are not novel-to-the-industry, they
are novel-to-Holistika because the agent surfaced them via research sweep.

Cite the research sweep inline in the inline-ratify call's option labels
(per Principle 4: cite evidence inline by file path or URL). Example:

```
Option C — adopt the ResearchOps 8-Pillar shape (novel framing —
ResearchOps Community canonical at https://researchops.community/about/
adopted in 2018 + reaffirmed in Kate Towsey 2024)
```

The research sweep's full output (URLs + retrieval dates + relevance
summaries) goes in the Evidence-base section of whichever canonical the
inline-ratify gate ratifies into (per `RESEARCH_HEAD_DISCIPLINE.md` §6
Backfill protocol). The inline-ratify call cites only the load-bearing
snippet, not the full sweep.

Cross-references for this principle:

- [`RESEARCH_HEAD_DISCIPLINE.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/RESEARCH_HEAD_DISCIPLINE.md)
  §3.2 (Sourcing pillar) + §5 (External-research checklist).
- [`akos-applied-research-discipline.mdc`](../../../.cursor/rules/akos-applied-research-discipline.mdc)
  RULE 2 (external citation when novel framing).
- Principle 1 (evidence sweep) above — the foundation; Principle 1.5
  extends rather than replaces.
- Principle 6 (welcome novel framings) below — the receiver; many novel
  framings emerge from research sweeps.
```

## 8. Forward-charter candidates (flag-only; not authored today)

| ID | Candidate | Trigger condition | Owner | Notes |
|:---|:---|:---|:---|:---|
| **C-NN-A** | Research Area v3.1 baseline manifesto (does Research need its own area canonical like People's HOLISTIKA_ORGANISING_DOCTRINE.md?) | Operator-ratified intent to mint a Research-area-specific manifesto; OR D-IH-86-RH-A ratifies People-canonical home (which arguably removes the need) | Founder + KM Officer | RESEARCH_AREA_CHARTER.md already plays partial manifesto role. The candidate would author a higher-altitude Research Area Manifesto that names the area's CORE values, lived practice, and inheritance posture — analog to HOLISTIKA_ORGANISING_DOCTRINE. **Recommend defer** unless operator surfaces it as a felt gap; current 4-discipline-charter structure may suffice. |
| **C-NN-B** | process_list.csv tranche for Research-area meta-processes (research_canonical_authoring, applied_research_audit, wave_research_enrichment, canonical_evidence_base_backfill) | Operator-ratified intent to formalise the discipline as governed processes; SOP-META order requires CSV rows before SOPs | Founder + Compliance | 4 candidate process rows. Each pairs with a future SOP. Tranche size ~4-6 rows; operator-gated per canonical-CSV discipline. |
| **C-NN-C** | ResearchOps tooling decision (Dovetail / Maze / Notion-as-research-repo / homegrown md+CSV+Supabase?) | Operator surfaces need for tooling beyond current md+Trello; or substrate audit identifies it; or future hire (Research Director / KM Officer) needs better collab surface | Tech Lead + KM Officer + Founder | Current stack (md + Trello + Tier 1 WIP) is operator-fit but does not scale to 2+ researchers. Dovetail is industry standard but bypasses Holistika's git-canonical posture. **Recommend defer** until a second researcher joins. |
| **C-NN-D** | PEOPLE_DESIGN_PATTERN_REGISTRY.csv row `research_first_canonical_authoring` | Operator-ratified intent to register the discipline as a People design pattern (i.e., a pattern other areas inherit and `process_list.csv` rows can FK against) | People Operations Manager + Founder | After RESEARCH_HEAD_DISCIPLINE.md lands, the pattern row is a natural sibling. Pattern-class enum may need an extension. **Recommend ride next People design pattern tranche**. |
| **C-NN-E** | `validate_research_backing.py` validator | Operator-ratified intent + a stable enough schema for canonical `evidence_base` frontmatter to scan | System Owner + KM Officer | Would scan canonicals' frontmatter for the `evidence_base` slot; FK against `source_taxonomy.md` + `confidence_levels.md`. INFO-only at v1; FAIL-tier after backfill stabilises (mirrors the BBR drift gate INFO→FAIL ramp). **Recommend defer** until 5+ canonicals have evidence_base sections to validate. |
| **C-NN-F** | Cross-area canonical Evidence-base backfill wave (per §4 gap analysis priority order: KB readability → agentic framework landscape → BBR → agentic doctrine → PRECEDENCE) | Operator-ratified intent + bandwidth for cross-area sweep | Founder + each area lead | A 5-7 canonical backfill wave; surface as Wave I or later candidate. |

## 9. Practical constraints honored

- [x] Single deliverable: `lane-d-research-area-sweep-2026-05-19.md` at the named path.
- [x] No files outside the report minted. The Combo C+D artifacts are **drafted** in §7 above, NOT written to their target paths.
- [x] Honors `akos-people-discipline-of-disciplines.mdc`: canonical home = People (Rule 1 — People mints patterns; other areas author processes).
- [x] Honors `akos-planning-traceability.mdc`: report carries `intellectual_kind`, `linked_decisions`, `status: draft`, structured sections.
- [x] Honors `akos-inline-ratification.mdc`: decisions surfaced in §5 as ratify-bait; parent coordinator will pose to operator.
- [x] Honors `akos-conflict-surfacing-and-blocker-trackers.mdc`: where the Combo C+D design has structural conflict potential (decisions D-IH-86-RH-A/B/C/D/E/F/G/H), each is named explicitly with recommended default + alternative tradeoff.
- [x] No commit. Parent commits after Lane A + Lane C close.
- [x] Token budget respected (~700 lines target; report fits within 50-80K tokens read+write).

## 10. Suggested next actions for parent coordinator

1. **Drain operator scratchpad** if any new entries arrived during Lane D execution.
2. **Surface inline-ratify gate** to operator with the 8 decisions in §5 (D-IH-86-RH-A through D-IH-86-RH-H). Batch as a single AskQuestion call per inline-ratify-craft Principle 5.
3. **Apply operator ratifications** by minting the three target files per §7.A / §7.B / §7.C drafts — adjust per-decision (e.g., if D-IH-86-RH-B picks 7 or 8 pillars instead of 5, expand §3 of the canonical accordingly).
4. **Append decision rows** D-IH-86-RH-A..H to `DECISION_REGISTER.csv`.
5. **Append CHANGELOG entry** + update `docs/wip/planning/86-initiative-cluster-execution-coordinator/files-modified.csv`.
6. **Cross-link** the new canonical from `PRECEDENCE.md` (canonical row), `HOLISTIKA_ORGANISING_DOCTRINE.md` `companion_to:` frontmatter, and `RESEARCH_AREA_CHARTER.md` cross-references.
7. **Verify** via `py scripts/validate_hlk.py` + `py scripts/release-gate.py` + `py scripts/validate_hlk_vault_links.py` (the cross-link validation will exercise the new canonical's `linked_canonicals` frontmatter resolution).
8. **Flag forward-charters** C-NN-A through C-NN-F in the wave closure report's `## Research enrichment` subsection (which by construction is the FIRST application of RULE 3 of the new cursor rule — closing the loop in the same Wave H closure).

## 11. Closing note

The operator's framing — "I don't think it's that new" — is **structurally correct**, and that is the load-bearing reason this Combo C+D scope is the right one. The Research area exists; the discipline exists in the operator's lived practice; the only authentically-new piece is **transmissibility** (to AICs, to collaborators, to future-self-reading-cold). Three lean artifacts close that gap. The discipline becomes legible. Continuity is achieved.

The forward-charter candidates in §8 are exactly the over-engineering temptations to avoid today. Lane D recommends honoring the operator's "not overengineered" directive: ship the three lean artifacts, ride the cursor rule into the next wave's closure report (RULE 3 self-application), and let evidence-base backfill, validator design, and process_list mint accumulate one canonical at a time over future waves.

---

*End of Lane D Wave H sweep + design report.*
