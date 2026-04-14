# Phase plan — Madeira write / browser profile (Executor + HITL)

**Initiative:** `02-hlk-on-akos-madeira`  
**Status:** Planned — **additive** to closed read-only hardening ([MADEIRA_HARDENING_CONSOLIDATED_PLAN.md](MADEIRA_HARDENING_CONSOLIDATED_PLAN.md))  
**Date:** 2026-04-15  

---

## Asset classification (per [PRECEDENCE.md](../../../references/hlk/compliance/PRECEDENCE.md))

| Class | Paths |
|:------|:------|
| **Canonical SSOT** | `config/openclaw.json.example`, `config/agent-capabilities.json`, `prompts/`, `akos/` routing and policy |
| **Canonical HLK** | `docs/references/hlk/compliance/*` only if org facts policy changes (rare); prefer `hlk_*` tools |

---

## Decision log

| ID | Question | Decision |
|:---|:-----------|:---------|
| D-MWB-1 | Gateway widening | Any write/browser/MCP expansion stays **behind Executor + explicit HITL**; Madeira remains router-first unless superseded by a future D1 revision with tests |
| D-MWB-2 | Inventory | Preserve **full** provider/model/agent contract from `config/openclaw.json.example` per governance remediation |

---

## Verification matrix

Full [DEVELOPER_CHECKLIST.md](../../../docs/DEVELOPER_CHECKLIST.md) on every merge that touches runtime config, prompts, or `akos/` — including `verify_openclaw_inventory.py`, `check-drift.py`, `test.py all`, `pytest tests/test_api.py`, `release-gate.py`, `validate_hlk.py` when HLK assets change.

---

## Phased actions (outline)

1. Threat model + operator UX for HITL gates — **delivered:** [reports/madeira-write-browser-threat-model.md](reports/madeira-write-browser-threat-model.md).
2. Incremental `alsoAllow` / deny deltas in `openclaw.json.example` mirrored in capabilities + tests.
3. `/agents/{id}/policy` and capability-drift tests must stay green.
4. Lane A + Lane B UAT after each increment.

**Registry:** [REG.004](../06-planning-backlog-registry/master-roadmap.md).
