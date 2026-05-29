---
title: Research rollout backlog — managed path after the CORPINT lifecycle logic change
language: en
intellectual_kind: rollout_backlog_tracker
sharing_label: internal_only
audience: J-OP;J-AIC
role_owner: PMO (interim) + Lead Researcher
co_owner_role: System Owner
status: active
authored: 2026-05-29
last_review: 2026-05-29
ratifying_decisions:
  - D-IH-75-G
  - D-IH-75-H
parent_initiative: INIT-OPENCLAW_AKOS-86
mint_home_initiative: INIT-OPENCLAW_AKOS-75
linked_decisions:
  - D-IH-75-G
  - D-IH-75-H
  - D-IH-86-FG
  - D-IH-86-FH
  - D-IH-86-FI
  - D-IH-86-FJ
---

# Research rollout backlog — the managed path

> **Why this exists.** The Research area just took a big move — the CORPINT lifecycle became its
> organizing spine (`D-IH-75-G`). A move that size leaves a *wake* of follow-up work: things
> deferred on purpose, cross-area hand-offs to wire, and a whole data-management thrust (DAMA) the
> operator wants next. This file is the **PM path**: one place where every open item lives, with an
> owner, a priority, a status, a dependency, and a pointer to its formal home (an `OPS-86-*` action,
> an initiative, or a candidate). It is **propagated under I86** (the cluster coordinator) and
> **maintained** at the cadence in §7. Nothing here is lost; everything here is managed.
>
> **How to read it:** §1–§5 are the themes (what the work *is*); §6 is the single consolidated table
> (the queryable backlog); §7 is the maintenance contract (how the path stays alive).

## 1. Theme A — Research area-build follow-ups (the wake of the logic change)

The C6 build (commit `2839f22`) shipped the area logic + structure. It deliberately deferred the
heavier, riskier, or co-ratification-dependent pieces:

| Ref | Item | Why deferred | Home |
|:---|:---|:---|:---|
| A1 | **Counter-Intelligence discipline mint** (PROTECT stage → full discipline) | Needs People/Ethics + People/Compliance co-ratification (single-ownership) | `OPS-86-27` · `D-IH-75-H` |
| A2 | **Legacy SSOT migration** (SOPs + IntelligenceOps register CSV → top-level `Research/`) | SSOT-path change ripples into PRECEDENCE + validators + cursor-rule globs; operator-gated | `OPS-86-26` · migration proposal |
| A3 | **`SOP-RESEARCH_OUTAKE_HANDOFF_001`** (the SHARE→Marketing hand-off checklist) | Net-new SOP; lands with the per-engagement cadence phase | I75 P5 |
| A4 | **Derived-recall principle → Methodology canonical** (the RECALL discipline) | Low priority; the load-bearing half (retrieval infra) is Tech-owned | I75 (Methodology) |
| A5 | **Per-discipline SOP buildout** (Methodology/Intelligence/Diagnosis/Validation) — now lifecycle-framed | The original I75 P1–P4 scope; reframed, not replaced | I75 P1–P4 |
| A6 | **files-modified.csv backfill** for the C6 build | Traceability hygiene; no validator blocks it; backfill-allowed | `OPS-86-31` |

## 2. Theme B — Cross-area reciprocal pointers (single-ownership; KB-integrity I81)

The lifecycle doctrine documents **Research's side** of each cross-area join. The **reciprocal
pointer on the sister area's canonical** is that area's to ratify — tracked here so the work *helps*
those areas instead of being imposed on them.

| Ref | Join | Sister area adds (their ratification) | Home |
|:---|:---|:---|:---|
| B1 | **SHARE** | Marketing/Brand: a render-side pointer (Research internal-register → external-register hand-off) | `OPS-86-28` |
| B2 | **STORE + RECALL** | Tech/KB: a KB-side pointer (KM Topic-Fact-Source + Neo4j + KiRBe ingestion of research output) | `OPS-86-28` |
| B3 | **PROTECT** | People/Ethics (counter-intelligence red lines) + People/Compliance (access/confidence/redaction) | `OPS-86-28` · `D-IH-75-H` |

## 3. Theme C — DAMA data-management + research-feed delivery (the operator's next thrust)

> Operator framing (2026-05-29): *"i'm thinking about DAMA for all of this … we already have data
> consumers or ETLs that wire here — KiRBe and its ever growing sources, ERP, KB, Supabase, our
> orchestration systems, RPAs — that I'd like to e.g. get a proper research feed in my inbox or
> pushed through other media like Discord, Slack, Telegram."*

