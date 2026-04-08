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
| **Control Plane** | Gateway daemon, FastAPI API, GPU provider manager (RunPod + ShadowPC OpenStack), auto-failover router | `openclaw.json` + `akos/api.py` on port 8420 |
| **Integration Layer** | Channel adapters, 11 MCP servers + gateway-enforced tool profiles | WebChat + optional Telegram, Slack, WhatsApp via `bindings` |
| **Execution Layer** | 5-agent runner (Madeira, Orchestrator, Architect, Executor, Verifier) | Answer, decompose, plan, build, validate |
| **Intelligence Layer** | Flat memory architecture, context compression | MCP Memory server, workspace files, Intelligence Matrix fact tagging |

## Architecture

The system implements the **Four-Layer LLMOS Paradigm** with a **Multi-Agent Model** (v0.6.0) that separates cognitive workload:

- **Madeira Agent** -- user-facing HLK lookup assistant that answers directly and escalates write/admin workflows
- **Orchestrator Agent** -- decomposes user requests into sub-tasks and delegates to the right agent
- **Architect Agent** -- operates in read-only, high-context planning mode using sequential thinking
- **Executor Agent** -- fast, read-write model that executes strict directives from the Architect
- **Verifier Agent** -- validates Executor output via lint, test, build, and browser verification

This separation eliminates cognitive overload and adds a quality gate with a 3-retry error recovery loop.

