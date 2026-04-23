# Madeira structured handoff (Orchestrator)

When the user pastes or carries a **Madeira plan draft** into this session:

1. Look for a JSON object that matches `config/schemas/madeira-plan-handoff.schema.json` (or a fenced `json` block).
2. Treat it as **non-canonical** until Architect review + operator promotion. Do not assume CSV or vault rows match the draft.
3. **Hydrate** from `citations` and HLK tools where execution depends on org facts—do not rely on long Madeira chat transcripts as SSOT.
4. Fold **goal**, **assumptions**, and **phases_mermaid** (if present) into your **Delegation Plan**; mark risky phases with `requires_approval`.
5. Route planning-heavy work to **Architect** first; keep Executor on mutations with Verifier gates.
