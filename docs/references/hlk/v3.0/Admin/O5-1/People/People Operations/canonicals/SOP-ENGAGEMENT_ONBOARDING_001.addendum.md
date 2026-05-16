---
language: en
status: active
canonical: true
role_owner: People Operations Lead
co_owner_role: PMO
area: People
entity: Holistika
intellectual_kind: sop-addendum
authored: 2026-05-16
last_review: 2026-05-16
last_review_by: People Operations Lead
last_review_decision_id: D-IH-80-D
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-73-D
  - D-IH-73-K
  - D-IH-80-D
parent_sop: SOP-ENGAGEMENT_ONBOARDING_001.md
companion_to:
  - SOP-ENGAGEMENT_ONBOARDING_001.md
  - LEARNING_CHARTER.md
ssot: true
---

# SOP-ENGAGEMENT_ONBOARDING_001 — Addendum (Four-channel persistence + apprentice curriculum integration depth)

> Access level 5. Authored at I80 P5 (D-IH-80-D Option B retrofit pilot, 2026-05-16). The body executor needs the routing logic; this addendum carries the four-channel persistence dimensions, apprentice curriculum integration mechanics, access-level routing matrix, and out-of-scope cross-area handoffs that PMO / Learning Lead / System Owner reference when onboarding flows into adjacent processes.

## A. Four-channel persistence — what each channel carries and why

Per [`WORKSPACE_BLUEPRINT_HOLISTIKA.md`](../../../Operations/PMO/canonicals/WORKSPACE_BLUEPRINT_HOLISTIKA.md) §1, every engagement persists across four channels. The auditor-facing detail per channel:

### A.1 Git canonical (the AKOS repository)

The git repo is the canonical SSOT for engagement contracts (NDA + IP clause + retribution clause attached as Markdown), engagement README, and any methodology artefact the engagement consumes (read-only references). Git is append-only-with-history; revisions create commits; commit hashes are the audit anchor.

What lives in git: engagement README + frontmatter + commit-trail of substantive revisions + any operator-authored artefact tied to the engagement.

What does NOT live in git: live cap-table state (drive); live deal-pipeline state (CRM); transient per-day work-products (drive). The git layer is structural; the others are operational.

### A.2 Drive (Google Workspace / equivalent)

Drive is the operational layer for live artefact collaboration — documents in active edit, files shared with the counterparty, attachments to email threads. Engagement folder shape mirrors the git skeleton (`Think Big/Clients/<engagement>/`, `Think Big/Advisers/<advisor>/`, etc.).

What lives in drive: live work-products + counterparty-shared files + meeting recordings + any artefact too large for git (videos, design files).

What does NOT live in drive: canonical contracts (those are git); methodology artefacts (those are git read-only).

The drive is propagated from git templates at engagement instantiation time (the runbook copies `_engagement-template/` from git to drive). After instantiation, drive is operationally independent.

### A.3 SQL mirror (Supabase compliance.* + holistika_ops.*)

The Supabase mirror surfaces the engagement metadata for cross-area joins. `compliance.engagement_registry_mirror` carries the engagement metadata; `holistika_ops.lead_intake` upstream feeds the engagement at intake time; `finops.registered_fact` downstream records monetary events tied to the engagement.

Supabase is read-mostly for People (SQL gates per `akos-holistika-operations.mdc` §"Two-plane model"); writes go through CSV mirror sync (`compliance_mirror_emit` profile). Live engagement state in Supabase is the *projection* of git canonical CSVs, not a second SSOT.

### A.4 HLK-ERP (the operator-facing dashboard)

HLK-ERP at `127.0.0.1:18789` is the role-owner-facing surface for engagement operations: list view of active engagements, drill-down to engagement panel (per-engagement page with current status + recent commits + recent FINOPS events), and routing to upstream systems.

People Operations Lead uses HLK-ERP for daily operations; the four-channel persistence ensures the data shown in HLK-ERP is consistent with git canonical + drive operational + SQL projection at any moment. Drift between channels is an audit finding.

## B. Apprentice curriculum integration (D-IH-73-K)

When the routed class is `eng_model_apprentice_learner`, the onboarding step §4 invokes the apprentice curriculum runbook. The integration depth:

The runbook reads from three sources:
- [`LEARNING_CHARTER.md`](../../Learning/canonicals/LEARNING_CHARTER.md) — the doctrinal frame for apprentice cohorts.
- [`HOLISTIK_RESEARCHER_ONBOARDING_CURRICULUM.md`](../../Learning/canonicals/curriculum/HOLISTIK_RESEARCHER_ONBOARDING_CURRICULUM.md) — the curriculum content (12 modules across 12 weeks; minted at I73 P2).
- [`LEARNING_OPS_BACKLOG.csv`](../../Learning/canonicals/dimensions/LEARNING_OPS_BACKLOG.csv) — the per-apprentice progress tracker.

