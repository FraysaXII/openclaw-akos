---
language: en
status: active
canonical: true
role_owner: COO
classification: way_of_working
intellectual_kind: charter
ssot: true
authored: 2026-06-10
last_review: 2026-06-10
last_review_at: 2026-06-10
last_review_by: COO
methodology_version_at_review: v3.1
inherited_pattern_id: pattern_area_buildout
ratifying_decisions:
  - D-IH-94-A
linked_canonicals:
  - OPERATIONS_DELIVERY_DISCIPLINE.md
  - PMO/canonicals/OPERATIONAL_COHESION_DOCTRINE.md
  - RevOps/canonicals/REVOPS_AREA_CHARTER.md
  - SMO/canonicals/SOP-SERVICE_MGMT_001.md
  - ../../People/canonicals/AREA_GOVERNANCE_DISCIPLINE.md
  - ../../People/Compliance/canonicals/PRECEDENCE.md
upstream_ssot:
  - ../../../../../../docs/wip/planning/94-area-architecture-and-completeness-v2/reports/i94-operations-operational-sweep-thinking-synthesis-2026-06-10.md
companion_to:
  - OPERATIONS_DELIVERY_DISCIPLINE.md
  - RevOps/canonicals/REVOPS_AREA_CHARTER.md
---

# OPERATIONS_AREA_CHARTER — Operations area (I94 P3 / P1)

> Root area charter for Holistika's **delivery-capacity** area (`delivery_capacity` /
> Think Big / COO). Minted per
> [`i94-operations-operational-sweep-thinking-synthesis-2026-06-10.md`](../../../../../../docs/wip/planning/94-area-architecture-and-completeness-v2/reports/i94-operations-operational-sweep-thinking-synthesis-2026-06-10.md)
> and operator ratification (full sweep, automation-first, 6–8h/day until GTM).
> Sibling to [`REVOPS_AREA_CHARTER.md`](RevOps/canonicals/REVOPS_AREA_CHARTER.md) which
> governs the RevOps sub-area only.

## 1. Mission

Operations exists so Holistika **delivers** — initiatives, engagements, services,
and cross-area handoffs — with governed cadence and maximal automation. Operations:

1. **Executes** PMO program/portfolio cadence, RevOps value-mapping, SMO service
   rhythm, and Engagement client-delivery SOPs.
2. **Registers** process_list rows, adapter registries, service catalog, and
   cohesion routing — but does not replace other areas' domain doctrine.
3. **Automates** inbox/WIP/cohesion/mirror/area-completeness loops for solo
   operator + AIC posture.
4. **Routes** operator intent across AKOS markdown, ERP panels, external render,
   and OpenClaw runtime per OPERATIONAL_COHESION_DOCTRINE.

The verb is **deliver**: Operations does not own Marketing campaigns, Data
governance standards, or Finance ledger facts — it **runs the spine** that connects
them at execution time.

## 2. Sub-areas + roles

| Sub-area | Folder | Role anchor | Delivery mode tag |
|:---|:---|:---|:---|
| **PMO** | `Operations/PMO/` | COO → PMO | project + program |
| **RevOps** | `Operations/RevOps/` | COO → RevOps Manager | project (engagement spine) |
| **SMO** | `Operations/SMO/` | COO → Service Manager | service |
| **Engagement** | `Operations/Engagement/` | PMO + RevOps | project (client delivery) |

**IntelligenceOps** (`Operations/IntelligenceOps/`) is **misplaced** — research-
application work belongs under Research; eviction planned at I94 P3 placement gate
(charter-only until operator approves file moves).

**business-strategy** under `PMO/canonicals/business-strategy/` is **placement debt**
(I95 L6); register strategy there; execute via Marketing/Finance/RevOps elsewhere.

## 3. Area boundary

- **Operations INTEGRATES delivery** across PMO, RevOps, SMO, Engagement.
- **Operations does NOT own** Marketing execution, Data SSOT, Finance monetary facts,
  or People methodology minting.
- **Operations does NOT replace RevOps** — RevOps charter governs value-mapping;
  this charter governs the umbrella delivery-capacity area.
- **Project vs service** is a **tag** on work items, not a split of the Operations
  area (per I94 Round-3 Q-OPS).

## 4. PMBOK spine

Delivery maturity is scored on PMBOK Guide 7th Edition performance domains via
[`OPERATIONS_DELIVERY_DISCIPLINE.md`](OPERATIONS_DELIVERY_DISCIPLINE.md) (AREA-03).
PMBOK 8 domain names (Governance, Scope, Schedule, Finance, Stakeholders,
Resources, Risk) align ERP and forward panels without duplicating Finance/Data
doctrine.

## 5. Cross-area integrations

| Consumer / provider | Contract |
|:---|:---|
| **Data** | Mirror emit trigger; schema in migrations; Operations never authors DDL |
| **People / Compliance** | process_list + baseline gates before net-new rows |
| **Finance** | FINOPS bridge SOP; registered_fact entity gate |
| **Tech / Envoy** | CICD baseline, deploy-health fleet hygiene |
| **Marketing** | MKTOPS quality bar enforced by RevOps; not duplicated here |

## 6. Area-completeness posture

At charter mint (2026-06-10): 70% score, crit@L3 9/10. P1 targets AREA-02/03/11/13;
P6 target crit@L3 10/10 COMPLETE for tier.

## 7. Cross-references

- Delivery doctrine: [`OPERATIONS_DELIVERY_DISCIPLINE.md`](OPERATIONS_DELIVERY_DISCIPLINE.md)
- Cohesion routing: [`PMO/canonicals/OPERATIONAL_COHESION_DOCTRINE.md`](PMO/canonicals/OPERATIONAL_COHESION_DOCTRINE.md)
- RevOps sub-charter: [`RevOps/canonicals/REVOPS_AREA_CHARTER.md`](RevOps/canonicals/REVOPS_AREA_CHARTER.md)
- I94 sweep charter: [`i94-operations-operational-sweep-charter-2026-06-10.md`](../../../../../../docs/wip/planning/94-area-architecture-and-completeness-v2/reports/i94-operations-operational-sweep-charter-2026-06-10.md)
- Cursor rule: [`.cursor/rules/akos-operations-delivery.mdc`](../../../../../../.cursor/rules/akos-operations-delivery.mdc)
