---
language: en
status: active
canonical: true
role_owner: People Operations Lead + Founder + CPO
classification: doctrine
intellectual_kind: organising_manifesto
ssot: true
access_level: 5
register: internal
authored: 2026-05-15
last_review: 2026-05-15
authority: Founder + People Operations Lead + Compliance Officer + Ethics Advisor + Learning Curator
companion_to:
  - PEOPLE_AREA_RESTRUCTURE.md
  - HOLISTIKA_AGENTIC_DOCTRINE.md
  - PEOPLE_DESIGN_PATTERN_LIBRARY.md
  - Ethics/canonicals/ETHICAL_AGENTIC_BOUNDARIES.md
  - Compliance/canonicals/access_levels.md
  - Compliance/canonicals/source_taxonomy.md
  - Compliance/canonicals/confidence_levels.md
  - Operations/PMO/canonicals/KB_HUMAN_READABILITY_CHARTER.md
  - People Operations/canonicals/dimensions/ENGAGEMENT_MODEL_REGISTRY.csv
ratified_by:
  - D-IH-79-A (mega-charter scope)
  - D-IH-79-B (manifesto home)
  - D-IH-79-G (Madeira named-explicit role-class footnote)
  - D-IH-79-K (KB-stewardship-across-every-role; no new baseline_organisation row)
  - D-IH-79-H (Cursor rule akos-people-discipline-of-disciplines.mdc)
---

# Holistika Organising Doctrine

> The People manifesto. How Holistika organises itself, why we organise that way, what we owe each other and our collaborators, and the invariant principles every other area inherits.

**Item Name**: Holistika Organising Doctrine
**Item Number**: HLK-PEOPLE-DOCTRINE-001
**Version**: 1.0
**Authored**: 2026-05-15 (I79 P0 charter; I79 P1 publish)
**Ratifying Decisions**: D-IH-79-A, D-IH-79-B, D-IH-79-G, D-IH-79-H, D-IH-79-K (and the full I79 charter set D-IH-79-A..N)
**Cursor Rule**: [`.cursor/rules/akos-people-discipline-of-disciplines.mdc`](../../../../../../.cursor/rules/akos-people-discipline-of-disciplines.mdc) (always-applied; codifies the discipline this doctrine names)

---

## 0. Where this doctrine sits

This is the People area's manifesto. It belongs to People (not Marketing, not Operations, not Tech). It is internal-cleared (`access_level: 5`); the public-facing translation lives in Marketing canonicals (`BRAND_VOICE_FOUNDATION.md`, `BRAND_BASELINE_REALITY_MATRIX.md`) per the dual-register discipline. Read this side first if you carry an internal role; read the Marketing side if you address a customer / investor / advisor / regulator / partner / recruiter.

Two parents inform this doctrine:

- [`PEOPLE_AREA_RESTRUCTURE.md`](PEOPLE_AREA_RESTRUCTURE.md) — the structural restructure that split the legacy *Talent* monolith into four sub-roles: **Compliance + Ethics + Learning + People Operations** (per `D-IH-70-Q`). This doctrine builds *on top* of that structure.
- The closed I73 initiative (`D-IH-73-CLOSURE`, 2026-05-15) — the operational layer that minted [`ENGAGEMENT_MODEL_REGISTRY`](../People%20Operations/canonicals/dimensions/ENGAGEMENT_MODEL_REGISTRY.csv), the engagement-lifecycle SOPs, the [`KB_HUMAN_READABILITY_CHARTER`](../../Operations/PMO/canonicals/KB_HUMAN_READABILITY_CHARTER.md), and the [`METHODOLOGY_IP_MINTING_PATH`](../../Marketing/Brand/canonicals/METHODOLOGY_IP_MINTING_PATH.md). I79 (this doctrine + sibling P2..P6 deliverables) is the *doctrinal layer* that frames why those deliverables matter and how every other area inherits them.

---

## 1. The operating story (CPO frame, recorded verbatim)

