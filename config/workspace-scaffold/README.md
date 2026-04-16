# Workspace Scaffold

Template files placed here are copied to agent workspaces during first setup.

## Structure

```
madeira/       Files for Madeira (HLK operations assistant) workspace
orchestrator/  Files for the Orchestrator (multi-agent coordinator) workspace
architect/     Files for the Architect (read-only planner) workspace
executor/      Files for the Executor (read-write builder) workspace
verifier/      Files for the Verifier (quality gate) workspace
```

## Deployment

- `RULES.md` is deployed to each agent workspace. Agents read it at session start via SOUL.md directive for user-defined conventions.
- **Tool profiles are enforced at the gateway level** (v0.5.0), not just via prompts. Bootstrap translates `config/agent-capabilities.json` into per-agent OpenClaw `tools.profile`; the gateway blocks unauthorized tool calls even if an agent is prompt-injected.
- **Provider inventory is full-only**: bootstrap retains every provider in `config/openclaw.json.example` and emits warnings for unresolved env-backed URLs/keys instead of stripping provider blocks.
- **Madeira scaffold files**: `IDENTITY.md`, `USER.md`, `MEMORY.md`, and `WORKFLOW_AUTO.md` bootstrap Madeira's startup contract without overriding the canonical HLK vault.
- **Orchestrator workflow scaffold**: `WORKFLOW_AUTO.md` is also seeded for Orchestrator so startup recovery has deterministic workspace guidance after compaction/restart cycles.

## Usage

Copy these into the respective `~/.openclaw/workspace-{agent}/` directories
when setting up a new deployment. Files already present in the target workspace
are NOT overwritten -- these templates are defaults for fresh installs only.

The assembled SOUL.md prompts (from `prompts/assembled/`) should be placed in
the workspace root after assembly:

```
~/.openclaw/workspace-madeira/SOUL.md         <-- MADEIRA_PROMPT.{variant}.md
~/.openclaw/workspace-orchestrator/SOUL.md  <-- ORCHESTRATOR_PROMPT.{variant}.md
~/.openclaw/workspace-architect/SOUL.md     <-- ARCHITECT_PROMPT.{variant}.md
~/.openclaw/workspace-executor/SOUL.md      <-- EXECUTOR_PROMPT.{variant}.md
~/.openclaw/workspace-verifier/SOUL.md      <-- VERIFIER_PROMPT.{variant}.md
```

This is handled automatically by `python scripts/switch-model.py <environment>` and by **`py scripts/bootstrap.py`** Phase 4 (`deploy_soul_prompts`), which writes all five `SOUL.md` files after `assemble-prompts.py`. OpenClaw's **Bootstrap file** column in `openclaw status --all` should read **PRESENT** for every agent after a full bootstrap or switch-model run.
