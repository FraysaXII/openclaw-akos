---
intellectual_kind: operator_guide
sharing_label: internal_only
initiative_id: INIT-OPENCLAW_AKOS-90
authored: 2026-06-01
language: en
linked_decisions:
  - D-IH-90-G
  - D-IH-90-L
  - D-IH-90-V
---

# Two-seat setup guide — I90 worked example (2026-06-01)

> **Canonical repo guide:** [`docs/guides/cursor-two-seat-routing.md`](../../../../guides/cursor-two-seat-routing.md)
> (durable; all initiatives). This file is the **I90** snapshot + cluster-specific notes.
>
> **Purpose:** How the operator switches between the **thinking seat** (judgment)
> and the **execution seat** (Composer 2.5). Documentation only — no secrets in git.

## Seats

| Seat | Agent file | Model | Can write? |
|:---|:---|:---|:---:|
| Thinking | [`.cursor/agents/planner.md`](../../../../.cursor/agents/planner.md) | Opus / thinking (picker) | **No** (`readonly: true`) |
| Execution | [`.cursor/agents/executor.md`](../../../../.cursor/agents/executor.md) | **composer-2.5** | Yes |
| Review (optional) | [`.cursor/agents/reviewer.md`](../../../../.cursor/agents/reviewer.md) | inherit | No |

## Custom Modes (recommended)

1. **Holistika — Think** — bind Agent mode to your thinking model; paste
   `planner.md` instructions or @-mention the planner agent.
2. **Holistika — Execute** — bind Agent mode to **Composer 2.5**; use
   `executor.md` for packet runs.

## Workflow

1. **Think** in planner seat → decompose into packets + inline-ratify gates.
2. **Hard stop** at handoff block (`=== OPUS DONE -> SWITCH TO COMPOSER ===` or
   `=== THINKING DONE — operator review ===` in Composer-only sessions).
3. **Switch** model / mode to Composer 2.5.
4. **Execute** one packet per thread (fresh thread for large fleets: P3b, P3c,
   I91 mirror families).
5. On blocker → `=== COMPOSER BLOCKED -> SWITCH TO OPUS ===` and return to
   thinking seat.

## Verify executor pin

In the executor chat, ask: *"Which model are you?"* If not Composer 2.5, fix the
mode picker before running validators or CSV edits.

## Statusline

Optional: configure Cursor statusline (bundled skill at
`~/.cursor/skills-cursor/statusline/SKILL.md`) to show active model + context %.

## P2e follow-up

Plan commits [`.cursor/hooks/seat_handoff_reminder.py`](../../../../.cursor/hooks/seat_handoff_reminder.py)
on `stop` event — redundant reminder if you forget the handoff block.

## References

- [`akos-aic-delegation.mdc`](../../../../.cursor/rules/akos-aic-delegation.mdc)
- [`aic-delegation-craft`](../../../../.cursor/skills/aic-delegation-craft/SKILL.md)
- [`model-routing-map.md`](../../../intelligence/model-selection-2026-05-28/model-routing-map.md)
