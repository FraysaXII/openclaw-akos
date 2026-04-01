# OpenCLAW-AKOS Architecture

## Four-Layer LLMOS Paradigm

The system decouples the reasoning engine from its tools and channels across four functional domains.

```
┌─────────────────────────────────────────────────────────┐
│                    CONTROL PLANE                        │
│              (Gateway — openclaw daemon)                │
│         Bound to 127.0.0.1:18789 (localhost)           │
│    agents.list routing · Auth · Channel multiplexing    │
├─────────────────────────────────────────────────────────┤
│                  INTEGRATION LAYER                      │
│              (Channel Adapters + MCP)                   │
│                                                         │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────────┐ │
│  │ Telegram │ │  Slack   │ │ WhatsApp │ │   A2UI    │ │
│  │  Bot     │ │ Adapter  │ │ Adapter  │ │  Canvas   │ │
│  └──────────┘ └──────────┘ └──────────┘ └───────────┘ │
├─────────────────────────────────────────────────────────┤
│                  EXECUTION LAYER                        │
│          (Multi-Agent Runner Model — v0.4.0)            │
│                                                         │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐   │
│  │ ORCHESTRATOR │ │  ARCHITECT   │ │   EXECUTOR   │   │
│  │ (Coordinator)│ │ (Planner)    │ │  (Builder)   │   │
│  └──────┬───────┘ └──────┬───────┘ └──────┬───────┘   │
│         │                │                │             │
│         │ delegates      │ Plan Document  │             │
│         ├───────────────►├───────────────►│             │
│         │                                 │             │
│         │  ┌──────────────┐               │             │
│         │  │   VERIFIER   │◄──────────────┘             │
│         │  │ (Quality     │   verify                    │
│         │  │   Gate)      │──────────────► fix loop     │
│         │  └──────────────┘                             │
│         │                                               │
├─────────────────────────────────────────────────────────┤
│                 INTELLIGENCE LAYER                       │
│          (Flat Memory Architecture — v0.4.0)             │
│                                                         │
│  ┌───────────────────────┐ ┌──────────────────────┐    │
│  │  MCP Memory Server    │ │  Workspace Files     │    │
│  │  (key-value recall)   │ │  MEMORY.md / USER.md │    │
│  └───────────────────────┘ └──────────────────────┘    │
│  ┌───────────────────────┐ ┌──────────────────────┐    │
│  │  Context Compressor   │ │  Intelligence Matrix │    │
│  │  (window management)  │ │  (fact tagging)      │    │
│  └───────────────────────┘ └──────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

## Multi-Agent Model (v0.4.0)

Forcing a single agent to simultaneously architect a solution and write the underlying syntax causes **cognitive overload**, resulting in context degradation, hallucinations, and infinite debugging loops.

The multi-agent paradigm separates concerns across four specialized roles:

### Orchestrator Agent (new in v0.3.0)

- Receives user requests and decomposes into sub-tasks
- Delegates to Architect, Executor, and Verifier
- Tracks progress, handles failures, supports parallel delegation
- **Cannot** execute tasks directly

### Architect Agent

- Operates in **read-only** mode
- Uses `sequential_thinking` MCP for structured reasoning
- Produces a plan document with explicit tool selections and risk assessments
- **Cannot** write files, execute shell commands, or make API calls

### Executor Agent

- Operates in **read-write** mode
- Reads the Architect's plan before taking any action
- Executes strict, well-scoped directives
- 3-retry error recovery loop guided by the Verifier

### Verifier Agent (new in v0.3.0)

- Validates Executor output via lint, test, build, and browser verification
- Diagnoses failures and suggests targeted fixes
- Escalates to Orchestrator after 3 failed attempts

### Agent Behavioral Protocols (new in v0.4.0)

All agents gained behavioral protocols in v0.4.0:

- **Self-Verification** -- Executor auto-verifies after every edit (lint/test); never moves to next step with failures.
- **Loop Detection** -- Orchestrator and Executor detect repetitive failures and escalate to user after 3 attempts.
- **Memory Hygiene** -- All agents proactively store decisions in MEMORY.md and via `memory_store()`.
- **Structured Planning** -- Orchestrator and Architect use conditional tasklist triggers; multi-step work produces numbered plans with checkboxes.
- **RULES.md** -- All agents read workspace `RULES.md` at session start for user-defined conventions.

### Role-Safe Capability Enforcement (new in v0.4.0)

Role safety is enforced at the configuration layer, not just by prompt instructions:

- `config/agent-capabilities.json` defines per-role tool access as a single source of truth.
- `akos/policy.py` loads the matrix and generates tool profiles.
- API endpoints `/agents/{id}/policy` and `/agents/{id}/capability-drift` provide runtime audit.

### Runtime Configuration (agents.list)

All four agents are registered in `openclaw.json` under `agents.list`:

```json
"agents": {
  "defaults": {
    "model": {
      "primary": "ollama/qwen3:8b",
      "fallbacks": ["ollama/deepseek-r1:14b", "ollama/qwen3:8b"]
    },
    "thinkingDefault": "off"
  },
  "list": [
    { "id": "orchestrator", "identity": { "name": "Orchestrator", "emoji": "🎯" } },
    { "id": "architect", "identity": { "name": "Architect", "emoji": "📐" } },
    { "id": "executor", "identity": { "name": "Executor", "emoji": "🔧" } },
    { "id": "verifier", "identity": { "name": "Verifier", "emoji": "✅" } }
  ]
}
```

Each agent has its own workspace directory and can be selected from the WebChat dashboard (`openclaw dashboard`). External channel routing via `bindings` is optional and can be layered on when channel adapters are configured.

#### Schema Corrections (learned during implementation)

The following corrections were discovered during live deployment against OpenCLAW v2026.2.26 and differ from what the SOP's original text described:

1. **`identity` is an object, not a string path.** The schema validates `identity` as `{ name, emoji, theme }` -- display metadata for the agent. Passing a file path (e.g., `"prompts/ARCHITECT_PROMPT.md"`) causes `Invalid config: expected object, received string`.

2. **System prompts go in `SOUL.md`, not `identity`.** Behavioral instructions (read-only constraints, HITL enforcement, Sequential Thinking directives) are loaded from a file named `SOUL.md` placed inside each agent's workspace directory. OpenCLAW reads this file at the start of every session. The deployed locations are:
   - `~/.openclaw/workspace-architect/SOUL.md` (copy of `prompts/ARCHITECT_PROMPT.md`)
   - `~/.openclaw/workspace-executor/SOUL.md` (copy of `prompts/EXECUTOR_PROMPT.md`)

3. **`thinkingDefault` must match model capability.** OpenCLAW defaults to `thinking: "low"` for models it classifies as reasoning-capable. Small Ollama models (e.g. `qwen3:8b`) may not support the `think` parameter, causing a 400 error. The `dev-local` profile now sets `thinkingDefault: "low"` for the medium-tier `deepseek-r1:14b` which supports reasoning. For small models, set `thinkingDefault: "off"`. Per-agent `thinkingDefault` overrides are not yet available in v2026.2.26 (tracked in [openclaw/openclaw#11479](https://github.com/openclaw/openclaw/issues/11479)).

4. **`verboseDefault: "on"` enables tool visibility in WebChat.** By default, OpenCLAW hides tool call activity from the chat surface (`verboseDefault: "off"`). When the user cannot see tool calls, web searches, or reasoning steps, the agent appears to freeze before producing a wall-of-text response. Setting `agents.defaults.verboseDefault: "on"` causes tool summaries to appear as separate bubbles in real-time. Users can override per-session with `/verbose off` or escalate to full output with `/verbose full`. Reference: [OpenCLAW Thinking Levels docs](https://docs.openclaw.ai/tools/thinking).

5. **Ollama `num_ctx` must be set explicitly.** Ollama defaults to `num_ctx=4096` tokens unless the Modelfile overrides it. Even though `openclaw.json` declares `contextWindow: 131072`, this only tells the OpenCLAW gateway the model's theoretical capacity -- it does NOT configure Ollama's actual context window. If the system prompt + SOUL.md + conversation exceeds 4K tokens, Ollama silently truncates the input, often clipping the SOUL.md behavioral instructions. Fix by creating a custom Modelfile with `PARAMETER num_ctx 16384` and rebuilding the model (`ollama create qwen3:8b -f Modelfile`). The provider-level `options` key in `openclaw.json` does not reliably pass through when using `api: "openai-completions"` (legacy; local Ollama providers now use `api: "ollama"` by default). See [openclaw/openclaw#3775](https://github.com/openclaw/openclaw/issues/3775).

6. **SOUL.md prompts must be hardened for small models.** 8B-parameter models (like `qwen3:8b`) reliably follow 3-5 key rules but degrade beyond 10. The SOUL.md prompts were compressed to under 40 lines each, using `MUST` directives with word-count limits, decision tables instead of prose, and concrete inline examples. Soft language ("should", "consider", "when appropriate") was replaced with explicit mandates. Optional features (like `sequential_thinking`) are marked as optional rather than required, since small models may fail silently when they cannot invoke a tool.

### Agent Observability

Visibility into agent activity is a core DX requirement. Without it, the user cannot distinguish between an agent that is working and one that is stuck.

#### Config: `verboseDefault`

```json
"agents": {
  "defaults": {
    "verboseDefault": "on"
  }
}
```

Verbose levels:
- `off` (default) -- hides raw tool details; only final replies are visible
- `on` -- shows tool summaries as separate bubbles when each tool starts
- `full` -- includes complete tool outputs after completion

The `/verbose` inline directive can override per-message or toggle the session default. Send `/verbose` with no argument to check the current level.

#### SOUL.md: Adaptive Response Modes

The SOUL.md prompts use an adaptive response mode pattern (inspired by Google Antigravity's `task_boundary`, Manus agent loop, Claude Code conciseness, and Traycer AI's read-only lead):

- **Conversational Mode** -- for greetings, simple questions, casual messages. Direct, concise responses with no formal structure.
- **Analysis Mode** -- for multi-step requests requiring research or reasoning. Acknowledges the request first, emits progress updates between tool calls, then produces a structured Plan Document.
- **Handoff Mode** -- when the Architect produces actionable directives for the Executor. Includes an explicit Handoff Summary so the Executor can act without reading the full reasoning trace.

#### SOUL.md: Progress Signaling

Both agents use `MUST` directives (not soft guidance) to prevent silence during multi-step operations:

- Architect: MUST emit 1-2 sentences (8-15 words) before every tool call, MUST summarize results in 1 sentence before continuing
- Executor: MUST emit 1 sentence before every action, MUST emit 1 sentence after every action
- Both: NEVER produce a tool call without preceding text

The prompts include concrete examples to anchor the model's behavior. This approach was derived from patterns in Codex CLI (for mini models) and VSCode Agent `gpt-5-mini.txt`, which demonstrated that small models follow `MUST` + word-count + examples more reliably than descriptive prose.

## Multi-Model / Multi-Environment Architecture

The system supports seamless switching between model tiers and deployment environments without code changes or prompt duplication.

### Model Tier Registry

`config/model-tiers.json` is the SSOT for model classification. Every model is assigned to exactly one tier, which determines its `thinkingDefault`, context budget, and SOUL.md prompt variant.

| Tier | Context Budget | thinkingDefault | Prompt Variant | Example Models |
|:-----|:---------------|:----------------|:---------------|:---------------|
| small | 16,384 | off | compact | ollama/qwen3:8b, ollama/llama3.2:3b |
| medium | 32,768 | low | standard | ollama/deepseek-r1:14b, groq/llama-3.3-70b |
| large | 131,072 | medium | full | anthropic/claude-sonnet-4, vllm-runpod/deepseek-r1-70b |
| sota | 200,000 | high | full | openai/gpt-5, anthropic/claude-opus-4 |

### Prompt Tiering (Base + Overlay)

SOUL.md prompts are assembled from a base file plus tier-appropriate overlays. This avoids duplication while allowing richer prompts for more capable models.

```
prompts/base/ARCHITECT_BASE.md  +  overlays/  -->  assembled/ARCHITECT_PROMPT.<variant>.md
```

| Variant | Overlays Included |
|:--------|:------------------|
| compact | None (base only -- 3-5 MUST rules for small models) |
| standard | OVERLAY_REASONING + OVERLAY_PLAN_TODOS + OVERLAY_STARTUP_COMPLIANCE |
| full | OVERLAY_REASONING + OVERLAY_PLAN_TODOS + OVERLAY_INTELLIGENCE + OVERLAY_RESEARCH + OVERLAY_CONTEXT_MANAGEMENT + OVERLAY_TOOLS_FULL + OVERLAY_STARTUP_COMPLIANCE |

Build all variants: `python scripts/assemble-prompts.py`

### Startup Compliance (Phase 10)

The gateway emits a "Post-Compaction Audit" warning when an agent fails to `read_file` its required workspace files after a session start or context reset. Base prompts now use SOTA-inspired enforcement patterns (explicit `read_file()` calls, `CRITICAL` gate, self-correction mandate) to ensure models actually execute the reads. The `OVERLAY_STARTUP_COMPLIANCE.md` overlay (medium+ tiers) adds a recency rule (re-read within 5 messages), an invariant check, and good/bad examples to prevent hallucinated "I've restored..." claims.

### Langfuse Environment Wiring

Langfuse credentials (`LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, `LANGFUSE_HOST`) are now present in all three `config/environments/*.env.example` files. `scripts/serve-api.py` loads `config/eval/langfuse.env` at startup so the `/health` endpoint accurately reports Langfuse status. `scripts/log-watcher.py` detects Post-Compaction Audit entries in gateway logs and traces them to Langfuse with a `startup_compliance` score (0.0 or 1.0). `scripts/run-evals.py` creates Langfuse scored traces for eval task results when credentials are configured.

