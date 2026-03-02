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
│            (Dual-Agent Runner Model)                    │
│                                                         │
│  ┌─────────────────────┐ ┌────────────────────────┐    │
│  │    ARCHITECT         │ │     EXECUTOR           │    │
│  │  (Read-Only Planner) │ │  (Read-Write Builder)  │    │
│  │                      │ │                         │    │
│  │  • Sequential        │ │  • File system ops      │    │
│  │    Thinking MCP      │ │  • Shell execution      │    │
│  │  • Context analysis  │ │  • API calls            │    │
│  │  • Tool selection    │ │  • Code generation      │    │
│  │  • Risk assessment   │ │  • Strict directives    │    │
│  └──────────┬───────────┘ └────────────┬───────────┘    │
│             │    Plan Document          │                │
│             └──────────────────────────►│                │
├─────────────────────────────────────────────────────────┤
│                 INTELLIGENCE LAYER                       │
│          (Knowledge Graph + Memory)                      │
│                                                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │              GraphRAG (Knowledge Graph)            │   │
│  │  • Predicate allowlists                           │   │
│  │  • Confidence thresholds                          │   │
│  │  • Cryptographic Source of Truth (SSOT)           │   │
│  │  • Intelligence Matrix fact classification        │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

## Dual-Agent Model

Forcing a single agent to simultaneously architect a solution and write the underlying syntax causes **cognitive overload**, resulting in context degradation, hallucinations, and infinite debugging loops.

The dual-agent paradigm separates concerns:

### Architect Agent

- Operates in **read-only** mode
- Uses `sequential_thinking` MCP for structured reasoning
- Produces a plan document with explicit tool selections and risk assessments
- **Cannot** write files, execute shell commands, or make API calls

### Executor Agent

- Operates in **read-write** mode
- Reads the Architect's plan before taking any action
- Executes strict, well-scoped directives
- Fast model optimized for throughput over deep reasoning

### Runtime Configuration (agents.list)

Both agents are registered in `openclaw.json` under `agents.list` using the native OpenCLAW multi-agent schema:

```json
"agents": {
  "defaults": {
    "model": { "primary": "ollama/qwen3:8b" },
    "thinkingDefault": "off"
  },
  "list": [
    {
      "id": "architect",
      "identity": { "name": "Architect", "theme": "...", "emoji": "📐" }
    },
    {
      "id": "executor",
      "identity": { "name": "Executor", "theme": "...", "emoji": "🔧" }
    }
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

3. **`thinkingDefault: "off"` is required for Ollama models.** OpenCLAW defaults to `thinking: "low"` for models it classifies as reasoning-capable. Ollama's `qwen3:8b` does not support the `think` parameter, causing a 400 error that silently prevents the agent from replying. Setting `agents.defaults.thinkingDefault: "off"` in `openclaw.json` resolves this. Per-agent `thinkingDefault` overrides are not yet available in v2026.2.26 (tracked in [openclaw/openclaw#11479](https://github.com/openclaw/openclaw/issues/11479)).

4. **`verboseDefault: "on"` enables tool visibility in WebChat.** By default, OpenCLAW hides tool call activity from the chat surface (`verboseDefault: "off"`). When the user cannot see tool calls, web searches, or reasoning steps, the agent appears to freeze before producing a wall-of-text response. Setting `agents.defaults.verboseDefault: "on"` causes tool summaries to appear as separate bubbles in real-time. Users can override per-session with `/verbose off` or escalate to full output with `/verbose full`. Reference: [OpenCLAW Thinking Levels docs](https://docs.openclaw.ai/tools/thinking).

5. **Ollama `num_ctx` must be set explicitly.** Ollama defaults to `num_ctx=4096` tokens unless the Modelfile overrides it. Even though `openclaw.json` declares `contextWindow: 131072`, this only tells the OpenCLAW gateway the model's theoretical capacity -- it does NOT configure Ollama's actual context window. If the system prompt + SOUL.md + conversation exceeds 4K tokens, Ollama silently truncates the input, often clipping the SOUL.md behavioral instructions. Fix by creating a custom Modelfile with `PARAMETER num_ctx 16384` and rebuilding the model (`ollama create qwen3:8b -f Modelfile`). The provider-level `options` key in `openclaw.json` does not reliably pass through when using `api: "openai-completions"`. See [openclaw/openclaw#3775](https://github.com/openclaw/openclaw/issues/3775).

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
| standard | OVERLAY_REASONING.md (sequential thinking, thinking trace) |
| full | OVERLAY_REASONING.md + OVERLAY_INTELLIGENCE.md + OVERLAY_TOOLS_FULL.md |

Build all variants: `python scripts/assemble-prompts.py`

### Multi-Provider Configuration

`openclaw.json.example` declares five provider blocks using `${VAR}` environment variable substitution:

- `ollama-local` -- local Ollama at 127.0.0.1:11434
- `ollama-gpu` -- remote Ollama on a GPU server (URL from env)
- `openai` -- OpenAI API (key from env)
- `anthropic` -- Anthropic API (key from env)
- `vllm-runpod` -- vLLM endpoint on RunPod/ShadowGPU (URL from env)

### Environment Profiles

Each deployment target has a pair of files in `config/environments/`:

- `<env>.env.example` -- committed template with placeholder values for secrets
- `<env>.json` -- JSON overlay for `openclaw.json` (model, thinkingDefault, etc.)

Profiles: `dev-local` (small/local), `gpu-runpod` (large/remote GPU), `prod-cloud` (SOTA/cloud APIs).

### Model Switching Workflow

A single cross-platform command switches everything atomically:

```
python scripts/switch-model.py <env-name>
```

This copies the `.env`, deep-merges the JSON overlay, deploys the correct SOUL.md variant, and restarts the gateway. Supports `--dry-run` to preview.

### Known Limitations

1. **Per-agent model override bug** ([#29571](https://github.com/openclaw/openclaw/issues/29571)): `agents.defaults.model.primary` overrides per-agent model settings at runtime, so all agents currently share the same model. Model switching must happen at the global level.
2. **Ollama `num_ctx` requires Modelfile**: The `contextWindow` declared in `openclaw.json` does not configure Ollama's actual context window. Each local model needs a custom Modelfile with `PARAMETER num_ctx <value>`.

## MCP Server Topology

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
            ┌────────────────┼────────────────┐
            │                │                │
   ┌────────▼───────┐ ┌─────▼──────┐ ┌───────▼───────┐
   │  Sequential    │ │ Playwright │ │    GitHub     │
   │  Thinking      │ │  Browser   │ │  Codebase     │
   │                │ │ Automation │ │   Auditor     │
   │ Structured     │ │            │ │               │
   │ reasoning,     │ │ DOM-level  │ │ Repo metadata,│
   │ branching,     │ │ interaction│ │ file search,  │
   │ revision       │ │ JS eval    │ │ code search   │
   └────────────────┘ └────────────┘ └───────────────┘
```

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

