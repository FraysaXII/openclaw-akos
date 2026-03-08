# Workflow: Verify Changes

## Agent Sequence
1. **Verifier** -- full verification suite

## Required Tools
- `shell_exec`, `read_file`, `browser_screenshot`

## Steps
1. [ ] Run linter on changed files
2. [ ] Run test suite (full or targeted)
3. [ ] Run build if applicable
4. [ ] Capture browser screenshots if UI changes
5. [ ] Produce verification report

## Completion Criteria
- All checks pass or failures documented
- Verification report with PASS/FAIL per check