### Multi-Provider Configuration

`openclaw.json.example` declares five provider blocks using `${VAR}` environment variable substitution:

- `ollama` -- local Ollama at 127.0.0.1:11434 (native `api: "ollama"`)
- `ollama-gpu` -- remote Ollama on a GPU server (URL from env)
- `openai` -- OpenAI API (key from env)
- `anthropic` -- Anthropic API (key from env)
- `vllm-runpod` -- vLLM endpoint on RunPod/ShadowGPU (URL from env)

### Environment Profiles

Each deployment target has a pair of files in `config/environments/`:

- `<env>.env.example` -- committed template with placeholder values for secrets
- `<env>.json` -- JSON overlay for `openclaw.json` (model, thinkingDefault, etc.)

Profiles: `dev-local` (medium/local), `gpu-runpod` (large/remote GPU), `prod-cloud` (large/cloud APIs).

### Environment Placeholder Hardening

OpenClaw's `${VAR}` substitution in `openclaw.json` crashes the gateway if an env var resolves to an empty string. All `.env.example` files now set non-empty placeholder values for inactive providers:

| Var | Placeholder | Purpose |
|:----|:------------|:--------|
| `OLLAMA_GPU_URL` | `http://localhost:11434` | Prevents empty-string crash; gateway ignores provider with placeholder URL |
| `OLLAMA_API_KEY` | `not-configured` | Satisfies `${OLLAMA_API_KEY}` substitution |
| `OPENAI_API_KEY` | `not-configured` | Satisfies `${OPENAI_API_KEY}` substitution |
| `ANTHROPIC_API_KEY` | `not-configured` | Satisfies `${ANTHROPIC_API_KEY}` substitution |
| `VLLM_RUNPOD_URL` | `http://localhost:8000/v1` | Prevents crash in serverless profile before endpoint is provisioned |

