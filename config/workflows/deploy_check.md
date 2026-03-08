# Workflow: Deployment Readiness Check

## Agent Sequence
1. **Architect** -- readiness assessment
2. **Verifier** -- validation

## Steps
1. [ ] Verify all tests pass
2. [ ] Check runtime drift (no mismatches)
3. [ ] Verify prompt sync status
4. [ ] Check MCP server availability
5. [ ] Verify model/provider readiness
6. [ ] Create pre-deployment checkpoint
7. [ ] Produce readiness report

## Completion Criteria
- All checks pass
- Checkpoint created
- Readiness report with GO/NO-GO recommendation
