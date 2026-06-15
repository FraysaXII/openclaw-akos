---
intellectual_kind: mint_gate_packet
authored: 2026-06-15
status: operator_ratified_2026-06-15
ratified_by: operator
ratified_at: 2026-06-15
execution_tranche: T1b
prerequisite: week-1-substrate-reliability-refresh-charter.md + prong-synthesis-P-I
gate_type: canonical_csv_mint
---

# Mint gate packet — substrate adapter registry (tranche T1b)

## Mint tranche T1b — executed 2026-06-15

Operator ratified. Canonical rows landed:

| Registry | Rows |
|:---|:---|
| SUBSTRATE_REGISTRY | +3 (`SUBS-HOLISTIKA-OPENCLAW-WINDOWS`, `SUBS-LANGGRAPH-OSS-SELFHOST`, `SUBS-HOLISTIKA-LLAMAINDEX-WORKER`) |
| DATA_CONTRACT_REGISTRY | +1 (`DC-HOL-SUBSTRATE-ADAPTER-001`) |
| PROOF_ADAPTER_REGISTRY | +2 (`PAD-006`, `PAD-007`) |
| EVIDENCE_CLASS_REGISTRY | +2 (`ECB-0012`, `ECB-0013`) |
| DECISION_REGISTER | +1 (`D-IH-76-MINT`) |
| FOUNDER_METHODOLOGY_VERSIONING | v3.2 lineage row |

`py scripts/validate_hlk.py` — **PASS**

## Proposed rows (summary)

### SUBSTRATE_REGISTRY (additions / amendments)

| substrate_id | substrate_name | bearer | notes |
|:---|:---|:---|:---|
| `openclaw_local_windows` | OpenClaw gateway (Windows scheduled task) | Envoy Tech Lab | Primary Scenario A; upstream reliability class per P-I |
| `langgraph_oss_selfhost` | LangGraph OSS + Postgres checkpointer | Envoy Tech Lab | Evaluation spike candidate; not α0 primary |
| `llamaindex_worker` | LlamaIndex retrieval worker | Research / KiRBe | Already in PoC lineage; formalize row |

Make / n8n: remain **scheduled** pending inventory tranche (substrate audit § gaps).

### DATA_CONTRACT (draft → mint)

| contract_id | Consumer | Producer | Proof class |
|:---|:---|:---|:---|
| `DC-HOL-SUBSTRATE-ADAPTER-001` | AKOS runtime, I90 routing | OpenClaw CLI + user config | automated + trace |

Fields: normalize path, repair runbook, check-only post-reboot, grace windows, OPS escalation slug `gateway-cold-start`.

### PROOF_ADAPTER (new)

| proof_adapter_id | Evidence | Binds to |
|:---|:---|:---|
| `proof-openclaw-gateway-repair-json` | `artifacts/gateway-repair-post-reboot-2026-06-15.json` success | CO-90-004 closure |
| `proof-openclaw-check-only-post-reboot` | `--check-only --json` PASS within 180s wait | Post-reboot health contract |

### CAPABILITY_REGISTRY (seed backfill — subset)

From `capability-functionality-inventory-matrix.md` — only rows where `capability_tier` = adapter/runtime health (CAP-M01, CAP-M05, CAP-M12 per matrix); full 30-row tranche remains **D-MBH-05** separate gate.

## Verification matrix (post-mint)

```powershell
py scripts/validate_hlk.py
py scripts/validate_research_action.py --source-ledger docs/wip/intelligence/madeira-brand-capability-harmonization-v32-alpha-2026-06-14/source-ledger.csv
py scripts/openclaw_gateway_repair.py --check-only --json
```

## Parallel execution (not blocked on mint)

- I96 browser manifest (Scenario B)
- Context economics WIP → spec
- I100 lab component probes
- I87/I90 OpenClaw hardening tranche (runtime improvements)
