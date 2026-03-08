
## Context Window Management (large+ models)

### Compression Protocol

When the context window approaches 60% capacity:

1. **Summarize completed actions** -- replace detailed tool outputs with 1-sentence summaries.
2. **Preserve priority content** in this order:
   - Active Plan Document or Delegation Plan (never compress)
   - Current task context and recent errors
   - Recent actions (last 5)
   - Older actions (summarize to 1 line each)
3. **Never compress**: the active Handoff Summary, IDENTITY.md content, or HITL gate specifications.

### Multi-Task Context

When working on multiple tasks concurrently:
- Keep the full context for the active task.
- Keep only the summary (Task ID, status, last outcome) for paused tasks.
- When switching tasks, emit: "Switching to T-{ID}: {1-sentence context reload}."
