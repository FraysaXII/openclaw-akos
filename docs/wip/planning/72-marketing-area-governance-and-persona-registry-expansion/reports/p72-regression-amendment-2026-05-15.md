---
language: en
phase: R-A..R-F (post-P10 regression amendment)
initiative: INIT-OPENCLAW_AKOS-72
authored: 2026-05-15
authored_by: CMO
last_review: 2026-05-17
last_review_by: System Owner
last_review_decision_id: D-IH-72-AP
methodology_version_at_review: v3.0
status: shipped
backfill_context: 2026-05-17 mechanical-backlog regression sweep
backfill_decision_basis: 7 DECISION_REGISTER rows D-IH-72-AI..AO cite this path; canonical narrative already shipped under p72-closing.md §"Regression amendment R-A..R-F (post-P10)" (lines 84-244)
---

# I72 regression amendment — R-A..R-F (post-P10)

> Cited by 7 `D-IH-72-A*` rows in [`DECISION_REGISTER.csv`](../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv) as `decision_log_path`. The full narrative — phase-by-phase rationale, file-by-file deltas, FK cascades, and operator's "disciplines ≠ roles, no horizontal bloat" architectural framing — lives in [`p72-closing.md`](p72-closing.md) §"Regression amendment R-A..R-F (post-P10)" (lines 84-244). This document is the structured per-decision crosswalk so each cited row resolves to a file that exists.

## Why this report was backfilled (2026-05-17)

The I72 P10 closure commit `fed64fc` consolidated all R-A..R-F narrative into `p72-closing.md` rather than spinning a separate amendment report. The 7 amendment decisions (D-IH-72-AI through D-IH-72-AO) and the closure ratification (D-IH-72-AP) were appended to `DECISION_REGISTER.csv` with `decision_log_path` pointing to `p72-regression-amendment-2026-05-15.md` — but that file was never created. The 2026-05-17 mechanical regression sweep flagged this as 7 advisory warnings from [`validate_decision_register.py`](../../../../../scripts/validate_decision_register.py). Per the parent agent's mechanical-backlog directive, this report was backfilled to resolve the citation gap without mutating `DECISION_REGISTER.csv` (which would require operator approval per `akos-governance-remediation.mdc`). The amendment work itself shipped on `main` between 2026-05-15 01:30..01:52 UTC+2 in commits `93f82db` through `fed64fc`; this document records the per-decision crosswalk for audit traceability.

## Closure header

- **Cycle**: post-P10 regression amendment R-A..R-F.
- **Trigger**: agent-led 9-question regression review surfaced after `D-IH-72-CLOSURE`; operator's responses crystallised one architectural principle.
- **Architectural principle ratified**: *"Disciplines ≠ roles. New roles should do lots of things; do not bloat the organisation horizontally."*
- **Initiative status posture**: `INIT-OPENCLAW_AKOS-72` remains `status: closed` (regression-amend cycle, NOT re-opening) per operator framing "*this is nothing but a regression, a big one*".
- **SemVer posture**: no v3.2.0 cut; v3.1 is still being built and v3.2 will mark a methodological breakthrough, not a registry consolidation pass.
- **Closure ratification**: `D-IH-72-AP` ratifies R-A..R-E en bloc; `INITIATIVE_REGISTRY.csv` row 58 `last_review_decision_id` bumped to `D-IH-72-AP`.

## Per-decision crosswalk

