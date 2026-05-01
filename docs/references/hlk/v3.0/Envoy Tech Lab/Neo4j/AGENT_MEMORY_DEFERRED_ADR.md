---
language: en
status: active
intellectual_kind: architecture_decision_record
role_owner: System Owner
area: Tech / Envoy Tech Lab / Neo4j
entity: Holistika Research
authority: Founder + System Owner
last_review: 2026-05-01
artifact_role: canonical_doctrine
topic_ids:
  - topic_holistik_ops_discovery
parent_topic: topic_holistik_ops_discovery
---

# ADR-46-A — Agent / user memory KG: deferred

> **Status:** ACCEPTED (2026-05-01).
> **Decision:** AKOS will NOT build agent / user memory KG (use-case C from [`NEO4J_STRATEGY.md`](NEO4J_STRATEGY.md)) in Initiative 46. Build is deferred until one of three named trigger conditions fires.
> **Decision-makers:** System Owner (Founder ratification 2026-05-01).
> **Re-eval cadence:** Triggered (not time-based). When trigger fires, a new initiative (I47+) opens.

## Context

The [`NEO4J_STRATEGY.md`](NEO4J_STRATEGY.md) doctrine separates Neo4j use into three independent use-cases:

- **A. Governance KG** — built and live (I7 → I32)
- **B. GraphRAG over the HLK vault** — PoC in I46 P3, conditional ship in I46 P5
- **C. Agent / user memory KG** — temporal facts about user preferences, past sessions, conversation history, tenant-scoped memory

This ADR is about **use-case C**.

The 2026 field has converged on the Zep / Mem0 / Cognee / Letta architectural pattern — temporal knowledge graphs with first-class time dimensions, capable of answering "what did we tell user X 6 weeks ago" and "your billing plan changed January 15". Per **AgentMarketCap "Agent Memory at Scale 2026"**:

| Provider | Architecture | LongMemEval | License |
|:---------|:-------------|:-----------:|:--------|
| Mem0 | Dual-store (vector + KG, gated $249/mo) | 49.0% | OSS / commercial |
| Zep / Graphiti | Temporal KG (time-first) | **63.8%** | OSS / commercial |
| Cognee | Ingest pipeline + KG (multimodal) | not published | OSS |
| Letta | Virtual-memory paging | n/a | OSS |

Per the **Tianpan.co 2026 piece**: *Neo4j Graphiti is explicitly NOT for document retrieval — it is for agent memory*. Conflating use-case B with use-case C routes us to the wrong tool.

## Why we're not building it now

Three negatives, all current:

1. **Use-case absent**. AKOS today is single-operator. There is no multi-tenant load. There is no recurring "what did we tell user X 6 weeks ago" ask. Building memory before the use case exists creates a half-built system that costs maintenance with no return.

2. **No conversational depth signal**. Madeira sessions today are bounded — each interaction is a single skill (lookup / plan / verify) with little cross-session state. The MADEIRA UAT (D-IH-32-Q9) confirmed in-process probes complete in ~750ms with no need for prior-session context.

3. **Buying when the trigger fires is cheaper than building before it does**. Zep at scale costs ~$X/tenant/month; building an in-house equivalent that matches Zep's 63.8% LongMemEval is a multi-week effort with ongoing maintenance.

## Trigger conditions

The build is reopened when **any one** of these conditions fires:

### Trigger 1 — Multi-tenant load (operator default; selected 2026-05-01)

**When:** Initiative 34 (multi-tenant productisation; opens MADEIRA-SaaS) closes successfully.

**Signal:** `SKILL_REGISTRY.csv` carries skill rows with `tenant_scope != 'shared'`. The first tenant-scoped skill triggers re-eval.

**Why this is the default:** Most concrete signal. Most-aligned with the existing roadmap (I34 is the next planned multi-tenant initiative). Longest deferral horizon (gives I46 closure room before reopening).

### Trigger 2 — Conversation depth

**When:** A Madeira session crosses N skills in 1 conversation, where N is operator-set (default proposal: N=4).

**Signal:** `compliance.eval_run` (I45 P4) shows >=10% of MADEIRA traces in a 7-day window with `skills_invoked_count >= 4`.

