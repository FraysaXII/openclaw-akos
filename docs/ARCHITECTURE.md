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

The multi-agent paradigm separates concerns across five specialized roles:

### Madeira Agent (new in v0.6.0)

- **User-facing operational assistant** for the Holistika knowledge vault
- Operates in **read-only lookup** mode -- answers HLK questions directly using `hlk_*` tools and a deterministic exact-lookup -> ranked-search ladder
- Default dashboard entrypoint for end-user HLK usage
- Escalates multi-step administrative tasks (`admin_escalate`) and coding/browser/MCP execution intents (`execution_escalate`) to the Orchestrator for swarm handoff
- Uses a **minimal** gateway profile with curated `alsoAllow` for `read`, memory lookups, `sequential_thinking` (post-tool reasoning only), read-only browser observation tools (`browser_snapshot`, `browser_screenshot`), HLK/finance runtime tools, and explicit `deny` for write/edit/exec (coarse `browser` navigate/click remains off-template; mutating browser tools stay out of `alsoAllow`)
- **Compact tier:** `config/model-tiers.json` applies `OVERLAY_HLK_COMPACT.md` and `OVERLAY_STARTUP_COMPACT.md` to Madeira only when `promptVariant` is `compact`, preserving HLK and startup invariants on small models within `bootstrapMaxChars`
- **Cannot** write files, execute commands, or navigate browsers

### Orchestrator Agent (new in v0.3.0)

- Receives user requests and decomposes into sub-tasks
- Delegates to Architect, Executor, and Verifier
- Tracks progress, handles failures, supports parallel delegation
- **Cannot** execute tasks directly -- coordinator role only

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
- Uses the `coding` profile with explicit `browser` exposure plus write/edit/apply_patch denies

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

All five agents are registered in `openclaw.json` under `agents.list`:

```json
"agents": {
  "defaults": {
    "model": {
      "primary": "ollama/deepseek-r1:14b",
      "fallbacks": ["ollama/qwen3:8b"]
    },
    "thinkingDefault": "low"
  },
  "list": [
    { "id": "madeira", "identity": { "name": "Madeira", "emoji": "🌊" } },
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

2. **System prompts go in `SOUL.md`, not `identity`.** Behavioral instructions (read-only constraints, HITL enforcement, Sequential Thinking directives) are loaded from a file named `SOUL.md` placed inside each agent's workspace directory. OpenCLAW reads this file at the start of every session. The deployed locations include:
   - `~/.openclaw/workspace-madeira/SOUL.md` (copy of `prompts/MADEIRA_PROMPT.md`)
   - `~/.openclaw/workspace-orchestrator/SOUL.md` (copy of `prompts/ORCHESTRATOR_PROMPT.md`)
   - `~/.openclaw/workspace-architect/SOUL.md` (copy of `prompts/ARCHITECT_PROMPT.md`)
   - `~/.openclaw/workspace-executor/SOUL.md` (copy of `prompts/EXECUTOR_PROMPT.md`)
   - `~/.openclaw/workspace-verifier/SOUL.md` (copy of `prompts/VERIFIER_PROMPT.md`)

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
| standard | OVERLAY_REASONING + OVERLAY_PLAN_TODOS + OVERLAY_STARTUP_COMPLIANCE + OVERLAY_HLK |
| full | OVERLAY_REASONING + OVERLAY_PLAN_TODOS + OVERLAY_INTELLIGENCE + OVERLAY_RESEARCH + OVERLAY_CONTEXT_MANAGEMENT + OVERLAY_TOOLS_FULL + OVERLAY_STARTUP_COMPLIANCE + OVERLAY_HLK |

Build all variants: `python scripts/assemble-prompts.py`

### Startup Compliance (Phase 10)

The gateway emits a "Post-Compaction Audit" warning when an agent fails to `read` its required workspace files after a session start or context reset. Base prompts now use SOTA-inspired enforcement patterns (explicit `read()` calls, `CRITICAL` gate, self-correction mandate) to ensure models actually execute the reads. The `OVERLAY_STARTUP_COMPLIANCE.md` overlay (medium+ tiers) adds a recency rule (re-read within 5 messages), an invariant check, and good/bad examples to prevent hallucinated "I've restored..." claims. Bootstrap also seeds dated continuity notes under `workspace-*/memory/YYYY-MM-DD.md` so post-compaction recovery has a deterministic file path instead of depending on ad-hoc model behavior.

### Langfuse Environment Wiring

Langfuse credentials (`LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, `LANGFUSE_HOST`) are present in the real profile env files under `config/environments/*.env`, while `.env.example` files remain reference-only. The single live secret authority is `~/.openclaw/.env` (or exported process env). Non-secret watcher settings live in `config/openclaw.json.example` under `diagnostics.logWatcher` and are written to `~/.openclaw/akos-config.json`. `scripts/serve-api.py`, `scripts/log-watcher.py`, `scripts/run-evals.py`, `scripts/test-langfuse-trace.py`, `scripts/doctor.py`, and `scripts/gpu.py` all resolve runtime secrets from process env first, then `~/.openclaw/.env`. `scripts/log-watcher.py` detects Post-Compaction Audit entries, reviews Madeira session transcripts for answer-quality events, sends both to Langfuse, and mirrors answer-quality records locally under `~/.openclaw/telemetry/`.

