---
language: en
status: active
canonical: true
role_owner: People Operations Manager
co_owner_role: Legal Counsel
area: People
entity: Holistika
intellectual_kind: sop-addendum
authored: 2026-05-16
last_review: 2026-05-16
last_review_by: People Operations Manager
last_review_decision_id: D-IH-80-D
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-73-D
  - D-IH-73-E
  - D-IH-80-D
parent_sop: SOP-ENGAGEMENT_HIRING_LIFECYCLE_001.md
companion_to:
  - SOP-ENGAGEMENT_HIRING_LIFECYCLE_001.md
ssot: true
---

# SOP-ENGAGEMENT_HIRING_LIFECYCLE_001 — Addendum (Legal templates + IP clause matrix + workspace blueprint depth)

> Access level 5. Authored at I80 P5 (D-IH-80-D Option B retrofit pilot, 2026-05-16) as a paired-file companion. The body executor needs to know *how* to classify a new engagement and route legal templates; this addendum carries the decision-tree depth — IP clause class semantics, retribution-pattern enum interpretation, multi-class ambiguity adjudication, workspace-folder shape rationale — that Legal Counsel / People Operations Manager reference when classification is genuinely ambiguous.

## A. ENGAGEMENT_MODEL_REGISTRY columns the classifier reads

The body's §3 names registry rows have `retribution_pattern`, `soc_posture`, `access_level_default`, `ip_clause_class`. The auditor-facing detail per column:

### A.1 `retribution_pattern` enum (5 values)

- `hourly` — paid per hour worked (consultant patterns; `hourly_consultant`).
- `milestone` — paid per defined deliverable milestone (`milestone_consultant`).
- `percentage` — paid as percentage of revenue or deal close (`percentage_collaborator`).
- `equity` — paid in equity grant + vesting cadence (`investor_advisor` primarily).
- `fixed` — flat retention or honorarium with no per-unit semantic (`outsourced_helper` capped budget).

When an engagement does not cleanly fit one pattern (e.g., milestone + percentage hybrid), the convention is to pick the *primary* pattern + record the secondary in the engagement README's frontmatter. The class assignment follows the primary pattern. Hybrid retribution structures that recur warrant a future I-NN proposal to extend the enum.

### A.2 `soc_posture` enum (3 values)

- `full_trust` — collaborator has full methodology access (only the operator + named role-owners + cleared employees in this class).
- `scoped` — collaborator has scoped knowledge access for the duration of the engagement; no methodology tutoring; deliverables are work-product (`outsourced_helper` per `D-IH-73-E`).
- `methodology_restricted` — collaborator engages with methodology in read-only mode (apprentice learners; investors-as-advisors before becoming cleared).

The SOC posture maps directly to the access-level routing in [`access_levels.md`](../../Compliance/canonicals/access_levels.md): `full_trust` → level 5; `scoped` → levels 1-2; `methodology_restricted` → levels 3-4.

### A.3 `ip_clause_class` enum (3 values)

- `work_product_only` — collaborator delivers work product; IP transfers to Holistika at delivery; no methodology contribution claim. NDA + standard IP assignment template.
- `shared_methodology` — collaborator engages with methodology and may contribute refinements; refinements become Holistika IP; collaborator retains attribution. NDA + co-contribution template.
- `ip_contributor` — collaborator brings IP that becomes part of Holistika's methodology; brand-vs-name decision per `D-IH-73-F` filing-time matrix; revenue-share or equity-share negotiated separately.

`work_product_only` is the default for outsourced-helper, hourly-consultant, and milestone-consultant. `shared_methodology` is the default for percentage-collaborator and apprentice-learner (after graduation). `ip_contributor` is rare; flagged for Methodology IP filing-time review per `D-IH-73-F`.

## B. Multi-class ambiguity adjudication

When a new engagement's shape does not cleanly map to one class:

1. **Identify primary axis.** Which axis (retribution / SOC / IP / access-level) is most load-bearing for this engagement? Pick the class that matches that axis.
2. **Record secondary axes in the engagement README frontmatter.** This preserves the audit trail for why the primary class was chosen.
3. **Escalate to PMO + Ethics if SOC conflict.** When SOC posture conflicts with the operator's narrative for the engagement (e.g., "this advisor is `methodology_restricted` per the class but will need `full_trust` for the work they're doing"), the conflict is structural; PMO + Ethics review.
4. **Check for class-extension trigger.** If three or more engagements present the same multi-class ambiguity in a quarter, that is the trigger for a new class proposal per `SOP-ENGAGEMENT_MODEL_REGISTRY_MAINTENANCE_001.md` §4.

