# Structured Planning Protocol

## When to Create a Plan

Create a numbered plan with checkboxes when ANY of these triggers apply:

- Multi-file or cross-layer changes
- More than 2 edit/verify iterations expected
- More than 5 information-gathering calls expected
- User explicitly requests planning or says "plan this"
- Task involves coordination between multiple agents

## When to SKIP Planning

Skip for:

- Single, straightforward tasks (rename, typo fix, config tweak)
- Purely conversational or informational requests
- Tasks completable in under 3 trivial steps

Do NOT add planning overhead to trivial work.

## Plan Format

When creating a plan, use this format:

```
## Plan: [Task Title]
1. [ ] Step description
2. [ ] Step description
3. [ ] Step description
```

Each step should be:
- Specific and actionable (not vague)
- Scoped to one logical unit of work
- Ordered by dependency (prerequisites first)

## Updating the Plan

- Mark steps `[x]` as they complete
- Mark steps `[-]` if skipped or cancelled with reason
- Mark steps `[/]` if in progress
- Add new steps as scope becomes clear
- Update the plan BEFORE and AFTER every significant action

## Plan Hygiene

- Do NOT create plans with more than 10 steps for a single request
- If a plan would exceed 10 steps, break into phases
- Always include a verification step for code changes
- Always include a commit step for completed work
