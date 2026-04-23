# UAT — Madeira UC-ID matrix (Tier 3)

**Date:** 2026-04-21  
**Runner:** _pending operator_  
**Environment:** _gateway URL / model / AKOS API port_  

Evidence for [`docs/uat/madeira_use_case_matrix.md`](../../../../uat/madeira_use_case_matrix.md). **No secrets or full prompts with PII** in this file.

| UC-ID | Step ref | Result | Note |
|:------|:---------|:-------|:-----|
| M-HLK-04 | Fuzzy / acronym | N/A | Awaiting WebChat run |
| M-HLK-05 | Multi-fact | N/A | |
| M-HLK-06 | Graph | SKIP | Optional when Neo4j/graph disabled |
| M-FIN-01 | Quote | N/A | |
| M-FIN-02 | Sentiment | N/A | |
| M-RT-02 | Execution escalate | N/A | |
| M-RT-03 | Mixed intent | N/A | |
| M-PLAN-01 | Plan draft | N/A | Use `/madeira/control` + WebChat |
| M-OPS-01 | Ops copy | N/A | |
| M-NEG-01 | Injection | N/A | Clean session required |
| M-NEG-02 | Hallucination | N/A | |

**Automated parity (Tier 2) at authoring time:** Scenario 0 HTTP slice extended in `scripts/browser-smoke.py` (finance, mixed routing, Madeira mode, control page).
