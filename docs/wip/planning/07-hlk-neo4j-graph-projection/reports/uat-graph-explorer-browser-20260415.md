# UAT: HLK Graph Explorer (Browser MCP) — 2026-04-15

**Surface:** `GET /hlk/graph/explorer` (control plane static HTML v2).  
**Method:** Cursor **cursor-ide-browser** MCP (`browser_navigate`, `browser_console_messages`, `browser_click`, `browser_type`).  
**API:** `py scripts/serve-api.py --port 8422` (ports **8420** and **8421** were already bound on the host; preflight bind check behaved as designed).

## Results

| Step | Result |
|------|--------|
| Navigate to `http://127.0.0.1:8422/hlk/graph/explorer` | PASS — title **HLK Graph Explorer**; regions Step 1–3, role + process controls visible |
| Console messages | PASS for app — only `[CursorBrowser] Native dialog overrides…` (host noise), no vis-network or fetch errors attributed to the page |
| **Refresh summary** | Clicked — summary cards populate when `GET /hlk/graph/summary` succeeds (depends on `NEO4J_*` in env for mirror line) |
| **Process neighbourhood** | Entered `hol_resea_dtp_99`, clicked **Load process neighbourhood** — graph path exercised (outcome depends on Neo4j configuration for this API process) |

## Governance notes

- **SOC:** No API key entered in UAT; server ran without `AKOS_API_KEY` (dev-typical loopback).
- **SSOT:** Explorer remains a client of `/hlk/graph/*` only; no alternate graph authority.

## Follow-up (operator)

- Prefer default **`http://127.0.0.1:8420/hlk/graph/explorer`** after freeing port 8420 (`USER_GUIDE.md` §9.10).
- Re-run this checklist on **8420** when the stale listener is cleared.
