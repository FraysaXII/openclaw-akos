# Cursor two-seat routing (repo guide)

> **Durable guide** for separating **judgment** (thinking seat) from **mechanical execution**
> (Composer seat) in this workspace. Applies to **any** initiative — not a single planning folder.
>
> **Ratifying decision:** `D-IH-90-R` (first worked example:
> [`docs/wip/planning/90-routing-and-wiring/`](../wip/planning/90-routing-and-wiring/)).

## When to use two seats

| Use two seats when | Single seat is enough |
|:---|:---|
| Canonical CSV tranches, multi-file governance mints, validator fleets | Typo fixes, one-file refactors, narrow questions |
| Operator pause points + inline-ratify batches | Read-only exploration |
| Large P3 backlog drains with fresh threads per packet | Sub-30-minute scoped edits |

## Seats

| Seat | Agent file | Typical model | Writes? |
|:---|:---|:---|:---:|
| Thinking | [`.cursor/agents/planner.md`](../../.cursor/agents/planner.md) | Opus / thinking picker | **No** (`readonly: true`) |
| Execution | [`.cursor/agents/executor.md`](../../.cursor/agents/executor.md) | **composer-2.5** (pin in frontmatter) | Yes |
| Review (optional) | [`.cursor/agents/reviewer.md`](../../.cursor/agents/reviewer.md) | inherit | No |

## Custom modes (recommended)

1. **Holistika — Think** — thinking model + `planner.md` instructions (or @ planner agent).
2. **Holistika — Execute** — Composer 2.5 + `executor.md` for packet runs.

## Workflow

1. **Think** — decompose into packets; cite evidence; surface inline-ratify gates where needed.
2. **Hard stop** at a handoff marker (below).
3. **Switch** model / mode to Composer 2.5.
4. **Execute** one packet per thread (fresh thread for large fleets: mirror families, rule sweeps).
5. On blocker → `=== COMPOSER BLOCKED -> SWITCH TO OPUS ===` and return to thinking seat.

## Handoff markers (copy/paste)

```text
=== OPUS DONE -> SWITCH TO COMPOSER ===
=== THINKING DONE — operator review ===
=== COMPOSER BLOCKED -> SWITCH TO OPUS ===
```

A **stop** hook in [`.cursor/hooks.json`](../../.cursor/hooks.json) prints a reminder if you forget the handoff block.

## Verify executor pin

In the executor chat, ask which model is active. If not Composer 2.5, fix the mode picker before CSV edits or validator runs.

## Worked examples (copy the rhythm)

| Programme | Workflow doc | First executor packet |
|:---|:---|:---|
| I90 routing (first example) | [`two-seat-setup-guide-2026-05-30.md`](../wip/planning/90-routing-and-wiring/reports/two-seat-setup-guide-2026-05-30.md) | (initiative-specific) |
| I93 DATA area | [`93-data-area-foundation-and-governance/master-roadmap.md`](../wip/planning/93-data-area-foundation-and-governance/master-roadmap.md) §9 packets | P0–P8 inline packets |
| **Finance full area (I88)** | [`finance-area-two-seat-workflow-2026-06-05.md`](../wip/planning/88-cross-area-ops-wiring-review-discipline/reports/finance-area-two-seat-workflow-2026-06-05.md) | [`finance-area-executor-packet-f1-2026-06-05.md`](../wip/planning/88-cross-area-ops-wiring-review-discipline/reports/finance-area-executor-packet-f1-2026-06-05.md) |

**Packet template (any initiative):** [`docs/wip/planning/_templates/executor-packet-template.md`](../wip/planning/_templates/executor-packet-template.md).

## Initiative context

Charters, decision logs, and gate reports live under `docs/wip/planning/<NN>-<slug>/` — see [`docs/wip/planning/README.md`](../wip/planning/README.md). This guide does not duplicate per-initiative tables.

## Related doctrine

- [`.cursor/rules/akos-aic-delegation.mdc`](../../.cursor/rules/akos-aic-delegation.mdc)
- [`.cursor/skills/aic-delegation-craft/SKILL.md`](../../.cursor/skills/aic-delegation-craft/SKILL.md)
- [`AGENTS.md`](../../AGENTS.md) — workspace index + tier model
- [`config/cursor-rule-tiers.json`](../../config/cursor-rule-tiers.json) — always-on cap + core rule list
