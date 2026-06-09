---
intellectual_kind: research_action_synthesis
parent_initiative: INIT-OPENCLAW_AKOS-95
lane: L4-HCAM-P2-Neo4j
authored: 2026-06-09
authored_by: Execution seat (Composer) — RA-2 mint per thinking-seat 5b1b3f98
status: active
incident_class: aura_free_credential_misguidance
source_ledger: i95-neo4j-aura-free-recovery-source-ledger.csv
control_confidence_level: Safe
linked_research_sources:
  - docs/wip/planning/95-canonical-articulation-model/reports/i95-neo4j-aura-free-recovery-source-ledger.csv
downstream_artifact:
  - docs/wip/planning/95-canonical-articulation-model/reports/i95-neo4j-credential-recovery-2026-06-09.md
discipline: RESEARCH_ACTION_DISCIPLINE.md (15th Quality Fabric specialty; D-IH-86-FF)
---

# I95 Neo4j Aura Free recovery — research action (2026-06-09)

> **Control layer** for credential-recovery doctrine after operator STOP on reckless clone guidance.
> Paired ledger: [`i95-neo4j-aura-free-recovery-source-ledger.csv`](i95-neo4j-aura-free-recovery-source-ledger.csv).
> Downstream runbook: [`i95-neo4j-credential-recovery-2026-06-09.md`](i95-neo4j-credential-recovery-2026-06-09.md).

## 0. Operator trigger (verbatim intent)

Operator ratified **STOP** for Neo4j recovery guidance that recommended **Clone instance** without disclosing **paid Professional tier (~$65/mo)**, cited generic **CREATE USER** docs on **Aura Free**, and failed the research-to-decision bar.

## 1. Named downstream decision

> **D-N4J-FREE-REC — What recovery paths may AKOS operator docs recommend for Aura Free credential failures without surprise billing or tier-inappropriate Cypher?**

| Tag | Sub-question |
|:---|:---|
| `free_recovery_paths` | Which **$0** paths are officially or internally verified? |
| `anti_pattern_paid_paths` | Which paths require **paid opt-in** and what cost floor? |
| `incident_class_contradiction` | Which internal precedents contradict Free-tier reality? |

## 2. Eight-stage loop status

| Stage | Artifact | Status |
|:---|:---|:---|
| 1 Ingest | Source ledger SRC-N4J-01..08 | ✅ done |
| 2 Rate | Per-row reliability + credibility + Safe/Euclid/Keter | ✅ done |
| 3 Rank | External Neo4j KB/docs first; internal CORPINT second | ✅ done |
| 4 Synthesize | This file + recovery runbook rewrite (RA-1) | ✅ done |
| 5 Govern | AskQuestion if password lost + no credentials file + non-CSV state must be kept | ⏳ operator gate |
| 6 Implement | Recovery runbook updated | ✅ done |
| 7 Test | `validate_research_action.py --source-ledger` | ⏳ execution seat |
| 8 Iterate | `incident_class: aura_free_credential_misguidance` for future validator | ✅ logged |

## 3. Prong A — External Neo4j doctrine (SRC-N4J-01..06)

**Load-bearing findings:**

1. **No support/console DB password reset on lost password** (SRC-N4J-01). Support explicitly cannot recover passwords.
2. **Credentials file is one-time at creation** (SRC-N4J-02). F2 is the only Neo4j-native way to recover an unchanged password.
3. **Browser `:server change-password` works when current password is known** (SRC-N4J-02) — F4; not a console button.
4. **Free tier pauses after 72h without writes** (SRC-N4J-05) — F1 resume path; keepalive workflow rationale (D-IH-95-G).
5. **Clone targets Professional** (SRC-N4J-04) + **one Free instance per account** (SRC-N4J-05) → clone-to-new is **not** a Free recovery path.
6. **Cost floor ~$65/mo** for Professional 1GB (SRC-N4J-06) — mandatory in DO NOT box.

## 4. Prong B — Internal Holistika doctrine (SRC-N4J-07..08)

1. **F5 CSV projection rebuild** is AKOS-preferred $0 path when password is irrecoverable (SRC-N4J-07). Governed sync: `py scripts/sync_hlk_neo4j.py`.
2. **INC-NEO4J-2026-05-01** recommended console Reset password (SRC-N4J-08) — **Euclid** confidence because operator proved Free UI differs; marks `aura_free_credential_misguidance` class.

## 5. Verified Free-tier path summary (implements RA-1)

| Path | Action | Source IDs |
|:---|:---|:---|
| **F1** | Resume paused instance | SRC-N4J-05 |
| **F2** | Recover credentials file | SRC-N4J-02 |
| **F3** | Browser login test | SRC-N4J-02 + operator finding |
| **F4** | `:server change-password` when known | SRC-N4J-02 |
| **F5** | Replace Free instance + AKOS CSV rebuild | SRC-N4J-07 + SRC-N4J-01 |

## 6. Anti-patterns + incident class

```
INCIDENT_CLASS: aura_free_credential_misguidance
```

| Anti-pattern | Source IDs | Cost / failure |
|:---|:---|:---|
| Recommend clone without ~$65/mo + opt-in | SRC-N4J-04; SRC-N4J-06 | Surprise billing |
| CREATE USER on Free | operator finding | `42NFF` |
| Console DB reset from May 2026 incident doc | SRC-N4J-08 | UI absent on Free |
| Instance id as username | operator + `akos/hlk_neo4j.py` | Auth fail |

## 7. Governance — AskQuestion (when F2/F3 fail)

Surface to operator when password is lost, no credentials file found, and non-CSV graph state may matter:

- **A (recommended):** F5 — replace Free + CSV rebuild ($0; loses keepalive/ad-hoc nodes)
- **B:** Export `.backup` → destroy → new Free → restore (manual; not in lost-password KB verbatim)
- **C:** Paid clone/upgrade (~$65/mo) — **explicit billing opt-in only**
- **D:** STOP — search password manager for original credentials file

## 8. Cross-references

- Recovery runbook: [`i95-neo4j-credential-recovery-2026-06-09.md`](i95-neo4j-credential-recovery-2026-06-09.md)
- CQ UAT (blocked): [`i95-neo4j-cq-uat-2026-06-09.md`](i95-neo4j-cq-uat-2026-06-09.md)
- E2e charter: [`i95-neo4j-e2e-cutover-charter-2026-06-09.md`](i95-neo4j-e2e-cutover-charter-2026-06-09.md)
- Discipline: [`RESEARCH_ACTION_DISCIPLINE.md`](../../../../../docs/references/hlk/v3.0/Research/Methodology/canonicals/RESEARCH_ACTION_DISCIPLINE.md)
- Validator: `py scripts/validate_research_action.py --source-ledger docs/wip/planning/95-canonical-articulation-model/reports/i95-neo4j-aura-free-recovery-source-ledger.csv`
