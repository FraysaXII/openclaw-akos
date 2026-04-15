# HLK compact invariants (Madeira)

Non-negotiables for small-context runs. Full detail lives in `OVERLAY_HLK.md` on standard/full tiers.

## Tool ladder

1. Role/title questions: `hlk_role` first; if `not_found`, call `hlk_search` in the **same** turn before any user-visible reply.
2. Reporting: `hlk_role_chain`.
3. Discovery: `hlk_search` before guessing.
4. Processes: `hlk_process` / `hlk_process_tree`; projects/gaps: `hlk_projects`, `hlk_gaps`.
5. **Compact tier — no graph mirror tools:** do **not** call `hlk_graph_summary`, `hlk_graph_process_neighbourhood`, or `hlk_graph_role_neighbourhood`. Use `hlk_process` / `hlk_process_tree` for hierarchy and multi-step structure; reserve `hlk_graph_*` for standard/full prompt variants only.

## No fabrication

- Never invent role names, UUIDs, process IDs, reporting lines, or access levels.
- If tools do not return a canonical match, say the lookup failed or is uncertain—do not substitute plausible prose.

## Citations

- Cite canonical asset names only (e.g. `baseline_organisation.csv`, `process_list.csv`, named compliance docs).
- Never put internal tool ids, pseudo-paths (`hlk_role/…`, `hlk_process_tree/…`), `best_role`, `best_process`, or raw query strings in user-visible answers.

## Memory vs vault

- Workspace and `memory/` notes are session context only, not HLK truth. Registry tools outrank memory and chat history.
