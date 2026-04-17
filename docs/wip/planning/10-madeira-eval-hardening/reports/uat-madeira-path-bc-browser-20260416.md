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

---

## Addendum — 2026-04-16 (gateway + API recovery)

**Context:** Foreground `openclaw gateway run --port 18789 --force` after config parse fix; AKOS `serve-api` on **8420**; default chat model set to **`ollama/qwen3:8b`** in operator `~/.openclaw/openclaw.json` so `hlk_*` tool calls are viable (see Scenario 0 model note in [`hlk_admin_smoke.md`](../../../../docs/uat/hlk_admin_smoke.md)). **SOC:** no tokens or prompt bodies below.

| Area | Step | Result | Notes |
|:-----|:-----|:-------|:------|
| **Loopback** | `GET http://127.0.0.1:18789/` | **PASS** | HTTP 200 (cold gateway startup ~90s before ready). |
| **Loopback** | `GET http://127.0.0.1:8420/health` | **PASS** | `status: ok` from control plane. |
| **Loopback** | `GET http://127.0.0.1:8420/agents` | **PASS** | JSON lists **madeira** plus orchestrator, architect, executor, verifier. |
| **Scenario 0** | Step 1 — five agents | **PASS** | Same five agents via **8420** `/agents` SSOT; gateway **`/agents`** returns 200 (dashboard SPA). |
| **Scenario 0** | Step 2 — Madeira chat entry | **PASS** (shell) | `GET /chat?session=agent:madeira:main` on **18789** returns **200** (chat shell reachable). |
| **Scenario 0** | Steps 3–7 — WebChat behaviour | **SKIP** | Qualitative prompts (startup cleanliness, CTO / Research / KiRBe / Finance escalation) not executed in this agent session; run in a real browser with a **fresh** Madeira session. |
| **Automated** | `py scripts/browser-smoke.py` (HTTP-only) | **PARTIAL** | **PASS:** `dashboard_health`, `agent_visibility`, `hlk_graph_summary`, `hlk_graph_explorer`. **`swagger_health`:** FAIL (request **timed out** against `/docs` or `/health` probe — treat as env/perf follow-up, not SSOT regression). |
| **Automated** | `py scripts/browser-smoke.py --playwright` | **SKIP** | Playwright worker subprocesses exited **3221225477** (`0xC0000005`) on this host; install/repair browsers (`py -m playwright install chromium`) or use HTTP-only / manual UAT. |
| **Automated parity** | Scenario 0 pytest slice ([`hlk_admin_smoke.md`](../../../../docs/uat/hlk_admin_smoke.md) table) | **PASS** | `TestAgents::test_agents_returns_list`, `TestRouting::test_madeira_policy_includes_sequential_thinking`, `TestRouting::test_classify_admin_route`. |

**Cursor plan YAML:** `~/.cursor/plans/madeira_b+c_and_sota_eval_9721d1fe.plan.md` — `phase2c-docker-win-docs` and `phase3b-madeira-sota` reconciled to **completed** (USER_GUIDE §14.3b Docker/WSL2 + Path C / overlays already landed in repo); see plan file frontmatter.

---

## Addendum — Cursor IDE Browser MCP (Scenario 0 spot-check) — 2026-04-17

**Method:** Cursor **cursor-ide-browser** MCP, view navigated to `http://127.0.0.1:18789/chat?session=agent%3Amadeira%3Amain`. **SOC:** no bearer tokens, no full assistant bodies — outcome labels only.

| Scenario 0 step | Result | Notes |
|:----------------|:-------|:------|
| 1–2 (dashboard + Madeira chat) | **PASS** | OpenClaw Control UI; message field **“Message Madeira (Enter to send)”**; model selector shows **qwen3:8b · ollama**. |
| 3 (startup / ready) | **PASS** | Prior turn shows configured greeting + session startup instruction surface (no `NO_REPLY` placeholder in a11y snapshot). |
| 4 (“Who is the CTO?”) | **PASS** | **Tool call `hlk_role`** / **Tool output `hlk_role`** controls present; assistant summary line names **Chief Technology Officer (CTO)** and **Think Big** / **Tech** (qualitative spot-check on visible copy only). |
| 5 (“Show me all Research roles”) | **SKIP** | Follow-up remained **queued** / generation did not surface **Holistik Researcher** in the page within **120s** (`browser_wait_for` timeout). Re-run with idle gateway queue or fresh `/new` session. |
| 6–7 | **SKIP** | Not executed in this MCP pass; registry parity for KiRBe + Finance escalation is covered by **HTTP** `scenario0_*` rows in `py scripts/browser-smoke.py` when `serve-api` is up. |

