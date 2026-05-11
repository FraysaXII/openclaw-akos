---
sop_id: SOP-ENG_ESTIMATION_DISCIPLINE_001
title: Engagement Estimation Discipline
version: 1.0
status: active
classification: canonical
access_level: 4
language: en
register: external
process_id: hol_eng_prc_estimation_001
role_owner: Project Manager
role_parent_1: PMO
area: Operations
entity: Holistika
governance:
  - SOP-ENG_PROPOSAL_001 (consumer)
  - SOP-ENG_DISCOVERY_QUESTIONNAIRE_001 (sister)
  - SOP-ENG_ENGAGEMENT_DESIGN_001 (sister)
linked_initiative: customer-engagements-2026 (candidate)
created: 2026-05-10
last_review: 2026-05-10
sister_sops:
  - SOP-ENG_PROPOSAL_001
  - SOP-ENG_DISCOVERY_QUESTIONNAIRE_001
  - SOP-ENG_ENGAGEMENT_DESIGN_001
---

# SOP-ENG_ESTIMATION_DISCIPLINE_001 — Engagement Estimation Discipline

> Project-Manager-owned **per-engagement process** that produces an effort × cost × duration triangle (min / par / max) for any Holistika engagement. The discipline is reusable across customer / partner / advisor scopes; it is the **shared math** behind the proposal's commercial schedule, the deck's pricing slide, and the internal go / no-go review.

## 1. Purpose and scope

* **Purpose** — give every Holistika proposal a defensible price, a calibrated effort budget, and a country-aware schedule, anchored on three governed CSVs (no spreadsheet sprawl).
* **In scope** — customer engagements, partner co-delivery scopes, ad-hoc advisor missions, ongoing-support tiers.
* **Out of scope** — internal Holistika programmes (no monetary side), pure-research programs without a counterparty, brand-only surface deliverables (handled by `SOP-ENG_PROPOSAL_001` directly without an estimation pass).

## 2. Inputs

| Input | Path | Owner | What it provides |
|:---|:---|:---|:---|
| Role × hourly-rate matrix | `docs/references/hlk/compliance/baseline_organisation.csv` | CPO + Business Controller | Per-role triangle (`role_hourly_min_eur` / `_par_` / `_max_`) — Madrid SME consulting baseline. |
| Process × effort hours | `docs/references/hlk/compliance/process_list.csv` | PMO | Per-process triangle (`time_hours_min` / `_par` / `_max`) for engagement-execution items. |
| Country work calendar | `docs/references/hlk/compliance/dimensions/COUNTRY_WORK_CALENDAR.csv` | Business Controller | Per-country `legal_hours_per_day`, `public_holidays_per_year_avg`, `locale_uplift_pct`. |
| Engagement scope | `docs/wip/intelligence/<slug>/scope.yaml` | Project Manager | Per-package method × role-mix × multipliers. |

## 3. Method library (~12 methods)

The reusable method shapes; effort hours are **calibrated** to the Madrid SME consulting baseline and **validated** against off-repo competitive distillations (a 1,500-person 15-year cabinet serving IBEX35-class clients in Spain). Any change to these constants must land here **and** in `akos/engagement_estimation.py`'s `METHODS` registry simultaneously; drift is detected by `tests/test_estimation_constants_match_sop.py`.

| Method id | Label | Effort h (min/par/max) | Default role mix |
|:---|:---|:---|:---|
| `discovery_kickoff` | Discovery — kickoff workshop and framing | 8 / 12 / 18 | Project Manager 0.5, Holistik Researcher 0.5 |
| `discovery_interviews` | Discovery — stakeholder interviews + synthesis grid | 12 / 20 / 32 | Holistik Researcher 0.7, Project Manager 0.3 |
| `discovery_synthesis` | Discovery — baseline assessment write-up | 8 / 14 / 24 | Holistik Researcher 0.6, Project Manager 0.4 |
| `design_workshop` | Design — joint design workshop (counterparty-side) | 10 / 16 / 28 | Project Manager 0.4, Tech Lead 0.3, O5-1 0.3 |
| `design_specification` | Design — functional + technical specification | 24 / 40 / 72 | Tech Lead 0.5, Project Manager 0.3, UX Designer 0.2 |
| `build_prototype_excel` | Build — Phase 1 Excel/Power Query prototype | 40 / 80 / 140 | Back-End Developer 0.5, Tech Lead 0.3, Project Manager 0.2 |
| `build_webapp` | Build — Phase 2 lightweight web application | 140 / 240 / 400 | Back-End Developer 0.35, Front-End Developer 0.25, Tech Lead 0.2, Project Manager 0.1, UX Designer 0.1 |
| `build_integration_study` | Build — Phase 3 integration feasibility study | 40 / 80 / 140 | Tech Lead 0.5, AI Engineer 0.2, Project Manager 0.3 |
| `transfer_training` | Transfer — operator training | 12 / 20 / 32 | Project Manager 0.6, Tech Lead 0.4 |
| `transfer_documentation` | Transfer — SOP + runbook + handover pack | 12 / 20 / 32 | Project Manager 0.5, Tech Lead 0.3, Holistik Researcher 0.2 |
| `close_review` | Close — engagement review + lessons-learned | 4 / 8 / 14 | Project Manager 0.5, O5-1 0.5 |
| `ongoing_support_month` | Ongoing support — per month | 8 / 16 / 32 | Back-End Developer 0.5, Project Manager 0.5 |

## 4. Role × hourly rate matrix (6-tier mapping)

Hourly rates (€/h) are anchored on the Madrid SME consulting market. Daily rates are derived from country calendars (e.g. ES 8 h × par-rate; FR 7 h × par-rate × FR locale uplift). The 6 tiers below are how `baseline_organisation.csv` is populated; AI personas (Susana Madeira, AIC) carry NULL rates and are non-billable.

