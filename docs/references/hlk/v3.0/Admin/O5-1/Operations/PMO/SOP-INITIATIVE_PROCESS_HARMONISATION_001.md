---
language: en
Item Name: Initiative ↔ process_list harmonisation (recipe and gates)
Item Number: SOP-INITIATIVE_PROCESS_HARMONISATION_001
Object Class: Guideline and Procedure
Confidence Level: Safe
Security Level: 2 (Internal Use)
Entity Owner: Think Big
Area Owner: Operations
Associated Workstream: Think Big Operational Excellence
Version: 0.1
Revision Date: 2026-05-06
status: review
Inherited Pattern: pattern_paired_sop_runbook
linked_runbooks:
  - scripts/validate_initiative_registry.py
Paired Runbook: scripts/validate_initiative_registry.py
Acceptance Criteria Human: PMO updates manifests_processes per Case A/B without the validator.
Acceptance Criteria Automation: validate_initiative_registry.py PASS on registry commit.
---

## Purpose

Define how a planning **initiative** (governed by [SOP-INITIATIVE_GOVERNANCE_001.md](SOP-INITIATIVE_GOVERNANCE_001.md)) declares which `process_list.csv` rows it **manifests** (delivers, exercises, or matures), and how new `process_list` rows get minted when an initiative discovers a process that does not yet exist.

This SOP closes a long-standing gap: planning initiatives implicitly performed work that "lived" in `process_list` clusters, but the linkage was prose-only. The new `manifests_processes` column on `INITIATIVE_REGISTRY.csv` (introduced by Initiative [59](../../../../../wip/planning/59-hlk-governance-clean-slate/master-roadmap.md), D-IH-59-G) makes the linkage **explicit, validated, and graph-traversable**.

## Preconditions

- Initiative has an `INITIATIVE_REGISTRY.csv` row (see [SOP-INITIATIVE_GOVERNANCE_001.md](SOP-INITIATIVE_GOVERNANCE_001.md)).
- The candidate `item_id` values from `process_list.csv` are **stable** (i.e. the initiative is past inception and knows which workstream(s) it belongs to).

## Recipe

### Case A — initiative manifests existing `process_list` rows

The common case. A planning initiative drives execution of one or more *already-minted* process clusters (workstreams, projects, or leaves).

1. Identify the **highest-meaningful-granularity** rows in `process_list.csv` that the initiative exercises. Prefer **workstream** (`item_granularity=workstream`) or **project** (`item_granularity=project`) IDs over raw leaves; a single initiative typically manifests one or two clusters, not dozens of leaves.
2. Set the `INITIATIVE_REGISTRY.csv` `manifests_processes` column to a **semicolon-delimited list** of those `item_id` values (e.g. `gtm_pm_ws_5;gtm_kdb_pj_finetune_madeira`).
3. The validator (`scripts/validate_initiative_registry.py`) FK-resolves each id against `process_list.csv` `item_id`. Unresolved entries are validation failures.
4. The list is **nullable**: leave the column empty (or use `—`) when no process row applies (yet). Empty is **explicit** and fine; **wrong** is not.

### Case B — initiative discovers a missing `process_list` row

The initiative implies a recurring process that is genuinely missing from `process_list.csv` (the row does not exist at any granularity).

This is **gated by operator approval**, per `.cursor/rules/akos-governance-remediation.mdc` and SOP-META_PROCESS_MGMT_001 §4.2–4.3:

1. **Draft proposal.** Author a short proposal under `docs/wip/planning/<NN>-<slug>/reports/process-list-mint-proposal-<topic>-YYYY-MM-DD.md` listing each candidate row with `item_id`, parent chain, role_owner, and rationale. The Initiative 59 P8 proposal report (`docs/wip/planning/59-hlk-governance-clean-slate/reports/p8-process-list-harmonisation-proposal-2026-05-06.md`) is the working template.
2. **Operator approval gate.** PMO + the role_owner sign off in writing (decision in the initiative's `decision-log.md` mirrored to `DECISION_REGISTER.csv` with `decision_class=architectural` and the explicit `linked_policies` of `SOP-META_PROCESS_MGMT_001`).
3. **Mint the rows.** Edit `process_list.csv` directly per [SOP-PMO_PROCESS_LIST_CSV_MAINTENANCE_001.md](SOP-PMO_PROCESS_LIST_CSV_MAINTENANCE_001.md) (unique `item_name`, parent ids dual-written with names, `item_granularity` correct).
4. **Run** `py scripts/validate_hlk.py` until PASS (it runs `validate_process_list` and the new I59 validators).
5. **Update** the initiative's `manifests_processes` column to include the new ids and re-run validation. The forward link is now traversable from both sides (initiative → process via the registry; process → initiative via reverse-lookup queries on the mirror).
6. **Baseline tranche.** If the new process rows require **new** `role_owner` lines in `baseline_organisation.csv`, those receive the **same operator approval gate** — do **not** fold baseline changes into a process tranche without explicit review.

### Case C — initiative is self-contained (no harmonisation)

Some initiatives are pure-meta (e.g. I59 itself) or one-shot remediation that legitimately has no recurring `process_list` counterpart. Leave `manifests_processes` empty. Document the rationale in master-roadmap.md `## Scope decisions`.

## Examples

| initiative_id | manifests_processes | rationale |
|---|---|---|
| `i57_post_closure_followup` | `gtm_pm_ws_5` | Post-closure follow-up exercises the Trello-to-process_list cluster |
| `i58_cycle_2_multi_track` | `gtm_pm_ws_5;gtm_kdb_pj_finetune_madeira` | Cycle exercises both PMO operational excellence and the fine-tune project |
| `i59_hlk_governance` | (empty) | Pure HLK meta-governance; no recurring process_list row applies |
| `i32_repo_health` | `gtm_pm_ws_5` (proposal: add `gtm_pm_st_repohealth`) | Existing cluster covers it; new sub-row deferred to operator approval |

## Out of scope

- Editing `process_list.csv` without going through Case B's operator approval gate.
- Treating `manifests_processes` as a **routing** field — it is metadata only; agents do not dispatch from it without role-aware checks.
- Backfilling old (closed) initiatives en masse. Backfill happens organically: when an old initiative is touched (status change, new decision, OPS forwarding), opportunistically populate the column.

## Registry cross-reference

- Companion SOP: [SOP-INITIATIVE_GOVERNANCE_001.md](SOP-INITIATIVE_GOVERNANCE_001.md).
- Maintenance SOP for `process_list.csv`: [SOP-PMO_PROCESS_LIST_CSV_MAINTENANCE_001.md](SOP-PMO_PROCESS_LIST_CSV_MAINTENANCE_001.md).
- Promotion gate (Trello → process_list): [SOP-PMO_VAULT_PROMOTION_GATE_001.md](SOP-PMO_VAULT_PROMOTION_GATE_001.md).
- Meta-SOP authority: [`SOP-META_PROCESS_MGMT_001.md`](../../../../../compliance/SOP-META_PROCESS_MGMT_001.md).
- Canonical CSVs: `INITIATIVE_REGISTRY.csv` (`manifests_processes` column), `process_list.csv`, `baseline_organisation.csv`.
- Validator: `scripts/validate_initiative_registry.py` (FK resolution of every `manifests_processes` entry).

## Ratification

This SOP is at **`status: review`**. Part of Initiative 59 P9 ratification scope. Operator approval (G-59-D) ratifies this SOP and flips its frontmatter to `status: active`. Until ratification this SOP is normative for I59-driven harmonisation activity (no `process_list` minting yet — see I60 candidate) and reviewed-but-non-binding for backlog work.
