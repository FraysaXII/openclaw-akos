---
language: en
status: active
intellectual_kind: phase_evidence
role_owner: System Owner
area: Tech / Holistik Ops
entity: Holistika Research
authority: Founder + System Owner
last_review: 2026-05-01
artifact_role: governed_evidence
topic_ids:
  - topic_holistik_ops_discovery
parent_topic: topic_holistik_ops_discovery
---

# I46 P0 — Audit of the current Neo4j surface

**Audit id:** AUDIT-NEO4J-SURFACE-2026-05-01
**Closes:** I46 P0 entry criteria; feeds evidence-matrix rows E1-E12.
**Method:** Read-only walk of `akos/hlk_neo4j.py`, `scripts/sync_hlk_neo4j.py`, `scripts/hlk_graph_mcp_server.py`, `scripts/hlk_graph_explorer.py`, `akos/api.py` graph endpoints, `prompts/overlays/OVERLAY_HLK_GRAPH.md`, `agent-capabilities.json`, plus subagent inventory commissioned during planning.

## TL;DR

Neo4j is **NOT write-only**. We have:
- 4 read endpoints in the FastAPI surface
- 3 MCP tools
- 1 Streamlit explorer
- 1 prompt overlay
- 1 live test class (`@pytest.mark.neo4j`)
- 0 doctrine pages explaining what it is FOR

The investment is real; the doctrine is missing.

## Inventory

### Write side (the projection)

| Component | File | What it does |
|:----------|:-----|:-------------|
| Sync script | `scripts/sync_hlk_neo4j.py` | Full rebuild: 65 roles + 1093 processes + 12 programs + 27 topics + 6 axis-6 dimensions = ~2330 edges |
| Graph model | `akos/hlk_graph_model.py` | Type definitions: `GraphLabel` (node labels), `EdgeType` (edge types), build functions per axis |
| Driver helper | `akos/hlk_neo4j.py` `get_neo4j_driver()` | TLS modes: system / all (rewrites `+s` → `+ssc`) / custom (CA bundle) — D-IH-32-Q hard-won |
| Constraints + indexes | `akos/hlk_neo4j.py` `_ensure_constraints()` | Unique constraints on `Role.role_name`, `Process.item_id`, `Program.program_id`, `Topic.topic_id`; range indexes on lifecycle/code/plane/class |
| Idempotency | proven D-IH-32-Q (2026-05-01) | 2 consecutive `sync` runs → identical output |

### Read side — FastAPI endpoints

| Endpoint | File | Cypher source | Auth |
|:---------|:-----|:--------------|:-----|
| `GET /hlk/graph/summary` | `akos/api.py` ~840-870 | `graph_summary()` in `hlk_neo4j.py:472-488` (`MATCH (n) RETURN labels(n)[0]…`) | Depends on AKOS_API_KEY |
| `GET /hlk/graph/process/{item_id}/neighbourhood` | `akos/api.py` ~873-892 | `process_neighbourhood()` in `hlk_neo4j.py:491-651` (root + bounded optional matches) | Depends on AKOS_API_KEY |
| `GET /hlk/graph/role/{role_name}/neighbourhood` | `akos/api.py` ~895-941 | `role_neighbourhood()` in `hlk_neo4j.py:671-737` | Depends on AKOS_API_KEY |
| `GET /hlk/graph/explorer` | `akos/api.py` ~829-837 | static HTML shell (no Bolt) | Depends on AKOS_API_KEY |

### Read side — MCP tools

| Tool | File | Source | Wire-up |
|:-----|:-----|:-------|:--------|
| `hlk_graph_summary` | `scripts/hlk_graph_mcp_server.py:51-74` | `graph_summary()` | `config/mcporter.json.example:98-104` |
| `hlk_graph_process_neighbourhood` | same file 77-91 | `process_neighbourhood()` | same |
| `hlk_graph_role_neighbourhood` | same file 94-108 | `role_neighbourhood()` | same |

The 6 axis-6 dimensions added in I32 P5/P6 (Skill, TouchpointKitCell, Policy, GoiPoi, Channel, Sourcing — 6 new node labels) are **projected to Neo4j but have no MCP tool surface**. Agents see them via the CSV vault (`hlk_search`), not via graph traversal. **This is gap E3 in the evidence matrix.**

### Read side — Streamlit explorer