The founder, acting as Chief People Officer, dictated the operating story when ratifying this initiative. It is preserved here because doctrine that loses its origin voice loses its centre of gravity:

> *Isn't it our job to maintain the baseline organisation? And clear the way for people to know and understand us? And to use our knowledge efficiently while ensuring healthy computational capacity? We are not research, but we manage the human way of approaching anything.*
>
> *For us, being Holistik means achieving singularity at least process-wise, holistikally. For that, you need to compress and categorize information in a way you would remember. That is easier said than done, so from our CORPINT experience we set out to create a company that is self-governable if one knows its knowledge base entirely. And if they have the capacity to anchor more people to it, even if they do not know everything, it is fine if they know their part — provided one knows exactly what that part means. That makes knowledge scalable.*
>
> *Of course the support and infrastructure is key, and we try to cover that by building a scalable knowledge base where any or almost any activity can have a place — or not. Only the architecture lets one know what our organisation is about, how we categorise our processes, a few SOPs for specific allrounder processes tactically selected, updated, researched, tested and engineered that can chart logic ways of working and specs of each role, and use cases (both internal and external) that can extend the former and can be managed as business as usual operations if well engineered.*
>
> *We hope to adapt to others' use cases with our knowledge and help them be holistik in their own way, by adapting ourselves fully to their scenario and designing the best solution we can with all of our given capabilities where relevant. That is our selling point.*

This passage is the source of every section that follows. When a future agent or operator is uncertain whether a doctrinal claim still holds, return to this passage and re-derive.

---

## 2. The People area is the discipline of disciplines

People is **not** an operations area, not a back-office function, not a hiring desk. People is the discipline that designs *how every other discipline operates* inside Holistika. That phrasing is load-bearing: People mints the patterns; other areas author their own processes from those patterns; People supports them when a breakthrough comes.

Three operational consequences follow:

1. **Pattern-mint vs process-authoring is split.** People mints **consulting design patterns** in the [`PEOPLE_DESIGN_PATTERN_REGISTRY.csv`](../Compliance/canonicals/dimensions/PEOPLE_DESIGN_PATTERN_REGISTRY.csv) (engagement-model registry; paired SOP+runbook; persona registry; classification lattice; access-level scaffolding; intelligenceops register; normalized adapter pattern; lifecycle SOP shape; cross-area breakthrough propagation; and any pattern minted by future initiatives). Other areas — Marketing/Resonance, Tech Lab/System Owner, Research, Operations, Legal, Compliance, Ethics — *author their own processes* under their own area `canonicals/` folder. People does not write another area's processes for them.

2. **Process singularity is countable, not aspirational.** Process singularity is the Holistik claim that we eventually run on a small set of patterns reused across many concrete processes (rather than re-inventing each process from scratch). To make it countable, [`process_list.csv`](../Compliance/canonicals/process_list.csv) carries a nullable `inherited_pattern_id` column (FK to `PEOPLE_DESIGN_PATTERN_REGISTRY.pattern_id`). Any area's process row can declare which People pattern parents it. The query `SELECT COUNT(*) FROM process_list WHERE inherited_pattern_id = '<X>'` yields the adoption surface of pattern X. We measure singularity, we do not preach it.

3. **Cross-area support is operational, not advisory.** When People mints a new pattern row, the breakthrough propagates to consuming areas via [`SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.md`](SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.md) and its paired runbook [`scripts/peopl_cross_area_breakthrough_announce.py`](../../../../../../scripts/peopl_cross_area_breakthrough_announce.py). People supports the consuming area's adoption — not by writing their SOPs, but by clarifying the pattern, providing examples, and iterating the pattern row when feedback comes back from the field.

This is what *discipline of disciplines* means in practice: People is upstream of every area's process design, but downstream of every area's process execution. The ratio is roughly 1:N — one pattern minted by People, N processes authored by other areas inheriting it.

---

## 3. Knowledge base stewardship is everyone's job in People

