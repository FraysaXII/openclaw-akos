---
intellectual_kind: research_prong
prong: C
topic_cluster: external_domain_boundaries
authored: 2026-06-05
status: active
language: en
---

# Prong C — How industry defines what a "domain / area" actually is

> External research-sweep (`SRC-AREA-EXT-24..46`). Answers `def-area`: is "folder + roles +
> processes" the right unit, or is there a sharper, load-bearing boundary criterion?

## C.1 The boundary is about *meaning*, not folders (DDD)

DDD's **Bounded Context** (`SRC-AREA-EXT-24`, `SRC-AREA-EXT-26`) defines a domain boundary as
"the largest scope within which a model remains internally consistent" — an
**understandability/linguistic boundary** (`SRC-AREA-EXT-27`, `SRC-AREA-EXT-28`), *not* a
code or folder boundary. The load-bearing insight: total unification across a large system
"is not feasible"; you divide into contexts, each internally consistent, with **explicit
translation (anti-corruption layer)** at the seams.

**Applied to us:** our F-TOPO-1 finding — Tech split across `Tech/` + `Envoy Tech Lab/` —
is precisely a *single area with two unreconciled models*. DDD says either draw one boundary
(one consistent model) or make the seam explicit. The 14-component bar can't see this because
it has no boundary criterion. **This is the strongest external case that `def-area` needs a
criterion beyond "a folder exists."**

## C.2 The boundary should align to a *stream of value* and *cognitive load* (Team Topologies)

Team Topologies (`SRC-AREA-EXT-29..32`) defines the primary unit as a **stream-aligned team**
owning "a slice of the business domain end-to-end," sized by **cognitive load** — when a
boundary holds too much, you split or offload to platform/enabling/complicated-subsystem
teams. Boundaries are **explicitly flexible** and renegotiated as the system evolves.

**Applied to us:** our areas map cleanly to stream-aligned ownership (Finance owns FINOPS
end-to-end). The "cognitive load" test offers a **boundary heuristic we lack**: if an area's
surface exceeds what its role-owner can govern at depth, that is the signal to split a
sub-area into its own area (Brand-out-of-Marketing; Envoy-Tech-Lab-out-of-Tech). It also
names two *support* shapes — **platform** and **enabling** — that match People (the
discipline-of-disciplines / enabling) and Tech (the substrate/platform), suggesting not all
seven areas are the *same kind* of area.

## C.3 Treat each domain as an owned *product* with contracts (Data Mesh)

Data Mesh (`SRC-AREA-EXT-33..36`) gives four principles: **domain ownership**, **data as a
product**, **self-serve platform**, **federated computational governance**. The 2026 field
read (`SRC-AREA-EXT-36`) is blunt: domain ownership fails as "lip service" without **robust
versioned contracts + quality SLOs + clear ownership**; "data as a product = value not
perfection."

**Applied to us:** we already have `DATA_CONTRACT_REGISTRY` (`SRC-AREA-INT-19`) and federated
governance (People mints patterns, areas self-own). The missing principle is **data/area as a
product with an owner + a contract + an SLO** — i.e. an area is "complete" when it ships a
*consumable product with a contract*, not when it has the right folders. Feeds `def-complete`.

## C.4 Areas evolve; not all are at the same stage (Wardley) and platforms pave golden paths

- **Wardley** (`SRC-AREA-EXT-41..43`): components sit on a value chain and **evolve**
  genesis → custom → product → commodity; you manage them *differently* by stage. Supports
  the idea that Finance (newly built, "custom") and People (mature, "product/commodity")
  warrant **different governance density** — a per-area *tier*, not a flat bar.
- **Capability models / TOGAF** (`SRC-AREA-EXT-37..40`): a capability = "what not how" =
  people + process + information + technology, visualized via **heat maps colored by
  maturity / strategic-importance / risk**. This is *exactly* a weighted, leveled area
  matrix — and it is the mainstream EA way to show "how complete/strong is each area."
- **Golden paths / platform engineering** (`SRC-AREA-EXT-44..46`): Spotify's "opinionated,
  supported path" with **blessed tools** and a **Golden State** (knowing if you're on the
  path) is the direct analogue of `pattern_area_buildout` + the matrix. Validates our
  approach and suggests the bar is a "Golden State" tracker — *and that a path needs a
  clearly-defined audience and one primary focus*, which our flat bar lacks.

## C.5 What Prong C establishes for the decision

- `def-area`: an area is best defined as a **bounded context (consistent model) aligned to a
  value stream, sized by cognitive load, owned end-to-end, exposing a contract** — far richer
  than "a folder." Gives us a real **boundary criterion** (consistency + stream + load + owner
  + contract) to resolve F-TOPO-1 and future splits.
- `def-complete`: "area as a product" → complete = *ships a contracted, owned, consumable
  capability*, not *has the artifacts*. Outcome axis confirmed missing.
- `def-threshold`: Wardley evolution + capability heat-maps → **per-area tier/level** is the
  mainstream shape, not a flat global %.
