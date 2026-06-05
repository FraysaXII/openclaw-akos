---
initiative_id: 88
title: I88 decision log — Cross-area Ops wiring review discipline (every-area + 3-tier) × 10-pillar Holistika ReOps lens
authored: 2026-05-24
last_review: 2026-06-05
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

### D-IH-88-A — tier assignment at P1 entry

**2026-06-05** (I88 P1 FINOPS pillar sweep; operator ratification **Option C** at P1 entry gate — sequential OPS-86-15 close then P1 sweep).

**Question.** Tier assignment for each of the 7 areas at P1 entry. (Tier 1 dense weekly-to-monthly / Tier 2 quarterly / Tier 3 semi-annual-or-on-trigger.)

**Decision.** Ratify charter §1.4 defaults without amendment:

| Area | Tier |
|:---|:---|
| FINOPS | Tier 1 |
| Research OPS | Tier 1 |
| Marketing | Tier 1 (Reach) / Tier 3 (Brand sub-area) |
| Tech Lab | Tier 1–2 |
| Legal | Tier 1 (LegalOps↔FINOPS) / Tier 2 (LegalOps↔RevOps) |
| Operations | Tier 1 |
| People | Tier 1–2 |

**Owner.** Founder/CEO + System Owner.

**Rationale.** Defaults match wiring density observed in internal evidence sweep (FINOPS + Operations spines highest traffic; Brand sub-area correctly Tier 3 until Account Management RevOps tie-in matures per charter). Team Topologies interaction-modeling posture ([EXT-06] in P1 entry research) supports explicit boundary review at these cadences without collapsing areas.

**Evidence.** [`reports/p1-finops-pillar-sweep-2026-06-05.md`](reports/p1-finops-pillar-sweep-2026-06-05.md) §Tier assignment.

**Reversibility.** Partial — tier promotion/demotion via successor decision per area without re-minting I88 charter.

### D-IH-88-B — FINOPS pillar 9 + 10 closure bar at P1 sweep

**2026-06-05** (I88 P1 FINOPS pillar sweep; same ratification batch as D-IH-88-A).

**Question.** FINOPS pillar 9 (Brand-axis on FINOPS-outbound surfaces) + pillar 10 (UX of HLK-ERP FINOPS dashboard) closure criteria — what counts as PASS for each pillar at the P1 sweep?

**Decision.**

- **Pillar 9 (Brand):** **PASS** requires dual-register citation + render-trail on each outbound FINOPS artifact class. **PASS-WITH-FOLLOWUP** accepted at P1 close (doctrine binding live; FINOPS-specific outbound audit deferred to OPS-81-20 mint).
- **Pillar 10 (UX):** **CHARTER-class PASS** accepted at P1 close because `UX_DISCIPLINE.md` (D-IH-86-AX forward-charter) remains charter-only. **FULL PASS** deferred until UX discipline promotes to active + HLK-ERP FINOPS panel meets Quality Fabric scenario bar.

**Owner.** Founder/CEO + System Owner + Brand Manager (pillar 9) + UX owner at UX promotion time (pillar 10).

**Rationale.** Avoids FAIL-ramp on pillars blocked by sibling initiatives (UX charter; OPS-81-20 judgment layer) while keeping falsifiable closure targets. P1 sweep records **8 PASS + 2 PASS-WITH-FOLLOWUP** on pillars — overall P1 **PASS-WITH-FOLLOWUP**, sufficient to enter P2 without P3 canonical mint.

**Evidence.** [`reports/p1-finops-pillar-sweep-2026-06-05.md`](reports/p1-finops-pillar-sweep-2026-06-05.md) §D-IH-88-B closure criteria + per-pillar table.

**Reversibility.** Partial — CHARTER-class bar lifts automatically when UX_DISCIPLINE promotes; pillar 9 bar tightens when OPS-81-20 ships.

### D-IH-88-E — FINANCE-AREA-FULL programme inception (F0 gate)

**2026-06-05** (operator ratification: finance full-area programme + separate F0 decision row before F1 vault mint).

**Question.** Should Finance become the **second full governed O5-1 area** after Data (I93), via programme **FINANCE-AREA-FULL** (F0–F4), absorbing I88 P1 as spine evidence only?

**Decision.** **Yes** — launch FINANCE-AREA-FULL as the **primary** track. Closure bar: area matrix **≥88% / 0 gaps** + falsifiable gates **M1–M5** (see research master synthesis). I88 P2 Research OPS runs parallel after F1; I88 P3 canonical mint remains **after** F4 + P2.

**Locked homes (F1 packet §0):**

- FINOPS **CSV SSOT** — `People/Compliance/canonicals/finops/` (unchanged).
- FINOPS **doctrine** — `Finance/Governance/canonicals/FINOPS_DISCIPLINE.md`.
- Area **charter** — `Finance/canonicals/FINANCE_AREA_CHARTER.md`.

**Owner.** CFO + Business Controller (area); CPO (`pattern_area_buildout`); CDO (DC-* producer review at F2).

