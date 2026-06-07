---
title: Capability collapse synthesis (6 area maps -> reconciled enterprise map)
initiative: INIT-OPENCLAW_AKOS-95
decision: D-IH-95-I
authored: 2026-06-08
language: en
status: ratified
---

# L2 capability collapse — synthesis + ratified plan (D-IH-95-I)

Consolidates the six area-clustering agents into one reconciled plan. Operator-ratified 2026-06-08.

## 1. Per-area results (the six maps)

| Area | rows | -> capabilities | evict | cross-area flags | map |
|:---|---:|---:|---:|:---|:---|
| Operations | 404 | 18 | 9 | 8 + 3 RevOps (nets ~7-10) | operations-collapse-map.md |
| Tech | 379 | 27 | 27 (+~20 secondary) | 5 | tech-collapse-map.md |
| People | 93 | 22 | 2 | 6 | people-collapse-map.md |
| Research | 82 | 12 | 0 (9 dedup; 18 tags->topics) | 2 Delivery + 10 imports | research-collapse-map.md |
| Marketing | 117 | 11 | 3 | 2 + MKT/Marketing fix | marketing-collapse-map.md |
| Data/Finance/Legal | 44 | 11 (4/4/3) | 0 | few | data-finance-legal-collapse-map.md |
| **Raw** | **1,119** | **~101** | **~41 (+~20)** | **~33 flagged** | — |

After cross-area reconciliation (merge duplicates, rehome to true area) the **enterprise net is ~80**
— a ~14:1 de-densification, squarely in the research's predicted strategic band.

## 2. Ratified decisions (D-IH-95-I)

| # | Decision | Verdict |
|:--|:--|:--|
| Eviction target | code-symbols + tools don't fit `COMPONENT_PRIMITIVE_REGISTRY` (render-primitives) | **SPLIT**: SaaS tools (Mailchimp/Calendly/Terraform/CUDA) -> `SUBSTRATE_REGISTRY`; code-symbols (~31, LLMConfig etc.) -> verify in `COMPONENT_SERVICE_MATRIX`, then **remove** from capability registry (implementation internals, not capabilities) |
| Cross-area | ~33 flagged | **RECONCILE** — rehome to true area + merge dups -> deduped enterprise net (~80) |
| L1 domain | ~9 domains != 8 HLK areas | **keep `area` = HLK area; ADD `l1_domain` field** (lightweight grouping; both views coexist) |
| Contested folds | per-agent | **ACCEPT all**: People 14-row methodology fold = 1 capability; Tech ~20 secondary LlamaIndex -> evict with the 27; Research 18 subject-tags -> `TOPIC_REGISTRY`; Research protect/counter-intel gap -> flag to Semantic Council (no hollow row) |
| Execution order | per-domain slices | **PILOT Data+Finance+Legal (44->11, clean)** -> Marketing -> Research -> People -> Operations -> Tech |
| bearer + MKT | collapse-time mechanics | **BOTH**: `bearer_class` -> realization edge (capabilities become bearer-agnostic; bearer derived from the realizing process's owner) + normalize the 1 stray `Marketing` area value -> `MKT` |

## 3. New CAPABILITY_REGISTRY schema (applied at collapse)

- **ADD** `l1_domain` (the ~9-domain grouping), `definition` (1-sentence; or fold into `notes`).
- **REMOVE** `bearer_class` (capabilities are bearer-agnostic; bearer lives on the realizing process row in `process_list`).
- **KEEP** `capability_tier` (differentiating|utility), `area`, `role_owner`, `originating_process_ids` (now N:N), `lifecycle_status`, review-stamps, `notes`.
- The i81 seed-audit fields (`i81_verdict`/`i81_gap_summary`/`external_register_summary`) are seed-specific; disposition (drop vs keep-as-historical) is an execution-time call — lean **drop** (they describe the old seed rows, not the stable capabilities).

## 4. Eviction routing (ratified split)
- **Tools** (SaaS/platforms): `SUBSTRATE_REGISTRY` (substrate-landscape doctrine).
- **Code-symbols** (~31, the `gtm_madeira_dtp_191..217` block + Tech LlamaIndex + Operations scripts): verify presence in `COMPONENT_SERVICE_MATRIX.csv`; if present, simply remove from the capability registry; if missing, add to the component matrix first.
- **Kanban states / TBD placeholders / Trello-links**: delete (not entities).

## 5. process_list radical cleanup (NEW — operator 2026-06-08, scope pending)
The collapse revealed `process_list` carries the same pollution (Trello task-grain, code-symbols,
mind-map imports, bilingual dups, cross-area mis-tags). Operator wants a **radical but governed**
cleanup. Scoped by the process-list issue-inventory agent (-> `process-list-issue-inventory-2026-06-08.md`)
+ an AskQuestion before any `process_list` edit (hardest-gated canonical). Coordinated with the
collapse because they share rows (capability `originating_process_ids` must stay valid).

## 6. Execution sequencing (gated, per slice, validate_hlk between)
1. Capability schema change (add `l1_domain`, remove `bearer_class`, +mirror) — foundation.
2. **Pilot:** Data+Finance+Legal collapse (44->11).
3. Marketing (117->11) -> Research (82->12) -> People (93->22) -> Operations (404->18) -> Tech (379->27).
4. Cross-area reconciliation pass (merge the ~33 flagged -> net ~80).
5. Evictions (tools->substrate; code-symbols->component-matrix/remove).
6. process_list cleanup (coordinated, after its AskQuestion).
Each slice is a gated canonical-CSV change with `validate_hlk` + the capability-rollup audit.
