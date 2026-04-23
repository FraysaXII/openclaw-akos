# Madeira context economics (wip)

Non-release contract for initiative 17. Operators: keep Ask on **compact** Madeira assembly; use **plan_draft** only when producing structured drafts.

## Per-mode overlay / assembly

| `madeiraInteractionMode` | Madeira assembled base | Extra overlay appended to `SOUL.md` |
|--------------------------|------------------------|-------------------------------------|
| `ask` | `MADEIRA_PROMPT.compact.md` | none |
| `plan_draft` | `MADEIRA_PROMPT.standard.md` | `OVERLAY_MADEIRA_PLAN_DRAFT.md` |

Other agents always use the **global** prompt variant from the active model tier / switch (`deploy_soul_prompts`).

## Swarm hydration

- Orchestrator and Architect MUST prefer **structured handoff JSON + citations** from the user message or paste buffer.
- Do **not** treat full multi-turn Madeira chat transcripts as SSOT; re-ground with `hlk_*` / repo reads as needed.

## Telemetry (target fields)

- `madeira_interaction_mode` on answer-quality rows when present in session metadata (future gateway) or inferred from control plane.
