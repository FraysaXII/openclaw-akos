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
22. [What's New in v0.5.0](#22-whats-new-in-v050)
23. [What's New in v0.4.0](#23-whats-new-in-v040)
24. [HLK Operator Model](#24-hlk-operator-model)

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

**See also:** [`guides/akos_content_navigator.md`](guides/akos_content_navigator.md) — one-screen index of where to find live prompts, answers, test content, and status surfaces (dossier console, both gateways, WIP dashboard, scenario CSV, cassettes, brand SSOT, decision logs).

---

## 2. Prerequisites

| Requirement | Minimum | Recommended |
|:------------|:--------|:------------|
| Python | 3.10+ (see repo `pyproject.toml` `requires-python`; `.python-version` pins **3.13** for dev) | 3.12+ |
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
# Optional — RunPod SDK (gpu-runpod, `scripts/gpu.py`):
pip install -r requirements-gpu.txt
# Optional — OpenStack SDK (ShadowGPU / `gpu-shadow`, `akos/openstack_provider.py`):
pip install -r requirements-openstack.txt
```

**Windows / Python 3.14 free-threaded:** If `pip install` tries to **build `cryptography` from source** and fails, install **OpenSSL** headers/libs and set **`OPENSSL_DIR`** to that prefix (vendor docs), **or** use CPython **3.13** / **3.12** where wheels exist, **or** install only `requirements.txt` without `requirements-gpu.txt` until wheels catch up.

The base `requirements.txt` dependencies are:

| Package | Purpose | Required? |
|:--------|:--------|:----------|
| `pydantic>=2.0` | Config validation and type safety | Yes |
| `pytest>=7.0` | Test suite | Yes (for dev) |
| `langfuse>=2.0` | Observability telemetry | Optional (graceful no-op) |
| `runpod>=1.7.0` (via `requirements-gpu.txt`) | RunPod GPU provider | Optional (graceful no-op) |
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
| `--primary-model MODEL` | Override primary model (default: `deepseek-r1:14b`) |
| `--embed-model MODEL` | Override embedding model (default: `nomic-embed-text`) |
| `--json-log` | Structured JSON log output |

### 3.3.1 Agent workspaces, SOUL.md, and OpenClaw "Bootstrap file"

OpenClaw `openclaw status --all` lists a **Bootstrap file** column per agent. AKOS satisfies this by deploying **`SOUL.md`** at the root of each agent workspace (`~/.openclaw/workspace-madeira`, `workspace-orchestrator`, `workspace-architect`, `workspace-executor`, `workspace-verifier`).

**Deterministic path (all five agents):**

1. `py scripts/assemble-prompts.py` — writes `prompts/assembled/*_PROMPT.{compact|standard|full}.md`.
2. `py scripts/bootstrap.py` — Phase 4 calls `deploy_soul_prompts()` (see `akos/io.py`), which copies the correct variant into each workspace as **`SOUL.md`**.

`py scripts/switch-model.py <profile>` also refreshes `SOUL.md` after merges. If any agent still shows **ABSENT**, re-run the steps above (do not rely on manual copy unless you accept drift from SSOT).

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

All configuration lives under the `config/` directory. Real `*.env` files are the operative runtime profiles in this workspace. Files ending in `.example` are reference templates only and should not be used directly by runtime paths.

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
    dev-local.env              Local env profile (operative)
    dev-local.env.example      Reference template
    gpu-runpod.json            RunPod overlay (full profile)
    gpu-runpod.env             RunPod env profile (operative)
    gpu-runpod.env.example     Reference template
    gpu-runpod-pod.env         RunPod dedicated pod env profile (operative)
    gpu-runpod-pod.env.example Reference template
    gpu-shadow.env             Shadow OpenStack env profile (operative)
    gpu-shadow.env.example     Reference template
    prod-cloud.env             Cloud API env profile (operative)
    prod-cloud.env.example     Reference template
    prod-cloud.json            Cloud API overlay
  eval/
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

**Agent tool policy:** In `agents.list[].tools`, use gateway core IDs for profile/deny semantics (`read`, `write`, `edit`, `apply_patch`, `exec`, etc.) and expose plugin-registered runtime tools through `alsoAllow`. Raw `mcporter` server entries do not become agent tools by themselves; AKOS bridges `hlk_*` and `finance_*` through the repo-managed `akos-runtime-tools` OpenClaw plugin. Do not rely on legacy `tools.allow` for plugin exposure.

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

Each deployment environment now has a real operative `*.env` file in the repo. `.env.example` files remain reference-only and should not be used directly by runtime commands.

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

**Ask vs Plan draft:** Madeira’s dashboard behaviour follows **`madeiraInteractionMode`** in `~/.openclaw/.akos-state.json` (defaults to **`ask`** — compact assembled prompt). Switch to **`plan_draft`** when you want structured plans plus a **JSON handoff** (`config/schemas/madeira-plan-handoff.schema.json`) for the Orchestrator swarm. Update mode via the control plane (`py scripts/serve-api.py` → `GET`/`POST http://127.0.0.1:8420/agents/madeira/interaction-mode`) or open **`http://127.0.0.1:8420/madeira/control`**. After changing mode with **redeploy** enabled, start a **new** WebChat session. **Run** (code/exec) remains the Orchestrator → Architect → Executor → Verifier path—not a Madeira mode.

**Role:** User-facing operational assistant for the Holistika knowledge vault.

**Mode:** Read-only lookup at the gateway. Cannot write files, execute commands, or use the browser. Code, browser automation, MCP-heavy mutations, and multi-step writes are classified via `akos_route_request` (`execution_escalate`) and handed to the **Orchestrator** for swarm execution (Architect → Executor → Verifier).

**Key behaviors:**
- **AKOS operator paths (Path 1–4):** Summarised in `prompts/base/MADEIRA_BASE.md` — simple inquiry stays in Madeira; canonical vault edits use the human git workflow in the repo; code/browser/MCP/registry mutations require switching to the **Orchestrator** agent in the dashboard (swarm path). Do not confuse these labels with Holistika methodology “pillars” (programme language).
- **Lookup mode (default):** Answers factual HLK questions directly using `hlk_*` tools, citing canonical sources. Open-web or narrative reasoning does not replace `hlk_*` for organisational facts.
- **Deterministic search ladder:** tries exact role/process lookup first when the intent is specific, retries with `hlk_search` in the same turn on `not_found`, and answers directly when a clear best match exists.
- **Summary mode:** Synthesises multi-tool answers with structured formatting.
- **Escalation mode:** Acknowledges multi-step admin requests (`admin_escalate`) or execution requests (`execution_escalate`) and delegates to the Orchestrator using the handoff pattern in `MADEIRA_BASE.md`.
- **`sequential_thinking`:** Allowed for post-tool disambiguation, synthesis, and escalation packaging—not to guess vault facts without retrieval.
- **Compact tier:** Small models still receive `OVERLAY_HLK_COMPACT.md` and `OVERLAY_STARTUP_COMPACT.md` so HLK and startup invariants are not dropped when `model-tiers.json` selects the `compact` variant.
- Never responds with generic "check your HR system" fallbacks when HLK tools are available.
- Never asks the user whether it should search; search is part of the lookup job.

**Madeira vs Executor:** Use Madeira for HLK/finance lookups and read-only guidance. Use the swarm (starting with Orchestrator) for anything that mutates repos, runs shell/browser automation, or drives MCP writes.

**Workspace:** `~/.openclaw/workspace-madeira/` (scaffold includes `WORKFLOW_AUTO.md`, `MEMORY.md`, and `memory/README.md` describing `memory/YYYY-MM-DD.md` continuity notes).

**Further UAT:** Execution-layer checks live in [`docs/uat/dashboard_smoke.md`](uat/dashboard_smoke.md).

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

**Mode:** Read-focused validation. Can run validation commands and browser checks, but does not mutate production files directly.

**Key behaviors:**
- Runs linters, test suites, build commands, and browser screenshots.
- Classifies results as PASS, FAIL, or SKIP.
- On failure: diagnoses root cause, suggests a targeted fix with confidence rating (HIGH/MEDIUM/LOW).
- Escalates to Orchestrator after 3 failed fix attempts.

**Workspace:** `~/.openclaw/workspace-verifier/`

### 5.7 Selecting Agents

Agents are available via the OpenCLAW WebChat dashboard (`openclaw dashboard`). Select an agent from the sidebar.

- **Start with Madeira** for HLK operations -- role lookups, process navigation, gap detection, vault searches.
- On **medium+ models** (`standard` / `full` prompt variants), Madeira also supports **day-to-day ops help**: standup outlines, email **drafts** (explicitly non-canonical until verified), meeting prep, and a structured **handoff pack** when escalating to the Orchestrator. Canonical registry changes still require the swarm path.
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
| `OVERLAY_HLK_COMPACT.md` | Madeira (`compact` only) | Short HLK ladder, anti-fabrication, citation rules |
| `OVERLAY_STARTUP_COMPACT.md` | Madeira (`compact` only) | Mandatory startup reads and memory note pattern |
| `OVERLAY_MADEIRA_OPS.md` | Madeira (`standard` / `full` only) | Day-to-day drafts, checklists, Orchestrator handoff pack (governance-safe) |
| `OVERLAY_MADEIRA_PLAN_DRAFT.md` | Madeira (appended at deploy when `plan_draft`) | Plan draft banner, JSON handoff requirements (non-canonical) |
| `OVERLAY_ORCHESTRATOR_MADEIRA_HANDOFF.md` | Orchestrator (`standard` / `full`) | Consume Madeira structured handoff JSON |
| `OVERLAY_ARCHITECT_MADEIRA_HANDOFF.md` | Architect (`standard` / `full`) | Treat Madeira plan JSON as draft input; re-ground with `hlk_*` |

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
| `dev-local` | `ollama/deepseek-r1:14b` | medium | Local development; `switch-model.py dev-local` applies this profile directly |
| `gpu-runpod` | `vllm-runpod/deepseek-r1-70b` | large | Remote GPU, full capabilities |
| `prod-cloud` | `anthropic/claude-sonnet-4` | large | Cloud APIs, production |

### 7.2 Switching Environments

```bash
python scripts/switch-model.py dev-local       # Local Ollama
python scripts/switch-model.py gpu-runpod       # RunPod GPU
python scripts/switch-model.py prod-cloud       # Cloud APIs
```

Preferred operator flow:

1. `py scripts/doctor.py --repair-gateway`
2. `py scripts/switch-model.py <profile>`
3. `py scripts/gpu.py` only when the chosen profile needs external GPU provisioning
4. Re-run `py scripts/doctor.py` and provider-specific health checks

**AKOS vs OpenClaw hot-switch contract:** `scripts/switch-model.py` is the **authoritative** merge + prompt deploy + gateway restart for model/environment changes. `POST /switch` on the FastAPI control plane is the HTTP automation surface for the same **class** of operations and does **not** replace gateway repair (`doctor.py`). Optional **Neo4j / Streamlit** tooling never runs inside the OpenClaw gateway; the graph explorer is supervised only from `scripts/serve-api.py`.

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

2. Create `config/environments/my-env.env` with any required env vars.
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
3. Edit the real env file `config/environments/gpu-runpod.env`.
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

If endpoint creation is blocked by account state or worker policy, use the exact operator steps in [`docs/uat/gpu_provider_unblock_checklist.md`](uat/gpu_provider_unblock_checklist.md).

### 8.4 Serverless Configuration

The full RunPod profile in `config/environments/gpu-runpod.json`:

| Field | Description | Default |
|:------|:------------|:--------|
| `gpuIds` | GPU types to use | `["AMPERE_80", "ADA_80_PRO"]` |
| `templateName` | RunPod template name | `akos-vllm-deepseek-r1-70b-awq` |
| `vllmImage` | Docker image for vLLM worker | `runpod/worker-v1-vllm:v2.14.0` |
| `modelName` | HuggingFace model ID | `casperhansen/deepseek-r1-distill-llama-70b-awq` |
| `maxModelLen` | Maximum context length | `32768` |
| `activeWorkers` | Min workers (always on) | `0` |
| `maxWorkers` | Max workers (scales up) | `1` |
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

The dedicated pod profile lives in `config/environments/gpu-runpod-pod.json`. It shares the same vLLM tuning parameters as the serverless profile but targets a persistent pod instead of a serverless endpoint. Normal runtime use only needs the pod's `VLLM_RUNPOD_URL`, but the `deploy-pod` provisioning flow still requires `RUNPOD_API_KEY` to create or terminate the pod.

#### Setup

Deploy a dedicated vLLM pod with a single command:

```bash
python scripts/gpu.py deploy-pod
```

The interactive flow:

1. **Select a model** from `config/model-catalog.json` (the GPU model SSOT). The picker shows parameter count, VRAM requirement, reasoning capability, and tool-call parser for each entry.
2. **Select a GPU** type and count. The CLI recommends a default based on the model's VRAM needs and computes the minimum GPU count automatically.
3. **Confirm and deploy**. The CLI provisions a pod on RunPod with the `vllm/vllm-openai:v0.16.0` image, passes the correct vLLM flags (including `--tool-call-parser`, `--reasoning-parser` when applicable), switches the gateway to the new endpoint, and persists the URL to both the repo `.env` and `~/.openclaw/.env`.

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

#### 8.7.1 Endpoint URL alias seam (D-IH-58-G)

Some external tools (and the I58 long-lived `~/.openclaw/.env` block) refer to the same endpoints with alias names: `RUNPOD_ENDPOINT_URL` (alias for `VLLM_RUNPOD_URL`) and `KALAVAI_ENDPOINT_URL` (alias for `VLLM_SHADOW_URL`). The single source of truth for resolving these is `akos.runpod_provider.resolve_endpoint_url(kind)`:

```python
from akos.runpod_provider import resolve_endpoint_url

url = resolve_endpoint_url("runpod")   # VLLM_RUNPOD_URL > RUNPOD_ENDPOINT_URL
url = resolve_endpoint_url("shadow")   # VLLM_SHADOW_URL > KALAVAI_ENDPOINT_URL
```

Precedence is fixed: the canonical `VLLM_*` name always wins when set. The alias fills in only when the canonical is unset or empty. **Empty alias values never shadow a populated canonical.** This means you can safely keep both pairs in `~/.openclaw/.env` for external-tool compatibility — the AKOS runtime ignores the aliases whenever the canonical names are populated.

### 8.8 ShadowGPU (OpenStack cloud)

**ShadowGPU** is Shadow’s cloud GPU service: you connect through **OpenStack** (API, CLI, or Horizon) to run workloads on their EU GPU fleet. It is the sovereign-EU vLLM alternative to RunPod for this repo’s `gpu-shadow` profile. **ShadowPC** is a separate product (the local Windows dev/gaming machine); do not conflate the two when talking to operators or vendors.

The `gpu-shadow` profile deploys vLLM through cloud-init onto a ShadowGPU instance and then points the gateway at the instance's floating IP.

Setup flow:

1. Edit the real env file `config/environments/gpu-shadow.env`.
2. Fill in your OpenStack auth values or set `OS_CLOUD` to a working `clouds.yaml` entry.
3. Run a dry-run first:

```bash
python scripts/gpu.py deploy-shadow --dry-run
```

4. Then deploy:

```bash
python scripts/gpu.py deploy-shadow
```

Current known-good ShadowGPU / tenant defaults (check Skyline for your project):

- Image: `Ubuntu-22.04`
- Flavor: `power-c32m112-gpu-A4500-4`
- Model profile: `casperhansen/deepseek-r1-distill-llama-70b-awq`

Operational note:

- Some ShadowGPU tenants forbid security-group creation through policy. If that happens, AKOS now falls back to project-default networking instead of failing the deploy before instance creation.
- If compute server creation is blocked by role/policy, use the exact operator steps in [`docs/uat/gpu_provider_unblock_checklist.md`](uat/gpu_provider_unblock_checklist.md) (and coordinate with the ShadowGPU operator for `servers:create` if needed).

---

## 9. MCP Server Ecosystem

### 9.0 Operator paths (script spine)

| Goal | Command | Notes |
|:-----|:--------|:------|
| First-time workspace + gateway prep | `py scripts/bootstrap.py` | Does not require Neo4j |
| Health + gateway repair | `py scripts/doctor.py` / `py scripts/doctor.py --repair-gateway` | Same paths as release gate hints |
| Control plane API + optional graph stack | `py scripts/serve-api.py` | When `NEO4J_*` is non-placeholder and Bolt is up, **Streamlit** `hlk_graph_explorer.py` may auto-start as a **child process**; stdout line `AKOS_GRAPH_EXPLORER_URL=…`; `GET /health` exposes `graph_explorer` + `neo4j_mirror`. CI/headless: `--no-graph-explorer` or `AKOS_GRAPH_EXPLORER=0` |
| Thin dispatcher (same scripts) | `py scripts/akos_operator.py serve-api` / `doctor` / `bootstrap` / `test` | Forwards only; no duplicate logic |
| HLK graph tests | `py scripts/test.py graph` | `pytest -m graph`; live Bolt subset: `python -m pytest -m "graph and neo4j"` with `NEO4J_*` set |

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
| `hlk_projects()` | List all 11 top-level projects with child counts (process inventory is larger; see ARCHITECTURE HLK registry counts) |
| `hlk_gaps()` | Identify items with missing metadata, TBD owners, or empty descriptions |
| `hlk_search(query)` | Fuzzy search across roles and processes by name, description, or ID |

**Data source:** All tools read from the canonical vault CSVs (`docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/baseline_organisation.csv` and `process_list.csv`). The CSVs remain SSOT; optional Neo4j (below) is a mirrored index only.

**Setup:** Requires `pip install mcp`. No API keys needed. Prompt behaviour: `OVERLAY_HLK.md` plus `OVERLAY_HLK_GRAPH.md` (standard/full variants in `config/model-tiers.json`) teach graph tools; compact Madeira uses `OVERLAY_HLK_COMPACT.md` only (no `hlk_graph_*` in prompt ladder).

### 9.10 HLK Graph (optional Neo4j mirror)

When operators enable Neo4j (`NEO4J_URI`, `NEO4J_PASSWORD`, optional `NEO4J_USERNAME` in `~/.openclaw/.env`, same file as Langfuse), agents gain **read-only** multi-hop helpers. **`py scripts/serve-api.py`** may **auto-sync** the mirror when canonical CSV fingerprints drift (`validate_hlk.py` then `sync_hlk_neo4j.py`, file lock, state under `~/.openclaw/.akos-neo4j-sync-state.json`). Set `AKOS_NEO4J_AUTO_SYNC=0` to disable. Operators may still run `py scripts/sync_hlk_neo4j.py` manually (add `--with-documents` to project v3.0 markdown `Document` nodes and internal `LINKS_TO` edges; set `AKOS_NEO4J_SYNC_WITH_DOCUMENTS=1` for the automated path).

**Production operations (mirrored class):**

1. **Bring-up (Neo4j Aura — recommended):** In the Aura console, copy the connection URI. Prefer `neo4j+s://…` when system CAs validate the chain. If you hit `SSLCertVerificationError`, prefer fixing trust (install the inspecting CA); otherwise set **`NEO4J_URI=neo4j+ssc://…`** directly (typical stable choice on some networks) and **leave `NEO4J_TRUST` unset**. Alternatively, keep `neo4j+s://…` and set `NEO4J_TRUST=all` so the driver rewrites to `neo4j+ssc` (weaker than full CA pin — see `SECURITY.md` §4a). Put `NEO4J_URI`, `NEO4J_USERNAME`, and `NEO4J_PASSWORD` in `~/.openclaw/.env` only (same bootstrap as the control plane).
2. **Bring-up (local Docker — optional dev only):** `docker compose -f compose.neo4j.yml up -d` is for a **local** Community Edition mirror, not a substitute for Aura. Then use `bolt://127.0.0.1:7687` (or `bolt+ssc://` if you enable strict TLS locally) in `NEO4J_URI`.
3. **Populate / refresh:** After any merge that changes canonical CSVs (or when enabling document projection), run `py scripts/sync_hlk_neo4j.py` from the repo root; use `--dry-run` first in automation. Expect non-zero exit on validation/connection failure. Successful runs log counts such as `roles_written`, `processes_written`, `edges_written`.
4. **Health:** `GET /hlk/graph/summary` returns `neo4j: connected` when the driver works; neighbourhood routes return `503` when Neo4j is unset or down (by design).
5. **Backup / DR:** Prefer **rebuild from git** (re-run `validate_hlk.py`, `sync_hlk_neo4j.py`) as the canonical recovery for mirrored data. For enterprise retention, use Neo4j’s own backup tooling; never treat the database as SSOT ([`PRECEDENCE.md`](references/hlk/compliance/PRECEDENCE.md)).

| Surface | Purpose |
|:--------|:--------|
| MCP server `hlk-graph` in `config/mcporter.json.example` | `hlk_graph_summary`, `hlk_graph_process_neighbourhood`, `hlk_graph_role_neighbourhood` |
| REST `GET /hlk/graph/summary` etc. | Same data via FastAPI when `scripts/serve-api.py` is running |
| `GET /hlk/graph/explorer` | **Primary** operator UI (`static/hlk_graph_explorer.html` + vis-network CDN): summary cards; **registry pickers** (areas, roles, projects, children, `/hlk/search`) feed the graph—same SSOT as `/hlk/*`; depth/limit sliders; **node size basis** (children / degree / balanced) and **edge label mode** (auto / always / hover-only) with **sessionStorage** persistence and **re-render without re-fetch**, aligned with the Streamlit explorer’s PARENT_OF / OWNED_BY sizing and edge colour/abbrev conventions; **zoom-out landmark labels** (names on the largest hubs only until you zoom back in); optional API key in **sessionStorage** only; same `Authorization: Bearer` as other `/hlk/*` routes when `AKOS_API_KEY` is set |
| `scripts/hlk_graph_explorer.py` | **Secondary** Streamlit UI: same registry + `/hlk/search` + `/hlk/graph/*` as the HTML explorer. **Single canvas**; lenses **Role / Process / Saved**; **force vs tree** layout (vis hierarchical + BFS levels from API root; auto **force** fallback when a `REPORTS_TO` cycle blocks tree levels); **force-directed physics** (tuned `barnesHut`) with optional **NetworkX initial seed** or **lock layout** (static freeze, force mode only); **graph engine** `streamlit-agraph` (default) or **`vis_component`** — local `streamlit.components.v1` bundle at `static/streamlit_components/hlk_vis_network/` (vis-network CDN) for **drag-end pin / magnetic MVP** with state echoed to the Python session and the same **zoom-out hub labels** as the HTML explorer (`streamlit-agraph` cannot hook vis zoom for this); **semantic node colours** (label family + stable id hue nudge) and **relationship-coloured edges** (abbrev labels + rich **hover `title`**); **node size basis** (PARENT_OF children for processes, OWNED_BY fan-in for roles, or degree / balanced); **edge label mode** auto/always/hover-only; **colour & link legend** expander; **selected node** detail expander; **bulk discovery** (merge cap + batch sizes); **label focus** + **highlight substring**; **Save lens** preset **v2**, **Apply & fetch**, **Re-fetch current**; tab **favicon** `static/hlk_graph_explorer_favicon.png`; shell links to `{AKOS_API_URL}/hlk/graph/explorer`, `/docs`, optional **`AKOS_WEB_DASHBOARD_URL`**. CDN-blocked drag workflows: use **HTML** explorer or the vis component path per sidebar help. Run **`py scripts/hlk_graph_explorer.py`** or **`py -m streamlit run scripts/hlk_graph_explorer.py`**. Requires **`py scripts/serve-api.py`** on `AKOS_API_URL` (default 8420). |

**Control plane default URL and port conflicts:** Run `py scripts/serve-api.py` (default **`http://127.0.0.1:8420`**). Graph explorer: **`http://127.0.0.1:8420/hlk/graph/explorer`**. If startup fails with *address already in use* (Windows: `WinError 10048`), `scripts/serve-api.py` exits early with a stderr hint. If **`GET /hlk/graph/summary` returns 404** but `/docs` returns 200, another application may be bound to 8420 (stale build without graph routes): on Windows run `netstat -ano | findstr :8420`, identify the PID (`tasklist /FI "PID eq <pid>"`), stop that process, then restart `serve-api.py`. For `py scripts/browser-smoke.py` against a different port, set **`AKOS_BROWSER_SMOKE_API_URL`** (see script docstring).

**Operator UAT:** Record thorough dashboard + Neo4j checks using [`docs/wip/planning/07-hlk-neo4j-graph-projection/reports/uat-neo4j-graph-evidence-template.md`](wip/planning/07-hlk-neo4j-graph-projection/reports/uat-neo4j-graph-evidence-template.md) or a dated copy under the same `reports/` folder. For **Cursor / agent-driven browser** UAT against the embedded explorer, see [`cursor-browser-mcp-graph-explorer.md`](wip/planning/07-hlk-neo4j-graph-projection/reports/cursor-browser-mcp-graph-explorer.md).

**Control-plane explorer note:** The embedded page loads **vis-network** from jsDelivr. Locked-down environments may block that CDN; use REST/MCP or Streamlit in those cases.

**Recommended validation prompts:**
- `Who is the CTO?`
- `Show me all Research roles.`
- `What workstreams are under KiRBe Platform?`
- `I want to add a new process under the Data Governance project.`

---

## 10. Tool Permissions and HITL Gates

### 10.1 Classification

Every tool is classified in `config/permissions.json` as either **autonomous** (no approval needed) or **requires_approval** (human must confirm).

`permissions.json` includes a mix of gateway core IDs, plugin tool IDs, and AKOS logical aliases. In the live gateway template, use gateway core IDs such as `read`, `write`, `edit`, `apply_patch`, and `exec`, then expose plugin-registered runtime tools through `tools.alsoAllow`. For AKOS HLK and finance lookups, the runtime registration is provided by `openclaw-plugins/akos-runtime-tools`, not by `mcporter.json` alone.

**Autonomous tools** (examples):
`read`, `web_search`, `web_fetch`, `memory_search`, `memory_get`, `sequential_thinking`, `finance_quote`, `finance_search`, `finance_sentiment`, `hlk_role`, `hlk_role_chain`, `hlk_area`, `hlk_process`, `hlk_process_tree`, `hlk_projects`, `hlk_gaps`, `hlk_search`, `hlk_graph_summary`, `hlk_graph_process_neighbourhood`, `hlk_graph_role_neighbourhood`

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

Langfuse is the primary observability backend. It provides per-request agent traces, answer-quality telemetry, model comparison, and cost tracking.

**Setup:**

1. Sign up at [cloud.langfuse.com](https://cloud.langfuse.com) (free tier) or self-host.
2. Put `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, and `LANGFUSE_HOST` into `~/.openclaw/.env` or export them in the process environment.
3. Keep non-secret watcher settings in `config/openclaw.json.example` under `diagnostics.logWatcher` (bootstrap writes them to `~/.openclaw/akos-config.json`).
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
| `--environment`, `-e` | Environment tag (dev-local, gpu-runpod, prod-cloud) |
| `--json-log` | Structured JSON output |

**Environment:**
- `LANGFUSE_PUBLIC_KEY` -- your Langfuse public key
- `LANGFUSE_SECRET_KEY` -- your Langfuse secret key
- `LANGFUSE_HOST` -- Langfuse endpoint (default: `https://cloud.langfuse.com`)
- `LOG_WATCHER_POLL_INTERVAL` -- optional environment override; otherwise `diagnostics.logWatcher.pollIntervalSeconds` is used

**Per-environment Langfuse setup (Phase 10):**

All real environment profiles under `config/environments/*.env` include the Langfuse placeholders (`LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, `LANGFUSE_HOST`) needed by runtime. When you run `py scripts/switch-model.py <env>`, the selected real env profile is copied into `~/.openclaw/.env`. The repo no longer uses `config/eval/langfuse.env`.

**Startup compliance tracing:**

The log watcher now detects "Post-Compaction Audit" gateway entries and sends scored traces to Langfuse (`startup_compliance: 0.0` for failures, `1.0` for passes). It also reviews Madeira session transcripts and emits `answer_quality` traces plus a local jsonl mirror under `~/.openclaw/telemetry/`. When residual flags fire (for example internal tool strings in user-visible text, pseudo `hlk_*/` paths, or UUID-shaped tokens on HLK-classified turns without `hlk_*` tool calls), matching rows in `config/eval/alerts.json` raise real-time alerts forwarded through the same telemetry path. This enables monitoring startup compliance rates, grounding quality, and flagship UX residuals across models and environments.

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
   If it prints "Test trace sent to Langfuse successfully", check the Tracing tab (traces may take a few seconds to appear). If it fails, ensure `~/.openclaw/.env` has valid `LANGFUSE_PUBLIC_KEY` and `LANGFUSE_SECRET_KEY`.
3. **Confirm log path** — The watcher reads `%TEMP%\openclaw\openclaw-YYYY-MM-DD.log` (Windows) or `/tmp/openclaw/openclaw-YYYY-MM-DD.log` (Linux). Ensure the OpenCLAW gateway writes there.

#### 12.2.0 Langfuse metadata contract and volume controls

Canonical metadata keys and SOC rules live in [docs/ARCHITECTURE.md](ARCHITECTURE.md) (Langfuse metadata contract). In short: only short categorical strings (for example `EU-AIA-1`, `hlk_surface=log_watcher`, `hlk_tool=hlk_role`, `compliance_family=hlk_csv`); never paste secrets, prompts, or CSV rows into Langfuse fields.

- **`LANGFUSE_TRACE_SAMPLE_RATE`** — unset or `1` = send all traces. Set to a decimal between `0` and `1` to probabilistically drop trace roots (use for load tests or deliberate prod sampling).
- **Eval / datasets** — filter the Langfuse UI by tags and metadata keys above. For a scripted list of recent trace ids matching a tag, run `py scripts/langfuse_list_traces_by_tag.py --tag <tag> --limit 50` (requires the same `LANGFUSE_*` credentials as the watcher).

#### 12.2.1 Langfuse Trace Taxonomy

All traces emitted by the log watcher and telemetry module follow a consistent naming convention. Use these patterns when building Langfuse dashboard filters and score queries.

| Trace Name Pattern | When Fired | Score | Description |
|:-------------------|:-----------|:------|:------------|
| `akos-{agent_role}` | Every agent request | -- | Per-request agent activity trace |
| `akos-startup-{agent_role}` | Session startup | `startup_compliance: 0.0/1.0` | Startup file read compliance |
| `akos-eval-{task_id}` | Eval run | `eval_pass: 0.0/1.0` | Agent reliability eval result |
| `akos-alert-{severity}` | SOC alert fired | `soc_alert: 0.25-1.0` | SOC alert forwarded to Langfuse |
| `akos-answer-quality-{agent_role}` | Flagship user-visible answer | `answer_quality`, `citation_present`, `compaction_clean` | Local + Langfuse answer-quality event from session review |
| `akos-metric-{name}` | Periodic (every 100 entries) | -- | DX metric sample (latency, count) |
| `akos-health-runpod` | Periodic health check | -- | RunPod/vLLM infrastructure health |

Scores with a `0.0/1.0` range are boolean pass/fail. The `soc_alert` score maps severity to a float: `CRITICAL=1.0`, `HIGH=0.75`, `MEDIUM=0.5`, `LOW=0.25`.

#### 12.2.2 Langfuse Dashboard Setup Guide

Follow these steps to build a monitoring dashboard from AKOS traces.

**1. Create a Langfuse project and get API keys:**

Sign up at [cloud.langfuse.com](https://cloud.langfuse.com) (free tier is sufficient). Create a project, then go to **Settings > API Keys** and copy the public and secret keys.

**2. Configure credentials:**

Edit `~/.openclaw/.env` and fill in:

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

Then open the **Tracing** tab in Langfuse. A test trace should appear within a few seconds. If it doesn't, double-check the keys in `~/.openclaw/.env`. If the dashboard still stays empty while the local watcher is emitting mirror files in `~/.openclaw/telemetry/`, treat that as a project/account alignment issue rather than a repo-side watcher failure.

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

### 14.3 OpenClaw gateway security audit

After material changes to gateway bind addresses, authentication, plugins, tool allowlists or denylists, DM/group exposure, or agent tool profiles, run:

```bash
openclaw security audit
```

Use `openclaw security audit --deep` when diagnosing suspected over-exposure or incident-style review. Optional `--fix` applies safe remediations when the CLI offers them. Treat this as part of operator hygiene alongside tightening tool blast radius before widening network access.

**Interpreting common findings (AKOS dev-local / native Windows):**

| OpenClaw signal | Typical meaning | AKOS response options |
|:----------------|:----------------|:------------------------|
| **CRITICAL** — small models with ambient web tools and sandboxing off | OpenClaw may still flag conservative risk if local models are tiny and many tools are enabled. | AKOS SSOT now uses **Path B** (`agents.defaults.sandbox.mode: strict`, `tools.exec.host: sandbox`) and **Path C** (no `web_search` / `web_fetch` on Orchestrator/Architect; Architect keeps sandboxed `browser`). Prefer **medium+ tiers** for tool-heavy Madeira; see §14.3a–b. |
| **WARN** — `tools.exec.host` sandbox vs `sandbox.mode` off | Mismatch between exec plane and session sandbox flags. | With AKOS template, both should align (**`strict`** + **`sandbox`**). If your OS cannot host sandboxed exec, use **WSL2** or **Docker Desktop 4.58+** sandboxes per §14.3b, then re-run `openclaw security audit`. |
| **WARN** — `gateway.trustedProxies` empty | Expected when `gateway` bind is **loopback-only** and Control UI is not behind a reverse proxy. | No action until you terminate TLS or expose the dashboard through a proxy; then set trusted proxy CIDRs per OpenClaw docs. |
| **WARN** — `gateway.nodes.denyCommands` ineffective entries | OpenClaw matches **exact command IDs**, not free-text shell fragments. | Replace entries with exact IDs from the audit message (for example `canvas.present`, `canvas.eval`, …) or remove stale rows. |

**Commands (stack vs gateway-only):**

- `openclaw gateway status` / `openclaw gateway status --deep` — service + **RPC** probe to `ws://127.0.0.1:18789`.
- `openclaw status` / `openclaw status --all` / `openclaw status --deep` — broader local diagnosis (agents, providers, pasteable report). Prefer `--all` when sharing output (tokens redacted).

**Madeira note:** The gateway `deny` list and minimal profile are the backstop against prompt injection expanding effective permissions. Prefer instruction-hardened **medium-tier or larger** models for tool-heavy Madeira sessions; very small local models carry higher injection risk when many tools are enabled.

### 14.3a Research without `web_search` / `web_fetch` (Path C)

Orchestrator and Architect no longer expose `web_search` / `web_fetch`. Use this **decision tree**:

1. **Org / registry facts** — `hlk_role`, `hlk_search`, and related `hlk_*` tools (same ladder as Madeira).
2. **Structured relationships** — When Neo4j is configured, `hlk_graph_*` tools; if graph is off, say so and stay on CSV-backed tools.
3. **Public documentation** — Architect may use the coarse **`browser`** tool (SSRF policy in `openclaw.json.example`) for vendor or standards pages—not for inventing Holistika org truth.
4. **Side effects / unclear routing** — Escalate to Orchestrator → Executor per delegation prompts.

If MCP is degraded or unreachable, answer with explicit **D3** uncertainty—do **not** fill gaps from unconstrained web guesses.

### 14.3b Strict sandbox on Windows (Path B + Docker / WSL2)

Native Windows may not provide the isolation OpenClaw expects for **`sandbox.mode: strict`** and **`tools.exec.host: sandbox`**. Mitigations (pick one or combine):

1. **Docker Desktop 4.58+** — Enable features required for [Docker Desktop sandboxes](https://docs.docker.com/ai/sandboxes/docker-desktop/) (microVM + isolated daemon + workspace sync). Use host **File Sharing** so `~/.openclaw` and your repo root are visible to the VM. Optional: `docker sandbox network proxy` / `docker sandbox network log` for egress visibility.
2. **WSL2 (Ubuntu recommended)** — Run Ollama + OpenClaw gateway inside Linux; browse WebChat from Windows to `127.0.0.1:18789`.
3. **Doctor hints** — `py scripts/doctor.py` prints **WARN** (non-fatal) lines about Docker CLI / WSL presence on Windows to remind operators of the above.
4. **Engine pipe check** — `py scripts/doctor.py --docker-sandbox` verifies the Docker engine IPC endpoint (named pipe or UNIX socket) within about two seconds and exits non-zero when it cannot connect. Tier-3 Playwright runs can optionally set **`AKOS_REQUIRE_DOCKER_PREFLIGHT=1`** so `py scripts/browser-smoke.py --playwright` fails fast with the same hygiene (default remains warn-only for CI laptops without Docker). (internal tool leakage, pseudo HLK paths, or UUID-shaped answers without `hlk_*` tool use), treat it like a narrow incident: pause or tighten tools if needed, review recent sessions, rotate secrets if compromise is suspected, then re-run the audit above.

**OpenClaw CLI upgrade:** After `openclaw update`, restart the gateway and run `openclaw status --all`, `py scripts/doctor.py`, and AKOS gates (`verify_openclaw_inventory`, `check-drift`, `release-gate` or full matrix in `docs/DEVELOPER_CHECKLIST.md`). See [CONTRIBUTING.md](../CONTRIBUTING.md) — OpenClaw CLI upgrades.

### 14.4 Reporting Vulnerabilities

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
| `--axe` | **(Initiative 54 P1)** Run axe-core a11y audit on Playwright-loaded pages (today: `/madeira/control`). Requires `axe-playwright-python` from `requirements-dev.txt` (`pip install -r requirements-dev.txt`). SKIPs gracefully when the dev dep is not installed (R-54-1 / R-54-4). Fail bar: any **Critical** axe finding = release-gate fail (D-IH-54-A); **Serious** is warn-only at first run, escalates after one clean cycle. Combine with `--playwright`: `py scripts/browser-smoke.py --playwright --axe`. |

If Playwright is not installed, `--playwright` is skipped with a clear message. The release gate runs browser smoke when Playwright is available.

**Initiative 54 — Surface a11y hardening:** the `playwright_a11y_smoke` profile in `config/verification-profiles.json` runs the new `tests/playwright/` DOM-source contract tests (without Playwright installed; ~0.25s) plus `py scripts/browser-smoke.py --playwright --axe` (when the dev tooling is installed). This profile is opt-in at pre-commit (warn-only on Critical) and Critical-only-blocking at release-gate (D-IH-54-B split runner). See [`docs/wip/planning/54-surface-test-hardening/`](wip/planning/54-surface-test-hardening/) for the full operator-side install path + audit-report contract.

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

### Windows: dashboard unreachable or `port already in use` after reboot

**Cause:** The OpenClaw gateway supervisor and a crashed/orphan Node listener can disagree; `gateway stop` may not free TCP `18789`, so the supervised service cannot bind on restart.

**Fix (preferred):**

```bash
py scripts/doctor.py --repair-gateway
```

This runs the same sequence as `scripts/switch-model.py` after a profile switch: upstream OpenClaw doctor repair, gateway stop, Windows-only release of stale listeners on port 18789, then gateway start. Use `py scripts/doctor.py --force-gateway-repair` if the upstream doctor supports a more aggressive repair flag.

If the dashboard still does not answer, confirm the OpenClaw CLI is on PATH as `openclaw`, `openclaw.cmd`, or `openclaw.exe` (npm shims on Windows). If `openclaw gateway install --force` fails with access denied, re-run the installer command from an elevated PowerShell so the Scheduled Task can be updated.

### `py scripts/doctor.py --repair-gateway` still fails (RPC / WebSocket 1006)

**Cause:** OpenClaw’s gateway can exit its RPC/WebSocket plane while HTTP is still inconsistent. A frequent upstream correlate is **model pricing bootstrap** hitting the network and **timing out**, after which `openclaw gateway call health` may report **WebSocket 1006** (abnormal closure).

**What AKOS does:** `akos.runtime.recover_gateway_service()` waits briefly after `gateway start` (cold-start window), polls longer than before, and on failure builds **operator hints** from `openclaw gateway status` (including the **File log(s):** path), the last **RPC health** capture, and **keyword-filtered** lines from the tail of that log (no full log dump).

**Fix / verification path:**
1. Run `openclaw gateway status` and open the log path it prints.
2. If you see pricing/bootstrap **TimeoutError**, treat it as an **upstream network / OpenClaw** issue: ensure HTTPS egress from the machine, retry on a stable network, and check the OpenClaw version’s docs or issue tracker for disabling or caching model pricing if your environment is offline or filtered.
3. Re-run `py scripts/doctor.py --repair-gateway` after the gateway process stays up without new ERROR lines on startup.

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

Set these environment variables (already configured in `dev-local.env`) for optimal local performance:

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

The `dev-local` environment profile is pre-configured to use `deepseek-r1:14b` as primary with `qwen3:8b` as fallback. Bootstrap and `switch-model.py dev-local` now align on that same medium-tier default.

### RunPod vLLM Best Practices

The `gpu-runpod.json` profile includes production-grade vLLM settings. Key recommendations:

- **Tool calling**: Set `ENABLE_AUTO_TOOL_CHOICE=true` and `TOOL_CALL_PARSER=deepseek_v3` for structured tool output (without this, tool calls return as raw text).
- **Prefix caching**: `ENABLE_PREFIX_CACHING=true` avoids recomputing the 3-10K SOUL.md system prompt tokens on every request.
- **RunPod worker compatibility**: For `runpod/worker-v1-vllm:*`, use `KV_CACHE_DTYPE=auto` and `VLLM_ATTENTION_BACKEND=TRITON_ATTN` to avoid FlashInfer JIT startup failures on workers without `nvcc`.
- **AWQ dtype**: `QUANTIZATION=awq` should pair with `DTYPE=float16` for stable startup.
- **GPU selection**: `AMPERE_80` (A100-80GB) and `ADA_80_PRO` are recommended for 70B distilled models.
- **Concurrency**: `MAX_NUM_SEQS=64` (down from default 256) trades batch throughput for lower tail latency in agent workloads.

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

**Common causes:**

1. Workers are still warming up (first model load can take several minutes).
2. Worker image starts with FP8/FlashInfer settings that require CUDA toolkit binaries (`nvcc`) not present in the container.
3. AWQ model selected with non-float16 dtype.

**Fix / verification path:**

1. Verify health:
```bash
curl http://127.0.0.1:8420/runpod/health
```
2. If workers stay `throttled` or repeatedly exit, set these envs in `gpu-runpod.json`:
   - `DTYPE=float16` (for AWQ)
   - `KV_CACHE_DTYPE=auto`
   - `VLLM_ATTENTION_BACKEND=TRITON_ATTN`
3. Recreate the endpoint so workers pick up the patched template/env.
4. Re-run an inference smoke request and confirm `/runpod/health` shows `ready > 0`, `throttled = 0`, and `jobs.completed` increasing.

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
3. If checks fail, run the AKOS repair path:
   - `py scripts/doctor.py --repair-gateway`
4. Then validate again:
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

**Cause:** The live `openclaw.json` references `${OLLAMA_GPU_URL}`, `${VLLM_RUNPOD_URL}`, `${VLLM_SHADOW_URL}`, `${OPENAI_API_KEY}`, or `${ANTHROPIC_API_KEY}` via env-var substitution, but no `.env` file exists at `~/.openclaw/.env` to supply them. Bootstrap now auto-seeds this file with deterministic placeholder values on first run.

**Fix:**
1. Re-run bootstrap: `py scripts/bootstrap.py --skip-ollama`
2. Or manually run: `py scripts/switch-model.py dev-local`
3. Then repair/start the gateway: `py scripts/doctor.py --repair-gateway`

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
                               [--environment ENV] [--json-log]
```

Tails the gateway log, pushes traces to Langfuse, mirrors Madeira answer-quality telemetry locally, evaluates SOC alerts, and monitors RunPod health.

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

### GET /agents/{id}/policy

Returns the effective capability policy for the given agent role from `config/agent-capabilities.json`.

### GET /agents/{id}/capability-drift

Returns the live drift issues relevant to a single agent by filtering the same repo-vs-runtime checks used by `py scripts/check-drift.py`. This is the fastest API surface for spotting tool-profile mismatch, tool-block drift, or inventory drift for one role.

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
- **Per-agent tool profiles** enforced at gateway level — Madeira uses `minimal` with curated `alsoAllow` for `read`, memory lookups, HLK/finance tools, **read-only** `browser_snapshot` / `browser_screenshot`, and `deny: ["write", "edit", "apply_patch", "exec"]` (no coarse `browser` token); Orchestrator and Architect use `minimal` with curated `alsoAllow`; Executor and Verifier use `coding`, and both expose `browser` explicitly for UI validation flows (Verifier still denies `write`, `edit`, `apply_patch`)
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
- Audit via `GET /agents/{id}/policy` and `GET /agents/{id}/capability-drift` (live drift data, not placeholder output)

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

## 24. HLK Operator Model

This section explains how to operate the Holistika Knowledge Vault through MADEIRA and the AKOS platform.

### 24.1 Three Layers You Should Understand

| Layer | What it is | Lifetime | Where it lives |
|:------|:-----------|:---------|:---------------|
| **Session** | A single conversation or workflow run | Temporary -- ends when the chat closes or the agent resets | Agent memory, chat history |
| **Workspace** | An agent's operating folder with identity, memory, and rules | Persists across sessions but is agent-scoped | `~/.openclaw/workspace-{agent}/` |
| **Vault** | The canonical business knowledge system | Permanent -- versioned in git, synced to Drive | `docs/references/hlk/` |

**Initiative 14 (internal GTM / marketing ops):** Planning and SOPs live under [`docs/wip/planning/14-holistika-internal-gtm-mops/`](wip/planning/14-holistika-internal-gtm-mops/master-roadmap.md); `process_list.csv` rows originally `holistika_gtm_dtp_*` were renamed to `holistika_reach_dtp_*` per `D-IH-72-Z` Round 7 GTM-to-Reach migration (I72 P1; SOPs migrated to `Marketing/Reach/canonicals/`).

**Initiative 72 (Marketing Area Governance + RevOps activation):** Planning under [`docs/wip/planning/72-marketing-area-governance-and-persona-registry-expansion/`](wip/planning/72-marketing-area-governance-and-persona-registry-expansion/master-roadmap.md). P4 extended `process_list.csv` with 7 new value-mapping columns (`m3_sub_area`, `engagement_template_id`, `persona_id`, `cadence_type`, `min_rev_value_eur`, `par_rev_value_eur`, `max_rev_value_eur`) per `D-IH-72-AF` + `D-IH-72-AG`; sparse population intent (existing 1144+ rows backwards-compatible with NULL cells; new RevOps-authored rows populate axis cells). RevOps Manager + RevOps Analyst + 4 expansion roles + CRO added to `baseline_organisation.csv` per `D-IH-72-AC` + `D-IH-72-AD` (status=`gated_operator` until I71 P5 Pack A4 ships activation gate; expansion roles status=`gated_ahead_of_growth_stage`; CRO status=`gated_ahead_of_executive_activation`).

**Engagement folder doctrine (P13):** Every Think Big engagement folder (outbound under `Clients/`, inbound under `Advisers/`) conforms to the canonical shape locked in [`WORKSPACE_BLUEPRINT_HOLISTIKA.md`](references/hlk/v3.0/Admin/O5-1/Operations/PMO/WORKSPACE_BLUEPRINT_HOLISTIKA.md). The blueprint encodes the engagement-types matrix, per-root folder shape, file-tracking policy (branded PDFs tracked; markdown sidecars ignored), and the role-owner-canonical vs `compliance/`-tightened-mirror contract.

**Initiative 84 (Substrate Doctrine and Commercial Readiness):** Planning under [`docs/wip/planning/84-substrate-doctrine-and-commercial-readiness/`](wip/planning/84-substrate-doctrine-and-commercial-readiness/master-roadmap.md). P3 minted the **substrate doctrine canonical chain**: [`SUBSTRATE_REGISTRY.csv`](references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/SUBSTRATE_REGISTRY.csv) (18-column dimensional canonical per `D-IH-84-F`; 18 rows seeded covering 8 framework substrates + 7 agent-SDK substrates + 3 architectural-posture substrates) + [`SUBSTRATE_LANDSCAPE_DOCTRINE.md`](references/hlk/v3.0/Research/Methodology/canonicals/SUBSTRATE_LANDSCAPE_DOCTRINE.md) (Research-area canonical at status:review per `D-IH-84-G`). Pydantic SSOT [`akos/hlk_substrate_registry_csv.py`](../akos/hlk_substrate_registry_csv.py); validator [`scripts/validate_substrate_registry.py`](../scripts/validate_substrate_registry.py) (wired into `validate_hlk.py` umbrella); Supabase mirror DDL at [`supabase/migrations/20260517000000_i84_substrate_registry_mirror.sql`](../supabase/migrations/20260517000000_i84_substrate_registry_mirror.sql) (operator-apply via `supabase db push` per `akos-holistika-operations.mdc` §"Operator SQL gate" Step 4); sync via `py scripts/sync_compliance_mirrors_from_csv.py --substrate-registry-only`. Pairs with the Tech-Lab-side [`AGENTIC_FRAMEWORK_LANDSCAPE.md`](references/hlk/v3.0/Admin/O5-1/Envoy%20Tech%20Lab/canonicals/AGENTIC_FRAMEWORK_LANDSCAPE.md) as the meta-discipline that audits which substrates earn canonical status. P4 batched ratification (D-IH-84-B AKOS substrate baseline / D-IH-84-C AIC framing F1-F5 / D-IH-84-D MADEIRA productization shape / D-IH-84-E KiRBe framework narrowing) is operator-gated and consumes this registry as evidence input.

**Render-ownership declaration discipline (I71 P5 Pack A4):** Every customer-facing rendered deliverable in an engagement folder (`02-customer-pack/deck.*.md`, `proposal.*.md`, `tarification.*.md`, `gantt.*.md`, `dossier.*.md`, engagement `README*.md` counterparty briefs, `01-operator-pack/objections*.md`, `02-customer-pack/press*.md`, `02-customer-pack/advisor-email*.md`) should declare a `role_owner:` (or `owner:`) field in its YAML frontmatter that matches the canonical assignment per [`WORKSPACE_BLUEPRINT_HOLISTIKA.md §16`](references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/WORKSPACE_BLUEPRINT_HOLISTIKA.md). The canonical 9-row mapping: **deck** → Copywriter, **proposal** → PMO, **tarification** → PMO, **gantt** → UX Designer, **dossier** → PMO, **counterparty_brief** → Copywriter, **objections** → Account Manager, **press** → Storytelling Manager, **advisor_email** → PMO. Missing `role_owner:` surfaces as `info` advisory; mismatched value surfaces as `warning` advisory. Default posture is advisory (`AKOS_RENDER_OWNERSHIP_STRICT=0` default; never blocks CI); operators can promote individual deliverable_kinds to `error` severity via [`canonicals/_validators/render-ownership-pack.yml`](references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/_validators/render-ownership-pack.yml) per-rule override, or globally via `AKOS_RENDER_OWNERSHIP_STRICT=1` env in CI. Run the validator manually: `py scripts/validate_render_ownership.py` (defaults to scanning both Think Big roots). When canonical assignments differ for an engagement-specific reason, add a `render_ownership_rules:` override entry in `render-ownership-pack.yml` with the engagement-specific `expected_role_owner`. The validator also surfaces `info` transition-trigger advisories when ≥ 3 active engagements ship PMO-owned deliverables (PMO → RevOps activation signal per WORKSPACE §16.3 + I72 P4 RevOps activation gate).

**Operating rule:** Session state is disposable. Workspace state helps agents remember context. The vault is the source of truth. Never rely on session memory for business facts -- always ground answers in the vault.

### 24.1.1 Operator-facing UAT dossier (Initiative 48)

Use **`py scripts/render_uat_dossier.py`** for a single timestamped pack under `artifacts/uat-dossier/uat-dossier-<UTC>/`: `dossier.md`, optional `dossier.pdf` / `dossier.html`, and `manifest.json`. Default **`--mode snapshot`** reads existing artifacts only (fast). **`--mode live`** re-runs the orchestrated validators and eval CLI surface (~minutes). **`--mode tier-b`** is env-gated (`AKOS_DOSSIER_TIER_B=1`) and cost-capped via `MAX_DOSSIER_USD`. Trend sparklines (Section 11) append to `artifacts/uat-dossier/index.json` locally and optionally mirror to `compliance.dossier_run` when Supabase service-role env vars are set.

When `--format html` (or `--format all`) is passed, a second standalone HTML file `dossier-console.html` is emitted alongside `dossier.html`. The **Operator Console** is a visual companion — same brand SSOT, no JS / no CDN — with nine panels: cover + system-status pills, trend small-multiples, persona × difficulty heatmap (`PERSONA_SCENARIO_REGISTRY.csv`), diversified scenario sample cards (prompt / expected / forbidden / topic chips), decisions taken across the last three initiatives, skill registry visual, recent dossier runs timeline, and one cassette transcript per skill (`tests/evals/cassettes/<skill_id>/*.jsonl`). Open it in any browser; it answers *what was asked, what the system did, what was decided*.

### 24.2 How You Use MADEIRA Day-to-Day

MADEIRA is your single entrypoint for HLK operations. You talk to MADEIRA. MADEIRA queries the vault.

**Common tasks and what to say:**

| Task | What to ask MADEIRA | Tool MADEIRA uses |
|:-----|:--------------------|:------------------|
| Find a role | "Who is the Data Architect?" | `hlk_role` |
| Check reporting chain | "Who does DevOPS report to?" | `hlk_role_chain` |
| List an area | "Show me all Research roles" | `hlk_area` |
| Find a process | "What is hol_resea_dtp_142?" | `hlk_process` |
| Explore a project | "What workstreams are under KiRBe Platform?" | `hlk_process_tree` |
| See all projects | "List all 11 top-level projects" | `hlk_projects` |
| Find gaps | "What baselines need remediation?" | `hlk_gaps` |
| Search anything | "Find everything related to HUMINT" | `hlk_search` |

### 24.2.1 Three-light verdict and cadence (Initiative 49)

Releases use a **three-light** model (all green = ship). Operator cadence and thresholds are written in the hardened MADEIRA plan **Part H** ([`MADEIRA_HARDENING_CONSOLIDATED_PLAN.md`](../wip/planning/02-hlk-on-akos-madeira/MADEIRA_HARDENING_CONSOLIDATED_PLAN.md) — section "Verdict and cadence"). Day-to-day commands stay in §24.1.1 (`py scripts/render_uat_dossier.py`; optional `--filter madeira` once enabled) and `docs/guides/madeira_operator_quickstart.md` when that guide lands.

### 24.3 Adding Knowledge to the Vault

1. **Identify the owner** -- look up the role in `baseline_organisation.csv` that should own this knowledge.
2. **Navigate to the folder** -- go to `docs/references/hlk/v3.0/Admin/O5-1/{area}/{role}/`.
3. **Write markdown** -- create the document following the SOP-META envelope if it is a formal procedure.
4. **Register the process** -- if this is a new process, add a row to `process_list.csv` with the correct `item_parent_1`, `role_owner`, and `item_granularity`.
5. **Commit** -- git tracks the change. Drive syncs the folder.

### 24.3.1 Governed KM (Topic–Fact–Source and Output 1)

For **visuals and other knowledge artifacts** that must stay traceable across Obsidian, Drive, and git, follow the Topic–Fact–Source contract in `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/HLK_KM_TOPIC_FACT_SOURCE.md`:

- **Output 1 (images / Excalidraw exports):** keep binaries under `docs/references/hlk/v3.0/_assets/<topic_id>/` with a `*.manifest.md` sidecar and a short companion `.md` stub for search.
- **Tags:** use only the controlled vocabulary and prefixes defined in that contract.
- **External backlogs (e.g. Trello):** use the PMO registry `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/RESEARCH_BACKLOG_TRELLO_REGISTRY.md` as the canonical **index**; Trello remains non-authoritative. Board exports for id reconciliation live under `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/imports/` (see `imports/README.md`).
- **WIP syntheses** tied to registry rows: `docs/wip/intelligence/<topic_id>/research-synthesis-*.md` (interpretation layer until promoted; legacy `hlk-km/` archived at `docs/wip/_archived/hlk-km-pre-2026-05-12/` per D-IH-86-FJ).
- **Validation:** after editing manifests under `v3.0/_assets/`, run `py scripts/validate_hlk_km_manifests.py`.
- **UAT:** `docs/uat/hlk_admin_smoke.md` Scenario 8 (KM manifests + registry + imports).

See also `docs/references/hlk/v3.0/index.md` (Knowledge management section), `docs/wip/README.md` (wip layout), and `docs/wip/planning/03-hlk-km-knowledge-base/master-roadmap.md` for initiative traceability.

### 24.3.2 Promotion Ladder For Founder-Governance Work

Not every business artifact should jump straight into `process_list.csv`.

Use this order:

| Layer | What belongs there | Where it lives |
|:------|:-------------------|:---------------|
| Working synthesis | Redacted interpretation, validation, source comparison | `docs/wip/` (see `docs/wip/README.md`; Research Tier-1 under `docs/wip/intelligence/<topic_id>/`) |
| Case docs | Current founder/entity decisions, evidence packs, rationale notes | `docs/references/hlk/v3.0/` |
| SOPs | Repeatable procedures with stable inputs/outputs | `docs/references/hlk/v3.0/` |
| Registry rows | Runtime-discoverable projects, workstreams, processes, tasks | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/process_list.csv` |
| Org changes | Role ownership changes only | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/baseline_organisation.csv` |

**Current founder-governance bundle examples:**

- Legal: `Founder Entity Formation Readiness`, `Trademark and Naming Governance`
- Finance: `Founder-to-Company Funding Path`
- Compliance: `ENISA Readiness and Evidence Pack`
- Case layer: entity-formation memo, capitalization note, ENISA evidence pack, trademark scope note, Research-vs-Tech-Lab rationale

**Scaling rule:** If the same founder-governance activity repeats, promote the stable part upward into SOP + registry layers. If it stays case-specific, keep it in role-owned case docs rather than bloating the registry.

### 24.3.3 Trello-derived GTM registry (cluster layer)

Large PMO/Trello promotions into `process_list.csv` use an intermediate **cluster** `process` row (`item_id` prefix `gtm_cl_*`) between the English **workstream** and each leaf task so both `item_parent_1` and `item_parent_2` resolve to real `item_name` values in the same CSV. After changing merge rules or path shapes, operators run `py scripts/refine_gtm_process_hierarchy.py --write` (see `docs/wip/planning/02-hlk-on-akos-madeira/reports/trello-list-to-workstream-matrix.md`, Pattern 2).

### 24.3.4 Program layer and parent identifiers

Some projects use an extra **program** **workstream** row (`item_id` prefix `hlk_prog_*`) between the **project** and several GTM-aligned workstreams to group radar/planning/sales vs engineering/UX (see Pattern 3 in the same matrix doc). **Repeatable “methods”** stay in SOPs, `instructions`, and vault markdown—there is no separate `method` granularity in `process_list.csv`.

The CSV may also include **`item_parent_1_id`** and **`item_parent_2_id`**: when present, they must match the `item_id` of the row whose `item_name` equals `item_parent_1` / `item_parent_2`. After tooling backfills these columns, **new and edited rows must keep parent names and parent IDs in sync**; run `py scripts/validate_hlk.py` before merge. API consumers may use `GET /hlk/processes/id/{item_id}/tree` for stable parent-child navigation by id.

**Column contract for external tools:** The authoritative column order and headers are defined as **`PROCESS_LIST_FIELDNAMES`** in `akos/hlk_process_csv.py` (currently 21 columns, including the two parent-id fields). Importers that assume a fixed legacy width should read the header row or import that constant from the repo instead of hard-coding 19 columns.

**Forks and older branches:** If your checkout predates the parent-id columns, **merge current `main` before editing** `process_list.csv`, then run **`py scripts/check_process_list_header.py`** so the header matches `PROCESS_LIST_FIELDNAMES`. Scripts that still embed a 19-column `FIELDNAMES` list will mis-align or drop columns when writing.

**Full maintenance SOP:** `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/SOP-PMO_PROCESS_LIST_CSV_MAINTENANCE_001.md` (column contract, duplicate-name workflow with `--suggest`, merge hazards, tooling table).

### 24.3.5 GitHub repositories (Envoy Tech Lab hub)

Holistika tracks **many GitHub repositories** (platform, internal tools, client-delivery). Authority split:

| Layer | Canonical in vault | SSOT for code |
|:------|:-------------------|:--------------|
| **Which repos exist, class, owner role, topic links** | `docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/REPOSITORIES_REGISTRY.md` | GitHub remote |
| **Optional API metadata** (`api_spec_pointer`, `api_topic_id` on registry rows) | Same registry table | OpenAPI/AsyncAPI **files** live in the repo (path pointed to) |
| **CTO-chain component/service inventory** (per-component `api_exposure`, owners, runbooks; join on `repo_slug`) | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/techops/COMPONENT_SERVICE_MATRIX.csv` | Relocated 2026-05-22 per **D-IH-81-G-T5** (I81 P2 T5) |
| **Policy** (pointer-first, submodule criteria) | `docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/README.md` | — |
| **Non-repo client/program files** (SOWs, commercials, decks) | `docs/references/hlk/v3.0/Think Big/` (see `Think Big/README.md`) | — |

**API lifecycle:** `docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/SOP-HLK_API_LIFECYCLE_MANAGEMENT_001.md`. **Matrix maintenance (CTO chain):** `SOP-HLK_COMPONENT_SERVICE_MATRIX_MAINTENANCE_001.md` in the same folder.

Cross-engagement topic index (pilot): `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/TOPIC_PMO_CLIENT_DELIVERY_HUB.md` (includes the **PMO project portfolio SSOT** table and GOI/POI-style stakeholder index). Full placement rules: `docs/references/hlk/v3.0/index.md` (Entity placement). Precedence: `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md` (GitHub repositories vs vault authority).

### 24.4 Maintaining Baselines

The canonical baselines live in `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/`:

| File | What to edit | When |
|:-----|:-------------|:-----|
| `baseline_organisation.csv` | Roles, hierarchy, access levels, descriptions | New role, role change, access review |
| `process_list.csv` | Processes, projects, workstreams, tasks | New process, hierarchy change, ownership change; follow **SOP-PMO_PROCESS_LIST_CSV_MAINTENANCE_001** (`docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/SOP-PMO_PROCESS_LIST_CSV_MAINTENANCE_001.md`) |
| `techops/COMPONENT_SERVICE_MATRIX.csv` | Components, services, integrations (CTO SSOT). Relocated 2026-05-22 per **D-IH-81-G-T5**. | New system, ownership or API exposure change; follow **SOP-HLK_COMPONENT_SERVICE_MATRIX_MAINTENANCE_001** (`docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/SOP-HLK_COMPONENT_SERVICE_MATRIX_MAINTENANCE_001.md`); validate via `py scripts/validate_hlk.py` |
| `finops/FINOPS_COUNTERPARTY_REGISTER.csv` (moved to `finops/` 2026-05-23 per I81 P2 T1 / D-IH-81-Q under D-IH-81-G umbrella) | Counterparty metadata only—vendors, customers, partners (no amounts; Business Controller / CFO chain) | New counterparty, classification, or renewal review; follow **SOP-HLK_FINOPS_COUNTERPARTY_REGISTER_MAINTENANCE_001** (`docs/references/hlk/v3.0/Admin/O5-1/Finance/Business Controller/SOP-HLK_FINOPS_COUNTERPARTY_REGISTER_MAINTENANCE_001.md`); Supabase mirror **`compliance.finops_counterparty_register_mirror`** (mirror table name unchanged) via `sync_compliance_mirrors_from_csv.py --finops-counterparty-register-only` or **`py scripts/verify.py compliance_mirror_emit`** after DDL |
| `Learning/canonicals/dimensions/LEARNING_OPS_BACKLOG.csv` | Apprentice / cohort onboarding backlog (`engagement_model_id` FK to `eng_model_*`, `methodology_version_at_onboarding`) — **Learning Curator** chain | New apprentice binds to [`HOLISTIK_RESEARCHER_ONBOARDING_CURRICULUM.md`](references/hlk/v3.0/Admin/O5-1/People/Learning/canonicals/curriculum/HOLISTIK_RESEARCHER_ONBOARDING_CURRICULUM.md); follow [`LEARNING_CHARTER.md`](references/hlk/v3.0/Admin/O5-1/People/Learning/canonicals/LEARNING_CHARTER.md); operator checklist runbook `scripts/peopl_engagement_apprentice_curriculum_assign.py` |
| `GOI_POI_REGISTER.csv` | Groups of Interest / Persons of Interest dimension (organisations + persons referenced by canonical text via ref_id; private parties obfuscated, public entities un-redacted) — **Compliance** chain | New stakeholder, sensitivity change, or program reuse; follow **SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001** (`docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md`); Supabase mirror **`compliance.goipoi_register_mirror`** via `sync_compliance_mirrors_from_csv.py --goipoi-register-only` or **`py scripts/verify.py compliance_mirror_emit`** after DDL (Initiative 21) |
| `ADVISER_ENGAGEMENT_DISCIPLINES.csv` | External Adviser Engagement (ADVOPS) plane disciplines lookup — Legal / Fiscal / IP / Banking / Certification / Notary — **PMO** chain | New discipline; follow **SOP-EXTERNAL_ADVISER_ENGAGEMENT_001** (`docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md`); mirror **`compliance.adviser_engagement_disciplines_mirror`** via `--adviser-disciplines-only` or **`py scripts/verify.py compliance_mirror_emit`** (Initiative 21) |
| `ADVISER_OPEN_QUESTIONS.csv` | Adviser-facing questions and actions across all disciplines and programs (replaces `FOUNDER_OPEN_QUESTIONS_EXTERNAL_COUNSEL.md` as SSOT — vault MD becomes a derived per-discipline view) — **PMO/Legal** | New / answered / escalated question; mirror **`compliance.adviser_open_questions_mirror`** via `--adviser-questions-only` or **`py scripts/verify.py compliance_mirror_emit`** (Initiative 21) |
| `advops/FILED_INSTRUMENTS.csv` | Filed legal/fiscal/IP/banking/certification/notary instruments across draft/signed/filed/superseded statuses (replaces `FOUNDER_FILED_INSTRUMENT_REGISTER.md` as SSOT — vault MD becomes a derived per-discipline view) — **Legal** chain. Relocated + renamed at I81 P2 T3 (D-IH-81-S, 2026-05-23) from `canonicals/FOUNDER_FILED_INSTRUMENTS.csv`; legacy path supported via deprecation alias for one cycle. | New filing or status change; mirror **`compliance.filed_instruments_mirror`** (renamed from `founder_filed_instruments_mirror`) via `--founder-filed-instruments-only` (CLI flag name retained for one cycle) or **`py scripts/verify.py compliance_mirror_emit`** (Initiative 21) |
| `access_levels.md` | Access level definitions | Policy change (rare) |
| `confidence_levels.md` | Confidence level definitions | Policy change (rare) |
| `source_taxonomy.md` | Source categories and credibility levels | New source type (rare) |
| `PRECEDENCE.md` | What is canonical vs mirrored | Governance change |
| `CANONICAL_REGISTRY.csv` | Machine-readable index of vault canonicals (pairs with PRECEDENCE narrative) | New canonical mint / area backfill |
| HCAM articulation (`ENTITY_CATALOG.csv`, `CANONICAL_RELATIONSHIP_REGISTRY.csv`, `CANONICAL_ARTICULATION_MODEL.md`) | Enterprise ontology — **T1 git + T3 Neo4j graph projection**; no Supabase compliance mirror unless separately ratified (D-IH-95-B) | Entity/triple changes; `py scripts/validate_canonical_articulation.py` |
| `HLK_KM_TOPIC_FACT_SOURCE.md` | Topic / Fact / Source, Output 1 manifests, Obsidian tags | KM contract or manifest rules change |

**After editing baselines:** Restart the AKOS API (`py scripts/serve-api.py`) to reload the HLK registry from the updated CSVs.

Current canonical examples include founder-governance processes under Legal, Finance, and Compliance such as `Founder Entity Formation Readiness`, `Trademark and Naming Governance`, `Founder-to-Company Funding Path`, and `ENISA Readiness and Evidence Pack`.

### 24.5 Vault Structure Reference

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
    Envoy Tech Lab/               Repositories/ (GitHub index), KiRBe, MADEIRA, Showcases
    Think Big/                    README, Projects, Clients (non-repo artifacts)
  Research & Logic/               v2.7 historical reference (read-only)
```

### 24.6 Quick Reference Card

| Question | Answer |
|:---------|:-------|
| Where do I edit? | `docs/references/hlk/v3.0/` for documents, `compliance/` for baselines |
| Where do old docs live? | `Research & Logic/` (v2.7, read-only) |
| How does MADEIRA find things? | Via HLK runtime tools backed by `HlkRegistry` and the `akos-runtime-tools` bridge |
| What happens if I edit both vault and DB? | Vault wins. See `PRECEDENCE.md` for conflict resolution. |
| How do I restart after baseline edits? | `py scripts/serve-api.py --port 8420` |
| How do I check integrity? | `py scripts/test.py hlk` or use `/hlk/gaps` endpoint |
| How do I validate KM visual manifests? | `py scripts/validate_hlk_km_manifests.py` |
| Where are Holistika GitHub repos indexed? | `docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/REPOSITORIES_REGISTRY.md` |
| How do I export an adviser handoff bundle? | `py scripts/export_adviser_handoff.py --discipline {legal,fiscal,ip,banking,certification,notary,all} --format md --out artifacts/exports/handoff-<YYYY-MM-DD>.md` (Initiative 21 / P7) |
| How do I export the same bundle as PDF? | `py scripts/export_adviser_handoff.py --discipline all --format pdf --out artifacts/exports/handoff-<YYYY-MM-DD>.pdf` after `py -m pip install --only-binary=:all: -r requirements-export.txt` (Initiative 22 / P6; renderer chain WeasyPrint → fpdf2 → pandoc) |
| How do I smoke-test the adviser export (MD)? | `py scripts/verify.py export_adviser_handoff_smoke` |
| How do I smoke-test the adviser export (PDF)? | `py scripts/verify.py export_adviser_handoff_pdf_smoke` (SKIPs gracefully when no PDF renderer is installed) |
| Where do new program-scoped vault docs go? | Under the role folder's `programs/<program_id>/` subfolder (Initiative 22 P3) — e.g. `docs/references/hlk/v3.0/Admin/O5-1/People/Legal/programs/PRJ-HOL-FOUNDING-2026/` |
| Where do new KM Output-1 visuals go? | Under `_assets/<plane>/<program_id>/<topic_id>/` (Initiative 22 P2) — see `docs/references/hlk/v3.0/_assets/README.md` |
| How do I render a KM Mermaid diagram? | `py scripts/render_km_diagrams.py <path>.mmd --update-manifest` (Initiative 22 P5; uses `mmdc` if installed, else mermaid.ink HTTP fallback) |
| Where is the program registry? | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/PROGRAM_REGISTRY.csv` (Initiative 23 P1; 12 programs with unique 3-letter `program_code`s; canonical `program_id` is PRJ-HOL-style per D-IH-8). |
| Where is the cross-program glossary? | [`docs/reference/glossary-cross-program.md`](reference/glossary-cross-program.md) (Initiative 23 P5; program codes, discipline codes, sensitivity bands, sharing labels, GOI/POI class taxonomy, status enums, voice registers). |
| How do I check for compliance mirror drift? | `py scripts/probe_compliance_mirror_drift.py --emit-sql` (prints SELECT for `user-supabase` MCP `execute_sql`), paste JSON to `artifacts/probes/mirror-drift-<YYYYMMDD>.json`, then `py scripts/probe_compliance_mirror_drift.py --verify` (or profile `compliance_mirror_drift_probe`). SKIPs gracefully when no fresh artifact exists (Initiative 23 P4). |
| How do I onboard a new program? | (1) Add a row to `PROGRAM_REGISTRY.csv` with unique `program_code`. (2) Create `_assets/<plane>/<program_id>/<topic_id>/` for the first topic. (3) Add `programs/<program_id>/README.md` under each role-folder root that has program-specific casework (evidence-based — only roots with supporting `process_list.csv` rows). (4) Run `validate_hlk.py` (covers PROGRAM_REGISTRY + cross-asset consistency). See [Initiative 23 PRJ-HOL-KIR-2026 onboarding](wip/planning/23-hlk-program-registry-and-program-2/reports/uat-i23-program-registry-20260429.md) as a worked example. |

### 24.7 External Adviser Engagement (ADVOPS) plane

The **External Adviser Engagement** plane (ADVOPS) sits parallel to MKTOPS / FINOPS / OPS / TECHOPS and governs how Holistika engages **all** external advisers (Legal, Fiscal, IP, Banking, Certification, Notary) for any program. Initiative 21 promoted four ad-hoc artifacts to canonical CSVs and added a deterministic GOI/POI obfuscation dimension:

- Plane SOP — `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md`
- Router — `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/EXTERNAL_ADVISER_ROUTER.md`
- Cursor rule — `.cursor/rules/akos-adviser-engagement.mdc`
- KM Topic — `docs/references/hlk/v3.0/_assets/advops/2026-holistika-incorporation/adviser_handoff/topic_external_adviser_handoff.manifest.md`
- Initiative folder — `docs/wip/planning/21-hlk-adviser-engagement-and-goipoi/`

**Day-to-day operator commands:**

```pwsh
py scripts/validate_hlk.py
py scripts/verify.py compliance_mirror_emit
# After review: apply mirror DML to linked Supabase (see docs/guides/holistika-mirror-dml-apply.md)
# pwsh -File scripts/apply_mirror_batches.ps1 -BatchDir artifacts/sql/mirror-batches/<date>
py scripts/verify.py export_adviser_handoff_smoke
py scripts/export_adviser_handoff.py --discipline legal --format md --out artifacts/exports/legal-handoff-2026-04.md
```

**Privacy posture (D-CH-2)**: Canonical text uses GOI/POI ref_ids only; raw names of private parties live off-repo. Public authorities (AEAT, ENISA, OEPM, mercantile registries) may be named directly. See `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/SOP-HLK_TRANSCRIPT_REDACTION_001.md` and `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md`.

### 24.7.1 FINOPS writer substrate (I81 P2 Bundle B-2; 2026-05-24)

Bundle B-2 stands up Holistika's first prod-ready FINOPS event pipeline. From Stripe webhook → counterparty resolution → FX snapshot → `finops.registered_fact` write, with full DLQ + observability. Architecture R1..R5 ratified 2026-05-23; D-IH-81-V / W / X closed end-to-end 2026-05-24.

**What it does (plain language).** Every Stripe payment event (charge succeeded, subscription created/updated/cancelled, etc.) arrives at the webhook handler. The handler returns 200 to Stripe in < 5 seconds (so Stripe never retries), then enqueues the event on a Postgres-native queue (`pgmq.finops_writer_queue`). A cron-triggered worker drains the queue every minute, resolves the counterparty per the engagement model's strategy, snapshots the ECB FX rate, and writes a governed fact row. Failures route to a DLQ; depth > 10 emits a `dlq_threshold_exceeded` OPS row that surfaces in HLK-ERP.

**5-component stack:**

| Component | Surface | Role |
|:---|:---|:---|
| Stripe webhook handler v6 | [`supabase/functions/stripe-webhook-handler/index.ts`](../supabase/functions/stripe-webhook-handler/index.ts) | Dispatch-pattern entry; signature-verifies + dispatches to `finops_dispatch.ts` (new) or `kirbe_holistika_dispatch.ts` (pre-B-2b verbatim) |
| FINOPS dispatch | [`supabase/functions/stripe-webhook-handler/dispatch/finops_dispatch.ts`](../supabase/functions/stripe-webhook-handler/dispatch/finops_dispatch.ts) | Logs raw event to `holistika_ops.stripe_events` + enqueues to `pgmq.finops_writer_queue` |
| FX cache | Edge Function [`fx-rate-cache-refresh`](../supabase/functions/fx-rate-cache-refresh/index.ts) + cron `30 15 * * *` | Daily ECB rate refresh (USD/EUR + GBP/EUR + CHF/EUR + EUR/EUR identity); persists to `holistika_ops.fx_rate_cache` |
| Writer worker | Edge Function [`finops-writer-worker`](../supabase/functions/finops-writer-worker/index.ts) + cron `* * * * *` | Drains `pgmq.finops_writer_queue` (MAX_BATCH=25; VISIBILITY_TIMEOUT=90s); resolves counterparty + FX snapshot + writes `finops.registered_fact`; failures → DLQ after MAX_RETRIES=5 |
| DLQ drain runbook | [`scripts/finops_dlq_drain.py`](../scripts/finops_dlq_drain.py) | Operator drain tool when `dlq_threshold_exceeded` OPS row fires; `--self-test` validates Pydantic + RPC wiring |

**Engagement-model router (R1-a).** The 17-column `compliance.engagement_model_registry_mirror` carries `counterparty_resolution_strategy` (`NOT NULL` + `CHECK` enum) with 5 strategies: `stripe_customer_link_lookup` (default; consultancy customers + SaaS subscribers) / `metadata_engagement_id` (4 ad-hoc engagement classes) / `metadata_billing_plane` / `rpp_payout_attribution` / `manual_review` (3 unknown classes). Pydantic SSOT in [`akos/hlk_engagement_model_csv.py`](../akos/hlk_engagement_model_csv.py); TS resolver in [`supabase/functions/_shared/finops/counterparty_resolver.ts`](../supabase/functions/_shared/finops/counterparty_resolver.ts).

**Day-to-day operator commands:**

```pwsh
py scripts/validate_finops_ledger.py
py scripts/validate_finops_counterparty_register.py
py scripts/finops_dlq_drain.py --self-test
py scripts/stripe_audit_metadata.py --self-test
py -m pytest tests/test_validate_engagement_model_registry.py tests/test_validate_finops_ledger.py tests/test_hlk_fx_rate.py tests/test_finops_dlq_drain.py tests/test_resolve_counterparty_id.py
```

**Production deployment knobs:**

- **Exposed schemas (Supabase Dashboard → Project Settings → API → Exposed schemas):** `public, storage, graphql_public, realtime, supabase_functions, vault, kirbe, gemini_fastapi, compliance, ai_use_cases, stripe_gtm, stripe_public, compliance_001, holistika_ops, finops`. PostgREST gates Edge Function `.schema()` access; `holistika_ops` + `finops` must remain in this list or writer worker + FX refresh will 404 with a schema error.
- **Cron jobs (verify via `SELECT * FROM cron.job`):** `fx_rate_cache_refresh_daily` (`30 15 * * *`) + `finops_writer_worker_every_minute` (`* * * * *`) + `kirbe_monitoring_logs_retention` (`0 3 * * *`).
- **pgmq RPC wrappers (5 `SECURITY DEFINER` functions):** `pgmq_send_finops_writer` / `pgmq_read_finops_writer` / `pgmq_delete_finops_writer` / `pgmq_archive_finops_writer` / `pgmq_metrics_finops_writer` — anon + PUBLIC EXECUTE revoked; `service_role` only. See [`supabase/migrations/20260524130000_i81_p2_b2b_pgmq_rpc_wrappers_role_lockdown.sql`](../supabase/migrations/20260524130000_i81_p2_b2b_pgmq_rpc_wrappers_role_lockdown.sql).

**What's deferred (OPS rows):** Stripe live AT MCP audit (OPS-81-X; requires `mcp_auth user-stripe` reconnaissance against the live Stripe AT environment after operator authentication). Closure UAT at [`docs/wip/planning/81-vault-integrity-layout-milestones-retrofit/reports/i81/p2-bundle-b2-closure-uat-2026-05-24.md`](wip/planning/81-vault-integrity-layout-milestones-retrofit/reports/i81/p2-bundle-b2-closure-uat-2026-05-24.md) verdict: PASS-WITH-FOLLOWUP.

### 24.8 Initiative status taxonomy

Every initiative under `docs/wip/planning/` carries a `status:` field in its `master-roadmap.md` frontmatter. The status uses a **seven-value taxonomy** defined in [`akos/planning/status_taxonomy.py`](../akos/planning/status_taxonomy.py) (the `InitiativeStatus` enum). Each value maps to a distinct operator expectation and determines which companion frontmatter fields are required:

| Status | When to use | Required companion fields |
|:-------|:------------|:--------------------------|
| `closed` | Work is complete and accepted | `closed_at` (YYYY-MM-DD); typically `closure_decision_id` |
| `archived` | Superseded or abandoned; kept for reference | `archived_at` (YYYY-MM-DD), `superseded_by` |
| `active` | Currently under development | None required; `last_review` informs the freshness canary |
| `continuous` | Ongoing operational concern with no target end date | `continuous_rationale` |
| `program_line` | Recurring cadence-driven workstream | `cadence` (weekly \| monthly \| quarterly \| event_driven) |
| `gated_external` | Blocked on an external party | `gated_on` (free-form prose) |
| `gated_operator` | Blocked on an explicit operator action | `gated_on`, `operator_action` |

The `scripts/render_wip_dashboard.py` renderer splits `WIP_DASHBOARD.md` into sections per status. Initiatives marked `gated_operator` surface in [`docs/wip/planning/OPERATOR_INBOX.md`](wip/planning/OPERATOR_INBOX.md), which is the operator's primary triage view. Adding a new status value requires extending the `InitiativeStatus` enum and adding a corresponding dashboard section.

### 24.9 HLK initiative governance

Initiative 59 introduced **five new compliance dimensions** that bring planning-workspace state under the same governed HLK pattern as the existing vault CSVs. Each dimension follows the standard lifecycle: **canonical CSV → Pydantic schema → validator script → optional Supabase compliance mirror**.

| Dimension | CSV | Validator | Purpose |
|:----------|:----|:----------|:--------|
| `REPOSITORY_REGISTRY` | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/REPOSITORY_REGISTRY.csv` | `scripts/validate_hlk.py` | Holistika-tracked GitHub repositories |
| `INITIATIVE_REGISTRY` | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_REGISTRY.csv` | `scripts/validate_initiative_registry.py` | Governed initiative metadata (status, owners, FK to cycles/decisions) |
| `OPS_REGISTER` | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/OPS_REGISTER.csv` | `scripts/validate_hlk.py` | Operator actions and OPS-ticket audit trail |
| `CYCLE_REGISTER` | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/CYCLE_REGISTER.csv` | `scripts/validate_hlk.py` | Execution cycles with date ranges |
| `DECISION_REGISTER` | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv` | `scripts/validate_decision_register.py` | Queryable `D-IH-XX-Y` decision metadata |

The five dimensions form a **foreign-key web**: initiatives reference cycles and decisions; OPS actions reference initiatives; the decision register cross-links to initiative IDs. Validators enforce these FK constraints at commit time.

Two new SOPs govern the lifecycle: [`SOP-INITIATIVE_GOVERNANCE_001.md`](references/hlk/v3.0/Admin/O5-1/Operations/PMO/SOP-INITIATIVE_GOVERNANCE_001.md) (how to open, review, close, and archive initiatives) and [`SOP-INITIATIVE_PROCESS_HARMONISATION_001.md`](references/hlk/v3.0/Admin/O5-1/Operations/PMO/SOP-INITIATIVE_PROCESS_HARMONISATION_001.md) (forward-looking process-list minting from initiative patterns).

### 24.10 Decision audit trail

The **`DECISION_REGISTER.csv`** at `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv` is the queryable SSOT for all governed decisions. Each row carries a `D-IH-XX-Y` identifier (where `XX` is the initiative number and `Y` is a per-initiative sequence), the decision date, status, rationale summary, and FK links to the initiative and cycle that produced it.

Per-initiative `decision-log.md` files (e.g. `docs/wip/planning/59-hlk-governance-clean-slate/decision-log.md`) remain **canonical for prose** — they hold the full context, alternatives considered, and operator sign-off narrative. The CSV is the **governed metadata frame**: it enables programmatic queries, cross-initiative aggregation, and Supabase mirror projections without replacing the human-readable log. The validator `scripts/validate_decision_register.py` enforces schema, enum, and FK integrity at commit time.

### 24.11 Process harmonisation (forward-looking)

When recurring initiative patterns stabilise into repeatable operating procedures, they become candidates for **process-list minting** — the addition of new rows to the canonical `process_list.csv`. This lifecycle is governed by [`SOP-INITIATIVE_PROCESS_HARMONISATION_001.md`](references/hlk/v3.0/Admin/O5-1/Operations/PMO/SOP-INITIATIVE_PROCESS_HARMONISATION_001.md).

The first concrete candidate is **I60 — Process List Harmonisation**, tracked at [`docs/wip/planning/_candidates/i60-process-list-harmonisation.md`](wip/planning/_candidates/i60-process-list-harmonisation.md). It proposes minting `process_list.csv` rows for the initiative-governance and cycle-management patterns that I59 proved out.

Actual process-list minting is **operator-approval-gated** per `.cursor/rules/akos-governance-remediation.mdc`: new `process_list.csv` rows require explicit operator approval before committing, must pass `py scripts/validate_hlk.py`, and trigger a corresponding update to this user guide (§24.4) if role or process counts change. Baseline-organisation rows needed by new processes share the same approval gate.

### 24.12 Mission Control (hlk-erp external repo)

Initiative 62 (I62) introduces **Mission Control**, the operator surface that consumes AKOS canonical data through the existing `compliance.*` Supabase mirrors. It lives in the external repo [`hlk-erp`](https://github.com/FraysaXII/hlk-erp) and is governed from this repo via:

- The canonical [`SUBDOMAINS_REGISTRY.md`](references/hlk/v3.0/Envoy%20Tech%20Lab/Repositories/SUBDOMAINS_REGISTRY.md) — every Holistika subdomain (`erp.holistika.com`, `madeira.holistika.com`, `status.holistika.com`, plus reserved entries) is recorded here. Validation: `py scripts/validate_subdomains_registry.py` (also wired into `release-gate.py`).
- Three governed Supabase migrations (`supabase/migrations/20260506130*.sql`) creating the `holistika_ops` RBAC tables, the read-side `erp.*` projection views, and the `demo.*` showcase schema. Operator approval gate: [`docs/wip/planning/62-mission-control/reports/sql-proposal-mission-control-2026-05-06.md`](wip/planning/62-mission-control/reports/sql-proposal-mission-control-2026-05-06.md).
- The I62 master roadmap, decision log, asset classification, evidence matrix and Impeccable shape reports under [`docs/wip/planning/62-mission-control/`](wip/planning/62-mission-control/).

**Operator topology**:

| Surface       | URL                          | Auth  | Data mode | Notes |
|:--------------|:-----------------------------|:------|:----------|:------|
| Mission Control | `erp.holistika.com`        | Required (Supabase Auth, AKOS access_level 0–6) | live | Read-side only over `compliance.*` and `erp.*` |
| Showcase     | `madeira.holistika.com`      | Open  | demo      | Seeded fictional data, no service-role key |
| Status       | `status.holistika.com`       | Open  | live      | Aggregate health + last-sync, no row data |

**Day-to-day operator commands** (from the AKOS root):

```pwsh
py scripts/validate_subdomains_registry.py
py scripts/release-gate.py
```

When a new subdomain is needed, propose a row in the registry first, run the validator, then provision the Vercel custom domain — never the other way around.

### 24.13 Blessing a new external repo

The "bless" pattern lets you scaffold a new Holistika-tracked external repository (e.g. `kirbe`, future client-delivery repos) with the standard governance + CI/CD + observability artifacts in one command. AKOS stays SSOT; the consuming repo gets a deterministic, drift-detectable copy.

**Prerequisite**: register the repo in [`docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/REPOSITORY_REGISTRY.csv`](references/hlk/compliance/REPOSITORY_REGISTRY.csv) (slug, GitHub URL, class, primary_owner_role, lifecycle_status). For `class=reference` (e.g. `boilerplate`), the bless script light-touches per D-IH-32-N.

**One-time bless (operator-invoked)**:

```pwsh
py scripts/bless_external_repo.py --repo-slug <slug> --repo-path <abs-path> --dry-run
py scripts/bless_external_repo.py --repo-slug <slug> --repo-path <abs-path>
```

What gets written (stack-aware):

- `.cursor/rules/akos-mirror.mdc` (verbatim of the AKOS template) + `.akos-mirror.sha256` drift marker
- `EXTERNAL_REPO_CONTRACT.md` (rendered from the canonical template, slug-aware)
- `CONTRIBUTING.md` (root, rendered)
- `.github/PULL_REQUEST_TEMPLATE.md`
- `.gitattributes` (only when missing)
- CI/CD baseline: `.github/workflows/ci.yml`, `dependabot.yml`, `CODEOWNERS`, `docs/runbooks/branch-protection.md` (when templates exist)
- Issue templates and `LICENSE` (when templates exist)
- Opt-in via `--with`: `sentry`, `slack`, `postman`, `sbom`, `semgrep`, `codecov`, `supabase-lint`

**Idempotency**: subsequent runs SKIP files unchanged since last bless. Hand-edited files are refused unless `--force` is passed; the operator sees the diff before clobbering.

**Drift auto-PR (nightly)**: `--auto-pr` opens a PR via `gh` against the consuming repo when sha256 drift is detected, gracefully no-opping if `gh` is unavailable.

**Verification**:

```pwsh
py scripts/release-gate.py    # includes the external-repo contract check
py -m pytest tests/test_bless_external_repo.py -v
```

Cross-references: [`SOP-EXTERNAL_REPO_BLESSING_001.md`](references/hlk/v3.0/Admin/O5-1/Envoy%20Tech%20Lab/External%20Repos/SOP-EXTERNAL_REPO_BLESSING_001.md), [I63 charter](wip/planning/63-external-repo-governance-codification/master-roadmap.md).

#### 24.13 ¶3 — External repo governance (continuous loop)

Once a repo is blessed, four nightly / weekly automations keep it in shape without operator effort:

| Loop | Script | Cadence | What it does |
|:---|:---|:---|:---|
| Drift detection | `scripts/bless_external_repo.py --repo-slug <slug> --auto-pr` | nightly | Compares AKOS template sha256 against consumer copy; opens a PR via `gh` when drifted (idempotent on PR title). |
| Posture | `scripts/check_external_repo_ci_posture.py [--auto-fix]` | nightly + release-gate | Checks `ci.yml` jobs, branch protection, Vercel projects, Sentry liveness, Slack webhook presence, secret rotation freshness. Optional `--auto-fix` opens tracking issues for fixable observability gaps. |
| Snapshot | `scripts/snapshot_external_repos.py` | weekly | Writes a row into [`REPO_HEALTH_SNAPSHOT.csv`](references/hlk/compliance/REPO_HEALTH_SNAPSHOT.csv) with contract / mirror / CI / license / secret-rotation columns. |
| Type regeneration | `scripts/regen_consumer_types.py [--auto-pr]` | on canonical CSV change | Emits TypeScript interfaces from each consumed mirror CSV into the consumer's `lib/types/akos-mirrors.generated.ts`. |
| Canonical change broadcast | `scripts/notify_consumers_of_canonical_change.py --changed <name>[,…] [--open-issue]` | on canonical CSV change | Slack ops post + optional consumer issues for repos whose `consumes_mirrors` includes the changed name. |
| Branch protection | `scripts/configure_branch_protection.py [--repo-slug <slug>]` | weekly | Idempotent PUT to GitHub branch protection on `main`; aligns reviews, status checks, force-push, deletion, conversation resolution. |
| Vercel provisioning | `scripts/provision_vercel_project.py [--subdomain <slug>]` | on `SUBDOMAINS_REGISTRY.md` change | Ensures every active subdomain row has its named Vercel project + custom domain attached. |
| Secret rotation reminders | `scripts/secret_rotation_reminders.py [--strict]` | daily | Markdown summary + Slack post of overdue / approaching secret rotations across all blessed repos. |
| Un-blessed row detection | `scripts/detect_unblessed_registry_rows.py [--strict]` | release-gate | Surfaces `REPOSITORY_REGISTRY.csv` rows that are reachable on disk but missing the bless artefacts. |

The release-gate runs the contract check, the CI/CD posture check, and the un-blessed row detection (soft) on every invocation. The other loops are intended for nightly cron / GitHub Actions schedule on AKOS itself.

The three SOPs that procedurally document the bless / drift / propagation flow are:

- [`SOP-EXTERNAL_REPO_BLESSING_001.md`](references/hlk/v3.0/Admin/O5-1/Envoy%20Tech%20Lab/External%20Repos/SOP-EXTERNAL_REPO_BLESSING_001.md) — apply the kit.
- [`SOP-EXTERNAL_REPO_DRIFT_REMEDIATION_001.md`](references/hlk/v3.0/Admin/O5-1/Envoy%20Tech%20Lab/External%20Repos/SOP-EXTERNAL_REPO_DRIFT_REMEDIATION_001.md) — keep it aligned.
- [`SOP-CROSS_REPO_SCHEMA_PROPAGATION_001.md`](references/hlk/v3.0/Admin/O5-1/Envoy%20Tech%20Lab/Cross%20Repo/SOP-CROSS_REPO_SCHEMA_PROPAGATION_001.md) — propagate canonical CSV changes.

These ship at `status: review` 2026-05-06 (Initiative 63 P1). Promotion to `status: active` is gated by the I63 P3 operator review of the [CSV proposal](wip/planning/63-external-repo-governance-codification/reports/csv-proposal-2026-05-06.md).