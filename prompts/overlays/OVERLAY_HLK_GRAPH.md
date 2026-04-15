# HLK optional Neo4j graph (mirrored index)

These tools apply only when the Neo4j mirror is configured (`NEO4J_*` in `~/.openclaw/.env`). The graph is **derived** from canonical CSVs and validated vault links — never authoritative over `baseline_organisation.csv` or `process_list.csv`.

## Tool ladder (graph)

1. After you have a canonical `item_id` or `role_name` from `hlk_process` / `hlk_search` / `hlk_role`, you may use `hlk_graph_process_neighbourhood` or `hlk_graph_role_neighbourhood` for **multi-hop** relationship questions only.
2. Use `hlk_graph_summary` for **operator-style diagnostics** (counts), not for ordinary factual lookups.

## Protocol alignment (with OVERLAY_HLK)

- Optional **mirrored** Neo4j graph: neighbourhood tools only after canonical ids or role names are known from registry tools.
- Final citations must still name `process_list.csv` or `baseline_organisation.csv`, not Neo4j.

## Allowed tools (graph subset)

When your role allowlists them:

- `hlk_graph_summary` — optional Neo4j mirror diagnostics (counts only)
- `hlk_graph_process_neighbourhood` — optional bounded multi-hop graph around a canonical `item_id`
- `hlk_graph_role_neighbourhood` — optional bounded graph around a canonical `role_name`

## Citations

- Cite canonical asset names only. Never cite `hlk_role`, `hlk_search`, `hlk_graph_*`, `best_role`, or the raw query string in the final answer.