### Multi-Provider Configuration

`openclaw.json.example` declares six provider blocks using `${VAR}` environment variable substitution:

- `ollama` -- local Ollama at 127.0.0.1:11434 (native `api: "ollama"`)
- `ollama-gpu` -- remote Ollama on a GPU server (URL from env)
- `openai` -- OpenAI API (key from env)
- `anthropic` -- Anthropic API (key from env)
- `vllm-runpod` -- vLLM endpoint on RunPod (URL from env)
- `vllm-shadow` -- vLLM endpoint on ShadowPC OpenStack (URL from env)

### Environment Profiles

Each deployment target has a committed runtime profile in `config/environments/` plus an optional reference template:

- `<env>.env` -- operative env profile consumed by runtime paths and `switch-model.py`
- `<env>.env.example` -- reference template only
- `<env>.json` -- JSON overlay for `openclaw.json` (model, thinkingDefault, etc.)

Profiles: `dev-local` (medium/local), `gpu-runpod` (large/RunPod serverless), `gpu-runpod-pod` (large/RunPod dedicated), `gpu-shadow` (large/ShadowPC OpenStack), `prod-cloud` (large/cloud APIs).

### Environment Placeholder Hardening

OpenClaw's `${VAR}` substitution in `openclaw.json` crashes the gateway if an env var resolves to an empty string. AKOS now keeps a shared runtime placeholder contract and materializes non-empty placeholder values into real env files:

| Var | Placeholder | Purpose |
|:----|:------------|:--------|
| `OLLAMA_GPU_URL` | `http://localhost:11434` | Prevents empty-string crash; gateway ignores provider with placeholder URL |
| `OLLAMA_API_KEY` | `not-configured` | Satisfies `${OLLAMA_API_KEY}` substitution |
| `OPENAI_API_KEY` | `not-configured` | Satisfies `${OPENAI_API_KEY}` substitution |
| `ANTHROPIC_API_KEY` | `not-configured` | Satisfies `${ANTHROPIC_API_KEY}` substitution |
| `VLLM_RUNPOD_URL` | `http://localhost:8000/v1` | Prevents crash in serverless profile before endpoint is provisioned |
| `VLLM_SHADOW_URL` | `http://localhost:8080/v1` | Prevents crash before a Shadow instance publishes a floating-IP endpoint |

`scripts/bootstrap.py` seeds `~/.openclaw/.env` from the shared runtime placeholder contract on first run, and `scripts/gpu.py` re-asserts missing placeholders after GPU deployments. Empty env values are also filtered during env loading (`if v:` guard on `os.environ.setdefault`).

### Model Switching Workflow

A single cross-platform command switches everything atomically:

```
python scripts/switch-model.py <env-name>
```

This copies the `.env`, deep-merges the JSON overlay, deploys the correct SOUL.md variant, and restarts the gateway. Supports `--dry-run` to preview.

### Windows gateway supervision and port recovery

