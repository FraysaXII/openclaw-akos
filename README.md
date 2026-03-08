# OpenCLAW-AKOS

**Agentic Knowledge Operating System — Enterprise-Grade LLMOS Transformation for OpenCLAW**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![SOP Version](https://img.shields.io/badge/SOP-v3.0_March_2026-blue.svg)](docs/SOP.md)

## Overview

OpenCLAW-AKOS provides the architectural blueprints, standard operating procedures, and reference configurations required to upgrade a vanilla [OpenCLAW](https://github.com/openclaw/openclaw) deployment into a secure, modular, enterprise-grade **Large Language Model Operating System (LLMOS)**.

Out-of-the-box, OpenCLAW operates as an isolated conversational agent. This project transforms it into an **Agentic Knowledge Operating System** — an active participant that validates data against defined methodologies, orchestrates deterministic workflows, and maintains persistent identity across sessions.

## Key Capabilities

| Layer | Role | Implementation |
|:------|:-----|:---------------|
| **Control Plane** | Gateway daemon, FastAPI API, RunPod manager | `openclaw.json` + `akos/api.py` on port 8420 |
| **Integration Layer** | Channel adapters, 8 MCP servers | WebChat + optional Telegram, Slack, WhatsApp via `bindings` |
| **Execution Layer** | 4-agent runner (Orchestrator, Architect, Executor, Verifier) | Decompose, plan, build, validate |
| **Intelligence Layer** | Flat memory architecture, context compression | MCP Memory server, workspace files, Intelligence Matrix fact tagging |

## Architecture

The system implements the **Four-Layer LLMOS Paradigm** with a **Multi-Agent Model** (v0.4.0) that separates cognitive workload:

- **Orchestrator Agent** -- decomposes user requests into sub-tasks and delegates to the right agent
- **Architect Agent** -- operates in read-only, high-context planning mode using sequential thinking
- **Executor Agent** -- fast, read-write model that executes strict directives from the Architect
- **Verifier Agent** -- validates Executor output via lint, test, build, and browser verification

This separation eliminates cognitive overload and adds a quality gate with a 3-retry error recovery loop.

## Core MCP Integrations

- **Sequential Thinking** (`@modelcontextprotocol/server-sequential-thinking`) -- structured multi-step reasoning
- **Playwright** (`@playwright/mcp@latest`) -- deep web automation with DOM-level interaction
- **GitHub** -- governed codebase auditing without exhausting context windows
- **Memory** (`@modelcontextprotocol/server-memory`) -- cross-session key-value recall
- **Filesystem** (`@modelcontextprotocol/server-filesystem`) -- structured file operations
- **Fetch** (`@modelcontextprotocol/server-fetch`) -- HTTP client for API integration
- **LSP** (`@akos/mcp-lsp-server`) -- type-aware code navigation (go-to-definition, find-references, diagnostics)
- **Code Search** (`@akos/mcp-code-search`) -- semantic code search via ripgrep + tree-sitter
- **mcporter** -- CLI and configuration manager for all MCP connections

## Security Posture

> The discovery of the **ClawHavoc** campaign distributing Atomic Stealer (AMOS) malware via malicious ClawHub skills dictates that a **Zero-Trust, sandboxed operational posture** is mandatory.

- **Pre-execution skill auditing** via `skillvet` (48 vulnerability checks)
- **Human-in-the-Loop (HITL)** enforcement for all mutative operations
- **WSL2 / Docker sandbox** isolation — the agent never runs on bare metal
- **SIEM integration** (Splunk) for SOC-level anomaly detection
- **EU AI Act 2026 compliance** — automated record-keeping, human oversight, risk management

See [SECURITY.md](SECURITY.md) for the full security policy.

## Quick Start

### Any OS (Cross-Platform Bootstrap)

Requires Python 3.10+, Node.js >= 22, and Ollama running:

```bash
python scripts/bootstrap.py
```

The script detects your OS, checks prerequisites, pulls Ollama models, patches `openclaw.json`, sets up MCP servers, and assembles tiered prompts. Use `--skip-ollama` or `--skip-mcp` to skip phases.

### Windows (PowerShell Bootstrap)

If you prefer native PowerShell:

```powershell
.\scripts\bootstrap.ps1
```

Use `-SkipWSL`, `-SkipOllama`, or `-SkipMCP` to skip individual phases.

### Switching Models / Environments

After bootstrap, switch between model tiers and deployment targets with a single command:

```bash
python scripts/switch-model.py dev-local      # Local Ollama (small model)
python scripts/switch-model.py gpu-runpod      # Remote GPU (large model, auto-provisions RunPod endpoint)
python scripts/switch-model.py prod-cloud      # Cloud APIs (SOTA model)
python scripts/switch-model.py dev-local --dry-run  # Preview without applying
```

This atomically updates the config, deploys the correct SOUL.md prompt variant, and restarts the gateway. For `gpu-runpod`, it also provisions the RunPod vLLM endpoint and writes the URL to `.env`.

### Control Plane API

```bash
python scripts/serve-api.py --port 8420
```

Exposes REST endpoints for health, status, model switching, RunPod management, agent listing, metrics, alerts, workspace checkpoints, and a live log WebSocket at `/logs`.

### Windows (Manual / WSL2)

```bash
# 1. Install Ubuntu under WSL2
wsl --install -d Ubuntu-24.04

# 2. Enable systemd
sudo tee /etc/wsl.conf >/dev/null <<'EOF'
[boot]
systemd=true
EOF

# 3. Restart WSL and create a dedicated service account
wsl --shutdown
sudo adduser --system --group openclaw
sudo mkdir /opt/openclaw && sudo chown openclaw:openclaw /opt/openclaw

# 4. Install OpenCLAW CLI
curl -fsSL https://molt.bot/install.sh | bash

# 5. Bootstrap the gateway
openclaw onboard --install-daemon
```

### macOS / Linux (Docker Sandbox)

```bash
# 1. Pull the model and create the sandbox
docker model pull ai/gpt-oss:20B-UD-Q4_K_XL
docker sandbox create --name openclaw -t olegselajev241/openclaw-dmr:latest shell

# 2. Lock down the network
docker sandbox network proxy openclaw --allow-host localhost

# 3. Launch the gateway
docker sandbox run openclaw ~/start-openclaw.sh
```

See the full [Standard Operating Procedure](docs/SOP.md) for detailed step-by-step instructions.

## Repository Structure

```
openclaw-akos/
  akos/                             Shared orchestration library (Python)
    __init__.py                     Package marker + version (v0.4.0)
    models.py                       Pydantic schemas for all config files (incl. RunPod)
    io.py                           load_json, save_json, deep_merge, AGENT_WORKSPACES (4-agent)
    log.py                          JSONFormatter + HumanFormatter, setup_logging()
    process.py                      CommandResult + run() subprocess wrapper with timeouts
    state.py                        AkosState model + load/save for deployment tracking
    telemetry.py                    LangfuseReporter + DX metrics tracking
    alerts.py                       AlertEvaluator for real-time + periodic checks
    runpod_provider.py              RunPod SDK wrapper (endpoint lifecycle, health, inference)
    api.py                          FastAPI control plane (REST + WebSocket)
    tools.py                        Dynamic tool registry (mcporter + permissions)
    checkpoints.py                  Workspace snapshot/restore for reversible execution
  config/
    openclaw.json.example           Gateway config template with multi-provider support
    model-tiers.json                SSOT for model classification (small/medium/large/sota)
    mcporter.json.example           MCP server definitions (T-2.3–T-2.6)
    permissions.json                HITL policy — autonomous vs requires_approval (T-3.3)
    logging.json                    Structured JSON logging config (T-3.5)
    intelligence-matrix-schema.json Holistika DI fact schema (T-4.3)
    environments/
      dev-local.env.example         Local Ollama env vars
      dev-local.json                Config overlay for local dev
      gpu-runpod.env.example        RunPod/ShadowGPU env vars
      gpu-runpod.json               Config overlay for GPU deployment
      prod-cloud.env.example        Cloud API keys (placeholder)
      prod-cloud.json               Config overlay for cloud APIs
    splunk/
      inputs.conf                   Splunk Universal Forwarder template (T-3.6)
    compliance/
      eu-ai-act-checklist.json      EU AI Act compliance evidence map (T-3.7)
    eval/
      langfuse.env.example          Eval platform scaffold (T-5.1)
      baselines.json                DX metric baselines (T-5.2)
      alerts.json                   SOC alerting thresholds (T-5.3)
  prompts/
    ORCHESTRATOR_PROMPT.md          Coordinator system prompt (compact)
    ARCHITECT_PROMPT.md             Read-only planner system prompt (compact)
    EXECUTOR_PROMPT.md              Read-write builder system prompt (compact)
    VERIFIER_PROMPT.md              Quality gate system prompt (compact)
    base/
      ORCHESTRATOR_BASE.md          Core orchestrator identity and rules
      ARCHITECT_BASE.md             Core architect identity and rules
      EXECUTOR_BASE.md              Core executor identity and rules (3-retry recovery loop)
      VERIFIER_BASE.md              Core verifier identity and rules
    overlays/
      OVERLAY_REASONING.md          Sequential thinking (medium+ models)
      OVERLAY_INTELLIGENCE.md       Intelligence matrix (large+ models)
      OVERLAY_CONTEXT_MANAGEMENT.md Context compression (large+ models)
      OVERLAY_TOOLS_FULL.md         Advanced tool patterns (large+ models)
      OVERLAY_PLAN_TODOS.md            Structured planning protocol (standard+ models)
      OVERLAY_RESEARCH.md              Research with citations (full models)
      OVERLAY_WORKFLOWS.md             Workflow invocation protocol (full models)
    assembled/                      Generated by assemble-prompts.py (gitignored)
  scripts/
    bootstrap.py                    Cross-platform setup (Python, any OS)
    bootstrap.ps1                   Windows-native setup (PowerShell)
    assemble-prompts.py             Build tiered SOUL.md from base + overlays
    switch-model.py                 Activate environment profile and deploy prompts
    log-watcher.py                  Tail gateway logs, push to Langfuse, evaluate alerts
    vet-install.sh                  Safe skill installation wrapper (T-3.2)
    serve-api.py                    FastAPI control plane launcher
    check-drift.py                 Runtime drift detection (repo vs live)
    doctor.py                      One-command system health check
    sync-runtime.py                Runtime hydration from repo SSOT
    release-gate.py                Unified release gate runner
    browser-smoke.py               Programmatic browser smoke test (6 scenarios)
    run-evals.py                   Agent reliability eval runner (5 canonical tasks)
    checkpoint.py                  Checkpoint CLI (create/list/restore snapshots)
    test.py                        Friendly test runner with groups
  tests/
    conftest.py                     Shared fixtures
    validate_configs.py             Config JSON validation via Pydantic
    validate_multimodel.py          Multi-model architecture validation
    validate_prompts.py             Prompt content validation
    validate_scripts.py             Shell script validation
    e2e_scaffolding.py              E2E: tree completeness, cross-refs, secrets scan
    test_akos_models.py             Pydantic model unit tests (good/bad data)
    test_akos_alerts.py             AlertEvaluator unit tests (synthetic log entries)
    test_runpod_provider.py         RunPod provider tests (mocked SDK)
    test_api.py                     FastAPI endpoint tests (TestClient)
    test_checkpoints.py             Workspace checkpoint tests
    test_live_smoke.py             Opt-in live provider tests (@pytest.mark.live)
    evals/                         Agent reliability eval tasks (tasks.json)
  docs/
    SOP.md                          Full Standard Operating Procedure
    ARCHITECTURE.md                 Four-Layer LLMOS architecture diagrams
    USER_GUIDE.md                  End-user installation, config, usage guide
    wip/                           Work-in-progress improvement proposals
  config/
    agent-capabilities.json         Role capability matrix SSOT
    workflows/                      Reusable workflow definitions (6 workflows)
    templates/                      Session templates (architecture review, bug investigation, refactor)
    memory-templates/               Memory domain templates (decisions, incidents, policies, sources)
    policies/                       Governance policy packs (engineering-safe, compliance, incident-response)
    workflow-packs/                 Team-distributable workflow collections (release, backend)
    workspace-scaffold/*/RULES.md   User-customizable rules for each agent
  docs/uat/
    dashboard_smoke.md              Browser smoke test scenarios (6 scenarios)
    rollback_guide.md               Rollback guidance by failure class
```

## Observability

The log watcher tails the OpenCLAW gateway log, pushes agent traces to Langfuse, and evaluates real-time SOC alerts.

### Activating Langfuse Telemetry

1. Sign up at [app.langfuse.com](https://cloud.langfuse.com) (free tier) or [self-host](https://langfuse.com/docs/deployment/self-host)
2. Copy the template: `cp config/eval/langfuse.env.example config/eval/langfuse.env`
3. Fill in your keys in `config/eval/langfuse.env`
4. Start the watcher alongside the gateway:

```bash
# Foreground watcher (loads keys from config/eval/langfuse.env automatically)
python scripts/log-watcher.py

# Dry-run mode (prints traces without calling Langfuse SDK)
python scripts/log-watcher.py --dry-run

# Custom env file location
python scripts/log-watcher.py --env-file /path/to/langfuse.env

# Single pass for CI
python scripts/log-watcher.py --once --json-log
```

Without credentials, telemetry degrades gracefully to a no-op -- the watcher still evaluates alerts and logs to stdout.

## Running Tests

```bash
# Install dependencies (pydantic is required; langfuse is optional)
pip install -r requirements.txt

# Full suite (193+ tests) -- pyproject.toml configures discovery
py -m pytest -v

# Individual batches
py -m pytest tests/validate_configs.py -v       # Config validation (Pydantic)
py -m pytest tests/validate_multimodel.py -v    # Multi-model architecture
py -m pytest tests/validate_prompts.py -v       # Prompt content
py -m pytest tests/test_akos_models.py -v       # Pydantic model schemas
py -m pytest tests/test_akos_alerts.py -v       # Alert evaluation engine
py -m pytest tests/test_runpod_provider.py -v   # RunPod provider (mocked SDK)
py -m pytest tests/test_api.py -v               # FastAPI control plane
py -m pytest tests/test_checkpoints.py -v       # Workspace checkpoints
py -m pytest tests/e2e_scaffolding.py -v        # E2E scaffolding check

# Friendly test runner
py scripts/test.py                    # All tests
py scripts/test.py api                # FastAPI endpoints
py scripts/test.py security           # Alerts + configs
py scripts/test.py drift              # Runtime drift check
py scripts/test.py live               # Live provider smoke (needs AKOS_LIVE_SMOKE=1)
py scripts/test.py uat                # Start live API for Swagger testing
py scripts/test.py --list             # Show all groups

# Release gate (all lanes)
py scripts/release-gate.py

# System health check
py scripts/doctor.py
```

## Documentation

| Document | Description |
|:---------|:------------|
| [SOP](docs/SOP.md) | Complete Standard Operating Procedure for the LLMOS transformation |
| [Implementation Task Registry](docs/SOP.md#80-implementation-task-registry) | 33 traceable tasks across 6 phases with SSOT/SOC/DI/DX attributes |
| [Architecture](docs/ARCHITECTURE.md) | Four-Layer LLMOS architecture and data flow diagrams |
| [Security](SECURITY.md) | Zero-Trust security policy, threat model, and compliance |
| [User Guide](docs/USER_GUIDE.md) | End-user installation, configuration, and usage manual |
| [Changelog](CHANGELOG.md) | Version history from v0.0.1 to current |
| [Contributing](CONTRIBUTING.md) | How to contribute to this project |

## Methodology

The architectural design is grounded in the **Holistika Methodological Trinity**:

1. **Strategy** — The agent as an Agentic Knowledge Operating System (AKOS), not a passive responder
2. **Tactics** — The Intelligence Matrix for structured data classification (Fact IDs, source credibility, impact scoring)
3. **Processes** — Modular execution via MCP, decoupling reasoning from infrastructure

## Metrics and Evaluation

| Metric | Target |
|:-------|:-------|
| **Completion Rate** | >60% success on multi-step autonomous workflows |
| **Containment Rate** | Minimize human escalation for low-risk tasks |
| **PR Throughput** | 46%+ increase via multi-agent paradigm |
| **Prompt Injection Vulnerability Rate** | Absolute minimization |

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Acknowledgments

- [OpenCLAW](https://github.com/openclaw/openclaw) — the foundational agent framework
- [Model Context Protocol](https://github.com/modelcontextprotocol) — universal tool integration standard
- Holistika Framework — business logic methodology informing the architectural design
