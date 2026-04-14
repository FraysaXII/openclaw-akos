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
