---
intellectual_kind: capability_collapse_map
parent_initiative: INIT-OPENCLAW_AKOS-95
lane: L2 — Capability de-densify (R2-01) · area slice = Research
area: Research
authored: 2026-06-08
status: proposed
proposes_under: D-IH-95-H
language: en
audience: J-OP;J-AIC
register: internal
control_confidence_level: Euclid
internal_citations: 9
external_citations: 4
linked_decisions:
  - D-IH-95-H   # L2 capability de-densify ratification (organic count; capability_tier; bearer_class->edge)
  - D-IH-95-G   # R2-01 keep-separate + de-densify; R2-02 sellable CI-quality -> Research
  - D-IH-82-P   # CAPABILITY_REGISTRY seed mint (the 1:1 process-shadow being collapsed)
linked_canonicals:
  - docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/CAPABILITY_REGISTRY.csv
  - docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/COMPONENT_PRIMITIVE_REGISTRY.csv
  - docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/TOPIC_REGISTRY.csv
  - docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_BASELINE_REALITY_MATRIX.md
  - docs/references/hlk/v3.0/Research/canonicals/RESEARCH_AREA_CHARTER.md
note: >
  Proposed (not executed) de-densification of the Research-area slice of CAPABILITY_REGISTRY
  (82 process-shadow rows -> 12 stable capabilities). The collapse itself is a GATED canonical-CSV
  change (per-domain slice per D-IH-95-H); this doc is the reviewable proposal for the Research gate.
  Research = the corporate-intelligence (CORPINT) area (R2-02). Internal register is permitted here
  (docs/wip/intelligence/**) but every differentiating capability carries its external rendering so
  the `translatability` confidence axis is legible at collapse-time.
---

# L2 collapse map — **Research** area (82 → 12)

> **One-line result:** the Research-area slice de-densifies from **82 process-shadow rows** to
> **12 stable capabilities**, all under the L1 domain **Corporate Intelligence & Research**,
> organised along the CORPINT information lifecycle. **70 rows** roll up into the 12; **12 rows**
> are flagged out (2 belong to Delivery & Client Engagement Ops, 10 are mind-map imports naming
> other areas' work). **Zero** code-symbol evictions to the component registry (the Research slice
> has none). Every one of the 82 rows is accounted for below.

This is the first area collapse-map authored under the **L2 lane** of I95 (capability de-densify,
ratified **D-IH-95-H**). It follows the 6-step collapse method in
[`l2-capability-densify-findings-2026-06-07.md`](../l2-capability-densify-findings-2026-06-07.md)
§3.2 and uses the same 5-section shape the lane expects (proposed capabilities → rollup → evictions
→ cross-area flags → count summary).

**Why Research is special.** Research is not a research-action queue — it is Holistika's
**corporate-intelligence operating system across the full information lifecycle**
(`acquire → process → store → recall → share → protect`, per
[`akos-research-area.mdc`](../../../../../.cursor/rules/akos-research-area.mdc) RULE 1). That lifecycle
maps cleanly onto the standard five-phase **intelligence cycle** used in intelligence studies —
*planning & direction → collection → processing → analysis & production → dissemination* — with the
recognised collection disciplines **OSINT** and **HUMINT** and the primary type **counter-intelligence
(CI)** [E-1][E-3][E-4]. I use that lifecycle as the **spine** of the map so the capabilities are
mutually exclusive by *stage of the cycle*, not by org unit. The sellable "corporate-intelligence
quality" the operator routed to Research under R2-02 is precisely the differentiating band of this
map (the elicitation / source-grading / reporting trio), and those are exactly the capabilities that
score **low on `translatability`** — the internal CORPINT name does not render cleanly to an external
audience, so each carries its external rendering per the dual-register matrix [I-7].

---

## Section 1 — Proposed capabilities (the stable WHAT)

12 capabilities, all `L1 = Corporate Intelligence & Research`. Names are **noun/gerund,
outcome-oriented, technology-neutral** (collapse method step 4). `tier` is the proposed
`capability_tier` (added empty at the D-IH-95-H pre-step) — **differentiating** = the sellable CI
edge; **utility** = table-stakes research hygiene. `→ external` is the translated rendering for any
non-cleared audience (the `translatability` axis); "clean" means the internal name already renders
externally.

| # | Proposed ID | L2 capability (stable WHAT) | Lifecycle stage | Tier | → External rendering (translatability) | Rolls up |
|:--|:--|:--|:--|:--|:--|:--:|
| 1 | `CAP-RES-01` | **Deep Research Methodology & Source-Ledger Discipline** | Planning & Direction (spine) | differentiating | *Structured Research Methodology* (clean) | 4 |
| 2 | `CAP-RES-02` | **Counterparty Elicitation & Human-Source Discovery** | Collection — HUMINT | differentiating | *Structured Stakeholder Discovery* (**low** — "counterparty"/"elicitation" must translate) | 6 |
| 3 | `CAP-RES-03` | **Open-Source Intelligence Collection (OSINT)** | Collection — OSINT | differentiating | *Open-Source / Web & Social Research* (medium) | 5 |
| 4 | `CAP-RES-04` | **Secondary Research & Evidence Synthesis** | Collection / Processing — desk | utility | *Secondary Research & Evidence Synthesis* (clean) | 3 |
| 5 | `CAP-RES-05` | **Source Reliability Grading & Credibility Assessment** | Processing | differentiating | *Source Confidence Scoring* (**low** — "reliability grading" must translate) | 2 |
| 6 | `CAP-RES-06` | **Intelligence Classification & Fact Structuring** | Processing | differentiating | *Evidence Structuring & Tagging* (medium-low) | 3 |
| 7 | `CAP-RES-07` | **Analytic Assessment, Frameworks & Foresight** | Analysis & Production | differentiating | *Analysis, Scenario & Foresight* (clean) | 10 |
| 8 | `CAP-RES-08` | **Competitive & Market Intelligence** | Analysis & Production — applied | differentiating | *Competitive & Market Intelligence* (clean) | 2 |
| 9 | `CAP-RES-09` | **Business & Process Engineering Analysis** | Analysis & Production — applied | differentiating | *Business & Process Engineering Analysis* (clean) — *cross-area candidate, see §4* | 3 |
| 10 | `CAP-RES-10` | **Intelligence Reporting & Research Output Packaging** | Dissemination | differentiating | *Research Briefing & Deliverable Packaging* (**low** — "intelligence report" must translate) | 7 |
| 11 | `CAP-RES-11` | **Research Knowledge Base, Pipeline & Freshness** | Store / Recall | utility | *Research Knowledge Base & Pipeline* (clean) | 7 |
| 12 | `CAP-RES-12` | **Multi-Domain Research Coverage & Sense-Making** | Coverage (cross-stage) | utility | *Multi-Domain Research Coverage* (clean) | 18 |

**Lifecycle coverage check (a finding, not just a layout).** Five of the six CORPINT stages are
staffed by ≥1 capability. **`protect` (counter-intelligence) is unstaffed** — no row maps to a
counter-intelligence ability; the closest signals ("Security & Intelligence" subject tags) are
*coverage topics*, not a CI capability. This matches the known thin-stage warning in
[`akos-research-area.mdc`](../../../../../.cursor/rules/akos-research-area.mdc) RULE 1 ("the thin stages
today are SHARE/OUTAKE, RECALL, PROTECT") and the intelligence-doctrine fact that CI is a *primary*
type, not optional [E-4]. **Recommendation:** leave `protect` as an explicit, named gap in the map
(do not invent a hollow row) and surface it to the Semantic Council as a future capability to mint.

**Translatability finding.** The three lowest-translatability capabilities (`CAP-RES-02`, `-05`,
`-10`) are exactly the **differentiating** ones. This is the `translatability` confidence axis doing
its job: the capabilities that most differentiate Holistika are the ones whose *internal* names leak
tradecraft and therefore must be translated before any external render [I-7]. At rating time these
three should score low on `translatability` and high on the other four axes.

---

## Section 2 — Rollup (every source row → its capability)

Each block lists the **source rows that collapse into one capability**, with the collapse ratio.
`originating_process_ids` for the new capability (TRP-006, N:N) = the union of the listed rows'
process IDs. The 8 `active` rows are tagged **(active)**; all others are `planned` seed-shadows.

**`CAP-RES-01` Deep Research Methodology & Source-Ledger Discipline — 4 → 1**
- `CAP-HOL-RESEA-DTP-302` Deep Research Methodology
- `CAP-HOL-RESEA-DTP-RESEARCH-ACTION-001` Research Action source-ledger + 8-stage operating loop **(active)**
- `CAP-HOL-RESEA-DTP-161` Research Dos & Dont's for a given process
- `CAP-GTM-RESEARCH-DTP-1` Build Research Process
- *The methodology spine — the ACQUIRE/PROCESS discipline that governs how every other research capability runs.*

**`CAP-RES-02` Counterparty Elicitation & Human-Source Discovery (HUMINT) — 6 → 1**
- `CAP-HOL-RES-PRC-COUNTERPARTY-BASELINE-ASSESS-001` Counterparty baseline reality assessment **(active)**
- `CAP-HOL-RES-PRC-ELICITATION-DISCIPLINE-001` Elicitation discipline **(active)**
- `CAP-HOL-RESEA-DTP-94` Enriched Interview · `CAP-HOL-RESEA-DTP-95` Focus group
- `CAP-HOL-RESEA-DTP-310` Stakeholder Interview Protocol · `CAP-HOL-RESEA-DTP-311` Field Observation
- *All human-source collection. `discovery_questionnaire_001` co-realizes this via N:N but its home is Delivery — see §4.*

**`CAP-RES-03` Open-Source Intelligence Collection (OSINT) — 5 → 1**
- `CAP-HOL-RESEA-DTP-322` Web Intelligence Gathering · `CAP-HOL-RESEA-DTP-323` Social Media Intelligence
- `CAP-HOL-RESEA-DTP-324` Publication Monitoring
- `CAP-GTM-RESEARCH-DTP-2` Gather Research Channels · `CAP-GTM-RESEARCH-DTP-4` Scrape Reseach Channels *(sic)*
- *All open-source collection — the OSINT discipline [E-1][E-5]. The OSINT-Analyst-owned rows + the channel-gathering/scraping process rows are one ability.*

**`CAP-RES-04` Secondary Research & Evidence Synthesis — 3 → 1**
- `CAP-HOL-RESEA-DTP-317` Literature Review · `CAP-HOL-RESEA-DTP-319` Multi-Source Synthesis
- `CAP-HOL-RESEA-DTP-320` Contradiction Resolution

**`CAP-RES-05` Source Reliability Grading & Credibility Assessment — 2 → 1**
- `CAP-HOL-RES-PRC-RELIABILITY-GRADING-001` Source reliability grading **(active)**
- `CAP-HOL-RESEA-DTP-312` Source Credibility Assessment

**`CAP-RES-06` Intelligence Classification & Fact Structuring — 3 → 1**
- `CAP-HOL-RESEA-DTP-142` Place in Intelligence Matrix · `CAP-HOL-RESEA-DTP-143` Classify Intel
- `CAP-HOL-RESEA-DTP-313` Fact Table Entry

**`CAP-RES-07` Analytic Assessment, Frameworks & Foresight — 10 → 1**
- `CAP-HOL-RESEA-DTP-154` Intelligence Assessment · `CAP-HOL-RESEA-DTP-303` Intelligence Assessment Cycle
- `CAP-HOL-RESEA-DTP-99` HxPESTAL · `CAP-HOL-RESEA-DTP-315` PESTEL Analysis · `CAP-HOL-RESEA-DTP-110` 6 Ws
- `CAP-HOL-RESEA-DTP-100` Create Analogy · `CAP-HOL-RESEA-DTP-283` Foresight (Variable Scenario Analysis)
- `CAP-HOL-RESEA-DTP-314` Temporal Impact Analysis
- `CAP-HOL-RESEA-DTP-150` Generational Filter · `CAP-HOL-DTP-162` Generational Filter (execution task)
- *The analyst's processing toolkit + the judgment it produces. `150`+`162` are the same lens under two conventions (dedup, see §3). The analysis step is what converts information into intelligence [E-4].*

**`CAP-RES-08` Competitive & Market Intelligence — 2 → 1**
- `CAP-HOL-RESEA-DTP-230` Competitive Intelligence and Positioning · `CAP-HOL-RESEA-DTP-316` Competitive Benchmarking

**`CAP-RES-09` Business & Process Engineering Analysis — 3 → 1** *(cross-area candidate)*
- `CAP-HOL-RESEA-DTP-280` Process Engineering (Ingenieria de Procesos)
- `CAP-HOL-RESEA-DTP-281` Business Engineering (Ingenieria de Negocios)
- `CAP-HOL-RESEA-DTP-282` Factor Combination (Process + Business Alignment)
- *Kept in Research (role_owner = Holistik Researcher; an analytic modelling ability) but flagged for Delivery/Strategy review — see §4.*

**`CAP-RES-10` Intelligence Reporting & Research Output Packaging — 7 → 1**
- `CAP-HOL-RES-PRC-INTELLIGENCE-REPORT-001` Intelligence report **(active)**
- `CAP-HOL-RESEA-DTP-318` Research Brief · `CAP-HOL-RESEA-DTP-321` Research Output Packaging
- `CAP-HOL-RESEA-DTP-144` Output 1 · `CAP-HOL-RESEA-DTP-145` Output 2 · `CAP-HOL-RESEA-DTP-146` Output 3
- `CAP-HOL-RESEA-DTP-112` List Examples for Engage Project Charter
- *The DISSEMINATION stage [E-3]. "Output 1/2/3" are vague seed names for report-packaging variants; `112` is a task-grain micro-step that realizes packaging, not its own capability.*

**`CAP-RES-11` Research Knowledge Base, Pipeline & Freshness — 7 → 1**
- `CAP-HOL-RESEA-DTP-RESEARCH-RADAR-001` Research Radar freshness sweep **(active)**
- `CAP-GTM-PROC-RESEARCH-PIPELINE` Research material pipeline execution
- `CAP-GTM-CL-7981FE46F14496` Research material — curated learning playlists
- `CAP-GTM-CL-C1DADAF241D4C5` Research material pipeline execution — sources: Pipeline
- `CAP-GTM-RESEARCH-DTP-5` Build Data Governance for Research · `CAP-GTM-RESEARCH-DTP-20` Research Material (2)
- `CAP-SOP-FLOWMAKER-RESEARCH-PIPELINE-002` FlowMaker Research Pipeline
- *The STORE/RECALL stage. "Build Data Governance for Research" co-realizes the Data area's governance capability via N:N (noted §4). The two `CAP-GTM-CL-*` rows carry mojibake/hash IDs — data-quality flag in §3.*

**`CAP-RES-12` Multi-Domain Research Coverage & Sense-Making — 18 → 1**
- Subject-domain rows (first pass): `CAP-GTM-RESEARCH-DTP-8` People · `-9` Security & Intelligence ·
  `-13` Macro Economists & Investments · `-14` AI · `-15` Politics · `-16` Social · `-17` Logic ·
  `-18` Legal · `-19` UX – Customer Relationship
- Convention-duplicate `(2)` rows: `CAP-GTM-RESEARCH-DTP-22` People (2) · `-23` Security & Intelligence (2) ·
  `-27` Macro Economists & Investments (2) · `-28` AI (2) · `-29` Politics (2) · `-30` Social (2) ·
  `-31` Logic (2) · `-32` Legal (2) · `-33` UX – Customer Relationship (2)
- *These are **subjects the research function covers**, not capabilities. They collapse into one
  "ability to run structured intelligence across a standing subject portfolio." The 9 `(2)` rows are
  pure convention duplicates of the first 9 (cross-convention dedup, method step 3). **Strong
  recommendation:** the subject list itself belongs in `TOPIC_REGISTRY` (the L5 topic spine,
  D-IH-95-H), not the capability registry — see §3 soft-eviction.*

**Subtotal rolled up into the 12 capabilities: 70 rows.** The remaining **12 rows** are flagged out
in §4 (cross-area). Detailed dedup / eviction dispositions in §3.

> **Note — divergence from the illustrative cluster #11.** The L2 method doc's worked cluster #11
> ("Counterparty Intelligence & Source-Grading", ~5→1) fused elicitation + baseline-assessment +
> reliability-grading + intelligence-report into a single capability *as a scale-illustration* across
> the 1,119-row registry. Doing the Research area in detail with an **organic count** (D-IH-95-H), I
> deliberately split that into three lifecycle-distinct capabilities (`CAP-RES-02` collection,
> `CAP-RES-05` processing, `CAP-RES-10` dissemination). Rationale: they have **different maturity
> profiles** (a team can elicit well but report poorly), so separate rows make the weekly
> confidence-rating loop meaningful — which is the whole point of de-densifying [L2 §4].

---

## Section 3 — Evictions

The L2 method's headline eviction class is **code symbols → component registry** (`LLMConfig`,
`Sentiment Analyzer`, `*_SYSTEM_PROMPT`) [I-1 §3.2 step 1]. Applied to Research:

**(a) Component-registry evictions: ZERO.** The Research slice contains **no** code-symbol rows. The
~27 code-symbols D-IH-95-H earmarked for eviction are all in the **Applied AI & MADEIRA** area
(registry rows 600–626 [I-1]), not Research. `COMPONENT_PRIMITIVE_REGISTRY.csv` today holds 25
deliverable/UI composition primitives (`CP-COVER-PAGE` … `CP-CONFIDENTIALITY-BLOCK`) [I-4] — the
Research collapse **adds nothing** to it. *This is a clean, falsifiable result: the Research-area
noise is duplication + subject-tags + mind-map imports, not buried components.*

**(b) Convention-duplicate eliminations (method step 3 — not carried as separate rows):**
- The **9 `(2)` subject rows** (`CAP-GTM-RESEARCH-DTP-22/23/27/28/29/30/31/32/33`) are byte-for-byte
  duplicates of `-8/9/13/14/15/16/17/18/19` under a `(2)` naming convention. Folded into `CAP-RES-12`.
- `CAP-HOL-DTP-162` "Generational Filter (execution task)" duplicates `CAP-HOL-RESEA-DTP-150`
  "Generational Filter" (note its **malformed ID** `hol__dtp_162` — empty entity segment, a seed
  artifact). Folded into `CAP-RES-07`.

**(c) Soft-eviction to `TOPIC_REGISTRY` (recommended at collapse-time):** the **18 subject-domain
rows** rolled into `CAP-RES-12` represent *subjects the research function covers* (People, Security &
Intelligence, Macro/Investments, AI, Politics, Social, Logic, Legal, UX–Customer Relationship), not
abilities. The single capability `CAP-RES-12` stays; the **subject list itself should be re-homed as
`subject_kind` rows in `TOPIC_REGISTRY`** (the L5 topic spine, D-IH-95-H [I-2][I-8]). This keeps the
capability registry strategic and routes the coverage taxonomy to the dimension that owns it — a
direct hand-off between the L2 (capability) and L5 (topic) lanes.

**(d) Data-quality flags (clean at collapse-time, do not evict):**
`CAP-GTM-CL-7981FE46F14496` and `CAP-GTM-CL-C1DADAF241D4C5` carry **mojibake** (the `–` em-dash
rendered as `�`) and **hash-based source IDs** — Trello-card import artifacts. Normalise the
capability name when minting `CAP-RES-11`.

---

## Section 4 — Cross-area flags (12 rows that are not Research capabilities)

**1. → Delivery & Client Engagement Ops (2 rows, both `active`).**
- `CAP-HOL-ENG-PRC-ENGAGEMENT-DESIGN-001` Engagement design (multi-cell)
- `CAP-HOL-ENG-PRC-DISCOVERY-QUESTIONNAIRE-001` Discovery questionnaire ops

  Both are `hol_eng_prc_*` engagement processes; the L2 worked **cluster #12** homes them in
  *"Engagement Design, Estimation & Proposal"* under Delivery & Client Engagement Ops [I-1 §3.3].
  They are tagged `area=Research` only because `role_owner=Holistik Researcher`. **Disposition:**
  capability home = Delivery (counted in the Delivery slice, not Research's 12). `discovery_questionnaire`
  **co-realizes** `CAP-RES-02` (elicitation) via N:N — a process may realize capabilities in two areas.

**2. → Other-area mind-map imports (10 rows).** The GTM "Research material" board mixed subjects with
team-function names; these 10 name *other areas'* work, not Research abilities:

| Row | Capability home |
|:--|:--|
| `CAP-GTM-RESEARCH-DTP-3` Integrate Research Material into MADEIRA | Applied AI & MADEIRA |
| `CAP-GTM-RESEARCH-DTP-6` Build UI for KMS/MADEIRA interaction | Product & Platform Eng / Applied AI |
| `CAP-GTM-RESEARCH-DTP-10` Design · `-24` Design (2) | Go-to-Market & Brand / Product |
| `CAP-GTM-RESEARCH-DTP-11` System Design · `-25` System Design (2) | Product & Platform Engineering |
| `CAP-GTM-RESEARCH-DTP-12` Content & Channel Strategy · `-26` (2) | Go-to-Market & Brand |
| `CAP-GTM-RESEARCH-DTP-7` Office Automation · `-21` (2) | Operations / Tech (or `task`-grain) |

  **Disposition:** do **not** carry as Research capabilities. They collapse into the named area's
  capability as realizing processes (N:N) or remain `task`-grain `process_list` rows. The
  conservative, de-densify-correct call: flag to the named area's collapse-map; the Research gate
  does not adopt them.

**3. Boundary note — `CAP-RES-09` Business & Process Engineering Analysis.** Kept in Research
(role_owner = Holistik Researcher; an analytic modelling lens), but *"Ingenieria de Negocios/
Procesos"* could equally sit in **Delivery & Client Engagement Ops** or a future **Strategy** L1.
Surface to the Semantic Council; **default = keep in Research**.

**4. N:N edges to record at collapse-time (links, not removals).**
- `CAP-RES-11` (via "Build Data Governance for Research") co-realizes **Data Governance & Enterprise
  Knowledge**.
- `CAP-RES-09` associates with **Delivery / Strategy** (see boundary note).

**5. Lifecycle gap — `protect` (counter-intelligence).** Cross-*stage*, not cross-area: no Research
row maps to a CI ability [E-4]. Flag to the Semantic Council as a future capability to mint; do not
fabricate a hollow row now.

---

## Section 5 — Count summary (82 → 12)

| Bucket | Rows |
|:--|:--:|
| **Source rows** (Research area, `CAPABILITY_REGISTRY.csv`) | **82** |
| − Cross-area flags → **Delivery & Client Engagement Ops** (§4.1) | −2 |
| − Cross-area flags → Product / GTM / Applied-AI / Ops (§4.2) | −10 |
| = Rows rolling up into Research-owned capabilities | **70** |
| **Proposed Research capability map** (§1) | **12** |
| Component-registry evictions (§3a) | **0** |

**Result: 82 → 12.** Collapse ratio ≈ **6.8 : 1** overall (≈ **5.8 : 1** counting only the 70 in-area
rows). All 12 capabilities sit under L1 **Corporate Intelligence & Research**, spanning **5 of 6**
CORPINT lifecycle stages (`protect` is a named, deliberate gap).

**Within the 70 in-area rows:** 9 are `(2)` convention duplicates eliminated by dedup; 1 is the `162`
lens duplicate; 18 subject rows are soft-recommended for `TOPIC_REGISTRY` (the subject list, not the
capability). **8 `active` rows preserved** — 6 land in Research (`CAP-RES-01/02×2/05/10/11`), 2 flag
to Delivery (`engagement_design`, `discovery_questionnaire`).

**Every one of the 82 source rows is accounted for** across §2 (70 roll up) + §4 (12 flagged out).

**Gate posture.** This collapse is a **gated canonical-CSV change** (per-domain slice, D-IH-95-H
[I-2]); this doc is the reviewable Research proposal. At execution: assign final `capability_id`s
(proposed `CAP-RES-NN`), set `capability_tier` per §1, wire `originating_process_ids` (TRP-006, N:N),
place `bearer_class` on the realization **edge** (not the row), and run `validate_hlk.py`.

---

## Citations

**Internal**
- **[I-1]** [`l2-capability-densify-findings-2026-06-07.md`](../l2-capability-densify-findings-2026-06-07.md) — 6-step collapse method (§3.2); worked clusters #11/#12 (§3.3); code-symbol eviction class.
- **[I-2]** [`decision-log.md`](../../../planning/95-canonical-articulation-model/decision-log.md) D-IH-95-H — organic area-by-area count; `capability_tier`; `bearer_class`→edge; per-domain gated tranche.
- **[I-3]** `CAPABILITY_REGISTRY.csv` — the 82 Research-area process-shadow rows being collapsed.
- **[I-4]** `COMPONENT_PRIMITIVE_REGISTRY.csv` — 25 deliverable/UI primitives; eviction target (zero Research adds).
- **[I-5]** [`akos-research-area.mdc`](../../../../../.cursor/rules/akos-research-area.mdc) RULE 1 — CORPINT lifecycle (`acquire→process→store→recall→share→protect`); thin-stage warning.
- **[I-6]** [`RESEARCH_AREA_CHARTER.md`](../../../../../docs/references/hlk/v3.0/Research/canonicals/RESEARCH_AREA_CHARTER.md) — Research = corporate-intelligence area.
- **[I-7]** [`BRAND_BASELINE_REALITY_MATRIX.md`](../../../../../docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_BASELINE_REALITY_MATRIX.md) §3 — dual-register translation (counterparty / elicitation / reliability-grading / intelligence-report → external); the `translatability` axis.
- **[I-8]** `TOPIC_REGISTRY.csv` — L5 topic spine; soft-eviction target for the 18 subject rows.
- **[I-9]** `decision-log.md` D-IH-95-G — R2-01 keep-separate + de-densify; R2-02 sellable CI-quality → Research.

**External**
- **[E-1]** Maltego — *Understanding the Different Types of Intelligence Collection Disciplines* (OSINT/HUMINT; the INTs). https://www.maltego.com/blog/understanding-the-different-types-of-intelligence-collection-disciplines/
- **[E-3]** IOSS — *Intelligence Threat Handbook* §2 (the five-phase intelligence cycle; planning→collection→processing→dissemination). https://irp.fas.org/nsa/ioss/threat96/part02.htm
- **[E-4]** US DoD — *JP 2-0, Chapter II* (intelligence cycle; **counter-intelligence (CI) as a primary source type**; "analysis transforms information into intelligence"). https://irp.fas.org/doddir/dod/jp2-0/j2-0ch2.htm
- **[E-5]** US Naval War College — *Types of Intelligence Collection* (OSINT; collection-discipline taxonomy). https://usnwc.libguides.com/c.php?g=494120&p=3381426

## Cross-references
- Parent lane: I95 master-roadmap → **L2** (capability de-densify); sibling area collapse-maps land beside this one under `l2-collapse-maps/`.
- Method: [`l2-capability-densify-findings-2026-06-07.md`](../l2-capability-densify-findings-2026-06-07.md) [I-1].
- Hands off to: L5 topic lane (the §3c subject-row soft-eviction → `TOPIC_REGISTRY` [I-8]).
- Governs the gate: capability collapse = canonical-CSV gate ([`akos-baseline-governance.mdc`](../../../../../.cursor/rules/akos-baseline-governance.mdc)); the Research-area identity ([`akos-research-area.mdc`](../../../../../.cursor/rules/akos-research-area.mdc) [I-5]).