| Component | File | Notes |
|:----------|:-----|:------|
| Streamlit app | `scripts/hlk_graph_explorer.py` | Calls control-plane `/hlk/graph/summary` + `/hlk/graph/.../neighbourhood` via httpx (`_api_get` lines 221, 1701) |
| Routing | `akos/graph_stack.py` ~179-323 | Supervises mirror sync (writes via subprocess `sync_hlk_neo4j.py`); fingerprint/health |

### Test surface

| Test class | File | Marker | What it exercises |
|:-----------|:-----|:-------|:------------------|
| Graph stack live | `tests/test_graph_stack.py` ~34-65 | `@pytest.mark.neo4j` | `verify_connectivity()` when `NEO4J_*` set; otherwise skipped |
| API graph endpoints | `tests/test_api.py` ~206-234 | none | Graph summary JSON without Bolt; neighbourhood endpoints `503` when Neo4j unconfigured; explorer HTML smoke |
| Browser smoke | `scripts/browser-smoke.py` ~130-148, ~667-730 | optional `--playwright` | Hits `/hlk/graph/summary` |
| Holistik Ops 6-axis projection | `tests/test_holistik_ops_axis_graph.py` (I32 P5) | none | `sync_hlk_neo4j.py` dry-run output assertions |

### Prompt surface

| File | Role |
|:-----|:-----|
| `prompts/overlays/OVERLAY_HLK_GRAPH.md` (lines 1-19) | Optional Neo4j mirror tools; names `hlk_graph_summary`, `hlk_graph_process_neighbourhood`, `hlk_graph_role_neighbourhood`. Explicitly stresses CSV SSOT over Neo4j. |
| `prompts/base/MADEIRA_BASE.md` (lines 108-137) | Tells Madeira **NOT** to cite `hlk_graph_*` as a source line. Does **NOT** list `hlk_graph_*` in the "Allowed Tools" bullet list. |
| `config/agent-capabilities.json` (lines 92-105) | `madeira` role lists `hlk_graph_summary`, `hlk_graph_process_neighbourhood`, `hlk_graph_role_neighbourhood`. So gateway COULD expose them when configured; prompt does not invite their use. |

### Cross-repo Neo4j state

| Repo | Has Neo4j? | Purpose | I32 stance |
|:-----|:-----------|:--------|:-----------|
| AKOS | Yes (Aura) | Governance KG (this initiative) | Authoritative |
| KiRBe | Yes (separate Aura) | Vault search (per `kirbe-sync-contract.md` §11 + I32 architecture audit) | D-IH-32-M: STAYS SEPARATE |
| hlk-erp | No | — | — |
| boilerplate | No | — | — |

D-IH-32-M is firm: do NOT cross-merge KiRBe's Neo4j with AKOS Neo4j. P1 doctrine restates this for permanence.

## Use-case classification (per cursor plan)

| Use-case | Definition | Status today | I46 P3+P4+P5 posture |
|:---------|:-----------|:-------------|:---------------------|
| **A. Governance KG** | CSV-to-Neo4j projection of governance dimensions (roles, processes, topics, personas, skills, etc.) | Built, idempotent, 4 read endpoints, 3 MCP tools | Keep + harden (P2 adds 1 MCP tool + drift canary) |
| **B. GraphRAG over the HLK vault** | LLM queries Neo4j to ground answers in graph context | Not built | PoC in P3, conditional ship in P5 |
| **C. Agent / user memory KG** | Temporal facts about user prefs / past sessions | Not built | Defer with trigger ADR in P4 |

## Findings

### F1 — Use-case A is sound but under-consumed

The projection works. The 4 read endpoints work. The 3 MCP tools work. **But MADEIRA does not consume them at routing time.** Per `MADEIRA_BASE.md`, the graph tools are:
- Not in the "Allowed Tools" list (so prompt-side Madeira does not invite use)
- Explicitly noted as "do NOT cite as source line" (citation requirement is CSV-rooted)

Result: we pay Aura cost + projection maintenance cost + ~2330 edges of MERGE work per sync, and capture zero MADEIRA value. **Gap E2.**

### F2 — Axis-6 dimensions have no MCP traversal surface

I32 P5/P6 added 6 new node labels and `:UNDER_TOPIC` edges. The 3 existing MCP tools cover only Process and Role neighbourhoods. **An agent cannot ask "show me all skills under topic X" via the graph today.** P2 adds `hlk_graph_skill_neighbourhood` as the first axis-6 traversal tool; future initiatives can extend.

