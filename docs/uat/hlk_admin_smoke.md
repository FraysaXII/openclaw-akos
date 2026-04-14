# HLK Admin Smoke Test Scenarios

**Purpose**: Validate that MADEIRA and the HLK registry endpoints work correctly for common admin tasks.
**Prerequisites**:
- Local OpenClaw gateway reachable (`http://127.0.0.1:18789` returns HTTP 200). If the host just rebooted or the dashboard refuses connections, run `py scripts/doctor.py --repair-gateway` first (see `docs/USER_GUIDE.md` §17 Windows gateway recovery).
- AKOS API running (`py scripts/serve-api.py --port 8420`) and HLK MCP server available.
**GPU note**: If a live GPU lane is in scope for this UAT run, complete [`gpu_provider_unblock_checklist.md`](gpu_provider_unblock_checklist.md) first.

## Scenario 0: Dashboard Entrypoint (MADEIRA agent)

**Goal**: Verify the Madeira agent is accessible and answers HLK questions directly in the dashboard.

| Step | Action | Expected |
|:-----|:-------|:---------|
| 1 | Open `http://127.0.0.1:18789/agents` | Madeira is visible as a distinct agent entry alongside the other 4 agents |
| 2 | Open `http://127.0.0.1:18789/chat?session=agent:madeira:main` or start a fresh Madeira session from `/new` | Madeira loads in WebChat |
| 3 | Start the session and wait for the first ready state | No raw startup-control leakage and no `NO_REPLY` placeholder |
| 4 | Ask: "Who is the CTO?" | Tool-backed answer citing `baseline_organisation.csv`, access level 5, no fabricated UUIDs, and no detour asking whether Madeira should search |
| 5 | Ask: "Show me all Research roles" | Direct answer listing only canonical Research roles; no invented names or placeholder identifiers |
| 6 | Ask: "What workstreams are under KiRBe Platform?" | Graph navigation response containing only canonical workstreams from `process_list.csv` |
| 7 | Ask: "I need to restructure the Finance area" | Madeira acknowledges scope and escalates to Orchestrator |

**Pass criteria**: Steps 4-6 produce grounded answers backed by canonical HLK sources, with no fabricated names, UUIDs, workstreams, leaked internal tool/source strings, or user-facing "should I search?" detours. Step 3 is startup-clean, and Step 7 triggers escalation instead of direct execution.

### Scenario 0 model matrix (multi-lane)

Repeat **steps 3–6** (and spot-check step 7 on one lane) on **at least two** medium-or-above model configurations (for example local `ollama/deepseek-r1:14b` and a cloud or RunPod lane). Use the same canonical prompts per row.

| Model id (example) | Tier / variant | Pass |
|:-------------------|:---------------|:-----|
| | compact / standard / full | Tool use + grounded fields + no fabricated UUIDs + no internal tool leakage |

Document the actual model ids and tiers used in your UAT notes.

**Restart/bootstrap flow** (run these before UAT if config or prompts changed):
```bash
py scripts/bootstrap.py --skip-ollama
py scripts/doctor.py --repair-gateway
```

### Automated parity checks (no WebChat, no browser)

Use these when you want **repo-level** confirmation aligned with Scenario 0 expectations without opening the dashboard or any browser automation:

| Doc expectation (Scenario 0) | Command / test (run from repo root) |
|:-----------------------------|:-------------------------------------|
| Five agents including Madeira | `py -m pytest tests/test_api.py::TestAgents::test_agents_returns_list -v` |
| Madeira policy includes `sequential_thinking` and matches capabilities SSOT | `py -m pytest tests/test_api.py::TestRouting::test_madeira_policy_includes_sequential_thinking -v` |
| Execution/code intents escalate (`execution_escalate`) | `py -m pytest tests/test_intent.py tests/test_api.py::TestRouting::test_classify_execution_route -v` |
| Admin restructure still escalates | `py -m pytest tests/test_api.py::TestRouting::test_classify_admin_route -v` |
| Madeira prompt contract (startup reads, anti-fabrication, HLK ladder) | `py -m pytest tests/validate_prompts.py::TestMadeiraPrompt -v` |
| Log-watcher grounding flags + eval alert wiring | `py -m pytest tests/test_log_watcher.py -v` |
| Assembled prompts within bootstrap char budget | `py scripts/assemble-prompts.py` |
| Full gate before merge | `py scripts/test.py all` and `py -m pytest tests/test_api.py -v` |

