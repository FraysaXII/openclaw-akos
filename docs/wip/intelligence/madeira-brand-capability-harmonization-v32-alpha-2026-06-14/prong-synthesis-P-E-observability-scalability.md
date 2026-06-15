---
intellectual_kind: research_synthesis_prong
prong_id: P-E
prong_topic: Operational observability and scalability
authored: 2026-06-14
parent_pack: madeira-brand-capability-harmonization-v32-alpha-2026-06-14
control_confidence: Euclid
---

# Prong P-E — Observability and scalability

## Load-bearing finding

Holistika chose **Langfuse v4 + OTEL convergence** early (I10 D-EVAL) — aligned with 2026 industry direction (SRC-MBH-EXT-018..021). Scalability for MADEIRA alpha is **not** "infinite agents" first; it is **deterministic health semantics** (gateway RPC, deploy smoke, dossier three-lights) at increasing cohort size.

CO-90-004 (gateway repair tranche) proves local control-plane fragility is an **observability contract bug**: `Runtime: unknown` when RPC fails despite listener — fixed in code but **live PASS pending** on operator host.

## Observability stack (as-built)

| Signal | Source | Alpha gate |
|:---|:---|:---|
| Traces/spans | Langfuse via `akos.telemetry` | Required for scenario A/C |
| Eval rubrics | `tests/evals/suites/` | Tier-B weekly dossier |
| Runtime health | `scripts/doctor.py`, gateway repair | Scenario A blocker until green |
| Deploy | deploy-health craft + Vercel MCP | Scenario B/C consumer repos |
| Regression | release-gate + inter-wave sweep | Pre-cohort expand |

## Scalability dimensions

1. **Horizontal** — Hosted SDK (I74) + state externalization (P-A); not local gateway duplication.
2. **Context** — KiRBe index scale (I96); cache policy (P-B).
3. **Organizational** — Alpha cohort rings (50–100); not public launch.
4. **Governance** — Validator matrix must stay green as artifacts grow (index integrity).

## Gaps

| Gap | Notes |
|:---|:---|
| Cache/token metrics absent from telemetry | Finops blind (P-D) |
| No SLO doc for MADEIRA alpha | Propose p95 latency + error budget |
| SigNoz/OTEL dual-backend not decided | Langfuse primary; SigNoz optional for infra |
| Zombie gateway class not in incident SOP | Partially in OPENCLAW_RUNTIME_HEALTH_TRIAGE §4.6 |

## Ranked insights

1. **OTEL-native observability = anti-lock-in for ops** — RANK 1
2. **Gateway health is alpha-critical path for Cursor-local** — RANK 1
3. **Dossier three-lights scales eval discipline to cohort size** — RANK 2