Every piece of ingested data passes through the Intelligence Matrix before entering the Knowledge Graph:

1. **Ingestion** — File upload, web scrape, or API response
2. **Fact Extraction** — Assign unique `fct_XXX` identifiers to isolated concepts
3. **Source Credibility Scoring** — Numerical score against an average baseline
4. **Impact Analysis** — Direct and indirect impact quantification
5. **Framework Application** — PESTEL, generational filters, and domain-specific analytics
6. **Graph Insertion** — Only relationships with verifiable SSOT are committed to GraphRAG

## Orchestration Library (`akos/`)

All AKOS automation scripts share a typed Python library under `akos/`. This eliminates helper duplication, provides runtime config validation, and centralises logging, subprocess safety, and observability.

| Module | Responsibility |
|:-------|:---------------|
| `akos/models.py` | Pydantic schemas for `model-tiers.json`, `openclaw.json`, environment overlays, alerts, baselines |
| `akos/io.py` | `load_json`, `save_json`, `deep_merge`, `resolve_openclaw_home` |
| `akos/log.py` | `JSONFormatter` + `HumanFormatter`; `setup_logging(json_output)` configures the root logger |
| `akos/process.py` | `CommandResult` dataclass + `run()` wrapper with timeouts and structured error capture |
| `akos/state.py` | `AkosState` Pydantic model tracking the active environment/model; `load_state`, `save_state`, `record_switch` |
| `akos/telemetry.py` | `LangfuseReporter` wrapping the Langfuse SDK; graceful no-op when credentials are absent |
| `akos/alerts.py` | `AlertEvaluator` — checks real-time log entries against `alerts.json` and periodic metrics against `baselines.json` |

All scripts (`bootstrap.py`, `switch-model.py`, `assemble-prompts.py`, `log-watcher.py`) import from `akos/` and accept `--json-log` for structured CI output.

### Rollback Safety

`switch-model.py` wraps steps 2-4 (config merge, prompt deploy, gateway restart) in a `try/finally` block. On failure, `openclaw.json.bak` is restored automatically and a failed state is recorded. Use `--rollback` to manually restore the previous config.

### Future: FastAPI Control Plane

