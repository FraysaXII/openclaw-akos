---
initiative_id: INIT-OPENCLAW_AKOS-73
title: I73 risk register
status: active
authored: 2026-05-15
last_review: 2026-05-15
role_owner: PMO
language: en
---

# I73 risk register

> Detailed risk register companion to the Cursor plan §"Risk-register preview (R-IH-73-1..10)". Each entry below carries full mitigation detail + owner + close-out phase. The Cursor plan body holds the queryable preview table; this file holds the rationale + mitigation breakdown.

## R-IH-73-1 — 8-strand mega-initiative pause-fatigue at P3+

- **Likelihood.** High.
- **Impact.** Med.
- **Description.** I73 spans 11 phases across ~6-8 calendar weeks. By P3-P4, operator-side pause-fatigue is the modal failure mode for long initiatives (per [`akos-agent-checkpoint-discipline.mdc`](../../../../.cursor/rules/akos-agent-checkpoint-discipline.mdc) §"What pause-point fatigue looks like"). If every phase carries a hard operator pause point, the operator stops engaging substantively by P3 and rubber-stamps the rest.
- **Mitigation.**
  - Front-load substantive operator ratification at P0 (this charter, ratified 2026-05-15) and P1 (canonical-CSV gate; mandatory). After P1 lands, the architecture is operator-approved and downstream pauses become "did you do what you said?" reviews — much faster.
  - Apply per-phase **inline-ratify gates** (AskQuestion in same chat) for conundrums C-73-1..C-73-8 rather than file-based operator-pause-records. Per `akos-inline-ratification.mdc`, conundrums get surfaced inline; operator-pause-records reserved only for hard canonical-CSV / brand / trademark gates (P1, P6, P8 here).
  - **Soft-pause auto-clear**: if operator silence ≥ 24h AND validators clean, the phase commits with the recommended default and logs `decision_source: agent_inline_default` per `akos-inline-ratification.mdc` §6.5.
- **Owner.** PMO + Founder (front-load review investment).
- **Close-out.** R closes when I73 closes (P11) without operator-perceived pause-fatigue. Tracked in `reports/p11-closure-uat-<date>.md` operator UAT row.

## R-IH-73-2 — ENGAGEMENT_MODEL_REGISTRY CSV gate becomes contentious mid-P1

