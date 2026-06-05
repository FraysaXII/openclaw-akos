---
intellectual_kind: research_brainstorm
parent_initiative: INIT-OPENCLAW_AKOS-94
related_initiatives: [93, 88, 23, 25, 32, 7]
authored: 2026-06-05
status: active
language: en
named_decision: D-ARTIC (canonical articulation model)
control_confidence_level: Keter
note: MADEIRA-grade craft per operator request; foundational metamodel; destined for option-set ratify then research-action formalisation
---

# Canonical Articulation Model — brainstorm (how everything links, across layers)

> **Operator brief (2026-06-05, verbatim):** *"I never got how to properly link role with
> processes knowing each have layers, let alone with other articulable canonicals, like topic,
> project, workstream, engagement, component, or any other canonical artifact or each between
> themselves. I really need help to decide about this … you will need to go craft again … the
> best of your help as my MADEIRA AIC … extra computational capacity and a lot of brainstorming
> and research and context awareness, well and empathy to understand how people and AIC will
> behave or interact around this."*
>
> This is that craft. It is a **brainstorm + proposed model + option set** — no canonical edit
> until you pick. If you pick a build option, it formalises into a full research-action pack
> (source ledger + the 8-stage loop).

## 1. The problem, named precisely

Holistika has **~20 canonical artifact types**. Each has **internal layers** (a hierarchy
within the type). And they must **link to each other**. Today there is **no single model** that
says (a) what the types are, (b) what relationships are allowed between them, (c) how the layers
nest. It grew organically — one FK column per CSV, one edge type per initiative.

**The smoking gun** (from the live Neo4j projection, `akos/hlk_graph_model.py`): the *same*
whole-part relationship is **forked into three edge names** — `PARENT_OF` (process),
`PROGRAM_PARENT_OF` (program), `TOPIC_PARENT_OF` (topic) — and `TOPIC_SUBSUMES` /
`PROGRAM_SUBSUMES` again. They were renamed each time *to avoid collision* because no metamodel
said "this is one relationship; the node labels already disambiguate." That forking is the cost
of having no articulation model. It will keep happening every time a new canonical type lands.

## 2. The two sub-problems (your "each have layers" + "between themselves")

| Sub-problem | Example | What it needs |
|:---|:---|:---|
| **Intra-type layers** | process: process→activity→task (APQC); role: reports_to seniority; topic/area/program: parent→child | a **whole-part** relationship (one type), recursive |
| **Inter-type links** | role *performs* process; process *realizes* capability; engagement *consumes* process; decision *influences* anything; pattern *parents* process | a **closed set of typed relationships** with valid (source→target) rules |

## 3. The external answer — three frameworks that already solved this

**ArchiMate 3.1** (The Open Group — the enterprise-architecture metamodel) is the direct hit. It
defines a **closed set of ~10 relationship types** that link elements *across layers*:

| ArchiMate relationship | Meaning | Holistika use (replaces today's ad-hoc edge) |
|:---|:---|:---|
| **Composition** | strong whole-part (part dies with whole) | area→sub-area; process→activity→task (`PARENT_OF`/`PROGRAM_PARENT_OF`/`TOPIC_PARENT_OF` → **one** edge) |
| **Aggregation** | weak whole-part (part lives independently) | topic aggregates facts; program aggregates initiatives |
| **Assignment** | who performs / owns / is responsible | role→process (`OWNED_BY`); role→role (`REPORTS_TO`); area→role |
| **Realization** | concrete realizes abstract | process *realizes* capability; pattern *realizes-as* process (inherited_pattern_id); discipline *realizes* a Quality-Fabric specialty |
| **Serving** | provides function to a consumer | engagement *served-by* process; platform area *serves* every area; adapter *serves* a channel |
| **Access** | behavior reads/writes passive data | process *accesses* a registry/dataset |
| **Influence** | affects a motivation element | decision *influences* process/area; OPS *influences* initiative |
| **Triggering** | temporal/causal sequence | process→process handoff; lifecycle stage→stage |
| **Flow** | transfer between elements | engagement→FINOPS counterparty; producer→consumer (`PRODUCES_FOR`/`CONSUMES`) |
| **Specialization** | "is a kind of" | sub-mark *specializes* brand; persona *specializes* audience |

The genius for us: **the relationship type is the edge; the node labels disambiguate context.**
"Parent-of" is *composition* whether the nodes are processes, programs, or topics — so the three
forked edges collapse to **one**. ArchiMate also formalises **derivation** — indirect
relationships inferred from a chain (role→process→capability ⇒ role *contributes-to* capability)
— which is exactly the cross-layer query you could never express.

**Property-graph rules** (Neo4j — what we already run): use *specific* relationship types (never
a generic `RELATED_TO` filtered by property); labels classify entities; **promote a relationship
to a node when it carries its own metadata** (e.g. an *engagement* is a relationship between a
counterparty and our delivery that grew enough metadata to become its own node). This tells us
*when a link becomes a canonical type*.

**Zachman** (the enterprise ontology — what/how/where/who/when/why) is the **coverage lattice**:
it lets us verify the model has no blind spot — Who=role, How=process, What=topic/component/data,
Why=decision/motivation, When=cadence/lifecycle, Where=area/entity. Every canonical type sits in
a Zachman cell; every relationship crosses cells.

## 4. The proposed model — Holistika Canonical Articulation Model (HCAM)

**(a) Entity catalog** — the closed set of canonical artifact types (node labels). Today's graph
has 10 (Role, Process, Program, Topic, Persona, Channel, Sourcing, Skill, TouchpointKitCell,
Policy). The full set adds the ~10 not-yet-projected: **Capability, Component, Engagement,
Decision, OPS-action, Pattern, Area, Entity, Adapter, Audience, Source/Fact, Workstream**. Each
maps to one Zachman cell + one ArchiMate layer.

**(b) Relationship taxonomy** — the closed ArchiMate-grounded set (§3 table). ~10 typed
relationships replace the 13 forked edges. A **`CANONICAL_RELATIONSHIP_REGISTRY.csv`** governs
the valid `(source_type, relationship, target_type)` triples — the ArchiMate "metamodel rules"
made into a queryable CSV (e.g. `Role —assignment→ Process` valid; `Topic —assignment→ Role`
invalid).

**(c) Layers = composition/aggregation** — intra-type hierarchies (process granularity, role
seniority, topic/area/program trees) are all **composition** (or aggregation where parts live
independently). One recursive relationship, not N forked ones.

**(d) SSOT unchanged** — the CSV registries stay the authoring SSOT (the FK columns *are* the
edges); Neo4j is the rebuildable projection; HCAM is the **metamodel layer above both** (like
DAMA-DMBOK's metadata layer). No re-authoring of content — a re-interpretation + a thin registry.

## 5. The empathy lens (how people + AICs behave around this)

This is why a *closed* taxonomy matters more than a clever one:

- **A person learns ~10 verbs, not 13+ growing edge names.** "Who is *assigned* this? What does
  it *realize*? What *serves* this engagement?" is teachable on day one. Forked edges
  (`PROGRAM_PARENT_OF` vs `TOPIC_PARENT_OF`) are not — they're memorization.
- **An AIC queries uniformly.** A closed relationship set is a small, stable vocabulary an agent
  can reason over without re-learning per type. The MADEIRA-style "show me the chain from this
  role to the capabilities it ultimately realizes" becomes one derivation query, not bespoke code.
- **New canonical types stop forking the graph.** When the next type lands (say *workstream*), it
  reuses the existing relationship verbs against its valid triples — no new edge name, no
  collision-rename. The model *absorbs* growth instead of accreting debt. (This is the operator's
  "scalable even in management and ops" applied to the metamodel itself.)
- **Governance, not gatekeeping.** The valid-triple registry makes "can X link to Y?" an
  answerable, reviewable fact — no exceptions on key chains, exactly as you required.

## 6. Option set — D-ARTIC (you pick; beyond-A options included per your nudge)

| # | Option | Scope | Risk | What you get |
|:--|:---|:---|:---|:---|
| **A** | sub_area FK only | narrow | none | solves AREA-16 sub-folder=role; leaves the deep linking unsolved (the thing you've never cracked) |
| **B** | **Relationship registry first** (`CANONICAL_RELATIONSHIP_REGISTRY.csv`: entity catalog + closed ArchiMate-grounded relationship taxonomy + valid-(source,rel,target) triples) — govern the model, let links accumulate against it, migrate later | medium | low | the metamodel SSOT exists + is enforced; nothing re-wired yet; **my recommendation as step 1** |
| **C** | B + **unify the Neo4j edges** to the taxonomy (collapse the 3 forked `*_PARENT_OF` → composition; rename edges to ArchiMate set) + derivation queries | larger | medium | the live graph speaks the metamodel; cross-layer queries work |
| **D** | C + **map every CSV FK column + every canonical type to its ArchiMate element/relationship** repo-wide (full metamodel adoption) | initiative-sized | medium-high | complete articulation; every link typed + governed; the definitive answer |
| **E** | Adopt **ArchiMate-as-canon** explicitly + publish HCAM as a People/Tech meta-canonical that all areas inherit (like AREA_GOVERNANCE), with the registry + Neo4j + a cursor rule + skill | initiative-sized | medium | the model becomes governed doctrine any seat/AIC inherits; pairs with the area model |

**My recommendation (MADEIRA): B → C → E, staged.** Mint the relationship registry + entity
catalog + valid-triple rules **now** (B — the governing SSOT, low risk, immediately answers
"what can link to what"); unify the forked graph edges next (C); then publish HCAM as inherited
doctrine + wire the rule/skill (E). This mirrors how the area model worked — *define the model,
let things accumulate against it, migrate incrementally* — and it's an initiative in its own
right (proposed **I95 — Canonical Articulation Model**, sibling to I94).

## 7. How this lands the operator's other answers

- **Q2 (Lead naming):** roles are ArchiMate *business roles*; "Lead" is a seniority layer
  (composition under the area role), not a separate type — so simplifying "Lead" (except Data
  Governance Lead, kept for disambiguation) is consistent with HCAM. Prepared as a gated
  `baseline_organisation` tranche.
- **Q3 (ghost folders):** Growth/Social/Storytelling are deprecated *sub-area* nodes — merge
  their content into the surviving sub-areas (composition re-parent) + delete empties.
- **Q4 (Research tree):** Research's technique folders are *components/methods* (the "what"),
  the analyst roles are the "who" — HCAM says they link by **assignment** (analyst performs
  technique). Deferred to I75 but with the model to guide it (no infinite deferral — the
  relationship is now nameable).

## 8. Cross-references

- Subject: `akos/hlk_graph_model.py` (the live projection — 10 labels / 13 edges) + the CSV registries
- External grounding: ArchiMate 3.1 (opengroup.org) · property-graph modeling (neo4j.com) · Zachman (zachman-feac.com)
- Sibling initiatives that grew the graph organically: I23 (Program), I25 (Topic), I32 (6 axes), I7 (Neo4j projection)
- Pairs with: I94 area model (AREA-14 kind/entity + AREA-15 placement are HCAM relationships) + `D-ARTIC`
