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

## References

- Full implementation details: [SOP.md](SOP.md)
- Security controls: [SECURITY.md](../SECURITY.md)
