# Re-evaluation trigger — FINOPS / TECHOPS second canonical CSV

**Status**: TEMPLATE / NOT FIRED (2026-04-29).
**Owners**: Compliance (primary), Business Controller (FINOPS lens), System Owner (TECHOPS lens).
**Authority**: Wave-2 plan §"Decisions" **D-IH-14**; this initiative's [`decision-log.md`](../decision-log.md).
**Pattern source**: I22-P8 [`re-eval-trigger.md`](../../22-hlk-scalability-and-i21-closures/reports/re-eval-trigger.md).

## Why this template exists

The Wave-2 plan §"Pre-Wave §3" assessed both planes and concluded **DO NOT ADD a second canonical CSV** for either FINOPS or TECHOPS today:

- **FINOPS** today owns `FINOPS_COUNTERPARTY_REGISTER.csv` + `finops.registered_fact` (operational ledger). A `FINOPS_CONTRACT_REGISTER.csv` would duplicate Stripe FDW's authoritative contract metadata.
- **TECHOPS** today owns `COMPONENT_SERVICE_MATRIX.csv`. A `TECHOPS_API_REGISTRY.csv` would duplicate the matrix's `api_spec_pointer` column + `REPOSITORIES_REGISTRY.md`.

This template captures **the conditions under which that decision should be reopened** so the next operator (or agent) can act fast without reconstructing the rationale.

## Triggers

Reopen the decision when **either** condition fires:

1. **FINOPS reopen** — a third FINOPS use case surfaces beyond counterparty + ledger. Examples that would qualify:
   - A new SaaS contract management workflow with vault SSOT requirements (e.g. renewal calendar, change-control evidence) that **cannot be expressed via Stripe FDW joins**.
   - A new financial reporting dimension (cost centers, transfer pricing, multi-entity consolidation) that needs canonical row metadata distinct from counterparty + ledger.
2. **TECHOPS reopen** — TECHOPS adds a second register beyond `COMPONENT_SERVICE_MATRIX.csv`. Examples:
   - An API contract registry that cannot be expressed via `api_spec_pointer` + `REPOSITORIES_REGISTRY.md` (e.g. cross-repo API ownership tracking with row-level access control).
   - A SLA / SLO registry for production services that's distinct from the matrix's component metadata.

## Trigger record (fill on activation)

```yaml
fired_on: <YYYY-MM-DD>
trigger_kind: <finops_third_use_case | techops_second_register>
detected_by: <role / person>
evidence:
  - <link to issue, slack thread, or operator memo describing the gap>
  - <link to data/process that cannot be expressed in current registers>
proposed_csv:
  name: <CSV file name>
  fieldnames: [...]
  ssot_authority: <who authors? operator? feed from upstream system?>
  fk_targets: [<existing CSVs the new one references>]
operator_approvals:
  - <Compliance | Business Controller | System Owner | CFO | CTO>
proposed_initiative_slot: <NN-finops-second-register | NN-techops-second-register>
```

## Force-action checklist (do NOT skip steps)

- [ ] **Trigger documented** above. The trigger MUST fall into one of the two categories; if it does not, escalate the underlying gap to a separate decision in the appropriate initiative's `decision-log.md` first.
- [ ] **Evidence cited**: link concrete operational pain (issue, memo, blocked workflow) — not speculation.
- [ ] **Proposed CSV scoped**: column list + FK targets + SSOT authority pre-defined before the new initiative starts (avoids scope creep).
- [ ] **Plane owner approval** (Business Controller for FINOPS; System Owner for TECHOPS) recorded with date.
- [ ] **Compliance approval** for the new canonical CSV row in `PRECEDENCE.md`.
- [ ] **Initiative slot reserved** in `docs/wip/planning/README.md` before P0 begins.
- [ ] **Mark this template "FIRED + RESOLVED on `<YYYY-MM-DD>`"** with link to the closure PR after the new initiative ships.

## Cursor-rule guardrails (always-on)

Per [`akos-holistika-operations.mdc`](../../../../.cursor/rules/akos-holistika-operations.mdc) §"New git-canonical compliance registers (pattern)" and [`akos-governance-remediation.mdc`](../../../../.cursor/rules/akos-governance-remediation.mdc) §"HLK compliance governance":

- **Inventory-before-greenfield**: confirm extensions, foreign servers, foreign tables before adding a new schema or CSV.
- **Two-plane Supabase**: schema DDL via `supabase/migrations/`; mirror DML via `compliance_mirror_emit`. Never commit large `INSERT` mirror batches as migration files.
- **PRECEDENCE row required**: canonical + mirror entries before any code references the new CSV.
- **`akos/hlk_*_csv.py` fieldname tuple**: must match CSV header exactly; tested via `tests/test_hlk_*.py`.

## Cross-references

- [Initiative 26 master roadmap](../master-roadmap.md)
- [Initiative 26 decision log](../decision-log.md) (D-IH-14 reference)
- [Wave-2 plan §"Pre-Wave §3"](~/.cursor/plans/hlk_scalability_wave_2_initiatives_639a02d7.plan.md)
- I22 follow-up addendum: [`docs/wip/planning/22a-i22-post-closure-followups/reports/post-closure-followups-20260429.md`](../../22a-i22-post-closure-followups/reports/post-closure-followups-20260429.md) §3 (the original DO-NOT-ADD assessment)