Holistika is self-governable if one knows its knowledge base entirely. We treat that as an engineering goal, not a slogan. The architecture lets a reader see what our organisation is about, how we categorise our processes, which all-rounder SOPs do the heavy lifting, what each role specifies, and which use cases — internal and external — extend the former. If the architecture is right, a new collaborator who only knows their part can still anchor to the whole *because they know exactly what their part means*.

Knowledge-base stewardship therefore lives across **every** role in the People area, not in a dedicated "knowledge base steward" role. We considered minting one and decided against it (`D-IH-79-K`). Concentrating stewardship in a single role would imply concentration of ownership; the operating story calls for distributed responsibility.

Concretely:

- **Compliance** maintains the canonical CSVs ([`baseline_organisation.csv`](../Compliance/canonicals/baseline_organisation.csv), [`process_list.csv`](../Compliance/canonicals/process_list.csv), [`PEOPLE_DESIGN_PATTERN_REGISTRY.csv`](../Compliance/canonicals/dimensions/PEOPLE_DESIGN_PATTERN_REGISTRY.csv), all dimension registries) and the access-level scaffolding ([`access_levels.md`](../Compliance/canonicals/access_levels.md), [`source_taxonomy.md`](../Compliance/canonicals/source_taxonomy.md), [`confidence_levels.md`](../Compliance/canonicals/confidence_levels.md)). This is the structural layer of the knowledge base.
- **Ethics** owns the boundary canonicals ([`ETHICAL_AUTOMATION_POSTURE.md`](../Ethics/canonicals/ETHICAL_AUTOMATION_POSTURE.md), [`ETHICAL_AGENTIC_BOUNDARIES.md`](../Ethics/canonicals/ETHICAL_AGENTIC_BOUNDARIES.md), the People Compliance vs Ethics boundary). Ethics is what we owe the people we serve and the work we do *when no one is watching*. We become unethical when we unlearn — that is the inseparability claim that ties Ethics to Learning.
- **Learning** owns the corpus and curriculum ([`LEARNING_CHARTER.md`](../Learning/canonicals/LEARNING_CHARTER.md), the Holistik Researcher onboarding curriculum, [`LEARNING_OPS_BACKLOG.csv`](../Learning/canonicals/dimensions/LEARNING_OPS_BACKLOG.csv)). Learning ensures the knowledge base does not stagnate; it cycles, gets reviewed, and matures collaborators into authors.
- **People Operations** owns the engagement-model registry, lifecycle SOPs, and the persona-routing of the knowledge base per the [`KB_HUMAN_READABILITY_CHARTER.md`](../../Operations/PMO/canonicals/KB_HUMAN_READABILITY_CHARTER.md). Different engagement classes get different readable surfaces; that mapping is People Operations' responsibility.

The Tech Lab area owns the **infrastructure** that makes the knowledge base work — file format compatibility (Obsidian-readable; Markdown-first), embedders and transformers, the path under which collaborators access knowledge through enterprise tools. Tech Lab's stewardship is technical; People's stewardship is doctrinal. Where the two layers intersect — for instance, when a knowledge-management decision affects both readable surfaces and the indexing infrastructure — People's stewardship is primary and Tech Lab co-signs.

We design the knowledge base to be agnostic by construction: the prose we write should travel from Markdown to a structured database to a customer-facing portal without losing meaning. In plain language, that means our doctrine reads in Obsidian today, stays portable to whichever indexing or rewriting tool comes next tomorrow, and transforms cleanly into the customer-facing surfaces of our enterprise knowledge tool. Nothing in our doctrine should bind us to a single vendor or tool.

---

## 4. Process singularity is the daily lever

> *Being Holistik means achieving singularity at least process-wise, holistikally.*

Process singularity is what makes the rest of the company tractable. It is also the daily lever every role pulls on, not a once-a-year strategic exercise.

What singularity looks like in motion:

