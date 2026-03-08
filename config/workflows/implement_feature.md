# Workflow: Implement Feature

## Agent Sequence
1. **Architect** -- plan the feature
2. **Executor** -- implement per plan
3. **Verifier** -- validate implementation

## Required Tools
- `read_file`, `write_file`, `shell_exec`, `sequential_thinking`

## Approval Points
- Plan review before Executor begins
- HITL gate on any destructive operations

## Steps
1. [ ] Architect analyzes requirements and existing code
2. [ ] Architect produces Plan Document with action items
3. [ ] Operator reviews and approves plan
4. [ ] Executor implements each action item
5. [ ] Verifier runs lint, tests, and build
6. [ ] Executor fixes any verification failures (up to 3 cycles)
7. [ ] Final verification pass

## Completion Criteria
- All plan actions executed and verified
- Tests pass
- No lint errors introduced
