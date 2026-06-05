---
research_kind: phase_research_packet
phase: F2a
program: FINANCE-AREA-FULL
authored: 2026-06-05
control_confidence_level: Safe
---

# F2a research — rev-rec, pricing registry, DC seeds

## Internal evidence sweep

| Anchor | Finding |
|:---|:---|
| OPS-81-5 / OPS-81-6 | CRITICAL/HIGH open; `FINOPS_REVENUE_RECOGNITION_POLICY.md` + `PRICING_TIER_REGISTRY.csv` not minted |
| `thi_finan_dtp_126`, `thi_finan_dtp_203` | Pricing processes exist; `Finance/Business Controller/Pricing/` empty |
| PMO `PRICING_MODEL.md` | Commercial narrative; must join registry at F2a (not duplicate) |
| I93 `DATA_CONTRACT_REGISTRY.csv` | 4 seed rows; ODCS column shape is template for DC-FINOPS-* |
| Finance matrix F1 | 77%; AREA-08 gap = no area-local dimension CSVs |
| `CAPABILITY_REGISTRY` | 16 Finance CAP rows; CONFIDENCE=0 (AREA-06 partial) |

## External grounding (novel framing → cite)

| ID | Source | Use in F2a |
|:---|:---|:---|
| EXT-04 | KPMG ASC 606 handbook 2025 | Rev-rec policy structure |
| EXT-03 | Business Software FP&A semantic layer | Metric catalog join to `METRICS_REGISTRY` seeds |
| EXT-09 | Fullcast RevOps–Finance alignment | DC-REVOPS-FINOPS-ENGAGEMENT-001 consumer story |

## F2a mint list (ordered)

1. `FINOPS_REVENUE_RECOGNITION_POLICY.md` (charter → active at F2a close)
2. `PRICING_TIER_REGISTRY.csv` + Pydantic + `validate_pricing_tier_registry.py`
3. `DATA_CONTRACT_REGISTRY` — 5 DC-FINOPS-* rows (from master synthesis §cross-area table)
4. `CAPABILITY_CONFIDENCE_REGISTRY` — 16 CONF seed rows for Finance CAP-* IDs
5. `runbook_path` on `thi_finan_dtp_303` (pilot paired SOP+runbook; full 16 at F2b hygiene)

## Out of scope (F2b)

- `FINOPS_TAX_CALENDAR.csv` (OPS-81-13)
- `FINOPS_TAX_STRATEGY_DOCTRINE.md` (OPS-81-20 bundle)
