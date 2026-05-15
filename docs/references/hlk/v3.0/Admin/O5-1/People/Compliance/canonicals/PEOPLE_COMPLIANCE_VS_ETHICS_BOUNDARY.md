---
language: en
status: active
canonical: true
role_owner: CPO
intellectual_kind: governance_boundary
authored: 2026-05-15
last_review: 2026-05-15
---

# People Compliance vs Ethics boundary

Defines **ownership splits** between the People **Compliance**, **Ethics**, and **Learning** sub-roles introduced per [`PEOPLE_AREA_RESTRUCTURE.md`](../../canonicals/PEOPLE_AREA_RESTRUCTURE.md). Aligns with the inseparable Ethics + Learning thesis in §3 of that canonical and with posture doctrine in [`ETHICAL_AUTOMATION_POSTURE.md`](../../Ethics/canonicals/ETHICAL_AUTOMATION_POSTURE.md).

Edge-case adjudication defaults (**C-73-5**, inline-ratify during I73 P6 — rationale captured in initiative decision log `INIT-OPENCLAW_AKOS-73`):

| Edge-case axis | Default primary owner |
|:---------------|:----------------------|
| GDPR / personal-data handling / retention / DPIA-style regulatory posture | **Compliance** |
| AI-overreach / second-order automation accountability / CSOLT-style escalation posture | **Ethics** |
| AI-assisted customer disclosure (human vs blended messaging on outward-facing artefacts) | **Joint — Compliance + Ethics** |

---

## Process-class routing table

**Primary owner** is the sub-role accountable for **process-list stewardship** and **SOP/runbook pairing** for new rows in that class (see [`process_list.csv`](process_list.csv) `role_owner`). **Joint** rows require explicit RACI in instructions or addendum (Ethics + Compliance co-review on material changes).

| Process class / theme | Primary People sub-role | Joint / notes |
|:----------------------|:------------------------|:--------------|
| Regulatory compliance packs; startup certification evidence (e.g. ENISA pathway); policy-framework methodology under Compliance Methodology workstream | **Compliance** | Coordinate Legal Counsel where instruments are filed |
| Identity / access-level taxonomy; confidence/source taxonomies as organizational controls | **Compliance** | Cross-read Ethics when automation applies classification |
| GDPR / data-protection operations and evidence control | **Compliance** | Ethics consulted when AI touches personal data flows |
| Doctrine about ethics, moral frameworks, “allies/neutrals/enemies” style posture codification | **Ethics** | Compliance retains adjacent methodology-tree placement until optional tree refactor |
| Automation posture; quarterly Ethics + Learning co-review cadence | **Ethics** | Learning Curator mandatory co-reviewer per ETHICAL_AUTOMATION_POSTURE §5 |
| Curriculum design; training frameworks; capability-building workstreams | **Learning** | Ethics pairing per PEOPLE_AREA_RESTRUCTURE §3 |
| Hiring; payroll; engagement lifecycle; recruiter/recruitment onboarding execution | **People Operations** | Ethics / Compliance consulted per engagement model SOC |

---

## Access-level alignment

[`access_levels.md`](access_levels.md) remains **Compliance-owned taxonomy**. Ethics and Learning processes **consume** access levels when defining posture (e.g. outsourced-helper SOC); they do not redefine numeric levels without Compliance charter amendment.

---

## Cross-references

- [`ETHICAL_AUTOMATION_POSTURE.md`](../../Ethics/canonicals/ETHICAL_AUTOMATION_POSTURE.md) — automation + customer-engagement posture SSOT
- [`PEOPLE_AREA_RESTRUCTURE.md`](../../canonicals/PEOPLE_AREA_RESTRUCTURE.md) — 4 sub-role split + deferred CSV migration notes (§5)
- [`access_levels.md`](access_levels.md) — confidentiality ladder