Native Windows OpenClaw installs rely on a Scheduled Task supervisor. When `gateway stop` leaves an orphan Node process holding `127.0.0.1:18789`, the next start fails with port-in-use errors. `akos.runtime.recover_gateway_service()` chains upstream `openclaw doctor --repair --yes`, `gateway stop`, **Windows-only** parsing of `netstat -ano` plus `taskkill` for listeners on port 18789, then `gateway start` (with a restart fallback). Operators should use `py scripts/doctor.py --repair-gateway` as the single supported entrypoint; `scripts/switch-model.py` calls the same recovery path after merges. Re-installing the scheduled task (`openclaw gateway install --force`) may still require an elevated shell when Windows denies task registration.

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

Ollama server-level performance tuning (set in `dev-local.env`):
- `OLLAMA_FLASH_ATTENTION=1` — faster inference, lower VRAM, no quality loss
- `OLLAMA_KV_CACHE_TYPE=q8_0` — 8-bit KV cache quantization halves VRAM usage

### RunPod vLLM Optimization

The `gpu-runpod.json` profile includes production-grade vLLM inference settings:

| Setting | Value | Impact |
|:--------|:------|:-------|
| `KV_CACHE_DTYPE` | `auto` (RunPod worker default) | Avoids FlashInfer JIT startup failures on workers without `nvcc` |
| `VLLM_ATTENTION_BACKEND` | `TRITON_ATTN` | Forces non-JIT attention backend for deterministic startup on RunPod worker images |
| `DTYPE` (AWQ models) | `float16` | Required for stable AWQ startup on RunPod worker-v1-vllm |
| `ENABLE_PREFIX_CACHING` | `true` | Avoids recomputing 3-10K SOUL.md system prompt tokens |
| `ENABLE_CHUNKED_PREFILL` | `true` | New requests can start during prefill |
| `TOOL_CALL_PARSER` | per-model (from catalog) | Structured tool calls; parser set by `model-catalog.json` entry |
| `REASONING_PARSER` | per-model (conditional) | Chain-of-thought mapped to AKOS thinking levels; omitted for non-reasoning models |
| `CHAT_TEMPLATE` | per-model (conditional) | Custom chat template path; omitted when the model default suffices |
| `MAX_NUM_SEQS` | `64` | Lower tail latency and reduced startup pressure for 70B AWQ workers |
| `MAX_MODEL_LEN` | `32768` (pod default) | Reduced from 131072 to fit 2x A100-80GB with fp8 KV cache headroom |

### Multi-Provider GPU Architecture

GPU inference deployments support three modes across two providers, selected by environment profile:

| Mode | Profile | Provider | How vLLM Runs | URL Pattern | Scaling |
|:-----|:--------|:---------|:--------------|:------------|:--------|
| **Serverless** | `gpu-runpod` | RunPod | RunPod serverless endpoint | `https://api.runpod.ai/v2/{endpoint_id}/openai/v1` | Auto-scaled by RunPod |
| **Dedicated Pod** | `gpu-runpod-pod` | RunPod | Persistent vLLM process on a reserved pod | `https://{pod_id}-8080.proxy.runpod.net/v1` | Fixed; operator-managed |
| **OpenStack Instance** | `gpu-shadow` | ShadowPC | vLLM via cloud-init on OpenStack GPU instance | `http://{floating_ip}:8080/v1` | Fixed; operator-managed |

ShadowPC instances use `OpenStackProvider` (`akos/openstack_provider.py`) with the `openstacksdk` Python SDK. The provider handles Keystone auth, Nova instance lifecycle, optional Neutron security groups, floating IP assignment, and spot termination detection (via instance metadata `cloud_termination_time`). Config is in `OpenStackInstanceConfig` (Pydantic model in `akos/models.py`). On policy-restricted tenants, explicit security-group creation may be forbidden; AKOS now tolerates that by omitting explicit group attachment and relying on project defaults when necessary.

Dedicated pod mode is configured via `PodConfig` (Pydantic model in `akos/models.py`) and provisioned by `scripts/gpu.py deploy-pod`. The container image is `vllm/vllm-openai:v0.16.0`, which has `ENTRYPOINT ["python3", "-m", "vllm.entrypoints.openai.api_server"]` -- so `dockerStartCmd` passes only vLLM CLI flags (no `python -m ...` prefix). The pod exposes an OpenAI-compatible endpoint on port 8080 via RunPod's HTTPS proxy.

