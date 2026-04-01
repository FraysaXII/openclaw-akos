# Workflow: HLK Admin

## Agent Sequence
1. **Orchestrator** -- receives admin request, delegates appropriately
2. **Architect** -- queries HLK registry, analyses gaps, produces action plan
3. **Executor** -- implements approved changes to vault CSVs or documentation
4. **Verifier** -- validates changes against baseline integrity rules

## Required Tools
- `hlk_role`, `hlk_role_chain`, `hlk_area`, `hlk_process`, `hlk_process_tree`
- `hlk_projects`, `hlk_gaps`, `hlk_search`
- `read_file`, `write_file` (for vault CSV and markdown edits)
- `sequential_thinking` (for multi-step governance reasoning)

## Approval Points
- Before any edit to `baseline_organisation.csv` or `process_list.csv`
- Before creating or modifying any SOP document
- Before changing compliance taxonomy documents

## Steps
1. [ ] Orchestrator identifies the admin task (role update, process addition, gap remediation, etc.)
2. [ ] Architect queries the HLK registry to understand current state
3. [ ] Architect produces a change proposal with specific field values and rationale
4. [ ] Operator reviews and approves the proposal
5. [ ] Executor applies the changes to the canonical vault files
6. [ ] Verifier checks: no broken parent refs, no orphans, no duplicate IDs, role_owner resolves
7. [ ] Executor fixes any verification failures
8. [ ] Final integrity check against baseline_organisation.csv and process_list.csv

## Completion Criteria
- All proposed changes applied and verified
- 0 broken parent references in process_list.csv
- 0 orphan items (non-project rows without item_parent_1)
- All role_owner values resolve against baseline_organisation.csv
- PRECEDENCE.md governance rules respected
- Changes documented in the relevant Phase report
