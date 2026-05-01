---
language: en
status: draft
initiative: 32-holistik-ops-maturation
report_kind: external-team-architecture-audit
program_id: PRJ-HOL-KIR-2026
plane: techops
authority: Founder + System Owner + AI Engineer
last_review: 2026-04-30
audience: KiRBe team lead + KiRBe engineering
---

# KiRBe architecture audit (Initiative 32 P7)

**Date:** 2026-04-30
**Scope:** Audit of KiRBe `v1.2` against the 6-axis Holistik Ops doctrine + cross-repo extraction discipline.
**Source materials read:** `c:\Users\Shadow\cd_shadow\root_cd\kirbe\README.md`, `kirbe/.cursor/rules/00-project-standards.mdc`, `kirbe/.cursor/rules/01-docs-first.mdc`, `kirbe/.cursor/rules/50-database-supabase-postgres.mdc`, `kirbe/.cursor/rules/60-graphdb-neo4j.mdc`, `kirbe/.cursor/rules/90-deployment-runtime.mdc`, plus REPO_HEALTH_SNAPSHOT for `kirbe-platform` (2026-04-30).

## Executive summary

KiRBe is mature: v1.2 production with 7 connectors, hybrid search (BM25 + vector + RRF), audit logging (SOC2/GDPR-ready, 2-year retention), Stripe billing FDW + webhook, per-tenant usage metering, WebSocket progress streams, service-first DI, LlamaIndex readers, **its own local Neo4j**, Pydantic Logfire observability. This is **not a beginner brief**.

The audit confirms the v1.2 reality and recommends **5 architecture-level deltas** that consume the new I31 / I32 mirrors read-only without touching the substrates that are working. **3 things are explicitly NOT recommended for change**: billing-plane discipline, local Neo4j, LlamaIndex pipeline.

## v1.2 confirmed reality (E11)

| Capability | Source of truth in KiRBe |
|:-----------|:-------------------------|
| 5-step onboarding wizard | KiRBe v1.2 README §"Guided Onboarding" |
| 7 connectors (Discord, Gmail, Notion, Web, Google Drive, simpledir, yt_transcript) | KiRBe v1.2 README §"Enhanced Connectors" + `app/readers/` |
| Hybrid search (BM25 + vector + RRF) | `POST /api/v1/search/hybrid` |
| Audit logging (SOC2/GDPR-ready, 2-year retention) | KiRBe v1.2 README §"Audit Logging" |
| Stripe billing with FDW + webhook | `kirbe.subscriptions` + Edge Function webhook handler |
| Per-tenant usage metering with quotas | Free / Pro / Team / Enterprise tiers; HTTP 429 enforcement |
| WebSocket progress streams | `/ws/progress/{task_id}` with heartbeats |
| Service-first DI | `app/api/dependencies.py` cached via `functools.lru_cache`, Logfire spans |
| LlamaIndex readers + presets | `simpledir` with `minimal | pdf_only | office_only | rich | default_rich` presets |
| Local Neo4j (vault search graph) | `app/common/pipeline/graphdb/` per `kirbe/.cursor/rules/60-graphdb-neo4j.mdc` |
| Pydantic Logfire observability | per `kirbe/.cursor/rules/03-logfire-core.mdc` + `04-logfire-fastapi.mdc` |

## 5 architecture-level deltas (recommendations on a non-blocking timeline)

### Delta 1 — Persona-aware vault search

**What:** ingest `compliance.persona_registry_mirror` read-only and expose a "persona-aware vault search" filter. When a query enters via the dashboard, resolve the requesting user's intent to a persona archetype (per the 6-axis routing flow in HOLISTIK_OPS_DISCOVERY.md §3) and bias hybrid search results by `persona_id`.

**Why:** today hybrid search is persona-blind. Founder-asking-a-finance-question and Investor-asking-a-finance-question return the same RRF-fused result set. Persona-aware filtering improves perceived precision without retraining anything.

**Cost:** ~1 day. KiRBe ingests one new mirror; query layer adds one optional `persona_id` filter param.

