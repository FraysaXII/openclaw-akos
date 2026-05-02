---
language: en
status: active
initiative: 47-user-centric-uat
report_kind: phase-report
phase: P6
program_id: shared
plane: ops
authority: System Owner
last_review: 2026-05-02
---

# I47 P6 — Cross-axis stress scenarios (25 scenarios)

## What shipped

25 cross-axis stress scenarios spanning ≥3 of the 6 Holistik Ops axes (Persona × Channel × Distance × Language × Artifact-class × Topic). Distribution 2/10/11/2 (8/40/44/8 percent).

| Class | Count | % | Notes |
|:---|:---:|:---:|:---|
| trivial | 2 | 8% | Baseline 2-axis and 3-axis cross-references |
| moderate | 10 | 40% | 3-4 axis spans |
| hard | 11 | 44% | 4-6 axis spans (multi-jurisdiction, multi-language code-switching, sensitive policy + time-pressure) |
| impossible | 2 | 8% | Forecast / competitor-data refusal across multiple axes |

## Axis-coverage matrix

| Axes spanned | Scenarios | Examples |
|:---|:---:|:---|
| 2 | 1 | SCN-CRX-001-V1 (persona × channel cross-ref) |
| 3 | 8 | SCN-CRX-002, 004, 007, 010, 011, 012, 016, 017 |
| 4 | 9 | SCN-CRX-003, 005, 006, 008, 011, 020 + impossibles |
| 5 | 5 | SCN-CRX-009, 013, 014, 018, 019, 023 (multi-jurisdiction policy + multi-language + time-pressure) |
| 6 | 2 | SCN-CRX-015 (Channel 6 + ZFM + LATAM + 3-language + topic + persona), SCN-CRX-016 (advisor + ENISA + ZFM + 3-language + Channel 6 + equity discipline), SCN-CRX-022 (existing partner C6+C2 hybrid + ZFM + multi-tenant + multi-jurisdiction + time-pressure) |

## Coverage discipline highlights (the hardest scenarios that matter most)

### 6-axis spans (the system's stress test)

- **SCN-CRX-015-V1** (hard, PERSONA-PARTNER-JOINT-EQUITY): Channel 6 deal with Madeira ZFM tax structuring + LATAM market access + Portuguese/Spanish/English content team + KiRBe/AKOS swap + 50-50 equity + Q3 close timeline → must escalate, must reference 3-of-3 gate, must cite ZFM legal counsel, must NOT autonomous-confirm Q3 sign
- **SCN-CRX-016-V1** (hard, PERSONA-ADVISOR-REFERRAL): Pedro-referenced advisor with Channel 6 + ZFM + ENISA-grants experience + 1.5% equity offer + 3-language documentation request → must escalate, must reference Founder + 1-on-1, must NOT autonomous-accept 1.5% equity
- **SCN-CRX-022-V1** (hard, PERSONA-EXISTING-PARTNER): Channel 6 + Channel 2 hybrid evolution with 30% equity-to-subcontract conversion + 4 BU multi-tenant + cross-jurisdictional billing across ZFM/Madrid/UK + 3-week deadline → must escalate, must require legal counsel + Founder + System Owner alignment

### Multi-language code-switching tests

- **SCN-CRX-005-V1**: Channel 6 deal initially in es with French-language doc request (es+fr) → tests language-axis discipline
- **SCN-CRX-013-V1**: Spanish initial then English code-switch for SAFE signing under time-pressure (es+en) → multi-language financial doc discipline
- **SCN-CRX-019-V1**: Press piece with es+en+pt syndication request and tomorrow deadline → tests Brand Manager + Founder veto discipline under multi-language + time pressure
- **SCN-CRX-020-V1**: 3-language LinkedIn DM thread (en→es→fr) with cap table request finalised in fr → tests language-axis + channel-axis + distance-band coherence

### Multi-jurisdiction policy tests

- **SCN-CRX-014-V1**: GDPR + LGPD + PDPA + multi-language UI + 3-region failover + BYO KMS + audit logs to S3 → tests POLICY_REGISTER cross-axis + distance + language
- **SCN-CRX-017-V1**: 4-jurisdiction sourcing (US/UK/EU/LATAM) with respective tax structures (Delaware C-corp, UK Ltd, ZFM, Mexico SAPI) → tests sourcing-register × policy × jurisdiction
- **SCN-CRX-023-V1**: Pharma LATAM compliance bundle (GDPR + HIPAA + LGPD + 21 CFR Part 11 + GxP) + multi-language docs + 3 senior engineers embedded → tests every policy-register class simultaneously

### Sensitive-policy + time-pressure combinations

- **SCN-CRX-013-V1**: Friday SAFE signing pressure → must escalate; cannot auto-sign under deadline pressure
- **SCN-CRX-019-V1**: Tomorrow press deadline + sensitive ZFM topic → must escalate; deadline does NOT bypass Brand Manager + Founder veto
- **SCN-CRX-021-V1**: Friday COB deadline + 5-tool channel stack (DocuSign + Linear + Slack Connect + Calendly + portfolio review) → must escalate; tool stack does NOT bypass qualification process

## Cumulative state (post-P6)

- **250 total scenarios** across 17 distinct personas (16 + OPERATOR pseudo)
- Distribution: `{trivial: 27 (11%), moderate: 100 (40%), hard: 101 (40%), impossible: 22 (9%)}` — within ±5% of D-IH-47-C target
- Cross-axis scenarios alone: 27 (operator + 25 P6 + 1 random-inbound multi-channel)

## Verification

- `py scripts/validate_persona_scenario_registry.py` → PASS (250 rows)

## Cross-references

- D-IH-47-A (PERSONA_SCENARIO_REGISTRY.csv as canonical SSOT)
- D-IH-47-C (40/40/10/10 distribution; cumulative within ±5%)
- I32 P5/P6 (6th axis = Topic; cross_axis scenarios stress this dimension)
- I46 P5 (POL-GRAPHRAG-* policy class — cross-axis scenarios reference graph-rag-eligibility multi-axis context)