A planned HTTP API layer (FastAPI) will expose model switching, dashboard data, and webhook integration over REST. The `akos/` library already provides the typed models and I/O utilities that this layer will consume. This is documented here for forward planning but is not yet implemented.

## Observability Stack

| Component | Role | Target |
|:----------|:-----|:-------|
| Structured JSON Logs | Agent activity tracing | `/opt/openclaw/logs/` or `$TEMP/openclaw/` |
| `akos/log.py` | Script-level JSON logging | stdout (human or JSON mode) |
| `scripts/log-watcher.py` | Tails gateway logs, pushes traces to Langfuse, evaluates real-time alerts | Langfuse Cloud / stdout |
| `akos/alerts.py` (AlertEvaluator) | Real-time pattern matching against `alerts.json`; periodic baseline checks | `CRITICAL`-level log entries |
| Langfuse | Agent telemetry, tracing, model comparison | `config/eval/langfuse.env.example` |
| Splunk Universal Forwarder | Log shipping | `ai_agent_ops` index |
| skillvet | Security posture | Prompt-injection vulnerability rate |

## Implementation Task Map

The [SOP Section 8.0](SOP.md#80-implementation-task-registry) decomposes the architecture into 33 individually traceable tasks across 6 phases. Each phase maps to the LLMOS layers it implements:

| Phase | SOP Section | LLMOS Layers | Category | Tasks |
|:------|:------------|:-------------|:---------|:------|
| **Phase 0** — Environment Assessment | 3.0 | Control Plane | `ENV` | T-0.1 through T-0.6 |
| **Phase 1** — Configuration Bootstrapping | 4.1–4.2 | Control Plane, Integration | `CONFIG` | T-1.1 through T-1.5 |
| **Phase 2** — MCP Provisioning | 5.1–5.4 | Integration, Execution | `MCP` | T-2.1 through T-2.8 |
| **Phase 3** — Security Implementation | 6.1–6.3 | All | `SECURITY`, `LOGGING` | T-3.1 through T-3.7 |
| **Phase 4** — Dual-Agent Prompt Engineering | 2.0, 5.2 | Execution, Intelligence | `PROMPT` | T-4.1 through T-4.4 |
| **Phase 5** — Observability and DX Metrics | 7.0 | All | `METRIC`, `LOGGING` | T-5.1 through T-5.3 |

Every task carries SSOT traceability (Task ID), SOC relevance tagging, HITL gate classification, and a verification command. See the full registry for details.

## Implementation Scaffolding

The following files implement the architecture described above as committable configuration templates, prompt definitions, and security scripts. Each file traces to a specific task in the [SOP task registry](SOP.md#80-implementation-task-registry).

| LLMOS Layer | File | SOP Task |
|:------------|:-----|:---------|
| Control Plane | [`config/openclaw.json.example`](../config/openclaw.json.example) | T-1.2 |
| Control Plane | [`config/model-tiers.json`](../config/model-tiers.json) | T-5.4 |
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
| All | [`akos/`](../akos/) | Orchestration library (models, I/O, logging, process, state, telemetry, alerts) |
| All | [`config/compliance/eu-ai-act-checklist.json`](../config/compliance/eu-ai-act-checklist.json) | T-3.7 |
| All | [`config/eval/baselines.json`](../config/eval/baselines.json) | T-5.2 |
| All | [`config/eval/alerts.json`](../config/eval/alerts.json) | T-5.3 |
| All | [`config/eval/langfuse.env.example`](../config/eval/langfuse.env.example) | T-5.1 |
| All | [`config/environments/`](../config/environments/) | T-5.4 |

A validation test suite (`tests/`) provides 120+ automated checks covering JSON integrity, Pydantic model validation, cross-file reference consistency, alert evaluation, secret scanning, and SOP task coverage.

## Live Configuration Status

The dual-agent architecture has been wired into the live `~/.openclaw/openclaw.json` using the native `agents.list` schema. Both agents are accessible via `openclaw dashboard` (WebChat). A backup of the original config exists at `~/.openclaw/openclaw.json.bak`.

To disconnect the AKOS architecture from OpenCLAW:
1. Restore backup: copy `openclaw.json.bak` over `openclaw.json`
2. Optionally remove `~/.mcporter/mcporter.json` to disable MCP servers
3. Restart: `openclaw restart`

## References

- Implementation task registry: [SOP.md Section 8.0](SOP.md#80-implementation-task-registry)
- Full SOP (sections 1.0–7.0): [SOP.md](SOP.md)
- Security controls: [SECURITY.md](../SECURITY.md)
- EU AI Act compliance evidence: [`config/compliance/eu-ai-act-checklist.json`](../config/compliance/eu-ai-act-checklist.json)
