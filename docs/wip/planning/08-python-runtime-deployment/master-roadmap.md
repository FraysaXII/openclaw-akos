# Initiative 08 — Python runtime, deployment, operator journey, Neo4j graph stack

**Status:** execution in progress (repo implementation tracks this roadmap).  
**Asset classification (PRECEDENCE):** This folder is **reference / coordination** — not canonical HLK registry SSOT. Canonical CSVs and vault topics remain under `docs/references/hlk/compliance/` and `v3.0/` per [PRECEDENCE.md](../../references/hlk/compliance/PRECEDENCE.md).

## Goals

1. **Runtime & deps:** Tiered Python support (`.python-version`), optional `requirements-gpu.txt` / `requirements-openstack.txt`, documented OPENSSL_DIR last resort on Windows.
2. **Operator journey:** Single mental model — `bootstrap.py` / `doctor.py` next-step hints; optional thin `scripts/akos_operator.py`; USER_GUIDE “Operator paths” table.
3. **Test journey:** `scripts/test.py` `GROUPS` SSOT enriched; `graph` group; `neo4j` pytest marker; “if you touched X run Y” matrix in CONTRIBUTING.
4. **Neo4j / HLK graph:** Env-only `NEO4J_*`; `serve-api.py` supervises Streamlit **child process** (never OpenClaw gateway); auto-start when env real + Bolt probe; `--no-graph-explorer` / `AKOS_GRAPH_EXPLORER=0`; `/health` extensions `graph_explorer`, `neo4j_mirror`; fingerprint + validate-then-sync background path.
5. **Governance:** One atomic commit per phase; tests + required docs per phase; full verification matrix before merge ([akos-governance-remediation](../../../.cursor/rules/akos-governance-remediation.mdc)).

## Decision log

| ID | Question | Decision |
|:---|:-----------|:---------|
| D1 | OpenStack SDK in core requirements? | **`openstacksdk`** moved to **`requirements-openstack.txt`**; core `pip install -r requirements.txt` stays lean; Shadow lane documents `pip install -r requirements-openstack.txt`. |
| D2 | Graph explorer co-start | **Automatic** when `NEO4J_*` non-placeholder + Bolt OK; subprocess from **`serve-api.py`** only; disable via flag/env. |
| D3 | Mirror auto-sync | Background **fingerprint** of canonical CSVs + optional timer; **validate_hlk.py** before sync when drift touches canonical paths; state under `~/.openclaw/.akos-neo4j-sync-state.json`. |

## Verification matrix (implementation PR)

`verify_openclaw_inventory`, `check-drift`, `scripts/test.py all`, `browser-smoke.py --playwright`, `pytest tests/test_api.py -v`, `release-gate.py`, and `validate_hlk.py` / `validate_hlk_km_manifests.py` when compliance assets change.

## References

- Neo4j mirror drift incident context: operator transcript [Neo4j mirror drift](2ae1345d-d24c-4a37-ac54-188f0310f5fa) (Cursor parent chat).
- Related planning: [07-hlk-neo4j-graph-projection](../07-hlk-neo4j-graph-projection/master-roadmap.md).

## Reports

Place phase completion notes under `reports/` (e.g. `reports/phase-g-serve-api-graph.md`).
