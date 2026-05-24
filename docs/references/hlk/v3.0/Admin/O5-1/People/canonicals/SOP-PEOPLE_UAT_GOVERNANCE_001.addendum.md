---
title: SOP — People — UAT governance bar enforcement — Addendum (auditor + System Owner depth)
language: en
intellectual_kind: people-canonical-sop-addendum
sop_id: SOP-PEOPLE_UAT_GOVERNANCE_001
access_level: 5
confidence_level: A1
source_taxonomy: holistika-internal-sop
authors:
  - PMO
  - System Owner
last_review: 2026-05-24
last_review_by: PMO
last_review_decision_id: D-IH-86-CW
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-86-AV
  - D-IH-86-AS
  - D-IH-86-CW
status: active
register: internal
parent_sop: SOP-PEOPLE_UAT_GOVERNANCE_001.md
companion_to:
  - SOP-PEOPLE_UAT_GOVERNANCE_001.md
  - SOP-PEOPLE_PWF_GOVERNANCE_001.md
  - UAT_DISCIPLINE.md
  - PASS_WITH_FOLLOWUP_GOVERNANCE_DISCIPLINE.md
ssot: true
---

# SOP — People — UAT governance bar enforcement — Addendum

> Access level 5. This addendum carries the auditor + System Owner depth for the closure-UAT enforcement contract: validator scope-creep failure modes, false-positive disposition trails, historical-report migration rationale, and the durably-active promotion criteria. The executor (PMO running per-wave UAT validation) does not need this — but auditors + System Owner reference it when the bar fires misfires or when the field-test window's revocation path is invoked.
>
> Authored at I86 Wave R+1 (D-IH-86-CW; 2026-05-24) as the third instantiation of `pattern_sop_addendum_split` after the AGENTIC_OPERATIONS pair (I80 P4) and the CROSS_AREA_BREAKTHROUGH pair.

---

## A. Validator scope-creep failure modes (what auditors should expect)

The 11-section strict v1 validator has 4 known failure modes the auditor should monitor across the 3-wave field-test window (Waves S, T, U):

### A.1 False positive: section-present but section-content-empty

The validator's structural check is "section heading present + ≥ 1 line of body content after the heading". A UAT author can satisfy this by writing a one-line N/A statement under each mandatory heading — which IS the intended escape hatch per [`UAT_DISCIPLINE.md`](UAT_DISCIPLINE.md) §8.5 "may collapse to a one-line N/A statement". Auditor risk: an author satisfies the validator without satisfying the intent of the bar. Mitigation: §10 7-item operator sign-off checklist asks the operator to explicitly confirm "every N/A section's N/A reason is genuine, not avoidance". The §10 checklist IS the substantive bar; the validator IS the structural bar.

### A.2 False positive: forward-only date misclassification

The validator parses `last_review:` frontmatter to determine whether the report is forward-only (≥ 2026-05-19) or historical (< 2026-05-19). When `last_review:` is missing OR malformed (not ISO-8601), the validator defaults to **forward-only enforcement** (safer default — fail-closed). Auditor risk: a historical report missing `last_review:` gets flagged as missing forward-only sections. Mitigation: the validator's INFO output flags the missing/malformed `last_review:` as a separate finding; the auditor distinguishes "real structural drift" from "missing frontmatter that happens to trigger strict enforcement".

### A.3 False negative: report misclassified as out-of-scope

The §"When this bar applies" trigger conditions (≥ 5 phases, canonical CSV touch, sibling-repo work, I86 cluster, browser/dashboard verification) are inferred by the validator from the parent initiative's `master-roadmap.md` frontmatter + `files-modified.csv` content. When the initiative's master-roadmap lacks the phase-count field OR the files-modified is missing a repo-column entry, the validator may default to "out of scope" and skip strict enforcement. Auditor risk: a report that should have been strict-validated gets a free pass. Mitigation: each wave-close inter-wave regression sweep dimension 6 (uat_report_class_completeness) cross-checks that closed-initiative UAT reports match `compose_UAT` output; misfires surface there.

### A.4 False positive: cluster-sibling §5 cross-check on non-cluster initiative

