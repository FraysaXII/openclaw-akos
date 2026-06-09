---
report_type: hygiene-settlement
parent_initiative: INIT-OPENCLAW_AKOS-95
phase: P95-Hygiene-C
authored: 2026-06-09
authored_by: Execution seat (Composer)
ratifying_decisions:
  - D-IH-95-K
  - D-IH-95-J
verdict: PASS
---

# I95 Hygiene C — Collaborator-share settlement tranche (2026-06-09)

**Operator ratification:** AskQuestion #2 scope **C** — full settlement tranche refreshing all 5 collaborator-share registers to match live engagement reality (`i95-round2-askquestion2-ratification-2026-06-09.md`).

**Hygiene B (same commit):** Charter vault CSV count **74 → 73** + GOV-1 inventory footnote in `universal-canonical-governance-charter-2026-06-09.md`.

---

## Engagement coverage map (before → after)

| Engagement | Before | After |
|:---|:---|:---|
| `ENG-SUEZ-WEBUY-2026` | 2 SHARE rows + 10 vendor rows | unchanged (consulting_direct + bd_commission_overlay) |
| `ENG-SUEZ-WEBUY-2026-AISHA-CONT` | 1 SHARE row, **0 vendor rows** | 1 SHARE row + **10 vendor rows** |
| `ENG-WEBSITZ-SHOPIFY-2026` | **missing** | 1 SHARE row + **10 vendor rows** |

---

## Row change log (canonical CSV gate)

### `COLLABORATOR_SHARE_REGISTRY.csv` — 2 rows touched

| Row ID | Change | Rationale |
|:---|:---|:---|
| `SHARE-SUEZ-AISHA-CONTINUITY-2026` | **Modified** — `share_override_decision_id` blank → `D-IH-86-EF`; notes + `last_review_at` | CS-04: `methodology_in_progress` on `deep_partner_65_35` requires ratifying decision FK; D-IH-86-EF is the existing engagement-class ratification for this slice |
| `SHARE-WEBSITZ-SHOPIFY-2026-DEEP-PARTNER` | **Appended** — `deep_partner_65_35` 65/35; `GOI-PRT-WEBSITZ-2026`; `methodology_trained`; rate 100 EUR/hr | Live engagement in `ENGAGEMENT_REGISTRY` + `POC-WEBSITZ-SHOPIFY-2026`; PRICING_MODEL §1.3 sub-contracted band; closes IT-3 commercial-accuracy gap (Websitz precedent cited in doctrine §3.1 but absent from registers) |

### `HOLISTIKA_VENDOR_SERVICES_BILLED.csv` — 20 rows appended

| Engagement | Rows | Rationale |
|:---|---:|:---|
| `ENG-SUEZ-WEBUY-2026-AISHA-CONT` | 10 | Mandatory 10-class roster per collaborator-share discipline; `research_head_discipline` links `clause_mentoring_methodology_in_progress` |
| `ENG-WEBSITZ-SHOPIFY-2026` | 10 | Same roster bar; `mktops_marketing` links `clause_partner_marketing_agency_overlap`; `front_end_engineering` billed for Shopify delivery |

### `COLLABORATOR_MARKET_RATE_REFERENCE.csv` — 4 rows touched

| Row ID | Change | Rationale |
|:---|:---|:---|
| `rate_fr_partner_b2b_delivery_mid` | **Appended** | CS-06 anchor for Websitz `partner_b2b_delivery_operator` @ 100 EUR/hr |
| `rate_fr_partner_operator_continuity_mid` | Notes refresh | Hygiene C audit trail for Aisha rate |
| `rate_fr_founder_principal_senior` | Notes refresh | Remove stale orchestration_broker reference post D-IH-86-EL |
| `rate_fr_partner_business_development_senior` | Notes refresh | Align with bd_commission_overlay (0 billed rate on overlay rows) |

### `PARTNER_OVERLAP_EXCLUSION_CLAUSES.csv` — 1 row appended

| Row ID | Rationale |
|:---|:---|
| `clause_mentoring_methodology_in_progress` | Documents in-kind mentoring Holistika provides when `methodology_in_progress` pairs with `deep_partner_65_35`; prevents "35% compromise" narrative collapse per D-IH-86-EN |

### `COLLABORATOR_RATE_OVERRIDES.csv` — 0 rows

No commercial deviations ratified in this tranche; default splits and market bands hold.

### `DECISION_REGISTER.csv` — 1 row appended

| Decision | Purpose |
|:---|:---|
| `D-IH-95-K` | Ratifies Hygiene C settlement tranche scope C |

---

## Validator evidence

Commands (reproducible):

```powershell
py scripts/validate_collaborator_share.py --strict
py scripts/validate_hlk.py
```

Record verbatim results in commit message / CI; expected: CS-01..CS-09 PASS; HLK OVERALL PASS.

---

## CS-04 / CS-05 / CS-06 disposition

| Check | Pre-tranche | Post-tranche |
|:---|:---|:---|
| CS-04 | PASS (SUEZ overlay 85/0 + 0/15 anchored to D-IH-86-EL) | PASS; Aisha row now carries D-IH-86-EF override FK; Websitz 65/35 default with D-IH-95-K |
| CS-05 | PASS (SUEZ only) | PASS; 4 new in_kind deviations carry `bill_mode_decision_id=D-IH-95-K` |
| CS-06 | PASS (Aisha 60 EUR/hr within continuity band) | PASS; Websitz 100 EUR/hr within new B2B delivery band (75–140 typical ±25%) |

---

## Rows changed count

| CSV | Appended | Modified | Total touched |
|:---|---:|---:|---:|
| COLLABORATOR_SHARE_REGISTRY | 1 | 1 | **2** |
| HOLISTIKA_VENDOR_SERVICES_BILLED | 20 | 0 | **20** |
| COLLABORATOR_MARKET_RATE_REFERENCE | 1 | 3 | **4** |
| PARTNER_OVERLAP_EXCLUSION_CLAUSES | 1 | 0 | **1** |
| COLLABORATOR_RATE_OVERRIDES | 0 | 0 | **0** |
| DECISION_REGISTER | 1 | 0 | **1** |
| **Canonical subtotal** | | | **28** |

Planning surfaces (Hygiene B): charter amend (74→73 + footnote).

---

## Cross-references

- Hygiene research: [`i95-hygiene-research-2026-06-09.md`](i95-hygiene-research-2026-06-09.md)
- AskQuestion #2 ratification: [`i95-round2-askquestion2-ratification-2026-06-09.md`](i95-round2-askquestion2-ratification-2026-06-09.md)
- Collaborator-share discipline: `.cursor/rules/akos-collaborator-share.mdc`
- Doctrine: `COLLABORATOR_SHARE_DOCTRINE.md` §3.1 (Websitz precedent)
