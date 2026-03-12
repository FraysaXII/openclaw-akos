
## Startup Compliance (medium+ models)

### Recency Rule

If you have not called `read_file` on your workspace startup files within your
last 5 messages, you MUST re-read them before continuing. Context compaction
may have evicted their contents. This is the #1 cause of audit warnings.

### Invariant

For every turn where you use any tool: verify you have read your startup files
in this session. If not, read them FIRST, then proceed with the requested action.

### What NOT to do

BAD: "I've restored the workflow protocols and memory logs." (without actually calling read_file)
BAD: Responding to a user message before reading startup files after a context reset.
GOOD: [silent read_file calls] -> then respond to user naturally.
