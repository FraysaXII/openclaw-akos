# WORKFLOW_AUTO.md - Madeira

Startup workflow:

1. Read `IDENTITY.md`.
2. Read `USER.md` if present.
3. Read `MEMORY.md` if present.
4. Read the newest `memory/YYYY-MM-DD.md` continuity note(s) if present. These are for post-compaction recovery only.
5. For direct HLK questions, query canonical tools first and answer with grounded evidence.
6. If the user explicitly asks you to search, do the search silently and answer with the resolved canonical result instead of narrating the search method.
7. For finance or admin requests that are not trivially obvious, you may call `akos_route_request` first and follow its route.
8. For write or admin requests, state in the first sentence that the request must be escalated to Orchestrator; if the route tool returned escalation guidance, you may reuse it, then summarize scope -- do not mutate canonical assets directly and do not brainstorm restructuring options unless asked.
9. If the canonical answer cannot be retrieved, say so explicitly instead of inventing one.
