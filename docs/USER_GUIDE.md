# OpenCLAW-AKOS User Guide

**Version 0.5.0 -- March 2026**

---

## Table of Contents

1. [What Is OpenCLAW-AKOS?](#1-what-is-openclaw-akos)
2. [Prerequisites](#2-prerequisites)
3. [Installation](#3-installation)
4. [Configuration](#4-configuration)
5. [The Multi-Agent System](#5-the-multi-agent-system)
6. [Prompt Tiering and Assembly](#6-prompt-tiering-and-assembly)
7. [Environment Profiles and Model Switching](#7-environment-profiles-and-model-switching)
8. [RunPod GPU Integration](#8-runpod-gpu-integration)
9. [MCP Server Ecosystem](#9-mcp-server-ecosystem)
10. [Tool Permissions and HITL Gates](#10-tool-permissions-and-hitl-gates)
11. [FastAPI Control Plane](#11-fastapi-control-plane)
12. [Observability and Monitoring](#12-observability-and-monitoring)
13. [Workspace Checkpoints](#13-workspace-checkpoints)
14. [Security](#14-security)
15. [EU AI Act Compliance](#15-eu-ai-act-compliance)
16. [Testing](#16-testing)
17. [Troubleshooting](#17-troubleshooting)
18. [CLI Reference](#18-cli-reference)
19. [API Reference](#19-api-reference)
20. [Configuration Reference](#20-configuration-reference)
21. [Glossary](#21-glossary)

---

## 1. What Is OpenCLAW-AKOS?

OpenCLAW-AKOS transforms a vanilla OpenCLAW deployment into an **Agentic Knowledge Operating System (LLMOS)**. It provides:

- A **5-agent architecture** (Madeira, Orchestrator, Architect, Executor, Verifier) that eliminates cognitive overload by separating user-facing lookup, task decomposition, planning, execution, and validation.
- **Tiered prompt assembly** keyed to model capability (small/medium/large/SOTA).
- **RunPod GPU integration** for serverless vLLM endpoints with auto-provisioning.
- A **FastAPI control plane** for programmatic system management.
- **11 MCP servers** for tools: reasoning, browser automation, GitHub, memory, filesystem, HTTP, LSP, code search, control plane, finance research, and HLK vault lookup.
- **Human-in-the-Loop (HITL) enforcement** on all mutative operations.
- **Observability** via Langfuse telemetry, SOC alerts, and structured logging.
- **Workspace checkpoints** for reversible execution.
- **EU AI Act 2026 compliance** evidence tracking.

The system supports three deployment environments -- local dev (Ollama), remote GPU (RunPod vLLM), and cloud APIs (OpenAI/Anthropic) -- switchable with a single command.

---

## 2. Prerequisites

| Requirement | Minimum | Recommended |
|:------------|:--------|:------------|
| Python | 3.10+ | 3.12+ |
| Node.js | 18+ | 22+ |
| Ollama | Latest | Latest |
| OS | Windows 10+, macOS 12+, Ubuntu 22.04+ | Windows 11 with WSL2 |
| RAM | 8 GB | 16 GB (32 GB for local 32B models) |

**Optional:**
- RunPod account (for GPU deployment)
- OpenAI / Anthropic API keys (for cloud deployment)
- Langfuse account (for observability)
- Docker (for sandboxed deployments)

---

## 3. Installation

### 3.1 Clone the Repository

```bash
git clone https://github.com/your-org/openclaw-akos.git
cd openclaw-akos
```

### 3.2 Install Python Dependencies

```bash
pip install -r requirements.txt
```

The dependencies are:

| Package | Purpose | Required? |
|:--------|:--------|:----------|
| `pydantic>=2.0` | Config validation and type safety | Yes |
| `pytest>=7.0` | Test suite | Yes (for dev) |
| `langfuse>=2.0` | Observability telemetry | Optional (graceful no-op) |
| `runpod>=1.7.0` | RunPod GPU provider | Optional (graceful no-op) |
| `fastapi>=0.115.0` | Control plane API | Optional (only for API server) |
| `uvicorn>=0.32.0` | ASGI server for FastAPI | Optional (only for API server) |
| `httpx>=0.27.0` | Async HTTP client | Optional (only for API tests) |

All optional packages degrade gracefully -- the system works without them.

### 3.3 Automated Bootstrap

The bootstrap script handles the full setup: prerequisite checks, Ollama model pulls, MCP server configuration, and prompt assembly.

**Python (any OS):**

```bash
python scripts/bootstrap.py
```

**PowerShell (Windows):**

```powershell
.\scripts\bootstrap.ps1
```

**Common flags:**

| Flag | Effect |
|:-----|:-------|
| `--skip-wsl` / `-SkipWSL` | Skip WSL2 checks (Windows only) |
| `--skip-ollama` / `-SkipOllama` | Skip Ollama model pulls |
| `--skip-mcp` / `-SkipMCP` | Skip MCP server setup |
| `--primary-model MODEL` | Override primary model (default: `qwen3:8b`) |
| `--embed-model MODEL` | Override embedding model (default: `nomic-embed-text`) |
| `--json-log` | Structured JSON log output |

### 3.4 Manual Setup

If you prefer manual setup:

1. Install OpenCLAW: `curl -fsSL https://molt.bot/install.sh | bash`
2. Onboard the gateway: `openclaw onboard --install-daemon`
3. Copy configs: `cp config/openclaw.json.example ~/.openclaw/openclaw.json`
4. Set up MCP: `cp config/mcporter.json.example ~/.mcporter/mcporter.json`
5. Assemble prompts: `python scripts/assemble-prompts.py`
6. Switch to your environment: `python scripts/switch-model.py dev-local`

---

## 4. Configuration

### 4.1 Configuration Files Overview

All configuration lives under the `config/` directory. Files ending in `.example` are committed templates; copy them (without the `.example` suffix) and fill in your values.

```
config/
  openclaw.json.example        Main gateway configuration
  model-tiers.json             Model tier definitions (SSOT)
  permissions.json             Tool permission classifications
  mcporter.json.example        MCP server definitions
  logging.json                 Structured log format
  intelligence-matrix-schema.json  Fact classification schema
  environments/
    dev-local.json             Local Ollama overlay
    dev-local.env.example      Local env vars
    gpu-runpod.json            RunPod overlay (full profile)
    gpu-runpod.env.example     RunPod env vars
    prod-cloud.json            Cloud API overlay
    prod-cloud.env.example     Cloud API keys
  eval/
    langfuse.env.example       Langfuse credentials
    baselines.json             DX metric baselines
    alerts.json                SOC alerting thresholds
  compliance/
    eu-ai-act-checklist.json   EU AI Act evidence map
  splunk/
    inputs.conf                Splunk forwarder template
  workspace-scaffold/
    orchestrator/              Orchestrator workspace defaults
    architect/                 Architect workspace defaults
    executor/                  Executor workspace defaults
    verifier/                  Verifier workspace defaults
    madeira/                   Madeira workspace defaults
```

### 4.2 openclaw.json

The main gateway configuration. Key sections:

**Gateway:** Bind address and port (default `127.0.0.1:18789`).

**Models:** Provider blocks for each model backend. Each provider has a `baseUrl`, `api` type, and `models` array. Supports `${VAR}` environment variable substitution in URLs.

Five pre-configured providers:
- `ollama` -- local Ollama at `127.0.0.1:11434` (native `api: "ollama"`)
- `ollama-gpu` -- remote Ollama on a GPU server
- `openai` -- OpenAI API
- `anthropic` -- Anthropic API
- `vllm-runpod` -- vLLM endpoint on RunPod

**Agents:** The `agents.defaults` block sets the model, thinking level, and verbose level for all agents. The `agents.list` array registers each agent with its ID, workspace path, and identity metadata.

**Agent tool policy:** In `agents.list[].tools`, use gateway core IDs for profile/deny semantics (`read`, `write`, `edit`, `apply_patch`, `exec`, etc.) and expose MCP plugin tools through `alsoAllow`. Do not rely on legacy `tools.allow` for plugin exposure.

**Bindings:** Optional channel routing rules (Telegram, Slack, etc.).

### 4.3 model-tiers.json

The single source of truth for model classification. Every model is assigned to exactly one tier, which determines its prompt variant and capabilities.

| Tier | Context Budget | Thinking | Prompt Variant | Example Models |
|:-----|:---------------|:---------|:---------------|:---------------|
| `small` | 16,384 | off | compact | `ollama/qwen3:8b`, `ollama/llama3.2:3b` |
| `medium` | 32,768 | low | standard | `ollama/deepseek-r1:14b`, `groq/llama-3.3-70b` |
| `large` | 131,072 | medium | full | `anthropic/claude-sonnet-4`, `vllm-runpod/deepseek-r1-70b` |
| `sota` | 200,000 | high | full | `openai/gpt-5`, `anthropic/claude-opus-4` |

The `variantOverlays` section maps each variant to its overlay files, with agent-level filtering:

| Variant | Overlays |
|:--------|:---------|
| `compact` | None (base only) |
| `standard` | `OVERLAY_REASONING.md` (Architect + Orchestrator only) |
| `full` | `OVERLAY_REASONING.md` + `OVERLAY_INTELLIGENCE.md` + `OVERLAY_CONTEXT_MANAGEMENT.md` + `OVERLAY_TOOLS_FULL.md` (filtered by agent) |

### 4.4 Environment Variables

Each deployment environment has a `.env.example` file. Copy it to `.env` (gitignored) and fill in real values.

**dev-local.env:**
```
OLLAMA_GPU_URL=    # Optional: remote Ollama URL
```

**gpu-runpod.env:**
```
RUNPOD_API_KEY=YOUR_RUNPOD_API_KEY
VLLM_RUNPOD_URL=   # Auto-populated by switch-model.py
RUNPOD_ENDPOINT_ID= # Auto-populated by switch-model.py
```

**prod-cloud.env:**
```
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
ANTHROPIC_API_KEY=YOUR_ANTHROPIC_API_KEY
```

**langfuse.env:**
```
LANGFUSE_PUBLIC_KEY=pk-xxx
LANGFUSE_SECRET_KEY=sk-xxx
LANGFUSE_HOST=https://cloud.langfuse.com
```

---

## 5. The Multi-Agent System

### 5.1 Architecture

The system uses five specialized agents, each with a distinct role:

```
User (HLK questions)
    |
    v
MADEIRA  (answers directly via HLK tools, escalates complex tasks)
    |
    | (multi-step admin tasks)
    v
ORCHESTRATOR  (decomposes, delegates, tracks)
    |
    +---> ARCHITECT   (analyzes, plans, produces Plan Document)
    |         |
    |         v
    +---> EXECUTOR    (executes actions from Plan Document)
    |         |
    |         v
    +---> VERIFIER    (validates output: lint, test, build, screenshot)
              |
              v
         PASS? --> Report to Orchestrator
         FAIL? --> Fix Suggestion --> Executor (up to 3 retries)
```

### 5.2 Madeira (new in v0.6.0)

**Role:** User-facing operational assistant for the Holistika knowledge vault.

**Mode:** Read-only lookup. Cannot write files, execute commands, or use the browser.

**Key behaviors:**
- **Lookup mode (default):** Answers factual HLK questions directly using `hlk_*` tools, citing canonical sources.
- **Summary mode:** Synthesises multi-tool answers with structured formatting.
- **Escalation mode:** Acknowledges multi-step admin requests and delegates to the Orchestrator.
- Never responds with generic "check your HR system" fallbacks when HLK tools are available.

**Workspace:** `~/.openclaw/workspace-madeira/`

### 5.3 Orchestrator

**Role:** Multi-agent coordinator. Receives user requests, decomposes them into sub-tasks, delegates to the appropriate agent, and tracks progress.

**Mode:** Read-only. Cannot execute tasks directly.

**Key behaviors:**
- Produces a **Delegation Plan** with numbered tasks, assigned agents, dependencies, and HITL gates.
- Supports **parallel delegation** for independent tasks.
- Emits progress summaries every 30 seconds during multi-task work.
- Handles errors: if a task fails after 3 Verifier-guided fix attempts, escalates to the user.

**Workspace:** `~/.openclaw/workspace-orchestrator/`

### 5.4 Architect

**Role:** Strategic planner. Analyzes requirements, performs research, and produces structured Plan Documents.

**Mode:** Read-only. Cannot write files, execute commands, or make API calls.

**Key behaviors:**
- Uses `sequential_thinking` MCP for structured reasoning.
- Produces Plan Documents with explicit tool selections, risk assessments, and verification commands.
- Supports response modes: Conversational, Analysis, Handoff, Deployment, Multi-Task, Browser-First.
- Tags external data with Intelligence Matrix fact IDs and source credibility scores.

**Workspace:** `~/.openclaw/workspace-architect/`

### 5.5 Executor

**Role:** Builder. Carries out action plans from the Architect or Orchestrator.

**Mode:** Read-write. Can write files, execute shell commands, and make API calls.

**Key behaviors:**
- Must read the Plan Document before executing. Refuses to proceed without one.
- Follows HITL gates: `autonomous` actions execute immediately; `requires_approval` actions halt for human confirmation.
- **Error recovery loop:** On failure, the Verifier diagnoses and suggests a fix. The Executor applies it and re-verifies, up to 3 attempts before escalating.
- Emits structured progress: announces each action before and after execution.

**Workspace:** `~/.openclaw/workspace-executor/`

### 5.6 Verifier

**Role:** Quality gate. Validates that the Executor's actions produced correct results.

**Mode:** Read-write (limited to validation commands). Cannot modify production files.

**Key behaviors:**
- Runs linters, test suites, build commands, and browser screenshots.
- Classifies results as PASS, FAIL, or SKIP.
- On failure: diagnoses root cause, suggests a targeted fix with confidence rating (HIGH/MEDIUM/LOW).
- Escalates to Orchestrator after 3 failed fix attempts.

**Workspace:** `~/.openclaw/workspace-verifier/`

### 5.7 Selecting Agents

Agents are available via the OpenCLAW WebChat dashboard (`openclaw dashboard`). Select an agent from the sidebar.

- **Start with Madeira** for HLK operations -- role lookups, process navigation, gap detection, vault searches.
- Use **Orchestrator** for multi-step tasks that require coordination across agents.
- Use **Architect** for research, analysis, and planning tasks.
- Use **Executor** when you have a clear, pre-written plan to execute.
- Use **Verifier** to validate a specific piece of work.

To open a Madeira session directly: `http://127.0.0.1:18789/chat?session=agent:madeira:main`

---

## 6. Prompt Tiering and Assembly

### 6.1 How It Works

SOUL.md prompts (the behavioral instructions loaded by each agent) are assembled from a **base file** plus zero or more **overlay files**, depending on the model tier.

```
prompts/base/ARCHITECT_BASE.md  +  overlays/OVERLAY_REASONING.md  +  ...
                                    |
                                    v
                    prompts/assembled/ARCHITECT_PROMPT.full.md
```

This avoids prompt duplication while allowing richer instructions for more capable models.

### 6.2 Base Files

Each agent has a base prompt in `prompts/base/`:

| File | Agent | Content |
|:-----|:------|:--------|
| `ORCHESTRATOR_BASE.md` | Orchestrator | Delegation protocol, task decomposition, error handling |
| `ARCHITECT_BASE.md` | Architect | Read-only rules, Plan Document structure, response modes |
| `EXECUTOR_BASE.md` | Executor | HITL enforcement, execution protocol, error recovery loop |
| `VERIFIER_BASE.md` | Verifier | Verification protocol, fix suggestions, abort conditions |
| `MADEIRA_BASE.md` | Madeira | Lookup-first behaviour contract, HLK tool catalogue, escalation rules |

### 6.3 Overlay Files

Overlays add capabilities for more capable models:

| File | Added To | Content |
|:-----|:---------|:--------|
| `OVERLAY_REASONING.md` | Architect, Orchestrator (standard+) | `sequential_thinking` usage, thinking trace |
| `OVERLAY_INTELLIGENCE.md` | Architect (full only) | Intelligence Matrix, fact classification, cross-referencing |
| `OVERLAY_CONTEXT_MANAGEMENT.md` | Orchestrator, Architect, Executor (full only) | Context compression at 60% capacity, multi-task context |
| `OVERLAY_TOOLS_FULL.md` | Executor, Verifier (full only) | Multi-tool orchestration, browser automation, memory, error recovery |

### 6.4 Assembling Prompts

Run the assembler to generate all variants:

```bash
python scripts/assemble-prompts.py
```

This produces 15 files in `prompts/assembled/` (5 agents x 3 variants):

```
ORCHESTRATOR_PROMPT.compact.md    ORCHESTRATOR_PROMPT.standard.md    ORCHESTRATOR_PROMPT.full.md
ARCHITECT_PROMPT.compact.md       ARCHITECT_PROMPT.standard.md       ARCHITECT_PROMPT.full.md
EXECUTOR_PROMPT.compact.md        EXECUTOR_PROMPT.standard.md        EXECUTOR_PROMPT.full.md
VERIFIER_PROMPT.compact.md        VERIFIER_PROMPT.standard.md        VERIFIER_PROMPT.full.md
MADEIRA_PROMPT.compact.md         MADEIRA_PROMPT.standard.md         MADEIRA_PROMPT.full.md
```

**Flags:**

| Flag | Effect |
|:-----|:-------|
| `--variant compact` | Build only the compact variant |
| `--dry-run` | Preview without writing files |
| `--json-log` | Structured JSON output |

A warning is emitted if any assembled prompt exceeds 20,000 characters (the `bootstrapMaxChars` safety limit for SOUL.md).

### 6.5 How Prompts Are Deployed

When you run `switch-model.py`, it:
1. Looks up the model's tier in `model-tiers.json`.
2. Determines the prompt variant (`compact`, `standard`, or `full`).
3. Copies the matching assembled prompt to each agent's workspace as `SOUL.md`.

Example: switching to `gpu-runpod` (model `vllm-runpod/deepseek-r1-70b`, tier `large`, variant `full`) copies:
```
prompts/assembled/ORCHESTRATOR_PROMPT.full.md  -->  ~/.openclaw/workspace-orchestrator/SOUL.md
prompts/assembled/ARCHITECT_PROMPT.full.md     -->  ~/.openclaw/workspace-architect/SOUL.md
prompts/assembled/EXECUTOR_PROMPT.full.md      -->  ~/.openclaw/workspace-executor/SOUL.md
prompts/assembled/VERIFIER_PROMPT.full.md      -->  ~/.openclaw/workspace-verifier/SOUL.md
prompts/assembled/MADEIRA_PROMPT.full.md       -->  ~/.openclaw/workspace-madeira/SOUL.md
```

---

## 7. Environment Profiles and Model Switching

### 7.1 Available Environments

| Environment | Model | Tier | Use Case |
|:------------|:------|:-----|:---------|
| `dev-local` | `ollama/deepseek-r1:14b` | medium | Local development after `switch-model.py dev-local`; bootstrap seed starts with `ollama/qwen3:8b` |
| `gpu-runpod` | `vllm-runpod/deepseek-r1-70b` | large | Remote GPU, full capabilities |
| `prod-cloud` | `anthropic/claude-sonnet-4` | large | Cloud APIs, production |

### 7.2 Switching Environments

```bash
python scripts/switch-model.py dev-local       # Local Ollama
python scripts/switch-model.py gpu-runpod       # RunPod GPU
python scripts/switch-model.py prod-cloud       # Cloud APIs
```

**What happens:**
1. The `.env` file for the target environment is copied to `~/.openclaw/.env`.
2. The JSON overlay is deep-merged into `~/.openclaw/openclaw.json`.
3. The correct SOUL.md prompt variant is deployed to all 4 agent workspaces.
4. For `gpu-runpod`: the RunPod vLLM endpoint is auto-provisioned (if `RUNPOD_API_KEY` is set).
5. The OpenCLAW gateway is restarted.

**Flags:**

| Flag | Effect |
|:-----|:-------|
| `--dry-run` | Preview all changes without applying |
| `--rollback` | Restore the previous config from `openclaw.json.bak` |
| `--no-restart` | Skip gateway restart |
| `--json-log` | Structured JSON output |

**Rollback safety:** Steps 2-4 are wrapped in `try/finally`. On failure, `openclaw.json.bak` is restored automatically and a failed state is recorded.

### 7.3 Adding a Custom Environment

1. Create `config/environments/my-env.json` with an `agents.defaults` block:

```json
{
  "agents": {
    "defaults": {
      "model": { "primary": "openai/gpt-5-mini" },
      "thinkingDefault": "low",
      "verboseDefault": "on"
    }
  }
}
```

2. Create `config/environments/my-env.env.example` with any required env vars.
3. Add the model to the appropriate tier in `config/model-tiers.json`.
4. Run `python scripts/switch-model.py my-env`.

---

## 8. RunPod GPU Integration

### 8.1 Overview

The RunPod integration supports **two deploy modes**:

- **Serverless endpoint** (`gpu-runpod`) -- auto-scaled, pay-per-request, best for intermittent workloads
- **Dedicated pod** (`gpu-runpod-pod`) -- persistent GPU, fixed hourly billing, best for sustained sessions and faster warm-starts

The operator entry point is [`scripts/gpu.py`](../scripts/gpu.py). It should guide the user to choose the right mode rather than forcing them to already understand RunPod's product surface.

The provider degrades gracefully: if `RUNPOD_API_KEY` is not set or the `runpod` package is not installed, all operations are silent no-ops.

### 8.2 Guided Operator Flow

Run:

```bash
py scripts/gpu.py
```

The interactive flow should guide the operator through:

1. choosing **local**, **serverless endpoint**, or **dedicated pod**
2. understanding the cost/cold-start tradeoff of that choice
3. selecting a model from `config/model-catalog.json`
4. receiving a clear summary of mode, model, URL, and next step

### 8.3 Serverless Endpoint Setup

1. Create a RunPod account at [runpod.io](https://www.runpod.io).
2. Generate an API key from the dashboard.
3. Copy the env template:

```bash
cp config/environments/gpu-runpod.env.example config/environments/gpu-runpod.env
```

4. Set your API key:

```
RUNPOD_API_KEY=your_key_here
```

5. Switch to the RunPod environment:

```bash
python scripts/switch-model.py gpu-runpod
```

This will:
- Load the RunPod config from `gpu-runpod.json`.
- Create a vLLM serverless endpoint with the configured GPU type and model.
- Write the endpoint URL to `VLLM_RUNPOD_URL` in your `.env` file.
- Run a health check to verify the endpoint is ready.

### 8.4 Serverless Configuration

The full RunPod profile in `config/environments/gpu-runpod.json`:

| Field | Description | Default |
|:------|:------------|:--------|
| `gpuIds` | GPU types to use | `["AMPERE_80", "ADA_80"]` |
| `templateName` | RunPod template name | `akos-vllm-deepseek-r1-70b` |
| `vllmImage` | Docker image for vLLM worker | `runpod/worker-v1-vllm:stable-cuda12.8.0` |
| `modelName` | HuggingFace model ID | `deepseek-ai/DeepSeek-R1-0528-Distill-Qwen-70B` |
| `maxModelLen` | Maximum context length | `131072` |
| `activeWorkers` | Min workers (always on) | `0` |
| `maxWorkers` | Max workers (scales up) | `2` |
| `idleTimeoutSeconds` | Workers spin down after | `300` (5 min) |
| `healthCheck.intervalSeconds` | Health poll frequency | `60` |
| `healthCheck.unhealthyThreshold` | Failures before alert | `3` |

### 8.5 Managing Endpoints via API

Once the FastAPI control plane is running:

```bash
# Check endpoint health
curl http://127.0.0.1:8420/runpod/health

# Scale workers
curl -X POST http://127.0.0.1:8420/runpod/scale \
  -H "Content-Type: application/json" \
  -d '{"min_workers": 1, "max_workers": 3}'
```

### 8.6 Health Monitoring

When `log-watcher.py` detects a RunPod environment, it automatically checks endpoint health every 60 seconds and:
- Logs worker count, queue depth, and status to Langfuse as a `runpod-health` trace.
- Fires a SOC alert if the endpoint becomes unhealthy.

### 8.7 Dedicated Pods

Serverless endpoints (Section 8.1-8.5) are ideal for bursty workloads with automatic scaling and pay-per-second billing. **Dedicated pods** are better when you need:

- **Persistent availability** -- no cold-start latency; the model stays loaded in GPU memory.
- **Predictable cost** -- fixed hourly rate instead of per-request billing.
- **Full SSH access** -- direct shell access for debugging, profiling, or running custom vLLM configurations.
- **Long-running sessions** -- extended agent conversations that would otherwise hit serverless idle timeouts.

Use serverless (`gpu-runpod`) for intermittent usage, low idle-cost operation, and lightweight production entry points. Use dedicated pods (`gpu-runpod-pod`) for sustained multi-hour sessions, debugging, and latency-sensitive development.

#### The `gpu-runpod-pod` environment profile

The dedicated pod profile lives in `config/environments/gpu-runpod-pod.json`. It shares the same vLLM tuning parameters as the serverless profile (FP8 KV cache, prefix caching, tool-call parsing) but targets a persistent pod instead of a serverless endpoint. Unlike `gpu-runpod`, it does **not** require `RUNPOD_API_KEY` or `RUNPOD_ENDPOINT_ID` -- only the pod's vLLM URL.

#### Setup

Deploy a dedicated vLLM pod with a single command:

```bash
python scripts/gpu.py deploy-pod
```

The interactive flow:

1. **Select a model** from `config/model-catalog.json` (the GPU model SSOT). The picker shows parameter count, VRAM requirement, reasoning capability, and tool-call parser for each entry.
2. **Select a GPU** type and count. The CLI recommends a default based on the model's VRAM needs and computes the minimum GPU count automatically.
3. **Confirm and deploy**. The CLI provisions a pod on RunPod with the `vllm/vllm-openai:latest` image, passes the correct vLLM flags (including `--tool-call-parser`, `--reasoning-parser` when applicable), switches the gateway to the new endpoint, and persists the URL to both the repo `.env` and `~/.openclaw/.env`.

Use `--dry-run` to preview the configuration without creating a pod:

```bash
python scripts/gpu.py deploy-pod --dry-run
```

After deployment completes, the gateway is automatically switched to the dedicated pod environment and the dashboard is ready to use.

#### Model Catalog

`config/model-catalog.json` is the SSOT for GPU-deployable models. Each entry specifies the HuggingFace ID, VRAM footprint, recommended GPU, vLLM parser, and served-model name. The deploy flow reads this catalog to auto-configure `PodConfig`, the environment overlay JSON, and vLLM launch flags. See [ARCHITECTURE.md](ARCHITECTURE.md#model-catalog) for the full field reference.

#### Other GPU CLI commands

```bash
python scripts/gpu.py status          # Show active infrastructure state
python scripts/gpu.py teardown        # Terminate the active pod
python scripts/gpu.py deploy-serverless --dry-run
python scripts/gpu.py deploy-pod --dry-run
```

#### Verifying the connection

After switching, confirm the gateway can reach your pod:

```bash
curl http://127.0.0.1:8420/health
```

The `runpod` field should show `"healthy"`. You can also test inference directly:

```bash
curl $VLLM_RUNPOD_URL/models
```

---

## 9. MCP Server Ecosystem

### 9.1 Installed Servers

Ten MCP servers provide the agent tool ecosystem:

| Server | Package | Purpose |
|:-------|:--------|:--------|
| `sequential-thinking` | `@modelcontextprotocol/server-sequential-thinking` | Structured reasoning with branching and revision |
| `playwright` | `@playwright/mcp@latest` | Browser automation: navigation, interaction, screenshots |
| `github` | `@modelcontextprotocol/server-github` | Repository metadata, file search, code search (extend for `search_commits`, `show_commit`) |
| `memory` | `@modelcontextprotocol/server-memory` | Cross-session key-value store for persistent recall |
| `filesystem` | `@modelcontextprotocol/server-filesystem` | Structured file read/write operations |
| `fetch` | `@modelcontextprotocol/server-fetch` | HTTP client for API calls |
| `akos` | `scripts/mcp_akos_server.py` | Control plane self-check: `akos_health`, `akos_agents`, `akos_status` |
| `lsp` | `@akos/mcp-lsp-server` | Type-aware code navigation (go-to-definition, find-references, diagnostics) |
| `code-search` | `@akos/mcp-code-search` | Semantic code search via ripgrep + tree-sitter |
| `finance` | `scripts/finance_mcp_server.py` | Read-only finance research: quotes, search, sentiment |

### 9.2 Configuration

MCP servers are defined in `config/mcporter.json.example`. Copy to `~/.mcporter/mcporter.json`:

```bash
cp config/mcporter.json.example ~/.mcporter/mcporter.json
```

If you copied the file manually instead of using bootstrap, resolve placeholder paths:

```bash
py scripts/resolve-mcporter-paths.py
```

Each server is an npm package launched via `npx`. Environment variables (like `GITHUB_TOKEN`) use `${VAR}` substitution.

### 9.3 Which Agents Use Which Servers

| Server | Madeira | Orchestrator | Architect | Executor | Verifier |
|:-------|:-------|:-------------|:----------|:---------|:---------|
| sequential-thinking | -- | standard+ | standard+ | -- | -- |
| playwright | -- | -- | -- | full | full |
| github | -- | -- | yes | yes | -- |
| memory | yes | full | full | full | -- |
| filesystem | -- | -- | -- | full | full |
| fetch | -- | -- | -- | full | -- |
| finance | yes | yes | yes | yes | yes |
| hlk | yes | yes | yes | yes | yes |

### 9.4 Memory Server Usage

The MCP Memory server provides persistent key-value storage across sessions. Agents use it for:

- **Orchestrator:** Stores task outcomes (`orchestrator/task/T-042-outcome`).
- **Architect:** Stores Intelligence Matrix facts (`architect/fact/fct_001`).
- **Executor:** Stores execution anomalies (`executor/anomaly/2026-03-08`).

Key naming convention: `{agent}/{category}/{identifier}`.

### 9.5 GitHub MCP and Commit Retrieval

Set `GITHUB_TOKEN` in your environment to enable GitHub integration. The server provides repository metadata, file search, and code search. Future extensions will add `search_commits(query, since)` and `show_commit(sha)` for historical context. See `config/mcporter.json.example` for the GitHub server entry.

### 9.6 cursor-ide-browser (Cursor IDE Only, Optional)

**cursor-ide-browser** is a Cursor IDE built-in MCP. Enable it in **Cursor Settings > Tools > MCP** for in-IDE WebChat testing. AKOS does not require it; the agent uses the Playwright MCP for browser automation. This is for Cursor users who want an in-IDE browser when developing or testing.

### 9.7 Custom AKOS MCP

The Custom AKOS MCP exposes control plane self-check tools to agents:

| Tool | Purpose |
|:-----|:--------|
| `akos_health()` | GET `/health` — gateway, RunPod, Langfuse status |
| `akos_agents()` | GET `/agents` — list 4 registered agents |
| `akos_status()` | GET `/status` — environment, model, tier |

**Setup:** The server is defined in `config/mcporter.json.example`. Bootstrap deploys it with the correct path. Requires `pip install mcp httpx`. Set `AKOS_API_URL` (default `http://127.0.0.1:8420`) if the API runs elsewhere.

### 9.8 Finance Research MCP

The Finance Research MCP gives agents read-only access to financial market data for research purposes.

| Tool | Purpose |
|:-----|:--------|
| `finance_quote(ticker)` | Quote bundle: price, day range, volume, market cap, exchange, currency |
| `finance_search(query)` | Resolve a company name or partial ticker to matching symbols |
| `finance_sentiment(tickers)` | News sentiment headlines and labels via Alpha Vantage |

**Data freshness:** Quotes from Yahoo Finance free tier are typically delayed ~15 minutes. This capability is for research, not trading decisions.

**Setup:** Requires `pip install mcp yfinance`. The `ALPHA_VANTAGE_KEY` environment variable is optional -- if absent, `finance_sentiment` returns a degraded response with a warning instead of failing. Sign up for a free key at [alphavantage.co](https://www.alphavantage.co/support/#api-key) (500 calls/day).

**Search quality upgrade:** If you also set `FINNHUB_API_KEY`, `finance_search` uses Finnhub fuzzy company-name search first, then falls back to yfinance metadata lookup when the key is absent or the provider fails. Sign up for a free key at [finnhub.io/register](https://finnhub.io/register).

**Limitations:** yfinance is a community library that scrapes Yahoo Finance. It may break when Yahoo changes their site. All provider-specific details are encapsulated in `akos/finance.py` so backends can be swapped without changing tool signatures.

### 9.9 HLK Registry MCP

The HLK Registry MCP gives agents read-only access to the Holistika organisation and process vault.

| Tool | Purpose |
|:-----|:--------|
| `hlk_role(role_name)` | Look up a role's description, access level, area, entity, and reporting chain position |
| `hlk_role_chain(role_name)` | Traverse the reports_to chain from a role up to Admin |
| `hlk_area(area)` | List all roles in an organisational area (Admin, AI, People, Operations, Finance, Marketing, Data, Tech, Legal, Research) |
| `hlk_process(item_id)` | Look up a process item by its ID (e.g. `hol_resea_dtp_99`) |
| `hlk_process_tree(item_name)` | List direct children of a process item by parent name |
| `hlk_projects()` | List all 11 top-level projects with child counts |
| `hlk_gaps()` | Identify items with missing metadata, TBD owners, or empty descriptions |
| `hlk_search(query)` | Fuzzy search across roles and processes by name, description, or ID |

**Data source:** All tools read from the canonical vault CSVs (`docs/references/hlk/compliance/baseline_organisation.csv` and `process_list.csv`). The vault is the database -- no external DB dependency required.

**Setup:** Requires `pip install mcp`. No API keys needed. The `OVERLAY_HLK.md` prompt overlay teaches agents when and how to use these tools, and how to cite canonical sources in responses.

**Recommended validation prompts:**
- `Who is the CTO?`
- `Show me all Research roles.`
- `What workstreams are under KiRBe Platform?`
- `I want to add a new process under the Data Governance project.`

---

## 10. Tool Permissions and HITL Gates

### 10.1 Classification

Every tool is classified in `config/permissions.json` as either **autonomous** (no approval needed) or **requires_approval** (human must confirm).

`permissions.json` includes a mix of gateway core IDs, MCP plugin IDs, and AKOS logical aliases. In the live gateway template, use gateway core IDs such as `read`, `write`, `edit`, `apply_patch`, and `exec`, then expose MCP plugins through `tools.alsoAllow`.

**Autonomous tools** (examples):
`read`, `web_search`, `web_fetch`, `memory_search`, `memory_get`, `sequential_thinking`, `finance_quote`, `finance_search`, `finance_sentiment`, `hlk_role`, `hlk_role_chain`, `hlk_area`, `hlk_process`, `hlk_process_tree`, `hlk_projects`, `hlk_gaps`, `hlk_search`

**Approval-gated tools** (examples):
`write`, `edit`, `apply_patch`, `exec`, `browser`, `sessions_send`, `sessions_spawn`, `subagents`, `memory_store`, `memory_delete`, `fetch_post`, `filesystem_write`, `filesystem_delete`, `git_push`, `git_commit`

### 10.2 How HITL Works

1. The Executor reads the HITL gate for each action from the Plan Document.
2. For `autonomous` actions: executes immediately.
3. For `requires_approval` actions: halts, displays the tool name, parameters, and risk, and waits for explicit approval.
4. When in doubt, the Executor treats the action as `requires_approval`.

### 10.3 Tool Registry

The dynamic tool registry (`akos/tools.py`) reads `mcporter.json.example` and `permissions.json` at runtime. You can query it:

```python
from akos.tools import ToolRegistry

registry = ToolRegistry()
registry.all_tools()           # All known tools
registry.classify("write")       # "requires_approval"
registry.is_available("memory_store")  # True
registry.server_names            # ["sequential-thinking", "playwright", ...]
```

---

## 11. FastAPI Control Plane

### 11.1 Starting the API

```bash
python scripts/serve-api.py --port 8420
```

The API binds to `127.0.0.1:8420` by default. Use `--host 0.0.0.0` for network access (not recommended for production without a reverse proxy).

| Flag | Default | Description |
|:-----|:--------|:------------|
| `--port` | 8420 | Port number |
| `--host` | 127.0.0.1 | Bind address |
| `--reload` | off | Auto-reload on file changes (dev only) |

### 11.2 Endpoints

| Method | Path | Description |
|:-------|:-----|:------------|
| GET | `/health` | System health: gateway, RunPod, Langfuse status, uptime |
| GET | `/status` | Current environment, model, tier, variant, last switch |
| POST | `/switch` | Switch environment (body: `{"environment": "gpu-runpod", "dry_run": false}`) |
| GET | `/agents` | List all 5 agents with workspace paths and SOUL.md status |
| GET | `/runpod/health` | RunPod endpoint health: workers, queue depth |
| POST | `/runpod/scale` | Adjust RunPod scaling (body: `{"min_workers": 1, "max_workers": 3}`) |
| GET | `/metrics` | DX baseline metrics from `baselines.json` |
| GET | `/alerts` | SOC alert definitions from `alerts.json` |
| POST | `/prompts/assemble` | Trigger prompt assembly (body: `{"variant": "full"}` or `{}`) |
| POST | `/checkpoints` | Create workspace checkpoint (body: `{"name": "...", "workspace": "..."}`) |
| GET | `/checkpoints?workspace=...` | List checkpoints for a workspace |
| POST | `/checkpoints/restore` | Restore a checkpoint (body: `{"name": "...", "workspace": "..."}`) |
| WS | `/logs` | Live log stream via WebSocket |

### 11.3 Example Usage

**Check system health:**
```bash
curl http://127.0.0.1:8420/health
```

```json
{
  "status": "ok",
  "gateway": "up",
  "runpod": "disabled",
  "langfuse": "disabled",
  "uptime_seconds": 42.7
}
```

**Switch to RunPod (dry run):**
```bash
curl -X POST http://127.0.0.1:8420/switch \
  -H "Content-Type: application/json" \
  -d '{"environment": "gpu-runpod", "dry_run": true}'
```

**List agents:**
```bash
curl http://127.0.0.1:8420/agents
```

**Stream logs (WebSocket):**
```javascript
const ws = new WebSocket("ws://127.0.0.1:8420/logs");
ws.onmessage = (event) => console.log(JSON.parse(event.data));
```

---

## 12. Observability and Monitoring

### 12.1 The Observability Stack

```
log-watcher.py --> Langfuse        (primary: per-request traces, model comparison)
               |-> AlertEvaluator  (real-time SOC alerts)
               |-> RunPod health   (periodic infrastructure monitoring)
               +-> stdout          (human-readable or JSON, always available)

Splunk UF (optional) --> ai_agent_ops index (enterprise SIEM)
```

### 12.2 Langfuse Telemetry

Langfuse is the primary observability backend. It provides per-request agent traces, model comparison, and cost tracking.

**Setup:**

1. Sign up at [cloud.langfuse.com](https://cloud.langfuse.com) (free tier) or self-host.
2. Copy the template: `cp config/eval/langfuse.env.example config/eval/langfuse.env`
3. Fill in your keys.
4. Start the watcher **alongside the gateway** (both must run for traces to appear):

```bash
python scripts/log-watcher.py
```

Without credentials, telemetry degrades to a no-op. The watcher still evaluates alerts and logs to stdout.

**No traces yet?** Run the smoke test first: `py scripts/test-langfuse-trace.py`. If that succeeds, traces reach Langfuse. Live traces require the **log-watcher to be running** while you send chat messages through the gateway. The watcher tails `%TEMP%/openclaw/openclaw-YYYY-MM-DD.log` (or `$TMPDIR/openclaw/` on macOS/Linux).

**Flags:**

| Flag | Effect |
|:-----|:-------|
| `--once` | Single pass then exit (for CI) |
| `--dry-run` | Print traces without sending to Langfuse |
| `--env-file PATH` | Custom Langfuse env file location |
| `--environment`, `-e` | Environment tag (dev-local, gpu-runpod, prod-cloud) |
| `--json-log` | Structured JSON output |

**Environment:**
- `LANGFUSE_PUBLIC_KEY` -- your Langfuse public key
- `LANGFUSE_SECRET_KEY` -- your Langfuse secret key
- `LANGFUSE_HOST` -- Langfuse endpoint (default: `https://cloud.langfuse.com`)
- `LOG_WATCHER_POLL_INTERVAL` -- seconds between log polls (default: 2)

**Per-environment Langfuse setup (Phase 10):**

All three environment templates (`dev-local.env.example`, `gpu-runpod.env.example`, `prod-cloud.env.example`) now include `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, and `LANGFUSE_HOST` placeholders. When you run `py scripts/switch-model.py <env>`, Langfuse credentials propagate automatically. For local development, you can also use `config/eval/langfuse.env` (loaded by `scripts/serve-api.py` and `scripts/log-watcher.py`).

**Startup compliance tracing:**

The log watcher now detects "Post-Compaction Audit" gateway entries and sends scored traces to Langfuse (`startup_compliance: 0.0` for failures, `1.0` for passes). This enables monitoring startup compliance rates across models and environments in the Langfuse dashboard.

**Dev vs prod trace separation:**

Traces are tagged with an `environment` so you can filter dev-local, gpu-runpod, and prod-cloud in Langfuse. Use the "Environment" filter in the Tracing UI or filter by metadata `environment: dev-local`. The log watcher reads `AKOS_ENV` from `~/.openclaw/.env` (set automatically by `switch-model.py` when you switch environments).

**"No traces yet?" troubleshooting:**

1. **Run the log watcher alongside the gateway** — Traces come from the watcher tailing the gateway log. Start both:
   ```bash
   openclaw gateway start &      # or your usual gateway command
   python scripts/log-watcher.py
   ```
2. **Verify credentials** — Run the smoke test:
   ```bash
   python scripts/test-langfuse-trace.py
   ```
   If it prints "Test trace sent to Langfuse successfully", check the Tracing tab (traces may take a few seconds to appear). If it fails, ensure `config/eval/langfuse.env` has valid `LANGFUSE_PUBLIC_KEY` and `LANGFUSE_SECRET_KEY`.
3. **Confirm log path** — The watcher reads `%TEMP%\openclaw\openclaw-YYYY-MM-DD.log` (Windows) or `/tmp/openclaw/openclaw-YYYY-MM-DD.log` (Linux). Ensure the OpenCLAW gateway writes there.

#### 12.2.1 Langfuse Trace Taxonomy

All traces emitted by the log watcher and telemetry module follow a consistent naming convention. Use these patterns when building Langfuse dashboard filters and score queries.

| Trace Name Pattern | When Fired | Score | Description |
|:-------------------|:-----------|:------|:------------|
| `akos-{agent_role}` | Every agent request | -- | Per-request agent activity trace |
| `akos-startup-{agent_role}` | Session startup | `startup_compliance: 0.0/1.0` | Startup file read compliance |
| `akos-eval-{task_id}` | Eval run | `eval_pass: 0.0/1.0` | Agent reliability eval result |
| `akos-alert-{severity}` | SOC alert fired | `soc_alert: 0.25-1.0` | SOC alert forwarded to Langfuse |
| `akos-metric-{name}` | Periodic (every 100 entries) | -- | DX metric sample (latency, count) |
| `akos-health-runpod` | Periodic health check | -- | RunPod/vLLM infrastructure health |

Scores with a `0.0/1.0` range are boolean pass/fail. The `soc_alert` score maps severity to a float: `CRITICAL=1.0`, `HIGH=0.75`, `MEDIUM=0.5`, `LOW=0.25`.

#### 12.2.2 Langfuse Dashboard Setup Guide

Follow these steps to build a monitoring dashboard from AKOS traces.

**1. Create a Langfuse project and get API keys:**

Sign up at [cloud.langfuse.com](https://cloud.langfuse.com) (free tier is sufficient). Create a project, then go to **Settings > API Keys** and copy the public and secret keys.

**2. Configure credentials:**

```bash
cp config/eval/langfuse.env.example config/eval/langfuse.env
```

Edit `config/eval/langfuse.env` and fill in:

```
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_HOST=https://cloud.langfuse.com
```

**3. Recommended dashboard widgets:**

| Widget | Filter / Group By | Purpose |
|:-------|:------------------|:--------|
| Startup compliance rate | Score name: `startup_compliance`, aggregate: avg | Track how often agents pass startup file-read checks |
| Alert frequency | Trace name: `akos-alert-*` | Monitor SOC alert volume over time |
| Cost by environment | Group by metadata `environment` | Compare spend across dev-local, gpu-runpod, prod-cloud |
| Eval pass rate | Score name: `eval_pass`, aggregate: avg | Agent reliability trend |
| P95 latency | Metric traces: `akos-metric-*`, latency field | Spot latency regressions |

**4. Environment filtering:**

Langfuse natively supports environment filtering when the SDK passes `environment=` at init. The log watcher sets this automatically from `AKOS_ENV`. Use the **Environment** dropdown in the Langfuse Tracing UI to filter by:

- `dev-local` -- local Ollama development
- `gpu-runpod` -- RunPod serverless endpoints
- `gpu-runpod-pod` -- RunPod dedicated pods
- `prod-cloud` -- cloud API providers (OpenAI, Anthropic)

**5. Verify the integration:**

```bash
python scripts/test-langfuse-trace.py
```

Then open the **Tracing** tab in Langfuse. A test trace should appear within a few seconds. If it doesn't, double-check the keys in `config/eval/langfuse.env`.

### 12.3 SOC Alerts

Real-time alerts are defined in `config/eval/alerts.json` and evaluated by `akos/alerts.py`. The log watcher checks every log entry against these rules.

**Built-in alert triggers:**

| Alert | Severity | Trigger |
|:------|:---------|:--------|
| `chmod` execution | CRITICAL | Real-time: `chmod` in tool output |
| `/etc/` or `~/.ssh/` access | CRITICAL | Real-time: sensitive path detected |
| `canvas_eval` invocation | HIGH | Real-time: JavaScript eval used |
| Prompt injection detected | CRITICAL | Continuous: pattern match |
| Completion rate below baseline | HIGH | Periodic: 7-day window |

Triggered alerts are logged at `CRITICAL` level and forwarded to Langfuse.

### 12.4 DX Metrics

The telemetry module (`akos/telemetry.py`) tracks DX-relevant metrics:

| Metric | Source |
|:-------|:-------|
| Task completion rate | Orchestrator traces |
| Time-to-first-response | Agent traces |
| Verification pass rate | Verifier traces |
| RunPod cost per task | RunPod inference results |
| Error recovery success rate | Executor retry traces |

Baselines are defined in `config/eval/baselines.json`.

---

## 13. Workspace Checkpoints

### 13.1 Overview

The checkpoint system (`akos/checkpoints.py`) provides reversible execution by snapshotting agent workspaces as tarballs. Inspired by Replit's snapshot engine and Windsurf's named checkpoints.

### 13.2 CLI Usage (via Python)

```python
from akos.checkpoints import create_checkpoint, restore_checkpoint, list_checkpoints
from pathlib import Path

workspace = Path.home() / ".openclaw" / "workspace-executor"

# Snapshot before a risky operation
create_checkpoint("before-refactor", workspace)

# List available checkpoints
for ckpt in list_checkpoints(workspace):
    print(f"{ckpt.name}  {ckpt.created_at}  {ckpt.size_bytes} bytes")

# Restore if something goes wrong
restore_checkpoint("before-refactor", workspace)
```

### 13.3 API Usage

```bash
# Create a checkpoint
curl -X POST http://127.0.0.1:8420/checkpoints \
  -H "Content-Type: application/json" \
  -d '{"name": "pre-deploy", "workspace": "/home/user/.openclaw/workspace-executor"}'

# List checkpoints
curl "http://127.0.0.1:8420/checkpoints?workspace=/home/user/.openclaw/workspace-executor"

# Restore
curl -X POST http://127.0.0.1:8420/checkpoints/restore \
  -H "Content-Type: application/json" \
  -d '{"name": "pre-deploy", "workspace": "/home/user/.openclaw/workspace-executor"}'
```

### 13.4 How It Works

- Checkpoints are stored as `.tar.gz` files inside `{workspace}/.checkpoints/`.
- Creating a checkpoint archives everything in the workspace except the `.checkpoints` directory itself.
- Restoring clears the workspace (except `.checkpoints`) and extracts the tarball.
- Multiple checkpoints with the same name are timestamped; restore always picks the most recent.

---

## 14. Security

### 14.1 Threat Model

OpenCLAW-AKOS deploys an autonomous agent with filesystem access, API credentials, and shell execution capabilities. This is equivalent to granting a new employee full workstation access.

Known active threats:
- **ClawHavoc Campaign** -- 341+ malicious ClawHub skills distributing Atomic Stealer (AMOS) malware.
- **CVE-2026-24763** -- Command injection vulnerability in the OpenCLAW gateway.
- **ClickFix Social Engineering** -- Prompt-injection payloads disguised as community skills.

### 14.2 Mandatory Controls

1. **Execution Isolation:** The agent must never run on bare metal. Use WSL2 (Windows) or Docker Sandbox (macOS/Linux).

2. **Pre-Execution Skill Auditing:** Never install skills directly from ClawHub.
   ```bash
   bash scripts/vet-install.sh <skill-slug>
   ```
   The `skillvet` scanner performs 48 vulnerability checks.

3. **HITL Enforcement:** All mutative tools require human approval (see Section 10).

4. **Network Egress Filtering:** The gateway binds to `127.0.0.1` only. Docker sandboxes restrict outbound traffic to localhost.

5. **SOC Monitoring:** Structured JSON logs with real-time alert evaluation (see Section 12).

### 14.3 Reporting Vulnerabilities

Do not open a public GitHub issue. Email the maintainer or use GitHub's private vulnerability reporting. We acknowledge reports within 48 hours.

---

## 15. EU AI Act Compliance

The system tracks EU AI Act 2026 compliance evidence in `config/compliance/eu-ai-act-checklist.json`.

| Requirement | Status | Evidence |
|:------------|:-------|:---------|
| **EU-AIA-1: Record-Keeping** | Implemented | Structured JSON logging, Langfuse traces, RunPod health monitoring, workspace checkpoints |
| **EU-AIA-2: Human Oversight** | Implemented | HITL gates in permissions.json, Orchestrator delegation with HITL per task, Verifier independent validation |
| **EU-AIA-3: Risk Management** | Implemented | skillvet scanner (48 checks), SOC alerts, Verifier quality gate, 3-attempt error recovery loop |

Overall status: **Partial** -- pending live Langfuse deployment and first audit cycle.

---

## 16. Testing

### 16.1 Quick Commands

All tests run through a single entry point -- `scripts/test.py`. No file paths to memorize.

```bash
py scripts/test.py              # all 193+ tests
py scripts/test.py api          # FastAPI endpoints + E2E pipeline
py scripts/test.py security     # alerts, permissions, config validation
py scripts/test.py runpod       # RunPod provider (mocked SDK)
py scripts/test.py prompts      # prompt structure + assembly
py scripts/test.py models       # Pydantic model schemas
py scripts/test.py checkpoints  # workspace snapshot/restore
py scripts/test.py scaffolding  # file tree integrity + secrets scan
py scripts/test.py e2e          # full system wiring
py scripts/test.py configs      # JSON integrity + cross-file refs
py scripts/test.py browser      # automated browser smoke (requires Playwright)
py scripts/test.py uat          # start live Swagger server for manual testing
py scripts/test.py --list       # show all available groups
```

Add `-q` for minimal output or `-v` for verbose (verbose is the default).

### 16.2 Test Categories

| Group | Tests | What They Validate |
|:------|:------|:-------------------|
| `api` | 31 | FastAPI endpoints + E2E pipeline wiring |
| `security` | 22+ | Alerts, permissions, config validation |
| `runpod` | 21 | All RunPod operations with mocked SDK |
| `prompts` | 35+ | Prompt structure, content, assembly, overlays |
| `models` | 20+ | Pydantic schemas (valid + invalid input) |
| `checkpoints` | 9 | Workspace snapshot create/restore/list |
| `scaffolding` | 20+ | File tree, secrets scan, SOP coverage |
| `e2e` | 18 | Full agent/tool/overlay system wiring |
| `configs` | 50+ | JSON integrity, model tiers, cross-file refs |
| `browser` | 1 | Automated browser smoke (Playwright) — dashboard health, agents, Swagger, workflow launch |

### 16.3 Browser-Based Smoke Test (UAT)

This section describes how to verify the system is working by interacting with it as an end user.

#### 16.3.1 Testing the Control Plane (Swagger UI)

1. **Start the API server:**
   ```bash
   py scripts/test.py uat
   ```
   You'll see: `Uvicorn running on http://127.0.0.1:8420`

2. **Open the Swagger UI** in your browser:
   ```
   http://127.0.0.1:8420/docs
   ```

3. **Test each endpoint** by clicking on it, then "Try it out", then "Execute":

   | Endpoint | What you expect |
   |:---------|:----------------|
   | GET `/health` | `"status": "ok"`, uptime counter |
   | GET `/agents` | Array with 5 agents: madeira, orchestrator, architect, executor, verifier |
   | GET `/metrics` | `"baselines"` array with 4 DX metrics |
   | GET `/alerts` | `"alerts"` array with SOC alert definitions |
   | POST `/prompts/assemble` | `"success": true` with 15 built prompts |
   | GET `/runpod/health` | `"enabled": false` (expected without API key) |
   | POST `/switch` (body: `{"environment": "dev-local", "dry_run": true}`) | Model/tier/variant for dev-local |

4. **Stop the server** with `Ctrl+C`.

#### 16.3.2 Testing the OpenCLAW Dashboard (End-User Experience)

This tests the actual product as users experience it.

**Prerequisites:** OpenCLAW gateway installed and running (see [Section 3](#3-installation)).

1. **Start the gateway** (if not already running):
   ```bash
   openclaw gateway start
   ```

2. **Open the dashboard** in your browser:
   ```
   http://127.0.0.1:18789
   ```
   Or use the CLI shortcut: `openclaw dashboard`

3. **Verify agents are listed.** You should see all 5 agents: Madeira, Orchestrator, Architect, Executor, and Verifier.

4. **Test the Architect** (read-only agent):
   - Select the **Architect** agent
   - Send: `Analyze the current project structure and suggest improvements.`
   - **Expected:** A structured plan output. The Architect should **not** execute any commands or write files.

5. **Test the Executor** (read-write agent):
   - Select the **Executor** agent
   - Send a simple task: `List the files in the workspace.`
   - **Expected:** The agent uses allowed tools. If the task is mutative, it should request HITL approval.

6. **Test MCP tools:**
   - Ask the Architect: `Use sequential thinking to analyze the pros and cons of microservices vs monolith.`
   - **Expected:** The agent calls the `sequential_thinking` MCP tool and produces a step-by-step reasoning chain.

7. **Test error recovery:**
   - Ask the Executor to do something that will fail (e.g., reference a non-existent file)
   - **Expected:** The Verifier-guided 3-retry loop activates. After 3 failures, it halts and reports.

#### 16.3.3 Automated Browser Smoke (Playwright)

When Playwright is installed, you can run automated DOM-based checks:

```bash
pip install playwright && playwright install chromium
py scripts/browser-smoke.py --playwright
py scripts/test.py browser      # same, via test runner
```

| Flag | Effect |
|:-----|:-------|
| `--playwright` | Run DOM-based checks (dashboard health, agent visibility, Swagger, Architect/Executor UI, workflow launch). Without this flag, only HTTP checks run. |
| `--headed` | Show the browser window during runs (default: headless). |

If Playwright is not installed, `--playwright` is skipped with a clear message. The release gate runs browser smoke when Playwright is available.

#### 16.3.4 Smoke Test Checklist

Use this checklist after any deployment or major configuration change:

- [ ] Gateway starts without errors
- [ ] Dashboard loads at `http://127.0.0.1:18789`
- [ ] All 5 agents are visible (Madeira, Orchestrator, Architect, Executor, Verifier)
- [ ] Architect responds in read-only mode (no file writes)
- [ ] Executor requests HITL approval for mutative operations
- [ ] MCP tools are available (sequential thinking, browser, GitHub)
- [ ] Control Plane API responds at `http://127.0.0.1:8420/health`
- [ ] Prompt assembly succeeds (POST `/prompts/assemble`)
- [ ] Log watcher is running (`scripts/log-watcher.py`)

### 16.4 CI Integration

For CI pipelines:
```bash
py scripts/test.py all -q
```

The `-q` flag produces minimal output suitable for CI logs.

---

## 17. Troubleshooting

### Agent is silent or freezes

**Cause:** `verboseDefault` is set to `"off"`, hiding tool calls.

**Fix:** Set `agents.defaults.verboseDefault` to `"on"` in `openclaw.json`. This shows tool summaries as real-time bubbles.

### Ollama model silently truncates prompts

**Cause:** Ollama defaults to `num_ctx=4096` unless the Modelfile overrides it.

**Fix:** Committed Modelfiles in `config/ollama/` already set `num_ctx` to match tier context budgets. Rebuild with:
```bash
ollama create qwen3:8b -f config/ollama/Modelfile.qwen3-8b
ollama create deepseek-r1:14b -f config/ollama/Modelfile.deepseek-r1-14b
```
Verify: `ollama show <model> --parameters` should display the correct `num_ctx`.

### Ollama Performance Tuning

Set these environment variables (already configured in `dev-local.env.example`) for optimal local performance:

| Variable | Value | Effect |
|:---------|:------|:-------|
| `OLLAMA_FLASH_ATTENTION` | `1` | Faster inference, lower VRAM, no quality loss |
| `OLLAMA_KV_CACHE_TYPE` | `q8_0` | 8-bit KV cache quantization halves VRAM for context |

Options for `OLLAMA_KV_CACHE_TYPE`: `f16` (default, no quantization), `q8_0` (recommended, negligible quality loss), `q4_0` (aggressive, for very constrained VRAM).

### Upgrading Local Models

To upgrade from the 8B small-tier model to the 14B medium-tier model:

1. Pull the model: `ollama pull deepseek-r1:14b`
2. Rebuild with committed Modelfile: `ollama create deepseek-r1:14b -f config/ollama/Modelfile.deepseek-r1-14b`
3. Switch environment: `python scripts/switch-model.py dev-local`

The `dev-local` environment profile is pre-configured to use `deepseek-r1:14b` as primary with `qwen3:8b` as fallback. Separately, the cross-platform bootstrap seeds an initial local-safe runtime using `qwen3:8b` before you explicitly switch environments.

### RunPod vLLM Best Practices

The `gpu-runpod.json` profile includes production-grade vLLM settings. Key recommendations:

- **Tool calling**: Set `ENABLE_AUTO_TOOL_CHOICE=true` and `TOOL_CALL_PARSER=deepseek_v3` for structured tool output (without this, tool calls return as raw text).
- **Prefix caching**: `ENABLE_PREFIX_CACHING=true` avoids recomputing the 3-10K SOUL.md system prompt tokens on every request.
- **FP8 KV cache**: `KV_CACHE_DTYPE=fp8` doubles KV cache capacity, enabling 131K context on A100-80GB.
- **GPU selection**: `AMPERE_80` (A100-80GB) and `ADA_80` (H100-80GB) are recommended for 70B distilled models.
- **Concurrency**: `MAX_NUM_SEQS=128` (down from default 256) trades batch throughput for lower tail latency in agent workloads.

### `thinkingDefault` causes 400 errors with Ollama

**Cause:** Small Ollama models (e.g. `qwen3:8b`) may not support the `think` parameter. OpenCLAW defaults to `thinking: "low"`.

**Fix:** The `dev-local` profile uses `deepseek-r1:14b` (which supports reasoning) with `thinkingDefault: "low"`. If you switch to a small model that doesn't support thinking, set `thinkingDefault` to `"off"` in your environment overlay.

### RunPod endpoint not provisioning

**Cause:** `RUNPOD_API_KEY` not set or `runpod` package not installed.

**Fix:**
1. Install: `pip install runpod`
2. Set: `RUNPOD_API_KEY=your_key` in `gpu-runpod.env`
3. Re-run: `python scripts/switch-model.py gpu-runpod`

### RunPod endpoint unhealthy after provisioning

**Cause:** Workers take 2-5 minutes to warm up after creation.

**Fix:** Wait and check again:
```bash
curl http://127.0.0.1:8420/runpod/health
```
The log watcher also monitors health every 60 seconds.

### Assembled prompt exceeds bootstrapMaxChars

**Cause:** An overlay file is too long.

**Fix:** Shorten the overlay or raise the limit in `assemble-prompts.py` (default: 20,000 chars).

### FastAPI won't start

**Cause:** Missing `fastapi` or `uvicorn` package.

**Fix:** `pip install fastapi uvicorn`

### Per-agent model override not working

**Known bug** ([#29571](https://github.com/openclaw/openclaw/issues/29571)): `agents.defaults.model.primary` overrides per-agent settings at runtime. All agents currently share the same model. Model switching must happen at the global level via `switch-model.py`.

### Switch-model.py fails and config is corrupt

**Fix:** The script auto-restores from `openclaw.json.bak`. You can also manually restore:
```bash
python scripts/switch-model.py --rollback
```

### "No nodes with system.exe available" (Nodes page)

**Cause:** The dashboard expects an exec-capable node but none is paired. This message appears on the Nodes settings page when `tools.exec.host` can use nodes but no paired node offers exec capability (`system.exe` on Windows or equivalent elsewhere).

**Fix:**
1. **Local exec only:** Set `tools.exec.host` to `"sandbox"` or `"gateway"` (AKOS default is `sandbox`).
2. **Use a node:** Pair an exec-capable node (`openclaw node install`, `openclaw nodes status`) and ensure it has `system.exe` (Windows) or equivalent for command execution.

### `openclaw gateway status` shows `Runtime: unknown` while RPC/listener are healthy

**Cause:** On Windows Scheduled Task supervision, OpenClaw can report service runtime metadata as `unknown` even when gateway socket and RPC probe are healthy.

**Fix / verification path:**
1. Run `py scripts/doctor.py`.
2. Confirm runtime-contract checks report both:
   - `Gateway runtime normalized to healthy (...)`
   - `Runtime status deterministic across repeated probes (healthy)`
3. If checks fail, restart and validate again:
   - `openclaw gateway restart`
   - `py scripts/doctor.py`

### `[config/schema]` sensitive-key warnings in diagnostics

**Meaning:**
- `[config/schema] info` = sensitive key-path is env-backed; informational only.
- `[config/schema] action` = sensitive key-path is not env-backed; fix required.

**Fix / verification path:**
1. Move hardcoded secrets to env-backed references (`${VAR}` or `{"source":"env","id":"VAR"}`).
2. Re-run `py scripts/doctor.py`.
3. Confirm only informational schema signals remain.

### `openclaw gateway restart` fails with `MissingEnvVarError`

**Cause:** The live `openclaw.json` references `${OLLAMA_GPU_URL}`, `${VLLM_RUNPOD_URL}`, `${OPENAI_API_KEY}`, or `${ANTHROPIC_API_KEY}` via env-var substitution, but no `.env` file exists at `~/.openclaw/.env` to supply them. Bootstrap (v0.5.0+) now auto-seeds this file from `config/environments/dev-local.env.example` on first run.

**Fix:**
1. Re-run bootstrap: `py scripts/bootstrap.py --skip-ollama`
2. Or manually run: `py scripts/switch-model.py dev-local`
3. Then restart: `openclaw gateway restart`

### Post-doctor verification checklist (custom provider/model blocks)

After `openclaw doctor --fix` or manual config edits, run this strict checklist:
1. `py scripts/legacy/verify_openclaw_inventory.py`
   - Expect every check to print `PASS` and final `OVERALL: PASS`.
2. `py scripts/check-drift.py`
   - Expect `PASS` with no repo/runtime drift.
3. `py scripts/doctor.py`
   - Confirm runtime contract checks are healthy and deterministic.
4. `openclaw gateway status`
   - Confirm listener/RPC are healthy. If raw runtime still shows `unknown` on Windows, rely on the doctor runtime-contract normalization result.
5. If any inventory check fails, reconcile the exact field names from `config/openclaw.json.example`:
   - `models.providers` IDs (exact set, no missing/extra entries)
   - provider `models` aliases and their `name`/`api`
   - `agents.list` IDs
   - `tools.agentToAgent.allow`

---

## 18. CLI Reference

### `bootstrap.py`

```
python scripts/bootstrap.py [--skip-wsl] [--skip-ollama] [--skip-mcp]
                             [--primary-model MODEL] [--embed-model MODEL]
                             [--json-log]
```

Full setup: prerequisite checks, Ollama pulls, MCP config, prompt assembly.

### `switch-model.py`

```
python scripts/switch-model.py ENVIRONMENT [--dry-run] [--rollback]
                                           [--no-restart] [--json-log]
```

Environments: `dev-local`, `gpu-runpod`, `prod-cloud`, or any custom `config/environments/*.json`.

### `assemble-prompts.py`

```
python scripts/assemble-prompts.py [--variant {compact,standard,full}]
                                    [--dry-run] [--json-log]
```

Builds 15 SOUL.md prompts (5 agents x 3 variants) from base + overlays.

### `log-watcher.py`

```
python scripts/log-watcher.py [--once] [--dry-run]
                               [--env-file PATH] [--json-log]
```

Tails the gateway log, pushes traces to Langfuse, evaluates SOC alerts, monitors RunPod health.

### `serve-api.py`

```
python scripts/serve-api.py [--port 8420] [--host 127.0.0.1] [--reload]
```

Launches the FastAPI control plane.

### `gpu.py`

```
python scripts/gpu.py COMMAND [--dry-run] [--json-log]
```

GPU infrastructure lifecycle management. Model catalog in `config/model-catalog.json`.

| Subcommand | Purpose |
|:-----------|:--------|
| `deploy-pod` | Interactive model/GPU picker, provisions a RunPod pod with vLLM, switches gateway |
| `teardown` | Terminates the active pod and resets state to local |
| `health` | Probes vLLM `/v1/models` and `/health` endpoints |
| `status` | Shows active infrastructure (pod ID, URL, model, GPU) |
| `list-gpus` | Prints available GPU types with VRAM and pricing |

### `vet-install.sh`

```
bash scripts/vet-install.sh <skill-slug>
```

Safe skill installation with 48 vulnerability checks via skillvet.

---

## 19. API Reference

**Base URL:** `http://127.0.0.1:8420`

### GET /health

Returns system health.

```json
{
  "status": "ok",
  "gateway": "up",
  "runpod": "disabled|healthy|unhealthy",
  "langfuse": "enabled|disabled",
  "uptime_seconds": 42.7
}
```

### GET /status

Returns current deployment state.

```json
{
  "environment": "gpu-runpod",
  "model": "vllm-runpod/deepseek-r1-70b",
  "tier": "large",
  "variant": "full",
  "last_switch": "2026-03-08T14:30:00",
  "last_switch_success": true
}
```

### POST /switch

Body: `{"environment": "gpu-runpod", "dry_run": false}`

Returns the switch result including model, tier, and variant.

### GET /agents

Returns an array of all 5 agents with workspace paths and SOUL.md status.

```json
[
  {
    "id": "orchestrator",
    "name": "ORCHESTRATOR",
    "workspace": "/home/user/.openclaw/workspace-orchestrator",
    "soul_md_exists": true,
    "soul_md_chars": 5283
  }
]
```

### GET /runpod/health

Returns RunPod endpoint health (or `{"enabled": false}` when disabled).

### POST /runpod/scale

Body: `{"min_workers": 1, "max_workers": 3}`

### GET /metrics

Returns DX baseline metrics from `baselines.json`.

### GET /alerts

Returns SOC alert definitions from `alerts.json`.

### POST /prompts/assemble

Body: `{"variant": "full"}` or `{}` for all variants.

### POST /checkpoints

Body: `{"name": "pre-deploy", "workspace": "/path/to/workspace"}`

### GET /checkpoints?workspace=...

Lists all checkpoints for the given workspace.

### POST /checkpoints/restore

Body: `{"name": "pre-deploy", "workspace": "/path/to/workspace"}`

### WebSocket /logs

Streams gateway log entries as JSON objects in real-time.

---

## 20. Configuration Reference

### 20.1 openclaw.json

| Key | Type | Description |
|:----|:-----|:------------|
| `gateway.host` | string | Bind address (default: `127.0.0.1`) |
| `gateway.port` | int | Bind port (default: `18789`) |
| `models.providers.{name}.baseUrl` | string | Provider endpoint URL (supports `${VAR}`) |
| `models.providers.{name}.api` | string | API type (`ollama` for local Ollama, `openai-completions` for vLLM/cloud) |
| `models.providers.{name}.models[]` | array | Model definitions with `id`, `name`, `contextWindow` |
| `agents.defaults.model.primary` | string | Default model for all agents |
| `agents.defaults.thinkingDefault` | string | `off`, `low`, `medium`, `high` |
| `agents.defaults.verboseDefault` | string | `off`, `on`, `full` |
| `agents.list[]` | array | Agent registrations with `id`, `workspace`, `identity` |
| `bindings[]` | array | Channel routing rules |

### 20.2 model-tiers.json

| Key | Type | Description |
|:----|:-----|:------------|
| `tiers.{name}.contextBudget` | int | Max context window for this tier |
| `tiers.{name}.thinkingDefault` | string | Default thinking level |
| `tiers.{name}.promptVariant` | string | `compact`, `standard`, or `full` |
| `tiers.{name}.models[]` | array | Model IDs belonging to this tier |
| `variantOverlays.{variant}[]` | array | Overlay entries with `file` and `agents` filter |

### 20.3 gpu-runpod.json

| Key | Type | Description |
|:----|:-----|:------------|
| `runpod.gpuIds` | array | GPU type IDs (`AMPERE_80`, `ADA_80`, etc.) |
| `runpod.templateName` | string | RunPod template display name |
| `runpod.vllmImage` | string | Docker image for vLLM worker |
| `runpod.modelName` | string | HuggingFace model ID |
| `runpod.maxModelLen` | int | Max context length |
| `runpod.activeWorkers` | int | Min workers (always on) |
| `runpod.maxWorkers` | int | Max workers (auto-scales) |
| `runpod.idleTimeoutSeconds` | int | Worker idle timeout |
| `runpod.envVars` | object | Environment variables for the vLLM worker |
| `runpod.healthCheck.intervalSeconds` | int | Health check frequency |
| `runpod.healthCheck.unhealthyThreshold` | int | Failures before alerting |

### 20.4 permissions.json

| Key | Type | Description |
|:----|:-----|:------------|
| `autonomous` | array | Tools that execute without approval |
| `requires_approval` | array | Tools that halt for human confirmation |

---

## 21. Glossary

| Term | Definition |
|:-----|:-----------|
| **AKOS** | Agentic Knowledge Operating System |
| **HITL** | Human-in-the-Loop: requiring human approval before executing |
| **LLMOS** | Large Language Model Operating System |
| **MCP** | Model Context Protocol: standard for tool integration |
| **Plan Document** | Structured output from the Architect with actions, tools, and verification steps |
| **Delegation Plan** | Structured output from the Orchestrator with tasks, agents, and dependencies |
| **SOUL.md** | The system prompt file loaded by each agent at session start |
| **SSOT** | Single Source of Truth |
| **SOC** | Security Operations Center |
| **DX** | Developer Experience |
| **UX** | User Experience |
| **vLLM** | High-throughput LLM inference engine |
| **Overlay** | A prompt extension added to the base prompt for more capable models |
| **Tier** | Model capability classification: small, medium, large, SOTA |
| **Variant** | Prompt complexity level: compact, standard, full |
| **Fix Suggestion** | Verifier's diagnosis and recommended code change after a failure |
| **Checkpoint** | Tarball snapshot of an agent workspace for rollback |
| **Intelligence Matrix** | Fact-tagging pattern for source credibility and SSOT verification |
| **skillvet** | Security scanner for OpenCLAW community skills (48 vulnerability checks) |
| **ClawHavoc** | Active malware campaign targeting OpenCLAW users via malicious skills |
| **mcporter** | MCP server manager CLI |

---

## 22. What's New in v0.5.0

### Gateway Runtime Wiring
- **Per-agent tool profiles** enforced at gateway level — Madeira uses `coding` with curated `alsoAllow` plus `deny: ["write", "edit", "apply_patch", "exec"]`; Orchestrator and Architect use `minimal` with curated `alsoAllow`; Executor and Verifier use `coding` (Verifier denies `write`, `edit`, `apply_patch`)
- **Exec security mode** per agent — allowlist for Executor, deny for Architect; Orchestrator/Architect never have full exec
- **Gateway-level loop detection** — defense-in-depth with prompt-level loop detection; circuit breaker thresholds configurable
- **Agent-to-agent tool** for Orchestrator delegation — target allowlist restricts invokable agents
- **Session idle reset policy** — 60-minute idle timeout
- **Typing indicators** during agent processing (thinking mode)
- **Message status reactions** — queued/thinking/tool/done emoji on messages
- **Browser SSRF protection** — `dangerouslyAllowPrivateNetwork: false` by default

Bootstrap translates `config/agent-capabilities.json` into OpenClaw's runtime config. See [ARCHITECTURE.md](ARCHITECTURE.md#bootstrap-translation-layer-v050).

---

## 23. What's New in v0.4.0

### Runtime Convergence
- All 5 agents (Madeira, Orchestrator, Architect, Executor, Verifier) now deploy correctly during bootstrap
- Gateway health check returns actual status instead of "unknown"
- MCP paths resolve correctly on Windows, macOS, and Linux
- Bearer token authentication via `AKOS_API_KEY` environment variable

### Self-Verifying Agents
- Executor auto-verifies after every edit (lint/test check)
- Loop detection prevents infinite retry cycles (escalates after 3 attempts)
- All agents proactively write to MEMORY.md and MCP Memory store

### Structured Planning
- Multi-step tasks produce numbered plans with checkboxes
- Trivial tasks skip planning overhead automatically
- Customize agent behavior via RULES.md in each workspace

### Role Safety
- Tool access enforced by `config/agent-capabilities.json`, not just prompts
- Audit via `GET /agents/{id}/policy` and `GET /agents/{id}/capability-drift`

### Code Intelligence
- LSP and code-search MCP servers for type-aware navigation
- Research overlay with citation requirements for Architect

### Workflows
- 6 reusable workflow definitions in `config/workflows/`
- Invoke: analyze_repo, implement_feature, verify_changes, browser_smoke, deploy_check, incident_review

### Operator Tooling
- `py scripts/doctor.py` -- one-command health check
- `py scripts/sync-runtime.py` -- hydrate runtime from repo
- `py scripts/release-gate.py` -- unified release gate
- `py scripts/check-drift.py` -- detect repo-to-runtime drift
- `py scripts/browser-smoke.py` -- programmatic browser smoke test (6 scenarios)
- `py scripts/run-evals.py --dry-run` -- agent reliability eval runner (5 canonical tasks)
- `py scripts/checkpoint.py create|list|restore` -- workspace checkpoint CLI

### Context Pinning
- Pin files for agent focus: `POST /context/pin` with `{"path": "src/main.py"}`
- List pins: `GET /context/pins`
- Unpin: `DELETE /context/pin`

### Cost Tracking
- Cost breakdown (placeholder for Langfuse integration): `GET /metrics/cost`

### Governance and Templates
- Session templates in `config/templates/` (architecture review, bug investigation, safe refactor)
- Memory domain templates in `config/memory-templates/` (decisions, incidents, policies, sources)
- Governance policy packs in `config/policies/` (engineering-safe, compliance-review, incident-response)
- Workflow packs in `config/workflow-packs/` (release, backend)
- Rollback guide: `docs/uat/rollback_guide.md`

### Testing
- 193+ tests (up from 191)
- Live smoke tests: `py scripts/test.py live` (requires `AKOS_LIVE_SMOKE=1`)
- Release gate: `py scripts/release-gate.py`
- Browser smoke scenarios: `docs/uat/dashboard_smoke.md`

### Troubleshooting (v0.4.1)

**Gateway crashes with `MissingEnvVarError`:**
Re-run `py scripts/bootstrap.py --skip-ollama`. Bootstrap now strips providers with unset env vars (e.g., `${OLLAMA_GPU_URL}`) automatically.

**Only 2 agents visible in dashboard:**
Re-run `py scripts/bootstrap.py --skip-ollama` then `openclaw gateway restart`. Bootstrap now force-syncs all 5 agents.

**`openclaw doctor` reports unknown keys:**
AKOS-specific keys (`logging`, `permissions`) are now stored in `~/.openclaw/akos-config.json` instead of the gateway config. Re-run bootstrap to fix.

**`/status` returns all "unknown":**
This is normal before the first environment switch. Run `py scripts/switch-model.py dev-local` to activate.

## 19. HLK Operator Model

This section explains how to operate the Holistika Knowledge Vault through MADEIRA and the AKOS platform.

### 19.1 Three Layers You Should Understand

| Layer | What it is | Lifetime | Where it lives |
|:------|:-----------|:---------|:---------------|
| **Session** | A single conversation or workflow run | Temporary -- ends when the chat closes or the agent resets | Agent memory, chat history |
| **Workspace** | An agent's operating folder with identity, memory, and rules | Persists across sessions but is agent-scoped | `~/.openclaw/workspace-{agent}/` |
| **Vault** | The canonical business knowledge system | Permanent -- versioned in git, synced to Drive | `docs/references/hlk/` |

**Operating rule:** Session state is disposable. Workspace state helps agents remember context. The vault is the source of truth. Never rely on session memory for business facts -- always ground answers in the vault.

### 19.2 How You Use MADEIRA Day-to-Day

MADEIRA is your single entrypoint for HLK operations. You talk to MADEIRA. MADEIRA queries the vault.

**Common tasks and what to say:**

| Task | What to ask MADEIRA | Tool MADEIRA uses |
|:-----|:--------------------|:------------------|
| Find a role | "Who is the Data Architect?" | `hlk_role` |
| Check reporting chain | "Who does DevOPS report to?" | `hlk_role_chain` |
| List an area | "Show me all Research roles" | `hlk_area` |
| Find a process | "What is hol_resea_dtp_142?" | `hlk_process` |
| Explore a project | "What workstreams are under KiRBe Platform?" | `hlk_process_tree` |
| See all projects | "List all 11 projects" | `hlk_projects` |
| Find gaps | "What baselines need remediation?" | `hlk_gaps` |
| Search anything | "Find everything related to HUMINT" | `hlk_search` |

### 19.3 Adding Knowledge to the Vault

1. **Identify the owner** -- look up the role in `baseline_organisation.csv` that should own this knowledge.
2. **Navigate to the folder** -- go to `docs/references/hlk/v3.0/Admin/O5-1/{area}/{role}/`.
3. **Write markdown** -- create the document following the SOP-META envelope if it is a formal procedure.
4. **Register the process** -- if this is a new process, add a row to `process_list.csv` with the correct `item_parent_1`, `role_owner`, and `item_granularity`.
5. **Commit** -- git tracks the change. Drive syncs the folder.

### 19.4 Maintaining Baselines

The canonical baselines live in `docs/references/hlk/compliance/`:

| File | What to edit | When |
|:-----|:-------------|:-----|
| `baseline_organisation.csv` | Roles, hierarchy, access levels, descriptions | New role, role change, access review |
| `process_list.csv` | Processes, projects, workstreams, tasks | New process, hierarchy change, ownership change |
| `access_levels.md` | Access level definitions | Policy change (rare) |
| `confidence_levels.md` | Confidence level definitions | Policy change (rare) |
| `source_taxonomy.md` | Source categories and credibility levels | New source type (rare) |
| `PRECEDENCE.md` | What is canonical vs mirrored | Governance change |

**After editing baselines:** Restart the AKOS API (`py scripts/serve-api.py`) to reload the HLK registry from the updated CSVs.

### 19.5 Vault Structure Reference

```
docs/references/hlk/
  compliance/                     Shared governance baselines (SSOT)
  v3.0/                           Active vault (organigram-mirrored folders)
    Admin/
      O5-1/
        Research/                  Holistik Researcher area
        People/                   CPO area
        Operations/               COO area
        Finance/                  CFO area
        Marketing/                CMO area
        Data/                     CDO area
        Tech/                     CTO area
      AI/                         Susana Madeira / AIC chain
    Envoy Tech Lab/               KiRBe, MADEIRA, Showcases
    Think Big/                    Projects, Clients
  Research & Logic/               v2.7 historical reference (read-only)
```

### 19.6 Quick Reference Card

| Question | Answer |
|:---------|:-------|
| Where do I edit? | `docs/references/hlk/v3.0/` for documents, `compliance/` for baselines |
| Where do old docs live? | `Research & Logic/` (v2.7, read-only) |
| How does MADEIRA find things? | Via HLK MCP tools backed by `HlkRegistry` reading the canonical CSVs |
| What happens if I edit both vault and DB? | Vault wins. See `PRECEDENCE.md` for conflict resolution. |
| How do I restart after baseline edits? | `py scripts/serve-api.py --port 8420` |
| How do I check integrity? | `py scripts/test.py hlk` or use `/hlk/gaps` endpoint |
