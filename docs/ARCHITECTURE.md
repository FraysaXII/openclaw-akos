# OpenCLAW-AKOS Architecture

## Four-Layer LLMOS Paradigm

The system decouples the reasoning engine from its tools and channels across four functional domains.

```
┌─────────────────────────────────────────────────────────┐
│                    CONTROL PLANE                        │
│              (Gateway — openclaw daemon)                │
│         Bound to 127.0.0.1:18789 (localhost)           │
│    Workspace routing · Auth · Channel multiplexing      │
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

## Observability Stack

| Component | Role | Target |
|:----------|:-----|:-------|
| Structured JSON Logs | Agent activity tracing | `/opt/openclaw/logs/` |
| Splunk Universal Forwarder | Log shipping | `ai_agent_ops` index |
| AI Evaluation Platform | Metrics (Langfuse / Maxim AI) | Completion rate, latency, cost |
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
| Integration | [`config/mcporter.json.example`](../config/mcporter.json.example) | T-2.3–T-2.6 |
| All | [`config/permissions.json`](../config/permissions.json) | T-3.3 |
| All | [`config/logging.json`](../config/logging.json) | T-3.5 |
| All | [`config/splunk/inputs.conf`](../config/splunk/inputs.conf) | T-3.6 |
| Intelligence | [`config/intelligence-matrix-schema.json`](../config/intelligence-matrix-schema.json) | T-4.3 |
| Execution | [`prompts/ARCHITECT_PROMPT.md`](../prompts/ARCHITECT_PROMPT.md) | T-4.1 |
| Execution | [`prompts/EXECUTOR_PROMPT.md`](../prompts/EXECUTOR_PROMPT.md) | T-4.2 |
| All | [`scripts/vet-install.sh`](../scripts/vet-install.sh) | T-3.2 |
| All | [`config/eval/baselines.json`](../config/eval/baselines.json) | T-5.2 |
| All | [`config/eval/alerts.json`](../config/eval/alerts.json) | T-5.3 |

A validation test suite (`tests/`) provides 70 automated checks covering JSON integrity, cross-file reference consistency, secret scanning, and SOP task coverage.

## References

- Implementation task registry: [SOP.md Section 8.0](SOP.md#80-implementation-task-registry)
- Full SOP (sections 1.0–7.0): [SOP.md](SOP.md)
- Security controls: [SECURITY.md](../SECURITY.md)
