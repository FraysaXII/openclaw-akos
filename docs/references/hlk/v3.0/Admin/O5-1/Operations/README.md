# Operations area (O5-1)

Holistika's **delivery-capacity** area — executes PMO, RevOps, SMO, and Engagement
work so programs run with governed cadence and maximal automation.

## Kind + entity

| Field | Value |
|:---|:---|
| Kind | `delivery_capacity` |
| Entity | Think Big |
| Area head | COO (`org_013`) |
| Area code | `Operations` in `process_list.csv` |

## Start here

| Need | Go to |
|:---|:---|
| Area mission + boundaries | [`OPERATIONS_AREA_CHARTER.md`](OPERATIONS_AREA_CHARTER.md) |
| PMBOK delivery doctrine (AREA-03) | [`OPERATIONS_DELIVERY_DISCIPLINE.md`](OPERATIONS_DELIVERY_DISCIPLINE.md) |
| Dual-surface routing (AKOS / ERP / render / runtime) | [`PMO/canonicals/OPERATIONAL_COHESION_DOCTRINE.md`](PMO/canonicals/OPERATIONAL_COHESION_DOCTRINE.md) |
| RevOps value-mapping sub-area | [`RevOps/canonicals/REVOPS_AREA_CHARTER.md`](RevOps/canonicals/REVOPS_AREA_CHARTER.md) |
| Executable catalog (PMO/SMO T1) | [`canonicals/OPERATIONS_PROCESS_CATALOG.yaml`](canonicals/OPERATIONS_PROCESS_CATALOG.yaml) |
| RevOps process catalog | [`RevOps/canonicals/REVOPS_PROCESS_CATALOG.yaml`](RevOps/canonicals/REVOPS_PROCESS_CATALOG.yaml) |
| Service management | [`SMO/canonicals/SOP-SERVICE_MGMT_001.md`](SMO/canonicals/SOP-SERVICE_MGMT_001.md) |
| I94 operational sweep plan | [`docs/wip/planning/94-area-architecture-and-completeness-v2/reports/i94-operations-operational-sweep-charter-2026-06-10.md`](../../../../../../docs/wip/planning/94-area-architecture-and-completeness-v2/reports/i94-operations-operational-sweep-charter-2026-06-10.md) |

## Sub-folder map

| Folder | Sub-area | Notes |
|:---|:---|:---|
| `PMO/` | Program / portfolio management | WIP, inbox, cohesion renders |
| `RevOps/` | Revenue operations | Adapters, engagement spine, QBR |
| `SMO/` | Service management | SERVICE_CATALOG, SLA_MATRIX |
| `Engagement/` | Client delivery SOPs | AREA-16 FK remediation at P3 |
| `IntelligenceOps/` | **Misplaced** — eviction to Research planned | Do not treat as delivery |

## Area-completeness

```powershell
py scripts/validate_area_completeness.py --area Operations --next
py scripts/validate_area_completeness.py --area Operations --matrix
```

Target: crit@L3 10/10 COMPLETE for tier (I94 P6).

## Cursor rule + skill

- Rule: [`.cursor/rules/akos-operations-delivery.mdc`](../../../../../../.cursor/rules/akos-operations-delivery.mdc)
- Skill: [`.cursor/skills/operations-delivery-craft/SKILL.md`](../../../../../../.cursor/skills/operations-delivery-craft/SKILL.md)