`PodConfig` fields:

| Field | Default | Description |
|:------|:--------|:------------|
| `modelName` | `deepseek-ai/DeepSeek-R1-Distill-Llama-70B` | HuggingFace model ID |
| `vllmPort` | `8080` | Port inside the container |
| `gpuType` | `NVIDIA A100-SXM4-80GB` | RunPod GPU type ID |
| `gpuCount` | `2` | Number of GPUs; also sets `--tensor-parallel-size` |
| `containerImage` | `vllm/vllm-openai:v0.16.0` | Docker image with vLLM ENTRYPOINT |
| `containerDiskGb` | `100` | Container disk size (min 20 GB) |
| `volumeGb` | `200` | Persistent network volume |
| `maxModelLen` | `131072` | `--max-model-len` passed to vLLM |

`build_vllm_command()` produces CMD args (not a full command) since the image ENTRYPOINT handles the Python invocation. Dynamic flags include `--quantization` (when `QUANTIZATION` env is set, e.g. `awq`), `--enforce-eager` (when `ENFORCE_EAGER` is `true`), `--max-num-batched-tokens` (when set), `--reasoning-parser` (when `REASONING_PARSER` env is set), `--chat-template` (when `CHAT_TEMPLATE` is set), and `--served-model-name` (auto-derived from `modelName.split("/")[-1]` unless overridden by `OPENAI_SERVED_MODEL_NAME_OVERRIDE`). The same command builder is used for both RunPod pods and ShadowPC instances (via cloud-init user-data).

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
| `quantization` | Weight quantization method (`awq`, `gptq`, `fp8`, `bitsandbytes`, or null for none) |
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

### Langfuse metadata contract (SOC / SSOT)

Optional dimensions are validated in `akos.models.LangfuseTraceContext` and merged into every `LangfuseReporter.trace_*` path after base fields (`environment`, `agent_role`, `tool_name`, metric fields, and so on). Metadata keys are normalized to lowercase alphanumeric plus underscore (max 64 characters); values are coerced to strings (max 200 characters). **Do not place in Langfuse metadata:** secrets, API keys, prompts, full gateway transcripts, CSV row payloads, or other high-sensitivity payloads.

| Key | Meaning | Example values |
|:----|:--------|:---------------|
| `eu_aia_req` | Pointer to EU AI Act checklist requirement id | `EU-AIA-1` |
| `hlk_surface` | Where the observation originated | `log_watcher`, `gateway_chat`, `mcp`, `rest_api`, `none` |
| `hlk_tool` | HLK tool id when known (name only; no tool arguments) | `hlk_role` |
| `compliance_family` | Evidence family (categorical) | `hlk_csv`, `vault_doc`, `none` |

The FastAPI control plane does **not** emit per-request Langfuse spans today; gateway traffic is mirrored through `scripts/log-watcher.py`, which supplies `hlk_surface=log_watcher` and `eu_aia_req=EU-AIA-1` on its trace paths. Any future `/hlk/*` or REST tracing must reuse `LangfuseTraceContext` rather than ad hoc key names.

**Volume control:** unset or `LANGFUSE_TRACE_SAMPLE_RATE=1` (default) retains full fidelity. Values in `0.0`–`1.0` probabilistically drop trace roots at the reporter (intended for load tests or deliberate prod sampling with operator awareness).