- **Likelihood.** Med.
- **Impact.** High.
- **Description.** The P1 PAUSE POINT lands a canonical-CSV gate for 7 enum rows + 17-col ENGAGEMENT_REGISTRY extension + ~6-8 `process_list.csv` rows + Supabase migration. The taxonomy is pre-ratified at P0 (D-IH-73-D), but the operator may surface late-arriving objections at the canonical-CSV gate AskQuestion (e.g., "actually, percentage_collaborator should be three sub-classes").
- **Mitigation.**
  - D-IH-73-D ratified at P0 with operator brief 2026-05-15 as primary evidence (case codenames Bâtard / Mark-II / Alias V / RCD Legal / L'Oréal arrangement explicitly mapped to the 7 classes).
  - Pre-P1 self-checkpoint (`sc-pre-p1-<date>.md`) reviews the canonical CSV schema + sample rows + Pydantic SSOT BEFORE the canonical-CSV gate AskQuestion. Operator reads schema + rows + Pydantic field list in a single skimmable artefact.
  - If operator surfaces late-arriving objections, **STOP-AND-CLARIFY posture** per `akos-inline-ratification.mdc` §6.2: write a clarification report, do NOT commit canonical CSV with unratified rows.
- **Owner.** People Operations Manager (data owner) + PMO.
- **Close-out.** P1 commit + operator approval in writing in `decision-log.md` D-IH-73-H..N.

## R-IH-73-3 — Methodology IP minting collides with BRAND_HIERARCHY_AND_TRADEMARK_SCOPE trademark posture

- **Likelihood.** Med.
- **Impact.** High.
- **Description.** P8 mints `METHODOLOGY_IP_MINTING_PATH.md` with a brand-vs-name decision matrix. The matrix may collide with [`BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md`](../../../references/hlk/v3.0/Admin/O5-1/People/Legal/BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md) Branded House trademark posture (e.g., per-jurisdiction Nice-class scope; cobranding pattern).
- **Mitigation.**
  - D-IH-73-F deferred-with-criteria-matrix (per-asset filing decision at filing time) keeps the brand vs personal-name choice flexible per asset.
  - Coordinate with Legal at P8 (Legal sub-role exists per [`PEOPLE_AREA_RESTRUCTURE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/PEOPLE_AREA_RESTRUCTURE.md)); P8 inline-ratify gate carries operator approval requirement for the criteria matrix wording.
  - Cross-link [`LOGIC_CHANGE_LOG.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/LOGIC_CHANGE_LOG.md) BT-01 brand-as-shield framing as the authoritative anchor (versioning founder understanding under brand umbrella precedes solid proof).
- **Owner.** Brand & Narrative Manager + Founder + Legal (P8 coordination).
- **Close-out.** P8 (criteria matrix ratified). Per-asset filings outside I73 scope; closes when first asset files under matrix.

## R-IH-73-4 — KB human-readability re-architects too aggressively, breaking existing KB consumers

- **Likelihood.** Low.
- **Impact.** High.
- **Description.** P7 KB persona views could be interpreted as a KB rewrite. If the agent treats persona views as a replacement for the existing KB structure, downstream consumers (Cursor sessions, hlk-erp routes, agent reads via `hlk_mcp_server.py`) break.
- **Mitigation.**
  - P7 charter explicitly states persona views are **additive overlays** on existing KB, not replacement. Charter prose carries the additive-only rule as a load-bearing invariant.
  - 4 hlk-erp panel filter routes are **filter views** over existing KB rows, not new KB structures.
  - Integration verification at P10 checks that existing KB consumers (Cursor sessions, MCP servers, agent reads) still function post-P7.
- **Owner.** PMO (Strand G owner) + System Owner (sibling-repo hlk-erp routes).
- **Close-out.** P10 integration verification PASS for existing KB consumers.

## R-IH-73-5 — Historical case-law leaks counterparty PII for Bâtard / RCD Legal / IAG-IBERIA / L'Oréal

- **Likelihood.** Med.
- **Impact.** High.
- **Description.** P4 `HISTORICAL_ENGAGEMENT_CASE_LAW.md` cites operator's history including real employers ([`FOUNDER_TRAJECTORY_INTERNAL.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/FOUNDER_TRAJECTORY_INTERNAL.md) §2 names Multiassistance, IBM, BICG, Econocom, Volvo, GMA Corporate, Europ Assistance/Generali, RCD Legal — and the current L'Oréal arrangement). Counterparty PII for Bâtard 2020 + RCD Legal + L'Oréal Europe Data Quality Manager arrangement could leak to external surfaces if frontmatter is wrong.
- **Mitigation.**
  - `access_level: 5 register: internal` frontmatter mandatory on `HISTORICAL_ENGAGEMENT_CASE_LAW.md` (matches FOUNDER_TRAJECTORY_INTERNAL precedent).
  - Anonymize counterparty names unless operator confirms explicit consent at C-73-8 inline-ratify gate. Preserve case codenames (Bâtard 2020 / Mark-II / Alias V / RCD Legal / L'Oréal arrangement) for cross-canon link only.
  - `validate_brand_baseline_reality_drift.py` PASS gate at P4 commit: no employer names leaked to external-register surfaces.
  - `akos-brand-baseline-reality.mdc` §"Forbidden contexts" explicitly forbids external decks / dossiers / public prose from quoting employer names; per-engagement counterparty briefs and operator-private SOPs are allowed.
- **Owner.** People Operations Manager (Strand F author) + Brand & Narrative Manager (drift-gate review).
- **Close-out.** P4 commit + validator PASS.

## R-IH-73-6 — Outsourced helper class SOC failure (low-trust collaborator gets cleared-collaborator KB access by mistake)

- **Likelihood.** Med.
- **Impact.** High.
- **Description.** D-IH-73-E `outsourced_helper` carries `default_access_level = 1` or `2` and `soc_posture = scoped-redacted`. If P7 KB-view low-trust route mis-implements the filter (e.g., access-level filter is or'd instead of and'd; engagement_model_id filter is dropped), a Fiverr/Cameroon helper gets cleared-collaborator KB access.
- **Mitigation.**
  - D-IH-73-E mandates separate engagement class (not a sub-class) so SOC posture is queryable from the registry.
  - P7 KB-view low-trust route enforces SOC posture at the route level: `WHERE access_level <= helper.access_level AND engagement_model_id = 'outsourced_helper'`. Both predicates required.
  - Integration test at P10 simulates an outsourced_helper session and asserts the KB view returns only `access_level <= 2` rows.
  - SOC review at P7 inline-ratify gate explicitly checks the route SQL/TypeScript.
- **Owner.** System Owner (sibling-repo hlk-erp route author) + People Operations Manager (engagement-class SOC owner).
- **Close-out.** P10 integration verification + P11 closure UAT.

## R-IH-73-7 — Engagement-lifecycle SOPs duplicate FINOPS counterparty register

- **Likelihood.** Low.
- **Impact.** Med.
- **Description.** P3 `SOP-ENGAGEMENT_PAYROLL_OPS_001.md` could accidentally duplicate [`FINOPS_COUNTERPARTY_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/FINOPS_COUNTERPARTY_REGISTER.csv) by minting a parallel counterparty list within the SOP.
- **Mitigation.**
  - P3 payroll SOP cross-links `FINOPS_COUNTERPARTY_REGISTER` per [`akos-holistika-operations.mdc`](../../../../.cursor/rules/akos-holistika-operations.mdc) §"Schema responsibilities" no-duplication rule.
  - Per-engagement counterparty rows live in `FINOPS_COUNTERPARTY_REGISTER`; `ENGAGEMENT_REGISTRY.csv` carries `counterparty_org_id` cross-link (no FK).
  - Pre-P3 self-checkpoint reviews SOP outline against FINOPS register schema.
- **Owner.** People Operations Manager (P3 author) + Business Controller (FINOPS owner).
- **Close-out.** P3 commit + validator PASS.

## R-IH-73-8 — Per-pillar Learning curriculum stalls awaiting I75 (Research area governance) pillar definitions

- **Likelihood.** Med.
- **Impact.** Low.
- **Description.** P2 `HOLISTIK_RESEARCHER_ONBOARDING_CURRICULUM.md` references methodology pillars. I75 (Research area governance) is the SSOT for the pillar list, but I75 is still a candidate (per [`docs/wip/planning/_candidates/i75-research-area-governance.md`](../_candidates/i75-research-area-governance.md)) — pillar definitions don't exist yet.
- **Mitigation.**
  - Stub curriculum with placeholder pillars at P2; revise after I75 P2 ships pillar definitions.
  - Bidirectional loose-coupling per dep map §3.5: I73 P1 + I75 P2 co-evolve; neither blocks the other.
  - Curriculum frontmatter cites `methodology_version_at_authoring` so I71 P4 review-stamp dimension flags drift when pillars land.
- **Owner.** Learning Curator (P2 author).
- **Close-out.** P11 closure UAT. Stub curriculum stays operational; I75 P2 triggers a curriculum revision in a future commit (outside I73 scope).

## R-IH-73-9 — Madeira AI O5-1 framing creates AIC SOP-consumption ambiguity per I72 D-IH-72-S

- **Likelihood.** Low.
- **Impact.** Med.
- **Description.** Madeira is the AI O5-1 permanent core per the operator brief. I72 D-IH-72-S ratified the binary AC axis (humans + AIC are SOP-readers on AC-HUMAN; unattended runbook firing is AC-AUTOMATION). If I73 frames Madeira as a separate engagement class, it collides with D-IH-72-S.
- **Mitigation.**
  - Madeira = `operator_self` extension (permanent core; not a separate engagement class). Reaffirmed at P1 in case-law section.
  - P1 ENGAGEMENT_MODEL_REGISTRY rows do NOT include a "madeira" or "AIC" class; the 7 classes are humans + operator-self.
  - I76 (MADEIRA elevation; candidate) is the future home for AIC role_owner architecture; I73 does not pre-empt it.
- **Owner.** PMO + System Owner.
- **Close-out.** P1 commit + I76 cross-link in `master-roadmap.md` forward-charters.

## R-IH-73-10 — P11 closure UAT slips because P9 first-engagement onboard depends on operator action outside agent control

- **Likelihood.** Med.
- **Impact.** Low.
- **Description.** P9 UAT requires a first engagement to be onboarded under the new model. If operator can't / doesn't onboard within the I73 execution window, P11 closure slips.
- **Mitigation.**
  - P9 explicitly operator-driven; agent does not block on it.
  - Option (a) operator-self ratification is lowest-friction path: operator runs `SOP-ENGAGEMENT_ONBOARDING_001` against own engagement-folder shape with `engagement_model_id = operator_self`. No external counterparty needed.
  - Option (b) first apprentice cohort onboarding is higher-friction but available; operator picks at P9 inline-ratify gate.
- **Owner.** Founder + People Operations Manager.
- **Close-out.** P9 UAT row PASS (either option).

## Cross-references

- Cursor plan (preview table): [`~/.cursor/plans/i73-people-ops-engagement-models-methodology-ip-c9d4e7f3.plan.md`](file:///~/.cursor/plans/i73-people-ops-engagement-models-methodology-ip-c9d4e7f3.plan.md) §"Risk-register preview (R-IH-73-1..10)".
- Decision log: [`decision-log.md`](decision-log.md).
- Master roadmap: [`master-roadmap.md`](master-roadmap.md).
- P0 charter report: [`reports/p0-charter-report.md`](reports/p0-charter-report.md).
- Risk-mitigation cursor rules: [`akos-agent-checkpoint-discipline.mdc`](../../../../.cursor/rules/akos-agent-checkpoint-discipline.mdc) §"What pause-point fatigue looks like"; [`akos-inline-ratification.mdc`](../../../../.cursor/rules/akos-inline-ratification.mdc) §6.2 STOP-AND-CLARIFY posture; [`akos-brand-baseline-reality.mdc`](../../../../.cursor/rules/akos-brand-baseline-reality.mdc) §"Forbidden contexts".
