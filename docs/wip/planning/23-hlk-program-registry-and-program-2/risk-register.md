# Initiative 23 — Risk Register

Per Wave-2 plan §"Wave-2 initiative-standard artifacts" — risk-register is now a standard P0 deliverable for every Wave-2 initiative.

## Active risks

| ID | Description | Mitigation | Owner | Status |
|:---|:-----------|:-----------|:-----:|:------:|
| **PR-23-1** | Forward-reference cycle introduced when seeding `consumes_program_ids` edges (e.g. A→B→A). Validator must catch before commit. | DAG cycle-detection in `scripts/validate_program_registry.py` (Tarjan or simple DFS); reject with explicit error path. Test coverage for cycles in `tests/test_validate_program_registry.py`. | Agent (P1) | OPEN |
| **PR-23-2** | `program_code` collision at seed time (e.g. two programs both `OPS`). | Validator enforces uniqueness with explicit error pointing at conflicting rows. YAML pre-fills proposed codes; operator flips on review. | Agent (P1) | OPEN |
| **PR-23-3** | Mirror drift if seed sha differs from canonical at MCP apply time (Initiative 22 P7 ledger-rename precedent). | Pin source sha in upsert SQL header; row-count probe after apply; rename local migration filenames to match remote `schema_migrations` ledger if MCP issues new timestamps. | Agent (P2) | OPEN |
| **PR-23-4** | Neo4j projection edge collision with existing `:PARENT_OF` (process→process) when adding program parent edges. | Use `:PROGRAM_PARENT_OF` (D-IH-18); validator-time assertion in `akos/hlk_graph_model.py` `EdgeType` enum prevents reuse. | Agent (Pgraph) | OPEN |
| **PR-23-5** | Operator never reviews agent-defaulted Tier-3 cells; defaults silently become permanent. | D-IH-23-A trigger sets review-by date 2026-05-15. Defaults annotated inline in YAML with `# agent default — operator review`. P0.5 phase report tracks confirmation count. Drift probe surfaces stale `start_date` anomalies (e.g. all rows = 2026-01-01 placeholder). | Operator | OPEN |
| **PR-23-6** | KiRBe onboarding (P6) creates 6 program-folder READMEs; if Compliance/Legal/Marketing is later required, on-demand creation lacks consistency. | D-IH-16 codifies "evidence-based" rule + 3 on-demand roots are explicitly listed. P0.5 YAML Section 4 `has_paying_customers_today` flips Compliance/Legal urgency. | Agent (P6) | OPEN |
| **PR-23-7** | `--allow-forward-references` escape hatch becomes a habit (always-on) instead of single-commit. | Validator emits a one-line warning when the flag is used; reviewer enforces "next commit MUST clear" via PR description checklist. CI grep for the flag in committed scripts blocks. | Operator + Agent | OPEN |
| **PR-23-8** | Neo4j unavailable in CI; graph projection silently skips and drift goes unnoticed. | `sync_hlk_neo4j_dry_run_smoke` verify profile asserts the parity-assert pass on Program builders even without Bolt; SKIP only when driver lib missing, not silently. | Agent (Pgraph) | OPEN |

## Closed risks

(none yet)

## Re-evaluation cadence

- **Quarterly review** of all OPEN risks.
- **Per-phase entry** for new risks discovered during execution.
- **Closure** requires linking to evidence (mitigation in place + verified).

## Cross-references

- Wave-2 plan §"Risk and rollback"
- [`akos-governance-remediation.mdc`](../../../../.cursor/rules/akos-governance-remediation.mdc) §"Strict verification matrix"
- Initiative 22 closure note (precedent for risk-register-style documentation)