**Eval and datasets:** use Langfuse UI filters on tags (for example `answer-quality`, agent role tags) plus the metadata keys above. For scripted trace-id collection see `scripts/langfuse_list_traces_by_tag.py`.

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
| hlk | `scripts/hlk_mcp_server.py` | HLK vault registry: `hlk_role`, `hlk_role_chain`, `hlk_area`, `hlk_process`, `hlk_process_tree`, `hlk_projects`, `hlk_gaps`, `hlk_search` (read-only) |

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
| `akos/models.py` | Pydantic schemas for `model-tiers.json`, `openclaw.json`, environment overlays (RunPod, OpenStack), alerts, baselines, finance response envelope, HLK domain models |
| `akos/model_catalog.py` | `CatalogEntry` Pydantic model + `load_catalog()` for `config/model-catalog.json`; drives the interactive GPU deploy picker |
| `akos/finance.py` | `FinanceService` — quote, search, sentiment via yfinance + Alpha Vantage; TTL cache; graceful degradation when backends are absent |
| `akos/hlk.py` | `HlkRegistry` — typed lookups over the HLK canonical vault CSVs (org roles, process items, gap detection, fuzzy search); lazy singleton; `HlkResponse` envelope |
| `akos/io.py` | `load_json`, `save_json`, `deep_merge`, `resolve_openclaw_home`, `AGENT_WORKSPACES` (5-agent mapping) |
| `akos/log.py` | `JSONFormatter` + `HumanFormatter`; `setup_logging(json_output)` configures the root logger |
| `akos/process.py` | `CommandResult` dataclass + `run()` wrapper with timeouts and structured error capture |
| `akos/state.py` | `AkosState` Pydantic model tracking the active environment/model; `load_state`, `save_state`, `record_switch` |
| `akos/telemetry.py` | `LangfuseReporter` wrapping the Langfuse SDK; `trace_metric()` for DX metrics; graceful no-op when credentials are absent |
| `akos/alerts.py` | `AlertEvaluator` -- checks real-time log entries against `alerts.json` and periodic metrics against `baselines.json` |
| `akos/runpod_provider.py` | RunPod SDK wrapper: endpoint lifecycle, health checks, scaling, inference, GPU discovery (v0.3.0) |
| `akos/openstack_provider.py` | ShadowPC OpenStack SDK wrapper: Keystone auth, Nova instance lifecycle, Neutron security groups, floating IPs, spot termination detection, vLLM cloud-init deployment |
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
| `/agents/{id}/capability-drift` | GET | Return live agent-specific drift issues from repo vs runtime checks |
| `/hlk/roles` | GET | All HLK baseline organisation roles |
| `/hlk/roles/{name}` | GET | Single role lookup |
| `/hlk/roles/{name}/chain` | GET | Reports-to chain traversal to Admin |
| `/hlk/areas` | GET | Area summary with role counts |
| `/hlk/areas/{area}` | GET | Roles in a given area |
| `/hlk/processes` | GET | Project summary (11 top-level projects) |
| `/hlk/processes/{id}` | GET | Single process item by ID |
| `/hlk/processes/id/{item_id}/tree` | GET | Direct children where `item_parent_1_id` matches the parent `item_id` |
| `/hlk/processes/{name}/tree` | GET | Direct children of a process item by parent `item_name` |
| `/hlk/gaps` | GET | Gap report (missing metadata, TBD owners) |
| `/hlk/search?q=` | GET | Fuzzy search across roles and processes |
| `/context/pin` | POST/DELETE | Pin or unpin context for agent focus |
| `/context/pins` | GET | List pinned context entries |
| `/metrics/cost` | GET | Cost breakdown by agent and environment |
| `/logs` | WebSocket | Live log stream |

The current HLK registry baseline exposes 11 projects and 1,065 registered items, including founder-governance processes under Legal, Finance, and Compliance for entity formation, founder funding, startup-certification readiness, and trademark/naming control, plus the GTM/Trello-harmonized operating tree merged from the MADEIRA planning candidate (Tier C backlog rows excluded). GTM leaves sit under English **cluster** process rows (`gtm_cl_*`) between workstreams and tasks; see `scripts/refine_gtm_process_hierarchy.py`. Optional **program** workstreams (`hlk_prog_*`) may sit between selected projects and their MADEIRA / Think Big GTM workstreams; see `scripts/migrate_process_list_program_layer.py`. The same CSV may include **`item_parent_1_id`** and **`item_parent_2_id`** (stable parent `item_id` pointers) dual-written with **`item_parent_1`** / **`item_parent_2`** names; see `scripts/backfill_process_parent_ids.py` and `scripts/validate_hlk.py`.

The founder-governance lower layer uses a staged document model to stay scalable: evidence and redacted synthesis live in `docs/wip/`, case-specific canonical notes live under role-owned `v3.0/` folders, repeatable procedures become SOPs, and only the repeatable process layer is registered in `process_list.csv`. This separation keeps founder-specific or potentially sensitive material out of the runtime registry while preserving a reusable operating model for future entity work.