### F3 — No drift canary between Neo4j and CSV

`sync_hlk_neo4j.py` runs only on `release-gate` (per release) or operator-manual invocation. Between syncs, CSV edits land but Neo4j is stale. Nobody alerts. **Gap E11.**

P2 adds a nightly `scripts/graphrag_drift_canary.py` that compares Neo4j node counts to CSV row counts; fails on >1 row deviation.

### F4 — `OVERLAY_HLK_GRAPH.md` is the only place that mentions Neo4j use-case at all

The overlay is a prompt fragment, not doctrine. It's loaded conditionally (per model-tier, per agent). It explicitly says "CSV SSOT over Neo4j" but does not explain WHEN graph traversal would be appropriate vs CSV lookup. **Gap E1.**

P1 doctrine fills this: 3 use-case framing, decision-frame for new graph features, cost/performance envelope.

### F5 — KiRBe local Neo4j separation is implicit

D-IH-32-M states "KiRBe's local Neo4j stays separate from AKOS Neo4j". This is documented in the I32 decision log but not in any vault doctrine page. KiRBe's `kirbe-sync-contract.md` §11 mentions cross-repo discipline but does not call out Neo4j separation specifically.

P1 doctrine restates this as a permanent doctrine rule (cross-referenced from `kirbe-sync-contract.md` §11 update).

### F6 — `hlk_graph_*` tools live in `agent-capabilities.json` but not in `MADEIRA_BASE.md` "Allowed Tools" list

This is a deliberate prompt-level reticence (Madeira should default to CSV; graph is gateway-allowed but not prompt-suggested). The asymmetry is correct for current Madeira posture but creates a knob the operator should know about explicitly.

P1 doctrine documents this asymmetry (gateway-allowed vs prompt-invited).

### F7 — `tests/test_graph_stack.py` is the only place we test Neo4j connectivity end-to-end

`@pytest.mark.neo4j` marker → opt-in (not in default pytest run unless env vars set). After D-IH-32-Q (auth fixed 2026-05-01), this should be added to the recurring release-gate idempotency check (P2 deliverable).

### F8 — No agent memory work today (use-case C)

Zero code, zero schema, zero prompts mention Zep/Mem0/Cognee/Letta. Use-case C is uncharted; P4 ADR codifies the deferral with explicit trigger.

## Risks not yet on register

- **R-AUDIT-N1** — `prompts/overlays/OVERLAY_HLK_GRAPH.md` is the de-facto doctrine because nothing else exists. When P1 ships `NEO4J_STRATEGY.md`, the overlay becomes redundant on framing (kept for prompt-side tool listing). Cross-reference must be added in P1. **(Already in P1 plan; track here.)**
- **R-AUDIT-N2** — D-IH-32-M (KiRBe Neo4j separation) is currently only in I32 decision-log; if I32 docs ever get retired, the doctrine is lost. P1 doctrine inheritance prevents this. **(Already in P1 plan.)**
- **R-AUDIT-N3** — `akos/api.py` graph endpoints depend on `AKOS_API_KEY`; in dev (no key), they return the SPA shell instead of JSON. Operator surprise factor. P1 doctrine notes this as a known deployment gotcha. **(Mention in P1.)**

## Closure assertion

I46 P0 audit complete. Evidence-matrix rows E1-E12 are sourced from this file. No code changes; observation-only.

## Pointers for downstream phases

- **P1 doctrine** must include: 3 use-case framing, scale envelope (~1000 process rows = small corpus per 2026 cost research), portability posture (CSV SSOT, Neo4j rebuildable), KiRBe separation restated, gateway-vs-prompt asymmetry note, deployment gotcha (`AKOS_API_KEY` SPA fallback).
- **P2** must add `hlk_graph_skill_neighbourhood`, drift canary, idempotency-recurring on release-gate, and update `agent-capabilities.json` for the new MCP tool.
- **P3 PoC** must respect the cost ceiling (R-46-1) and use Ollama-local for embeddings to minimise spend.
- **P4 ADR** must name 3 candidate triggers; operator picks one; ADR signed by System Owner.
- **P5 conditional ship** depends on I45 P3 router refactor having shipped (cross-initiative dependency).
- **P6 cassettes** depend on I45 P2 cassette infrastructure.
