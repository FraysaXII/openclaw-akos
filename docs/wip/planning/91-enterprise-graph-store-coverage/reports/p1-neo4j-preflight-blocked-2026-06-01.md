---
intellectual_kind: phase_report
sharing_label: internal_only
initiative_id: INIT-OPENCLAW_AKOS-91
authored: 2026-06-01
language: en
linked_decisions:
  - D-IH-91-A
phase: P1
status: BLOCKED-ENV
---

# I91 P1 — Neo4j preflight (blocked on operator env)

## Blocker

Agent session has **no** `NEO4J_URI` / `NEO4J_USER` / `NEO4J_PASSWORD` in `~/.openclaw/.env` (same pre-flight as I90 P0, 2026-06-01).

## Operator unblock

1. Add Neo4j credentials per I07 [`master-roadmap.md`](../../07-hlk-neo4j-graph-projection/master-roadmap.md).
2. Run locally:

```powershell
py scripts/sync_hlk_neo4j.py --dry-run
py scripts/sync_hlk_neo4j.py
```

3. Reply `continue I91 P1` when dry-run PASS.

## Mechanical checks (no Neo4j required)

| Check | Command | 2026-06-01 |
|:---|:---|:---|
| HLK umbrella | `py scripts/validate_hlk.py` | PASS |
| Vault links | `py scripts/validate_hlk_vault_links.py` | *(run at P1 entry)* |
| Sync script import | `py -c "import scripts.sync_hlk_neo4j"` | *(optional smoke)* |

## Verdict

**BLOCKED-ENV** — P2 coverage matrix may proceed with git + mirror inventory; graph-backed rows stay `TBD` until P1 clears.
