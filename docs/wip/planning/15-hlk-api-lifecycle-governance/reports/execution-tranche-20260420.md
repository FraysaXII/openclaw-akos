# Execution report — HLK API lifecycle + component matrix (2026-04-20)

## Operator verification

| Gate | Result |
|------|--------|
| `py scripts/validate_hlk.py` | PASS (includes COMPONENT_SERVICE_MATRIX) |
| `py scripts/backfill_process_parent_ids.py --write` | PASS (0 holes) |
| Process items count | 1077 |

## Process tree — `GET /hlk/process-tree-by-parent-id` (runtime check)

**Parent `env_tech_ws_api_1`:** direct child `env_tech_dtp_306` (HLK API lifecycle and portfolio governance).

**Parent `env_tech_dtp_306`:** children `env_tech_dtp_307`, `308`, `309`, `311`, `312` (five items). Matches planned edge set.

## Component matrix

- **Rows:** 97 (from Matriz *components* sheet)
- **Validator:** `scripts/validate_component_service_matrix.py`

## Artifacts touched (summary)

- `docs/references/hlk/compliance/COMPONENT_SERVICE_MATRIX.csv` (new)
- `docs/references/hlk/compliance/process_list.csv` (+8 rows, instruction updates)
- `docs/references/hlk/compliance/PRECEDENCE.md`
- `akos/hlk_component_service_csv.py`, `scripts/validate_component_service_matrix.py`, `scripts/ingest_matriz_componentes_to_matrix.py`
- `scripts/validate_hlk.py` (invokes matrix validator)
- Vault SOPs under `docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/`
- `REPOSITORIES_REGISTRY.md` + `Repositories/README.md`
- `docs/USER_GUIDE.md`, `docs/ARCHITECTURE.md`, `docs/DEVELOPER_CHECKLIST.md`, `CHANGELOG.md`
- `requirements.txt` (`openpyxl`)
- Removed repo-root `Matriz componentes.xlsx`

## Operator approval

Tranche executed in development workspace per user request; formal operator sign-off line can be appended when PMO/CTO reviews CSV diffs in production workflow.