The §5 D-IH-86-D mechanical cross-check ROW is mandatory for I86 cluster siblings. For non-cluster initiatives, the §5 row collapses to one-line N/A "not a cluster sibling". The validator's I86-membership check parses the parent initiative's `cluster_id:` frontmatter; when the frontmatter cluster_id is set to `I86` but the cluster coordinator master-roadmap §1.3 sibling table doesn't actually contain the initiative, the validator may falsely demand §5 cross-check. Mitigation: cluster_id frontmatter on initiative master-roadmaps is operator-curated; the validator emits an INFO finding when cluster_id is set but FK-resolution to the cluster coordinator's sibling table fails.

## B. Historical-report migration rationale (the §migration posture forward-only watershed)

The canonical [`UAT_DISCIPLINE.md`](UAT_DISCIPLINE.md) §"Migration posture for pre-2026-05-19 initiatives" explicitly exempts pre-2026-05-19 reports from the 11-section bar. This addendum names the rationale:

- **Historical drift cost**: backfilling ~5-10 historical UAT reports to the 11-section shape would cost ~30-60 min per report (estimated from the I77 P3→P4 amendment precedent — a single UAT amendment for brand-canon drift took ~45 min including verdict_history append + per-row re-disposition). Total cost: ~5 hours of operator + agent attention for zero forward-going benefit (the historical initiative is already closed; the UAT report's archeological function is preserved by the original verdict).
- **Audit chain integrity**: amending historical reports breaks the audit chain — a closed-initiative UAT report should NOT be retroactively rewritten unless a substantive defect is discovered (the I77 P3→P4 brand-canon drift IS such a defect; routine section-bar drift is NOT).
- **Forward-only signalling**: the watershed (D-IH-86-AS, 2026-05-20) is the formal boundary between "old bar" and "new bar". The validator respects this boundary mechanically; the cursor rule respects it doctrinally.

Auditor implication: when the validator's INFO output flags a historical report as non-strict, the auditor records "historical-exempt per §migration posture" rather than opening a remediation issue.

## C. 3-wave field-test window — operator-side revocation path (D-IH-86-CW-revoke)

The promotion-with-revocability framing (meta4-b ratification) requires an explicit revocation path that the operator can invoke without re-litigating the original promotion decision. The path:

### C.1 Trigger conditions for D-IH-86-CW-revoke

Operator may invoke `D-IH-86-CW-revoke` when **any** of:

- ≥ 2 of the 3 field-test waves (S, T, U) produce validator misfires (false positives OR false negatives) attributable to validator scope, not author error.
- The 11-section bar produces sustained author friction (≥ 50% of in-scope UATs in a wave require operator-explicit override to satisfy the bar) — i.e., the bar is over-fitted to a single precedent (Wave R closure) and doesn't generalize.
- A net-new failure mode emerges across Waves S+T+U that the strict-v1 validator cannot mechanically catch (e.g., the §5 cross-check pattern needs amending; the verdict enum needs extension).

### C.2 Mechanical effects of revocation

When invoked, `D-IH-86-CW-revoke` triggers:

1. **UAT_DISCIPLINE.md frontmatter flips** `status: active` → `status: charter-revoked-pending-v2`.
2. **`scripts/validate_uat_report.py` strict mode demotes** to INFO-only across all closure UATs until v2 ships.
3. **A successor decision row `D-IH-86-CW-v2`** mints the v2 scope (which sections to keep strict, which to demote to INFO, which to add).
4. **The cursor rule `akos-uat-discipline.mdc` RULE 3 amends** to reflect the v2 scope OR maintains a contra-precedent §"Revocation history" sub-section.
5. **A new field-test window** opens for the v2 bar (Waves U+1, U+2, U+3).

### C.3 Successful field-test (no revocation)

If Waves S, T, U all close with zero validator misfires AND zero sustained author friction, the operator records a closure decision `D-IH-86-CW-durable` in DECISION_REGISTER.csv noting "3-wave field-test window cleared; v1 bar promoted to durably-active without revocation". The status remains `active`; the addendum's §C section is preserved as historical context for the v1 promotion-with-revocability pattern.

## D. Interaction with PASS_WITH_FOLLOWUP_GOVERNANCE_DISCIPLINE (12th specialty)

This SOP and [`SOP-PEOPLE_PWF_GOVERNANCE_001.md`](SOP-PEOPLE_PWF_GOVERNANCE_001.md) (the 12th specialty paired SOP, minted in the same Wave R+1 commit-triple) are **structurally complementary**:

- This SOP enforces UAT closure quality at mint-time (validator runs when UAT is being authored).
- The PWF SOP enforces PWF discipline at audit-time (validator runs to scan historical UAT reports for PWF abuse pattern: PWF verdicts without `verdict_followup_rationale:`; PWF verdicts whose followup never resolved; PWF verdicts disguising scope-creep).

The two validators share a Pydantic chassis: [`akos/hlk_uat_report.py`](../../../../../../akos/hlk_uat_report.py) provides the frontmatter schema; the PWF validator extends with `PWFFinding` + `PWFAbusePattern` enums. When a UAT report mints with verdict=PASS-WITH-FOLLOWUP AND no `verdict_followup_rationale:`, BOTH validators FAIL (UAT validator: missing-mandatory-frontmatter; PWF validator: PWF-without-rationale-anti-pattern).

Auditor implication: a finding flagged by one validator should be cross-checked against the other before disposition — the failure may be a single structural drift that both validators surface from different angles.

## E. Process-catalog row metadata (auditor-specific fields)

The `hol_peopl_dtp_uat_governance_001` row in [`process_list.csv`](../Compliance/canonicals/process_list.csv) carries auditor-relevant fields beyond the executor-facing description:

- **`co_owner_role: AIC`** (encoded in instructions text per ex4-c ratification) — confirms the SOP is consumable by AIC role_owner (Madeira; future AICs) without operator hand-holding.
- **`cadence: event_triggered`** — fires at UAT report commit AND at wave-close commit AND at canonical-CSV mint commit (per akos-quality-fabric.mdc + akos-planning-traceability.mdc trigger conditions union).
- **`inherited_pattern_id: pattern_uat_class_taxonomy`** — the design pattern this process realizes; auditor traces the pattern's `consumer_areas:` to confirm cross-area inheritance.
- **`last_review_decision_id: D-IH-86-CW`** — the ratifying decision row.
- **`methodology_version_at_review: v3.1`** — vault version this row was authored against.

## Cross-references

- Parent SOP: [`SOP-PEOPLE_UAT_GOVERNANCE_001.md`](SOP-PEOPLE_UAT_GOVERNANCE_001.md).
- Canonical doctrine: [`UAT_DISCIPLINE.md`](UAT_DISCIPLINE.md).
- 12th specialty pair: [`PASS_WITH_FOLLOWUP_GOVERNANCE_DISCIPLINE.md`](PASS_WITH_FOLLOWUP_GOVERNANCE_DISCIPLINE.md) + [`SOP-PEOPLE_PWF_GOVERNANCE_001.md`](SOP-PEOPLE_PWF_GOVERNANCE_001.md).
- Pattern: `pattern_uat_class_taxonomy` in [`PEOPLE_DESIGN_PATTERN_REGISTRY.csv`](../Compliance/canonicals/dimensions/PEOPLE_DESIGN_PATTERN_REGISTRY.csv).
- Cursor rule: [`akos-uat-discipline.mdc`](../../../../../../.cursor/rules/akos-uat-discipline.mdc).
- Paired skill: [`.cursor/skills/uat-discipline-craft/SKILL.md`](../../../../../../.cursor/skills/uat-discipline-craft/SKILL.md).
- Sister addendum precedent: [`SOP-PEOPLE_AGENTIC_OPERATIONS_001.addendum.md`](SOP-PEOPLE_AGENTIC_OPERATIONS_001.addendum.md), [`SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.addendum.md`](SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.addendum.md).

@docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/SOP-PEOPLE_UAT_GOVERNANCE_001.md
@docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/UAT_DISCIPLINE.md
