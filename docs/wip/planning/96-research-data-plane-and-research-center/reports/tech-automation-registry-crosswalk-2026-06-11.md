---
initiative_id: INIT-OPENCLAW_AKOS-96
report_kind: crosswalk
authored: 2026-06-11
status: review
parent_initiative: INIT-OPENCLAW_AKOS-96
handoff_to: INIT-OPENCLAW_AKOS-95
---

# Tech automation registry crosswalk — D5 prep (no CSV mint)

Maps Automation OS ledger prongs (BL-*) to existing Tech Lab adapter/process surfaces. **Read-only crosswalk** — no `process_list.csv` or adapter-registry mint in P0.

## Scope

| In scope | Out of scope |
|:---|:---|
| Inventory of ledger prongs vs `OPERATIONS_PROCESS_CATALOG.yaml` adapters | Net-new process_list rows |
| Gap flags for D5 adapter-registry tranche | CSV edits to `INITIATIVE_REGISTRY.csv` |
| Handoff notes for I95 HCAM verb alignment | Neo4j edge mint |

## Prong → adapter mapping (sample)

| Ledger prong | Functional area | Existing adapter / script | Coverage |
|:---|:---|:---|:---:|
| BL-TECH | Tech Lab runtime | `scripts/openclaw_health_escalate.py` | partial |
| BL-ENVOY | Envoy plane | `scripts/hlk_mcp_server.py` | partial |
| BL-DATA | Data integration | `akos/research_ledger_ops.py` | wired |
| BL-RPA | RPA lane | `scripts/browser-smoke.py` | reference |
| BL-OPS | Operations PMO | `scripts/pmo_program_anchor_backfill.py` | wired |
| BL-REVOPS | RevOps | `scripts/render_operator_inbox.py` | partial |
| BL-PEOPLE | People compliance | `scripts/validate_hlk.py` | wired |
| BL-QF | Quality Fabric | `scripts/validate_synthesis_before_tranche.py` | wired |
| BL-RESEARCH | Research methodology | `scripts/research_ledger.py` | wired |
| BL-INTEL | IntelligenceOps | `scripts/research_radar_sweep.py` | wired |
| BL-COMPLIANCE | Compliance gates | `scripts/validate_hlk.py` + hooks | wired |
| BL-FINANCE | Finance ops | `scripts/finance_mcp_server.py` | partial |
| BL-LEGAL | Legal surfaces | — | gap |
| BL-MKT | Marketing | `scripts/validate_brand_baseline_reality_drift.py` | partial |
| BL-CRM | CRM lane | — | gap |

## D5 tranche prep checklist

1. Operator ratify gap rows (LEGAL, CRM) before adapter-registry mint.
2. Pair each net-new adapter with SOP+runbook per executable-process-catalog discipline.
3. Wire `status` enum (`active` / `planned` / `deprecated`) on adapter rows.
4. Re-run `validate_research_action.py` after D4 synthesis closes Track A.

## Verification

```text
py scripts/validate_hlk.py
  OVERALL: PASS (no CSV mint — crosswalk doc only)
```