**Why this could trigger first:** If MADEIRA usage patterns evolve toward multi-skill conversations (e.g., "find the role then plan a migration then verify"), session-level memory becomes valuable.

### Trigger 3 — Compliance ask

**When:** A Holistika legal / compliance request lands asking "what did we tell user X N weeks ago" or equivalent retrospective audit query.

**Signal:** Operator forwards an external ask via the Adviser Engagement plane (I21).

**Why this is the highest-urgency trigger:** A compliance ask is non-deferrable. If this fires, build immediately.

## When trigger fires: evaluation framework for the new initiative (I47+)

The reopening initiative will evaluate, in this order:

### Step 1 — Decide buy vs build

| Path | When |
|:-----|:-----|
| **Buy Zep / Graphiti** (managed) | Default if trigger 1 or trigger 3 fires. Faster to ship; benchmarked best (63.8%). Ongoing $X/mo; predictable. |
| **Buy Mem0** (managed; gated graph) | If we want a gentler price point and accept the 49% benchmark. |
| **Build minimal in-house Neo4j temporal layer** | Only if (a) a buy-side option fails our cost ceiling AND (b) trigger gives ≥6 weeks lead time AND (c) we have engineering bandwidth. |

### Step 2 — Schema (whether buy or build)

The temporal KG schema will carry, at minimum:
- `:User` node (or `:Tenant` for multi-tenant) with stable id
- `:Fact` node with `valid_from` + `valid_to` + `superseded_by` columns
- `:Session` node with start_at + end_at + skill_invocations
- `(:User)-[:HOLDS_FACT {recorded_at}]->(:Fact)` edge
- `(:Session)-[:UNDER_USER]->(:User)` edge
- `(:Session)-[:INVOKED]->(:Skill)` edge — links to existing governance KG

The schema sits in a NEW Neo4j database (separate from the governance KG per D-IH-32-M-style discipline). Cross-merging governance + memory entangles two cost lines and two RLS regimes.

### Step 3 — Privacy + retention

The new initiative MUST resolve before any build:
- PII scope (which user fields are stored vs hashed vs not stored)
- Retention windows (per-fact `expires_at`)
- Right-to-erasure mechanism (cascade delete by user_id)
- Cross-tenant isolation (RLS / schema-level / instance-level)

These are addressed via new POLICY_REGISTER rows (`policy_class=pii_scope` already exists) and a new SOP under `Admin/O5-1/People/Compliance/`.

### Step 4 — Eval

The new initiative MUST also bring its own eval suite:
- LongMemEval-style benchmark (or our adapted version)
- Cassettes via I45 P2 mechanism
- Promotion gate via I45 P7 mechanism (extended for `tenant_scope` validation)

## Sunset clause

If 12 months pass post-this-ADR without any trigger firing, the ADR is reviewed (not auto-revived). Possible outcomes at review:
- Status quo (defer continues)
- Trigger conditions revised (e.g., tighten signal thresholds)
- Adopt anyway (operator decision)

## Cross-references

- [`NEO4J_STRATEGY.md`](NEO4J_STRATEGY.md) — the doctrine that separates the 3 use-cases
- D-IH-46-B in [`docs/wip/planning/46-neo4j-strategic-posture/decision-log.md`](../../../../wip/planning/46-neo4j-strategic-posture/decision-log.md) — the operator ratification of the defer-with-trigger position
- D-IH-32-M — KiRBe Neo4j separation (the structural precedent for "do not cross-merge graph stores"; same discipline applies to a future memory KG)
- Initiative 34 (future) — multi-tenant productisation; carries trigger 1
- Initiative 21 (closed) — Adviser Engagement plane; carries the trigger 3 channel
- 2026 sources cited:
  - Tianpan.co "GraphRAG in production 2026" (Neo4j Graphiti = agent memory, NOT document retrieval)
  - AgentMarketCap "Agent Memory at Scale 2026" (Mem0 vs Zep vs Cognee vs Letta benchmarks)

## Sign-off

- **Author:** AKOS Architect, 2026-05-01
- **Approved by:** System Owner (default trigger choice = Trigger 1 — Multi-tenant load via I34)
- **Operator change of trigger choice:** edit decision-log entry with new D-IH-46-Decision-P4-MEMORY-TRIGGER and update this ADR's "operator default" reference