`scripts/gpu.py` enforces this via `_ensure_env_placeholders()`, which re-asserts placeholder values in `~/.openclaw/.env` after every deployment. The `_ENV_PLACEHOLDERS` dict in `gpu.py` is the SSOT for these defaults. Empty env values are also filtered during env loading (`if v:` guard on `os.environ.setdefault`).

### Model Switching Workflow

A single cross-platform command switches everything atomically:

```
python scripts/switch-model.py <env-name>
```

This copies the `.env`, deep-merges the JSON overlay, deploys the correct SOUL.md variant, and restarts the gateway. Supports `--dry-run` to preview.

### Provider Failover and Model Routing

The `agents.defaults.model` block supports a `fallbacks` list for automatic provider failover. When the primary model returns 429/500/timeout, the gateway rotates to the next entry with exponential backoff cooldown (1 min, 5 min, 25 min, 1 hour cap). Auth profile rotation is attempted first within the same provider before advancing to fallbacks.

```
Request → Model Selector → Primary Provider
                              │
                              ├─ healthy → Response
                              │
                              └─ 429/500/timeout → Cooldown → Fallback 1
                                                                │
                                                                ├─ healthy → Response
                                                                │
                                                                └─ fail → Fallback 2 → Response
```

Fallback chains per environment:
- **dev-local:** `ollama/deepseek-r1:14b` → `ollama/qwen3:8b`
- **gpu-runpod:** `vllm-runpod/deepseek-r1-70b` → `anthropic/claude-sonnet-4` → `ollama/deepseek-r1:14b`
- **prod-cloud:** `anthropic/claude-sonnet-4` → `openai/gpt-5-mini` → `vllm-runpod/deepseek-r1-70b`

### Ollama Modelfile Convention

Committed Modelfiles in `config/ollama/` define `num_ctx` and `temperature` per model. This eliminates the manual Modelfile workaround and ensures reproducible context windows.

| Modelfile | `num_ctx` | Tier | Temperature |
|:----------|:----------|:-----|:------------|
| `Modelfile.qwen3-8b` | 16,384 | small | 0.7 |
| `Modelfile.deepseek-r1-14b` | 32,768 | medium | 0.6 |

After editing a Modelfile, rebuild with `ollama create <model> -f config/ollama/<Modelfile>`.

Ollama server-level performance tuning (set in `dev-local.env.example`):
- `OLLAMA_FLASH_ATTENTION=1` — faster inference, lower VRAM, no quality loss
- `OLLAMA_KV_CACHE_TYPE=q8_0` — 8-bit KV cache quantization halves VRAM usage

### RunPod vLLM Optimization

The `gpu-runpod.json` profile includes production-grade vLLM inference settings:

| Setting | Value | Impact |
|:--------|:------|:-------|
| `KV_CACHE_DTYPE` | `fp8` | 2x KV cache capacity on A100-80GB |
| `ENABLE_PREFIX_CACHING` | `true` | Avoids recomputing 3-10K SOUL.md system prompt tokens |
| `ENABLE_CHUNKED_PREFILL` | `true` | New requests can start during prefill |
| `TOOL_CALL_PARSER` | per-model (from catalog) | Structured tool calls; parser set by `model-catalog.json` entry |
| `REASONING_PARSER` | per-model (conditional) | Chain-of-thought mapped to AKOS thinking levels; omitted for non-reasoning models |
| `CHAT_TEMPLATE` | per-model (conditional) | Custom chat template path; omitted when the model default suffices |
| `MAX_NUM_SEQS` | `128` | Lower tail latency for agent workloads |
| `MAX_MODEL_LEN` | `32768` (pod default) | Reduced from 131072 to fit 2x A100-80GB with fp8 KV cache headroom |

### Dual-Mode RunPod Architecture

RunPod deployments support two modes, selected by environment profile:

| Mode | Profile | How vLLM Runs | URL Pattern | Scaling |
|:-----|:--------|:--------------|:------------|:--------|
| **Serverless** | `gpu-runpod` | RunPod serverless endpoint | `https://api.runpod.ai/v2/{endpoint_id}/openai/v1` | Auto-scaled by RunPod |
| **Dedicated Pod** | `gpu-runpod-pod` | Persistent vLLM process on a reserved pod | `https://{pod_id}-8000.proxy.runpod.net/openai/v1` | Fixed; operator-managed |

Dedicated pod mode is configured via `PodConfig` (Pydantic model in `akos/models.py`) and provisioned by `scripts/gpu.py deploy-pod`. The container image is `vllm/vllm-openai:latest`, which has `ENTRYPOINT ["python3", "-m", "vllm.entrypoints.openai.api_server"]` -- so `dockerStartCmd` passes only vLLM CLI flags (no `python -m ...` prefix). The pod exposes an OpenAI-compatible endpoint on port 8080 via RunPod's HTTPS proxy.

`PodConfig` fields:

| Field | Default | Description |
|:------|:--------|:------------|
| `modelName` | `deepseek-ai/DeepSeek-R1-Distill-Llama-70B` | HuggingFace model ID |
| `vllmPort` | `8080` | Port inside the container |
| `gpuType` | `NVIDIA A100-SXM4-80GB` | RunPod GPU type ID |
| `gpuCount` | `2` | Number of GPUs; also sets `--tensor-parallel-size` |
| `containerImage` | `vllm/vllm-openai:latest` | Docker image with vLLM ENTRYPOINT |
| `containerDiskGb` | `100` | Container disk size (min 20 GB) |
| `volumeGb` | `200` | Persistent network volume |
| `maxModelLen` | `131072` | `--max-model-len` passed to vLLM |

`build_vllm_command()` produces CMD args (not a full command) since the image ENTRYPOINT handles the Python invocation. Dynamic flags include `--reasoning-parser` (when `REASONING_PARSER` env is set), `--chat-template` (when `CHAT_TEMPLATE` is set), and `--served-model-name` (auto-derived from `modelName.split("/")[-1]` unless overridden by `OPENAI_SERVED_MODEL_NAME_OVERRIDE`).

### Model Catalog

`config/model-catalog.json` is the SSOT for GPU-deployable models. Each entry maps a HuggingFace model ID to its VRAM footprint, recommended GPU, vLLM parser configuration, and OpenClaw served-model name. `akos/model_catalog.py` provides the Pydantic schema (`CatalogEntry`) and loader (`load_catalog()`).

| Field | Purpose |
|:------|:--------|
| `hfId` | HuggingFace model identifier (e.g., `deepseek-ai/DeepSeek-R1-Distill-Llama-70B`) |
| `displayName` | Human-readable name for the interactive picker |
| `family` | Model family (deepseek, llama, qwen, mistral, hermes) |
| `paramsBillions` | Parameter count in billions |
| `vramGb` | Minimum VRAM required to load the model |
| `toolCallParser` | vLLM `--tool-call-parser` value |
| `reasoningParser` | vLLM `--reasoning-parser` (null if model has no chain-of-thought) |
| `chatTemplate` | Custom chat template path (null to use model default) |
| `servedModelName` | Name exposed via the OpenAI-compatible API |
| `reasoning` | Whether the model produces reasoning traces |
| `defaultGpu` | `{ type, count }` -- recommended GPU configuration |
| `maxModelLen` | Default `--max-model-len` for this model |
| `envOverrides` | Additional vLLM env vars (e.g., `KV_CACHE_DTYPE`, `ENABLE_PREFIX_CACHING`) |

`CatalogEntry.min_gpus_for(gpu_vram)` computes the minimum GPU count for a given per-GPU VRAM capacity.

#### Interactive Model Picker

`scripts/gpu.py deploy-pod` uses the catalog to drive an interactive deployment flow:

```
1. _pick_model(catalog)    → user selects from numbered model list
2. _pick_gpu(model)         → GPU type/count based on model VRAM needs
3. _apply_catalog_to_pod    → overwrite PodConfig from catalog entry
4. _update_overlay_json     → rewrite gpu-runpod-pod.json to match
5. PodManager.create_pod()  → provision on RunPod
6. _save_key_to_env()       → persist VLLM_RUNPOD_URL + RUNPOD_POD_ID
7. _ensure_env_placeholders → restore gateway-required placeholder vars
```

### FailoverRouter

`akos/router.py` implements automatic provider failover for inference requests:

```
Request → FailoverRouter → Primary Provider
                              │
                              ├─ healthy → Response
                              │
                              └─ 3 consecutive failures → INFRA_FAILOVER_TRIGGERED alert
                                                          → next provider in chain
                                                            │
                                                            ├─ healthy → Response
                                                            │
                                                            └─ recovery probe → restore primary
```

- **Threshold:** 3 consecutive failures trigger failover.
- **SOC integration:** `INFRA_FAILOVER_TRIGGERED` alert fires on each failover event and is forwarded to Langfuse via `trace_alert()`.
- **Recovery:** The router periodically probes the failed provider and restores it when healthy.
- **Multi-provider:** Supports arbitrary-length fallback chains per environment.

### vLLM Health Probe

`probe_vllm_health()` performs an HTTP GET against the vLLM `/v1/models` and `/health` endpoints on dedicated pods. Requests include `User-Agent: akos-gpu-cli/1.0` and `Accept: application/json` headers for compatibility with reverse proxies and CDNs that may filter bare requests. Results are consumed by:

- `doctor.py` (`check_runpod_readiness()`) — validates config, API key presence, and live vLLM reachability.
- `/health` API — includes `vllm_status` in the response body.
- `FailoverRouter` — uses probe results to decide failover/recovery transitions.

### Langfuse Trace Taxonomy

All Langfuse traces follow a structured taxonomy with environment tagging:

| Trace Type | Function | Data |
|:-----------|:---------|:-----|
| `trace_request` | Per-inference request | Model, latency, tokens, environment |
| `trace_startup_compliance` | Post-Compaction Audit | Agent, compliance score (0.0/1.0) |
| `trace_alert` | SOC alert forwarding | Alert name, severity, context |
| `trace_metric` | DX metrics | Request counts, p50/p95 latency |

Environment tags (e.g. `gpu-runpod`, `gpu-runpod-pod`, `dev-local`) enable per-environment filtering in the Langfuse dashboard.

### Known Limitations

