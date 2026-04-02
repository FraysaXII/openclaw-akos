# MADEIRA Runtime UX Stabilization Report

**Source plan**: `C:\Users\Shadow\.cursor\plans\madeira_runtime_ux_4745c47a.plan.md`
**Timeline**: 2026-03-31
**Outcome**: **GO** -- Madeira agent live, bootstrap propagation fixed, prompt contract shipped, docs synced
**Author**: MADEIRA (Runtime UX execution)

---

## 1. Executive Summary

The dashboard UX loop for simple HLK lookups was broken because users talked to the Orchestrator (a coordinator that delegates, not answers) and the live runtime never exposed `hlk_*` tools to minimal-profile agents. This stabilization introduced a dedicated **Madeira** agent as the user-facing dashboard entrypoint, fixed the bootstrap tool propagation bug, created a lookup-first prompt contract, and documented the full end-to-end flow.

## 2. Problem Diagnosis

| Root Cause | Impact | Fix |
|------------|--------|-----|
| Dashboard used `orchestrator` session | Orchestrator delegates instead of answering directly | Introduced `madeira` agent as the user-facing entrypoint |
| `_sync_tool_profiles_from_capability_matrix()` preserved old `minimal` allowlists verbatim | `hlk_*` tools never reached the live runtime for orchestrator/architect | Union template allowlist with MCP tools from capability matrix |
| No agent prompt designed for direct factual lookup | Agents fell back to generic prose when tools were available | Created `MADEIRA_BASE.md` with lookup/summary/escalation modes |

## 3. Deliverables

| Commit | Scope | Files Changed |
|--------|-------|---------------|
| `feat(madeira): add dedicated user-facing madeira agent` | Fifth agent in gateway template, capability matrix, workspace scaffold, io.py, model-tiers.json | `config/openclaw.json.example`, `config/agent-capabilities.json`, `config/model-tiers.json`, `akos/io.py`, `scripts/assemble-prompts.py`, `config/workspace-scaffold/madeira/IDENTITY.md` |
| `fix(runtime): propagate HLK tools into live minimal profiles` | Bootstrap now unions template allow + capability matrix MCP tools | `scripts/bootstrap.py` |
| `feat(madeira): add lookup-first prompt contract` | Base prompt with 3 modes + overlay integration | `prompts/base/MADEIRA_BASE.md` |
| `feat(madeira): add dashboard-facing UAT and runtime docs` | Docs sync across 7+ files | `docs/ARCHITECTURE.md`, `docs/USER_GUIDE.md`, `docs/SOP.md`, `docs/uat/hlk_admin_smoke.md`, `CHANGELOG.md`, phase reports |

## 4. Verification Results

| Check | Result |
|-------|--------|
| `py scripts/bootstrap.py --skip-ollama` | 22 PASS, 0 FAIL |
| `py scripts/check-drift.py` | No drift detected |
| `py -m pytest tests/test_hlk.py -v` | 45 passed |
| `py scripts/assemble-prompts.py` | 15 prompts, 0 warnings |
| Live config: orchestrator hlk_* tools | 8 tools present |
| Live config: architect hlk_* tools | 8 tools present |
| Live config: madeira hlk_* tools | 8 tools present |
| JSON validity (all config files) | Valid |

## 5. Runtime Shape After Stabilization

```
User (HLK questions)
    |
    v
MADEIRA  ──── hlk_role, hlk_search, hlk_process_tree, ...
    |
    | (multi-step admin tasks only)
    v
ORCHESTRATOR ──── delegates ──── ARCHITECT / EXECUTOR / VERIFIER
```

## 6. Dashboard UAT Guide

1. Bootstrap: `py scripts/bootstrap.py --skip-ollama`
2. Restart gateway: `openclaw gateway restart`
3. Open Madeira session: `http://127.0.0.1:18789/chat?session=agent:madeira:main`
4. Test queries:
   - "Who is the CTO?" -- expects tool-backed answer with access level 5
   - "Show me all Research roles" -- expects 7 roles from `hlk_area`
   - "What workstreams are under KiRBe Platform?" -- expects graph navigation
   - "Restructure the Finance area" -- expects escalation to Orchestrator

## 7. Rollback

- If Madeira destabilizes existing sessions: keep agent config but switch dashboard default back to orchestrator
- If bootstrap propagation causes broader regression: scope allowlist extension to madeira only
- If prompt routing is unstable: keep runtime/tool fixes and iterate on prompt contract separately

## 8. Next Steps

- Run live browser UAT once gateway is restarted
- Monitor Madeira session telemetry in Langfuse
- Iterate on prompt contract based on real user interaction patterns

## 9. Post-Report Addendum (2026-04-02)

The stabilization work in this report successfully introduced Madeira as the dashboard entry surface, but it did not fully align the live gateway contract with OpenClaw's canonical runtime tool IDs. A follow-up remediation plan now closes that gap across:

- gateway template tool IDs and `alsoAllow` usage
- bootstrap translation behavior
- drift / doctor validation
- five-agent browser and API verification
- Madeira startup hygiene and anti-fabrication UAT

See `madeira-gateway-alignment-remediation-report.md` for the governed remediation evidence and final verification state.
