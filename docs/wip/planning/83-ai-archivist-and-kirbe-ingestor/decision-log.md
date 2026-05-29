---
title: I83 AI Archivist + KiRBe ingestor — decision log
language: en
intellectual_kind: initiative_decision_log
sharing_label: internal_only
audience: J-OP;J-AIC
parent_initiative: INIT-OPENCLAW_AKOS-83
authored: 2026-05-29
last_review: 2026-05-29
status: active
---

# I83 — decision log

> Human-readable companion to the `D-IH-83-*` rows in
> [`DECISION_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv).
> Formalizes the master-roadmap §"Decisions preview (full set)". Authored at I86 Wave R+5 close to
> thicken the I83 governance kit (was master-roadmap-only — a KPI-ownership gap). I83 is **chartered
> but pre-substantive-execution**: P0 charter expansion + full-sweep inventory happen at I83's own
> first wave once CTO + System Owner schedule it.

## Ratified

### D-IH-83-A — I83 mega-charter scope
**Question.** Charter the KiRBe ingestor MVP + audience translation + Knowledge panel?
**Decision.** Yes. Ratified via the `D-IH-86-CC` Wave-O OVERRIDE (speculative-promotion debt
accepted; I83 promoted first of I83/I74/I75 because the cleanest substrate was ready via I84 P4
`D-IH-84-E` framework narrowing). **Owner.** CTO (Tech Lab Lead). **Reversibility.** Medium. **Status.** Active.

### D-IH-83-D — Native build vs Composio adoption
**Question.** Adopt Composio, or build natively?
**Decision.** **NATIVE BUILD** (Wave P Push 2, 2026-05-21) — refactor the existing KiRBe POC while
maintaining versioning; reject Composio. Rationale: the KiRBe POC already covers Composio's surface
area + more (multi-source ingestion + audience translation + classification-aware filtering);
adopting Composio would discard the operator's prior investment + the audit lineage. **Owner.** CTO.
**Reversibility.** Medium. **Status.** Active.

### D-IH-83-F — Full-sweep scope expansion umbrella
**Question.** Is I83 KiRBe-only, or the umbrella for the broader tech-stack governance sweep?
**Decision.** Full-sweep (Wave P Push 2, 2026-05-21) — I83 P0 absorbs governance of Cloudflare +
Sentry + Langfuse + component-registry backfill + a custom Excalidraw MCP craft + v2.7 MADEIRA
architecture extraction + Output-1 blueprint sweep + Highway AI sub-deliverable + multi-tenant
customer-vault forward-charter + MCP inventory. Per-area applicability codified ("not only for
KiRBe — for everything"). Scope ceiling reset to 13–17d; P0 ≤ 5d hard cap with fork-to-dedicated-
initiative if a sub-sweep overruns (per `akos-conflict-surfacing-and-blocker-trackers.mdc`).
**Owner.** Founder + CTO + System Owner. **Reversibility.** Medium. **Status.** Active.

## Proposed (open gates; close at the named phase)

### D-IH-83-B — Tech Lab framework choice
LlamaIndex / LangGraph / composition of both (per `D-IH-84-E` E1, narrowed to 2 finalists).
**Status.** Proposed. Close-out: P1 (deferred from P0 per `D-IH-83-F` — needs existing KiRBe
codebase + Supabase table review first). **Owner.** CTO + System Owner.

### D-IH-83-C — Schema home
`holistika_ops.kirbe_*` vs a new `kirbe.*` schema. **Status.** Proposed. Close-out: P1.
**Owner.** System Owner. Canonical-CSV gate at P2 DDL apply (Supabase two-plane).

### D-IH-83-E — Read-only MVP vs read-write
Read-only MVP, or read-write (forward-charter to I84 if read-write)? **Status.** Proposed.
Close-out: P1. **Owner.** System Owner.

### D-IH-83-G..L — Reserved for P0 inline-ratify
Per-MCP governance + per-component remediation priority + Excalidraw MCP feature set + v2.7
extraction targets + Highway AI architecture + customer-vault tenant model. **Status.**
Forward-charter from `D-IH-83-F`. Close-out: P0. **Owner.** CTO + System Owner.
(`D-IH-83-G` already partly consumed at Wave Q close: `SUBS-HOLISTIKA-OBSIDIAN-READER` +
`SUBS-HOLISTIKA-KIRBE` substrate rows backfilled.)

## Cross-references

- Master-roadmap: [`master-roadmap.md`](master-roadmap.md). Risk register: [`risk-register.md`](risk-register.md). Files modified: [`files-modified.csv`](files-modified.csv).
- Candidate: [`i83-ai-archivist-and-kirbe-ingestor.md`](../_candidates/i83-ai-archivist-and-kirbe-ingestor.md).
- Rollout backlog (I83-side D2 + the C5 KiRBe-ingestor + C2 feed-delivery wiring): [`research-rollout-backlog-2026-05-29.md`](../86-initiative-cluster-execution-coordinator/research-rollout-backlog-2026-05-29.md).
- Promotion override: `D-IH-86-CC`. Framework narrowing: `D-IH-84-E`.
