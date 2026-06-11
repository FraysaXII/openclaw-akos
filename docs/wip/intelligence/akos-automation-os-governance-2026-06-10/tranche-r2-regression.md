---
report_type: tranche-regression
tranche: R2
parent_initiative: IO-CAP-AKOS-AUTOMATION-OS-2026-001
authored: 2026-06-11
status: pass
---

# Tranche R2 regression — Tech + Envoy vault harvest

## Tranche summary

| Metric | Target | Actual | Verdict |
|:---|---:|---:|:---|
| CORPINT (R2 slice) | 35 | 34 (`SRC-AOS-R2I-*`; 1 URL dedup vs R1 TECHOPS) | PASS |
| OSINT (R2 slice) | 44 | 44 (`SRC-AOS-R2E-*`) | PASS |
| Cumulative ledger | 174 | 173 | PASS |
| `validate_research_action.py` | PASS | PASS | PASS |

## §7.1 seven-point regression

| # | Standard | Result | Evidence |
|---:|:---|:---|:---|
| 1 | Coverage | PASS | CORP-VAULT-TECH + CORP-VAULT-ENVOY + OSINT-CICD-OS/MONOREPO/AGENT-CLI |
| 2 | Dual-source | PASS | 34 CORPINT + 44 OSINT |
| 3 | Voice diversity | PASS | SRE, platform eng, monorepo maintainers, agent-framework vendors, skeptic |
| 4 | Prong binding | PASS | P1-TECH + P11-ENVOY-MADEIRA; ICS in `notes` |
| 5 | KiRBe schema | PASS | Validator PASS on 173-row cumulative ledger |
| 6 | Skeptic balance | PASS | 6/44 OSINT (14%) with `CON:` in `notes` |
| 7 | Downstream hook | PASS | Feeds D5 TECH_AUTOMATION_REGISTRY column spec; R3 Data/RPA harvest |

## Vault CORPINT anchors (sample)

| Vault asset | Functional role |
|:---|:---|
| `SOP-CICD_BASELINE_001.md` | Fleet CI/CD baseline for automation registry |
| `SOP-MCP_SERVER_DEFINITION.md` | MCP tool-plane governance |
| `SOP-OPENCLAW_RUNTIME_HEALTH_TRIAGE_001.md` | OpenClaw runtime ops |
| `MADEIRA_METHODOLOGY_MODE.md` | HxPESTAL intent representation vehicle |
| `AGENTIC_FRAMEWORK_LANDSCAPE.md` | Substrate/tool inventory for Envoy |

## Disposition

**PASS** — ready for phase commit.