**HLK governed KM (Topic–Fact–Source):** Canonical rules for sources, facts, topics, output types 0–4, and Output 1 (visual) manifests live in `docs/references/hlk/compliance/HLK_KM_TOPIC_FACT_SOURCE.md`. Binary visuals ship under `docs/references/hlk/v3.0/_assets/<topic_id>/` with `*.manifest.md` sidecars. Operators validate manifest shape and raster paths with `scripts/validate_hlk_km_manifests.py`. The PMO-owned `RESEARCH_BACKLOG_TRELLO_REGISTRY.md` indexes external Trello cards to `topic_id` candidates without treating Trello as SSOT.

**Envoy Tech Lab repository hub:** Holistika-tracked GitHub repositories are indexed in `docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/REPOSITORIES_REGISTRY.md` (GitHub remains SSOT for code trees; the registry is canonical for membership and metadata per `PRECEDENCE.md`). Think Big vault folders hold non-repo client/program artifacts; see `docs/references/hlk/v3.0/Think Big/README.md` and PMO `TOPIC_PMO_CLIENT_DELIVERY_HUB.md`.

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
| `scripts/validate_hlk_km_manifests.py` | Validate HLK KM visual manifest frontmatter and raster paths under `v3.0/_assets/**/*.manifest.md` |
| `scripts/merge_gtm_into_process_list.py` | Idempotent-style merge helper: harmonize GTM candidate CSV into `process_list.csv` (English parents, Tier C exclusion); run with `--write` after operator approval |
| `scripts/refine_gtm_process_hierarchy.py` | Pattern 2 pass: insert `gtm_cl_*` cluster processes from Trello path prefixes, rewire `item_parent_1` / `item_parent_2`, sanitize code-like `item_name` values on existing GTM rows; run with `--write` after merge |
| `scripts/migrate_process_list_program_layer.py` | Pattern 3: insert `hlk_prog_*` program workstreams and re-parent listed GTM workstreams under MADEIRA Platform / Think Big Operational Excellence |
| `scripts/backfill_process_parent_ids.py` | Resolve `item_parent_*` names to `item_parent_*_id` in `process_list.csv`; run after header/column migration |
| `scripts/dedupe_ambiguous_process_item_names.py` | One-time-style repair: rename a fixed set of rows so every `item_name` is unique, enabling full parent-id backfill; run before release if `validate_hlk` reports duplicate-name debt |
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

- **`agent-capabilities.json` → per-agent `tools.profile`**: The capability matrix defines `allowed_categories`, `allowed_tools`, and `denied_tools` per role. Bootstrap translates these into OpenClaw's `agents.list[].tools` block (profile name) while preserving template-curated `alsoAllow` and `deny` fields.
- **Gateway-agnostic design**: If you swap OpenClaw for another gateway, you only rewrite the bootstrap translation. Prompts, policies, workflows, capability matrix, and eval gates survive unchanged.
- **Principle**: Define once in AKOS, push via bootstrap, see in dashboard.

### Runtime SSOT Chain

For runtime-facing work, AKOS uses a layered SSOT chain:

| Layer | File | Role |
|:------|:-----|:-----|
| Repo gateway intent | `config/openclaw.json.example` | Canonical gateway template in git (`.example` suffix = contains `${VAR}` credential placeholders, not optional) |
| Repo MCP intent | `config/mcporter.json.example` | Canonical MCP server template in git (`.example` suffix = contains credential placeholders, not optional) |
| Policy/audit SSOT | `config/agent-capabilities.json` | AKOS logical role policy and drift basis |
| Translation layer | `scripts/bootstrap.py` | Converts repo intent into live runtime files |
| Live gateway runtime | `~/.openclaw/openclaw.json` | Active OpenClaw runtime consumed by the gateway |
| Live MCP runtime | `~/.mcporter/mcporter.json` | Active MCP runtime consumed by mcporter/OpenClaw |

### Tool Policy Split

The capability matrix and the gateway tool policy do not serve the same purpose:

- **`config/agent-capabilities.json`** is the AKOS-layer SSOT for audit, policy reporting, and drift detection.
- **`config/openclaw.json.example`** is the gateway-compatibility SSOT for curated core tool IDs plus MCP plugin names exposed through `tools.alsoAllow`.
- **Bootstrap** translates the runtime profile from the capability matrix, preserves template-curated `alsoAllow` / `deny` entries, and rejects legacy `tools.allow` drift so gateway-visible tool IDs stay deterministic.

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
| HLK Registry         | `akos/hlk.py`, `scripts/hlk_mcp_server.py`                                                                                      | Organisation, process, and compliance vault lookups | MCP server registered in mcporter; agents invoke tools autonomously; OVERLAY_HLK.md teaches agents vault protocol |
| RunPod Provider      | `akos/runpod_provider.py`                                                                                                       | GPU infrastructure lifecycle                                                  | Manages vLLM endpoints; OpenClaw uses them via `vllm-runpod` provider     |
| Checkpoints          | `akos/checkpoints.py`                                                                                                           | Workspace snapshot/restore                                                    | AKOS-only concept; operates on workspace dirs                             |
| Tool Registry        | `akos/tools.py`                                                                                                                 | Dynamic tool inventory from mcporter + permissions                            | AKOS-layer classification of MCP tools                                    |
| State Tracking       | `akos/state.py`                                                                                                                 | Deployment state (active env, model, tier)                                    | AKOS-only; tracks switch-model history                                    |
| Operator Scripts     | `scripts/doctor.py`, `gpu.py`, `sync-runtime.py`, `release-gate.py`, `check-drift.py`, `browser-smoke.py`, `run-evals.py`, `checkpoint.py` | Health, GPU deploy, sync, release, drift, smoke, eval, checkpoint CLIs         | AKOS-only operator tooling                                                |
| Bootstrap            | `scripts/bootstrap.py`                                                                                                          | **Translation layer** — converts AKOS SSOT to OpenClaw config                 | The bridge; rewrites `~/.openclaw/openclaw.json` from AKOS sources        |
| Test Suite           | `tests/` (300+ tests)                                                                                                           | Config validation, Pydantic models, API, prompts, E2E, telemetry, router, live smoke, evals | AKOS quality gates                                                        |
| Compliance           | `config/compliance/eu-ai-act-checklist.json`                                                                                     | EU AI Act evidence map                                                        | AKOS-only governance                                                      |
| Model Tiers          | `config/model-tiers.json`                                                                                                       | Model classification (small/medium/large/sota)                                | Drives prompt variant selection; OpenClaw uses the selected model         |
| Environment Profiles | `config/environments/*.json` + `*.env`                                                                                           | Multi-environment profiles (dev-local, gpu-runpod, gpu-runpod-pod, gpu-shadow, prod-cloud) | Merged into OpenClaw config by `switch-model.py`                          |
| Eval Configs         | `config/eval/alerts.json`, `baselines.json`                                                                                      | SOC thresholds, DX metrics                                                    | AKOS-only evaluation framework                                            |

### OpenClaw Layer (runtime enforcement — configured by bootstrap, visible in dashboard)

