---
parent_initiative: INIT-OPENCLAW_AKOS-96
authored: 2026-06-11
exploration_ids: E1-E10
---

# I96 exploration matrix — 2026-06-11

Pre-flight validation for Tracks B–D. Sibling repos read at `root_cd/` per REPOSITORY_REGISTRY.csv.

## Summary table

| ID | Topic | Verdict | Load-bearing finding |
|:---|:---|:---|:---|
| **E1** | KiRBe API surface | **PASS** | FastAPI `app/api/main.py` + health routes; hybrid search + ingest in production v1.2 |
| **E2** | HLK-ERP Research Center | **PASS (stub)** | Stub UI + mock `/facts`; BFF covers ingest/health only — **no search/hybrid proxy** |
| **E3** | AKOS→Supabase→KiRBe sync | **PASS w/ risk** | 16-mirror one-way contract; prod drift class OPS-86-32 |
| **E4** | Research Radar loop | **PASS** | `research_radar_sweep.py` + `staleness_posture=block_govern` |
| **E5** | DATA_INTEGRATION_PLANE | **PASS** | Stream B pattern applies; §research extension at P1 optional |
| **E6** | Sibling overlap | **PASS** | I65 Contents pattern reusable; I89 read-only consumer |
| **E7** | Automation OS R7–R12 | **PASS** | Charter §7 quotas defined; 467 rows remain |
| **E8** | Holistic-agentic blocker | **PASS** | R4–R12 blocked on D4 only |
| **E9** | Neo4j posture | **PASS** | D-IH-32-M: KiRBe local ≠ AKOS graph |
| **E10** | Multi-channel feed | **DEFER** | CHANNEL_TOUCHPOINT_REGISTRY exists; P10 after P7 |

---

## E1 — KiRBe (`root_cd/kirbe`)

| Column | Finding |
|:---|:---|
| **Endpoints** | `/health`, `/api/health`, `/api/v1/health` (`app/api/vercel_entry.py`); main API in `app/api/main.py` |
| **Ingest** | WebSocket/async jobs; LlamaIndex readers; `kirbe.*` schema (32 tables) |
| **Search** | Hybrid BM25 + vectors + RRF (v1.2 registry narrative) |
| **Idempotency** | Task IDs on `/status/{task_id}` pattern in archivist POC paths |
| **Metadata** | Vault docs + vectors; compliance mirror read-only |
| **Reuse for I96** | BFF proxy pattern from ERP; ingest contract maps ledger `SRC-*` → vault tags |

## E2 — HLK-ERP (`root_cd/hlk-erp`)

| Column | Finding |
|:---|:---|
| **Research Center** | `app/research-center/page.tsx` — **stub** (3 placeholder cards, no data) |
| **KiRBe BFF** | `/api/kirbe/health`, `/api/kirbe/simpledir/scan`, `/api/kirbe/yt-transcript/*`, `/api/kirbe/docs`, `/api/kirbe/tasks/status/*` |
| **Auth** | `lib/auth/route-matrix.ts` lists `/api/kirbe/health` |
| **Client** | `lib/services/kirbe.ts` — TanStack/fetch wrappers |
| **Reuse** | Extend BFF for search panel; GitHub Contents for WIP packs (I65) |
| **Break points** | No JWT forwarded to KiRBe upstream; TanStack `useMirrorView` unused on research routes; WebSocket/SSE not proxied |

## E1 break points (load-bearing)

- KiRBe Render API live; Vercel deployment health-only.
- Document idempotency via `checksum_sha256`; task IDs are not idempotent.
- Persona/channel mirrors not yet consumed in hybrid search (I32 audit deltas).
- Browser must use ERP BFF — not KiRBe host directly.

## E3 — Sync contract

| Column | Finding |
|:---|:---|
| **Authority** | Canonical vault → `compliance.*` mirrors → KiRBe read-only |
| **Mirrors** | 16 listed in `config/sync/kirbe-sync-contract.md` §2 |
| **Break points** | Mirror emit lag (OPS-86-32); KiRBe never writes compliance |
| **Scripts** | `sync_compliance_mirrors_from_csv.py` family in AKOS |
| **AKOS daemon** | `kirbe_sync_daemon.py` — **dry-run only**; `--apply` is gated no-op |
| **Validator gap** | `validate_kirbe_sync.py` not shipped (contract §future) |

## E4 — Research Radar

| Column | Finding |
|:---|:---|
| **Register** | `INTELLIGENCEOPS_REGISTER.csv` |
| **Engine** | `scripts/research_radar_sweep.py`, `akos/hlk_research_radar.py` |
| **Govern hook** | `staleness_posture=block_govern` blocks govern until refresh |
| **ERP panel** | Surface `next_verify_by` + queue from sweep output |

## E5 — DATA plane

Stream B (Edge Function → holistika_ops → pgmq) is binding template. Research feed delivery is **SHARE** stage — forward to P10; field mapping at P1 sufficient for v1.

## E6 — Sibling initiatives

| Initiative | Overlap | Resolution |
|:---|:---|:---|
| I83 P4 Knowledge panel | KiRBe search | I96 owns Research Center; I83 owns ingest |
| I92 stub | ERP owner | I96 P6 spec → I92 expands roadmap |
| I65 planning workspace | GitHub Contents | Reuse BFF module pattern |
| I89 Research rollup | Persona route | Read-only consumer of Research Center |

## E7 — Automation OS remainder

| Tranche | Target rows | Vault focus |
|:---|---:|:---|
| R7 | 74 | Compliance, PRECEDENCE, process_list |
| R8 | 72 | Finance, Legal |
| R9 | 72 | Marketing, CRM adapters |
| R10 | 71 | verification-profiles |
| R11 | 71 | Monorepo, agent CLI |
| R12 | 106 | D4 synthesis + skeptic close |

## E8 — Holistic-agentic

R3 committed (305 rows). R4–R12 charter blocked until `implementation-spec-2026-06-11.md` operator ratification (D4).

## E9 — Neo4j

AKOS/I95 Neo4j = HCAM enterprise graph. KiRBe Neo4j = vault search only. **No merge.**

## E10 — Multi-channel feed

Slack/Discord/Telegram MCP inventory in workspace; CHANNEL_TOUCHPOINT_REGISTRY pattern available. **Go/no-go: defer to P10** after Research Center v1 PASS.
