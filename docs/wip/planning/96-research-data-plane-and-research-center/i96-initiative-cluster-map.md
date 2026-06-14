---
parent_initiative: INIT-OPENCLAW_AKOS-96
authored: 2026-06-11
---

# I96 initiative cluster map

## Diagram

```mermaid
flowchart TB
  I86[I86 Cluster Coordinator]
  I96[I96 Research Data Plane]
  I75[I75 Research Area Gov]
  I83[I83 KiRBe Ingestor]
  I92[I92 ERP Reassess]
  I95[I95 HCAM]
  I88[I88 Cross-Area Ops]
  AUTO[Automation OS WIP]
  HOL[Holistic-agentic WIP]

  I86 --> I96
  I96 --> I75
  I96 --> I83
  I96 --> I92
  I96 --> I95
  I96 --> I88
  I96 --> AUTO
  I96 --> HOL
  AUTO -->|R12 D4| HOL
```

## Table

| ID | I96 consumes | I96 produces |
|:---|:---|:---|
| **I86** | Cluster burndown cadence | Program-line tracking row |
| **I75** | Research area SOP buildout | Radar queue panel semantics |
| **I83** | KiRBe ingest implementation | `ledger-to-vault-ingest-contract.md` |
| **I92** | ERP shell + MC lineage | Research Center v1 route |
| **I95** | HCAM verbs, area SSOT sweep hook | Field mapping for graph edges |
| **I99** | Supabase Auth EG-5, SMTP, inbox tiers | Auth redirect + email tranche (P2); I96 consumer |
| **I88** | Research OPS 10-pillar lens | Data-consumer inventory (OPS-86-29) |
| **AUTO** | R7–R12 charter | 950-row ledger + D4 |
| **HOL** | D4 unblock | R4–R12 resume tracking |

## Research WIP lanes (linked, not duplicated)

- [`akos-automation-os-governance-2026-06-10/`](../../intelligence/akos-automation-os-governance-2026-06-10/)
- [`holistic-agentic-capability-orchestration-2026-06-10/`](../../intelligence/holistic-agentic-capability-orchestration-2026-06-10/)

Steering file: [`session-recap-2026-06-10.md`](../../intelligence/akos-automation-os-governance-2026-06-10/session-recap-2026-06-10.md) (`parent_initiative: INIT-OPENCLAW_AKOS-96`).
