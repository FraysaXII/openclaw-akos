---
language: en
status: active
canonical: true
role_owner: Account Management Manager
classification: way_of_working
intellectual_kind: charter
ssot: true
authored: 2026-05-14
last_review: 2026-05-14
last_review_at: 2026-05-14
last_review_by: CMO
last_review_decision_id: D-IH-72-A
methodology_version_at_review: v3.0
companion_to:
  - ../../canonicals/RESONANCE_AREA_CHARTER.md
  - ../../../canonicals/MARKETING_AREA_M3_REDESIGN.md
---

# ACCOUNT_MANAGEMENT_CHARTER — Marketing/Resonance/Account Management sub-discipline

> Authored I72 P1 per `D-IH-72-A` (P0 charter) + `D-IH-70-R` (Account Management surfaced as first-class role from SUEZ engagement diagnostic). Account Management owns the **1:1 counterparty relationship lifecycle** post-engagement-handoff: kickoff, mid-engagement health, expansion proposals, renewal cycles, and structured close. Per `D-IH-72-AN` (regression-amend 2026-05-15): the legacy Community Manager role row was deleted; the Community-Management discipline (peer-cohort + many-to-one community relationships) is now held by Resonance Manager directly as a discipline of that generalist role.

## 1. Mission

Account Management exists to **own the relationship health of every active counterparty engagement** — measured in 5 dimensions per `BRAND_BASELINE_REALITY_MATRIX.md` external register:

1. **Counterparty understanding**: Are we tracking the right counterparty signals (decision-maker stability, executive sponsor health, renewal-window calendar)?
2. **Engagement-on-track**: Is delivery against the engagement's stated outcomes proceeding to plan?
3. **Expansion-readiness**: Are there discoverable expansion paths (adjacent scope, sister-counterparty referrals, multi-year extension)?
4. **Risk surface**: Are there early signals of churn, dissatisfaction, sponsor departure, or budget compression?
5. **Renewal-readiness**: With X days to renewal-window-open, what is the recommended renewal posture?

## 2. Sub-discipline scope

Account Management is a **sub-discipline within Resonance**, not a parallel sub-area. The boundary:

- **Account Management owns 1:1 counterparty health** (single-account focus).
- **Resonance Manager (Community-Management discipline per D-IH-72-AN) owns 1:many cohort moments** (peer-cohort programs, customer-advisory boards, community channels).
- Both report to **Resonance Manager** (sub-area lead).

Account Management is the **primary contract-side counterpart** for the operator + the named delivery team during an active engagement. CRM-of-record interactions, Calendly scheduling for QBRs, expansion-proposal authoring all flow through Account Management.

## 3. Operating posture

Per `D-IH-70-R` codification + this charter:

- **Per-engagement P0 deliverable**: Account Management mints a per-account playbook at engagement P0 (named DM, sponsor, blockers, expansion hypotheses, renewal-window calendar).
- **Per-engagement steady-state**: monthly relationship-health pulse; quarterly QBR (with case-study deck deployed by Account Management; case study authored by Storytelling).
- **Per-engagement renewal-window**: T-90 renewal-readiness scoring; T-60 renewal-proposal authoring; T-30 negotiation; T-0 contracted close or graceful sunset.
- **Per-engagement close**: post-engagement debrief; case-study request to Storytelling (consent-permitting); referral hypothesis surfacing.

## 4. Cross-area integrations (DAMA-DMBOK)

