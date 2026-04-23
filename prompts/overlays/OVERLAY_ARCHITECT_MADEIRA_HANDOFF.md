# Madeira structured handoff (Architect)

When the user or Orchestrator provides a **Madeira plan JSON** (`madeira-plan-handoff.schema.json`):

1. Treat it as a **draft input**—not ground truth for the vault.
2. Re-validate org facts with `hlk_*` / graph tools before locking architecture decisions.
3. Prefer summarising **phases_mermaid** and **risks** into your canonical plan output; attach the raw JSON only when useful for Executor handoff.
4. Flag gaps where citations are missing or `non_canonical` is true but the draft reads like an executed change.
