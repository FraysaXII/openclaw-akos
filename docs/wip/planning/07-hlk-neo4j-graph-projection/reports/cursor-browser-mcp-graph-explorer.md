# Cursor browser / MCP UAT: HLK graph explorer

This runbook is for operators who want a **Cursor agent** (or you, with agent assistance) to exercise the **embedded** HLK graph UI served by the AKOS control plane—not Neo4j Browser itself. Data still lives in Neo4j Aura (or your configured `NEO4J_URI`); the explorer reads the API.

## Preconditions

1. **Populate Neo4j** (Aura): `NEO4J_*` in `~/.openclaw/.env`, then from repo root:
   - `py scripts/sync_hlk_neo4j.py`  
   - Optional document projection: add `--with-documents`.
2. **Run the API**: `py scripts/serve-api.py` (default [http://127.0.0.1:8420](http://127.0.0.1:8420)). If something else already binds `8420`, use `py scripts/serve-api.py --port 8421` and open [http://127.0.0.1:8421/hlk/graph/explorer](http://127.0.0.1:8421/hlk/graph/explorer). For `py scripts/browser-smoke.py`, set `AKOS_BROWSER_SMOKE_API_URL=http://127.0.0.1:8421` in that shell.
3. **Auth**: If `AKOS_API_KEY` is set, `/hlk/graph/explorer` requires the same **Bearer** token as other `/hlk/*` routes. For purely local agent browser smoke, you can **unset** `AKOS_API_KEY` in that shell so the page is open without a header (see `SECURITY.md`—do not use that pattern on shared hosts).

## Target URL

- Explorer: [http://127.0.0.1:8420/hlk/graph/explorer](http://127.0.0.1:8420/hlk/graph/explorer)
- JSON health: [http://127.0.0.1:8420/hlk/graph/summary](http://127.0.0.1:8420/hlk/graph/summary) (expect `neo4j: connected` when the mirror is up)

## Cursor: Simple Browser vs Playwright MCP

- **Cursor docs (web dev):** [Give Cursor access to browser](https://docs.cursor.com/guides/tutorials/web-development) points at the **Browser Tools MCP** install flow: [https://browsertools.agentdesk.ai/installation](https://browsertools.agentdesk.ai/installation) (console logs and network requests while you verify UI).
- **Simple Browser / built-in browser tools** (when your Cursor build exposes them): open the URL above after `serve-api.py` is running; sign in with Bearer only if your build supports setting headers—otherwise temporarily unset `AKOS_API_KEY` for localhost UAT.
- **Playwright MCP** (repo template: `config/mcporter.json.example` → `playwright` server): register that MCP server in Cursor, then ask the agent to navigate to the explorer URL, snapshot the page, and confirm the graph canvas or summary widgets load. If you need Bearer auth with Playwright, use your MCP client’s support for **extra headers** or environment-specific auth (varies by Cursor version); the API expects `Authorization: Bearer <AKOS_API_KEY>` when the key is set.

**Repo-automated check (no Cursor browser required):** from repo root with the API up, `py scripts/browser-smoke.py --playwright` exercises `GET /hlk/graph/explorer` and related routes (same checks an agent would do first).

## Minimal acceptance checks

1. `GET /hlk/graph/summary` shows `neo4j: connected` and non-empty `graph` when Neo4j is populated.
2. Explorer page returns `200` and renders without console errors (CDN blocked environments are called out in `docs/USER_GUIDE.md` §9.10).
3. After a canonical CSV change, re-run `py scripts/sync_hlk_neo4j.py` and confirm updated counts in the script log.

## Related

- Evidence template: [uat-neo4j-graph-evidence-template.md](./uat-neo4j-graph-evidence-template.md)
- Example Browser MCP run: [uat-graph-explorer-browser-20260415.md](./uat-graph-explorer-browser-20260415.md)
- Operator model: [docs/USER_GUIDE.md](../../../../USER_GUIDE.md) §9.10
