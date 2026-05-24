---
initiative_id: 88
title: I88 decision log — Cross-area Ops wiring review discipline (every-area + 3-tier) × 10-pillar Holistika ReOps lens
authored: 2026-05-24
last_review: 2026-05-24
audience: J-OP;J-AIC
access_level: 5
language: en
---

# I88 — Decision log

> Per `akos-planning-traceability.mdc` Governance Content Requirements: every initiative's decision-log records the choices made + deferred. IDs follow `D-IH-88-<X>` convention; lineage decisions from parent initiatives (I81 + I86) cited but not re-minted here.

## Lineage decisions (inherited from I81 + I86; reference only)

- **D-IH-81-O** (2026-05-22, I81 Bundle B-2 synthesis Decision C) — operator novel framing at FINOPS end-to-end synthesis ratification gate: *"add regressions or continuous revisions or enhancements or backfill for all of this. Because FINOPS is a backbone... review each area's OPS to ensure proper wiring maintenance"*. This is the **discipline-spawning decision**. Original framing carried backbone-areas-only scope (FINOPS / PeopleOps / RevOps / LegalOps).
- **D-IH-81-P** (2026-05-23, I81 internal-first FINOPS posture amendment) — operator amended A3 activation gate from "CFOaaS-firm-contracted OR operator-declares-interim-ownership" to "three-layer ownership posture model" (Layer A compliance bookkeeping + Layer B judgment/reporting/policy + Layer C external recruitment activation triggers). Removed CFOaaS-default. Cross-area sweeps inherit agent-recommends-outsource-path failure-mode sanity-check per OPS-81-21.
- **D-IH-81-T** (2026-05-23, I81 Wave R Bundle C amendment) — operator s4 second-novel framing: *"every area gets cross-area wiring review at its own hierarchy + ownership level; no such thing as small or big, only backfilling data; all areas deserve cross-area review with their hierarchy + each thing has its owner; improve integrity where it counts"*. **Supersedes** D-IH-81-O's backbone-only scope. Adds the 3-tier review-density framing (Tier 1 dense wiring spines / Tier 2 active but quieter / Tier 3 reference-frame areas). Adds the every-area scope. Amends A2 activation gate to "exercised on FINOPS + ONE additional area's Ops surface (any area)".

## I88-specific decisions

### D-IH-86-CW — promotion + activation + spawning

**2026-05-24** (I86 Wave R+1 OPS-86-22 + OPS-86-23 attack gate; META1..META6 ratification batch).

**Question (META4-b component).** Promote UAT_DISCIPLINE.md from `status: charter` to `status: active` with a 3-wave field-test window? (clean PASS now + explicit monitoring obligation, not a PWF deferral)

**Question (META1-a component).** Use Boulton 8-pillar ReOps frame for Research OPS substrate candidate (industry-default) OR extend to 10 pillars with Brand (pillar 9) + UX (pillar 10) (Holistika-specific extension)?

**Question (META2-b component).** Bundle C activation scope for I88: backbone-only (D-IH-81-O original) OR all-7-areas-with-2-deep-worked-examples (D-IH-81-T amended; Research OPS + FINOPS as deep examples + 5 paragraph framings)?

**Decision.**
- META4-b: PASS (UAT_DISCIPLINE promoted to active; 3-wave field-test window opened; machine-readable `field_test_window:` frontmatter block; revocation path documented in addendum).
- META1-a: Extend to 10 pillars (Brand + UX as Holistika-specific pillars 9 + 10).
- META2-b: All-7-areas-with-2-deep-worked-examples (Research OPS + FINOPS deep; Marketing + Tech Lab + Legal + Operations + People paragraph framings).

**Owner.** Founder/CEO + PMO (META4-b primary owner = System Owner per UAT_DISCIPLINE last_review_decision_id).

**Rationale.** Operator's META1-a verbatim selection of `m1-a-extend-8pillar` reflects the Holistika-specific intuition that research outputs are brand-touching by default and UX of consumer surfaces determines whether research lands. META2-b's all-7-areas choice operationalises D-IH-81-T's s4 framing in concrete deliverable shape (charter §1.4 paragraph framings for the 5 areas not yet deep-worked-example status). META4-b's clean-PASS-with-FTW choice avoids the "PWF discipline collapse" risk that the operator named at PC1 (Pre-Commit 1) round 2 questioning.

**Cited canonicals.** [`UAT_DISCIPLINE.md`](../../references/hlk/v3.0/Admin/O5-1/People/canonicals/UAT_DISCIPLINE.md), [`HOLISTIKA_QUALITY_FABRIC.md`](../../references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_QUALITY_FABRIC.md), [`_candidates/i-nn-research-ops-substrate.md`](../_candidates/i-nn-research-ops-substrate.md), [`_candidates/i-nn-cross-area-ops-wiring-review.md`](../_candidates/i-nn-cross-area-ops-wiring-review.md), [`_candidates/i-nn-research-area-cross-area-topic-intent-improvement.md`](../_candidates/i-nn-research-area-cross-area-topic-intent-improvement.md).

