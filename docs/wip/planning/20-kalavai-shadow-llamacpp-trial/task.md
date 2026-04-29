# Task: Kalavai / Shadow llama.cpp trial — DeepSeek-R1-Distill-Llama-70B (Q4)

**Owner:** operator (Fayçal) · **Contact:** Jean-Jacques Sauvanet (Kalavai / Shadow trial)  
**Created:** 2026-04-24 · **Trial end:** **2026-05-01** (extended; confirm with JJ if extended again).

## Updated endpoint (supersedes earlier `469544` host)

| Kind | URL |
|:-----|:----|
| **OpenAI-compatible API base** | `https://deepseek-r1-distill-llama-70b-e405de-shadow-llamacpp.spaces.kalavai.net/v1` |
| **Browser (smoke UI)** | `https://deepseek-r1-distill-llama-70b-e405de-shadow-llamacpp.spaces.kalavai.net/` |
| **Prior trial URL (deprecated)** | `https://deepseek-r1-distill-llama-70b-gguf-469544-shadow-llamacpp.spaces.kalavai.net/v1` |

**Live model id** (from `GET /v1/models` on 2026-04-24): `DeepSeek-R1-Distill-Llama-70B-Q4_K_M.gguf` (Q4_K_M).  
JJ’s email also referenced `MODEL_ID=unsloth/DeepSeek-R1-Distill-Llama-70B-GGUF` — use the **API’s** `id` from `/v1/models` in OpenClaw when wiring the gateway.

## Reported performance (JJ, 2026-04-15)

| Metric | Value |
|:-------|:------|
| Throughput (1 user) | ~14 tok/s |
| Throughput (5 concurrent) | ~40 tok/s **total** |
| TTFT (1 user) | ~5 s |
| TTFT (5 concurrent) | ~10 s |

**SLA alignment:** record your internal targets here after product review; no repo SSOT for commercial SLAs.

## Checklist

- [x] `GET /v1/models` returns 200 (verified 2026-04-24 from automation).
- [x] Set **`VLLM_SHADOW_URL`** to the **e405de** `/v1` base in `config/environments/gpu-shadow.env` (syncs via `switch-model`).
- [x] Map gateway primary to `vllm-shadow/DeepSeek-R1-Distill-Llama-70B-Q4_K_M.gguf` in `config/environments/gpu-shadow.json`.
- [x] Run `py scripts/switch-model.py gpu-shadow` and `py scripts/browser-smoke.py` (Madeira WebChat: operator spot-check in dashboard).
- [ ] Reply to JJ before **2026-05-01**: metrics feedback + go / no-go / follow-up call.

## Suggested reply (edit in your voice)

> Hi Jean-Jacques,  
> Thanks for the updated link (**e405de**) and the browser URL — we’ve wired the trial endpoint for integration tests.  
> The throughput and TTFT numbers you shared are a useful baseline; we’re mapping them to our internal latency/throughput expectations for Madeira and will come back with structured feedback before **1 May**.  
> Happy to book a short call once we’ve completed the tests.  
> Best,  
> Fayçal

---

*No API keys in this file; trial URL is vendor-provided and time-limited.*
