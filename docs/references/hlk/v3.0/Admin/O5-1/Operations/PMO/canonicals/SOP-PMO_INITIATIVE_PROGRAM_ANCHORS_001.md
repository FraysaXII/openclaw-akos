---
language: en
Item Name: PMO INITIATIVE_REGISTRY program-anchors maintenance
Item Number: SOP-PMO_INITIATIVE_PROGRAM_ANCHORS_001
Object Class: Guideline and Procedure
Confidence Level: Safe
Security Level: 2 (Internal Use)
Entity Owner: Holistika
Area Owner: Operations
Associated Workstream: Think Big Operational Excellence
Process Owner: PMO
Version: 1.0
Revision Date: 2026-05-17
Status: review
Inherited Pattern: pattern_paired_sop_runbook
Paired Runbook: scripts/pmo_program_anchor_backfill.py
Acceptance Criteria Human: A PMO operator (or AIC role_owner) can read this SOP and produce/refresh a `proposals.csv` without invoking the runbook.
Acceptance Criteria Automation: `scripts/pmo_program_anchor_backfill.py --coverage-report` and `--apply proposals.csv --dry-run` fire unattended in CI smoke contexts.
---

## Purpose

Maintain queryable links from initiatives in
[`INITIATIVE_REGISTRY.csv`](../../../People/Compliance/canonicals/INITIATIVE_REGISTRY.csv)
into the
[`PROGRAM_REGISTRY.csv`](../../../People/Compliance/canonicals/dimensions/PROGRAM_REGISTRY.csv)
so the `hlk-erp` operator surface, MCP servers, and Madeira agents can roll up
initiative portfolios per program without minting a new CSV pivot table.

Stage A (this SOP version) encodes anchors as a `Program anchors: PRJ-HOL-<CODE>-<YEAR>; ...`
prefix on the `notes` cell. Stage B (I86 P2; D-IH-86-J) promotes the prefix to a
first-class `program_anchors` semicolon-list column on `INITIATIVE_REGISTRY.csv`
and Supabase mirror.

## Scope

- Initiatives with `status in {active, continuous, program_line}`. Closed and
  archived rows are out of scope (their anchor history stays preserved in the
  closure decision rather than churning the canonical CSV).
- Anchors **must** FK-resolve to a `program_id` in `PROGRAM_REGISTRY.csv`. The
  validator at
  [`scripts/validate_initiative_program_anchors.py`](../../../../../../../scripts/validate_initiative_program_anchors.py)
  fails CI when an anchor is malformed or unknown.

## Preconditions

- Operator has confirmed the per-INIT anchor proposals via an inline-ratify
  `AskQuestion` batch on the relevant initiative (or a multi-INIT batch when
  promoting a tranche).
- Validators pass against the current canonical CSV: `py scripts/validate_hlk.py`
  and `py scripts/validate_initiative_program_anchors.py`.

## Steps

1. **Enumerate gaps** with the runbook list mode::

       py scripts/pmo_program_anchor_backfill.py --list-unanchored

   The runbook prints every active/continuous/program_line INIT row whose
   `notes` cell lacks the `Program anchors:` prefix. The list is the working
   set for the next operator inline-ratify gate.

2. **Author proposals.csv** with the operator-confirmed `initiative_id,anchors`
   pairs (anchors semicolon-separated). Each anchor MUST match `^PRJ-HOL-[A-Z]+-\d{4}$`
   and MUST resolve to a `program_id` in `PROGRAM_REGISTRY.csv`. Do not invent
   new program ids inside this SOP — open a separate PR against
   [`PROGRAM_REGISTRY.csv`](../../../People/Compliance/canonicals/dimensions/PROGRAM_REGISTRY.csv)
   under the program owner first.

3. **Dry-run** to preview the rewrite::

       py scripts/pmo_program_anchor_backfill.py --apply proposals.csv --dry-run

   The runbook lists per-row diffs and skips any row already carrying the
   prefix (idempotent contract).

