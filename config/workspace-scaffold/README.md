# Workspace Scaffold

Template files placed here are copied to agent workspaces during first setup.

## Structure

```
orchestrator/  Files for the Orchestrator (multi-agent coordinator) workspace
architect/     Files for the Architect (read-only planner) workspace
executor/      Files for the Executor (read-write builder) workspace
verifier/      Files for the Verifier (quality gate) workspace
```

## Usage

Copy these into the respective `~/.openclaw/workspace-{agent}/` directories
when setting up a new deployment. Files already present in the target workspace
are NOT overwritten -- these templates are defaults for fresh installs only.

The assembled SOUL.md prompts (from `prompts/assembled/`) should be placed in
the workspace root after assembly:

```
~/.openclaw/workspace-orchestrator/SOUL.md  <-- ORCHESTRATOR_PROMPT.{variant}.md
~/.openclaw/workspace-architect/SOUL.md     <-- ARCHITECT_PROMPT.{variant}.md
~/.openclaw/workspace-executor/SOUL.md      <-- EXECUTOR_PROMPT.{variant}.md
~/.openclaw/workspace-verifier/SOUL.md      <-- VERIFIER_PROMPT.{variant}.md
```

This is handled automatically by `python scripts/switch-model.py <environment>`.
