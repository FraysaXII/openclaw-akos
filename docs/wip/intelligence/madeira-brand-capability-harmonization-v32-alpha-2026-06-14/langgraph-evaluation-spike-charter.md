---
authored: 2026-06-15
status: open_fail_until_ci
opened: 2026-06-15
reopened: 2026-06-16
closure_report: docs/wip/planning/76-madeira-elevation/reports/langgraph-evaluation-spike-closure-2026-06-16.md
ci_proof: .github/workflows/langgraph-spike-smoke.yml
parent: prong-synthesis-P-I-substrate-reliability.md
timebox: 3 engineering days
---

# Evaluation spike — LangGraph OSS (second substrate method)

> **Purpose:** Prove one **non-OpenClaw** path can hit the same **CAP-M*** outcome rows for a bounded subset — per operator multi-method portfolio steering.

## Target capabilities (must match or narrow DATA_CONTRACT)

| CAP ID | Spike outcome |
|:---|:---|
| CAP-M05 | Research action loop on a fixed source-ledger fixture |
| CAP-M10 | Langfuse trace with `substrate_adapter_id=langgraph_oss_selfhost` |
| CAP-M21 | MCP tool call through graph node (read posture) |

## Spike architecture (minimal)

- LangGraph graph: ingest → rate → synthesize (mock)
- **PostgresSaver** checkpointer (local Docker Postgres)
- FastAPI `/health` + `/run` wrapper
- Langfuse callback on graph invoke

## Explicit non-goals

- Windows scheduled-task gateway parity
- Production autoscale
- Replacing OpenClaw as Scenario A primary

## Success criteria

1. One end-to-end run with trace URL + PASS on fixture validation
2. Written comparison note: cold-start, ops burden, portability vs OpenClaw-local
3. Input to mint gate: `langgraph_oss_selfhost` SUBSTRATE row (already drafted)

## Schedule

**Scheduled** for Week-2 after mint gate ratify — carryover pointer CO-MBH-W1 spike lane.

## Owner

Envoy Tech Lab / AIC execution; operator ratifies scope only if spike expands beyond 3 days.