1. **A new process surfaces** in any area (Marketing wants to onboard a new advisor; Tech Lab wants to add a new framework; Research wants a new program intake protocol).
2. **The author asks first**: which People design pattern parents this? They look at [`PEOPLE_DESIGN_PATTERN_LIBRARY.md`](PEOPLE_DESIGN_PATTERN_LIBRARY.md) (the human narrative) and [`PEOPLE_DESIGN_PATTERN_REGISTRY.csv`](../Compliance/canonicals/dimensions/PEOPLE_DESIGN_PATTERN_REGISTRY.csv) (the queryable rows).
3. **If a parent pattern exists**, the new process row in [`process_list.csv`](../Compliance/canonicals/process_list.csv) sets `inherited_pattern_id` to that pattern. Adoption is countable.
4. **If no parent pattern exists**, the author flags People. People decides whether the gap warrants a new pattern row (a *breakthrough*), or whether the new process is a one-off that belongs only in its area's `process_list.csv` rows.
5. **When a breakthrough lands**, the cross-area breakthrough SOP fires: People announces the new pattern; consuming areas migrate their relevant rows; the adoption surface grows.

This is not bureaucracy. It is the mechanism that compresses our process surface from N concrete processes to a small set of patterns that explain N processes. The fewer patterns we need to explain everything, the closer we get to singularity.

The complementary mechanic is **anti-duplication**: when an area mints a process that *should* have inherited a pattern but did not, the cross-area breakthrough SOP backfires the relationship. We treat duplication as a design smell to fix, not a fact of life.

---

## 5. The five invariants every area inherits

Every area in Holistika inherits five invariants from People. These are the **organising principles** any new area, role, process, SOP, or runbook must satisfy. If a deliverable cannot satisfy them, that is signal the deliverable needs redesign — not signal that the invariants need relaxing.

### 5.1 Simple

Prose that requires a glossary to parse is doctrine debt. We minimise jargon in People canonicals because People is the area that drives clarity for everyone. Technical sub-disciplines are owned by Tech Lab; their canonicals legitimately carry their vocabulary. People canonicals carry the cross-area vocabulary every collaborator can read on first encounter.

This invariant is mechanically enforced: the [`scripts/validate_design_pattern_registry.py --jargon-scan`](../../../../../../scripts/validate_design_pattern_registry.py) drift gate fails CI on forbidden tokens in People canonicals. The forbidden list is named in [`.cursor/rules/akos-people-discipline-of-disciplines.mdc`](../../../../../../.cursor/rules/akos-people-discipline-of-disciplines.mdc) §4 and revisited per cycle.

### 5.2 Actionable

Doctrine that does not change behaviour is decoration. Every doctrinal claim in this manifesto either points at a downstream artefact (SOP, runbook, validator, register row) or names the behaviour it changes. If you cannot ask *what does this make me do differently?*, the prose is not yet doctrine.

### 5.3 Shareable

What we author internally must travel without contortion to external surfaces — investors, advisors, regulators, partners, recruiters — through the dual-register translation in Marketing canonicals. We never claim two things; we claim one thing in two voices. The internal voice (this side) is precise and grounded in our experience; the external voice (Marketing side) translates without falsifying.

### 5.4 Democratic

Every collaborator anchored to Holistika gets the part of the knowledge base their access level + engagement class allow, with the architecture clear enough that they can ask intelligent questions about the parts they do not yet have. Knowledge is not hoarded by seniority; access scaffolding governs *how much* and *what kind* of knowledge each collaborator carries, and that scaffolding is documented and reviewable.

### 5.5 Friendly

We work with collaborators across enterprise, freelance, apprentice, investor, advisor, outsourced, and operator-self engagement classes (per [`ENGAGEMENT_MODEL_REGISTRY.csv`](../People%20Operations/canonicals/dimensions/ENGAGEMENT_MODEL_REGISTRY.csv)). Each class has a different posture, different knowledge access, different cadence. Friendly means designing for the collaborator we actually have, not the collaborator we wish we had. It also means we say *no* when *no* is the friendliest response (a refused task that protects the collaborator from setting themselves up to fail is friendlier than a yes that wastes their week).