| Decision | Phase | Commit | Files | Lines delta | Narrative source |
| :--- | :---: | :---: | ---: | ---: | :--- |
| `D-IH-72-AI` (Cursor rule path corrections — `akos-executable-process-catalog.mdc` Rule 2 + Rule 4 placement) | R-A | `93f82db` | 6 | +18 / -11 | [`p72-closing.md` §R-A](p72-closing.md#r-a--cursor-rule-hardening-commit-93f82db-6-files-1811) |
| `D-IH-72-AJ` (Cursor rule alwaysApply audit — flip 4 broad-governance rules + add frontmatter to `akos-executable-process-catalog.mdc`) | R-A | `93f82db` | 6 | +18 / -11 | [`p72-closing.md` §R-A](p72-closing.md#r-a--cursor-rule-hardening-commit-93f82db-6-files-1811) |
| `D-IH-72-AK` (`REVOPS_PROCESS_CATALOG` SOP backfill — author 3 missing SOPs + fix `crm_sync` stale pointer) | R-B | `16f08ae` | 9 | +327 / -4 | [`p72-closing.md` §R-B](p72-closing.md#r-b--folder-cleanup--sop-backfill-commit-16f08ae-9-files-3274) |
| `D-IH-72-AL` (`Marketing/Social/` + `Marketing/Growth/` folder cleanup — `git rm -r` dead `.gitkeep` shells) | R-B | `16f08ae` | 9 | +327 / -4 | [`p72-closing.md` §R-B](p72-closing.md#r-b--folder-cleanup--sop-backfill-commit-16f08ae-9-files-3274) |
| `D-IH-72-AM` (RevOps role slim — delete 4 expansion forward-charter rows; absorb disciplines into RevOps Lead generalist) | R-C | `dd86b22` | 4 | +14 / -17 | [`p72-closing.md` §R-C](p72-closing.md#r-c--revops-role-slim-commit-dd86b22-4-files-1417-baseline-8278) |
| `D-IH-72-AN` (Marketing sub-role selective collapse — delete 6 sub-roles + absorb disciplines into 4 Sub-Area Managers) | R-D | `ccbf87d` | 11 | +52 / -57 | [`p72-closing.md` §R-D](p72-closing.md#r-d--marketing-sub-role-selective-collapse-commit-ccbf87d-11-files-5257-baseline-7872) |
| `D-IH-72-AO` (Brand+Storytelling merger — Marketing M3 v3.1 collapse 5 sub-areas to 4 "Brand & Narrative"; -4 Brand sub-role rows; -1 Storytelling Manager row) | R-E | `a09fbe6` | 38 | +123 / -90 | [`p72-closing.md` §R-E](p72-closing.md#r-e--brandstorytelling--brand--narrative-merger-commit-a09fbe6-38-files-12390-baseline-7267) |
| `D-IH-72-AP` (R-A..R-E ratification en bloc; initiative `last_review_decision_id` bump; CHANGELOG `[Unreleased]` entries; `files-modified.csv` R-F closure rows) | R-F | `fed64fc` | 4 | +180 / -2 | [`p72-closing.md` §R-F](p72-closing.md#r-f--closing-amendment-report--d-ih-72-ap-this-commit) |

## Net delta vs P10 closure

| Metric | Before R-A | After R-F | Delta |
| :--- | ---: | ---: | ---: |
| `baseline_organisation.csv` rows | 82 | 67 | **−15** |
| Active Marketing sub-areas | 5 | 4 | **−1** (Brand+Storytelling merged) |
| RevOps active roles | 2 | 2 | 0 (4 forward-chartered specialists deleted) |
| Marketing sub-roles below sub-area manager | 9 | 3 | **−6** (selective collapse) |
| `D-IH-72-*` decisions ratified | 35 (A..AH + CLOSURE) | 42 (A..AP + CLOSURE) | **+7** |
| `Marketing/Social/` + `Marketing/Growth/` shells | present (dead) | deleted | cleanup |
| Cursor rules with `alwaysApply: true` (net-new I72 surface) | 0 of 5 | 5 of 5 | hardened |
| `REVOPS_PROCESS_CATALOG.yaml` `TODO[...]` pointers | 4 | 0 | resolved |

## UAT bands re-verification at R-F (per `p72-closing.md` §"UAT bands re-verification at R-F")

- **Band A — HLK validators**: `py scripts/validate_hlk.py` PASS (0 errors; 12 advisory warnings unchanged at the time of R-F closure).
- **Band B — Vault links**: `py scripts/validate_hlk_vault_links.py` PASS.
- **Band C — RevOps Spine** (P7 contract): PASS — slim role taxonomy doesn't affect the FK schema or governance view.
- **Band D — Adapter registries** (P9 contract): PASS — path corrections in R-A match where the registries actually shipped.
- **Band E — Process pairing** (P9 contract): PASS — 3 backfilled SOPs in R-B resolved 3 of 4 informational warnings; 1 informational warning remains as `tbi_ops_dtp_revops_media_review_001` per `D-IH-72-W` design tolerance.

## Filesystem strategy note (R-E)

`Marketing/Brand/` and `Marketing/Storytelling/` folders kept in place at R-E to preserve cross-reference stability. The conceptual merger lives in role descriptions, sub-area charters, frontmatter, and the registry. A future filesystem-only pass may consolidate the two folders under `Marketing/Brand & Narrative/` once cross-link debt is quantified — but R-E does NOT take that step (minimum-disruption principle).

## Cross-references

- [`DECISION_REGISTER.csv`](../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv) — 7 amendment decisions D-IH-72-AI..AO + closure D-IH-72-AP.
- [`p72-closing.md`](p72-closing.md) — full P10 closure report with R-A..R-F regression amendment section appended (lines 84-244 carry the per-decision narrative).
- [`master-roadmap.md`](../master-roadmap.md) — initiative `status: closed`.
- [`files-modified.csv`](../files-modified.csv) — R-A..R-F file deltas backfilled at R-F closure.
- [`CHANGELOG.md`](../../../../CHANGELOG.md) — `[Unreleased]` band carries R-A..R-F entries (no v3.2.0 cut per operator framing).
- [`akos-executable-process-catalog.mdc`](../../../../.cursor/rules/akos-executable-process-catalog.mdc) — Rule 2 + Rule 4 carry the D-IH-72-AI path corrections inline.
- [`akos-planning-traceability.mdc`](../../../../.cursor/rules/akos-planning-traceability.mdc) — `alwaysApply: true` per D-IH-72-AJ.
- [`akos-agent-checkpoint-discipline.mdc`](../../../../.cursor/rules/akos-agent-checkpoint-discipline.mdc) — `alwaysApply: true` per D-IH-72-AJ.
- [`akos-holistika-operations.mdc`](../../../../.cursor/rules/akos-holistika-operations.mdc) — `alwaysApply: true` per D-IH-72-AJ.
- [`akos-brand-baseline-reality.mdc`](../../../../.cursor/rules/akos-brand-baseline-reality.mdc) — `alwaysApply: true` per D-IH-72-AJ.

## Backfill authoring notes (2026-05-17)

This crosswalk was authored by a regression-sweep subagent on 2026-05-17 as part of the mechanical-backlog directive ("end the entire scope in this chat; no more handoffs"). The substantive amendment work itself shipped on 2026-05-15 in commits `93f82db..fed64fc`. This file does not introduce new decisions, new role mutations, or new architectural claims — it is a structured navigation aid so the 7 DECISION_REGISTER citations resolve to a real file. The canonical narrative (rationale, FK cascades, deltas, UAT bands) remains in `p72-closing.md` §"Regression amendment R-A..R-F (post-P10)".
