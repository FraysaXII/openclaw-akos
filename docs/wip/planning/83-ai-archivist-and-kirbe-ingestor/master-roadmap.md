---
initiative_id: INIT-OPENCLAW_AKOS-83
title: I83 AI Archivist and KiRBe ingestor - knowledge-base surfacing system + full-stack governance sweep
status: active
authored: 2026-05-21
last_review: 2026-05-21
inception_decision_id: D-IH-83-A
owner_role: CTO
co_owner_role: System Owner
authority: Founder + CTO + System Owner
language: en
parent_dependency:
  - INIT-OPENCLAW_AKOS-82
  - INIT-OPENCLAW_AKOS-86
sibling_initiatives:
  - INIT-OPENCLAW_AKOS-76
  - INIT-OPENCLAW_AKOS-82
  - INIT-OPENCLAW_AKOS-89
linked_decisions:
  - D-IH-83-A
  - D-IH-83-D
  - D-IH-83-F
  - D-IH-86-CC
  - D-IH-86-CJ
  - D-IH-84-E
linked_canonicals:
  - docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/KNOWLEDGE_PAIRING_REGISTRY.csv
  - docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/canonicals/AGENTIC_FRAMEWORK_LANDSCAPE.md
authoritative_plan: docs/wip/planning/83-ai-archivist-and-kirbe-ingestor/master-roadmap.md
methodology_version_at_authoring: v3.1
program_anchors:
  - PRJ-HOL-INF-2026
---

# I83 — AI Archivist and KiRBe ingestor (knowledge-base surfacing system)

> **Status: active** (promoted 2026-05-21 under I86 Wave O via OVERRIDE `D-IH-86-CC`; speculative-promotion debt explicitly accepted). Inception ratified by `D-IH-83-A`. Charter scaffold per `as-far-as-possible-with-defaults` pace clause; full P0 charter expansion happens at this initiative's own first wave once Tech Lab Lead + System Owner schedule it.

## Lineage (why I83 promotes now under OVERRIDE)

The candidate file [`docs/wip/planning/_candidates/i83-ai-archivist-and-kirbe-ingestor.md`](../_candidates/i83-ai-archivist-and-kirbe-ingestor.md) names hard prerequisites (I82 P4 closed + Tech Lab framework ratified + concrete consumer surface available). Per `D-IH-86-CC` Wave O OVERRIDE, the operator chose **Option C: promote all three (I83/I74/I75) to full active charters now; accept speculative-promotion debt; let them execute in parallel with their actual gates**. Order: I83 first (cleanest substrate ready via Strand B — `D-IH-84-E` ratified E1 = LlamaIndex-continue + LangGraph-workflow at I84 P4 so framework choice C-83-1 narrows to 2 finalists).

## Operating story

> *"It's also good for other things we may build atop our system, like our AI Archivist and all-in-one ingestor (sort of like Composio, but with a wider scope), KiRBe."* — operator at I80 P7 inline-ratify Round 9 (2026-05-16).

I83 builds the **system** that operationalises the Capability Doctrine's use-case-archive facet (I82 P4) and the audience-aware capability surfacing capability (I82 doctrine itself). The People area minted the doctrine + the registries; the Tech area builds the ingestor + the surfacing API + the UI panels.

## Phase shape (proposed; ratified at P0)

| Phase | Purpose | Deliverable | Effort | Pause-point |
|:---|:---|:---|---:|:---|
| **P0** | Charter + architectural decisions + **full-sweep inventory** (per `D-IH-83-F`) | D-IH-83-A..L; OPS-83-1..6; existing-KiRBe-codebase inventory; v2.7 MADEIRA architecture extraction; Output 1 blueprint inventory; component-registry backfill (Sentry + Langfuse + others); Cloudflare/Sentry/Langfuse MCP-governed surfaces inventory | 3-5d | standard |
| **P1** | Registry-side spec (which registries KiRBe consumes; query API spec) + **brownfield extraction** (refactor + version existing KiRBe POC code per `D-IH-83-D`) | Spec doc; OpenAPI schema; brownfield-extraction plan with versioning; existing-Supabase-table catalogue | 2d | standard |
| **P2** | Ingestor MVP — **native refactor from existing KiRBe POC** | KiRBe service behind `holistika_ops` or `kirbe.*` schema (per D-IH-83-C P1 ratify); Tech Lab framework ratified per D-IH-83-B P1 ratify | 3-5d | **canonical-CSV gate** (Supabase DDL via migrations per `akos-holistika-operations.mdc`) |
| **P3** | Audience translation layer (BRAND_BASELINE_REALITY_MATRIX integration) | Translation API; per-audience rendering tests | 2d | standard |
| **P4** | hlk-erp Knowledge panel integration (consumer-side; first UI) | Panel route; UAT against capability surfacing event | 2d | standard |
| **P5** | **Highway AI** + multi-tenant customer-vault forward-charter to I84 expansion | Highway AI spec doc (MCP/API governed routing for AICs); customer-vault subscription model forward-charter; closure pause record; UAT report | 1d | closure-mega-ratify |

