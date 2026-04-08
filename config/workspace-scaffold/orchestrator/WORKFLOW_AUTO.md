# WORKFLOW_AUTO.md - Orchestrator

Startup workflow:

1. Read `IDENTITY.md`.
2. Read `USER.md` if present.
3. Read `MEMORY.md` if present.
4. Read the newest `memory/YYYY-MM-DD.md` continuity note(s) if present.
5. For direct HLK lookup requests, route to Madeira first; reserve orchestration for multi-step or write-scoped work.
6. For canonical mutations, enforce approval gates before delegating to Executor.
7. If required context is missing, state the missing artifact explicitly instead of fabricating.
