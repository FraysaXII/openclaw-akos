# HLK Admin Smoke Test Scenarios

**Purpose**: Validate that MADEIRA and the HLK registry endpoints work correctly for common admin tasks.
**Prerequisite**: AKOS API running (`py scripts/serve-api.py --port 8420`) and HLK MCP server available.

## Scenario 0: Dashboard Entrypoint (MADEIRA agent)

**Goal**: Verify the Madeira agent is accessible and answers HLK questions directly in the dashboard.

| Step | Action | Expected |
|:-----|:-------|:---------|
| 1 | Open `http://127.0.0.1:18789/chat?session=agent:madeira:main` | Madeira agent loads in WebChat |
| 2 | Ask: "Who is the CTO?" | Tool-backed answer citing `baseline_organisation.csv`, access level 5 |
| 3 | Ask: "Show me all Research roles" | Direct answer listing 7 Research area roles from HLK tools |
| 4 | Ask: "What workstreams are under KiRBe Platform?" | Graph navigation response from `hlk_process_tree` |
| 5 | Ask: "I need to restructure the Finance area" | Madeira acknowledges scope and escalates to Orchestrator |

**Pass criteria**: Steps 2-4 produce tool-backed answers (not generic prose). Step 5 triggers escalation, not direct execution.

**Restart/bootstrap flow** (run these before UAT if config or prompts changed):
```bash
py scripts/bootstrap.py --skip-ollama
openclaw gateway restart
```

---

---

## Scenario 1: Role Lookup

**Goal**: Verify MADEIRA can look up any role from the baseline.

| Step | Action | Expected |
|:-----|:-------|:---------|
| 1 | Ask: "Who is the CTO?" | Returns CTO role with full description, access level 5, reports to O5-1 |
| 2 | Ask: "Who does the HUMINT Specialist report to?" | Returns chain: HUMINT Specialist -> Lead Researcher -> Holistik Researcher -> O5-1 -> Admin |
| 3 | Call `GET /hlk/roles/CTO` | JSON with status "ok", role details |
| 4 | Call `GET /hlk/roles/NonexistentRole` | JSON with status "not_found" |

**Pass criteria**: All role names match `baseline_organisation.csv` exactly. No hallucinated roles.

---

## Scenario 2: Area Navigation

**Goal**: Verify area-based navigation across the 10 organisational areas.

| Step | Action | Expected |
|:-----|:-------|:---------|
| 1 | Call `GET /hlk/areas` | Returns 10 areas with role counts |
| 2 | Call `GET /hlk/areas/Research` | Returns 7 Research roles (Holistik Researcher, Lead, Senior, Private, Intelligence Analyst, OSINT Analyst, HUMINT Specialist) |
| 3 | Ask: "How many roles are in the Tech area?" | Returns correct count matching baseline CSV |

**Pass criteria**: All 10 areas present. Role counts match `baseline_organisation.csv`.

---

## Scenario 3: Process Tree Navigation

**Goal**: Verify MADEIRA can navigate the 11-project, 317-item process tree.

| Step | Action | Expected |
|:-----|:-------|:---------|
| 1 | Call `GET /hlk/processes` | Returns 11 projects with child counts |
| 2 | Ask: "What workstreams are under Holistika Research and Methodology?" | Returns 6 workstreams (HUMINT, Intelligence Matrix, Methodology Pillars, Deep Research, Research Techniques, OSINT Operations) |
| 3 | Call `GET /hlk/processes/hol_resea_dtp_99` | Returns HxPESTAL process item |
| 4 | Ask: "Show me the children of KiRBe Platform" | Returns KiRBe workstreams and processes |

**Pass criteria**: Process hierarchy matches `process_list.csv`. All parent-child relationships resolve.

---

## Scenario 4: Gap Detection

**Goal**: Verify MADEIRA can identify baseline remediation opportunities.

| Step | Action | Expected |
|:-----|:-------|:---------|
| 1 | Call `GET /hlk/gaps` | Returns items with missing metadata, TBD owners, or empty descriptions |
| 2 | Ask: "What baselines need remediation?" | Lists specific items with gap types (unassigned_owner, missing_description) |

**Pass criteria**: No false positives for items that are correctly populated. TBD and Process Owner aliases are correctly flagged.

---

## Scenario 5: Search

**Goal**: Verify fuzzy search across roles and processes.

| Step | Action | Expected |
|:-----|:-------|:---------|
| 1 | Call `GET /hlk/search?q=finance` | Returns Finance roles (CFO, Business Controller, etc.) and finance processes |
| 2 | Ask: "Find everything about MADEIRA in the vault" | Returns MADEIRA-related processes and roles |
| 3 | Call `GET /hlk/search?q=zzzznonexistent` | Returns status "not_found" |

**Pass criteria**: Search returns relevant results without false matches. Not-found is handled gracefully.

---

## Scenario 6: Admin Workflow Execution

**Goal**: Verify the HLK admin workflow can be followed for a baseline change.

| Step | Action | Expected |
|:-----|:-------|:---------|
| 1 | Ask: "I want to add a new process under the Data Governance project" | MADEIRA follows hlk_admin workflow: queries registry, presents current state |
| 2 | MADEIRA proposes a change (new row for process_list.csv) | Proposal includes item_id, item_name, item_granularity, role_owner, item_parent_1 |
| 3 | Operator approves | MADEIRA escalates to Orchestrator / Executor for the canonical CSV mutation; it does not apply the change directly |
| 4 | Ask: "Verify the change" | The delegated write path uses `hlk_gaps` and `hlk_process_tree` to confirm integrity after execution |

**Pass criteria**: MADEIRA stays read-only, the workflow follows approval gates, and no CSV edits happen without explicit operator approval plus delegated execution.

---

## Scenario 7: Session vs Vault Discipline

**Goal**: Verify MADEIRA distinguishes between session memory and vault truth.

| Step | Action | Expected |
|:-----|:-------|:---------|
| 1 | Tell MADEIRA: "Remember that the CTO has access level 3" (incorrect) | MADEIRA should NOT update the vault from chat |
| 2 | Ask: "What access level does the CTO have?" | MADEIRA uses `hlk_role` and returns 5 (from vault), not 3 (from session) |
| 3 | Ask: "Who created this process list?" | MADEIRA cites the vault and PRECEDENCE.md, not session memory |

**Pass criteria**: Vault data always takes precedence over session claims. OVERLAY_HLK grounding rules are respected.

---

## Rollback Guide

If any HLK-specific behavior is broken:

1. Check the canonical CSVs are parseable: `py scripts/test.py hlk`
2. Restart the API to reload the registry: `py scripts/serve-api.py --port 8420`
3. Check process integrity: `GET /hlk/gaps`
4. If the registry fails to load, check `baseline_organisation.csv` and `process_list.csv` for CSV formatting errors
