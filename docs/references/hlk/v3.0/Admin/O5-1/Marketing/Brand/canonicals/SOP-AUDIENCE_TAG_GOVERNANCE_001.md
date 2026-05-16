---
sop_id: SOP-AUDIENCE_TAG_GOVERNANCE_001
title: Audience-tag governance
version: 1.0
status: review
classification: canonical
access_level: 4
register: internal
language: en
process_id: TODO[I85-P4-process-mint]
role_owner: Brand & Narrative Manager
role_parent_1: CMO
area: MKT
entity: Holistika
governance:
  - D-IH-85-A (narrow FK index scope)
  - D-IH-85-B (YAML list multi-audience encoding)
  - D-IH-85-C (operator-batch-approve sweep posture)
linked_initiative: I85
linked_runbook: TODO[I85-P2-audience-tag-runbook]
created: 2026-05-16
last_review: 2026-05-16
---

# SOP-AUDIENCE_TAG_GOVERNANCE_001 — Audience-tag governance

> Brand-and-Narrative-Manager-owned governance for the `audience: [J-*]` frontmatter tag system. The `AUDIENCE_REGISTRY.csv` is the FK source-of-truth for which audience codes exist; `BRAND_BASELINE_REALITY_MATRIX.md` remains SSOT for deep audience content (bridge framing, objection patterns, first-doubt triggers, voice deltas). Both stay synchronized.

## 1. Purpose

Every surface under `docs/references/hlk/v3.0/_assets/advops/**` and `docs/references/hlk/v3.0/_assets/touchpoint-kit/**` may carry an `audience: [J-*]` YAML-list frontmatter declaring its intended audience(s). The `craft` skill (per [`.cursor/skills/impeccable/SKILL.md`](../../../../../../../../.cursor/skills/impeccable/SKILL.md) line 20) hard-fails multi-audience surfaces; the drift gate detects unregistered codes; downstream consumers (touchpoint kit dispatcher, dossier-render pipeline, future audience-aware rendering per I74) FK-resolve against the registry.

This SOP governs three things: (a) how to **mint** a new audience row, (b) how to **modify** an existing row (especially `status` flips), and (c) how to **migrate** surfaces to or between audience tags.

## 2. Cadence

- **`event_triggered`** (primary): mint or modify a row when an operator-batch-approved tranche adds a new audience surface class, or when a planned/inactive audience promotes to active.
- **`scheduled`** (secondary): quarterly review (every 90 days from `last_review_at`) — re-verify each row's `register_side` against the brand register matrix, `typical_surfaces` against the live filesystem, and `status` against present surface usage.

## 3. Inputs

- [`AUDIENCE_REGISTRY.csv`](../../../People/Compliance/canonicals/dimensions/AUDIENCE_REGISTRY.csv) — the FK index.
- [`BRAND_BASELINE_REALITY_MATRIX.md`](BRAND_BASELINE_REALITY_MATRIX.md) — the SSOT for deep audience content.
- [`baseline_organisation.csv`](../../../People/Compliance/canonicals/baseline_organisation.csv) — FK source for `last_review_by`.
- [`DECISION_REGISTER.csv`](../../../People/Compliance/canonicals/DECISION_REGISTER.csv) — FK source for `last_review_decision_id` and `linked_decision_id`.

## 4. Steps

### 4.1 Mint a new audience row

1. Confirm the audience archetype is not already covered by an existing row (do not split J-IN into J-IN-COLD and J-IN-WARM — that is persona-class granularity, captured in `PERSONA_REGISTRY.csv`).
2. Confirm the bridge frame, objection patterns, and first-doubt trigger for the new archetype are authored in `BRAND_BASELINE_REALITY_MATRIX.md` first (matrix is SSOT for prose).
3. Mint a new `D-IH-NN-*` decision row in `DECISION_REGISTER.csv` capturing the operator approval (canonical-CSV gate per [`akos-governance-remediation.mdc`](../../../../../../../.cursor/rules/akos-governance-remediation.mdc) §"Canonical CSV gates").
4. Append a row to `AUDIENCE_REGISTRY.csv` with `status=active` (or `planned` if surfaces do not yet exist).
5. Append a `CANONICAL_REGISTRY.csv` row if this is a structurally new canonical (not required for adding a row to an existing registry).
6. Run `py scripts/validate_audience_registry.py` (must PASS) and `py scripts/validate_hlk.py` (must PASS overall).
7. Operator approval gate before commit.

