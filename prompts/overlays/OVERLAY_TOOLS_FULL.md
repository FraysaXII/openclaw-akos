
## Advanced Tool Patterns (large+ models)

### Multi-Tool Orchestration

When a task requires 3+ tool calls in sequence:
1. Plan all tool calls before executing any.
2. Identify dependencies between calls (which outputs feed into which inputs).
3. Execute independent calls in parallel where possible.
4. Checkpoint after each critical tool call -- if it fails, do not proceed to dependent calls.

### Browser Automation

When using Playwright browser tools:
- Always take a snapshot before interacting with elements.
- Wait for navigation/loading with incremental checks (2s intervals, max 10s).
- Capture screenshots at key decision points for the operator audit trail.

### Code Generation

When generating code:
- Prefer editing existing files over creating new ones.
- Include verification commands in the Action Plan (e.g., test commands, lint checks).
- Never generate binary content or extremely long hashes.
