---
language: en
status: active
authored: 2026-05-13
last_review: 2026-05-13
role_owner: PMO
classification: fact
ssot: true
---

# Initiative kickoff templates

Per-initiative copy-pasteable prompts you hand to a fresh agent (Cursor agent, Cloud Agent, or background subagent). Each template is **pre-filled for that specific initiative** — pick the right file, copy the entire content into a new Cursor chat, and the agent has everything it needs.

All six templates plug into the same Cursor rules:

- [`.cursor/rules/akos-inline-ratification.mdc`](../../../../.cursor/rules/akos-inline-ratification.mdc) — never write `OPERATOR PAUSE POINT`; surface options inline via `AskQuestion`.
- [`.cursor/rules/akos-planning-traceability.mdc`](../../../../.cursor/rules/akos-planning-traceability.mdc) — phase plan structure, master-roadmap mirror discipline.
- [`.cursor/rules/akos-governance-remediation.mdc`](../../../../.cursor/rules/akos-governance-remediation.mdc) — phase structure (scope / prerequisites / deliverables / verification).
- [`.cursor/rules/akos-mirror-template.mdc`](../../../../.cursor/rules/akos-mirror-template.mdc) — external-repo SSOT pointer.

For the **generic** prompt trio (Discovery / Plan-Author / Pre-flight) when authoring a brand-new initiative from scratch, see [`initiative-planning-prompts.md`](initiative-planning-prompts.md).

## Index

| Initiative | Current state | Template | Best next move | When to run |
|:---|:---|:---|:---|:---|
| **I71** — CI/CD + AIOps baseline | active, P0 shipped | [`i71-kickoff-prompt.md`](i71-kickoff-prompt.md) | Author Cursor plan from master-roadmap + start **P1 Pack A1** (Brand voice register expansion) | Anytime; sequential P1 → P2 → P3 → P4 → P5 → P6. |
| **I72** — Marketing Area Governance + Persona Registry + IntelligenceOps Register Expansion | gated_operator (existing INIT row at registry line 58) | [`i72-kickoff-prompt.md`](i72-kickoff-prompt.md) | **Discovery + Plan-Author + P0 charter** (3 super-strands; activates existing INIT row, does NOT mint a fresh one) | P0–P3 + P5 + P6 can run anytime; only **P4 (RevOps activation)** is hard-gated on **I71 P5 Pack A4** (`validate_render_ownership.py`). |
| **I73** — People Ops + Learning curriculum | candidate | [`i73-kickoff-prompt.md`](i73-kickoff-prompt.md) | **Discovery + Plan-Author + P0 charter** | After I72 P0 + first Holistik Researcher hire commitment. |
| **I74** — Brand-tooling productization | candidate (dormant by design) | [`i74-kickoff-prompt.md`](i74-kickoff-prompt.md) | **Hold** — TRIGGER-2 has not fired (0 external requests). Template includes the trigger-fired Discovery prompt. | Only when ≥2 external orgs request AKOS doctrine consumption without source-fork. |
| **I75** — Research area governance | candidate | [`i75-kickoff-prompt.md`](i75-kickoff-prompt.md) | **Discovery + Plan-Author + P0 charter** | After I71 + I72 + I73 P0 charters ship + Research Director commitment. |
| **I76** — MADEIRA elevation | candidate | [`i76-kickoff-prompt.md`](i76-kickoff-prompt.md) | **Strand A external research → C-76-1 ratification → Plan-Author → P0 charter** | After Strand A research completes (the AICs F1–F5 question must ratify before charter). |

## How each template is structured

Every template carries these sections (so you don't have to remember anything):

1. **Goal** — one line.
2. **Inputs to substitute** — usually just `[OPERATOR_NOTES]`; everything else is pre-filled.
3. **Read first** — the rules and canonicals the agent must read before acting.
4. **Initiative-specific guidance** — what to focus on, what conundrums matter most, what external sources to query.
5. **Inline-ratify discipline** — explicit reminder.
6. **Outputs** — the deliverables.
7. **Validation + commit** — the gates before commit.

## Why per-initiative and not just the generic trio

The generic [`initiative-planning-prompts.md`](initiative-planning-prompts.md) trio is the **author's reference**: it teaches an agent the discipline. The per-initiative kickoff templates are the **operator's runbook**: each one is a concrete launch command for one initiative, pre-filled with the right canonicals to read, the right conundrums to surface, and the right external sources to research. You copy the whole file into a new chat and the agent has the entire context — no substitution work, no guessing.