### 4.2 Modify an existing row

1. Identify the change (status flip, `typical_surfaces` extension, `register_side` correction).
2. Update the row, including `last_review_at` (today's date), `last_review_by`, `last_review_decision_id`, and `methodology_version_at_review`.
3. For substantive changes (status flip, register_side change), mint a new `D-IH-NN-*` decision row.
4. Run validators (4.1.6) and operator-approval (4.1.7).

### 4.3 Migrate surfaces to / between audience tags

1. Run a **dry-run report** via `audience_tag_assets.py --dry-run --tranche <name>` (paired runbook, P2 deliverable).
2. Operator reviews the dry-run output (which surfaces would change, what inferences were made).
3. Operator-batch-approve per tranche (e.g. `advops/decks`, then `advops/dossiers`, then `touchpoint-kit/emails`). Do not auto-apply — audience inference is judgement-heavy (per D-IH-85-C).
4. Apply the approved tranche; run `py scripts/validate_audience_tags.py` (drift gate, P2 deliverable) to confirm no unregistered codes leaked.
5. Commit the tranche as one phase-scoped commit.

## 5. Outputs

- Updated `AUDIENCE_REGISTRY.csv` (canonical).
- Updated `compliance.audience_registry_mirror` (post-mirror-sync via `sync_compliance_mirrors_from_csv.py`).
- Updated `BRAND_BASELINE_REALITY_MATRIX.md` (when prose changes).
- New `D-IH-NN-*` decision rows in `DECISION_REGISTER.csv`.
- Tranche-applied frontmatter updates on advops + touchpoint-kit surfaces (P2 migrations).

## 6. Failure modes

| Failure mode | Detection | Recovery |
|:---|:---|:---|
| New code minted without DECISION_REGISTER row | `validate_audience_registry.py` reports FK miss | Mint the missing decision row (operator-approval gate) and re-run validator |
| `typical_surfaces` references nonexistent glob | Periodic quarterly review (cadence §2 secondary) | Update `typical_surfaces` or move the row to `status=inactive` |
| Surface frontmatter `audience:` references unregistered code | `validate_audience_tags.py` drift gate (P2) | Either mint the code (4.1) or correct the frontmatter |
| Two audience codes have overlapping `intent_summary` | Quarterly review surfaces redundancy | Merge or deprecate; clearly document which absorbs which in the decision row |
| `register_side` drifts from `BRAND_BASELINE_REALITY_MATRIX.md` matrix | Quarterly review + drift gate | Matrix wins; update the CSV row to match |

## 7. Cross-references

- [`akos-brand-baseline-reality.mdc`](../../../../../../../.cursor/rules/akos-brand-baseline-reality.mdc) — dual-register contract (which `register_side` value to assign).
- [`akos-executable-process-catalog.mdc`](../../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 1 — paired SOP + runbook discipline (P2 ships the runbook).
- [`akos-holistika-operations.mdc`](../../../../../../../.cursor/rules/akos-holistika-operations.mdc) §"New git-canonical compliance registers (pattern)" — canonical CSV + Pydantic + validator + mirror pattern.
- [`.cursor/skills/impeccable/SKILL.md`](../../../../../../../.cursor/skills/impeccable/SKILL.md) line 20 — multi-audience hard-fail invocation.
- [I85 master-roadmap](../../../../../../wip/planning/85-audience-tag-canonicalization/master-roadmap.md) — the initiative this SOP serves.

## 8. Promotion to status: active

This SOP ships at `status: review` from I85 P1. Promotion to `status: active` happens at **I85 P4 closure** with the following gates:

1. P2 paired runbook `scripts/audience_tag_assets.py` exists and has been used at least once.
2. P3 `BRAND_BASELINE_REALITY_MATRIX.md` §"Multi-audience composition recipe" lands.
3. A `process_list.csv` tranche mints the corresponding `tbi_mkt_dtp_audience_tag_governance_001` (or equivalent) row.
4. The `process_id` frontmatter field is updated from `TODO[I85-P4-process-mint]` to the actual process_id.
5. `validate_hlk.py` PASS overall.
6. Operator approval gate.