**Related automation (repo):** `py scripts/browser-smoke.py` (HTTP) now emits `scenario0_hlk_cto`, `scenario0_hlk_research_area`, `scenario0_hlk_kirbe_children`, `scenario0_admin_escalation`; see `tests/test_browser_smoke_scenario0_evaluators.py` and `docs/uat/hlk_admin_smoke.md` automated parity table.

---

## Addendum — 2026-04-18 (session recovery + WebChat retry)

**Method:** Cursor **cursor-ide-browser** MCP; **New session** to clear queue; same Scenario 0 script as [`hlk_admin_smoke.md`](../../../../docs/uat/hlk_admin_smoke.md). **Deep troubleshooting:** [`SESSION_TROUBLESHOOTING.md`](SESSION_TROUBLESHOOTING.md). **SOC:** no secrets; assistant copy described at label level only.

| Scenario 0 step | Result | Notes |
|:----------------|:-------|:------|
| 5 — “Show me all Research roles” | **PASS** | **`hlk_search`** tool UI present; answer lists **Holistik Researcher** and other Research-area roles; assistant cites **`baseline_organisation.csv`** / **`process_list.csv`** in visible copy. |
| 6 — KiRBe Platform workstreams | **SKIP** (infra) | After step 5, gateway returned **`All models failed (3): ollama/… timeout`** for primary + fallbacks — **Ollama inference timeout**, not missing `hlk_*` tools. Warm Ollama / reduce load (see **SESSION_TROUBLESHOOTING**), then re-run. **Registry contract:** HTTP **`scenario0_hlk_kirbe_children`** when `serve-api` is up. |
| 7 — Finance restructure escalation | **SKIP** (infra) | Same model failure blocked a fresh assistant reply. **Routing contract:** HTTP **`scenario0_admin_escalation`** + pytest `test_classify_admin_route`. |

**Supersedes** step 5 **SKIP** in the 2026-04-17 addendum (queued-message timeout); root cause was **session queue**, fixed by **New session** + single prompt flow.

---

## Addendum — 2026-04-15 (Ollama stabilization + Scenario 0 steps 6–7 retry)

**Method:** Cursor **cursor-ide-browser** MCP; same flow as [`SESSION_TROUBLESHOOTING.md`](SESSION_TROUBLESHOOTING.md) — **no concurrent `ollama run`** during WebChat (terminated competing CLI warm-ups), **`ollama ps`** checked (`qwen3:8b` on GPU; embed model may also appear). Full page navigation to `http://127.0.0.1:18789/chat?session=agent:madeira:main` for a **clean** Madeira session; **one prompt at a time**; **180s** wait after each send. **SOC:** no secrets; assistant copy described at control / label level only.

| Scenario 0 step | Result | Notes |
|:----------------|:-------|:------|
| 6 — “What workstreams are under KiRBe Platform?” | **PASS** | **`hlk_search`** tool call + output controls present; visible answer cites **`process_list.csv`** and lists KiRBe-related project/process headings (e.g. KiRBe Platform, Envoy Tech Showcase, Traceability & Observability). |
| 7 — “I need to restructure the Finance area” | **PASS** | **`akos_route_request`** tool call + output controls present; visible reply includes **Escalation: admin** and read-only Madeira framing, plus suggested **Orchestrator → Architect → Executor → Verifier** swarm. |

**Supersedes** steps **6–7** **SKIP (infra)** rows in the **2026-04-18** addendum for this Browser MCP pass (timeouts were addressed by **not** running a parallel Ollama CLI against the same GPU during dashboard turns).
