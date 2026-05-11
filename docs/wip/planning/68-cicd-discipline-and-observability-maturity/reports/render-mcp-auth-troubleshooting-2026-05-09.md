---
linked_initiative: I68
date: 2026-05-09
status: cleared
status_history:
  - 2026-05-09 operator_action_required (filed)
  - 2026-05-10 cleared (operator confirmation)
kind: mcp_auth_troubleshooting
server: plugin-render-render
closure_decision: D-IH-68-K (Round 2 plan acceptance includes Render unblock confirmation)
last_review: 2026-05-10
---

> **2026-05-10 closure note (Round 2 plan).** The Render MCP `unauthorized` blocker described below is **CLEARED**. Operator confirmation received during the I68 Round-2 plan review. Effects on the I68 roadmap:
>
> - **P4** (Sentry deploy-health telemetry) and **P5** (CI baseline) now include `kirbe-platform` (Render-hosted) in their main paths from day 1 — no deferred P4b / P5b slices.
> - The proposed `OPS-68-1` Render-discovery action is **withdrawn** (not minted to `OPS_REGISTER.csv`).
> - **R-IH-68-11** in the plan's earlier draft ("Render MCP persists") is **dropped**; replaced by R-IH-68-11 NEW (InfraMonitor module-namespace prematurely couples with future SaaS multi-tenancy — see [`risk-register.md`](../risk-register.md)).
> - Phase-dependency mermaid in [`master-roadmap.md`](../master-roadmap.md) §3 is simplified (no Render-gating node).
> - Calendar effect: **zero** — the parallelism in the original plan absorbed the Render slice without slipping critical path.
>
> The original troubleshooting body below is preserved as historical reference and as the runbook to consult if the Render MCP credential expires / rotates again in the future.

# Render MCP Auth Troubleshooting — 2026-05-09 (CLEARED 2026-05-10)

## Current observed state

The Render MCP is reachable from Cursor, but the API credential/session is not accepted by the MCP server:

| Tool | Result | Interpretation |
|:---|:---|:---|
| `plugin-render-render.list_workspaces({})` | `unauthorized` | The MCP cannot authenticate to Render at all. |
| `plugin-render-render.get_selected_workspace({})` | `no workspace set. Prompt the user to select a workspace.` | Workspace selection has not occurred, but selection cannot happen until `list_workspaces` authenticates. |
| `plugin-render-render.list_services({})` | not attempted after latest auth failure | Would not work until a workspace is selected. |

This is **not** currently a "wrong workspace selected" problem. It is an authentication/session propagation problem.

## Why Cursor UI can say "logged in" while tools return `unauthorized`

Cursor MCP auth state has at least two layers:

1. **Cursor plugin UI state** — the UI can know that the plugin has been configured or that an OAuth flow was started/completed.
2. **MCP server runtime credential state** — the server process actually receives a valid Render credential and can call Render's API.

If those drift, the UI can look healthy while tool calls return `unauthorized`. Cursor's own MCP guidance notes that integrations can require multiple attempts and that **Reload server** is often needed after authorization/config changes.

## Most likely causes

1. **MCP server not reloaded after `mcp.json` edit.**  
   Editing the plugin `mcp.json` does not guarantee the already-running MCP server process sees the new environment/token.

2. **Credential pasted into the wrong config layer.**  
   Some Cursor MCP plugins use marketplace-managed auth; some use env vars inside `mcp.json`. If the plugin uses marketplace auth, manually pasting a key into a different local JSON may not affect the running server.

3. **Token has the wrong scope / expired / revoked.**  
   Render API keys can be valid for browser UI but not valid for API calls if the key is stale or not attached to the correct workspace/org account.

4. **Multiple Render MCP servers available.**  
   This workspace has `plugin-render-render` available. If a second Render MCP is installed elsewhere, the UI might show one plugin as logged in while the agent calls a different server identifier.

5. **Workspace selection required after auth.**  
   Once `list_workspaces` works, the agent must still ask the operator which workspace to select, then call `select_workspace(ownerID)`. The schema explicitly warns not to select automatically because it can affect destructive operations.

## Recovery checklist

Please perform these in order, then ask the agent to re-test:

1. **Cursor Settings → MCP → Render plugin → Reload server.**  
   This is the most likely missing step after editing `mcp.json`.

2. If reload does not work, **Disable → Enable** the Render MCP plugin.

3. If still unauthorized, **re-authenticate / reconnect** the Render plugin from Cursor's MCP UI.

4. If the plugin expects an API key:
   - Go to <https://dashboard.render.com/u/settings#api-keys>
   - Create a fresh API key.
   - Paste it into the Render MCP plugin's expected config field.
   - Reload the Render MCP server again.

5. Ask the agent to run:

   ```text
   plugin-render-render.list_workspaces({})
   ```

   Expected: list of workspaces with owner IDs.

6. The agent will then ask which workspace to select and only then call:

   ```text
   plugin-render-render.select_workspace({ "ownerID": "<operator-selected-owner-id>" })
   plugin-render-render.list_services({ "includePreviews": true })
   ```

## What the agent can do after Render MCP auth works

1. List all services and identify the KirBe backend service.
2. List last 5 deploys for each relevant service.
3. Pull build/runtime logs for failed deploys.
4. Report deploy duration + error patterns.
5. Add Render service health to I68's deploy-health evidence.

## Current blocker

Render backend inspection is blocked until `list_workspaces({})` no longer returns `unauthorized`.