| Feature                 | Config Key                            | Purpose                                            | How AKOS Interacts                                         |
| ----------------------- | ------------------------------------- | -------------------------------------------------- | ---------------------------------------------------------- |
| Gateway Daemon          | `gateway.port`, `gateway.bind`        | WebSocket + HTTP control                           | AKOS API probes health via `/api/health`                   |
| Agent Registry          | `agents.list[]`                       | Agent definitions (id, name, workspace, identity)  | Bootstrap force-syncs from `openclaw.json.example`         |
| Per-Agent Tool Profiles | `agents.list[].tools.*`                | Runtime tool access enforcement                    | `profile` comes from `agent-capabilities.json`; `alsoAllow` and `deny` stay curated in `openclaw.json.example` |
| Exec Security           | `tools.exec.security`                 | Shell command approval mode                        | Bootstrap sets per AKOS policy (deny/allowlist/full)        |
| Loop Detection          | `tools.loopDetection.*`               | Gateway-level repetition circuit breaker            | Defense-in-depth with AKOS prompt-level loop detection     |
| Agent-to-Agent          | `tools.agentToAgent.*`                | Gateway-native inter-agent calls                    | Enables Orchestrator delegation at runtime level           |
| Session Policy          | `session.reset.*`, `session.typingMode` | Session reset, typing indicators                | Bootstrap configures idle timeout and typing mode           |
| Browser Control         | `browser.*`                           | Browser automation, SSRF policy                    | Bootstrap sets headless mode and SSRF restrictions         |
| Message Reactions       | `messages.statusReactions.*`           | Lifecycle emoji on messages (queued/thinking/done)  | Bootstrap enables for UX                                  |
| Model Providers         | `models.providers.*`                  | LLM provider routing and failover                  | Bootstrap preserves full provider inventory; unresolved env inputs are surfaced as warnings |
| Channel Routing         | `bindings[]`                          | Route channels to agents                            | Defined in template; future expansion                      |
| MCP Servers             | via mcporter.json                     | Tool servers (11 total)                            | Bootstrap generates resolved paths; AKOS HLK/finance runtime exposure is bridged into OpenClaw by `akos-runtime-tools` |
| WebChat                 | `web.enabled`                         | Dashboard chat interface                            | Always enabled for AKOS                                    |
| Built-in Memory         | `memory.backend`                      | Native session memory                              | Complements AKOS MCP Memory + workspace MEMORY.md          |
| OpenTelemetry           | `diagnostics.openTelemetry.*`         | Traces/metrics export                               | Future: wire to Langfuse OTEL endpoint                     |
| Skills                  | `skills.*`                            | ClawHub skill management                           | Not managed by AKOS (future consideration)                 |
| Plugins                 | `plugins.*`                           | Extension plugins                                   | AKOS manages the `akos-runtime-tools` bridge plugin; other plugin governance remains future work |
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
| Langfuse (primary) | Agent telemetry, tracing, model comparison | process env or `~/.openclaw/.env` |
| Local telemetry mirror | Flagship answer-quality jsonl archive | `~/.openclaw/telemetry/` |
| Splunk Universal Forwarder (optional) | Enterprise SIEM log shipping | `ai_agent_ops` index |
| skillvet | Security posture | Prompt-injection vulnerability rate |

Langfuse is the recommended primary observability backend. `scripts/log-watcher.py` loads secrets from process env or `~/.openclaw/.env`; use `--dry-run` to preview traces without sending. Splunk is available for enterprise deployments that require a full SIEM; the `inputs.conf` template needs path adjustment for the target OS.

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
| All | [`config/environments/dev-local.env`](../config/environments/dev-local.env) | T-5.1 |
| All | [`config/environments/`](../config/environments/) | T-5.4 |

A validation test suite (`tests/`) provides 300+ automated checks covering JSON integrity, Pydantic model validation, cross-file reference consistency, alert evaluation, secret scanning, SOP task coverage, RunPod provider operations, FastAPI endpoints, workspace checkpoints, Langfuse telemetry (reporter lifecycle, metadata contract, sampling), failover router (10 tests), finance service behavior, and GPU deploy UX.

## Live Configuration Status

The multi-agent architecture (Madeira, Orchestrator, Architect, Executor, Verifier) has been wired into the live `~/.openclaw/openclaw.json` using the native `agents.list` schema. All five agents are accessible via `openclaw dashboard` (WebChat). A backup of the original config exists at `~/.openclaw/openclaw.json.bak`.

**Madeira** is the recommended dashboard default for end-user HLK operations. It answers factual questions directly using `hlk_*` tools and only escalates multi-step tasks to the Orchestrator.

To disconnect the AKOS architecture from OpenCLAW:
1. Restore backup: copy `openclaw.json.bak` over `openclaw.json`
2. Optionally remove `~/.mcporter/mcporter.json` to disable MCP servers
3. Restart: `openclaw restart`

## References

- Implementation task registry: [SOP.md Section 8.0](SOP.md#80-implementation-task-registry)
- Full SOP (sections 1.0–7.0): [SOP.md](SOP.md)
- Security controls: [SECURITY.md](../SECURITY.md)
- EU AI Act compliance evidence: [`config/compliance/eu-ai-act-checklist.json`](../config/compliance/eu-ai-act-checklist.json)

