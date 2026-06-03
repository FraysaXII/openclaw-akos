---
intellectual_kind: decision_brief
ops_id: OPS-86-9
initiative_id: INIT-OPENCLAW_AKOS-86
parent_initiative: INIT-OPENCLAW_AKOS-90
authored: 2026-06-01
status: pending_operator
linked_decisions:
  - D-IH-86-BU
  - D-IH-90-U
linked_packet: ../composer-packets/packet-ops-86-9-qf-runbooks.md
language: en
---

# Decision brief — OPS-86-9 (Quality Fabric specialty runbooks)

## Question

In what **order** do the four charter specialties (`DATAOPS`, `MKTOPS`, `TECHOPS`, `UX`) get paired runbooks, given chicken-and-egg dependencies?

## Decomposition (ratified at I90 P0 as D-IH-90-U)

| Specialty | Runbook | Execution phase | Blocker |
|:---|:---|:---|:---|
| **DataOps** | `scripts/dataops_quality_check.py` | **P3c** (OPS-86-19) | Doctrine `charter` until flip |
| **TechOps** | `scripts/techops_reliability_check.py` | **P3b** (no gate) | None — execute first |
| **MKTOPS** | `scripts/mktops_campaign_quality_check.py` | **Park** → OPS-86-25 | Parent specialty not chartered |
| **UX** | `SOP-PEOPLE_UX_RESEARCH_001` | Forward-charter | ≥3 channel doctrines active |

## Options

| Option | Summary |
|:---|:---|
| **A — TechOps-first** (recommended) | P3b ships TechOps runbook + tests + `pre_commit` self-test; DataOps/MKTOPS/UX remain framed. |
| **B — Big-bang quartet** | Mint all four runbooks in one commit — violates specialty mint contract when MKTOPS parent missing. |
| **C — DataOps before TechOps** | Flip DATAOPS first — increases P3c blast radius before reliability runbook exists. |

## Recommendation

**Option A** — aligns with [`dataops-activation-tracker.md`](../../_trackers/dataops-activation-tracker.md) and parks MKTOPS under **OPS-86-25**.

## OPS-86-9 closure criterion

Row closes when: (1) TechOps runbook PASS in CI; (2) DataOps forward-charter satisfied by OPS-86-19 plan; (3) MKTOPS + UX explicitly parked with tracker paths cited in OPS notes.
