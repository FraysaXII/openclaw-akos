# Madeira WebChat UAT — UC matrix (2026-04-25)

**Executor:** agent (Cursor Browser `ec5a86` + `py scripts/browser-smoke.py`)  
**Prerequisites:** `docs/uat/madeira_use_case_matrix.md`  
**Tier 3 (WebChat):** qualitative rows require a **completed assistant turn**; gateway must reach the model without sandbox preflight failure.

## Summary

| Layer | Result |
|:------|:-------|
| **HTTP Scenario 0** (`browser-smoke.py`) | **PASS 14/14** — registry slice, finance, routing, `madeira/control` HTTP, `mode=plan_draft` while control plane was in that state. |
| **WebChat (Madeira) — UC matrix** | **BLOCKED** — every send ended with: **“Failed to inspect sandbox image: … docker API at npipe:////./pipe/docker_engine”** (Docker Desktop not running or unreachable). No tool traces or model output observed in-UI. |

**Root cause for Tier 3:** OpenClaw **strict sandbox** / tool path expects a **running Docker** backend on Windows (`USER_GUIDE` §14.3b / Path B). Until Docker is up (or dev policy allows relaxing sandbox for local UAT), **M-HLK-***, **M-FIN-***, **M-RT-***, **M-OPS-01**, **M-PLAN-01** (chat half), **M-NEG-*** cannot be **PASS**’d in WebChat.

## UC-ID outcomes

| UC-ID | Result | Notes |
|:------|:------:|:------|
| M-HLK-04 | **BLOCKED** | No reply — sandbox error before model. |
| M-HLK-05 | **BLOCKED** | Same. |
| M-HLK-06 | **BLOCKED** | Same. |
| M-FIN-01 | **HTTP PASS** (parity) | Covered by `browser-smoke` `scenario0_finance_*`; not WebChat. |
| M-FIN-02 | **HTTP PASS** (parity) | Same. |
| M-RT-02 | **BLOCKED** | WebChat. |
| M-RT-03 | **BLOCKED** | WebChat. |
| M-PLAN-01 | **PARTIAL** | **Control:** `Set Plan draft` on `http://127.0.0.1:8420/madeira/control` + API `plan_draft` / `planOverlayActive: true` **PASS**. **Chat:** plan content + non-canonical banner + schema-valid JSON not observed — sandbox error. |
| M-OPS-01 | **BLOCKED** | WebChat. |
| M-NEG-01 | **NOT RUN** | Matrix requires clean session; blocked by same preflight. |
| M-NEG-02 | **NOT RUN** | Same. |

## Evidence commands (no secrets)

- `py scripts/browser-smoke.py` → 14/14 (this run).  
- `GET http://127.0.0.1:8420/agents/madeira/interaction-mode` after plan draft (during session) → `plan_draft`.

## Post-run

- **Reset:** `POST /agents/madeira/interaction-mode` with body `{"mode":"ask"}` to restore default **Ask** where applicable.

## Follow-up (operator)

1. **Start Docker Desktop** (or WSL2 + Docker) and confirm `npipe:////./pipe/docker_engine` is reachable, **or** follow **`USER_GUIDE` §14.3b** for a governed dev exception if your OpenClaw build allows it.  
2. Re-run WebChat UAT: **New session** → M-HLK-04 … → **`/new`** before M-NEG-*.  
3. If **vllm-shadow** still times out after sandbox is fixed, increase gateway timeout or verify **Kalavai** `VLLM_SHADOW_URL` health.

**Governance:** no PII, no full prompts, no API keys in this file.
