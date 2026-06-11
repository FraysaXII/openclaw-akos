---
report_type: tranche-regression
tranche: R11
parent_initiative: IO-CAP-AKOS-AUTOMATION-OS-2026-001
authored: 2026-06-11
status: pass
---

# Tranche R11 regression — Monorepo + agent CLI + adapter interop

## Tranche summary

| Metric | Target | Actual | Verdict |
|:---|---:|---:|:---|
| CORPINT (R11 slice) | 25 | 25 (`SRC-AOS-R11I-*`) | PASS |
| OSINT (R11 slice) | 46 | 46 (`SRC-AOS-R11E-*`) | PASS |
| Cumulative ledger | 843 | 843 | PASS |
| `validate_research_action.py` | PASS | PASS | PASS |

## §7.1 seven-point regression

| # | Standard | Result | Evidence |
|---:|:---|:---|:---|
| 1 | Coverage | PASS | CORP-VAULT-ENVOY (MADEIRA tool catalog, MCP topology, runtime health triage) + CORP-VAULT-ADAPTERS + OSINT-AGENT-CLI/MONOREPO |
| 2 | Dual-source | PASS | 25 CORPINT + 46 OSINT |
| 3 | Voice diversity | PASS | MCP spec / Anthropic tool-use (4.1), agent CLI vendors (3.1), skeptic tool-sprawl (2.1) |
| 4 | Prong binding | PASS | P3-ENVOY + P11-AGENT-CLI; ICS in `notes` |
| 5 | KiRBe schema | PASS | Validator PASS on 843-row cumulative ledger |
| 6 | Skeptic balance | PASS | 12/46 OSINT (26%) with `CON:` in `notes` |
| 7 | Downstream hook | PASS | Feeds D4 implementation spec (MCP + adapter crosswalk) + R12 skeptic close |

## Dedup disposition

Manifest overflow candidates used where prior-tranche URL collisions would have left charter deficits; net-new URLs only in ledger append.

## Vault CORPINT anchors (sample)

| Vault asset | Functional role |
|:---|:---|
| `MADEIRA_TOOL_CATALOG.md` | Governed tool inventory |
| `config/mcporter.json.example` | MCP server topology SSOT |
| `bless_external_repo.py` | Sibling-repo deploy smoke |
| `SOP-OPENCLAW_RUNTIME_HEALTH_TRIAGE_001.md` | Runtime health triage |

## Disposition

**PASS** — ready for phase commit.
