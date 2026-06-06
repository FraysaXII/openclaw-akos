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
  - D-IH-73-F
  - D-IH-73-L
  - D-IH-80-D
parent_sop: SOP-ENGAGEMENT_OFFBOARDING_001.md
companion_to:
  - SOP-ENGAGEMENT_OFFBOARDING_001.md
ssot: true
---

# SOP-ENGAGEMENT_OFFBOARDING_001 — Addendum (Investor-advisor round-review depth + Methodology IP filing-time matrix + Legal Counsel handoff)

> Access level 5. Authored at I80 P5 (D-IH-80-D Option B retrofit pilot, 2026-05-16). The body executor needs to know *what* to check at offboarding; this addendum carries the round-review depth (cap-table sanity + vesting cadence + SAFE/convertible event tracking), the Methodology IP brand-vs-name filing-time matrix per `D-IH-73-F`, the Legal Counsel handoff posture, and the four-channel archival mechanics that Legal Counsel / Founder / System Owner reference.

## A. Investor-advisor round-review depth (D-IH-73-L)

The body §4.2 names "round review checklist (cap table, vesting events, advisor obligations)" without specifying the auditor-facing depth.

### A.1 Cap-table sanity check

For `eng_model_investor_advisor` engagements, the cap-table state must be reviewed at every round. The check covers:

- **Pre-round table** vs **post-round table**: the differences should reflect only the round's transactions (new investments + advisor grants + exercises). Discrepancies indicate either an unrecorded transaction or a state-tracking error.
- **Total ownership** across all stakeholders: must sum to 100%. Discrepancies are immediate-stop blockers; do not archive offboarding until corrected.
- **Founder ownership floor**: per the founder's own pre-round commitments (varies by engagement; recorded in the engagement README); below-floor values trigger immediate Legal Counsel + Founder review.
- **Advisor grant vesting calendar**: each advisor grant has a cliff date + vesting schedule + acceleration triggers. The review confirms the calendar is current and that no triggers have fired silently.

### A.2 SAFE / convertible note conversion event tracking

When a SAFE or convertible note converts (typically at the next priced round or on exit), the conversion event triggers:

1. **Cap-table update** to reflect the converted equity grant.
2. **Counterparty role transition** from "investor (note)" to "investor (equity holder)" — recorded in `FINOPS_COUNTERPARTY_REGISTER.csv` and in the engagement README.
3. **Tax-form trigger**: depending on jurisdiction, conversion may trigger reporting requirements; FINOPS Lead handles via standard tax-form workflow.
4. **Engagement model re-classification consideration**: a converted SAFE holder may have changed posture (e.g., from `investor_advisor` to a passive equity holder); engagement model re-classification per `SOP-ENGAGEMENT_HIRING_LIFECYCLE_001.md` if posture has structurally changed.

### A.3 Advisor obligations review

Per the advisor grant agreement, advisors typically have ongoing obligations: minimum hours/quarter of engagement, attendance at board meetings, specific deliverable cadence. The review confirms:

- All obligations met for the period reviewed.
- Any gaps recorded (with reason: founder waiver / advisor unavailability / scope drift).
- Vesting acceleration / deceleration triggers from obligation gaps applied per the grant agreement.

Sustained obligation gaps may trigger renegotiation or grant cancellation; both routes go through Legal Counsel.

## B. Methodology IP brand-vs-name filing-time matrix (D-IH-73-F)

When an advisor contributes IP that becomes part of Holistika's methodology — typically a named framework, named methodology, named pattern — the body §4.3 defers to "D-IH-73-F matrix at filing time (no premature brand decisions)." The matrix detail:

The brand-vs-name decision asks: when filing a trademark or registering a methodology IP claim, does the filing carry the advisor's name OR the Holistika brand?

**Default posture** (most cases): Holistika brand. The advisor receives attribution in the methodology documentation (e.g., "the X framework, contributed by Advisor Y at Holistika") but the trademark filing is in the Holistika name. The advisor's grant agreement compensates the contribution.

