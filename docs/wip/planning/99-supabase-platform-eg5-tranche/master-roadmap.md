---
initiative_id: INIT-OPENCLAW_AKOS-99
initiative_slug: 99-supabase-platform-eg5-tranche
title: "I99 — Supabase Platform EG-5 Tranche"
status: active
authored: 2026-06-13
last_review: 2026-06-13
inception_decision_id: D-IH-99-A
owner_role: System Owner
co_owner_roles:
  - DataOps
  - Tech Lab Lead
parent_initiatives:
  - INIT-OPENCLAW_AKOS-95
related_initiatives:
  - INIT-OPENCLAW_AKOS-96
  - INIT-OPENCLAW_AKOS-83
  - INIT-OPENCLAW_AKOS-62
  - INIT-OPENCLAW_AKOS-68
  - INIT-OPENCLAW_AKOS-14
linked_decisions:
  - D-IH-99-A
  - D-SUP-MCP-01
  - D-SUP-EG5
language: en
audience: J-OP;J-AIC
program_anchors:
  - PRJ-HOL-DAT-2026
  - PRJ-HOL-PGF-2026
authoritative_plan: docs/wip/planning/99-supabase-platform-eg5-tranche/master-roadmap.md
research_lanes:
  - docs/wip/intelligence/supabase-platform-features-holistika-impact-2026-06-13/
promoted_from: docs/wip/intelligence/supabase-platform-features-holistika-impact-2026-06-13/research-synthesis-2026-06-13.md
---

# I99 — Supabase Platform EG-5 Tranche

> **Problem.** Holistika governs compliance mirrors, Edge Functions, and pgmq — but **Auth**, **Storage**, and **Realtime** remain ungoverned in `SUPABASE_MODULE_REGISTRY.csv`. Enabling Supabase MCP widens agent discovery without replacing the operator SQL gate; product modules turned ON without registry + process rows repeat prod-lag failure mode.
>
> **Outcome.** Close **EG-5** (Auth / Storage / Realtime adoption matrix) under I95 L1 doctrine; enable **Advisor** as read-only post-DDL lint; wire **I96 Research Center** as first consumer (auth redirect + Realtime staleness strip).

## Operator ratifications (2026-06-13)

| Gate | Choice |
|:---|:---|
| Strategy | **Option B** — Full EG-5 tranche (Auth + Storage + Realtime registries + `process_list` rows after canonical-CSV gate) |
| Advisor | **Enable in MCP now** (read-only) |
| First consumer | **I96** Research Center |
| Spine | **I99** (this initiative); ad-hoc experiments moved to [`00-ad-hoc-proposals/`](../00-ad-hoc-proposals/) |

## Phase shape

| Phase | Purpose | Deliverable | Verification |
|:---|:---|:---|:---|
| **P0** | Initiative mint + folder rename | Standard 6 artifacts; `00-ad-hoc-proposals/` legacy note | Planning README row; registry row |
| **P1** | MCP inventory reconcile | `reports/mcp-inventory-reconcile-2026-06-13.md` | **DONE** 2026-06-13 — 95 matched; 2 local-only (I96+I97); 1 remote-only; Advisor 237 lints |
| **P2** | Auth registry + I96 consumer spec | Auth hook/provider registry draft; I96 redirect contract; **auth email tranche** [`reports/auth-email-and-identity-inbox-tranche-2026-06-13.md`](reports/auth-email-and-identity-inbox-tranche-2026-06-13.md) (Resend + Cloudflare + inbox tiers) | **DONE** draft 2026-06-13 — [`reports/auth-registry-and-i96-consumer-spec-2026-06-13.md`](reports/auth-registry-and-i96-consumer-spec-2026-06-13.md); canonical CSV at **P5** gate |
| **P3** | Realtime publication contract | Realtime registry + I96 freshness strip wiring spec | **DONE** draft 2026-06-13 — [`reports/realtime-publication-and-i96-freshness-spec-2026-06-13.md`](reports/realtime-publication-and-i96-freshness-spec-2026-06-13.md); canonical CSV + publication DDL at **P5** gate |
| **P4** | Storage bucket/path registry | Storage registry draft + GTM asset delivery posture | **DONE** draft 2026-06-13 — [`reports/storage-bucket-and-gtm-asset-spec-2026-06-13.md`](reports/storage-bucket-and-gtm-asset-spec-2026-06-13.md); canonical CSV + bucket DDL at **P5** gate |
| **P5** | Canonical CSV tranche | **All 8 ungoverned** module rows + `process_list` where needed | **DONE** 2026-06-13 — **D-IH-99-J** Option A mint; DDL apply **scheduled** operator SQL gate |
| **P6** | EG-4 RLS posture (paired) | RLS registry + validator scaffold | Scheduled after P5 or parallel if resourced |
| **P7** | Closure UAT | `reports/uat-i99-eg5-tranche-*.md` | PASS-WITH-FOLLOWUP if I96 consumer UAT still open |

## Two-plane contract (binding)

1. **DDL** — `supabase/migrations/` only; operator SQL gate before apply.
2. **Mirror DML** — CSV emit/apply per `SOP-HOLISTIKA_COMPLIANCE_MIRROR_DML_001`.
3. **MCP** — discovery + Advisor read-only; no routine mutation.

## Verification matrix

```powershell
py scripts/validate_research_action.py --source-ledger docs/wip/intelligence/supabase-platform-features-holistika-impact-2026-06-13/source-ledger.csv
py scripts/validate_hlk.py
py scripts/validate_initiative_registry_frontmatter_sync.py
py scripts/render_wip_dashboard.py
```

## Cross-references

- Parent doctrine: [`SUPABASE_ECOSYSTEM_GOVERNANCE.md`](../../../references/hlk/v3.0/Admin/O5-1/Data/Architecture/canonicals/SUPABASE_ECOSYSTEM_GOVERNANCE.md) (I95 L1, **D-IH-95-G**)
- Research pack: [`../../intelligence/supabase-platform-features-holistika-impact-2026-06-13/`](../../intelligence/supabase-platform-features-holistika-impact-2026-06-13/)
- Implementation spec: [`reports/implementation-spec-2026-06-13.md`](reports/implementation-spec-2026-06-13.md)
- Auth registry + I96 consumer (P2): [`reports/auth-registry-and-i96-consumer-spec-2026-06-13.md`](reports/auth-registry-and-i96-consumer-spec-2026-06-13.md)
- Realtime + I96 freshness strip (P3): [`reports/realtime-publication-and-i96-freshness-spec-2026-06-13.md`](reports/realtime-publication-and-i96-freshness-spec-2026-06-13.md)
- Storage + GTM asset posture (P4): [`reports/storage-bucket-and-gtm-asset-spec-2026-06-13.md`](reports/storage-bucket-and-gtm-asset-spec-2026-06-13.md)
- Multi-store alignment (Analytics + Vector + Neo4j): [`reports/multi-store-data-plane-alignment-2026-06-13.md`](reports/multi-store-data-plane-alignment-2026-06-13.md)
- Auth email + identity inbox tranche: [`reports/auth-email-and-identity-inbox-tranche-2026-06-13.md`](reports/auth-email-and-identity-inbox-tranche-2026-06-13.md)
- First consumer: [`../96-research-data-plane-and-research-center/master-roadmap.md`](../96-research-data-plane-and-research-center/master-roadmap.md)