---

## 6. Where AI fits — agentic is itself a discipline of disciplines

We treat AI / agentic collaboration as a People sub-discipline, not as a tool category supervised externally. Two sub-claims:

1. **AI consumes the same knowledge base humans do**, under the same access scaffolding (per [`access_levels.md`](../Compliance/canonicals/access_levels.md)). An AI collaborator at access level 3 reads the same level-3 surface a human collaborator at access level 3 reads. We do not maintain a parallel KB for agents.

2. **Agentic itself is a discipline of disciplines.** The technical sub-disciplines that compose modern agentic systems — model orchestration, retrieval, indexing, tool calling, framework choice — are owned by Tech Lab as legitimate stack vocabulary. The *doctrine* of how Holistika collaborates with agents is owned by People and lives at [`HOLISTIKA_AGENTIC_DOCTRINE.md`](HOLISTIKA_AGENTIC_DOCTRINE.md) (a sibling canonical to this one, authored at I79 P3a). Ethics anchors the red lines at [`ETHICAL_AGENTIC_BOUNDARIES.md`](../Ethics/canonicals/ETHICAL_AGENTIC_BOUNDARIES.md). Tech Lab's framework landscape canonical lives at [`AGENTIC_FRAMEWORK_LANDSCAPE.md`](../../Envoy%20Tech%20Lab/canonicals/AGENTIC_FRAMEWORK_LANDSCAPE.md).

This three-part split[^1] is not bureaucratic. It mirrors the operating story: agentic is recursive (a discipline of disciplines composed of further sub-disciplines), so its governance has to be stratified to match. People owns the readable doctrine. Tech Lab owns the technical surface. Ethics owns the red lines. None of the three substitutes for the others.

The current AI Officer of the Holistika administrative class[^2] is **Madeira**. When this manifesto refers to *Madeira* it refers to the current embodiment of the role; when the role-class population grows beyond one, this doctrine refers to the class and specific embodiments are documented at [`docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/MADEIRA-AKOS/STATUS.md`](../../Envoy%20Tech%20Lab/MADEIRA-AKOS/STATUS.md).

---

## 7. The selling point — adapting fully to others' scenarios

> *We hope to adapt to others' use cases with our knowledge and help them be holistik in their own way, by adapting ourselves fully to their scenario and designing the best solution we can with all of our given capabilities where relevant. That is our selling point.*

This sentence carries our commercial posture and our methodological posture in one breath. It says: we sell adaptability. We do not sell a method we then bend the customer to fit; we read the customer's scenario fully and design the best solution we can with the capabilities we have.

For People, that means three operational rules:

1. **Engagement-model fit before scope.** The first question we ask a new collaborator or counterparty is *which engagement class fits this scenario?* (per [`ENGAGEMENT_MODEL_REGISTRY.csv`](../People%20Operations/canonicals/dimensions/ENGAGEMENT_MODEL_REGISTRY.csv)). Wrong engagement class kills the work before scope can save it.
2. **Capability-honest scoping.** We design within our given capabilities. When a customer needs a capability we do not have, the friendliest response is to name the gap and refer; the costliest response is to over-promise.
3. **Doctrine portability.** A pattern minted at Holistika should travel to a customer engagement without losing meaning. The cross-area breakthrough propagation SOP and the design pattern library exist partly to make that travel mechanical.

When this section disagrees with a downstream canonical, this section governs. When this section disagrees with the operating story (§1), the operating story governs.

---

## 8. What this manifesto refuses to do

A short list, because doctrine that does not name its non-goals tends to expand into them:

