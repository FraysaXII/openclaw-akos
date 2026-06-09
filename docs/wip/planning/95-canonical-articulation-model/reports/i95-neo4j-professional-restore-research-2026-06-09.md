---
intellectual_kind: research_action_synthesis
parent_initiative: INIT-OPENCLAW_AKOS-95
lane: L4-HCAM-P2-Neo4j
authored: 2026-06-09
authored_by: Execution seat (Composer) — RA-PRO-MINT per thinking-seat 1b47cc8b
status: active
recovery_path: C
source_ledger: i95-neo4j-professional-restore-source-ledger.csv
control_confidence_level: Safe
linked_research_sources:
  - docs/wip/planning/95-canonical-articulation-model/reports/i95-neo4j-professional-restore-source-ledger.csv
downstream_artifact:
  - docs/wip/planning/95-canonical-articulation-model/reports/i95-neo4j-professional-restore-charter-2026-06-09.md
discipline: RESEARCH_ACTION_DISCIPLINE.md (15th Quality Fabric specialty; D-IH-86-FF)
---

# I95 Neo4j Professional restore — research action (2026-06-09)

> **Control layer** for paid recovery path C after operator ratified Option C (~$65/mo Professional + backup restore).
> Paired ledger: [`i95-neo4j-professional-restore-source-ledger.csv`](i95-neo4j-professional-restore-source-ledger.csv).
> Downstream charter: [`i95-neo4j-professional-restore-charter-2026-06-09.md`](i95-neo4j-professional-restore-charter-2026-06-09.md).

## 0. Operator trigger

Operator ratified **Option C** — Paid Professional clone/upgrade (~$65/mo) with explicit billing opt-in. Operator exported Aura `.backup` to repo root (`b6d76b10-2026-06-09T14-30-52-b6d76b10.backup`, ~308 KB). Keepalive workflow fails with `42NFF` (stale GHA secrets).

## 1. Named downstream decision

> **D-N4J-PRO-REST — How does AKOS restore Neo4j graph + auth on AuraDB Professional when Free-tier F1–F5 paths fail the reliability bar?**

| Tag | Sub-question |
|:---|:---|
| `professional_restore` | What is the console + AKOS rewire sequence for backup restore on Professional? |
| `F6_vs_C` | Why is backup still valuable when operator chose paid path over Free restore? |
| `reliability_budget` | How does path C align D-IH-95-G R2-09? |
| `env_contract` | What URI/secret surfaces must change? |

## 2. Eight-stage loop status

| Stage | Artifact | Status |
|:---|:---|:---|
| 1 Ingest | Source ledger SRC-N4J-09..16 | ✅ done |
| 2 Rate | Per-row reliability + credibility + Safe/Euclid/Keter | ✅ done |
| 3 Rank | External Neo4j docs first; internal CORPINT second | ✅ done |
| 4 Synthesize | This file + restore charter (RA-PRO-MINT) | ✅ done |
| 5 Govern | AskQuestion execution parameters (instance name, billing, delete timing, backup retention) | ⏳ parent agent |
| 6 Implement | Charter minted; operator executes R0–R6 | ⏳ operator |
| 7 Test | `validate_research_action.py --source-ledger` | ⏳ execution seat |
| 8 Iterate | Cross-link from free recovery runbook | ✅ done |

## 3. Prong A — External Neo4j doctrine (SRC-N4J-09..12)

1. **Restore from backup file** on Aura console for exports <4 GB (SRC-N4J-09).
2. **Professional tier** has daily scheduled snapshots (7-day retention) vs Free pause doctrine (SRC-N4J-09, SRC-N4J-10).
3. **Clone / migration-free** paths target Professional (~$65/mo) — aligns operator Option C (SRC-N4J-12).
4. **neo4j-admin upload** is large-backup fallback only; not needed for ~308 KB export (SRC-N4J-11).

## 4. Prong B — Internal Holistika doctrine (SRC-N4J-13..16)

1. **Backup preserves non-CSV graph state** that F5 CSV rebuild would drop (SRC-N4J-13).
2. **D-IH-95-G R2-09** forward budget ~$65/mo Professional + keepalive (SRC-N4J-14).
3. **Free recovery runbook** documents incident class; F1–F5 superseded for this incident once R3 probe passes (SRC-N4J-15).
4. **I07 env contract** — `~/.openclaw/.env` + GHA secrets; `neo4j+s` URI (SRC-N4J-16).

## 5. F6 vs C summary

| Path | Cost | Graph | Auth | Reliability |
|:---|:---|:---|:---|:---|
| F6 Free + backup | $0 | Preserved | Backup-era password must match env | Free pause + keepalive |
| C Professional + backup | ~$65/mo | Preserved | Fresh credentials + restore password test | Daily snapshots; no Free pause |

Operator chose **C** for reliability; backup still load-bearing for graph preservation.

## 6. Cross-references

- Restore charter: [`i95-neo4j-professional-restore-charter-2026-06-09.md`](i95-neo4j-professional-restore-charter-2026-06-09.md)
- Free recovery runbook: [`i95-neo4j-credential-recovery-2026-06-09.md`](i95-neo4j-credential-recovery-2026-06-09.md)
- Validator: `py scripts/validate_research_action.py --source-ledger docs/wip/planning/95-canonical-articulation-model/reports/i95-neo4j-professional-restore-source-ledger.csv`