### Delta 2 — Channel-tagged ingestion provenance

**What:** ingest `compliance.channel_touchpoint_registry_mirror` and tie incoming web/Discord/Gmail/Notion ingestion to the matching `channel_id` in your `kirbe_documents` provenance metadata.

**Why:** today the connector that ingested a doc is implicit (`source_type` field). After this delta, the channel that surfaced the doc to KiRBe (LinkedIn DM upload, web form scrape, Cal scheduling intake, etc.) is queryable via FK. Powers cross-channel attribution dashboards.

**Cost:** ~½ day. One new mirror + one new optional column on ingestion metadata.

### Delta 3 — Tenant-facing skill dashboard tile (MADEIRA-SaaS bridge)

**What:** ingest `compliance.skill_registry_mirror` and expose a "what AKOS skills are wired against KiRBe data" dashboard tile per tenant. List the skills with `lifecycle_status='active'`, their `eval_baseline_pct`, and the topics they consume.

**Why:** this is the **MADEIRA-SaaS substrate visible to your customers**. Today MADEIRA is internal; the moment a tenant sees "we have 5 governed skills wired against your KM", MADEIRA is productisable per `MADEIRA_PLATFORM.md`. D-IH-32-J pre-wired the `tenant_scope` column for this future.

**Cost:** ~1 day. One new mirror + one new dashboard component.

### Delta 4 — KiRBe Neo4j stays separate (D-IH-32-M reaffirmation)

**What:** confirm in code comments and in `kirbe-sync-contract.md` §11 (already shipped) that KiRBe's local Neo4j (per `60-graphdb-neo4j.mdc`) is **independent** of AKOS Neo4j.

**Why:** AKOS Neo4j is the governance projection (16 node labels including the 6 new ones from I32 P5/P6). KiRBe Neo4j is the vault search graph. Different shapes, different audiences. Merging them couples release schedules and graph schemas — bad idea.

**Cost:** zero. Documentation only. The constraint is real and enforced by using different `NEO4J_URI` env vars on the two sides.

### Delta 5 — Cite policy_id from POLICY_REGISTER on every RLS rule in `kirbe.*`

**What:** every RLS rule in your `kirbe.*` schema cites a `policy_id` from `compliance.policy_register_mirror` (or proposes a new policy_id via PR to AKOS if no existing rule fits).

**Why:** cross-repo policy traceability. Audit query: "which AKOS-canonical policy governs `kirbe.subscriptions`?" — answerable via SQL JOIN. Today this is folklore in your code review process.

**Cost:** ~1 day. Audit existing RLS, propose missing policy rows to AKOS, cite in DDL comments going forward.

## 3 things to NOT change

1. **Billing-plane discipline** (`hlk_billing_plane` metadata, `kirbe.*` vs `holistika_ops.*`) — perfect as-is. AKOS does not override this.
2. **LlamaIndex pipeline + reader composition** — out of scope; KiRBe's domain.
3. **Existing `60-graphdb-neo4j.mdc` cursor rule + the local Neo4j vault graph** — keep separate from AKOS Neo4j (D-IH-32-M).

## Operator action

KiRBe team lead: review this audit + the 6-section memo + the 3-PR seed (`kirbe.patch`). Reply with feedback on the 5 deltas or "schedule against your roadmap".

## Cross-references

- KiRBe v1.2 README: `https://github.com/FraysaXII/kirbe/blob/main/README.md`
- KiRBe handoff memo (sibling): `kirbe-handoff-memo-2026-04-30.md`
- 3-PR seed: `external-repo-seed-prs/kirbe.patch`
- Updated sync contract: `config/sync/kirbe-sync-contract.md` (§2 rewritten + §11 new)
- POLICY_REGISTER.csv: `docs/references/hlk/compliance/dimensions/POLICY_REGISTER.csv` (Delta 5 reference)
- D-IH-32-M (KiRBe Neo4j separation), D-IH-32-J (skill registry tenant_scope future)
- MADEIRA_PLATFORM.md: `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/business-strategy/MADEIRA_PLATFORM.md` (Delta 3 substrate)
