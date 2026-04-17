# Initiative 11 — Madeira day-to-day ops copilot (SOTA-informed, governance-safe)

**Status:** active (implementation started 2026-04-15).  
**Related:** [Initiative 10 — Madeira eval hardening (closed)](../10-madeira-eval-hardening/master-roadmap.md); HLK governance [PRECEDENCE.md](../../../references/hlk/compliance/PRECEDENCE.md).

## Goal

Strengthen **day-to-day operational support** (drafts, checklists, clearer Orchestrator handoffs) **without** granting Madeira write access to canonical HLK assets or production systems. Mutations remain **Orchestrator → Architect → Executor → Verifier** with human approval.

## Asset classification (HLK)

Per [`docs/references/hlk/compliance/PRECEDENCE.md`](../../../references/hlk/compliance/PRECEDENCE.md):

| Class | In scope |
|:------|:-----------|
| **Canonical** | No edits to `baseline_organisation.csv` / `process_list.csv` without operator approval. Madeira never writes these. |
| **Mirrored / derived** | `config/openclaw.json.example`, `config/agent-capabilities.json`, `config/model-tiers.json`, `prompts/overlays/OVERLAY_MADEIRA_OPS.md`, `config/intent-exemplars.json`. |
| **Reference-only** | External SOTA repos (`claw-code`, Claude Code tool docs) — patterns only, no code copy. |

## Decision log

| ID | Decision |
|----|----------|
| D-OPS-1 | **Ops overlay** (`OVERLAY_MADEIRA_OPS.md`) ships on **standard** and **full** prompt variants only (`config/model-tiers.json`); **compact** tier unchanged for small-model `bootstrapMaxChars`. |
| D-OPS-2 | **Permission truth** stays in `config/agent-capabilities.json`; prompts do not add write tools. |
| D-OPS-3 | **`memory_store`** for scratch artifacts **deferred** — see [SECURITY.md](../../../../SECURITY.md) Madeira ops note; revisit only if overlay proves insufficient. |
| D-OPS-4 | Intent routing: **semantic exemplars** (`other`, `hlk_lookup`) expanded for day-to-day phrasing; **regex safety** for `admin_escalate` / `execution_escalate` unchanged (still wins when matched). |

## Governed verification matrix

Full gate set: [`docs/DEVELOPER_CHECKLIST.md`](../../../DEVELOPER_CHECKLIST.md) — inventory verify, drift, `py scripts/test.py all`, targeted pytest, `py scripts/release-gate.py`, `py scripts/validate_hlk.py` when compliance assets change (not expected for this initiative).

## Reports

- UAT evidence: [`reports/uat-madeira-ops-copilot-20260415.md`](reports/uat-madeira-ops-copilot-20260415.md)

## References (inspiration, patterns only)

- Harness / tool catalog discipline: external claw-code-style manifests.
- `akos_route_request` as Task-style delegation: Claude Code `Tools.json` patterns (when-not-to-use, parallel reads).
- Layered prompts: `system_prompts_examples` style — implemented as overlay, not base bloat.