This is the **STORE → RECALL → SHARE** data layer of the CORPINT lifecycle, operationalized as real
data products with real delivery. It is initiative-sized → new candidate
[`i-nn-research-data-management-and-feed-delivery.md`](../_candidates/i-nn-research-data-management-and-feed-delivery.md).

### 3.1 The lifecycle × DAMA-DMBOK map (the bridge)

| CORPINT stage | DAMA knowledge area(s) | Holistika surface |
|:---|:---|:---|
| ACQUIRE | Data Integration & Interoperability; Data Quality | HUMINT/OSINT collection; source ledgers; IntelligenceOps register |
| PROCESS | Data Quality; Metadata; Reference & Master Data | Research Action govern; Validation; the canonical registries |
| STORE | Data Storage & Operations; Data Architecture; Document & Content Mgmt | KM Topic-Fact-Source; Supabase mirrors; Neo4j; KiRBe |
| RECALL | Data Warehousing & BI; Metadata (findability) | Neo4j/MCP query; the register as queryable index |
| SHARE | Data Integration & Interoperability (delivery); Document & Content Mgmt | **research-feed delivery: inbox / Discord / Slack / Telegram** |
| PROTECT | Data Security; Data Governance | access levels; confidence; redaction; RLS |

### 3.2 The actionable pieces

| Ref | Item | DAMA area | Home |
|:---|:---|:---|:---|
| C1 | **Data-consumer / ETL inventory** — KiRBe (+ growing sources), ERP, KB, Supabase, orchestration systems, RPAs: who consumes/moves research data, in what shape | Data Integration & Interoperability | `OPS-86-29` · new candidate |
| C2 | **Multi-channel research-feed delivery** — the SHARE data-product pushed to operator inbox + Discord + Slack + Telegram (channel adapters; cadence; per-channel format) | Data Integration & Interoperability; Document & Content Mgmt | `OPS-86-30` · new candidate |
| C3 | **Data-ops readiness assessment** — honest gap map (operator: *"we still don't have data ops ready"*); what must exist before the feed is trustworthy | Data Storage & Operations; Data Governance | new candidate |
| C4 | **Research data-quality + metadata bar** — at STORE/RECALL (every shared fact carries its source + confidence) | Data Quality; Metadata | new candidate · Validation discipline |
| C5 | **KiRBe research-ingestor wiring** — research output as a KiRBe-ingestible product | Data Integration | I83 (AI-archivist + KiRBe ingestor) |

## 4. Theme D — Wave R+5 remaining chunks (already planned)

Per the [Wave R+5 plan](tranches/wave-r-plus-5-research-radar-and-governance-integrity.md) §3:

| Ref | Chunk | Status |
|:---|:---|:---|
| D1 | C2 — promote research-ops-substrate + topic+intent candidates; lifecycle-stage charters | open |
| D2 | C3 — I75 + I83 governance-kit backfill; Trello-topic → TOPIC_REGISTRY promotion | open |
| D3 | C5 — program-continuity + pre-action-reread specialty pair (optional) | open |
| D4 | R+5-close — inter-wave regression (13-dim) + index-integrity (8-dim) + closure UAT (11-section) | open |

## 5. Theme E — Proactive blind-spots ("more is needed")

| Ref | Item | Rationale | Home |
|:---|:---|:---|:---|
| E1 | **Area-identity anchor pattern → other areas** | The Research README + `akos-research-area.mdc` pattern should roll out to Marketing/Tech/People/Operations (each forgets its own identity too) | candidate (forward) |
| E2 | **Lifecycle doctrine → operator ERP panel** | Surface the CORPINT lifecycle + radar queue in hlk-erp as an operator research dashboard | I89 (ERP panels) / I83 |
| E3 | **Research-OPS substrate (10-pillar ReOps frame)** | The Boulton-8 + Brand + UX frame; pillars 3/4/7 overlap the DAMA thrust | [`i-nn-research-ops-substrate.md`](../_candidates/i-nn-research-ops-substrate.md) · `OPS-86-22/23` |
| E4 | **Cross-area Ops wiring review** | How every area wires its Ops surface to Research (the Asks & Logistics pillar) | I88 |

## 6. Consolidated backlog table (the queryable path)

