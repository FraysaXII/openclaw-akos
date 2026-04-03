
## Startup Compliance (medium+ models)

### Recency Rule

If you have not called `read` on your workspace startup files within your
last 5 messages, you MUST re-read them before continuing. Context compaction
may have evicted their contents. This is the #1 cause of audit warnings.

### Invariant

For every turn where you use any tool: verify you have read your startup files
in this session. If not, read them FIRST, then proceed with the requested action.
If dated continuity notes such as `memory/YYYY-MM-DD.md` exist, re-read the newest one or two after `MEMORY.md`.

### What NOT to do

BAD: "I've restored the workflow protocols and memory logs." (without actually calling read)
BAD: Responding to a user message before reading startup files after a context reset.
GOOD: [silent read calls, including dated continuity notes if present] -> then respond to user naturally.