**Reversibility.** Partial. UAT_DISCIPLINE promotion has documented revocation path (D-IH-86-CW-revoke template per addendum) and is reversible via charter status flip + frontmatter `field_test_window.status: revoked`. Bundle C activation as I88 is reversible via INITIATIVE_REGISTRY status flip to `paused` or `cancelled`, but the deliverables already minted (this commit) stay as governance artifacts. The 10-pillar +2 extension is reversible via successor decision (R-IH-88-2 mitigation path).

**Forward charter.** P1 (FINOPS pillar sweep) + P2 (Research OPS pillar sweep) + P3 (discipline canonical mint per quartet specialty contract). 4 new decision IDs reserved (D-IH-88-A through D-IH-88-D per master-roadmap §3 preview).

### D-IH-88-A (reserved; P1 entry)

**Question.** Tier assignment for each of the 7 areas at P1 entry. (Tier 1 dense weekly-to-monthly / Tier 2 quarterly / Tier 3 semi-annual-or-on-trigger.)

**Status.** Open. Ratifies at P1 entry. Default per charter §1.4 paragraph framings: FINOPS Tier 1; Research OPS Tier 1; Marketing Reach Tier 1 ↔ Brand Tier 3; Tech Lab Tier 1-to-2; Legal Tier 1 (LegalOps↔FINOPS) ↔ Tier 2 (LegalOps↔RevOps); Operations Tier 1 (PMO↔every-area); People Tier 1 (People↔every-area pairing).

### D-IH-88-B (reserved; P1 entry)

**Question.** FINOPS pillar 9 (Brand-axis on FINOPS-outbound surfaces) + pillar 10 (UX of HLK-ERP FINOPS dashboard) closure criteria — what counts as PASS for each pillar at the P1 sweep?

**Status.** Open. Ratifies at P1 entry. Depends on the forward-charter `UX_DISCIPLINE.md` (D-IH-86-AX) status (still at charter status; if still charter at P1 entry, the pillar 10 closure criteria may be CHARTER-class PASS rather than FULL PASS).

### D-IH-88-C (reserved; P2 entry)

**Question.** Research OPS pillar 3 (Tools/Infrastructure) + pillar 9 (Brand) + pillar 10 (UX) closure criteria — what counts as PASS for each pillar at the P2 sweep?

**Status.** Open. Ratifies at P2 entry. Likely interlocks with I75 (Research area governance) status at the time + the SUBSTRATE_LANDSCAPE_DOCTRINE active-status content.

### D-IH-88-D (reserved; P3 entry)

**Question.** Quality Fabric specialty inclusion ratification — does `CROSS_AREA_OPS_WIRING_REVIEW_DISCIPLINE.md` join the Quality Fabric §6 specialty list as the 13th or 14th specialty (depending on PWF_GOVERNANCE_DISCIPLINE mint timing, which is the planned 13th specialty per D-IH-86-CX reserved decision)?

**Status.** Open. Ratifies at P3 entry. Depends on whether the discipline operationalises any of the 5 axes (audience / channel / scenario / brand / governance) at composition time. If yes, joins QF. If no (e.g., the discipline is broader than pure quality-bar enforcement and is more usefully framed as a non-Fabric People discipline that the Fabric consumes), stays out of QF §6 and lands at `People/canonicals/` as a non-Fabric discipline.

## Decisions deferred (not in this initiative's scope)

- **Per-area deep worked example beyond FINOPS + Research OPS** — deferred to future cycle initiatives (e.g., a future I-NN-CROSS-AREA-WIRING-MARKETING-DEEP that exercises the discipline on Marketing's Ops surface end-to-end). Charter §1.3 + R-IH-88-1 explicitly note that paragraph-framing → deep-worked-example promotion path is future-cycle work, protecting against premature canonicalisation.
- **AT-Pymes gestoría onboarding** (Layer A FINOPS ownership per D-IH-81-P) — deferred to operator action via OPS row (likely an OPS-89-* row when I89 hooks in).
- **PWF_GOVERNANCE_DISCIPLINE mint (planned 13th specialty per D-IH-86-CX)** — deferred to Commit 3 of this same Wave R+1 attack push (per I86 Wave R+1 plan).
- **UX_DISCIPLINE.md promotion from charter to active** — deferred to a future cycle (still at charter status per Wave M P5 D-IH-86-AX forward-charter); P1 pillar 10 closure criteria may bridge in the interim.
