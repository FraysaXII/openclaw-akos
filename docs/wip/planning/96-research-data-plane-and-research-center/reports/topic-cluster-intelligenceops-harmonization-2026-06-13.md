---
parent_initiative: INIT-OPENCLAW_AKOS-96
report_kind: harmonization-spec
authored: 2026-06-13
audience: J-OP;J-AIC
status: active
---

# topic_cluster ↔ IntelligenceOps harmonization (2026-06-13)

> **Problem:** Research source ledgers use `topic_cluster` (pack taxonomy). The IntelligenceOps register uses `target_id` + `target_class` (live intel verify-by). Research Center BFF currently reads the register for staleness but does not wire ledger `topic_cluster` into prong/staleness cards consistently.

## GOJ implementation spec (binding — do not conflate)

From the governed operator journey implementation spec:

| Register | Governs | Research Center surface |
|:---|:---|:---|
| Source ledger `topic_cluster` | Which **research pack** a citation belongs to | Prong strip aggregates · ledger completion copy |
| `INTELLIGENCEOPS_REGISTER` | Which **intel targets** are overdue for verify | Radar freshness strip · staleness insight cards |

When the IntelligenceOps register is empty or thin, the UI must show an honest empty queue + sweep CTA — **not** substitute topic_cluster counts as fake staleness targets.

## Field mapping table

| Source ledger field | Example values | IntelligenceOps field | BFF / RC field | Notes |
|:---|:---|:---|:---|:---|
| `topic_cluster` | `governed_analytics`, `governed_operator_journey`, `corp_vault_research` | *(no direct column)* | `prongStrip.packCoverage[]` | Pack completion % — **not** radar queue membership |
| Pack folder slug | `governed-actionable-analytics-surfaces-2026-06-12` | `target_id` | `stalenessCards[].targetId` | 1:1 when pack is also an intel target |
| `prong` (BL-*) | `BL-DATA`, `BL-UX` | — | `prongStrip.prongs[]` | Baseline consumer IDs — SSOT [`source-ledger-prong-ssot-2026-06-12.md`](source-ledger-prong-ssot-2026-06-12.md) |
| — | — | `target_class` | `insight.type` chip | `recommendation`, `regulator`, `competitor_intelligence_target`, etc. |
| — | — | `staleness_posture` | Card severity + strip badge | `block_govern` → critical remediation |
| — | — | `next_verify_by` | Freshness strip + staleness card headline | ISO date compare in BFF |
| — | — | `output_artifact` | Navigate CTA `href` | Repo-relative path or WIP folder |
| — | — | `linked_runbook_path` | Drawer runbook `command` | e.g. `scripts/research_radar_sweep.py` |

## I96 pack → register row map (draft)

| topic_cluster (ledger) | IntelligenceOps `target_id` (proposed) | `register_id` |
|:---|:---|:---|
| `governed_analytics` | `governed-actionable-analytics-surfaces-2026-06-12` | `IO-I96-GOV-ANALYTICS-001` |
| `governed_operator_journey` / `operator_journey_ux` | `governed-operator-journey-ux-uat-2026-06-12` | `IO-I96-GOJ-UX-001` |
| `corp_vault_research` / research data plane | `I96-research-data-plane` | `IO-I96-RESEARCH-CENTER-001` |
| `corp_vault_tech` (AOS pack) | `akos-automation-os-governance-2026-06-10` | `IO-I96-AOS-GOV-001` |
| KiRBe / ingest | `kirbe-research-ingest-contract` | `IO-I96-KIRBE-DATA-001` |
| MADEIRA experiential | `aic-madeira-experiential-uat-2026-06-11` | `IO-I96-MADEIRA-UAT-001` |

**Rule:** One IntelligenceOps row per **verify-by intel target**. Multiple ledgers may share a `topic_cluster` label; register rows point to the **pack folder** or **program slug**, not individual `SRC-*` IDs.

## BFF contract notes (hlk-erp Research Center)

### `/api/research-center/insights` (read model)

1. **Staleness cards** — load `INTELLIGENCEOPS_REGISTER` mirror or git CSV reader; filter `lifecycle_status=active`; sort by `block_govern` first, then `next_verify_by` ascending.
2. **Prong strip** — aggregate `source-ledger.csv` rows per `prong` + optional `topic_cluster` grouping; expose `packId`, `completionPct`, `rowCount` — **separate array** from `stalenessQueue`.
3. **Empty honesty** — if register row count &lt; 3 active non-placeholder: emit `radarQueueEmpty: true` + CTA to sweep runbook; do not synthesize cards from ledger counts.
4. **Navigate CTAs** — `output_artifact` → GitHub blob or `docs/wip/` deep link; `linked_runbook_path` → drawer copy command.

### TypeScript sketch (additive fields)

```typescript
type StalenessTarget = {
  registerId: string;
  targetId: string;
  targetClass: string;
  stalenessPosture: 'block_govern' | 'cite_and_flag' | 'ok';
  nextVerifyBy: string; // ISO date
  outputArtifact: string;
  runbookPath: string;
};

type ProngPackCoverage = {
  topicCluster: string;
  prong: string;
  ledgerRowCount: number;
  completionPct: number;
};
```

### Anti-patterns (BFF)

- Using `topic_cluster` row count as `stalenessDays` proxy
- Showing `TODO[OPERATOR-*]` target_ids on T0 card face (Strict T3 — accordion only)
- Mixing prong strip and radar queue into one array (breaks GOJ tier separation)

## Verification

| Check | Command / signal |
|:---|:---|
| Ledger schema | `py scripts/validate_research_action.py --source-ledger <pack>/source-ledger.csv` |
| Register schema | `py scripts/validate_intelligenceops_register.py` |
| Sweep queue | `py scripts/research_radar_sweep.py` — DUE/STALE includes new I96 rows |
| BFF contract | hlk-erp pytest on insights route + localhost Operator lens shows register-driven card |

## Cross-references

- GOJ spec §topic_cluster: `docs/wip/intelligence/governed-operator-journey-ux-uat-2026-06-12/implementation-spec-2026-06-12.md`
- Population pack: [`intelligenceops-register-i96-population-2026-06-13.md`](intelligenceops-register-i96-population-2026-06-13.md)
- Governance corpus harmonization row: [`research-center-governance-corpus-2026-06-12.md`](research-center-governance-corpus-2026-06-12.md)