Total estimated effort: **13-17 days** post-charter-expansion (was 9-12d pre-expansion; full-sweep inventory at P0 + brownfield extraction at P1 add ~4d).

## Charter expansion (Wave P Push 2 amendment, 2026-05-21)

> **Source:** operator Wave P kickoff batch ratify gate response Q6 (2026-05-21). Operator framing: full sweep — "this is a full sweep" — KiRBe is the umbrella for Cloudflare + Sentry + Langfuse + components-backfill + Excalidraw blueprints + v2.7 MADEIRA architecture review + Output 1 blueprints + Highway AI + multi-tenant customer vaults + obsidian-reader registry. "It's not only for kirbe — for everything."
> **Ratifying decisions:** [`D-IH-83-D`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv) (native build refactored from existing KiRBe POC; maintain versioning) + [`D-IH-83-F`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv) (full-sweep scope expansion umbrella).
> **OPS rows:** OPS-83-1 through OPS-83-6 (Excalidraw MCP craft + v2.7 MADEIRA architecture extraction + COMPONENT_SERVICE_MATRIX Sentry/Langfuse backfill + Output 1 blueprint sweep + Highway AI sub-deliverable forward-charter + multi-tenant customer vaults forward-charter).

### Expansion scope (additive to the original P0..P5 phase shape)

**Brownfield reuse mandate (per `D-IH-83-D`).** KiRBe is **not greenfield**. The operator's existing KiRBe POC (multiple commits; substantial ingestor logic; demonstrated working ingestion flows; scalable architecture) is the **substrate** to refactor + version, not a reference to be discarded. P1 extracts the existing codebase + maps its capabilities against the I83 spec + produces a refactor-with-versioning plan that preserves operator trust in prior work. Composio adoption rejected: KiRBe already does what Composio does + more (per operator R-IH-83-2 commentary).

**Full-stack governance sweep (per `D-IH-83-F`).** I83 absorbs governance of the broader Holistika tech stack — not only KiRBe. Sub-deliverables:

