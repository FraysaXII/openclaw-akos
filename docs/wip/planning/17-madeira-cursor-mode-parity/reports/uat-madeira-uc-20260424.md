# Madeira WebChat UAT — UC matrix (2026-04-24)

**Profile:** `gpu-shadow` (runtime state + `openclaw.json` merge). **ShadowGPU deploy:** attempted per `docs/USER_GUIDE.md` §8.8.

**Prereq evidence:** `py scripts/gpu.py status` after `py scripts/switch-model.py gpu-shadow --no-restart` — `Environment: gpu-shadow`, `Model: vllm-shadow/deepseek-r1-70b`. **VLLM_SHADOW_URL** remained placeholder in `config/environments/gpu-shadow.env` (not a live vLLM endpoint in this run).

| Step | Result | Notes |
|:-----|:------:|:------|
| `py scripts/gpu.py deploy-shadow` (model **2** AWQ) | **FAIL** | OpenStack **HTTP 401** — *The request you have made requires authentication.* Fix app creds / password auth or set **VLLM_SHADOW_URL** manually to a healthy endpoint (§8.8). |
| `py scripts/switch-model.py gpu-shadow` (first run) | **PARTIAL** | Merged `gpu-shadow.json`, copied env; `gateway call health` exited 1; first run may not have completed `record_switch` (gateway recovery wait). |
| `py scripts/switch-model.py gpu-shadow --no-restart` | **PASS** | State saved: `.akos-state.json` has `activeEnvironment: gpu-shadow`, `activeModel: vllm-shadow/deepseek-r1-70b`. |
| `py scripts/gpu.py status` | **PASS** (with caveats) | Environment **gpu-shadow**; display still shows stale **RunPod** block from prior `activeInfra` (cosmetic; operator can ignore or clear state). |
| `py scripts/browser-smoke.py` | **PASS** (14/14) | **Final** run: `dashboard_health`, Scenario 0 registry slice, `mode=plan_draft` (after control plane), `madeira control` all PASS. (Earlier run had 13/14 when gateway was restarting.) |
| **Cursor Browser —** `http://127.0.0.1:18789/chat?session=agent:madeira:main` | **PARTIAL** | Dashboard loaded; **Madeira** session; model selector shows **vllm-shadow** as default. **No complete assistant turn** in WebChat: generation stayed in *Stop generating* with placeholder **VLLM** — consistent with missing **VLLM_SHADOW_URL**. |
| **`http://127.0.0.1:8420/madeira/control`** | **PASS** | **Set Plan draft** clicked; `GET /agents/madeira/interaction-mode` → `madeiraInteractionMode: plan_draft`, `planOverlayActive: true`. |

## UC-ID matrix (Tier 3 qualitative / tool loops)

| UC-ID | Result | Notes |
|:------|:------:|:------|
| M-HLK-04 | **SKIP** | Needs tool-capable model response + WebChat turn; **blocked** by unreachable **vllm-shadow** (no `VLLM_SHADOW_URL`). |
| M-HLK-05 | **SKIP** | Same. |
| M-HLK-06 | **SKIP** | Graph path optional; no chat turn. |
| M-FIN-01 | **SKIP** | Same. |
| M-FIN-02 | **SKIP** | Same. |
| M-RT-02 | **SKIP** | Same. |
| M-RT-03 | **SKIP** | Same. |
| M-PLAN-01 | **PARTIAL** | Control plane: **plan_draft** set and API confirms; **fenced JSON / WebChat banner** not exercised (no successful completion from model in chat). |
| M-OPS-01 | **SKIP** | Same as M-HLK-04. |
| M-NEG-01 | **SKIP** | Matrix asks **clean session** before negatives; not run. |
| M-NEG-02 | **SKIP** | Not run. |

## Follow-up (to reach full PASS on WebChat + ShadowGPU)

1. **Auth:** Fix OpenStack credentials (or use a valid `clouds.yaml` / application credential) and re-run `py scripts/gpu.py deploy-shadow`, **or** set **`VLLM_SHADOW_URL`** in `config/environments/gpu-shadow.env` to a **healthy** vLLM `/v1` base URL, then `py scripts/switch-model.py gpu-shadow`.
2. **Health:** `curl` / `Invoke-WebRequest` `$env:VLLM_SHADOW_URL/models` and confirm gateway uses **`vllm-shadow`** without indefinite stalls.
3. Re-run this matrix in WebChat with **`/new`** before **M-NEG-***; confirm tool traces in UI or logs.

**After capture:** `madeira/control` was set back to **Ask (compact)** so default operator posture is not left on plan draft.

**Governance:** No secrets, no PII, no full prompts stored here.