Live HLK tool-backed answers (steps 4–6) still require a running gateway, API, and MCP as in **Prerequisites**; the rows above lock **contracts** that prevent the documented failure modes when those services are healthy.

**Order (Lane A, then Lane B):** Run **automated parity + REST** checks above *before* dashboard WebChat so failures are not misread as model or prompt bugs when the real issue is API, MCP, or a non-tool-capable session model. See [Madeira consolidated plan (repo mirror)](../wip/planning/hlk-on-akos-madeira/MADEIRA_HARDENING_CONSOLIDATED_PLAN.md) Part B, subsection *UAT lane ordering*.

### Browser UAT (dashboard WebChat, including Cursor IDE Browser)

Use the same **Scenario 0** steps in a real browser (local Chrome/Edge, Playwright, or **Cursor’s built-in Simple Browser / IDE browser MCP**) when you want end-to-end validation with the live gateway.

- **Tool-capable model required:** If the session model does not support tool calling, the gateway may return an error such as `does not support tools` when Madeira invokes `hlk_*`—steps 4–6 will fail even though pytest contracts pass. For Scenario 0, select a **tool-capable** lane (see `docs/USER_GUIDE.md` — medium+ / instruction-hardened models for tool-heavy Madeira). Example fix: switch the chat model from `deepseek-r1:14b` to a tool-enabled Ollama or cloud id before re-running steps 4–7.
- **Clean session:** Prefer `/new` or a fresh `agent:madeira:*` session so prior chat (including injection tests) does not confuse startup and pass criteria.
- **AKOS API:** For REST-backed checks in [`dashboard_smoke.md`](dashboard_smoke.md) (`GET /health` on port **8420**), run `py scripts/serve-api.py --port 8420` first.

**Execution-layer browser UAT** (full dashboard panels, Playwright harness) remains documented in [`dashboard_smoke.md`](dashboard_smoke.md); run it manually or via `py scripts/browser-smoke.py --playwright` when Playwright is available. Keep **both** pytest parity (above) and browser UAT in your workflow: contracts in CI/dev, browser for operator sign-off on the live stack.

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
| 1 | Call `GET /hlk/search?q=CTO` | Returns status `ok`, ranked candidates, and `best_role.role_name == "CTO"` |
| 2 | Call `GET /hlk/search?q=finance` | Returns Finance roles (CFO, Business Controller, etc.) and finance processes |
| 3 | Ask: "Find everything about MADEIRA in the vault" | Returns MADEIRA-related processes and roles |
| 4 | Call `GET /hlk/search?q=zzzznonexistent` | Returns status "not_found" |

**Pass criteria**: Search returns relevant ranked results, exposes `best_role` / `best_process` when a clear canonical winner exists, and handles not-found gracefully.

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

## Scenario 8: HLK KM manifests and PMO Trello index

**Goal**: Confirm governed Output 1 manifests validate and the PMO backlog registry points at consistent paths (no API required beyond optional file inspection).

| Step | Action | Expected |
|:-----|:-------|:---------|
| 1 | Run `py scripts/validate_hlk.py` | `OVERALL: PASS` |
| 2 | Run `py scripts/validate_hlk_km_manifests.py` | `OVERALL: PASS` for all `docs/references/hlk/v3.0/_assets/**/*.manifest.md` |
| 3 | Open `docs/references/hlk/v3.0/_assets/km-pilot/VISUAL_km_pilot_001.manifest.md` | Frontmatter includes `source_id`, `output_type: 1`, indented `raster:`; body links resolve to `HLK_KM_TOPIC_FACT_SOURCE.md` |
| 4 | Open `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/RESEARCH_BACKLOG_TRELLO_REGISTRY.md` | Rows use 24-character hex `trello_card_id` values; wip synthesis links target `docs/wip/hlk-km/research-synthesis-*.md` |
| 5 | Open `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/imports/README.md` | Describes primary vs archive JSON slices; registry maintenance uses **primary** export |

**Pass criteria**: Both validators pass; spot-checks show contract links and registry ids aligned with [imports/trello_board_67697e19_primary.json](../references/hlk/v3.0/Admin/O5-1/Operations/PMO/imports/trello_board_67697e19_primary.json).

---

## Rollback Guide

If any HLK-specific behavior is broken:

1. Check the canonical CSVs are parseable: `py scripts/test.py hlk`
2. Restart the API to reload the registry: `py scripts/serve-api.py --port 8420`
3. Check process integrity: `GET /hlk/gaps`
4. If the registry fails to load, check `baseline_organisation.csv` and `process_list.csv` for CSV formatting errors