| Surface | Discipline | I83 deliverable |
|:---|:---|:---|
| **Cloudflare** | Hosting + Domain + Storage + Codebase + Security (4 rows already in `COMPONENT_SERVICE_MATRIX.csv`) | P0 inventory of existing governance posture + MCP usage charter (cloudflare-docs + cloudflare-observability + cloudflare-builds + cloudflare-bindings MCPs available) |
| **Sentry** | Error monitoring + alerts + workflow integration (sentry MCP available; missing from `COMPONENT_SERVICE_MATRIX.csv`) | P0 backfill row(s) in `COMPONENT_SERVICE_MATRIX.csv`; SOP-TECH_SENTRY_GOVERNANCE_001 forward-charter |
| **Langfuse** | LLM observability + tracing + prompt management (langfuse + langfuse-docs MCPs available; missing from `COMPONENT_SERVICE_MATRIX.csv`) | P0 backfill row(s) in `COMPONENT_SERVICE_MATRIX.csv`; SOP-TECH_LANGFUSE_GOVERNANCE_001 forward-charter |
| **Excalidraw** | Blueprint/diagram authoring (operator has "tons of Excalidraw+ cloud blueprints for almost all areas"; MCP does NOT exist; operator-flagged "the only MCP I miss") | P0 forward-charter: **agent crafts a custom Excalidraw MCP server** so operator's existing blueprint corpus becomes navigable through MCP (paste keys when ready). Becomes the 21st MCP server in the workspace MCP inventory. |
| **v2.7 MADEIRA architecture** | Operator's prior architectural work on MADEIRA (AIC behaviour; sources KiRBe should manage; data governance posture) | P0 inventory + extraction of relevant content into either: (a) `docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/MADEIRA-AKOS/historical-AIC/` (already exists as folder) OR (b) v3.0 doctrine canonicals where appropriate (with versioning trail back to v2.7) |
| **Output 1 blueprints** | Operator's Excalidraw+ cloud blueprints across all areas (not only KiRBe) | P0 inventory + governance/versioning posture proposal. Output 1 is the People-area's Output-1 visual asset class per Initiative 25 P0 (`docs/references/hlk/v3.0/_assets/<plane>/<program_id>/<topic_id>/`) — blueprints map to existing topic_ids OR mint new ones |
| **Highway AI** | MCP/API governed routing for AICs (per operator R-IH-83-2 vision; sibling to MADEIRA orchestrator pattern) | **P5 sub-deliverable**: Highway AI spec doc as the per-task dispatcher governing which MCP/API/AIC handles which request. Forward-charters tighter integration with I76 P4 MADEIRA_AIC_PER_TASK_REGISTRY dispatcher pattern mint |
| **Multi-tenant customer vaults** | Customer vaults hosted at price/subscription per operator R-IH-83-2 vision | **P5 sub-deliverable**: forward-charter to I84 expansion (vault-as-a-service model + billing + RLS per-tenant + KNOWLEDGE_PAIRING_REGISTRY classification per-tenant). Not in I83 MVP scope. |
| **obsidian-reader (alpha experiment)** | Operator's alpha-stage Obsidian-vault reader experiment | **Already registered** at [`REPOSITORY_REGISTRY.csv`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/REPOSITORY_REGISTRY.csv) line 16 as `status: active`, kind `experiment`, owner `AI Engineer`, last reviewed by D-IH-86-AC at I86 Wave I. I83 P0 cross-references the experiment as one of the "research lineages that brought us closer to understanding AI as we do now" (operator R-IH-83-2 commentary). **Substrate row backfilled at Wave Q close** per `D-IH-83-G`: `SUBS-HOLISTIKA-OBSIDIAN-READER` (experimental / pilot / not multi-tenant) joins KiRBe-as-substrate `SUBS-HOLISTIKA-KIRBE` (active / in-production / library-import) in [`SUBSTRATE_REGISTRY.csv`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/SUBSTRATE_REGISTRY.csv) so I83 P0 inventory can FK-resolve via substrate_id. |
| **MCP inventory** | Existing MCP servers (20 currently catalogued at workspace root `mcps/`) | P0 inventory + governance posture (which MCPs are operator-private vs workspace-shared; which carry secret material; which need rotation cadence). Crafts the 21st MCP server (Excalidraw) per above. Operator-flagged: ask operator if any other MCPs are missing |
| **legacy dashboard of boilerplate** | Operator's drafts on legacy dashboard of `boilerplate` repo (mentioned R-IH-83-2 alongside obsidian-reader as a research lineage) | P0 inventory + extract relevant patterns/drafts into either v3.0 canonicals OR archive. Cross-reference from this charter. |
| **kirbe-frontend POC** | Existing POC frontend that "doesn't follow our brand or ops at all, just an old experiment more than a POC" (operator R-IH-83-2 commentary; operator open to scratching) | P0 inventory + decision whether to: (a) refactor under v3.0 brand+ops compliance, (b) archive as historical experiment, or (c) delete. Operator-eligible decision at P0 inline-ratify gate; default = archive (preserve audit trail) |

### Per-area applicability

> Per operator framing *"it's not only for kirbe — for everything"*: the governance shape this charter expansion codifies is **not KiRBe-specific**. The Cloudflare/Sentry/Langfuse/Excalidraw/v2.7-MADEIRA/Output-1-blueprints/Highway-AI/customer-vaults/MCP-inventory sweep applies across **every area** — Marketing's brand assets, Research's intelligence outputs, Operations' PMO blueprints, Legal's contract templates, People's doctrine canonicals — all of which may carry observability gaps + blueprint sprawl + MCP-governance posture questions. I83 P0's sweep deliverable produces a **per-area inventory matrix** so subsequent area-scoped initiatives can pick up the relevant remediation slice.

## Decisions preview (full set)