**Evidence.** [`reports/research-finance-full-governed-area-2026-06-05/master-synthesis.md`](reports/research-finance-full-governed-area-2026-06-05/master-synthesis.md); [`reports/intent-regression-finance-bar-2026-06-05.md`](reports/intent-regression-finance-bar-2026-06-05.md); DECISION_REGISTER row `D-IH-88-E`.

**Reversibility.** Medium — vault shell + programme can revert via git; live Stripe/finops substrate unaffected.

### D-IH-88-C (reserved; P2 entry)

**Question.** Research OPS pillar 3 (Tools/Infrastructure) + pillar 9 (Brand) + pillar 10 (UX) closure criteria — what counts as PASS for each pillar at the P2 sweep?

**Status.** Open. Ratifies at P2 entry. Likely interlocks with I75 (Research area governance) status at the time + the SUBSTRATE_LANDSCAPE_DOCTRINE active-status content.

### D-IH-88-D (reserved; P3 entry)

**Question.** Quality Fabric specialty inclusion ratification — does `CROSS_AREA_OPS_WIRING_REVIEW_DISCIPLINE.md` join the Quality Fabric §6 specialty list as the 13th or 14th specialty (depending on PWF_GOVERNANCE_DISCIPLINE mint timing, which is the planned 13th specialty per D-IH-86-CX reserved decision)?

**Status.** Open. Ratifies at P3 entry. Depends on whether the discipline operationalises any of the 5 axes (audience / channel / scenario / brand / governance) at composition time. If yes, joins QF. If no (e.g., the discipline is broader than pure quality-bar enforcement and is more usefully framed as a non-Fabric People discipline that the Fabric consumes), stays out of QF §6 and lands at `People/canonicals/` as a non-Fabric discipline.

### D-IH-88-F — Intent-Ranked Regression discipline mint (active 2026-06-05)

**Decision.** Register the **Intent-Ranked Regression** as a governed People discipline — the **value layer** above the mechanical inter-wave regression (`pattern_inter_wave_regression_discipline`). Where the inter-wave sweep asks *is everything wired?* across 13 ~equal-weight structural dimensions, this discipline asks *is what the operator cares about most still served?* and orders the sweep by an **Intent Criticality Score** (ICS = `3·intent_value + 2·time_criticality + 2·risk_reduction + 1·detection_gap`, severity-first surfaces leading). Grounded in FMEA Risk Priority Number, WSJF cost-of-delay, and Test Impact Analysis (cited in the canonical §2).

**Origin.** Operator framing 2026-06-05: *"not mechanical — take all my intents, use cases, logic, scenarios, interactions, rank them, research inside and outside, review, then regress; and if you achieved a lot, mint the workflow improvements so we can do regressions like these better and more often, no matter the seat."* Operator full-registration approval same day.

**Surfaces minted.** Discipline canonical [`INTENT_RANKED_REGRESSION_DISCIPLINE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/INTENT_RANKED_REGRESSION_DISCIPLINE.md) + `SOP-PEOPLE_INTENT_RANKED_REGRESSION_001.md` + pattern row `pattern_intent_ranked_regression` (`intent_ranked_regression_cadence`, 17th pattern class) + process row `hol_peopl_dtp_intent_ranked_regression_001` + Pydantic SSOT `akos/hlk_intent_ranked_regression.py` + runbook `scripts/intent_ranked_regression.py` (`--rank` / `--self-test`) + craft skill + active cursor rule + three `CANONICAL_REGISTRY` rows + `pre_commit` self-test (verification-profiles + release-gate). Either-seat: execution seat runs `--rank`/`--self-test`; thinking seat runs the corpus-distillation + attribution + disposition judgment.

**Worked example.** [`reports/intent-ranked-regression-2026-06-05.md`](reports/intent-ranked-regression-2026-06-05.md) — 3552 pass / 9 fail attributed to **0 new regressions**; high-intent pre-existing `area_governance` enum drift fixed-now; `OPS-88-1` opened for the deck-count de-brittle (finding F-3); eval failures cited to `OPS-90-10`.

**Reversibility.** Medium — discipline + rows revert via git; the inter-wave safety net is unaffected (this layer sits on top, never replaces it).

## Decisions deferred (not in this initiative's scope)

- **Per-area deep worked example beyond FINOPS + Research OPS** — deferred to future cycle initiatives (e.g., a future I-NN-CROSS-AREA-WIRING-MARKETING-DEEP that exercises the discipline on Marketing's Ops surface end-to-end). Charter §1.3 + R-IH-88-1 explicitly note that paragraph-framing → deep-worked-example promotion path is future-cycle work, protecting against premature canonicalisation.
- **AT-Pymes gestoría onboarding** (Layer A FINOPS ownership per D-IH-81-P) — deferred to operator action via OPS row (likely an OPS-89-* row when I89 hooks in).
- **PWF_GOVERNANCE_DISCIPLINE mint (planned 13th specialty per D-IH-86-CX)** — deferred to Commit 3 of this same Wave R+1 attack push (per I86 Wave R+1 plan).
- **UX_DISCIPLINE.md promotion from charter to active** — deferred to a future cycle (still at charter status per Wave M P5 D-IH-86-AX forward-charter); P1 pillar 10 closure criteria may bridge in the interim.
