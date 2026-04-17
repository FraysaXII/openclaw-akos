# Deprecate legacy public process objects — proposal

**Targets:** `standard_process`, `workflows`, `workstreams`, legacy `public."Process list"`.

**Steps (after operator approval + backup):**

1. RLS lock or revoke app roles.
2. Rename `_deprecated_*` or move to `archive` schema.
3. ERP/UI reads **mirror** or CSV views only.
4. Document incident note + [PRECEDENCE.md](../../../references/hlk/compliance/PRECEDENCE.md) reference.

**Quarantine:** `test_*`, `rag_2` — restrict access; drop only after approval.
