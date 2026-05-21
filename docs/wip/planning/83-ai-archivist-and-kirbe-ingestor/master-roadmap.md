---
initiative_id: INIT-OPENCLAW_AKOS-83
title: I83 AI Archivist and KiRBe ingestor - knowledge-base surfacing system
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
  - D-IH-86-CC
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
| **P0** | Charter + architectural decisions | D-IH-83-A..F; OPS-83-1..4 | 1d | standard |
| **P1** | Registry-side spec (which registries KiRBe consumes; query API spec) | Spec doc; OpenAPI schema | 1d | standard |
| **P2** | Ingestor MVP (read-only) | KiRBe service behind `holistika_ops` schema; Tech Lab framework ratified | 3-5d | **canonical-CSV gate** (Supabase DDL via migrations per `akos-holistika-operations.mdc`) |
| **P3** | Audience translation layer (BRAND_BASELINE_REALITY_MATRIX integration) | Translation API; per-audience rendering tests | 2d | standard |
| **P4** | hlk-erp Knowledge panel integration (consumer-side; first UI) | Panel route; UAT against capability surfacing event | 2d | standard |
| **P5** | Closure + I84 forward-charter (operator-ratified scope expansion if needed) | Closure pause record; UAT report | 0.5d | closure-mega-ratify |

Total estimated effort: **9-12 days** for MVP (read-only Knowledge panel surfacing); production-ready with cross-source ingestion is a separate I84 expansion.

## Decisions preview (full set)

| ID | Question | Owner | Status entering | Close-out |
|:---|:---|:---|:---|:---|
| **D-IH-83-A** | I83 mega-charter scope — KiRBe ingestor MVP + audience translation + Knowledge panel | Tech Lab Lead | RATIFIED via D-IH-86-CC OVERRIDE | this commit |
| **D-IH-83-B** | Tech Lab framework choice (LlamaIndex / LangGraph / composition of both per `D-IH-84-E` E1) | Tech Lab Lead + System Owner | Proposed (D-IH-84-E narrowed to 2 finalists) | P0 |
| **D-IH-83-C** | Schema home — `holistika_ops.kirbe_*` vs new `kirbe.*` schema | System Owner | Proposed | P0 |
| **D-IH-83-D** | Composio adoption vs native build | Tech Lab Lead | Proposed | P0 |
| **D-IH-83-E** | Read-only MVP vs read-write (forward-charter to I84 if read-write) | System Owner | Proposed | P0 |

## Risks (top 5)

| ID | Risk | L | I | Mitigation |
|:---|:---|:---:|:---:|:---|
| **R-IH-83-1** | I82 not far enough along when I83 promotes — KiRBe has nothing to ingest | High | High | Hard prerequisite: **I82 P4** closed (use case archive minted) before I83 P0 enters substantive work |
| **R-IH-83-2** | Composio scope expansion is hard — building native is expensive | Medium | High | P0 conundrum; may scope down to read-only from existing canonical CSVs - HUMAN OPERATTOR: We have a huge wwoork aready done  in Kirbe and it's fly  or almost fuly  operational. t demonstrated it works  before. Itt has all the ingestors yoou  want and  a scallable POC.  Please  refacctoor  thhat while maintaining versioning  (my  keyyboard is brokken so  please  edit  tthis  to fit the  language forrmat. Ho'vve got allsoo the alpha experiment caled obsdan-reader (please add it to the regiry because it was a hge rresearch case that broght us coser tto nderstanding AI as we do now, allong with the draftts wwe made on legacy dasboard of boillerrplate. TThen there is the fact that irbe , ai arrchihvist, highway AI for MCP/API governed routing for AIC, MADEIRA the all orchestrattor simpple agentt tthat ehind is orr [or othhers  when commerciialliized] perfect allronder assistant that escales wwith -intsert madeira reworrk answwer- , any agent we want to craft for otthers no matter the framwork, RPAs, or own research works or others works, ccstomer vaults that we hhost foor them at a price/sbscripttioon/etc, we need to work on kirbe from all those prismas and moree  that i left out please )) (rephhrase my langagge please)|
| **R-IH-83-3** | RLS posture on kirbe.* schema unclear | Medium | High | Defaults: deny anon + authenticated; service_role only; classification-aware row filters per `KNOWLEDGE_PAIRING_REGISTRY.access_level` |
| **R-IH-83-4** | Audience translation hallucinates beyond canonical sources | Medium | High | Hard rule: KiRBe surfaces only registered rows; no LLM inference outside the registry-bounded answer space |
| **R-IH-83-5** | hlk-erp Knowledge panel not yet built — P4 has no UI consumer | Medium | Medium | Forward-charter; scope down to API-only MVP + defer UI to I85 |

## Closure criteria

- Charter (P0..P5) ratified.
- KiRBe MVP read-only operational against `KNOWLEDGE_PAIRING_REGISTRY` + `CAPABILITY_REGISTRY` (after I82 P4 mint).
- Audience translation layer integrated with `BRAND_BASELINE_REALITY_MATRIX`.
- hlk-erp Knowledge panel route shipped (or API-only MVP per R-IH-83-5 scope-down).
- Closure UAT report at `reports/uat-i83-closure-<YYYY-MM-DD>.md`.

## Cross-references

- Candidate: [`i83-ai-archivist-and-kirbe-ingestor.md`](../_candidates/i83-ai-archivist-and-kirbe-ingestor.md) (full architectural sketch + conundrum index).
- Promotion override: `D-IH-86-CC` (Wave O OVERRIDE).
- Framework narrowing: `D-IH-84-E` (E1 LlamaIndex-continue + LangGraph-workflow).
- Sibling: [I82 Capability Doctrine](../_candidates/i82-holistika-capability-doctrine-and-commercial-readiness.md) (hard prerequisite at P4).
- Sibling: [I76 MADEIRA elevation](../76-madeira-elevation/master-roadmap.md) (potential AIC pattern for audience translation layer).
- Cluster coordinator: [I86](../86-initiative-cluster-execution-coordinator/master-roadmap.md).
- Governing rules: [`akos-holistika-operations.mdc`](../../../.cursor/rules/akos-holistika-operations.mdc) §"Two-plane model".
