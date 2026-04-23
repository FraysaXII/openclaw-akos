# PMO Trello board imports (reference-only)

**Board ID:** `67697e19c67277de7ae1a85c`  
**Purpose:** Snapshot exports for reconciling [RESEARCH_BACKLOG_TRELLO_REGISTRY.md](../RESEARCH_BACKLOG_TRELLO_REGISTRY.md). **Not canonical business prose** — the registry markdown is the governed index; JSON is evidence.

## Files

| File | Contents |
|------|----------|
| `trello_board_67697e19_primary.json` | **Authoritative slice for registry maintenance** — first 73 cards from the combined export (ids `676993…` / `676992…` lists used in the PMO registry table). |
| `trello_board_67697e19_archive_slice.json` | Second concatenated slice from the same source file (ids `67698d…` prefix). Older or alternate export pass; **do not** mix ids across slices when editing the registry. |
| `trello_board_67697e19_full_formatted.json` | Original combined export as delivered (148 cards). Kept for audit; prefer **primary** when looking up card ids for new rows. |

## Refresh procedure

1. Export the board in the same JSON shape (array of card objects with `id`, `name`, `list.name`).
2. If the export is a single consistent id namespace, replace `trello_board_67697e19_primary.json` (or split using the same rule: second `"Readme"` card starts archive slice if two exports were concatenated).
3. Update [RESEARCH_BACKLOG_TRELLO_REGISTRY.md](../RESEARCH_BACKLOG_TRELLO_REGISTRY.md) and add a one-line note to `docs/wip/planning/03-hlk-km-knowledge-base/reports/` if history is material.

## Security

Exports may contain links or notes. Treat as **internal**; redact before wider distribution if needed.