1. **Per-agent model override bug** ([#29571](https://github.com/openclaw/openclaw/issues/29571)): `agents.defaults.model.primary` overrides per-agent model settings at runtime, so all agents currently share the same model. Model switching must happen at the global level.
2. **Ollama `num_ctx` managed via committed Modelfiles**: The `contextWindow` declared in `openclaw.json` does not configure Ollama's actual context window. Committed Modelfiles in `config/ollama/` set `num_ctx` to match the tier's `contextBudget`. Rebuild with `ollama create` after changes.

## MCP Server Topology (v0.5.0)

Ten MCP servers provide the agent tool ecosystem:

```
                    ┌─────────────────┐
                    │  openclaw.json  │
                    │   (Gateway)     │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │    mcporter     │
                    │ (MCP Manager)   │
                    └────────┬────────┘
                             │
    ┌─────────┬──────────┬───┴───┬──────────┬─────────┐
    │         │          │       │          │         │
┌───▼───┐ ┌──▼───┐ ┌────▼──┐ ┌─▼────┐ ┌───▼──┐ ┌───▼───┐
│Seqntl │ │Play- │ │GitHub │ │Memory│ │File  │ │ Fetch │
│Think  │ │wright│ │      │ │ K-V  │ │system│ │ HTTP  │
└───────┘ └──────┘ └──────┘ └──────┘ └──────┘ └───────┘
```

| Server | Package | Purpose |
|:-------|:--------|:--------|
| sequential-thinking | `@modelcontextprotocol/server-sequential-thinking` | Structured reasoning for Architect/Orchestrator |
| playwright | `@playwright/mcp` | Browser automation and UI verification |
| github | `@modelcontextprotocol/server-github` | Repo metadata, code search |
| memory | `@modelcontextprotocol/server-memory` | Cross-session key-value recall |
| filesystem | `@modelcontextprotocol/server-filesystem` | Structured file operations |
| fetch | `@modelcontextprotocol/server-fetch` | HTTP client for API integration |
| lsp | `@akos/mcp-lsp-server` | Type-aware code navigation (go-to-definition, find-references, diagnostics) |
| code-search | `@akos/mcp-code-search` | Semantic code search via ripgrep + tree-sitter |
| akos | `scripts/mcp_akos_server.py` | Custom AKOS MCP: `akos_health`, `akos_agents`, `akos_status` (control plane self-check) |
| finance | `scripts/finance_mcp_server.py` | Finance research: `finance_quote`, `finance_search`, `finance_sentiment` (read-only, yfinance + Alpha Vantage) |

### Cursor vs AKOS Browser Separation (Platform-Agnostic Design)

AKOS is platform-agnostic. The agent has its own browser capability independent of Cursor or any IDE.

| Capability | Owner | Purpose | Required for AKOS |
|:-----------|:------|:--------|:------------------|
| **Playwright MCP** | AKOS agent | Verifier screenshots, browser automation during execution | Yes |
| **browser-smoke.py** | AKOS operator | UAT, release gate, dashboard validation | Yes |
| **cursor-ide-browser** | Cursor IDE | In-IDE WebChat testing when using Cursor | No — Cursor-only |

The AKOS agent receives browser tools via Playwright MCP in `mcporter.json`. That MCP runs in the agent runtime (OpenClaw gateway), not in the IDE. `browser-smoke.py` is a separate operator script for pre-commit and release validation. Cursor users can optionally enable the built-in cursor-ide-browser in Cursor Settings for in-IDE testing; AKOS does not require it.

## Security Architecture

```
┌──────────────────────────────────────────────┐
│              HOST OPERATING SYSTEM            │
│                                               │
│  ┌──────────────────────────────────────┐    │
│  │     ISOLATION BOUNDARY               │    │
│  │   (WSL2 / Docker Sandbox)            │    │
│  │                                       │    │
│  │  ┌────────────────────────┐          │    │
│  │  │   openclaw daemon      │          │    │
│  │  │   (openclaw user)      │          │    │
│  │  │   non-root, limited    │          │    │
│  │  └───────────┬────────────┘          │    │
│  │              │                        │    │
│  │  ┌───────────▼────────────┐          │    │
│  │  │   HITL Gate            │          │    │
│  │  │   (mutative ops only)  │          │    │
│  │  └───────────┬────────────┘          │    │
│  │              │                        │    │
│  │  ┌───────────▼────────────┐          │    │
│  │  │   skillvet Scanner     │          │    │
│  │  │   (48 vuln checks)     │          │    │
│  │  └────────────────────────┘          │    │
│  │                                       │    │
│  │  Network: localhost only ◄────────┐  │    │
│  └───────────────────────────────────┘  │    │
│                                          │    │
│  ┌──────────────────────────────────┐   │    │
│  │  Splunk Universal Forwarder      │   │    │
│  │  → SIEM (SOC Monitoring)         │   │    │
│  └──────────────────────────────────┘   │    │
│                                          │    │
│  API Keys: Host env vars only           │    │
│  (injected via Docker proxy)            │    │
└──────────────────────────────────────────┘
```

## Data Flow: Intelligence Matrix

The Intelligence Matrix is a lightweight fact-tagging pattern used by the Architect agent (via `OVERLAY_INTELLIGENCE.md`). It does not require a graph database; facts are tagged inline in the Plan Document and stored as flat JSON when persistence is needed.

1. **Ingestion** -- File upload, web scrape, or API response
2. **Fact Extraction** -- Assign unique `fct_XXX` identifiers to isolated concepts
3. **Source Credibility Scoring** -- Numerical score against an average baseline
4. **SSOT Verification** -- Mark facts as `ssot_verified: true/false`
5. **Persistence** -- Store via MCP Memory server (`memory_store`) for cross-session recall

## Orchestration Library (`akos/`)

All AKOS automation scripts share a typed Python library under `akos/`. This eliminates helper duplication, provides runtime config validation, and centralises logging, subprocess safety, and observability.

| Module | Responsibility |
|:-------|:---------------|
| `akos/models.py` | Pydantic schemas for `model-tiers.json`, `openclaw.json`, environment overlays (incl. RunPod), alerts, baselines, finance response envelope |
| `akos/model_catalog.py` | `CatalogEntry` Pydantic model + `load_catalog()` for `config/model-catalog.json`; drives the interactive GPU deploy picker |
| `akos/finance.py` | `FinanceService` — quote, search, sentiment via yfinance + Alpha Vantage; TTL cache; graceful degradation when backends are absent |
| `akos/io.py` | `load_json`, `save_json`, `deep_merge`, `resolve_openclaw_home`, `AGENT_WORKSPACES` (4-agent mapping) |
| `akos/log.py` | `JSONFormatter` + `HumanFormatter`; `setup_logging(json_output)` configures the root logger |
| `akos/process.py` | `CommandResult` dataclass + `run()` wrapper with timeouts and structured error capture |
| `akos/state.py` | `AkosState` Pydantic model tracking the active environment/model; `load_state`, `save_state`, `record_switch` |
| `akos/telemetry.py` | `LangfuseReporter` wrapping the Langfuse SDK; `trace_metric()` for DX metrics; graceful no-op when credentials are absent |
| `akos/alerts.py` | `AlertEvaluator` -- checks real-time log entries against `alerts.json` and periodic metrics against `baselines.json` |
| `akos/runpod_provider.py` | RunPod SDK wrapper: endpoint lifecycle, health checks, scaling, inference, GPU discovery (v0.3.0) |
| `akos/api.py` | FastAPI control plane: REST endpoints for health, status, switching, RunPod, metrics, alerts, checkpoints, context pinning, WebSocket logs (v0.4.0) |
| `akos/tools.py` | Dynamic tool registry reading mcporter config + permissions.json; HITL classification (v0.3.0) |
| `akos/policy.py` | Role capability matrix loader, tool profile generation, drift detection (v0.4.0) |
| `akos/router.py` | `FailoverRouter` — automatic provider failover with 3-failure threshold, recovery probe, SOC alert integration |
| `akos/checkpoints.py` | Workspace snapshot/restore via tarballs for reversible execution (v0.3.0) |

All scripts (`bootstrap.py`, `switch-model.py`, `assemble-prompts.py`, `log-watcher.py`, `gpu.py`) import from `akos/` and accept `--json-log` for structured CI output.

### Rollback Safety

`switch-model.py` wraps steps 2-4 (config merge, prompt deploy, gateway restart) in a `try/finally` block. On failure, `openclaw.json.bak` is restored automatically and a failed state is recorded. Use `--rollback` to manually restore the previous config.

### FastAPI Control Plane (v0.3.0)

The `akos/api.py` module exposes a REST API for programmatic control:

| Endpoint | Method | Purpose |
|:---------|:-------|:--------|
| `/health` | GET | Gateway + RunPod + Langfuse status |
| `/status` | GET | Current environment, model, tier, variant |
| `/switch` | POST | Trigger model/environment switch |
| `/agents` | GET | List agents with workspace paths and SOUL.md status |
| `/runpod/health` | GET | RunPod endpoint health |
| `/runpod/scale` | POST | Adjust RunPod scaling |
| `/metrics` | GET | DX baselines from Langfuse |
| `/alerts` | GET | Recent SOC alerts |
| `/prompts/assemble` | POST | Trigger prompt assembly |
| `/checkpoints` | GET/POST | Workspace snapshot management |
| `/checkpoints/restore` | POST | Restore a workspace checkpoint |
| `/runtime/drift` | GET | Runtime drift detection (repo vs live) |
| `/agents/{id}/policy` | GET | Effective capability policy for an agent |
| `/agents/{id}/capability-drift` | GET | Check tool drift against policy |
| `/context/pin` | POST/DELETE | Pin or unpin context for agent focus |
| `/context/pins` | GET | List pinned context entries |
| `/metrics/cost` | GET | Cost breakdown by agent and environment |
| `/logs` | WebSocket | Live log stream |

Launch: `python scripts/serve-api.py --port 8420`

### Operator Scripts (v0.4.0)

| Script | Purpose |
|:-------|:--------|
| `scripts/legacy/verify_openclaw_inventory.py` | Strict full-inventory verifier with per-item PASS/FAIL output (providers/models/agents/A2A allowlist) |
| `scripts/check-drift.py` | Detect repo-to-runtime mismatches |
| `scripts/doctor.py` | One-command system health check; normalizes `Runtime: unknown` to `healthy` when probe/listener evidence is healthy, and checks determinism |
| `scripts/browser-smoke.py` | Programmatic browser smoke test (6+ scenarios); HTTP-only or Playwright DOM mode via `--playwright`, with Windows worker isolation for crash-to-SKIP fallback |
| `scripts/run-evals.py` | Agent reliability eval runner (5 canonical tasks) |
| `scripts/checkpoint.py` | Checkpoint CLI (create/list/restore workspace snapshots) |
| `scripts/sync-runtime.py` | Hydrate runtime from repo SSOT |
| `scripts/release-gate.py` | Unified release gate (tests + drift + smoke) |
| `scripts/resolve-mcporter-paths.py` | Resolve MCP config placeholder paths (idempotent, cross-platform) |

### Workflow Definitions (v0.4.0)

Reusable workflow specs in `config/workflows/`:

| Workflow | Agents | Purpose |
|:---------|:-------|:--------|
| `analyze_repo` | Architect, Orchestrator | Full codebase analysis |
| `implement_feature` | Architect, Executor, Verifier | Plan + implement + verify |
| `verify_changes` | Verifier | Lint, test, build, screenshot |
| `browser_smoke` | Verifier | Dashboard browser validation |
| `deploy_check` | Architect, Verifier | Deployment readiness assessment |
| `incident_review` | Architect, Orchestrator | Root cause and remediation |

## Bootstrap Translation Layer (v0.5.0)

Bootstrap is the **bridge** between AKOS's design-time SSOT and OpenClaw's runtime enforcement. Policy is defined once in AKOS files; bootstrap pushes it to OpenClaw's config schema; the dashboard shows the live state. The operator never manually edits the OpenClaw Config page.

- **`agent-capabilities.json` → per-agent `tools.profile`**: The capability matrix defines `allowed_categories`, `allowed_tools`, and `denied_tools` per role. Bootstrap translates these into OpenClaw's `agents.list[].tools` block (profile name, allowlist, denylist).
- **Gateway-agnostic design**: If you swap OpenClaw for another gateway, you only rewrite the bootstrap translation. Prompts, policies, workflows, capability matrix, and eval gates survive unchanged.
- **Principle**: Define once in AKOS, push via bootstrap, see in dashboard.

### Runtime SSOT Chain

For runtime-facing work, AKOS uses a layered SSOT chain:

| Layer | File | Role |
|:------|:-----|:-----|
| Repo gateway intent | `config/openclaw.json.example` | Canonical gateway template in git |
| Repo MCP intent | `config/mcporter.json.example` | Canonical MCP server template in git |
| Policy/audit SSOT | `config/agent-capabilities.json` | AKOS logical role policy and drift basis |
| Translation layer | `scripts/bootstrap.py` | Converts repo intent into live runtime files |
| Live gateway runtime | `~/.openclaw/openclaw.json` | Active OpenClaw runtime consumed by the gateway |
| Live MCP runtime | `~/.mcporter/mcporter.json` | Active MCP runtime consumed by mcporter/OpenClaw |

### Tool Policy Split

The capability matrix and the gateway allowlist do not serve the same purpose:

- **`config/agent-capabilities.json`** is the AKOS-layer SSOT for audit, policy reporting, and drift detection.
- **`config/openclaw.json.example`** is the gateway-compatibility SSOT for curated `tools.allow` entries that OpenClaw actually recognizes at runtime.
- **Bootstrap** translates profile and deny semantics from the capability matrix, but preserves template-curated `allow` lists for `minimal` roles to avoid injecting AKOS-only logical tool IDs into the gateway runtime.

## AKOS / OpenClaw Responsibility Matrix

The following matrix shows every component, who owns it, and how the two layers interact.

### AKOS Layer (design-time SSOT — lives in this repo, gateway-agnostic)

| Component            | File(s)                                                                                                                          | Purpose                                                                       | Relationship to OpenClaw                                                  |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| Capability Matrix    | `config/agent-capabilities.json`                                                                                                 | Per-role tool access SSOT                                                     | Bootstrap translates to OpenClaw `tools.profile` per agent                |
| Prompt System        | `prompts/base/`, `prompts/overlays/`, `prompts/assembled/`                                                                       | SOUL.md assembly (compact/standard/full)                                      | Deployed to agent workspace dirs; OpenClaw reads SOUL.md at session start |
| Workflow Engine      | `config/workflows/*.md`                                                                                                          | Reusable task workflows (6 definitions)                                       | AKOS-only concept; OpenClaw has no native workflow engine                 |
| Policy Packs         | `config/policies/*.md`                                                                                                           | Governance profiles (engineering-safe, compliance, incident)                  | AKOS-only concept                                                         |
| Memory Templates     | `config/memory-templates/*.md`                                                                                                   | Structured memory domains (decisions, incidents, policies, sources)           | AKOS-only concept; complements OpenClaw's built-in memory                 |
| Session Templates    | `config/templates/*.md`                                                                                                         | Pre-built session starters (architecture review, bug investigation, refactor) | AKOS-only concept                                                         |
| Workspace Scaffold   | `config/workspace-scaffold/`                                                                                                    | Agent identity, memory, heartbeat, rules files                                | Bootstrap deploys to `~/.openclaw/workspace-{agent}/`                     |
| RULES.md             | `config/workspace-scaffold/*/RULES.md`                                                                                           | User-customizable per-agent rules                                             | Deployed to workspace; agent reads at session start via SOUL.md directive |
| Policy Engine        | `akos/policy.py`                                                                                                                | Load matrix, generate profiles, check drift                                   | Feeds bootstrap translation; provides `/agents/{id}/policy` API           |
| Control Plane API    | `akos/api.py`                                                                                                                   | REST API (health, agents, drift, policy, context, metrics, checkpoints)       | Runs alongside OpenClaw gateway on port 8420                              |
| Telemetry            | `akos/telemetry.py`                                                                                                             | Langfuse integration, DX metrics                                              | Complements OpenClaw's built-in OpenTelemetry                             |
| Alert Engine         | `akos/alerts.py`                                                                                                                | SOC alerts from log patterns and baselines                                    | Processes OpenClaw gateway logs                                           |
| Model Catalog        | `akos/model_catalog.py`, `config/model-catalog.json`                                                                             | SSOT for GPU-deployable models (VRAM, parsers, GPU defaults)                   | `gpu.py` uses catalog to auto-configure PodConfig and overlay JSON         |
| Finance Service      | `akos/finance.py`, `scripts/finance_mcp_server.py`                                                                               | Read-only finance research (quotes, search, sentiment) via yfinance + Alpha Vantage | MCP server registered in mcporter; agents invoke tools autonomously        |
| RunPod Provider      | `akos/runpod_provider.py`                                                                                                       | GPU infrastructure lifecycle                                                  | Manages vLLM endpoints; OpenClaw uses them via `vllm-runpod` provider     |
| Checkpoints          | `akos/checkpoints.py`                                                                                                           | Workspace snapshot/restore                                                    | AKOS-only concept; operates on workspace dirs                             |
| Tool Registry        | `akos/tools.py`                                                                                                                 | Dynamic tool inventory from mcporter + permissions                            | AKOS-layer classification of MCP tools                                    |
| State Tracking       | `akos/state.py`                                                                                                                 | Deployment state (active env, model, tier)                                    | AKOS-only; tracks switch-model history                                    |
| Operator Scripts     | `scripts/doctor.py`, `gpu.py`, `sync-runtime.py`, `release-gate.py`, `check-drift.py`, `browser-smoke.py`, `run-evals.py`, `checkpoint.py` | Health, GPU deploy, sync, release, drift, smoke, eval, checkpoint CLIs         | AKOS-only operator tooling                                                |
| Bootstrap            | `scripts/bootstrap.py`                                                                                                          | **Translation layer** — converts AKOS SSOT to OpenClaw config                 | The bridge; rewrites `~/.openclaw/openclaw.json` from AKOS sources        |
| Test Suite           | `tests/` (300+ tests)                                                                                                           | Config validation, Pydantic models, API, prompts, E2E, telemetry, router, live smoke, evals | AKOS quality gates                                                        |
| Compliance           | `config/compliance/eu-ai-act-checklist.json`                                                                                     | EU AI Act evidence map                                                        | AKOS-only governance                                                      |
| Model Tiers          | `config/model-tiers.json`                                                                                                       | Model classification (small/medium/large/sota)                                | Drives prompt variant selection; OpenClaw uses the selected model         |
| Environment Profiles | `config/environments/*.json` + `*.env.example`                                                                                   | Multi-environment config (dev-local, gpu-runpod, prod-cloud)                  | Merged into OpenClaw config by `switch-model.py`                          |
| Eval Configs         | `config/eval/alerts.json`, `baselines.json`                                                                                      | SOC thresholds, DX metrics                                                    | AKOS-only evaluation framework                                            |

### OpenClaw Layer (runtime enforcement — configured by bootstrap, visible in dashboard)

| Feature                 | Config Key                            | Purpose                                            | How AKOS Interacts                                         |
| ----------------------- | ------------------------------------- | -------------------------------------------------- | ---------------------------------------------------------- |
| Gateway Daemon          | `gateway.port`, `gateway.bind`        | WebSocket + HTTP control                           | AKOS API probes health via `/api/health`                   |
| Agent Registry          | `agents.list[]`                       | Agent definitions (id, name, workspace, identity)  | Bootstrap force-syncs from `openclaw.json.example`         |
| Per-Agent Tool Profiles | `agents.list[].tools.profile`          | Runtime tool access enforcement                    | **Translated from `agent-capabilities.json` by bootstrap**  |
| Exec Security           | `tools.exec.security`                 | Shell command approval mode                        | Bootstrap sets per AKOS policy (deny/allowlist/full)        |
| Loop Detection          | `tools.loopDetection.*`               | Gateway-level repetition circuit breaker            | Defense-in-depth with AKOS prompt-level loop detection     |
| Agent-to-Agent          | `tools.agentToAgent.*`                | Gateway-native inter-agent calls                    | Enables Orchestrator delegation at runtime level           |
| Session Policy          | `session.reset.*`, `session.typingMode` | Session reset, typing indicators                | Bootstrap configures idle timeout and typing mode           |
| Browser Control         | `browser.*`                           | Browser automation, SSRF policy                    | Bootstrap sets headless mode and SSRF restrictions         |
| Message Reactions       | `messages.statusReactions.*`           | Lifecycle emoji on messages (queued/thinking/done)  | Bootstrap enables for UX                                  |
| Model Providers         | `models.providers.*`                  | LLM provider routing and failover                  | Bootstrap preserves full provider inventory; unresolved env inputs are surfaced as warnings |
| Channel Routing         | `bindings[]`                          | Route channels to agents                            | Defined in template; future expansion                      |
| MCP Servers             | via mcporter.json                     | Tool servers (10 total)                            | Bootstrap generates resolved paths                        |
| WebChat                 | `web.enabled`                         | Dashboard chat interface                            | Always enabled for AKOS                                    |
| Built-in Memory         | `memory.backend`                      | Native session memory                              | Complements AKOS MCP Memory + workspace MEMORY.md          |
| OpenTelemetry           | `diagnostics.openTelemetry.*`         | Traces/metrics export                               | Future: wire to Langfuse OTEL endpoint                     |
| Skills                  | `skills.*`                            | ClawHub skill management                           | Not managed by AKOS (future consideration)                 |
| Plugins                 | `plugins.*`                           | Extension plugins                                   | Not managed by AKOS (future consideration)                 |
| Cron Jobs               | `cron.*`                              | Scheduled automation                               | Not managed by AKOS (future consideration)                 |
| Hooks                   | `hooks.*`                             | Webhook/event handlers                             | Not managed by AKOS (future consideration)                 |

## Observability Stack

### Pipeline

```
log-watcher.py ──> Langfuse       (primary: per-request traces, model comparison, cost)
               ├─> AlertEvaluator (real-time SOC alerts → CRITICAL-level log entries)
               └─> stdout         (human-readable or JSON, always available)

Splunk UF (optional) ──> ai_agent_ops index (enterprise SIEM, config/splunk/inputs.conf)
```

### Components

| Component | Role | Target |
|:----------|:-----|:-------|
| Structured JSON Logs | Agent activity tracing | `$TEMP/openclaw/` (dev) or `/opt/openclaw/logs/` (prod) |
| `akos/log.py` | Script-level JSON logging | stdout (human or JSON mode) |
| `scripts/log-watcher.py` | Tails gateway logs, pushes traces to Langfuse, evaluates real-time alerts | Langfuse Cloud / stdout |
| `akos/alerts.py` (AlertEvaluator) | Real-time pattern matching against `alerts.json`; periodic baseline checks | `CRITICAL`-level log entries |
| Langfuse (primary) | Agent telemetry, tracing, model comparison | `config/eval/langfuse.env` (keys from `.example`) |
| Splunk Universal Forwarder (optional) | Enterprise SIEM log shipping | `ai_agent_ops` index |
| skillvet | Security posture | Prompt-injection vulnerability rate |

Langfuse is the recommended primary observability backend. The `--env-file` flag on `log-watcher.py` loads credentials from `config/eval/langfuse.env` (gitignored). Use `--dry-run` to preview traces without sending. Splunk is available for enterprise deployments that require a full SIEM; the `inputs.conf` template needs path adjustment for the target OS.

## Implementation Task Map

The [SOP Section 8.0](SOP.md#80-implementation-task-registry) decomposes the architecture into 33 individually traceable tasks across 6 phases. Each phase maps to the LLMOS layers it implements:

| Phase | SOP Section | LLMOS Layers | Category | Tasks |
|:------|:------------|:-------------|:---------|:------|
| **Phase 0** — Environment Assessment | 3.0 | Control Plane | `ENV` | T-0.1 through T-0.6 |
| **Phase 1** — Configuration Bootstrapping | 4.1–4.2 | Control Plane, Integration | `CONFIG` | T-1.1 through T-1.5 |
| **Phase 2** — MCP Provisioning | 5.1–5.6 | Integration, Execution | `MCP` | T-2.1 through T-2.11 |
| **Phase 3** — Security Implementation | 6.1–6.3 | All | `SECURITY`, `LOGGING` | T-3.1 through T-3.7 |
| **Phase 4** — Multi-Agent Prompt Engineering | 2.0, 5.2 | Execution, Intelligence | `PROMPT` | T-4.1 through T-4.6 |
| **Phase 5** — Observability and DX Metrics | 7.0 | All | `METRIC`, `LOGGING` | T-5.1 through T-5.5 |

Every task carries SSOT traceability (Task ID), SOC relevance tagging, HITL gate classification, and a verification command. See the full registry for details.

## Implementation Scaffolding

The following files implement the architecture described above as committable configuration templates, prompt definitions, and security scripts. Each file traces to a specific task in the [SOP task registry](SOP.md#80-implementation-task-registry).

| LLMOS Layer | File | SOP Task |
|:------------|:-----|:---------|
| Control Plane | [`config/openclaw.json.example`](../config/openclaw.json.example) | T-1.2 |
| Control Plane | [`config/model-tiers.json`](../config/model-tiers.json) | T-5.4 |
| Control Plane | [`config/model-catalog.json`](../config/model-catalog.json) | GPU model SSOT |
| Control Plane | [`config/ollama/`](../config/ollama/) | T-9.1 |
| Integration | [`config/mcporter.json.example`](../config/mcporter.json.example) | T-2.3–T-2.6 |
| All | [`config/permissions.json`](../config/permissions.json) | T-3.3 |
| All | [`config/logging.json`](../config/logging.json) | T-3.5 |
| All | [`config/splunk/inputs.conf`](../config/splunk/inputs.conf) | T-3.6 |
| Intelligence | [`config/intelligence-matrix-schema.json`](../config/intelligence-matrix-schema.json) | T-4.3 |
| Execution | [`prompts/ARCHITECT_PROMPT.md`](../prompts/ARCHITECT_PROMPT.md) | T-4.1 |
| Execution | [`prompts/EXECUTOR_PROMPT.md`](../prompts/EXECUTOR_PROMPT.md) | T-4.2 |
| Execution | [`prompts/base/`](../prompts/base/) | T-4.1–T-4.2 |
| Execution | [`prompts/overlays/`](../prompts/overlays/) | T-4.1–T-4.2 |
| All | [`scripts/vet-install.sh`](../scripts/vet-install.sh) | T-3.2 |
| All | [`scripts/bootstrap.py`](../scripts/bootstrap.py) | T-1.1 |
| All | [`scripts/assemble-prompts.py`](../scripts/assemble-prompts.py) | T-5.4 |
| All | [`scripts/switch-model.py`](../scripts/switch-model.py) | T-5.4 |
| All | [`scripts/log-watcher.py`](../scripts/log-watcher.py) | T-5.4–T-5.5 |
| All | [`akos/`](../akos/) | Orchestration library (models, model_catalog, I/O, logging, process, state, telemetry, alerts) |
| All | [`scripts/gpu.py`](../scripts/gpu.py) | GPU infrastructure CLI (deploy-pod, teardown, health, status) |
| All | [`config/compliance/eu-ai-act-checklist.json`](../config/compliance/eu-ai-act-checklist.json) | T-3.7 |
| All | [`config/eval/baselines.json`](../config/eval/baselines.json) | T-5.2 |
| All | [`config/eval/alerts.json`](../config/eval/alerts.json) | T-5.3 |
| All | [`config/eval/langfuse.env.example`](../config/eval/langfuse.env.example) | T-5.1 |
| All | [`config/environments/`](../config/environments/) | T-5.4 |

A validation test suite (`tests/`) provides 300+ automated checks covering JSON integrity, Pydantic model validation, cross-file reference consistency, alert evaluation, secret scanning, SOP task coverage, RunPod provider operations, FastAPI endpoints, workspace checkpoints, Langfuse telemetry (14 tests), failover router (10 tests), finance service behavior, and GPU deploy UX.

## Live Configuration Status

The multi-agent architecture (Orchestrator, Architect, Executor, Verifier) has been wired into the live `~/.openclaw/openclaw.json` using the native `agents.list` schema. All four agents are accessible via `openclaw dashboard` (WebChat). A backup of the original config exists at `~/.openclaw/openclaw.json.bak`.

To disconnect the AKOS architecture from OpenCLAW:
1. Restore backup: copy `openclaw.json.bak` over `openclaw.json`
2. Optionally remove `~/.mcporter/mcporter.json` to disable MCP servers
3. Restart: `openclaw restart`

## References

- Implementation task registry: [SOP.md Section 8.0](SOP.md#80-implementation-task-registry)
- Full SOP (sections 1.0–7.0): [SOP.md](SOP.md)
- Security controls: [SECURITY.md](../SECURITY.md)
- EU AI Act compliance evidence: [`config/compliance/eu-ai-act-checklist.json`](../config/compliance/eu-ai-act-checklist.json)