**Exception posture** (rare; requires explicit `D-IH-NN-X` decision): advisor's name. When the advisor brings a pre-existing named methodology that they have substantial reputation invested in (e.g., a methodology they have published under their name in academic or industry literature), filing under Holistika brand alone may misrepresent attribution. In this case the filing is co-branded or in the advisor's name with Holistika as exclusive licensee.

**Filing-time matrix** is applied per filing event, not at engagement intake. The reason: advisor methodology contributions accrete over the engagement; the brand-vs-name decision should be made when the filing is concrete, not speculatively at engagement start. The body's posture — "no premature brand decisions" — preserves this discipline.

## C. Legal Counsel handoff posture

The body §2 notes "Does NOT provide legal advice — Legal Counsel remains authoritative for instruments." The boundary detail:

- People Operations Manager executes the offboarding mechanics (revoke access, archive folders, run round review checklist).
- Legal Counsel executes anything that touches a legal instrument (cap-table changes, SAFE conversion paperwork, advisor grant cancellation, methodology IP filing, dispute resolution).
- The handoff is via a per-engagement Legal Counsel checklist row in the engagement README's frontmatter; People Operations Manager populates the row at offboarding start; Legal Counsel signs off when their checks are complete.

When Legal Counsel is unavailable (small-engagement offboardings; founder-attorney-of-record cases), the body §6 failure-mode of "Missing Legal sign-off on instrument changes" applies; archive promotion is blocked until sign-off.

## D. Four-channel archival mechanics

Offboarding archives the engagement across all four persistence channels per [`WORKSPACE_BLUEPRINT_HOLISTIKA.md`](../../../Operations/PMO/canonicals/WORKSPACE_BLUEPRINT_HOLISTIKA.md):

- **Git canonical**: tag the engagement folder at offboarding date (`engagement-<name>-offboarded-YYYY-MM-DD`); folder remains in git but read-only by convention; future revisions are forbidden without operator approval.
- **Drive operational**: export the engagement folder as a zip archive to a long-term storage drive; original folder moved to `_archived/` sub-folder; access permissions revoked except for legal hold cases.
- **SQL mirror**: `compliance.engagement_registry_mirror.status` flips to `archived`; the mirror retains the row for historical join integrity.
- **HLK-ERP**: engagement panel moves to "Archived engagements" view; surface from active dashboard.

The four-channel archive is reconciled quarterly per PMO cadence; drift between channels at archive time is an immediate audit finding.

## E. Operator framing decisions encoded

- **D-IH-73-F** (I73 P8) — methodology IP brand-vs-name filing-time matrix.
- **D-IH-73-L** (I73 P5) — investor-advisor round review process.
- **D-IH-80-D** (I80 P0) — body/addendum split retrofit pilot.

## F. Cross-references

- Body file: [`SOP-ENGAGEMENT_OFFBOARDING_001.md`](SOP-ENGAGEMENT_OFFBOARDING_001.md).
- Sibling lifecycle SOPs: [`SOP-ENGAGEMENT_HIRING_LIFECYCLE_001.md`](SOP-ENGAGEMENT_HIRING_LIFECYCLE_001.md), [`SOP-ENGAGEMENT_ONBOARDING_001.md`](SOP-ENGAGEMENT_ONBOARDING_001.md), [`SOP-ENGAGEMENT_PAYROLL_OPS_001.md`](SOP-ENGAGEMENT_PAYROLL_OPS_001.md).
- Methodology IP path (D-IH-73-F deliverable): looking forward to I73 P8 deliverable `METHODOLOGY_IP_MINTING_PATH` at Marketing/Brand canonicals when authored.
- Workspace doctrine: [`WORKSPACE_BLUEPRINT_HOLISTIKA.md`](../../../Operations/PMO/canonicals/WORKSPACE_BLUEPRINT_HOLISTIKA.md).
- Pattern provenance: [`PEOPLE_DESIGN_PATTERN_LIBRARY.md #pattern-sop-addendum-split`](../../canonicals/PEOPLE_DESIGN_PATTERN_LIBRARY.md#pattern-sop-addendum-split).
- I80 retrofit charter: [`docs/wip/planning/80-i79-lessons-learned/master-roadmap.md`](../../../../../../wip/planning/80-i79-lessons-learned/master-roadmap.md) §"P5".
