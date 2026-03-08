# Research Protocol

When performing research, codebase analysis, or planning tasks:

## Source Usage

1. Use `list_directory` and `read_file` (filesystem MCP) for local codebase exploration.
2. Use GitHub MCP (`git_status`, `git_diff`, `git_log`) for repository history and structure.
3. Use `fetch` MCP for external documentation when URLs are provided.
4. Use `sequential_thinking` for multi-step reasoning before conclusions.

## Citation Requirements

For planning, research, and compliance outputs:
- Cite source origin (repo file, external URL, memory entry, or inference).
- Cite freshness (when was this information last verified).
- Distinguish facts from inferences: prefix facts with [FACT] and inferences with [INFERENCE].
- When confidence is below 80%, explicitly state the uncertainty.

## Context Efficiency

- Start with the narrowest scope that answers the question.
- Expand scope incrementally only when initial results are insufficient.
- Summarize findings before presenting -- do not dump raw tool output.
- Pin critical context (task brief, key files, constraints) early and reference throughout.
