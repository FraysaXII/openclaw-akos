# OpenCLAW-AKOS

**Agentic Knowledge Operating System — Enterprise-Grade LLMOS Transformation for OpenCLAW**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![SOP Version](https://img.shields.io/badge/SOP-v2.1_March_2026-blue.svg)](docs/SOP.md)

## Overview

OpenCLAW-AKOS provides the architectural blueprints, standard operating procedures, and reference configurations required to upgrade a vanilla [OpenCLAW](https://github.com/openclaw/openclaw) deployment into a secure, modular, enterprise-grade **Large Language Model Operating System (LLMOS)**.

Out-of-the-box, OpenCLAW operates as an isolated conversational agent. This project transforms it into an **Agentic Knowledge Operating System** — an active participant that validates data against defined methodologies, orchestrates deterministic workflows, and maintains persistent identity across sessions.

## Key Capabilities

| Layer | Role | Implementation |
|:------|:-----|:---------------|
| **Control Plane** | Gateway daemon, routing, auth | `openclaw.json` bound to `127.0.0.1:18789` |
| **Integration Layer** | Channel adapters, MCP servers | WebChat + optional Telegram, Slack, WhatsApp via `bindings` |
| **Execution Layer** | Dual-agent runner (Architect + Executor) | Read-only Planner + Read-write Builder |
| **Intelligence Layer** | Knowledge graph, sequential reasoning | GraphRAG with predicate allowlists and confidence thresholds |

## Architecture

The system implements the **Four-Layer LLMOS Paradigm** with a **Dual-Agent Model** that separates cognitive workload:

- **Architect Agent** — operates in read-only, high-context planning mode using sequential thinking
- **Executor Agent** — fast, read-write model that executes strict directives from the Architect

This separation eliminates cognitive overload that causes context degradation, hallucinations, and infinite debugging loops.

## Core MCP Integrations

- **Sequential Thinking** (`@modelcontextprotocol/server-sequential-thinking`) — structured multi-step reasoning
- **Playwright** (`@playwright/mcp@latest`) — deep web automation with DOM-level interaction
- **GitHub** — governed codebase auditing without exhausting context windows
- **mcporter** — CLI and configuration manager for all MCP connections

## Security Posture

> The discovery of the **ClawHavoc** campaign distributing Atomic Stealer (AMOS) malware via malicious ClawHub skills dictates that a **Zero-Trust, sandboxed operational posture** is mandatory.

- **Pre-execution skill auditing** via `skillvet` (48 vulnerability checks)
- **Human-in-the-Loop (HITL)** enforcement for all mutative operations
- **WSL2 / Docker sandbox** isolation — the agent never runs on bare metal
- **SIEM integration** (Splunk) for SOC-level anomaly detection
- **EU AI Act 2026 compliance** — automated record-keeping, human oversight, risk management

See [SECURITY.md](SECURITY.md) for the full security policy.

## Quick Start

### Windows (Automated Bootstrap)

If you have Ollama and Node.js >= 22 installed, the bootstrap script handles everything else:

```powershell
.\scripts\bootstrap.ps1
```

The script is idempotent (safe to re-run) and covers WSL provisioning, Ollama model setup, OpenCLAW configuration, and MCP server injection. Use `-SkipWSL`, `-SkipOllama`, or `-SkipMCP` to skip individual phases.

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
  config/
    openclaw.json.example           Gateway config template (T-1.2)
    mcporter.json.example           MCP server definitions (T-2.3–T-2.6)
    permissions.json                HITL policy — autonomous vs requires_approval (T-3.3)
    logging.json                    Structured JSON logging config (T-3.5)
    intelligence-matrix-schema.json Holistika DI fact schema (T-4.3)
    splunk/
      inputs.conf                   Splunk Universal Forwarder template (T-3.6)
    compliance/
      eu-ai-act-checklist.json      EU AI Act compliance evidence map (T-3.7)
    eval/
      langfuse.env.example          Eval platform scaffold (T-5.1)
      baselines.json                DX metric baselines (T-5.2)
      alerts.json                   SOC alerting thresholds (T-5.3)
  prompts/
    ARCHITECT_PROMPT.md             Read-only planner system prompt (T-4.1)
    EXECUTOR_PROMPT.md              Read-write builder system prompt (T-4.2)
  scripts/
    bootstrap.ps1                   Full environment setup (Ollama, MCP, WSL)
    vet-install.sh                  Safe skill installation wrapper (T-3.2)
  tests/
    conftest.py                     Shared fixtures
    validate_configs.py             Unit tests for all JSON configs
    validate_prompts.py             Unit tests for prompt content
    validate_scripts.py             Unit tests for shell scripts
    e2e_scaffolding.py              E2E: tree completeness, cross-refs, secrets scan
  docs/
    SOP.md                          Full Standard Operating Procedure
    ARCHITECTURE.md                 Four-Layer LLMOS architecture diagrams
```

## Running Tests

```bash
# Full suite (76 tests: unit + E2E)
py -m pytest tests/validate_configs.py tests/validate_prompts.py tests/validate_scripts.py tests/e2e_scaffolding.py -v

# Individual batches
py -m pytest tests/validate_configs.py -v    # Config validation
py -m pytest tests/validate_prompts.py -v    # Prompt validation
py -m pytest tests/validate_scripts.py -v    # Script validation
py -m pytest tests/e2e_scaffolding.py -v     # E2E scaffolding check
```

## Documentation

| Document | Description |
|:---------|:------------|
| [SOP](docs/SOP.md) | Complete Standard Operating Procedure for the LLMOS transformation |
| [Implementation Task Registry](docs/SOP.md#80-implementation-task-registry) | 33 traceable tasks across 6 phases with SSOT/SOC/DI/DX attributes |
| [Architecture](docs/ARCHITECTURE.md) | Four-Layer LLMOS architecture and data flow diagrams |
| [Security](SECURITY.md) | Zero-Trust security policy, threat model, and compliance |
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
| **PR Throughput** | 46%+ increase via dual-agent paradigm |
| **Prompt Injection Vulnerability Rate** | Absolute minimization |

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Acknowledgments

- [OpenCLAW](https://github.com/openclaw/openclaw) — the foundational agent framework
- [Model Context Protocol](https://github.com/modelcontextprotocol) — universal tool integration standard
- Holistika Framework — business logic methodology informing the architectural design
