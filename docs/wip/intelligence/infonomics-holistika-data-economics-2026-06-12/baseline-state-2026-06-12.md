---
intellectual_kind: research_baseline
parent_initiative: INIT-OPENCLAW_AKOS-97
authored: 2026-06-12
status: active
language: en
sweep_id: infonomics-corpint-2026-06-12
---

# Baseline state — Infonomics internal CORPINT sweep (2026-06-12)

> P2 measured starting point before external OSINT (P3) and prong synthesis (P4). Evidence only; no vault edits.

## Step 1 — Ledger bar (D-IH-97-B)

| Metric | Target | Actual |
|:---|:---|:---|
| Internal CORPINT rows | ≥300 | **300** |
| Validator | PASS | **PASS** |
| Unique `source_id` | 300 | **300** |
| Topic clusters represented | 15 (charter) | **11** (P3 will widen) |
| Baseline prongs (`BL-*`) | 14 | **14** (min 4 / prong; BL-UX thinnest) |

Command:

```powershell
py scripts/validate_research_action.py --source-ledger docs/wip/intelligence/infonomics-holistika-data-economics-2026-06-12/source-ledger.csv
```

## Step 2 — Prong distribution (rank pass for P4)

| Prong | Rows | Read |
|:---|:---:|:---|
| BL-COMPLY | 63 | Compliance CSV gates + PRECEDENCE + initiative/decision registers dominate vault mass |
| BL-MKT | 41 | Brand/km-moat surfaces; economic narrative assets |
| BL-DATA | 32 | DAMA contracts + semantic layer + I93 closure artifacts |
| BL-OPS | 27 | RevOps spine + engagement economics |
| BL-INTEL | 19 | Radar + intelligence collection economics |
| BL-ENVOY | 18 | MADEIRA / agentic context + substrate |
| BL-RESEARCH | 16 | Methodology + research-action discipline cluster |
| BL-ADAPTER / BL-FIN / BL-LEGAL / BL-PEOPLE / BL-TECH | 15 each | Even minimum pass |
| BL-ETHICS | 5 | Ethics boundary canonicals (thin vault tree) |
| BL-UX | 4 | UX/journey packs + brand UX charter (P2 follow-up: deepen before P4 synth) |

## Step 3 — Corpus shape

| Pool | Rows | Notes |
|:---|:---:|:---|
| Vault (`docs/references/hlk/…`) | ~284 | Primary CORPINT mass |
| WIP planning + intelligence | ~16 | I96 three-plane, I97 pack, overlap tracker, prior packs |
| Code / guides (`akos/`, `scripts/`, GitHub URLs) | remainder | Executable SSOT + mirror/runbook economics |

**Zero literal “Infonomics”** in vault remains true; P2 rows compose **adjacent** economic doctrine (FINOPS, RevOps, contracts, share, research trust, agentic substrate).

## Step 4 — Overlap / dedupe posture

- Sibling packs (`area-completeness`, `automation-os`, `GOV-ANA`, `GOJ-UX`) cited by URL where load-bearing; notes mark `holistika-corpint` cluster.
- **I96 ↔ I97:** overlap tracker row CO-97-004 remains `overlap_pending` until P5 — Research Center economics not duplicated here as doctrine.

## Step 5 — Full-picture regression (light)

| Gate | Result |
|:---|:---|
| `validate_research_action.py` on I97 ledger | PASS (300 rows) |
| `validate_carryover_posture.py --index --strict` | PASS (unchanged) |
| Single spine (D-IH-98-STEERING) | I97 active; no parallel governance thread opened |

## P2 → P3 handoff

P2 **count bar met** (300 internal). P3 adds ≥500 OSINT toward 800 total. Before P4 synthesis: optional **UX/ETHICS prong top-up** from manual batch if operator wants ≥15 rows/prong everywhere.