## C. Legal template routing (Templates/Legal/ folder map)

The body's §3 references `default_legal_template` cells; the actual mapping lives in the Legal templates folder structure:

| Class | Default NDA template | Default IP clause | Default retribution clause |
|:---|:---|:---|:---|
| `hourly_consultant` | `NDA_consultant_001.md` | `IP_work_product_only_001.md` | `Retribution_hourly_001.md` |
| `milestone_consultant` | `NDA_consultant_001.md` | `IP_work_product_only_001.md` | `Retribution_milestone_001.md` |
| `percentage_collaborator` | `NDA_collaborator_001.md` | `IP_shared_methodology_001.md` | `Retribution_revenue_share_001.md` |
| `apprentice_learner` | `NDA_apprentice_001.md` | `IP_methodology_restricted_001.md` | `Retribution_apprentice_001.md` |
| `investor_advisor` | `NDA_investor_001.md` | `IP_advisor_001.md` (filing-time matrix) | `Retribution_advisor_grant_001.md` |
| `outsourced_helper` | `NDA_outsourced_001.md` | `IP_work_product_only_001.md` | `Retribution_outsourced_capped_001.md` |
| `operator_self` | n/a | n/a | n/a |

The classifier in §4 of the body picks the engagement_model_id; the runbook reads the model registry row's `default_legal_template:` cells; the runbook drops the templates into the engagement folder. Manual override lives in the engagement README; the override is recorded for audit.

## D. Workspace folder skeleton — Think Big/Clients/ vs Think Big/Advisers/ vs Think Big/Employees/

Per [`WORKSPACE_BLUEPRINT_HOLISTIKA.md`](../../../Operations/PMO/canonicals/WORKSPACE_BLUEPRINT_HOLISTIKA.md) §3-§4, the engagement folder shape depends on the class:

- `hourly_consultant` / `milestone_consultant` / `percentage_collaborator` → `Think Big/Clients/<engagement-name>/_engagement-template/` (4-channel persistence: git / Drive / SQL mirror / HLK-ERP).
- `apprentice_learner` → `Think Big/Apprentices/<apprentice-name>/_engagement-template/` (with curriculum sub-folder per `LEARNING_CHARTER.md`).
- `investor_advisor` → `Think Big/Advisers/<advisor-name>/_engagement-template/` (with cap-table + grant-vesting sub-folders).
- `outsourced_helper` → `Think Big/Outsourced/<helper-name>/` (no `_engagement-template/`; flat folder; SOC-restricted).
- `operator_self` → no folder; covered by Holistika operator-self artefacts in repo root.

The classifier picks the class; the runbook copies the correct skeleton. Folder shape mismatch is an audit finding; quarterly PMO review reconciles.

## E. Operator framing decisions encoded

- **D-IH-73-D** (I73 P1) — 7-class taxonomy.
- **D-IH-73-E** (I73 P3) — outsourced-helper work-product-only doctrine + `scoped` SOC posture default.
- **D-IH-73-F** (I73 P8) — methodology IP brand-vs-name filing-time matrix (deferred until filing-time review for `ip_contributor` class).
- **D-IH-80-D** (I80 P0) — body/addendum split retrofit pilot Option B.

## F. Cross-references

- Body file: [`SOP-ENGAGEMENT_HIRING_LIFECYCLE_001.md`](SOP-ENGAGEMENT_HIRING_LIFECYCLE_001.md).
- Sibling SOPs (lifecycle): [`SOP-ENGAGEMENT_ONBOARDING_001.md`](SOP-ENGAGEMENT_ONBOARDING_001.md) (downstream), [`SOP-ENGAGEMENT_OFFBOARDING_001.md`](SOP-ENGAGEMENT_OFFBOARDING_001.md), [`SOP-ENGAGEMENT_PAYROLL_OPS_001.md`](SOP-ENGAGEMENT_PAYROLL_OPS_001.md).
- Workspace doctrine: [`WORKSPACE_BLUEPRINT_HOLISTIKA.md`](../../../Operations/PMO/canonicals/WORKSPACE_BLUEPRINT_HOLISTIKA.md).
- Pattern provenance: [`PEOPLE_DESIGN_PATTERN_LIBRARY.md #pattern-sop-addendum-split`](../../canonicals/PEOPLE_DESIGN_PATTERN_LIBRARY.md#pattern-sop-addendum-split).
- I80 retrofit charter: [`docs/wip/planning/80-i79-lessons-learned/master-roadmap.md`](../../../../../../wip/planning/80-i79-lessons-learned/master-roadmap.md) §"P5".