4. **Apply** after operator ratification (canonical-CSV gate per
   [`.cursor/rules/akos-governance-remediation.mdc`](../../../../../../../.cursor/rules/akos-governance-remediation.mdc))::

       py scripts/pmo_program_anchor_backfill.py --apply proposals.csv

   The runbook rewrites `notes` with the prefix, stamps `last_review_at`,
   `last_review_by`, `last_review_decision_id`, and `methodology_version_at_review`.

5. **Validate** before the commit::

       py scripts/validate_initiative_program_anchors.py
       py scripts/validate_hlk.py

   Both must PASS. Resolve any FK error against `PROGRAM_REGISTRY.csv` before
   committing.

6. **Refresh the coverage report**::

       py scripts/pmo_program_anchor_backfill.py --coverage-report

   The runbook writes
   `docs/wip/planning/86-initiative-cluster-execution-coordinator/reports/coverage-by-persona-<DATE>.md`.

7. **Commit** the canonical CSV change with a HEREDOC commit message that names
   the operator ratification and links to the decision id used in the
   `last_review_decision_id` stamp.

## Out of scope

- Editing closed or archived INIT rows — preserve their lineage in the closure
  decision register rather than reanimating the `notes` column.
- Introducing new `program_id` rows in `PROGRAM_REGISTRY.csv` — that requires a
  separate program-owner-approved tranche.
- Programmatically munging `notes` content beyond the prefix; downstream prose
  (e.g. `seeded by I59 P3 audit pass`) is preserved verbatim.

## Failure modes

- **Malformed anchor token.** Validator fails on tokens that do not match
  `^PRJ-HOL-[A-Z]+-\d{4}$`. Fix the proposals file; do not patch the canonical
  CSV by hand.
- **Unknown anchor.** Validator fails when an anchor is not in
  `PROGRAM_REGISTRY.csv`. Open a separate PR against the program registry first;
  do not invent program ids.
- **Idempotent re-run.** Re-running `--apply` on already-prefixed rows is a
  no-op by design. Confirm via `--dry-run` if uncertain.

## Registry cross-reference

- Process row (canonical-CSV gate): `hol_ops_dtp_72` in
  [`process_list.csv`](../../../People/Compliance/canonicals/process_list.csv)
  (status: review; promotes to active after operator ratification at the I86
  P1 commit).
- Paired runbook:
  [`scripts/pmo_program_anchor_backfill.py`](../../../../../../../scripts/pmo_program_anchor_backfill.py).
- Validator:
  [`scripts/validate_initiative_program_anchors.py`](../../../../../../../scripts/validate_initiative_program_anchors.py).
- Pydantic chassis:
  [`akos/hlk_initiative_program_anchors.py`](../../../../../../../akos/hlk_initiative_program_anchors.py).
- Coordinating initiative:
  [I86 master-roadmap](../../../../../../../docs/wip/planning/86-initiative-cluster-execution-coordinator/master-roadmap.md).
- Stage B forward reference: same initiative P2 (column promotion;
  D-IH-86-J).

## Governance cross-references

- [`.cursor/rules/akos-executable-process-catalog.mdc`](../../../../../../../.cursor/rules/akos-executable-process-catalog.mdc)
  RULE 1 (paired SOP+runbook) — this SOP and its runbook satisfy the contract.
- [`.cursor/rules/akos-holistika-operations.mdc`](../../../../../../../.cursor/rules/akos-holistika-operations.mdc)
  §"Operator SQL gate" — canonical-CSV authoring discipline.
- [`.cursor/rules/akos-brand-baseline-reality.mdc`](../../../../../../../.cursor/rules/akos-brand-baseline-reality.mdc)
  — the literal `PRJ-HOL-` prefix is added to the internal-token forbid list in
  P1 per D-IH-86-L so adviser-external dossiers never leak program ids.