| ID | Item | Theme | Owner | Priority | Status | Depends on | Formal home |
|:---|:---|:---|:---|:---:|:---|:---|:---|
| A1 | Counter-Intelligence discipline mint | area-build | Lead Researcher + People co-owners | P2 | open | People co-ratify | `OPS-86-27` |
| A2 | Legacy SSOT migration | area-build | System Owner + PMO | P1 | open | operator approve mapping | `OPS-86-26` |
| A3 | OUTAKE hand-off SOP | area-build | Lead Researcher | P3 | open | — | I75 P5 |
| A4 | Derived-recall canonical | area-build | KM Officer | P3 | open | — | I75 |
| A5 | Per-discipline SOP buildout | area-build | Lead Researcher | P1 | open | — | I75 P1–P4 |
| A6 | files-modified backfill (C6) | area-build | PMO | P2 | open | — | `OPS-86-31` |
| B1–B3 | Cross-area reciprocal pointers | cross-area | PMO + sister areas | P2 | open | sister-area ratify | `OPS-86-28` |
| C1 | Data-consumer / ETL inventory | DAMA | System Owner + Lead Researcher | P1 | open | — | `OPS-86-29` |
| C2 | Multi-channel research-feed delivery | DAMA | System Owner + Lead Researcher | P1 | open | C1 + C3 | `OPS-86-30` |
| C3 | Data-ops readiness assessment | DAMA | System Owner | P1 | open | — | new candidate |
| C4 | Research data-quality + metadata bar | DAMA | KM Officer | P2 | open | — | new candidate |
| C5 | KiRBe research-ingestor wiring | DAMA | System Owner | P2 | open | I83 | I83 |
| D1–D4 | Wave R+5 remaining chunks | wave | PMO + Lead Researcher | P1 | open | per plan | Wave R+5 plan |
| E1 | Area-anchor pattern → other areas | blind-spot | PMO | P3 | open | — | candidate (forward) |
| E2 | Lifecycle → ERP operator panel | blind-spot | System Owner | P2 | open | I89/I83 | I89 |
| E3 | Research-OPS 10-pillar substrate | blind-spot | Lead Researcher | P2 | open | I88 | candidate |
| E4 | Cross-area Ops wiring review | blind-spot | PMO | P2 | open | — | I88 |

Priority key: **P1** = this rollout / next wave; **P2** = near-term (Wave S–T band); **P3** =
forward (when its trigger fires).

## 7. Maintenance contract (how the path stays alive)

This is the *"as PMs do — create the path and maintain it"* half. The backlog is maintained, not
abandoned:

1. **Owner:** PMO (interim) + Lead Researcher co-own; System Owner co-owns the DAMA theme (C-rows).
2. **Cadence:** reviewed at **every I86 wave-close** (the coordinator's natural beat) + on demand
   when the operator asks. Each review: flip statuses, add emergent items, close done rows (cite the
   commit), re-rank priorities.
3. **Promotion path:** a P1 item that grows past an `OPS-86-*` action gets promoted to an initiative
   (candidate → INITIATIVE_REGISTRY) per `akos-conflict-surfacing-and-blocker-trackers.mdc`.
4. **Closure:** a row closes when its formal home (OPS action / initiative phase / candidate) records
   the work done. The row is struck through here with the closing commit sha, not deleted (audit
   trail).
5. **Source of truth split:** the `OPS-86-*` rows in [`OPS_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/OPS_REGISTER.csv)
   are the canonical machine-readable backlog; this file is the human-readable themed view. When they
   disagree, the CSV wins.

## 8. Cross-references

- The move that spawned this backlog: [`RESEARCH_LIFECYCLE_DOCTRINE.md`](../../../references/hlk/v3.0/Research/canonicals/RESEARCH_LIFECYCLE_DOCTRINE.md) (`D-IH-75-G`).
- Coordinating wave: [Wave R+5 plan](tranches/wave-r-plus-5-research-radar-and-governance-integrity.md) · cluster coordinator [I86 master-roadmap](master-roadmap.md).
- Substantive home: [I75 Research area governance](../75-research-area-governance/master-roadmap.md).
- DAMA initiative candidate: [`i-nn-research-data-management-and-feed-delivery.md`](../_candidates/i-nn-research-data-management-and-feed-delivery.md).
- Related: [I83 AI-archivist + KiRBe ingestor](../83-ai-archivist-and-kirbe-ingestor/master-roadmap.md) · [research-ops-substrate candidate](../_candidates/i-nn-research-ops-substrate.md) · I88 cross-area Ops wiring.
- Formal backlog SSOT: [`OPS_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/OPS_REGISTER.csv) rows `OPS-86-26` … `OPS-86-31`.
