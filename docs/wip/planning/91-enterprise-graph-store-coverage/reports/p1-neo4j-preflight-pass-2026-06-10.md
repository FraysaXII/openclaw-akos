---
intellectual_kind: phase_report
sharing_label: internal_only
initiative_id: INIT-OPENCLAW_AKOS-91
authored: 2026-06-10
language: en
linked_decisions:
  - D-IH-91-A
  - D-IH-95-L
phase: P1
status: PASS
supersedes: p1-neo4j-preflight-blocked-2026-06-01.md
---

# I91 P1 — Neo4j preflight PASS

Unblocked by **I95 F6** (Neo4j Free-tier restore on instance `6c0d76bf`, 2026-06-09). Supersedes [`p1-neo4j-preflight-blocked-2026-06-01.md`](p1-neo4j-preflight-blocked-2026-06-01.md) (BLOCKED-ENV audit trail retained).

## Mechanical evidence (no secrets)

### Connectivity probe

```powershell
py scripts/neo4j_connectivity_probe.py
```

| Signal | Value |
|:---|:---|
| Exit code | **0** |
| Aura instance | `6c0d76bf` |
| URI host | `6c0d76bf.databases.neo4j.io` |
| Username posture | `6c0d76bf` (instance-id username — valid post-restore) |
| Bolt verdict | PASS (`RETURN 1 → 1` for user `6c0d76bf`) |
| Env bootstrap | `~/.openclaw/.env` present; `NEO4J_TRUST=all` (neo4j+s → neo4j+ssc rewrite) |

### Sync dry-run smoke

```powershell
py scripts/sync_hlk_neo4j.py --dry-run
```

| Signal | Value |
|:---|:---|
| Exit code | **0** |
| Registry load | 71 roles, 496 processes |
| Graph model | 1275 edges (legacy emit_mode); parity check only — no Bolt write |

## Verdict

**PASS** — I91 P1 exit gate cleared. P2 store-coverage matrix v1 may mark Neo4j-backed rows **PASS** (read projection) rather than TBD.

## Cross-references

- I95 CQ UAT: [`../../95-canonical-articulation-model/reports/i95-neo4j-cq-uat-2026-06-09.md`](../../95-canonical-articulation-model/reports/i95-neo4j-cq-uat-2026-06-09.md)
- I07 closure baseline: [`../../07-hlk-neo4j-graph-projection/reports/`](../../07-hlk-neo4j-graph-projection/reports/)
- Tranche 3 cluster evidence: [`../../95-canonical-articulation-model/reports/i95-tranche3-session-doctrine-2026-06-10.md`](../../95-canonical-articulation-model/reports/i95-tranche3-session-doctrine-2026-06-10.md)
