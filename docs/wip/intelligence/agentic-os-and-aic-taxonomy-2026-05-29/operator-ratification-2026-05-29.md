---
title: Operator ratification — agentic-entity taxonomy decision questions (2026-05-29)
language: en
intellectual_kind: wip_intelligence_synthesis
sharing_label: internal_only
audience: J-OP
authored: 2026-05-29
last_review: 2026-05-29
status: ratified
linked_research_sources:
  - docs/wip/intelligence/agentic-os-and-aic-taxonomy-2026-05-29/source-ledger.csv
linked_canonicals:
  - docs/references/hlk/v3.0/Research/Methodology/canonicals/RESEARCH_ACTION_DISCIPLINE.md
  - docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_AGENTIC_DOCTRINE.md
  - docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/AIC_REGISTRY.csv
---

# Operator ratification — DQ-TAX-01..05

> Verbatim operator verdicts distilled into a durable record for the
> agentic-entity taxonomy research. Ratified 2026-05-29 in-session via inline
> AskQuestion gate. Mirrors the shape of the model-selection ratification doc
> ([`operator-ratification-2026-05-28.md`](../model-selection-2026-05-28/operator-ratification-2026-05-28.md)).
> Tier-1 WIP: these verdicts govern the WIP synthesis now; formal
> DECISION_REGISTER rows + canonical promotion land at the gated
> entity-registry tranche (see DQ-TAX-05 + "Next gate" below).

## Summary table

| ID | Question (short) | Verdict |
|:---|:---|:---|
| **DQ-TAX-01** | Accept the concept/instance lines (manifesto vs product vs running AIC vs substrate vs non-AIC workers) | **Accept** |
| **DQ-TAX-02** | Add capability-tier axis (chatbot → workflow → agent → autonomous) as first-class | **Accept** |
| **DQ-TAX-03** | Lock AKOS identity = KB-first / coordination-layer AOS; defer the bare "AOS" brand label | **Accept** |
| **DQ-TAX-04** | Home model-seat routing as an advisory rule (no new/changed canonical CSV) | **Accept (advisory-only)** |
| **DQ-TAX-05** | Defer the wider non-AIC entity modelling + registry expansion | **OVERRIDDEN → include now**; shape ratified 2026-05-29 → Option 1 (new dedicated registry) + demonstrator seed |

---

## DQ-TAX-01 — Accept the clear lines (ratified)

The taxonomy's concept/instance separation is accepted as the foundation:
MADEIRA-the-manifesto (the role/position an agent holds) vs MADEIRA-the-product
vs a specific running AIC (e.g. Madeira-on-Cursor) vs the substrate it runs on
vs non-AIC workers (RPA, serverless, Agent-as-a-Service, harness-as-a-service,
text-only). Full lines: [`master-synthesis.md`](master-synthesis.md) §1.

## DQ-TAX-02 — Capability-tier axis is first-class (ratified)

The taxonomy keys on three axes, not two: **made-of** (substrate) ×
**intent** (role-class + task-class) × **capability-tier** (chatbot → workflow
→ agent → autonomous). Grounded in the field finding that most 2026 products
called "agents" are actually workflows ([`master-synthesis.md`](master-synthesis.md)
§1, SRC-TAX-02). This axis becomes a column wherever entities are registered.

## DQ-TAX-03 — AKOS identity locked; AOS brand label deferred (ratified)

- **Internal register (accurate):** AKOS is a *KB-first / coordination-layer
  agentic operating system with governance + graded provenance on every
  action* — it passes the field's weakest test (governance + audit) and does
  not claim the kernel-OS test it would fail (resource arbitration). Earned-label
  verdict: [`master-synthesis.md`](master-synthesis.md) §3.
- **External register:** do **not** lead with the bare "agentic operating
  system / AOS" label — the field calls it "agent-washing"; the term is diluted.
  The branding decision is a separate research: [`aos-branding-forward-charter.md`](aos-branding-forward-charter.md).

## DQ-TAX-04 — Model-seat routing ships advisory-only (ratified)

Model-seat routing (thinking vs execution model per task) is a **different
axis** from the existing per-task registry (which governs which AIC, what
tools, what permission). It ships as an **advisory Cursor rule**
(`akos-aic-delegation.mdc`) + the routing-map Layer 0 — **no new or changed
canonical CSV**. This is the lightest path and sidesteps the existing-registry
collision the Composer-plan regression surfaced. The existing
`MADEIRA_AIC_PER_TASK_REGISTRY.csv` (minted at the AIC-registry work, decision
`D-IH-82-S`) is left untouched.

## DQ-TAX-05 — Wider entity modelling: INCLUDE NOW (operator override)

**Recommended default was "defer"; operator overrode to "include now."** The
wider field (third-party AICs, RPA bots, serverless workers, Agent-as-a-Service,
harness-as-a-service, text-only) + the registry expansion are **in scope for
this rollout**, not a later tranche.

This is a **canonical-CSV mint** and therefore carries a **hard operator gate**
plus the full governance bundle (Pydantic model + validator + PRECEDENCE row +
mirror DDL + DECISION_REGISTER row + synthesis-before-tranche sweep). Before any
canonical row is written, one **structural shape** must be ratified — see below.

### Shape gate — RATIFIED 2026-05-29 (Option 1 + demonstrator seed)

How should the wider entities be modelled? Three structural options were
surfaced as a follow-up inline AskQuestion (kept here for the audit trail):

1. **New `AGENTIC_ENTITY_REGISTRY.csv`** for non-AIC + external entities, with
   `capability_tier` baked in (keeps the AIC registry pure — AICs hold named
   roles; RPA/serverless do not). ← **RATIFIED**
2. **Extend the existing `AIC_REGISTRY.csv`** with `entity_class` +
   `capability_tier` columns so one table holds both (touches the locked AIC
   schema + the schema-drift contract + the downstream capability-matrix FK).
3. **Both:** `capability_tier` column on AIC_REGISTRY for Holistika's own AICs,
   PLUS a new sibling registry for the external/non-AIC field.

**Operator verdict (2026-05-29):** **Option 1** + **demonstrator seed** — a new
dedicated registry; the existing AIC table stays the "agents holding named
roles" SSOT; the new table models the wider field. This clears the only gate
blocking the build. The mechanical activation bundle (new CSV + Pydantic model +
validator + PRECEDENCE row + mirror + DECISION_REGISTER row + sweeps) is now the
execution seat's job — build spec lives in
[`entity-registry-proposal-2026-05-29.md`](entity-registry-proposal-2026-05-29.md)
§"Governance bundle"; it runs the validators + sweeps as it lands. Nothing is
canonical until that build commits.

---

## Cross-references

- Taxonomy synthesis: [`master-synthesis.md`](master-synthesis.md) (32-source ledger).
- Research-action pack: [`research-action-pack.md`](research-action-pack.md).
- Branding deferral: [`aos-branding-forward-charter.md`](aos-branding-forward-charter.md).
- Sibling ratification (model selection): [`../model-selection-2026-05-28/operator-ratification-2026-05-28.md`](../model-selection-2026-05-28/operator-ratification-2026-05-28.md).
- Rollout plan: `~/.cursor/plans/aic_delegation_rollout_12e67d1a.plan.md`.
