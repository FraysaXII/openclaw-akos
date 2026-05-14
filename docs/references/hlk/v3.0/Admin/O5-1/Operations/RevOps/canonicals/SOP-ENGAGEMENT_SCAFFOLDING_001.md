---
language: en
status: review
canonical: true
role_owner: PMO
classification: way_of_working
intellectual_kind: SOP
ssot: true
authored: 2026-05-15
last_review: 2026-05-15
last_review_at: 2026-05-15
last_review_by: CMO
last_review_decision_id: D-IH-72-AK
methodology_version_at_review: v3.0
companion_to:
  - REVOPS_AREA_CHARTER.md
  - REVOPS_PROCESS_CATALOG.yaml
  - SOP-ENGAGEMENT_TEMPLATE_PROMOTION_001.md
---

# SOP-ENGAGEMENT_SCAFFOLDING_001 — Engagement RPA scaffolder cycle

> Authored I72 R-B (2026-05-15) per `D-IH-72-AK` (regression-amend SOP backfill). Closes the Rule 1 SOP-pairing gap that the I72 regression review (Q5-A) flagged for the `engagement_scaffold` entry in `REVOPS_PROCESS_CATALOG.yaml`. The runbook is `scripts/scaffold_engagement.py` (shipped at I72 P8 per `D-IH-72-P`); this SOP is its operator-facing counterpart.

## 1. Purpose

Provide an event-triggered scaffolder that, when a new engagement is opened against a promoted template, copies the template skeleton to the engagement's working folder, seeds frontmatter, and opens a PR for operator review. Operationalises the engagement-template lifecycle (per `D-IH-72-F` template registry + `D-IH-72-N` process catalog) and the value-mapping core function (per `D-IH-72-Y`) at the engagement-instantiation moment.

## 2. Scope

In scope:

- Trigger: a new row appended to `ENGAGEMENT_REGISTRY.csv` with `template_id` referencing an `ENGAGEMENT_TEMPLATE_REGISTRY.csv` row in `lifecycle_status: active`.
- Action: copy `Think Big/Clients/_engagement-template/<template-slug>/` skeleton to `Think Big/Clients/<engagement-slug>/`, seed frontmatter, open PR.
- Reviewer assignment based on the engagement's primary area (Marketing/Resonance for customer-success engagements; Operations/RevOps for revenue-attribution engagements; etc.).

Out of scope:

- Template authoring itself (lives in `SOP-ENGAGEMENT_TEMPLATE_PROMOTION_001.md`).
- Stripe-side counterparty link (lives in `SOP-FINOPS_BRIDGE_001.md`).
- Legal-template firing (lives in `SOP-LEGAL_TEMPLATE_FIRE_001.md`).

## 3. Steps

### 3.1 Event detection

The scaffolder watches `ENGAGEMENT_REGISTRY.csv` for new rows. PMO (or `revops-analyst-aic`) can also fire it manually:

```powershell
py scripts/scaffold_engagement.py --engagement-id <new-engagement-id> --template-id <template-id>
```

### 3.2 Template lookup

The scaffolder:

1. Reads the engagement row from `ENGAGEMENT_REGISTRY.csv`.
2. Looks up the matching `template_id` in `ENGAGEMENT_TEMPLATE_REGISTRY.csv`.
3. Verifies `lifecycle_status: active` (rejects scaffold if template is `scaffold` / `deprecated`).
4. Resolves the template skeleton path under `Think Big/Clients/_engagement-template/<template-slug>/`.

### 3.3 Folder copy + frontmatter seed

The scaffolder:

1. Creates `Think Big/Clients/<engagement-slug>/` (slug derived from engagement-row `engagement_name` per kebab-case convention).
2. Copies the template skeleton tree, preserving subfolders and `.gitkeep` placeholders.
3. Seeds frontmatter on the top-level `README.md` with: `engagement_id`, `template_id`, `counterparty_org_id`, `primary_persona_id`, `start_date`, `expected_end_date`, `primary_area`, `role_owner_human`, `forecast_revenue_eur`.
4. Stages all new files via `git add`.

### 3.4 PR open + reviewer assignment

The scaffolder:

1. Creates a feature branch named `engagement/<engagement-slug>-scaffold`.
2. Commits with message `engagement scaffold: <engagement-slug> from template <template-slug>`.
3. Opens a PR via `gh pr create` (when GH CLI is available) OR exits with the operator-action message "PR-open step deferred to operator" (when running without `gh`).
4. Tags the PR with the engagement's primary-area Sub-Area Manager as reviewer.

### 3.5 Operator review

PMO (or the engagement's primary-area Sub-Area Manager) reviews the scaffolded folder + PR diff:

- Verify frontmatter cells are populated correctly.
- Verify no template-specific TODO markers were left unfilled.
- Verify the engagement folder doesn't collide with an existing engagement.
- Approve + merge OR request changes.

### 3.6 Post-merge actions

Once the PR merges:

1. Trigger `SOP-FINOPS_BRIDGE_001.md` if the engagement transitions to `status: active`.
2. Trigger `SOP-PEOPLE_ENGAGEMENT_HANDOFF_001.md` if the engagement requires People Operations onboarding.
3. Trigger `SOP-LEGAL_TEMPLATE_FIRE_001.md` if the engagement reaches scope-lock.

## 4. Failure modes

- Template lookup fails (`template_id` not in registry) → exit code 2; operator manually appends template row + re-runs.
- Template `lifecycle_status: scaffold` → exit code 3; operator either promotes template via `SOP-ENGAGEMENT_TEMPLATE_PROMOTION_001.md` first, or overrides with `--allow-scaffold-template` flag (RevOps Lead-only).
- Folder collision (`Think Big/Clients/<engagement-slug>/` already exists) → exit code 4; operator picks a unique slug.
- `gh pr create` fails (no GH CLI / not authenticated) → exit code 0 with operator-action message; commit + push happen separately.

## 5. Acceptance criteria

Per [`akos-executable-process-catalog.mdc`](../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 5:

- **AC-HUMAN**: PMO (or `revops-analyst-aic`) runs §3 steps manually using only this SOP body (creates the folder, seeds frontmatter, opens PR via `gh pr create`).
- **AC-AUTOMATION**: `scripts/scaffold_engagement.py` exits 0 with new folder + frontmatter + PR opened (or operator-action message when `gh` unavailable); `validate_hlk.py` PASS.

## 6. Cross-references

- Parent: [`REVOPS_AREA_CHARTER.md`](REVOPS_AREA_CHARTER.md).
- Catalog entry: `REVOPS_PROCESS_CATALOG.yaml` `engagement_scaffold` (cadence: event_triggered; trigger: template_promoted).
- Sister SOPs: [`SOP-ENGAGEMENT_TEMPLATE_PROMOTION_001.md`](SOP-ENGAGEMENT_TEMPLATE_PROMOTION_001.md), [`SOP-FINOPS_BRIDGE_001.md`](SOP-FINOPS_BRIDGE_001.md), [`SOP-PEOPLE_ENGAGEMENT_HANDOFF_001.md`](SOP-PEOPLE_ENGAGEMENT_HANDOFF_001.md), [`SOP-LEGAL_TEMPLATE_FIRE_001.md`](SOP-LEGAL_TEMPLATE_FIRE_001.md).
- Runbook: `scripts/scaffold_engagement.py`.
- Data sources: `ENGAGEMENT_REGISTRY.csv`, `ENGAGEMENT_TEMPLATE_REGISTRY.csv`.
- Decisions: D-IH-72-AK (this SOP), D-IH-72-P (RPA scaffolder), D-IH-72-F (template registry), D-IH-72-N (process catalog architecture).