- **No ranking of areas.** People is the discipline of disciplines, but that is a *role*, not a *rank*. Marketing, Tech Lab, Research, Operations, Legal, Compliance, Ethics, and Finance own their own SSOTs and their own decisions. People mints patterns; it does not run those areas.
- **No knowledge-base sovereignty by gatekeeping.** Every collaborator gets the access level their engagement class warrants. We do not improvise temporary access levels to manage individual relationships; the access-level scaffolding is the governance.
- **No methodology as ornament.** A pattern row exists because it is operationally true. Ornamental rows that look good in a deck and do not parent any process row should be retired at the next cycle review.
- **No re-invention without precedent search.** Any new process row that does not set `inherited_pattern_id` must explicitly state why no pattern parents it. Silence is not signal; absence is the signal.
- **No infinite regression of doctrine.** This manifesto is the doctrinal terminal. Sub-canonicals (`HOLISTIKA_AGENTIC_DOCTRINE.md`, `PEOPLE_DESIGN_PATTERN_LIBRARY.md`, the breakthrough SOP) inherit their authority from this one. We do not author manifestos for sub-areas of People.

---

## 9. How this manifesto is maintained

Maintenance cadence and accountability, codified per [`.cursor/rules/akos-executable-process-catalog.mdc`](../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 1:

- **Owner**: People Operations Lead (primary) + Founder (co-sign for material revisions).
- **Cadence**: quarterly review by default; out-of-cycle review when a downstream canonical or pattern row contradicts §1–§8 of this manifesto.
- **Revision rule**: substantive revisions require a new `D-IH-NN-X` decision row in [`DECISION_REGISTER.csv`](../Compliance/canonicals/DECISION_REGISTER.csv) and a new `last_review` date here. Minor wording revisions update `last_review` only.
- **Drift gate**: the anti-jargon scanner ([`scripts/validate_design_pattern_registry.py --jargon-scan`](../../../../../../scripts/validate_design_pattern_registry.py)) covers this file. Forbidden-token introductions fail CI.
- **Companions**: any change to §3 (KB stewardship) or §6 (AI / agentic) must check companions for consistency: [`HOLISTIKA_AGENTIC_DOCTRINE.md`](HOLISTIKA_AGENTIC_DOCTRINE.md) (sibling), [`KB_HUMAN_READABILITY_CHARTER.md`](../../Operations/PMO/canonicals/KB_HUMAN_READABILITY_CHARTER.md) (cross-area), [`AGENTIC_FRAMEWORK_LANDSCAPE.md`](../../Envoy%20Tech%20Lab/canonicals/AGENTIC_FRAMEWORK_LANDSCAPE.md) (Tech Lab side).

When this manifesto and a sub-canonical disagree, this manifesto governs. When this manifesto and the operating story (§1) disagree, the operating story governs. Both rules are recorded explicitly so a future agent never has to guess the ordering.

---

## 10. Cross-references

### Upstream (parents)

- [`PEOPLE_AREA_RESTRUCTURE.md`](PEOPLE_AREA_RESTRUCTURE.md) — the four People sub-roles (`D-IH-70-Q`).
- I73 closure (`D-IH-73-CLOSURE`) — the operational layer this doctrine sits on.
- [`FOUNDER_TRAJECTORY_INTERNAL.md`](FOUNDER_TRAJECTORY_INTERNAL.md) (`access_level: 5`) — the founder context that motivates the CPO frame.

### Sibling (this initiative I79)

- [`HOLISTIKA_AGENTIC_DOCTRINE.md`](HOLISTIKA_AGENTIC_DOCTRINE.md) (P3a) — agentic-as-discipline-of-disciplines doctrine.
- [`RESEARCH_HEAD_DISCIPLINE.md`](RESEARCH_HEAD_DISCIPLINE.md) — companion: research-first canonical-authoring discipline (Research Head doctrine; I86 Wave H Lane D, `D-IH-86-RH-A`..`H`).
- [`PEOPLE_DESIGN_PATTERN_LIBRARY.md`](PEOPLE_DESIGN_PATTERN_LIBRARY.md) (P2) — human narrative for the design pattern library.
- [`PEOPLE_DESIGN_PATTERN_REGISTRY.csv`](../Compliance/canonicals/dimensions/PEOPLE_DESIGN_PATTERN_REGISTRY.csv) (P2) — queryable design pattern rows.
- [`SOP-PEOPLE_AGENTIC_OPERATIONS_001.md`](SOP-PEOPLE_AGENTIC_OPERATIONS_001.md) (P3a) — agentic ops cadence.
- [`SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.md`](SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.md) (P4) — pattern propagation contract.
- [`ETHICAL_AGENTIC_BOUNDARIES.md`](../Ethics/canonicals/ETHICAL_AGENTIC_BOUNDARIES.md) (P3a) — Ethics anchor; red lines only.
- [`AGENTIC_FRAMEWORK_LANDSCAPE.md`](../../Envoy%20Tech%20Lab/canonicals/AGENTIC_FRAMEWORK_LANDSCAPE.md) (P3b) — Tech Lab's stack-vocabulary canonical.

### Downstream (consumers)

- Marketing canonicals — translate this to external register: [`BRAND_VOICE_FOUNDATION.md`](../../Marketing/Brand/BRAND_VOICE_FOUNDATION.md), [`BRAND_BASELINE_REALITY_MATRIX.md`](../../Marketing/Brand/BRAND_BASELINE_REALITY_MATRIX.md), [`BRAND_DO_DONT.md`](../../Marketing/Brand/BRAND_DO_DONT.md).
- Tech Lab canonicals — operational counterparts: [`AGENTIC_FRAMEWORK_LANDSCAPE.md`](../../Envoy%20Tech%20Lab/canonicals/AGENTIC_FRAMEWORK_LANDSCAPE.md) (P3b), [`SOP-TECH_AGENTIC_INFRA_001.md`](../../Envoy%20Tech%20Lab/canonicals/SOP-TECH_AGENTIC_INFRA_001.md) (P3b).
- Operations / PMO — readable surfaces: [`KB_HUMAN_READABILITY_CHARTER.md`](../../Operations/PMO/canonicals/KB_HUMAN_READABILITY_CHARTER.md).
- Every area's `process_list.csv` row — `inherited_pattern_id` FK consumers (P6).

### Decision provenance

- I79 master roadmap: [`docs/wip/planning/79-people-manifesto-and-pattern-library/master-roadmap.md`](../../../../../wip/planning/79-people-manifesto-and-pattern-library/master-roadmap.md).
- I79 decision log: [`docs/wip/planning/79-people-manifesto-and-pattern-library/decision-log.md`](../../../../../wip/planning/79-people-manifesto-and-pattern-library/decision-log.md) — D-IH-79-A..N with full rationale.
- Cursor rule: [`.cursor/rules/akos-people-discipline-of-disciplines.mdc`](../../../../../../.cursor/rules/akos-people-discipline-of-disciplines.mdc) — always-applied; ratified at P0 per `D-IH-79-H`.

---

[^1]: Three-part means **People doctrine** (this manifesto + `HOLISTIKA_AGENTIC_DOCTRINE.md` + `SOP-PEOPLE_AGENTIC_OPERATIONS_001.md`) for the readable, jargon-free side; **Tech Lab landscape** (`AGENTIC_FRAMEWORK_LANDSCAPE.md` + `SOP-TECH_AGENTIC_INFRA_001.md`) for the technical, jargon-bearing side; **Ethics anchor** (`ETHICAL_AGENTIC_BOUNDARIES.md`) for the minimal red-lines-only side. Ratified at I79 P0 per `D-IH-79-F` (round 3 amendment) + `D-IH-79-L` (P3a/P3b split) + `D-IH-79-M` (Tech Lab landscape ownership).

[^2]: AI O5-1 is the role class; *Madeira* is the current embodiment per the I76 candidate. When the role-class population grows, this doctrine refers to the class. Per `D-IH-79-G` (Madeira named-explicit role-class footnote pattern).
