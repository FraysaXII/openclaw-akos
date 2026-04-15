# Initiative 07: HLK Neo4j graph projection

**Status:** Closeout — control-plane explorer, prompt DI (`OVERLAY_HLK_GRAPH`), browser-smoke parent fix, ops runbook.  
**Source plans (Cursor, read-only in repo):** `hlk_neo4j_graph_projection_ce908938.plan.md`, `hlk_graph_plan_closeout_23908221.plan.md` (under `~/.cursor/plans/`; do not duplicate edits here without operator intent).

## Phases (execution SSOT for this folder)

| Phase | Scope |
|-------|--------|
| A–D | Original Neo4j mirror, vault links, MCP/REST, Streamlit explorer, deferred GraphRAG (see source plan). |
| **E** | **Production graph operations** — compose bring-up, `NEO4J_*` in `~/.openclaw/.env`, post-CSV `sync_hlk_neo4j.py`, rebuild-from-git DR, evidence matrix ([`reports/uat-neo4j-graph-evidence-template.md`](reports/uat-neo4j-graph-evidence-template.md)). |
| **F** | **Operator UX** — primary `GET /hlk/graph/explorer` on FastAPI; Streamlit secondary. |
| **G** | **Smoke / DX** — Windows parent parses worker `JSON_RESULTS` on non-zero exit; exit `2` when no parseable JSON; release-gate soft-PASS for `2`. |
| **H** | **Prompt DI** — `OVERLAY_HLK_GRAPH.md` in `model-tiers.json` standard/full; compact omits graph ladder in prompts. |

## Asset classification (PRECEDENCE)

| Class | Assets |
|-------|--------|
| **Canonical** | `docs/references/hlk/compliance/*.csv`, compliance taxonomy markdown, v3.0 authored markdown |
| **Mirrored / derived** | Neo4j graph contents, optional Document/LINKS_TO projection from v3.0 |
| **Reference-only** | `docs/references/hlk/Research & Logic/` — do not ingest as SSOT into Neo4j |
| **Non-canonical** | This folder, UAT evidence under `reports/` |

Link: [PRECEDENCE.md](../../../references/hlk/compliance/PRECEDENCE.md).

## Decision log

| ID | Decision |
|----|-----------|
| D1 | Neo4j credentials only via `~/.openclaw/.env` using `bootstrap_openclaw_process_env()` from `akos.io` (same contract as `scripts/serve-api.py`). |
| D2 | Allowlisted Cypher only in `akos/hlk_neo4j.py`; MCP + REST share templates. |
| D3 | `validate_hlk_vault_links.py` is always-on in `release-gate.py` after stabilization. |
| D4 | **Primary** operator graph UI: `GET /hlk/graph/explorer` (static HTML + vis-network). **Secondary:** `scripts/hlk_graph_explorer.py` (Streamlit). |
| D5 | Compact-tier Madeira prompts omit `hlk_graph_*` ladder; standard/full append `OVERLAY_HLK_GRAPH.md`. |
| D6 | **Explorer UX:** `static/hlk_graph_explorer.html` — stepped journey + summary **cards** + **role** / **process** graph actions; **v3** adds registry-driven pickers (`/hlk/areas`, `/hlk/roles`, `/hlk/processes`, tree + search) and shared depth/limit sliders (SSOT via REST only); `data-testid` hooks; `serve-api.py` **preflight bind** (`USER_GUIDE` §9.10). |

## Governed verification matrix

Run before merge (same breadth as [docs/DEVELOPER_CHECKLIST.md](../../../DEVELOPER_CHECKLIST.md)):

- `py scripts/legacy/verify_openclaw_inventory.py`
- `py scripts/check-drift.py`
- `py scripts/test.py all`
- `py -m pytest tests/test_api.py -v`
- `py scripts/validate_hlk.py`
- `py scripts/validate_hlk_vault_links.py`
- `py scripts/validate_hlk_km_manifests.py` when `v3.0/_assets/**/*.manifest.md` change
- `py scripts/release-gate.py`
- `py scripts/browser-smoke.py --playwright` when dashboard/API/UI routes change
- `py scripts/sync_hlk_neo4j.py` when validating a live mirror (requires `NEO4J_*` + `pip install neo4j`)

**UAT evidence:** [`reports/uat-neo4j-graph-evidence-template.md`](reports/uat-neo4j-graph-evidence-template.md) and dated runs under `reports/`.

## Verification record (automated, agent)

| Check | Result | Date |
|-------|--------|------|
| release-gate | PASS | 2026-04-15 |
| test_browser_smoke_parse | PASS (pytest) | 2026-04-15 |
| tests/test_api.py TestHlkGraph | PASS (incl. explorer HTML) | 2026-04-15 |
| Browser MCP explorer UAT | PASS (see [`reports/uat-graph-explorer-browser-20260415.md`](reports/uat-graph-explorer-browser-20260415.md)) | 2026-04-15 |

Replace rows after each operator-run matrix.
