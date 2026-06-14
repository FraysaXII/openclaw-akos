---
initiative_id: INIT-OPENCLAW_AKOS-96
authored: 2026-06-11
---

# I96 evidence matrix

## Session commits (2026-06-10–11)

| Commit | Track | Evidence |
|:---|:---|:---|
| `8e4f51da` | Methodology | Prong lattice, HxPESTAL, pillars, `research_ledger_ops.py` |
| `39150275` | SSOT | `akos-ssot-canonical-touch.mdc`, skill, `SSOT_REGISTRY_AUDIT_DISCIPLINE.md` |
| `1d5c2c62` | Compliance | process_list umbrella + PESTEL + HxPESTAL |
| `c3a89463` | SSOT | CAPABILITY promote, QF §6, recursive rhythm |
| `0a5552d3` | Track A | Charter v2 ratified |
| `72cc0bb3` | Track A | R1 script census + ledger engine |
| `79eb4b79` | Track A | R2 Tech/Envoy |
| `7f79cba8` / `b9313160` | Track A | R3 Data/RPA + look-back |
| `ff16b725` / `a7db3d62` | Track A | R4 Ops/RevOps + look-back |
| `d5f0566b` / `8dded715` | Track A | R5 People/QF + look-back |
| `25bed2e5` / `f7d33db7` | Track A | R6 Research/Intel + look-back |
| `7139247a` | Track A | R4 manifest generator |
| `5724b62d` / `c545f466` | Holistic | R3 ledger + doctrine status |
| `e3ca3302` | PM | Session recap mint |
| `0fce2cae` | Track A | R7–R12 harvest + D4 draft (**949** cumulative rows) |

**Ledger status:** 949 / 950 charter budget (1 CORPINT short across R7–R12 aggregate).

## Methodology + SSOT lane inventory

| Surface | Path | Registry / note |
|:---|:---|:---|
| Prong lattice discipline | `docs/references/hlk/v3.0/Research/Methodology/canonicals/RESEARCH_PRONG_LATTICE_DISCIPLINE.md` | PRECEDENCE +6 |
| HxPESTAL pillar | `Research/Methodology/Pillars/HXPESTAL_ANALYSIS.md` | CANONICAL_REGISTRY |
| Porter pillar (promoted) | `Research/Methodology/Pillars/PORTER_COMPETITIVE_ANALYSIS.md` | via `forward-charter-porter-pillar-2026-06-10.md` |
| Prong synthesis SOP | `SOP-RESEARCH_PRONG_SYNTHESIS_001.md` | process_list pairing |
| SSOT audit discipline | `Admin/O5-1/Data/Governance/canonicals/SSOT_REGISTRY_AUDIT_DISCIPLINE.md` | recursive rhythm § |
| SSOT touch rule | `.cursor/rules/akos-ssot-canonical-touch.mdc` | paired skill |
| TRP-061..063 | `CANONICAL_RELATIONSHIP_REGISTRY.csv` | HCAM wiring |
| MADEIRA cross-link | `MADEIRA_METHODOLOGY_MODE.md` ↔ HxPESTAL | Envoy plane |
| Templates | `prong-synthesis-template.md`, `hxpestel-intent-tracking-template.md` | WIP pack |
| Ledger engine | `scripts/research_ledger.py`, `akos/research_ledger_ops.py` | D6 preview |

## Per-tranche WIP artifacts (Automation OS)

| Tranche | Doctrine | Regression | Manifest |
|:---|:---|:---|:---|
| R0 | `r0-session-doctrine-2026-06-10.md` | — | — |
| R1 | `r1-session-doctrine-2026-06-10.md` | `tranche-r1-regression.md` | `tranches/r1-manifest.json` |
| R2 | `r2-session-doctrine-2026-06-10.md` | `tranche-r2-regression.md` | `tranches/r2-manifest.json` |
| R3 | `r3-session-doctrine-2026-06-10.md` | `tranche-r3-regression.md` | `tranches/r3-manifest.json` |
| R4 | `r4-session-doctrine-2026-06-10.md` | `tranche-r4-regression.md` | `tranches/r4-manifest.json` |
| R5 | `r5-session-doctrine-2026-06-10.md` | `tranche-r5-regression.md` | `tranches/r5-manifest.json` |
| R6 | `r6-session-doctrine-2026-06-10.md` | `tranche-r6-regression.md` | `tranches/r6-manifest.json` |
| R7 | `r7-session-doctrine-2026-06-11.md` | `tranche-r7-regression.md` | `tranches/r7-manifest.json` |
| R8 | `r8-session-doctrine-2026-06-11.md` | `tranche-r8-regression.md` | `tranches/r8-manifest.json` |
| R9 | `r9-session-doctrine-2026-06-11.md` | `tranche-r9-regression.md` | `tranches/r9-manifest.json` |
| R10 | `r10-session-doctrine-2026-06-11.md` | `tranche-r10-regression.md` | `tranches/r10-manifest.json` |
| R11 | `r11-session-doctrine-2026-06-11.md` | `tranche-r11-regression.md` | `tranches/r11-manifest.json` |
| R12 | `r12-session-doctrine-2026-06-11.md` | `tranche-r12-regression.md` | `tranches/r12-manifest.json` |

## Holistic-agentic lane (Track A sibling)

| Tranche | Status | Blocker |
|:---|:---|:---|
| R1–R3 | Done | — |
| R4–R12 | **BLOCKED** | D4 synthesis ratification (`implementation-spec-2026-06-11.md`) |

Pack: `docs/wip/intelligence/holistic-agentic-capability-orchestration-2026-06-10/` — `parent_initiative: INIT-OPENCLAW_AKOS-96`.

## Cross-plane specs (I96 mint)

| Phase | Artifact |
|:---|:---|
| P1 | `three-plane-architecture.md`, `three-plane-field-mapping.md` |
| P2 | `reports/data-consumer-inventory-2026-06-11.md` |
| P3 | `staleness-loop-spec.md`, `src-tagging-contract.md` |
| P5 | `ledger-to-vault-ingest-contract.md` |
| P6 | `reports/research-center-page-spec-2026-06-11.md` |
| P0E | `reports/exploration-matrix-2026-06-11.md` |
| D5 prep | `reports/tech-automation-registry-crosswalk-2026-06-11.md` |
| D4 draft | `docs/wip/intelligence/akos-automation-os-governance-2026-06-10/implementation-spec-2026-06-11.md` |
| P0 UAT | `reports/uat-i96-p0-program-mint-2026-06-11.md` |
| P7 browser UAT | `reports/uat-i96-research-center-browser-2026-06-11.md` — **PWF** (`d6bcab24`); follow-ups: magic-link, axe py3.12, KiRBe env, page-spec |

## Verification by track

| Track | Gate command |
|:---|:---|
| A | `py scripts/validate_research_action.py --source-ledger …/source-ledger.csv` |
| B | `validate_hlk.py` if canonical touched |
| C | KiRBe health via ERP `/api/kirbe/health` |
| D | `py scripts/browser-smoke.py --playwright` on `/research-center` |
