# Trello list name → canonical English workstream (`item_name`)

**Evidence:** [trello_board_67697e19_archive_slice.json](../../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/imports/trello_board_67697e19_archive_slice.json), [trello_board_67697e19_primary.json](../../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/imports/trello_board_67697e19_primary.json) (`list.name`).

**Status columns (not registry parents):** `Done`, `Viejo` — workflow only; no `process_list` parent rows.

**Tier C (excluded from CSV merge):** `To Do`, `ToDo` — intake stays in Trello/WIP per USER_GUIDE §24.3.2.

| Trello `list.name` | Canonical English `item_name` | `item_granularity` | Parent project (`item_parent_1`) |
|--------------------|------------------------------|-------------------|-------------------------------------|
| Research Material | Research material and learning pipelines | workstream | Holistika Research and Methodology |
| MADEIRA Project | (split across MADEIRA workstreams below; no list-named parent) | — | MADEIRA Platform |
| Darnos a conocer | Brand presence and messaging | workstream | Think Big Channel and Marketing Operations |
| Crecer equipo | Team growth and talent pathways | workstream | Holistika People and Organisational Development |
| Salir a mercado | Go-to-market and entity readiness | workstream | Think Big Operational Excellence |
| Definir servicios | Service catalog and capability definition | workstream | Think Big Operational Excellence |
| Controlar la empresa | Operating model and internal controls | workstream | Think Big Operational Excellence |

**MADEIRA sub-buckets** (from card clusters / `item_parent_1` paths in candidate CSV; all workstreams under **MADEIRA Platform**):

| Cluster signal | Canonical English `item_name` |
|----------------|--------------------------------|
| Research - Topics on Radar, Political, Activism, Social, Technology, Legal, Economics | MADEIRA research radar topics |
| PMO - Product Owner, Planning Phase, Product Timeline, Sales Tools | MADEIRA product planning and PO timeline |
| Product Owner - UX, Capabilities, Persona, Use Cases, MADEIRA Components, KirBe Components | MADEIRA UX capability definitions |
| DevOps, CICD, Pipeline, LlamaIndex, Code Structure, module paths | MADEIRA DevOps and CI/CD delivery |
| Benchmarker, AI Ethics | MADEIRA benchmarking and AI ethics |

**Pipeline subprocess:** `Research Material / Pipeline` → intermediate **process** `Research material pipeline execution` under `Research material and learning pipelines` for the six pipeline tasks.

## Pattern 2 (cluster layer)

After the initial merge, **bulk Trello-derived tasks** are grouped under deterministic English **cluster** `process` rows (`item_id` prefix `gtm_cl_*`). Each cluster is keyed by the canonical **workstream** `item_name` plus the original Trello `item_parent_1` path from `candidate_gtm_process_rows.csv` (stable hash suffix in `item_id`).

| Registry column | Value for leaf tasks / processes |
|-----------------|----------------------------------|
| `item_parent_1` | Cluster `item_name` (immediate parent) |
| `item_parent_2` | Owning workstream `item_name` |
| Cluster row `item_parent_1` | Workstream |
| Cluster row `item_parent_2` | Owning project (`Holistika Research and Methodology`, `MADEIRA Platform`, Think Big projects, etc.) |
| Workstream row `item_parent_1` / `item_parent_2` | Both set to the owning **project** (same convention as other Holistika/Think Big workstreams) |

**Pipeline exception:** the six pipeline tasks attach directly to **`Research material pipeline execution`** (no extra `gtm_cl_*` row) with `item_parent_2` = `Research material and learning pipelines`.

**Sanitization:** code-like symbols (snake_case APIs, `.py` paths, HTTP route fragments) are moved into `description` / `addundum_extras`; registry `item_name` stays short English prose. Driver: `py scripts/refine_gtm_process_hierarchy.py --write`.

