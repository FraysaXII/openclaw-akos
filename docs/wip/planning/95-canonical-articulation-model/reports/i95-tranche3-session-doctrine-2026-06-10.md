---
authored: 2026-06-10
tranche: I95-T3
parent_initiative: INIT-OPENCLAW_AKOS-95
linked_initiative: INIT-OPENCLAW_AKOS-91
---

# I95 Tranche 3 session doctrine (I91 P1–P2)

Binding rule/skill card for this execution session. Refer back at each major action.

| When I touch… | Load… | One-line when |
|:---|:---|:---|
| I91 charter + phase gates | [`91-enterprise-graph-store-coverage/master-roadmap.md`](../../91-enterprise-graph-store-coverage/master-roadmap.md) | P1 preflight + P2 matrix v1 SSOT under I91 `reports/` |
| Cluster burndown rank 2 | [`i95-initiative-cluster-map.md`](../i95-initiative-cluster-map.md) | Exit: probe exit 0 + matrix minted |
| Neo4j harness (I95 F6) | [`akos/hlk_neo4j.py`](../../../../akos/hlk_neo4j.py) + [`scripts/neo4j_connectivity_probe.py`](../../../../scripts/neo4j_connectivity_probe.py) + [`scripts/sync_hlk_neo4j.py`](../../../../scripts/sync_hlk_neo4j.py) | Instance `6c0d76bf`; no secrets in reports |
| I93 scope split (no double-mint) | [`i91-i93-cross-initiative-regression-2026-06-04.md`](../../93-data-area-foundation-and-governance/reports/i91-i93-cross-initiative-regression-2026-06-04.md) | I93 owns DATA-FAM CAP rows; I91 owns coverage matrix |
| P0 evidence before edits | [`akos-applied-research-discipline.mdc`](../../../../.cursor/rules/akos-applied-research-discipline.mdc) + [`applied-research-craft/SKILL.md`](../../../../.cursor/skills/applied-research-craft/SKILL.md) | Internal sweep mandatory; external only if novel |
| Planning traceability | [`akos-planning-traceability.mdc`](../../../../.cursor/rules/akos-planning-traceability.mdc) | `files-modified.csv` + PMO sweep on touch |

## Tranche 3 action checklist

1. P0 research mint (`i95-p0-research-i91-store-coverage-2026-06-10.md`) — **before** execution
2. Run `neo4j_connectivity_probe.py` — capture PASS evidence (leak-safe JSON only)
3. Run `sync_hlk_neo4j.py --dry-run` — I91 P1 smoke per roadmap
4. Mint store-coverage matrix v1 under I91 `reports/store-coverage-matrix-2026-06-10.md`
5. Mint P1 preflight PASS report; update I91 `master-roadmap.md` P1/P2 lines
6. Update cluster map burndown rank 2 → DONE; PMO sweep §7; both `files-modified.csv`
7. Validators: `verify.py pre_commit_fast`
8. Single phase commit per operator gate

## Gates honored

- No `process_list.csv` / `baseline_organisation.csv` edits
- No INITIATIVE_REGISTRY CSV edits
- No canonical CSV promotion (matrix stays report-class v1; forward-charter to canonical if promoted later)
- AskQuestion skipped — no genuine fork (I95 F6 unblocked P1; matrix schema follows P0 inventory)
