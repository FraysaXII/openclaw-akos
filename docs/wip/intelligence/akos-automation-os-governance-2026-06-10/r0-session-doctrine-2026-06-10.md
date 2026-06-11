---
authored: 2026-06-10
last_review: 2026-06-11
tranche: akos-automation-os-R0-charter-kickoff
register_id: IO-CAP-AKOS-AUTOMATION-OS-2026-001
status: pending_ratification
operator_ratification:
  q12_option_a: automation_os_first_holistic_agentic_paused_r3
  q13_maximum_budget: 400_corpint_550_osint
  charter_batch: batch_2_2026-06-11
blocks_downstream:
  - holistic-agentic-R4-through-R12-until-D4
---

# AKOS Automation OS governance — R0 session doctrine (2026-06-10, expanded 2026-06-11)

## Purpose

Kickoff doctrine for the **Automation OS governance** research pack — prerequisite research that must
complete through **D4 implementation spec (R12)** before holistic-agentic **R4–R12** resumes.
Status: **pending operator ratification** of charter v1 (expanded).

## Operator ratification received (binding)

| Gate | Decision |
|:---|:---|
| **Q12 Option A** | Automation OS research **FIRST**; holistic-agentic **PAUSED at R3** (305-row ledger uncommitted) until D4 |
| **Q13** | **MAXIMUM** source budget — **400 CORPINT + 550 OSINT = 950 rows** after full POV expansion |

## Deliverables (draft — not committed)

| # | Artifact | Validator / gate |
|:---|:---|:---|
| D1 | `RESEARCH_CHARTER_AND_EXECUTION_PLAN.md` (v1 expanded) | Operator inline-ratify |
| D0 | This session doctrine | Operator-facing closure |
| §A | INTELLIGENCEOPS row draft (charter appendix) | **CSV edit gated** |

## R0 scope (charter v1 expanded)

| Dimension | Compact v0 (superseded) | v1 (current) |
|:---|:---|:---|
| Prongs | 7 | **12** with ICS tiers |
| Source budget | 150 | **950** (400+550) |
| CORP-VAULT categories | 8 | **14** (full O5-1 sweep) |
| OSINT categories | 7 | **14** |
| Tranches | R1–R4 | **R1–R12** dual-source |
| blocks_downstream | R4 | **R4–R12** until D4 |

### Twelve prongs (ICS summary)

| Prong | Area | ICS |
|:---|:---|:---|
| P1-TECH | Tech registry SSOT | **Load-bearing** |
| P2-DATA | DataOps lineage | **Load-bearing** |
| P3-OPS | Ops verify + RevOps | **Load-bearing** |
| P4-RESEARCH | research_ledger.py engine | **Load-bearing** |
| P5-PEOPLE | Paired SOP + synthesis gates | High |
| P6-COMPLIANCE | Canonical CSV gates | **Load-bearing** |
| P7-FINANCE | FinOps runbooks | High |
| P8-LEGAL | Audit trail bar | Medium |
| P9-MARKETING | CRM/MarTech adapters | Medium |
| P10-INTEL-OPS | Radar + IO register | High |
| P11-ENVOY-MADEIRA | OpenClaw + MADEIRA tools | High |
| P12-RPA-ADAPTERS | RPA + normalized adapters | **Load-bearing** |

**Load-bearing (6):** P1, P2, P3, P4, P6, P12. **High (5):** P5, P7, P10, P11. **Medium (2):** P8, P9.

### Twelve-tranche roadmap

| Tranche | CORPINT | OSINT | Focus |
|:---|---:|---:|:---|
| R1 | 55 | 40 | Script census + one-off anti-patterns |
| R2–R4 | 35 each | 44 each | Tech/Envoy; Data/RPA; Ops/RevOps |
| R5–R6 | 32 each | 44 each | People/QF; Research/IntelOps |
| R7–R9 | 30/28/28 | 44 each | Compliance; Finance/Legal; Marketing |
| R10–R11 | 25 each | 46 each | Verify/CI; monorepo/agent CLI |
| R12 | 40 | 66 | Skeptic close + **D4** (unblocks holistic-agentic) |

## Prior research crosswalk (charter §5)

| Pack | Inherit | Avoid |
|:---|:---|:---|
| Agentic-OS taxonomy | AKOS-as-substrate | Re-litigate AOS category |
| Area-completeness | 14-component bar, value ranking | Redefine "area" |
| HCAM | Graph articulation verbs | Neo4j rework in this pack |
| Wave R+4 | Ledger schema, 8-stage loop | MADEIRA thesis depth |
| Model selection | Two-seat routing | Leaderboard re-research |
| Research radar | INTELLIGENCEOPS freshness | Second ingest doctrine |
| Holistic-agentic | Orchestration contracts | R4+ until D4; no double engine |

## Gates honored

- Foreground execution; AskQuestion before commit
- **No git commit** until charter ratified
- **No INTELLIGENCEOPS_REGISTER.csv edit** — appendix §A only

## Operator ratification checklist (≤7 items)

| # | Item | Status |
|---:|:---|:---|
| 1 | Confirm Q12 Option A — Automation OS first; holistic-agentic paused at R3 | pending |
| 2 | Approve **400 CORPINT + 550 OSINT** (950 total) | pending |
| 3 | Approve **12 prongs** + ICS matrix + **12 tranches** | pending |
| 4 | Approve prior research crosswalk (§5 inherit/avoid) | pending |
| 5 | Confirm **R4–R12 blocked** until D4 at R12 | pending |
| 6 | Approve INTELLIGENCEOPS row mint at R1 gate | pending |
| 7 | Authorise **R1** (+55 CORPINT, +40 OSINT) script census | pending |

## Next (post-ratification)

**R1** — Full `scripts/*.py` census, one-off anti-pattern rows (`holistic_agentic_r*`, `i93_*`, `i94_*`),
bootstrap `source-ledger.csv` with 12 prong headers, `tranche-r1-regression.md`.

---

*R0 expanded 2026-06-11 — awaiting operator ratification before R1 execution.*
