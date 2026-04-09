# Startup compact (Madeira)

Before **any** user-visible reply on a new or reset session:

1. `read("IDENTITY.md")`, `read("USER.md")` if present.
2. `read("WORKFLOW_AUTO.md")`, `read("MEMORY.md")` if present.
3. If `memory/` exists, read the newest `memory/YYYY-MM-DD.md` note (one or two) after `MEMORY.md`.

Skip missing files silently. Do not respond before these reads complete. Never emit `NO_REPLY`.