| ID | Question | Owner | Status entering | Close-out |
|:---|:---|:---|:---|:---|
| **D-IH-83-A** | I83 mega-charter scope — KiRBe ingestor MVP + audience translation + Knowledge panel | Tech Lab Lead | RATIFIED via D-IH-86-CC OVERRIDE | Wave O |
| **D-IH-83-B** | Tech Lab framework choice (LlamaIndex / LangGraph / composition of both per `D-IH-84-E` E1) | Tech Lab Lead + System Owner | Proposed (D-IH-84-E narrowed to 2 finalists) | P1 (deferred from P0 per D-IH-83-F: needs existing KiRBe codebase review + Supabase table review first) |
| **D-IH-83-C** | Schema home — `holistika_ops.kirbe_*` vs new `kirbe.*` schema | System Owner | Proposed | P1 (deferred from P0 per D-IH-83-F: needs existing Supabase table review first) |
| **D-IH-83-D** | Composio adoption vs native build (refactored from existing KiRBe POC) | Tech Lab Lead | **RATIFIED via Wave P Push 2 (2026-05-21): NATIVE BUILD** refactored from existing KiRBe POC; maintain versioning; reject Composio per operator R-IH-83-2 commentary (KiRBe POC already substantial + scalable + demonstrated working) | Wave P Push 2 |
| **D-IH-83-E** | Read-only MVP vs read-write (forward-charter to I84 if read-write) | System Owner | Proposed | P1 (deferred from P0 per D-IH-83-F: needs existing Supabase table review + capability scope review first) |
| **D-IH-83-F** | **NEW** — Full-sweep scope expansion umbrella (Cloudflare + Sentry + Langfuse + components-backfill + Excalidraw MCP craft + v2.7 MADEIRA architecture extraction + Output 1 blueprint sweep + Highway AI sub-deliverable + multi-tenant customer vaults forward-charter + obsidian-reader registry cross-reference + legacy boilerplate dashboard inventory + kirbe-frontend POC disposition) | Founder + CTO + System Owner | **RATIFIED via Wave P Push 2 (2026-05-21)**: full-sweep scope is binding for I83 P0; per-area applicability codified (not KiRBe-specific). Scope ceiling reset: 13-17d (was 9-12d). | Wave P Push 2 |
| **D-IH-83-G..L** | Reserved for P0 inline-ratify decisions emerging from the full-sweep inventory (per-MCP governance, per-component remediation priority, Excalidraw MCP feature set, v2.7 extraction targets, Highway AI architecture, customer-vault tenant model) | Tech Lab Lead + System Owner | Forward-charter from D-IH-83-F | P0 |

## Risks (top 6)

| ID | Risk | L | I | Mitigation |
|:---|:---|:---:|:---:|:---|
| **R-IH-83-1** | I82 not far enough along when I83 promotes — KiRBe has nothing to ingest | High | High | Hard prerequisite: **I82 P4** closed (use case archive minted) before I83 P0 enters substantive work |
| **R-IH-83-2** | Composio adoption costs vs native build costs | Low (was Medium) | Low (was High) | **Resolved by D-IH-83-D: NATIVE BUILD**. Existing KiRBe POC is substantial, working, and scalable per operator R-IH-83-2 commentary (2026-05-21). I83 refactors + versions the existing codebase rather than rewriting from scratch OR adopting Composio. Rejection rationale: KiRBe POC already covers Composio's surface area + more (multi-source ingestion + audience translation + classification-aware filtering); adopting Composio would lose the operator's prior investment + the audit lineage. |
| **R-IH-83-3** | RLS posture on kirbe.* schema unclear | Medium | High | Defaults: deny anon + authenticated; service_role only; classification-aware row filters per `KNOWLEDGE_PAIRING_REGISTRY.access_level` |
| **R-IH-83-4** | Audience translation hallucinates beyond canonical sources | Medium | High | Hard rule: KiRBe surfaces only registered rows; no LLM inference outside the registry-bounded answer space |
| **R-IH-83-5** | hlk-erp Knowledge panel not yet built — P4 has no UI consumer | Medium | Medium | Forward-charter; scope down to API-only MVP + defer UI to I85 |
| **R-IH-83-6** | **NEW** — Full-sweep scope creep blows past 13-17d ceiling (Cloudflare + Sentry + Langfuse + Excalidraw MCP craft + v2.7 MADEIRA extraction + Output 1 blueprints all compound at P0) | Medium | High | P0 sweep produces a **per-area inventory matrix** (not exhaustive remediation); each area-scoped follow-up initiative picks its remediation slice. P0 deliverable = inventory + governance posture + remediation roadmap; NOT full execution of all remediation. Hard cap: P0 ≤ 5d; any sub-sweep that exceeds budget forks to a dedicated initiative (I83-A / I83-B / ...). Per [`akos-conflict-surfacing-and-blocker-trackers.mdc`](../../../.cursor/rules/akos-conflict-surfacing-and-blocker-trackers.mdc) Option-5 default posture: surfacing > absorbing. |

