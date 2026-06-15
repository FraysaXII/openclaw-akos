---
intellectual_kind: research_synthesis_prong
prong_id: P-H
prong_topic: v3.2 methodology lane closed alpha readiness
authored: 2026-06-14
parent_pack: madeira-brand-capability-harmonization-v32-alpha-2026-06-14
control_confidence: Euclid
---

# Prong P-H — v3.2 closed alpha readiness

## Load-bearing finding

**v3.2** per release taxonomy SOP is a **methodology lane** (`LOGIC_CHANGE_LOG.md` row), not a vault folder rename or git tag. Closed alpha can ship under **v3.0 vault + v3.2 logic version** when exit gates pass — matching your intent to open MADEIRA interaction on a sibling HLK instance without waiting for full vault migration.

Alpha is **NO-GO by default** (MADEIRA hardening Part H) until conversational + operator + surface lights green.

## Preconditions (ordered)

| # | Gate | Owner | Status (2026-06-14) |
|:---:|:---|:---|:---|
| 0 | CO-90-004 gateway live PASS | I90 | **Scheduled** — repair landed; host pending |
| 1 | Capability inventory ratified | I76 + this pack | **This research** |
| 2 | Context/cache/postprocess spec | I76/I84 tranche | **Gap (Keter)** |
| 3 | Scenario A experiential dossier | I49 | Partial — eval exists |
| 4 | Scenario B Research Center UAT | I96 | FAIL-until-evidence |
| 5 | Scenario C deploy smoke | I74 | Charter exists |
| 6 | v3.2 LOGIC_CHANGE_LOG row | Operator ratify | Not minted |
| 7 | Alpha cohort + exit criteria doc | I76 | Not minted |

## Proposed alpha phases (research recommendation)

| Phase | Cohort | Scenarios | Duration |
|:---|:---|:---|:---|
| **α0** | Internal operator + AIC | A only | 2 weeks |
| **α1** | 5–10 design partners | A + B | 4–6 weeks |
| **α2** | 30–50 B2B skeptics | A + B + C | 6–8 weeks |
| **α3** | Multi-org pilot | + D | Post-α2 ratify |

External benchmarks (SRC-MBH-EXT-013..015): 50–100 closed beta, week-4 retention ~40%, 10–15% WTP signal for B2B.

## Exit criteria (draft — ratify)

- Three-lights green on dossier `--filter madeira`
- Gateway repair PASS + browser-smoke gateway on CI
- Research Center experiential manifest for 375/768/1280
- Langfuse cost attribution per scenario tag
- Zero Keter gaps open without carryover row + review date

## Ranked insights

1. **Do not conflate v3.2 logic version with vault restructure** — RANK 1
2. **α0 internal is valid first ship; partners wait for B evidence** — RANK 1
3. **I76 is natural charter home; I96/I74 are scenario sub-spines** — RANK 2