| Cross-area | Integration | Reference |
|:---|:---|:---|
| **Operations/RevOps** | Renewal + expansion proposals route through `ENGAGEMENT_TEMPLATE_REGISTRY.csv` (P2) for repeatable contract patterns. Per-account `engagement_id` + `account_id` FK columns wired at P7 RevOps Spine. | `D-IH-72-F` (template registry as sibling), `D-IH-72-M` (RevOps spine). |
| **Storytelling** | Account Management briefs Storytelling on case-study opportunities (consent + materiality permitting). Storytelling authors; Account Management deploys in QBRs. | `STORYTELLING_AREA_CHARTER.md` §3. |
| **Reach** | Account Management hands off referral hypotheses (sister-counterparty, adjacent-scope) to Reach for top-of-funnel motion. | `REACH_AREA_CHARTER.md` §3. |
| **Research/Intelligence** | Per-account intelligence updates (counterparty-org changes, sponsor moves, regulatory shifts) flow from `INTELLIGENCEOPS_REGISTER.csv` (P6) to per-account playbook. | `D-IH-72-H` (IntelligenceOps register sibling). |
| **People/Compliance** | DPA + sub-processor disclosure cycles tracked per-account; renewal triggers re-confirmation per `BRAND_COUNTERPARTY_README_CONTRACT.md`. | `Marketing/Brand/canonicals/BRAND_COUNTERPARTY_README_CONTRACT.md`. |

## 5. Process catalog (initial; expanded at P8)

| Process | `item_id` | Cadence | Status | SOP (P8 deliverable) |
|:---|:---|:---|:---|:---|
| Per-account playbook authoring at engagement P0 | `mar_account_dtp_playbook_001` | event_triggered (engagement P0) | planned (P8) | `SOP-ACCOUNT_PLAYBOOK_001.md` |
| Monthly relationship-health pulse | `mar_account_dtp_pulse_001` | scheduled (monthly per active engagement) | planned (P8) | `SOP-ACCOUNT_PULSE_001.md` |
| Quarterly QBR cadence | `mar_account_dtp_qbr_001` | scheduled (quarterly per active engagement) | planned (P8) | `SOP-ACCOUNT_QBR_001.md` (paired with `SOP-REVOPS_QBR_001.md` at P4 for revenue-impact mapping) |
| Renewal-readiness scoring (T-90) | `mar_account_dtp_renewal_score_001` | scheduled (T-90 from renewal-window) | planned (P8) | `SOP-ACCOUNT_RENEWAL_SCORE_001.md` |
| Renewal proposal authoring (T-60) | `mar_account_dtp_renewal_propose_001` | event_triggered (T-60 from renewal-window) | planned (P8) | `SOP-ACCOUNT_RENEWAL_PROPOSAL_001.md` |
| Post-engagement debrief + case-study request | `mar_account_dtp_close_001` | event_triggered (engagement close) | planned (P8) | `SOP-ACCOUNT_CLOSE_001.md` |

## 6. Activation cadence + lifecycle

- **Activation cadence**: continuous (always-on per active engagement). Per-account intensity scales with engagement value + relationship-risk score.
- **Lifecycle status**: `active` (Account Management Manager active in baseline_organisation.csv; charter formalises operating contract).
- **Sub-discipline maturity**: P1 (this charter) → P8 SOPs minted → P10 closing UAT validates per-account playbook coverage.

## 7. Cross-references

- Parent: [`RESONANCE_AREA_CHARTER.md`](../../canonicals/RESONANCE_AREA_CHARTER.md) §2.
- Grandparent: [`MARKETING_AREA_M3_REDESIGN.md`](../../../canonicals/MARKETING_AREA_M3_REDESIGN.md) §2 (Resonance sub-area).
- Sibling: Community-Management discipline now held by Resonance Manager directly (legacy Community Manager role row deleted at I72 R-D per D-IH-72-AN).
- Cross-area: `Operations/RevOps/canonicals/REVOPS_AREA_CHARTER.md` (revenue-impact mapping); `Operations/RevOps/canonicals/dimensions/ENGAGEMENT_TEMPLATE_REGISTRY.csv` (P2; renewal patterns); `Operations/RevOps/canonicals/SOP-REVOPS_QBR_001.md` (P4; paired with account QBR).
- Brand: `Marketing/Brand/canonicals/BRAND_COUNTERPARTY_README_CONTRACT.md` (DPA + sub-processor disclosure); `Marketing/Brand/canonicals/BRAND_BASELINE_REALITY_MATRIX.md` (counterparty external register).
- Decisions: `D-IH-72-A` (P0 charter), `D-IH-70-R` (Account Management first-class role), `D-IH-72-AB` (3-function umbrella).