The runbook binds the apprentice to:
- A `cohort_id` (the apprentice's start cohort, used for batch knowledge-test cadence per `SOP-PEOPLE_AGENTIC_OPERATIONS_001.md`).
- A `methodology_version_at_onboarding:` field (the methodology version current at start; preserved through the apprenticeship for audit-trail of what the apprentice was taught).
- A `curriculum_path` (which 12-module sequence; default is the Holistik Researcher onboarding sequence).

After binding, the apprentice's onboarding folder in `Think Big/Apprentices/<name>/` carries a `curriculum/` sub-folder mirroring the chosen sequence + a per-module progress file. The Learning Lead (or equivalent role-owner per baseline_organisation) takes over from People Operations Lead for the duration of the apprenticeship; offboarding (graduation or withdrawal) routes back to People Operations Lead per `SOP-ENGAGEMENT_OFFBOARDING_001.md`.

## C. Access-level routing matrix

The body §4.2 names access tier from registry + access_levels.md. The deeper detail per class:

| Class | `access_level_default` | What this means in practice |
|:---|:---|:---|
| `hourly_consultant` | 4 | Internal-team-cleared; sees most internal canonicals; methodology read-write per scope. |
| `milestone_consultant` | 4 | Same as hourly; granular per milestone if scoped engagement. |
| `percentage_collaborator` | 4 | Same as consultant; methodology contribution rights per `D-IH-73-D` shared_methodology IP class. |
| `apprentice_learner` | 3 | Internal-cleared with read-only methodology; level escalates to 4 on graduation per `LEARNING_CHARTER.md`. |
| `investor_advisor` | 3 | Internal-cleared at advisor tier; cap-table + financial canonicals; not methodology read-write unless cleared as employee. |
| `outsourced_helper` | 1-2 | Scoped to engagement deliverable only; no methodology access; per `D-IH-73-E` work-product-only. |
| `operator_self` | 5 | Founder/operator; full clearance. |

Manual override is recorded in the engagement README's frontmatter `access_level_override:` field with rationale + ratifying-decision-id. Quarterly PMO review reconciles overrides; sustained overrides may indicate the class default needs revision.

## D. Out-of-scope cross-area handoffs

Body §2 notes "Out of scope: RevOps revenue recognition; FINOPS fact inserts." The integration boundaries:

- **RevOps boundary**: Revenue recognition for `percentage_collaborator` engagements happens at RevOps spine (`Operations/RevOps/canonicals/REVOPS_PROCESS_CATALOG.yaml` per I72 P8). When People Ops onboards a percentage-collaborator engagement, the RevOps spine is notified via the `compliance.engagement_registry_mirror` projection; RevOps reads new rows on its own cadence and configures revenue-share tracking in their pipeline.
- **FINOPS boundary**: Monetary fact inserts (`finops.registered_fact`) happen on revenue-event detection (Stripe webhook → `holistika_ops.lead_intake` → FINOPS). People Ops onboarding sets up the `finops_counterparty_id:` on the engagement instance; FINOPS reads the FK on its own cadence and processes monetary events.

People Operations Lead does NOT author RevOps or FINOPS rows directly; the cross-area integration is FK-projected.

## E. Operator framing decisions encoded

- **D-IH-73-D** (I73 P1) — 7-class taxonomy that drives onboarding routing.
- **D-IH-73-K** (I73 P2) — apprentice curriculum integration deliverable.
- **D-IH-80-D** (I80 P0) — body/addendum split retrofit pilot.

## F. Cross-references

- Body file: [`SOP-ENGAGEMENT_ONBOARDING_001.md`](SOP-ENGAGEMENT_ONBOARDING_001.md).
- Workspace doctrine: [`WORKSPACE_BLUEPRINT_HOLISTIKA.md`](../../../Operations/PMO/canonicals/WORKSPACE_BLUEPRINT_HOLISTIKA.md).
- Apprentice curriculum: [`LEARNING_CHARTER.md`](../../Learning/canonicals/LEARNING_CHARTER.md), [`HOLISTIK_RESEARCHER_ONBOARDING_CURRICULUM.md`](../../Learning/canonicals/curriculum/HOLISTIK_RESEARCHER_ONBOARDING_CURRICULUM.md).
- Pattern provenance: [`PEOPLE_DESIGN_PATTERN_LIBRARY.md #pattern-sop-addendum-split`](../../canonicals/PEOPLE_DESIGN_PATTERN_LIBRARY.md#pattern-sop-addendum-split).
- I80 retrofit charter: [`docs/wip/planning/80-i79-lessons-learned/master-roadmap.md`](../../../../../../wip/planning/80-i79-lessons-learned/master-roadmap.md) §"P5".
