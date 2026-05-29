---
language: en
status: active
canonical: true
ssot: true
role_owner: Lead Researcher (KM Officer steward; Founder interim per D-IH-84-H)
classification: way_of_working
intellectual_kind: area_doctrine
authored: 2026-05-29
last_review: 2026-05-29
last_review_decision_id: D-IH-75-G
ratifying_decisions:
  - D-IH-75-G
  - D-IH-75-H
companion_to:
  - ./RESEARCH_AREA_CHARTER.md
  - ../README.md
evidence_base:
  - "Intelligence Cycle (US joint/air-force doctrine, JP 2-0 2022 / AFDP 2-0 2023): planning-direction -> collection -> processing-exploitation -> analysis-production -> dissemination-integration -> feedback. Counter-intelligence is the paired field that impedes others' intelligence efforts."
  - "Knowledge-management lifecycle (Meyer & Zack 1999 five-stage: acquisition -> refinement -> storage/retrieval -> distribution -> presentation/use; Bukowitz & Williams; APQC seven-step capture->organize->store->share->apply->review/retire)."
  - "DIKW hierarchy (Ackoff 1989): data -> information -> knowledge -> wisdom; the why behind PROCESS turning raw collection into decision-useful judgement."
  - "SCIP Code of Ethics (Strategic & Competitive Intelligence Professionals): legal + ethical collection, public-source preference, red-face test, no misrepresentation - the ethical floor for ACQUIRE."
  - "Corporate counter-intelligence practice (SCIP; DCSA CI Best Practices; corporate-CI program literature 2025): crown-jewel protection, insider-threat awareness, source protection - the grounding for the PROTECT stage."
---

# RESEARCH_LIFECYCLE_DOCTRINE — the CORPINT lifecycle as the Research area's spine

> **What this is.** The single doctrine that says how the Research area is *organised*. It
> elevates the **CORPINT information lifecycle** (the flow information takes — acquire, process,
> store, share, recall, protect) to the **spine** of the area, and positions the **four
> disciplines** (Methodology / Intelligence / Diagnosis / Validation) as the **crafts** that move
> information through that flow. Where the flow crosses an area boundary, the **cross-area join**
> is made first-class — because Holistika is the sum of its areas.
>
> **Why it exists.** Founder-ratified **logic change** (`D-IH-75-G`, 2026-05-29). The prior
> structure carried two organising ideas that never reconciled — the disciplines (crafts) and the
> lifecycle (flow) — so three lifecycle stages (**share, recall, protect**) had no owner and fell
> through as "thin stages." This doctrine reconciles the two axes into one architecture and closes
> those gaps. Read this *with* the area anchor [`README.md`](../README.md) and the area charter
> [`RESEARCH_AREA_CHARTER.md`](RESEARCH_AREA_CHARTER.md): the README is the *map*, the charter is
> the *constitution*, this doctrine is the *operating logic* that binds the two.

## 1. The logic change in one paragraph

Research is **Holistika's corporate-intelligence (CORPINT) operating system**. An operating system
has a *flow* (what happens to information from the moment it enters to the moment it is retired or
protected) and *crafts* (the skilled moves that act on information at each step). The previous
v3.0 design named the crafts well (four disciplines) but treated the flow as prose in a README.
That left dissemination, retrieval, and protection homeless. The change ratified here: **the
six-stage lifecycle is the spine; the four disciplines are the crafts that operate across it; the
points where the lifecycle leaves Research and enters another area are named, owned joins.** This
is not a new vocabulary invented for Holistika — it is the synthesis of three well-established
public frameworks (the **intelligence cycle**, the **knowledge-management lifecycle**, and
**competitive-intelligence + counter-intelligence** practice), adapted to how Holistika actually
works. (See §8 for the grounding; the intelligence-analysis literature explicitly notes the
intelligence cycle "mirrors the research cycle.")

## 2. The CORPINT lifecycle — the six stages (the spine)

The coherent ordering — corrected from the README's earlier draft ordering as part of this
regrouping — is a flow with one loop and one cross-cutting guard:

```
ACQUIRE  ->  PROCESS  ->  STORE  <->  RECALL  ->  SHARE
                                  \________________________/
                          PROTECT  (cross-cutting guard over every stage)
```