### Operator R-IH-83-2 commentary — preserved verbatim (Wave P Push 2 audit-trail)

Per operator request "(rephrase my language please)", the original keyboard-broken text was reworded for clarity in the active R-IH-83-2 mitigation row above. The verbatim original is preserved here for audit-trail integrity:

> *"We have a huge work already done in KiRBe and it's fully or almost fully operational. It demonstrated it works before. It has all the ingestors you want and a scalable POC. Please refactor that while maintaining versioning. I've got also the alpha experiment called obsidian-reader (please add it to the registry because it was a huge research case that brought us closer to understanding AI as we do now, along with the drafts we made on legacy dashboard of boilerplate. Then there is the fact that KiRBe, AI Archivist, Highway AI for MCP/API governed routing for AICs, MADEIRA the all-orchestrator simple agent that behind is or [or others when commercialised] perfect all-rounder assistant that scales with [insert MADEIRA rework answer], any agent we want to craft for others no matter the framework, RPAs, or own research works or others works, customer vaults that we host for them at a price/subscription/etc, we need to work on KiRBe from all those prisms and more that I left out please)."* — operator R-IH-83-2 inline commentary (2026-05-21, rephrased above; verbatim here)

Cross-references:
- KiRBe + AI Archivist surface → I83 (this initiative).
- Highway AI sub-deliverable → I83 P5 (per D-IH-83-F charter expansion).
- MADEIRA orchestrator pattern → [I76 MADEIRA elevation](../76-madeira-elevation/master-roadmap.md).
- Any-agent-any-framework + RPA pattern → forward-charter to I84 expansion.
- Multi-tenant customer vaults at price/subscription → I83 P5 forward-charter to I84 expansion.
- obsidian-reader registry entry → already at [`REPOSITORY_REGISTRY.csv`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/REPOSITORY_REGISTRY.csv) line 16 since I86 Wave I (`D-IH-86-AC`).
- Legacy boilerplate dashboard drafts → I83 P0 inventory deliverable.

## Closure criteria

- Charter (P0..P5) ratified.
- KiRBe MVP read-only operational against `KNOWLEDGE_PAIRING_REGISTRY` + `CAPABILITY_REGISTRY` (after I82 P4 mint).
- Audience translation layer integrated with `BRAND_BASELINE_REALITY_MATRIX`.
- hlk-erp Knowledge panel route shipped (or API-only MVP per R-IH-83-5 scope-down).
- Closure UAT report at `reports/uat-i83-closure-<YYYY-MM-DD>.md`.

## Cross-references

- Candidate: [`i83-ai-archivist-and-kirbe-ingestor.md`](../_candidates/i83-ai-archivist-and-kirbe-ingestor.md) (full architectural sketch + conundrum index).
- Governance kit (landed I86 Wave R+5 close, 2026-05-29 — closes the "thinly governed" gap): [`decision-log.md`](decision-log.md) (D-IH-83-A..L) · [`risk-register.md`](risk-register.md) (R-IH-83-1..6) · [`files-modified.csv`](files-modified.csv).
- Promotion override: `D-IH-86-CC` (Wave O OVERRIDE).
- Framework narrowing: `D-IH-84-E` (E1 LlamaIndex-continue + LangGraph-workflow).
- Sibling: [I82 Capability Doctrine](../_candidates/i82-holistika-capability-doctrine-and-commercial-readiness.md) (hard prerequisite at P4).
- Sibling: [I76 MADEIRA elevation](../76-madeira-elevation/master-roadmap.md) (potential AIC pattern for audience translation layer).
- Cluster coordinator: [I86](../86-initiative-cluster-execution-coordinator/master-roadmap.md).
- Governing rules: [`akos-holistika-operations.mdc`](../../../.cursor/rules/akos-holistika-operations.mdc) §"Two-plane model".
