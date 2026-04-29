# `artifacts/probes/` — operator-pasted probe results

This directory holds the **JSON results** the operator pastes back from MCP / SQL probes. Files are **operator-local and dated**; they are **gitignored** (`.gitignore` allows only this README) so that stale snapshots never leak into git history.

## Currently used by

### Initiative 23 P4 — Compliance mirror drift probe

Workflow ([`scripts/probe_compliance_mirror_drift.py`](../../scripts/probe_compliance_mirror_drift.py)):

```bash
# 1. Emit the JSON-shaped SELECT
py scripts/probe_compliance_mirror_drift.py --emit-sql

# 2. Run the printed SQL via user-supabase MCP `execute_sql` (service_role)

# 3. Save the JSON result here, dated:
#    artifacts/probes/mirror-drift-<YYYYMMDD>.json
#    Format:  [ {"table_name": "<key>", "row_count": "<int>"}, ... ]

# 4. Verify
py scripts/probe_compliance_mirror_drift.py --verify
# or via the verify profile:
py scripts/verify.py compliance_mirror_drift_probe
```

`--verify` (the default mode) reads the most recent file matching `mirror-drift-*.json`, compares against canonical CSV row counts, and reports row-by-row PASS/FAIL. **SKIPs gracefully (exit 0) when no fresh artifact exists** — CI never goes red on a probe operators have not refreshed.

## SOC

- The JSON files are operator-local; they are **never committed** so stale row-counts do not pollute history or trigger false CI signals.
- `--emit-sql` does not include credentials. The operator runs the SQL inside their authenticated MCP session.
- `--verify` reads only the locally-pasted JSON; it never connects to the database.

## Cross-references

- [`scripts/probe_compliance_mirror_drift.py`](../../scripts/probe_compliance_mirror_drift.py)
- Verify profile: `compliance_mirror_drift_probe` in [`config/verification-profiles.json`](../../config/verification-profiles.json)
- Operator SQL gate: [`akos-holistika-operations.mdc`](../../.cursor/rules/akos-holistika-operations.mdc) §"Operator SQL gate"
- Wave-2 plan §"Initiative 23 P4": `~/.cursor/plans/hlk_scalability_wave_2_initiatives_639a02d7.plan.md`
