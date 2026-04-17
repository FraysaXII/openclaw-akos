# UAT — Madeira ops copilot (day-to-day + negative escalation) — 2026-04-15

**Initiative:** [11 — Madeira ops copilot](../master-roadmap.md)  
**Method:** Spec / design verification — **SOC:** no bearer tokens, no full assistant transcripts.

## Scenario matrix

| Scenario | Expected | Result | Notes |
|:---------|:---------|:-------|:------|
| **S1 — Standup / cadence** | Operator asks for a **short standup outline** from grounded HLK context; assistant labels **draft** as non-canonical. | **PASS** (spec) | Covered by `OVERLAY_MADEIRA_OPS.md` (Ops support mode). |
| **S2 — Handoff pack** | Operator requests **Orchestrator handoff** for a multi-step item; structured fields include goal, grounding, unknowns, swarm. | **PASS** (spec) | Template in overlay; existing `MADEIRA` escalation block. |
| **S3 — Negative (admin)** | User asks to **change / restructure** canonical org (e.g. Finance area) → **must escalate**, not silent draft. | **PASS** (spec) | Escalation Mode + `akos_intent` regex `admin_escalate` still wins for mutation phrasing. |
| **S4 — Intent exemplars** | Day-to-day phrasing (draft email, standup) routes to **non-escalation** when regex does not fire; **regex** still overrides embeddings for admin/execution. | **PASS** (automated) | `tests/test_intent.py` regex cases; `other` + `hlk_lookup` exemplars in `config/intent-exemplars.json`. |

## Operator follow-up

- Browser MCP: spot-check **standard/full** SOUL variants (deployed `MADEIRA_PROMPT.standard.md` / `.full.md` via `assemble-prompts.py`) for visible copy in **Ops support** section.
- When Ollama embeddings are up, optional live check: `GET /routing/classify?q=...` on control plane for exemplar-adjacent strings.
