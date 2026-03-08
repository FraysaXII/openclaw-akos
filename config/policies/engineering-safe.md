# Policy Pack: Engineering Safe

Default governance profile for standard development work.

## Rules
- All code changes must pass lint and tests before commit.
- Destructive operations (delete, overwrite) require HITL approval.
- External network calls require approval unless to known-safe domains.
- File writes outside the workspace directory are prohibited.

## Applies To
- Executor agent
- Verifier agent (limited write)