| Tier | Roles in scope (examples) | min €/h | par €/h | max €/h |
|:---|:---|---:|---:|---:|
| Founder / Admin | Admin, O5-1 | 100 | 130 | 165 |
| Strategic-C | CPO, COO, CFO, CMO, CDO, CTO | 80 | 110 | 145 |
| Senior Operational | Holistik Researcher, Lead Researcher, Compliance, Organisation, PMO, SMO, Business Controller, Financial Controller, Brand Manager, Social Media Manager, Growth Manager, Data Architect, Lead Data Scientist, Data Governance Lead, Legal Counsel | 60 | 80 | 100 |
| Tech Lab Engineering | Tech Lead, AI Engineer, DevOPS, System Owner | 70 | 90 | 115 |
| Operations / PM | Project Manager, Product Owner, Service Delivery Manager, Account Manager, Asset Manager, Pricing, Taxes, Front Office, O2C, PTP, Senior Researcher, Intelligence Analyst, OSINT Analyst, HUMINT Specialist, Ethics & Learning, Corporate Marketing, Talent, AV, Copywriter, Design, UX Designer, Community Manager, Paid Media Manager, Business Analyst, Data Engineer, Front-End Developer, Back-End Developer, Domain Specialist, Data Steward, Database Owner, Legal Consumer Specialist, Legal Collaborator Specialist | 45 | 60 | 75 |
| Junior / Support | Private Researcher, Public, D-Class | 30 | 40 | 55 |
| Non-billable | Susana Madeira, AIC | — | — | — |

## 5. Multipliers

Multipliers compound onto the **price**, not the effort. They are listed in `akos/engagement_estimation.py`'s `MULTIPLIERS` registry and in this SOP §5; both must agree.

| Multiplier id | Label | Factor | When applied |
|:---|:---|:---|:---|
| `enterprise_premium` | Enterprise premium | 1.20 | Counterparty is an enterprise (≥ 250 employees) with a formal procurement / DSI / legal-counsel chain. |
| `bridge_entity` | Bridge-entity coordination | 1.10 | Holistika reaches the counterparty through a partner bridge (extra alignment overhead). |
| `locale_uplift_fr` | French locale uplift | 1.20 | Engagement priced for a French-market counterparty (vs Madrid SME baseline). |
| `first_of_kind` | First-of-kind novelty | 1.15 | Engagement archetype is new to Holistika; learning-curve allowance. |
| `repeat_counterparty` | Repeat-counterparty discount | 0.90 | Counterparty has previously delivered with Holistika; relationship discount. |

## 6. Country calendar

Country-specific working-hour and public-holiday parameters live in `docs/references/hlk/compliance/dimensions/COUNTRY_WORK_CALENDAR.csv`.

| Country | legal_hours_per_day | public_holidays_per_year_avg | locale_uplift_pct |
|:---|:---|:---|:---|
| ES (baseline) | 8.0 | 14 | 0 |
| FR | 7.0 | 11 | 20 |

Adding a country = appending one row + (optionally) a multiplier. No code change required.

## 7. Math

* **PERT expected value** — per triangle (effort, cost, duration): `E = (min + 4·par + max) / 6`.
* **Blended rate** — share-weighted average of role hourly rates over the role mix; preserves the min/par/max triangle.
* **Cost (pre-multiplier)** — `effort_hours × blended_rate` per triangle level (min × min, par × par, max × max).
* **Cost (final)** — `cost_pre × Π(multiplier_factor)`.
* **Duration in working days** — `effort_hours / legal_hours_per_day` per triangle level.
* **End-date math** — sequential placement starting from `scope.start_date`, skipping Saturdays + Sundays, with a public-holiday bump computed from `public_holidays_per_year_avg × span_days / 365`.

## 8. Operator workflow (per engagement)

1. Author `docs/wip/intelligence/<slug>/scope.yaml` from `docs/references/hlk/v3.0/_assets/operations/shared/engagement/estimation/estimation-template.md`.
2. Run `py scripts/estimate_engagement.py --scope <scope.yaml> --out <commercial-schedule.md>`.
3. Review the rendered `commercial-schedule.md` (per-package math table + totals + Mermaid Gantt). Adjust multipliers or role-mix overrides if the par-cost or par-duration is implausible.
4. Paste the totals into the proposal's §4 Timeline + §5 Commercial Posture.
5. After engagement closure, append the realised effort + cost + duration to `docs/wip/intelligence/<slug>/realised-vs-estimated.csv` (created on first close); a calibration cycle is run twice a year to update the constants in §3.

## 9. Calibration discipline

* **Half-yearly review** — Project Manager + Business Controller compare realised vs estimated for closed engagements; update `METHODS` constants and the role-tier table; bump SOP version.
* **Drift safeguard** — `tests/test_estimation_constants_match_sop.py` enforces parity between the SOP body §3 and the `METHODS` registry. CI fails on drift.
* **Per-engagement note** — at proposal time, the `commercial-schedule.md` shows par-expected and PERT-expected; the gap is the operator's risk-cone (a large gap → flag in the proposal cover note).

## 10. Cross-references

* `akos/engagement_estimation.py` — Pydantic models + math + Mermaid Gantt.
* `scripts/estimate_engagement.py` — CLI.
* `docs/references/hlk/v3.0/_assets/operations/shared/engagement/estimation/estimation-template.md` — operator worksheet template.
* `tests/test_engagement_estimation.py` + `tests/test_estimation_constants_match_sop.py` — gates.
* Sister SOPs — `SOP-ENG_PROPOSAL_001`, `SOP-ENG_DISCOVERY_QUESTIONNAIRE_001`, `SOP-ENG_ENGAGEMENT_DESIGN_001`.