- **Gateway-agnostic design** — AKOS policy is defined in repo files and pushed to the runtime via bootstrap. See the [AKOS / OpenClaw Responsibility Matrix](docs/ARCHITECTURE.md#akos--openclaw-responsibility-matrix) for the full component map.

## Core MCP Integrations

- **Sequential Thinking** (`@modelcontextprotocol/server-sequential-thinking`) -- structured multi-step reasoning
- **Playwright** (`@playwright/mcp@latest`) -- deep web automation with DOM-level interaction
- **GitHub** -- governed codebase auditing without exhausting context windows
- **Memory** (`@modelcontextprotocol/server-memory`) -- cross-session key-value recall
- **Filesystem** (`@modelcontextprotocol/server-filesystem`) -- structured file operations
- **Fetch** (`@modelcontextprotocol/server-fetch`) -- HTTP client for API integration
- **LSP** (`@akos/mcp-lsp-server`) -- type-aware code navigation (go-to-definition, find-references, diagnostics)
- **Code Search** (`@akos/mcp-code-search`) -- semantic code search via ripgrep + tree-sitter
- **Custom AKOS MCP** (`scripts/mcp_akos_server.py`) -- control plane self-check: `akos_health`, `akos_agents`, `akos_status`
- **Finance Research MCP** (`scripts/finance_mcp_server.py`) -- read-only financial data: `finance_quote`, `finance_search`, `finance_sentiment` (yfinance + Alpha Vantage)
- **HLK Registry MCP** (`scripts/hlk_mcp_server.py`) -- read-only organisational and process lookup: `hlk_role`, `hlk_role_chain`, `hlk_area`, `hlk_process`, `hlk_process_tree`, `hlk_projects`, `hlk_gaps`, `hlk_search`
- **mcporter** -- CLI and configuration manager for all MCP connections

**Optional:** cursor-ide-browser (Cursor IDE built-in) for in-IDE WebChat testing; AKOS agent uses Playwright MCP.

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

The script detects your OS, checks prerequisites, pulls Ollama models, patches `openclaw.json`, sets up MCP servers, and assembles tiered prompts. Use `--skip-ollama` or `--skip-mcp` to skip phases. If you copied `mcporter.json.example` manually, run `py scripts/resolve-mcporter-paths.py` to resolve placeholder paths.

### Windows (PowerShell Bootstrap)

If you prefer native PowerShell:

```powershell
.\scripts\bootstrap.ps1
```

Use `-SkipWSL`, `-SkipOllama`, or `-SkipMCP` to skip individual phases.

### GPU Infrastructure Deployment

Deploy RunPod dedicated pods or serverless endpoints with a single command — no copy-paste, no manual dashboard steps:

```bash
py scripts/gpu.py
```

The interactive CLI guides you through choosing **local**, **RunPod serverless endpoint**, or **RunPod dedicated pod**, then auto-generates the right configuration from the model catalog. It manages pods via the `PodManager` REST API, auto-generates vLLM launch commands via `PodConfig.build_vllm_command()`, and derives `TENSOR_PARALLEL_SIZE` from `gpuCount` to avoid world-size errors. Idempotent: reuses an existing pod if one is already running. `ActiveInfra` state tracks what's running (pod/serverless/local).

### Switching Models / Environments

After bootstrap, switch between model tiers and deployment targets with a single command:

```bash
python scripts/switch-model.py dev-local      # Local Ollama (medium model)
python scripts/switch-model.py gpu-runpod      # Remote GPU (large model)
python scripts/switch-model.py prod-cloud      # Cloud APIs (SOTA model)
python scripts/switch-model.py dev-local --dry-run  # Preview without applying
```

This atomically updates the config, deploys the correct SOUL.md prompt variant, and restarts the gateway. For `gpu-runpod`, run `py scripts/gpu.py` first to provision the GPU infrastructure.

AKOS enforces a full-only provider inventory contract: bootstrap retains all providers from `config/openclaw.json.example` and reports unresolved env-backed inputs as warnings instead of deleting provider blocks. On first run, bootstrap auto-seeds `~/.openclaw/.env` with deterministic runtime placeholder values, and `switch-model.py` then copies the selected real profile env file from `config/environments/*.env`.

If the Windows gateway is flaky after reboot (timeouts, `port already in use` on 18789, or connection refused while a listener still shows in `netstat`), run:

```bash
py scripts/doctor.py --repair-gateway
```

That path runs upstream OpenClaw doctor repair, stops the gateway, clears orphan listeners on port 18789 on Windows, and starts the supervised gateway again—matching the recovery sequence used after `switch-model.py`.

Preferred operator flow:

1. `py scripts/doctor.py --repair-gateway`
2. `py scripts/switch-model.py <profile>`
3. `py scripts/gpu.py` only when a GPU provider is involved
4. Verify with `py scripts/doctor.py` and any provider-specific health checks

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
    __init__.py                     Package marker + version (v0.5.0)
    models.py                       Pydantic schemas for all config files (incl. RunPod)
    model_catalog.py                CatalogEntry model + load_catalog() for GPU model SSOT
    io.py                           load_json, save_json, deep_merge, AGENT_WORKSPACES (5-agent)
    log.py                          JSONFormatter + HumanFormatter, setup_logging()
    process.py                      CommandResult + run() subprocess wrapper with timeouts
    state.py                        AkosState model + load/save for deployment tracking
    telemetry.py                    LangfuseReporter + DX metrics tracking
    alerts.py                       AlertEvaluator for real-time + periodic checks
    runpod_provider.py              RunPod SDK wrapper + PodManager REST API (pod/serverless)
    openstack_provider.py           ShadowPC OpenStack SDK wrapper (instance lifecycle, spot, security groups)
    api.py                          FastAPI control plane (REST + WebSocket)
    tools.py                        Dynamic tool registry (mcporter + permissions)
    checkpoints.py                  Workspace snapshot/restore for reversible execution
  config/
    openclaw.json.example           Gateway config template with multi-provider support
    model-tiers.json                SSOT for model classification (small/medium/large/sota)
    model-catalog.json              SSOT for GPU-deployable models (VRAM, parsers, GPU defaults)
    mcporter.json.example           MCP server definitions (T-2.3–T-2.6)
    permissions.json                HITL policy — autonomous vs requires_approval (T-3.3)
    logging.json                    Structured JSON logging config (T-3.5)
    intelligence-matrix-schema.json Holistika DI fact schema (T-4.3)
    environments/
      dev-local.env                 Local Ollama env profile (operative)
      dev-local.env.example         Reference template
      dev-local.json                Config overlay for local dev
      gpu-runpod.env                RunPod serverless env profile (operative)
      gpu-runpod.env.example        Reference template
      gpu-runpod.json               Config overlay for GPU deployment
      gpu-runpod-pod.env            RunPod dedicated pod env profile (operative)
      gpu-runpod-pod.env.example    Reference template
      gpu-shadow.env                Shadow OpenStack env profile (operative)
      gpu-shadow.env.example        Reference template
      prod-cloud.env                Cloud API env profile (operative)
      prod-cloud.env.example        Reference template
      prod-cloud.json               Config overlay for cloud APIs
    splunk/
      inputs.conf                   Splunk Universal Forwarder template (T-3.6)
    compliance/
      eu-ai-act-checklist.json      EU AI Act compliance evidence map (T-3.7)
    eval/
      baselines.json                DX metric baselines (T-5.2)
      alerts.json                   SOC alerting thresholds (T-5.3)
  prompts/
    MADEIRA_PROMPT.md               HLK lookup assistant system prompt (compact)
    ORCHESTRATOR_PROMPT.md          Coordinator system prompt (compact)
    ARCHITECT_PROMPT.md             Read-only planner system prompt (compact)
    EXECUTOR_PROMPT.md              Read-write builder system prompt (compact)
    VERIFIER_PROMPT.md              Quality gate system prompt (compact)
    base/
      MADEIRA_BASE.md               Core Madeira identity and lookup rules
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
    gpu.py                          Interactive GPU infrastructure CLI (RunPod pod/serverless)
    check-drift.py                 Runtime drift detection (repo vs live)
    doctor.py                      One-command system health check
    sync-runtime.py                Runtime hydration from repo SSOT
    release-gate.py                Unified release gate runner
    resolve-mcporter-paths.py      Resolve MCP config placeholder paths
    browser-smoke.py               Programmatic browser smoke test (6 scenarios)
    run-evals.py                   Agent reliability eval runner (5 canonical tasks)
    checkpoint.py                  Checkpoint CLI (create/list/restore snapshots)
    test.py                        Friendly test runner with groups
    adhoc/                         Scratch operator scripts (RunPod/endpoints/etc.); not part of release gate
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
    test_pod_manager.py             PodManager dedicated pod lifecycle tests
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
2. Put `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, and `LANGFUSE_HOST` in `~/.openclaw/.env` or export them in the process environment.
3. Keep non-secret watcher settings in `config/openclaw.json.example` under `diagnostics.logWatcher` (bootstrap writes them to `~/.openclaw/akos-config.json`).
4. Start the watcher alongside the gateway:

```bash
# Foreground watcher (loads keys from process env or ~/.openclaw/.env)
python scripts/log-watcher.py

# Dry-run mode (prints traces without calling Langfuse SDK)
python scripts/log-watcher.py --dry-run

# Single pass for CI
python scripts/log-watcher.py --once --json-log
```

Without credentials, telemetry degrades gracefully to a no-op -- the watcher still evaluates alerts and logs to stdout.

Langfuse traces are tagged with the active environment name (e.g. `gpu-runpod`, `gpu-runpod-pod`) for multi-env filtering. The trace taxonomy includes `trace_request` (per-request), `trace_startup_compliance` (audit scores), `trace_answer_quality` (flagship user-visible outcomes), `trace_alert` (SOC alert forwarding), and `trace_metric` (DX request counts / latency). The watcher also mirrors answer-quality records locally under `~/.openclaw/telemetry/`.

## Running Tests

```bash
# Install dependencies (pydantic is required; langfuse is optional)
pip install -r requirements.txt

# Full suite (300+ tests) -- pyproject.toml configures discovery
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
py -m pytest tests/test_telemetry.py -v         # Langfuse telemetry (14 tests)
py -m pytest tests/test_router.py -v            # FailoverRouter (10 tests)

# Friendly test runner
py scripts/test.py                    # All tests
py scripts/test.py api                # FastAPI endpoints
py scripts/test.py security           # Alerts + configs
py scripts/test.py drift              # Runtime drift check
py scripts/test.py live               # Live provider smoke (needs AKOS_LIVE_SMOKE=1)
py scripts/test.py uat                # Start live API for Swagger testing
py scripts/test.py --list             # Show all groups

# Release gate (all lanes)
py scripts/legacy/verify_openclaw_inventory.py
py scripts/check-drift.py
py scripts/test.py all
py scripts/browser-smoke.py --playwright
py -m pytest tests/test_api.py -v
py scripts/release-gate.py
py scripts/validate_hlk.py
py scripts/validate_hlk_km_manifests.py   # when editing docs/references/hlk/v3.0/_assets/**/*.manifest.md

# System health check
py scripts/doctor.py
```

`scripts/doctor.py` includes a runtime-contract probe that normalizes `openclaw gateway status` output. If OpenClaw reports `Runtime: unknown` but `RPC probe: ok` and `Listening` are healthy, AKOS records runtime as `healthy` and verifies determinism across repeated probes. Doctor also runs `check_runpod_readiness()` (config, API key, vLLM health probe for dedicated pods) and `check_langfuse_readiness()` (credentials, SDK init).
On Windows hosts where Playwright browser processes crash (`0xC0000005`), `scripts/browser-smoke.py --playwright` isolates browser attempts in worker subprocesses and returns explicit `SKIP` outcomes instead of crashing the gate process.

## Documentation

| Document | Description |
|:---------|:------------|
| [SOP](docs/SOP.md) | Complete Standard Operating Procedure for the LLMOS transformation |
| [Implementation Task Registry](docs/SOP.md#80-implementation-task-registry) | 33 traceable tasks across 6 phases with SSOT/SOC/DI/DX attributes |
| [Architecture](docs/ARCHITECTURE.md) | Four-Layer LLMOS architecture and data flow diagrams |
| [AKOS / OpenClaw Responsibility Matrix](docs/ARCHITECTURE.md#akos--openclaw-responsibility-matrix) | Component ownership and interaction map |
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
