# Memory continuity (`memory/`)

Bootstrap and `scripts/bootstrap.py` create dated notes under this directory:

- Pattern: `memory/YYYY-MM-DD.md`
- Purpose: post-compaction session recovery; supporting context only, not HLK canonical truth.

After `MEMORY.md` is present, bootstrap seeds recent dates from `MEMORY.md`. Agents should read the newest one or two notes when the startup contract requires it.