| # | Stage | Plain definition | External lineage | Holistika instantiation |
|:--|:---|:---|:---|:---|
| 1 | **ACQUIRE** | Collect raw signal from human + open sources against a stated need. | Intelligence cycle *collection*; KM *capture*. | Research/Intelligence (HUMINT + OSINT); Methodology sets the requirement; IntelligenceOps register names the targets; Research Radar says what is stale and due. |
| 2 | **PROCESS** | Turn raw signal into decision-useful judgement (refine, classify, analyse, corroborate). | Intelligence cycle *processing + analysis*; KM *refine*; DIKW *data->information->knowledge*. | Research Action govern loop; Validation (truth-gating); Diagnosis (what's wrong); Methodology pillars (HxPESTAL, PESTEL, Foresight). |
| 3 | **STORE** | Commit validated knowledge to durable, addressable memory. | KM *storage*; Meyer-Zack *storage/retrieval*. | KM Topic-Fact-Source + TOPIC_REGISTRY; the IntelligenceOps register; Neo4j projection; KiRBe (forward). **Cross-area join: Tech owns the store; Research authors what is stored.** |
| 4 | **RECALL** | Retrieve the right stored knowledge at the moment of need. | KM *retrieval/apply*; Meyer-Zack *storage/retrieval* (the retrieval half). | Derived-recall principle; Neo4j/MCP query surfaces; the register as a queryable index. **Cross-area join: Tech owns the retrieval infra; Methodology owns the recall discipline.** |
| 5 | **SHARE / OUTAKE** | Deliver the finished product to whoever has to decide or act. | Intelligence cycle *dissemination*; KM *distribute*. | Research authors the brief / report in the internal CORPINT register. **Cross-area join: Marketing/Brand translates to the external register; External-Render delivers the surface.** |
| 6 | **PROTECT** | Guard sources, methods, and crown-jewel knowledge; keep collection legal + ethical. | Counter-intelligence (the field paired with the intelligence cycle); SCIP ethics. | GOI/POI stance + source-credibility discipline (Research side). **Cross-area join: People/Ethics owns the red lines; People/Compliance owns access + confidence + redaction.** |

PROTECT is drawn *across* the diagram rather than *in line* on purpose: counter-intelligence is not
a step you do once, it is a guard you hold over every other step (legal+ethical at ACQUIRE; source
protection at STORE; redaction at SHARE; access control at RECALL).

## 3. The four disciplines as crafts (what acts on the flow)

The disciplines did not change — they were correctly named at I70 P4.7. What changes is that each is
now explicitly *positioned on the lifecycle*: every discipline owns a primary stage and supports
others. (Full per-discipline definitions live in the four discipline charters; this is the
lifecycle view.)

| Discipline | The question it answers | Primary lifecycle ownership | Supports |
|:---|:---|:---|:---|
| **Methodology** | *how* we research | The requirement-setting that opens ACQUIRE + the craft of every stage (pillars, techniques, deep-research) | all stages |
| **Intelligence** | *what* we collect | **ACQUIRE** (HUMINT + OSINT collection) + the classification that begins PROCESS | PROCESS, STORE, PROTECT |
| **Diagnosis** | *what's wrong* | **PROCESS** (analysis/production — the verdict layer: engagement / system / methodology diagnostic) | SHARE |
| **Validation** | *what's true* | **PROCESS** (the truth-gate: source-reliability grading, corroboration, evidence-confidence) + the feedback loop | STORE, SHARE, PROTECT |

## 4. The discipline x lifecycle matrix (the load-bearing map)

Read a column to see what a discipline does across the flow; read a row to see which crafts touch a
stage. `++` = primary owner; `+` = active contributor; `>` = cross-area join (owner named in §5).

| Lifecycle stage | Methodology | Intelligence | Diagnosis | Validation | Cross-area join |
|:---|:--:|:--:|:--:|:--:|:---|
| **ACQUIRE** | + (requirement) | `++` (HUMINT/OSINT) | | | Operations (engagement trigger feeds the need) |
| **PROCESS** | + (pillars/techniques) | + (classify/matrix) | `++` (verdict) | `++` (truth-gate) | — |
| **STORE** | + (packaging) | + (fact-table entry) | | + (confidence stamp) | `>` Tech / KB (KM Topic-Fact-Source; Neo4j; KiRBe) |
| **RECALL** | `++` (derived-recall discipline) | + (register as index) | | | `>` Tech (Neo4j / MCP / search) |
| **SHARE** | + (brief/packaging) | + (intelligence product) | + (diagnostic report) | + (claim-confidence gate) | `>` Marketing/Brand (dual-register) + External-Render |
| **PROTECT** | | + (source protection / GOI-POI) | | + (reliability discipline) | `>` People/Ethics (red lines) + People/Compliance (access / confidence / redaction) |

The matrix is the artefact that prevents the prior failure mode: every stage now has at least one
`++` owner or a named `>` join — no stage is homeless.

## 5. Cross-area joins — Holistika is the sum of its areas

Research does not own the whole lifecycle, and pretending it does would violate the single-ownership
discipline the area charter §6 establishes (the *authoring-vs-consuming* rule: Research **authors**
investigative artefacts; other areas **consume** them, and own the surfaces Research's flow passes
into). The four joins below are the seams where the CORPINT lifecycle crosses into a sister area.

| Join | Research's side (we author) | Sister area's side (they own) | Governing canon |
|:---|:---|:---|:---|
| **STORE -> Tech / KB** | What is worth storing; the Topic-Fact-Source shape of each fact; reliability stamp. | The store itself (KM index, Neo4j projection, KiRBe ingestion, MCP surfaces). | `HLK_KM_TOPIC_FACT_SOURCE.md`; KiRBe (I83). |
| **SHARE -> Marketing/Brand + External-Render** | The finished brief/report in the **internal CORPINT register**. | Translation to the **external register** (dual-register contract) + the rendered surface (PDF/web/deck). | `BRAND_BASELINE_REALITY_MATRIX.md`; `akos-external-render-discipline.mdc`. |
| **RECALL -> Tech** | The recall discipline (what to ask for, the derived-recall principle); the register as a queryable index. | The retrieval infrastructure (search, graph, MCP). | KM + Neo4j projection. |
| **PROTECT -> People/Ethics + People/Compliance** | Source protection; GOI/POI stance; legal+ethical collection floor. | The ethical red lines; access levels; confidence taxonomy; redaction. | `ETHICAL_AGENTIC_BOUNDARIES.md`; `access_levels.md`; `confidence_levels.md`. |

**Single-ownership safeguard (per founder ratification + KB-integrity I81).** This doctrine
documents **Research's side** of each join. It does **not** unilaterally edit the sister areas'
canonicals. The reciprocal pointers (Marketing's render-side note, Tech's KB-side note,
People/Ethics' counter-intelligence-boundary note) are **governed follow-ups** that the owning area
ratifies — tracked so the work *helps* those areas rather than imposing on them. See §6.3 forward
work + the area charter §6.

## 6. Closing the three thin stages

### 6.1 SHARE / OUTAKE — from gap to named join

- **Was:** "thin — no Research-owned outake doctrine."
- **Now:** SHARE is a **two-party join**, not a missing discipline. Research's outake responsibility
  is to produce the intelligence product (brief / report / packaged output) in the internal
  register; Marketing/Brand translates and External-Render delivers. The capability already exists
  (Research Brief, Research Output Packaging, Output 1/2/3 — see §7). What was missing was the
  *naming* of the seam, now done in §5.
- **Forward work:** a thin `SOP-RESEARCH_OUTAKE_HANDOFF_001` (Research->Marketing handoff checklist)
  is the only net-new artefact; forward-chartered to I75 P5 (the per-engagement cadence phase).

### 6.2 RECALL — from gap to named join

- **Was:** "thin — no governed recall discipline."
- **Now:** RECALL is owned jointly by Methodology (the *discipline* of recall — the derived-recall
  principle: you retrieve by deriving the question, not by remembering the file) and Tech (the
  *infrastructure* — Neo4j, MCP, search). The IntelligenceOps register is the queryable index that
  makes recall mechanical.
- **Forward work:** the derived-recall principle is currently a one-line idea; promoting it to a
  short Methodology canonical is forward-chartered (low priority; the infra is the load-bearing part
  and Tech owns it).

### 6.3 PROTECT — from gap to first-class stage (the genuinely new claim)

- **Was:** "thin — no counter-intelligence doctrine."
- **Now:** PROTECT is established as a **first-class lifecycle stage** with a named **cross-area
  ownership triad** (`D-IH-75-H`):
  - **Research/Intelligence** owns *source protection* and the GOI/POI stance (who we are watching,
    who may be watching us, what we do not expose).
  - **People/Ethics** owns the *red lines* (the SCIP-style ethical floor: legal + ethical collection,
    no misrepresentation, the red-face test) — already partly carried by `ETHICAL_AGENTIC_BOUNDARIES.md`.
  - **People/Compliance** owns *access + confidence + redaction* (`access_levels.md`,
    `confidence_levels.md`, source taxonomy).
- **Forward work (governed follow-up, KB-integrity I81).** A full **Counter-Intelligence discipline**
  (a fifth Research craft, or a cross-cutting concern documented under Intelligence) is **forward-
  chartered**, not minted here — minting it would require ratification from People/Ethics +
  People/Compliance (the co-owners), which is exactly the reciprocal cross-area gate single-ownership
  requires. `D-IH-75-H` records the stage + triad; the discipline mint is a named successor.

## 7. Capability map — the techniques, by stage

These are the **existing** Research capability rows (the operator's work, seeded from the I81
KB-integrity matrix per `D-IH-82-P`) placed on the lifecycle. They live in
[`CAPABILITY_REGISTRY.csv`](../../Admin/O5-1/People/Compliance/canonicals/dimensions/CAPABILITY_REGISTRY.csv)
(filter `area = Research`); the per-sub-folder index READMEs cite them by ID. This map is the proof
that the structure holds real content, not empty husks.

| Stage | Discipline / sub-area | Capabilities (by registry name) |
|:---|:---|:---|
| ACQUIRE | Intelligence / HUMINT | Enriched Interview; Focus group; Stakeholder Interview Protocol; Field Observation |
| ACQUIRE | Intelligence / OSINT | Web Intelligence Gathering; Social Media Intelligence; Publication Monitoring |
| ACQUIRE | Methodology / Techniques | Literature Review; 6 Ws |
| PROCESS | Intelligence / Matrix | Classify Intel; Place in Intelligence Matrix; Source Credibility Assessment; Temporal Impact Analysis; Generational Filter |
| PROCESS | Methodology / Pillars | HxPESTAL; PESTEL Analysis; Process Engineering; Business Engineering; Factor Combination; Foresight |
| PROCESS | Methodology / Techniques | Create Analogy; Competitive Benchmarking; Multi-Source Synthesis |
| PROCESS | Diagnosis | Intelligence Assessment; Intelligence Assessment Cycle; Competitive Intelligence and Positioning |
| PROCESS | Validation | Source Credibility Assessment; Contradiction Resolution |
| STORE | Intelligence / Matrix | Fact Table Entry; Output 1 / Output 2 / Output 3 |
| RECALL | Methodology + cross-area Tech | derived-recall principle; IntelligenceOps register as index |
| SHARE | Methodology + Intelligence | Research Brief; Research Output Packaging; Output 1 / 2 / 3 |
| PROTECT | Intelligence + Validation | Source Credibility Assessment (protection side); GOI/POI stance |
| (spans PROCESS->STORE->RECALL) | Methodology / Deep-Research | Deep Research Methodology; FlowMaker Research Pipeline; Research-material pipeline (build process / gather channels / data governance / integrate-to-MADEIRA) |

## 8. Evidence base (the grounding for the novel framing)

Per [`akos-applied-research-discipline.mdc`](../../../../../../.cursor/rules/akos-applied-research-discipline.mdc)
RULE 2 (novel framing requires external grounding) + the Research Head backfill protocol
(`evidence_base` frontmatter). External sources are logged in the paired source ledger
[`docs/wip/intelligence/research-lifecycle-doctrine-2026-05-29/source-ledger.csv`](../../../../../wip/intelligence/research-lifecycle-doctrine-2026-05-29/source-ledger.csv).

- **Intelligence cycle** (high confidence / well-established): planning-direction -> collection ->
  processing -> analysis -> dissemination -> feedback, with counter-intelligence as the paired
  protective field (JP 2-0 2022; AFDP 2-0 2023; Wikipedia *Intelligence cycle management*; PSU
  GEOG 571 — which explicitly notes the intelligence cycle *mirrors the research cycle*). Grounds
  ACQUIRE -> PROCESS -> SHARE + PROTECT.
- **Knowledge-management lifecycle** (high confidence): Meyer & Zack (1999) five-stage acquisition ->
  refinement -> storage/retrieval -> distribution -> presentation/use; Bukowitz & Williams;
  APQC capture->organize->store->share->apply->review/retire. Grounds STORE + RECALL + SHARE.
- **DIKW hierarchy** (high confidence): Ackoff (1989) data -> information -> knowledge -> wisdom.
  Grounds *why* PROCESS exists (raw collection is not yet decision-useful).
- **SCIP Code of Ethics** (high confidence): legal + ethical collection, public-source preference,
  no misrepresentation, the red-face test. Grounds the ethical floor of ACQUIRE + PROTECT.
- **Corporate counter-intelligence** (medium-high confidence; an active, less-settled field):
  crown-jewel protection, source protection, insider-threat awareness (SCIP; DCSA CI Best Practices;
  corporate-CI program literature 2025). Grounds PROTECT.

**Internal precedent** (RULE 1): the README CORPINT lifecycle map; the four discipline charters
(I70 P4.7); the IntelligenceOps register + Research Radar (freshness axis); the source taxonomy
(OSINT/HUMINT/SIGINT/CORPINT/MOTINT); the capability registry (I81/I82); the dual-register +
external-render disciplines (the SHARE join); the GOI/POI stance (the PROTECT join).

## 9. Governance + cross-references

- **Decisions:** `D-IH-75-G` (the lifecycle-spine logic change; founder-ratified 2026-05-29) +
  `D-IH-75-H` (PROTECT stage + counter-intelligence cross-area ownership triad; forward-charters the
  Counter-Intelligence discipline mint). Both in
  [`DECISION_REGISTER.csv`](../../Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv).
- **Parent initiative:** [I75 Research area governance](../../../../../wip/planning/75-research-area-governance/master-roadmap.md)
  (substantive home; this doctrine is the area-architecture deliverable that reframes the P1-P4
  discipline buildout). Coordinated under
  [I86 Wave R+5](../../../../../wip/planning/86-initiative-cluster-execution-coordinator/tranches/wave-r-plus-5-research-radar-and-governance-integrity.md).
- **Area anchor:** [`README.md`](../README.md) — the navigable map (updated to this logic).
- **Area charter:** [`RESEARCH_AREA_CHARTER.md`](RESEARCH_AREA_CHARTER.md) — the constitution (§4 migration superseded; lifecycle reference added).
- **Discipline charters:** [Methodology](../Methodology/canonicals/METHODOLOGY_DISCIPLINE_CHARTER.md) · [Intelligence](../Intelligence/canonicals/INTELLIGENCE_DISCIPLINE_CHARTER.md) · [Diagnosis](../Diagnosis/canonicals/DIAGNOSIS_DISCIPLINE_CHARTER.md) · [Validation](../Validation/canonicals/VALIDATION_DISCIPLINE_CHARTER.md).
- **Lifecycle-adjacent disciplines:** [Research Action](../Methodology/canonicals/RESEARCH_ACTION_DISCIPLINE.md) (the ACQUIRE->PROCESS->govern loop) + [Research Radar](../Methodology/canonicals/RESEARCH_RADAR_DISCIPLINE.md) (the freshness/time axis on ACQUIRE).
- **Parent meta-doctrine:** [`HOLISTIKA_QUALITY_FABRIC.md`](../../Admin/O5-1/People/canonicals/HOLISTIKA_QUALITY_FABRIC.md) — the 5-axis composition this area composes under.
- **Governing rules:** [`akos-research-area.mdc`](../../../../../../.cursor/rules/akos-research-area.mdc) (area identity), [`akos-applied-research-discipline.mdc`](../../../../../../.cursor/rules/akos-applied-research-discipline.mdc) (research grounding), [`akos-people-discipline-of-disciplines.mdc`](../../../../../../.cursor/rules/akos-people-discipline-of-disciplines.mdc) (single-ownership + cross-area).
