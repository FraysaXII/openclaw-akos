# Workflow Invocation Protocol

## Recognizing Workflow Requests

When the user's message matches a known workflow pattern, invoke the corresponding workflow:

| User Signal | Workflow | Action |
|:------------|:---------|:-------|
| "analyze this repo", "codebase analysis" | `analyze_repo` | Delegate to Architect for full analysis |
| "implement", "build", "add feature" | `implement_feature` | Architect plans, Executor builds, Verifier checks |
| "verify", "check", "test" | `verify_changes` | Delegate to Verifier |
| "browser smoke", "dashboard test" | `browser_smoke` | Verifier runs browser scenarios |
| "deploy check", "ready to ship?" | `deploy_check` | Architect + Verifier readiness assessment |
| "incident review", "what went wrong" | `incident_review` | Architect root cause, Orchestrator remediation |

## Workflow Execution

When executing a workflow:
1. Announce the workflow name and agent sequence.
2. Follow the steps defined in `config/workflows/<name>.md`.
3. Report completion or failure at each step.
4. Produce a summary at the end.

## Custom Workflows

Users can create custom workflows by adding `.md` files to `config/workflows/` following the existing format.
