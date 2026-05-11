---
status: complete
classification: working
access_level: 5
language: en
register: internal
phase: P3b
phase_name: Canonical CSV extensions (baseline_organisation rates + process_list min/max + COUNTRY_WORK_CALENDAR)
recorded_at: 2026-05-10
---

# P3b — Canonical CSV extensions self-checkpoint

## Files modified

| File | Change | Rows touched |
|:---|:---|---:|
| `docs/references/hlk/compliance/baseline_organisation.csv` | +3 columns: `role_hourly_min_eur`, `role_hourly_par_eur`, `role_hourly_max_eur`. Populated for all 65 rows via 6-tier mapping. | 65 |
| `docs/references/hlk/compliance/process_list.csv` | +2 columns: `time_hours_min`, `time_hours_max`. Populated for engagement-execution `item_id`s. New row minted for the estimation discipline itself. | 4 populated, 1 net-new |
| `docs/references/hlk/compliance/dimensions/COUNTRY_WORK_CALENDAR.csv` | NEW canonical dimension CSV. Seed rows ES + FR. | 2 |
| `akos/hlk_process_csv.py` | `PROCESS_LIST_FIELDNAMES` extended with `time_hours_min` and `time_hours_max` after `time_hours_par`. | n/a |

## 6-tier baseline-organisation rate mapping

Per SOP-ENG_ESTIMATION_DISCIPLINE_001 §4 and operator instruction "Update the rates of all our baseline org if it wasn't there already":

| Tier | Rate (EUR/h) min/par/max | Roles assigned |
|:---|:---|:---|
| T1 Founder Time | 100 / 130 / 165 | Admin, O5, O5-1 |
| T2 Strategic-C | 80 / 110 / 145 | CTO, CFO, CMO, COO, CPO, CDO |
| T3 Senior Operational | 60 / 80 / 100 | Holistik Researcher, Lead Researcher, Brand Manager, Compliance, Organisation, Talent, PMO, SMO, Business Controller, Financial Controller, Social Media Manager, Growth Manager, Data Architect, Lead Data Scientist, Data Governance Lead, Legal Counsel |
| T4 Tech Lab Engineering | 70 / 90 / 115 | Tech Lead, AI Engineer, DevOPS, System Owner |
| T5 Operations / PM | 45 / 60 / 75 | Project Manager, Product Owner, Service Delivery Manager, Account Manager, Asset Manager, Pricing, Taxes, Front Office, O2C, PTP, Senior Researcher, Intelligence Analyst, OSINT Analyst, HUMINT Specialist, Ethics & Learning, Corporate Marketing, AV, Copywriter, Design, UX Designer, Community Manager, Paid Media Manager, Business Analyst, Data Engineer, Front-End Developer, Back-End Developer, Domain Specialist, Data Steward, Database Owner, Legal Consumer Specialist, Legal Collaborator Specialist |
| T6 Junior / Support | 30 / 40 / 55 | Private Researcher, Public, D-Class |
| AI / non-billable | NULL | Susana Madeira, AIC |

Validated: 65 rows mapped, 0 missing, RoleRate Pydantic constraints (all-or-none, monotone min/par/max) hold.

## Process-list min/par/max effort population

Engagement-execution rows populated:

| item_id | min | par | max |
|:---|---:|---:|---:|
| `hol_eng_prc_discovery_questionnaire_001` | 8 | 12 | 20 |
| `hol_eng_prc_proposal_001` | 12 | 18 | 28 |
| `hol_eng_prc_engagement_design_001` | 16 | 24 | 40 |
| `hol_eng_prc_estimation_001` (NEW) | 4 | 6 | 10 |

The new `hol_eng_prc_estimation_001` row codifies the estimation discipline itself as a process step that runs per engagement.

## COUNTRY_WORK_CALENDAR seed rows

| country_code | legal_h/day | holidays/yr | uplift min/par/max | notes |
|:---|---:|---:|:---|:---|
| ES | 8.0 | 14 | 0/0/0 | Madrid base; baseline market |
| FR | 7.0 | 11 | 15/20/25 | Practical 8h/legal 7h-35h-week; tactical uplift per operator direction |

## Verification

```
py -m pytest tests/test_engagement_estimation.py -v
==> 34 passed, 1 skipped (SUEZ scope.yaml smoke; will pass after P3c)

py scripts/validate_hlk.py
==> All organisation/process integrity checks PASS
==> All dimension validators PASS
==> One pre-existing INITIATIVE_REGISTRY FAIL (INIT-68 → D-IH-66-AC missing) — not introduced by P3b; tracked separately.
```

## Bug fix recorded

The first run of `scripts/_extend_baseline_org_with_rates.py` produced a misalignment on rows that ended with stray trailing commas in the source CSV (e.g. `AI Engineer`), surfacing as `(None, par, max)` on the `RoleRate` validator. Root cause: `csv.reader` returned 13 cells for those rows where the schema only declares 12 — so the `extend([min, par, max])` step landed at indices 13/14/15 instead of 12/13/14. Fixed by adding a "trim phantom trailing empty cells" pass in the helper before the rate columns are appended. Test `test_load_role_rates_from_canonical_csv_is_well_formed` now passes.

## Next

P3c — SUEZ application. Author `scope.yaml` for the SUEZ engagement (FR, kickoff 2026-05-19, three variants a/b/c), run `scripts/estimate_engagement.py` to render `commercial-schedule.md` with the bottom-up math + Mermaid Gantt block per variant, unskip the SUEZ smoke test.
