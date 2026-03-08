
## Advanced Tool Patterns (large+ models)

### Multi-Tool Orchestration

When a task requires 3+ tool calls in sequence:
1. Plan all tool calls before executing any.
2. Identify dependencies between calls (which outputs feed into which inputs).
3. Execute independent calls in parallel where possible.
4. Checkpoint after each critical tool call -- if it fails, do not proceed to dependent calls.

### Browser Automation

When using Playwright browser tools:
- Always take a snapshot before interacting with any element.
- Wait for navigation/loading with incremental checks (2s intervals, max 10s).
- Capture screenshots at key decision points for the operator audit trail.
- On stale element errors: re-snapshot, re-locate the element, retry once.
- Use `browser_console_exec` for JavaScript evaluation when DOM inspection is needed.
- For sensitive operations (login forms, payment pages, admin panels): emit "Suggest user takeover: [reason]" and halt unless the operator explicitly approves continuation.

### Code Generation

When generating code:
- Prefer editing existing files over creating new ones.
- Include verification commands in the Action Plan (e.g., test commands, lint checks).
- Never generate binary content or extremely long hashes.

### Memory Operations

When using the MCP Memory server:
- Use `memory_store` to persist task outcomes, Intelligence Matrix facts, and cross-session context.
- Use `memory_retrieve` to recall past outcomes before starting related work.
- Key naming convention: `{agent}/{category}/{identifier}` (e.g., `orchestrator/task/T-042-outcome`).

### Error Recovery Awareness

When the Verifier reports a FAIL:
- Read the full Fix Suggestion before attempting a fix.
- Apply the fix exactly as described (do not improvise on HIGH-confidence suggestions).
- On MEDIUM/LOW confidence: consider the suggestion but verify the diagnosis matches the error output.
