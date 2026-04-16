# UAT: Madeira Path B+C + Phase 6 browser matrix — 2026-04-16

**Initiative:** [10 — Madeira eval hardening](../master-roadmap.md)  
**Source plan (Phase 6):** Cursor `madeira_b+c_and_sota_eval` (browser / WebChat / Langfuse / graph / optional Docker).  
**Method this run:** Repo agent session — **SSOT + inventory verification**, `urllib` probes to loopback, `py scripts/browser-smoke.py --playwright` (JSON_RESULTS). **Not** Cursor IDE Browser MCP in this run (no live gateway during execution).

## Prerequisites (operator for full PASS rows)

- OpenClaw gateway listening on **`http://127.0.0.1:18789`**.
- Madeira chat model **tool-capable** for `hlk_*` (see [`docs/uat/hlk_admin_smoke.md`](../../../../docs/uat/hlk_admin_smoke.md) Scenario 0 note).
- Optional: AKOS control plane **`http://127.0.0.1:8420`** for `GET /agents` parity with smoke; Neo4j + `serve-api` for graph row; Langfuse project for M1 UI filters.

## Results (Phase 6 mapping)

| Area | Step | Result | Notes |
|:-----|:-----|:-------|:------|
| **Automated / SSOT** | `config/openclaw.json.example` contains **no** `web_search` / `web_fetch` strings | **PASS** | `rg` scan; Path C strip in template. |
| **Automated / SSOT** | Path B: `agents.defaults.sandbox.mode` + `tools.exec.host: sandbox` | **PASS** | `sandbox.mode` strict under defaults; `tools.exec.host` sandbox. |
| **Automated** | `py scripts/legacy/verify_openclaw_inventory.py` | **PASS** | `OVERALL: PASS` on example config (agent session). |
| **Automated** | `py scripts/browser-smoke.py --playwright` | **SKIP** (expected soft path) | `JSON_RESULTS:` all SKIP — `Gateway unreachable` / API `127.0.0.1:8420` unreachable (no local gateway during run). |
| **Loopback** | `GET http://127.0.0.1:18789/agents` | **SKIP** | WinError 10061 — connection refused. |
| **Loopback** | `GET http://127.0.0.1:8420/health` | **SKIP** | Connection refused. |
| **Madeira WebChat** | Scenario 0 steps 1–7 ([`hlk_admin_smoke.md`](../../../../docs/uat/hlk_admin_smoke.md)) | **SKIP** | Requires live gateway + operator browser / IDE browser MCP. |
| **Madeira dimensions** | D2 citation, D3 finance degraded, T4 ambiguity, T2 escalation, T5/T6 spot | **SKIP** | Same — WebChat + tool-capable model. |
| **Orchestrator / Architect** | Tool menu / policy: no ambient web tools; architect retains coarse `browser` in SSOT | **PASS** (SSOT) | Confirmed in `openclaw.json.example` agent `alsoAllow` / `deny` blocks; live UI not exercised. |
| **Path C scenario** | Public-doc style → browser or escalation (no tool-missing loop) | **SKIP** | Live session not run. |
| **Langfuse** | Filter traces by eval / `research_surface` (M1) | **N/A** | No Langfuse UI session this run; Langfuse MCP / SDK paths unchanged in repo. |
| **Graph** | `serve-api` + `/hlk/graph/explorer` minimal row | **SKIP** | Control plane down; see initiative **07** [`uat-graph-explorer-browser-20260415.md`](../../07-hlk-neo4j-graph-projection/reports/uat-graph-explorer-browser-20260415.md) for prior graph evidence. |
| **Windows** | Docker Desktop → Resources → File Sharing (`~/.openclaw`, repo root) | **N/A** | Host UI; operator checklist only ([`master-roadmap.md`](../master-roadmap.md) appendix A). |

## Governance (SOC)

- No API keys, tokens, or live prompt bodies recorded in this file.

## Operator follow-up

1. Start gateway + (optional) `serve-api`, then re-run **`py scripts/browser-smoke.py --playwright`** — expect non-SKIP rows when ports are open.
2. Execute **Scenario 0** in a real browser or Cursor Browser MCP; append a dated addendum table or new `uat-madeira-path-bc-browser-<YYYYMMDD>.md` with WebChat PASS/SKIP.
3. **Cursor plan YAML:** Reconcile todos in `madeira_b+c_and_sota_eval_9721d1fe.plan.md` (e.g. `phase2c-docker-win-docs`, `phase3b-madeira-sota` vs `phase6-verify-browser`) with repo reality — that file lives **outside** this git repo under `~/.cursor/plans/`.
