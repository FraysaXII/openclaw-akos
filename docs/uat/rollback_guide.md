# Rollback Guide

Guidance for rolling back by failure class.

## Runtime Drift

**Symptom**: `py scripts/check-drift.py` reports mismatches.
**Action**: `py scripts/sync-runtime.py` to re-hydrate runtime from repo.
**Verification**: `py scripts/check-drift.py` exits 0.

## Startup / Session Failure

**Symptom**: Agent workspace files missing or corrupted.
**Action**: Re-run `py scripts/bootstrap.py` to regenerate workspaces.
**Verification**: Open dashboard, verify all 5 agents visible.

## HITL Mismatch

**Symptom**: Agent has tools it should not (e.g., Architect has `write` or `exec`).
**Action**: Verify `config/agent-capabilities.json` is correct, then re-sync: `py scripts/sync-runtime.py`.
**Verification**: `GET /agents/{id}/capability-drift` returns empty issues.

## Tool Availability Mismatch

**Symptom**: Expected MCP server not responding.
**Action**: Check `~/.mcporter/mcporter.json` has all expected entries. Re-run bootstrap MCP phase: `py scripts/bootstrap.py --skip-ollama`.
**Verification**: `py scripts/check-drift.py` reports no missing MCP servers.

## Test Failure Regression

**Symptom**: `py scripts/test.py all` fails.
**Action**: Review failing tests. If introduced by recent change, revert the commit. If pre-existing, check CHANGELOG for known issues.
**Verification**: `py scripts/test.py all` passes.

## Full System Reset

If all else fails:
1. `py scripts/sync-runtime.py` -- re-sync from repo
2. `py scripts/bootstrap.py --skip-ollama` -- regenerate config
3. `openclaw gateway restart` -- restart gateway
4. `py scripts/doctor.py` -- verify health
5. `py scripts/test.py all` -- verify tests
