# Langfuse UAT — agent-proxy (2026-04-15)

**Method:** `user-langfuse` MCP `fetch_traces` + `py scripts/test-langfuse-trace.py`  
**SOC:** No API keys or hostnames recorded here.

## Results

| Step | Outcome |
|:-----|:--------|
| `py scripts/test-langfuse-trace.py` | **PASS** — `auth_check()` passed; test trace sent (`environment=dev-local`). |
| MCP `fetch_traces` (`age`: 10080 then 60 min, `limit` 5–10, compact) | **Empty list** (`item_count`: 0) — MCP-visible project returned no rows in the queried window. |
| Inference | **PARTIAL / visibility gap:** ingestion from the dev workspace reaches *a* project (per smoke script), while the Langfuse MCP session may be bound to a different project or API scope than the smoke trace destination. Align MCP credentials / project id with `LANGFUSE_*` env used by `test-langfuse-trace.py` (operator dashboard check). |

## Recommendation

Re-run `fetch_traces` with a matched project after confirming the Langfuse MCP server uses the same `LANGFUSE_PUBLIC_KEY` / host as local telemetry (`akos/telemetry.py`, `scripts/log-watcher.py`).

---

## Operator guide: align Cursor Langfuse MCP with `test-langfuse-trace.py`

**What the smoke script uses (same as runtime telemetry)** — see [`akos/telemetry.py`](../../../../../akos/telemetry.py) and [`scripts/test-langfuse-trace.py`](../../../../../scripts/test-langfuse-trace.py):

| Variable | Role |
|:---------|:-----|
| `LANGFUSE_PUBLIC_KEY` | Project API public key (identifies which project receives traces). |
| `LANGFUSE_SECRET_KEY` | Secret key for that **same** project. |
| `LANGFUSE_HOST` | API base URL (defaults to `https://cloud.langfuse.com` if unset; use your self-host URL if applicable). |
| `LANGFUSE_TRACING_ENVIRONMENT` | Optional; set by reporter from `AKOS_ENV` / `--environment` (e.g. `dev-local`). |
| `~/.openclaw/.env` | Loaded first by the smoke script via `load_runtime_env` — keys there override missing process env. |

**Why MCP returned empty traces while the script passed**

The Python script reads **`~/.openclaw/.env`** (and process env). The **Cursor `user-langfuse` MCP server** uses whatever credentials you configured in **Cursor MCP settings** (often a different `.env`, old keys, or another Langfuse project). Different **public key** = different project = `fetch_traces` shows nothing even though the dashboard where *you* look might be yet another project if you have multiple tabs.

**What to do (checklist)**

1. In Langfuse **Settings → API keys** for the project where you **actually** see the smoke trace, copy **public** and **secret** keys and note **region/host** (cloud vs EU vs self-hosted).
2. Open **`~/.openclaw/.env`** and confirm the same three values (`LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, `LANGFUSE_HOST`) match that project.
3. Open **Cursor → Settings → MCP** (or your `mcp.json`) for the **Langfuse** server and set **the identical** three values (or point its env file at the same `~/.openclaw/.env` if your setup allows one source of truth).
4. Restart Cursor (or reload MCP) so the server picks up new env.
5. Run `py scripts/test-langfuse-trace.py` again, confirm the trace in the **same** Langfuse project UI.
6. Run MCP `fetch_traces` with a small `age` (e.g. 30–60 minutes). You should see at least one trace once keys match.

**Sanity check:** In the dashboard, the project name / project id in the URL should correspond to the API keys you pasted—if in doubt, create a **new** API key pair in that project and use it everywhere (`.env` + Cursor MCP).
