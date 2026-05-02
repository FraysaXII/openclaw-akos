---
language: en
status: active
initiative: 47-user-centric-uat
report_kind: phase-report
phase: P5
program_id: shared
plane: ops
authority: System Owner
last_review: 2026-05-02
---

# I47 P5 — Tier-3 long-tail external personas (20 scenarios)

## What shipped

20 Tier-3 long-tail persona scenarios (4 personas × 5 each). Mixed per-persona distribution sums to overall 2/8/8/2 (10/40/40/10 percent).

| Persona | T | M | H | I | Total | Notes |
|:---|:--:|:--:|:--:|:--:|:--:|:---|
| PERSONA-PRESS | 1 | 2 | 2 | 0 | 5 | Brand Manager handles; Founder vetoes if sensitive |
| PERSONA-IDEA-PROPOSER | 0 | 2 | 2 | 1 | 5 | Informal first; advances to Channel 6 (JE) or Channel 2 (SC) |
| PERSONA-RANDOM-INBOUND | 1 | 2 | 2 | 0 | 5 | Catch-all; correct response is qualifying-question to bucket |
| PERSONA-CUSTOMER-SERVICE-PROSPECT | 0 | 2 | 2 | 1 | 5 | 30-min discovery + scope-shaping doc |
| **TOTAL Tier-3** | **2** | **8** | **8** | **2** | **20** | |

Cumulative state (post-P5): **225 total scenarios across all 16 PERSONA_REGISTRY archetypes + OPERATOR pseudo (17 distinct personas)**. Distribution `{trivial: 25 (11%), moderate: 90 (40%), hard: 90 (40%), impossible: 20 (9%)}` — within ±5% of D-IH-47-C target.

## Coverage discipline highlights

### PERSONA-PRESS

- **SCN-PRS-005-V1** (hard): "tax structures of EU AI startups, Madeira ZFM angle" → Founder veto MUST trigger; high-sensitivity press topic; correct response involves Brand Manager + Founder veto + legal counsel

### PERSONA-IDEA-PROPOSER

- **SCN-IDA-003-V1** (hard): informal-friend-relationship escalating to "draft term sheet by next week" → correct response is to redirect to Channel 6 3-of-3 gate; informal does NOT bypass gate
- **SCN-IDA-004-V1** (hard, cross_axis): MVP + paying customers + departing co-founder → multi-channel signal (Channel 2 + Channel 6 + advisor); correct response is Founder + 1-on-1
- **SCN-IDA-005-V1** (impossible): "predict if my SaaS will be unicorn" → REFUSE

### PERSONA-RANDOM-INBOUND

- **SCN-RAN-001-V1** (trivial): just "Hi." → correct response is qualifying-question; tests catch-all-routing baseline
- **SCN-RAN-004-V1** (hard): ambiguous multi-persona signal ("hiring, raising, OR selling — interested in all 3") → re-bucket
- **SCN-RAN-005-V1** (hard, cross_axis): multi-channel complaint (email + LinkedIn + web form) → tests channel × distance × catch-all awareness

### PERSONA-CUSTOMER-SERVICE-PROSPECT

- **SCN-CSP-003-V1** (hard): 4-month engagement + 3 senior engineers + 14-day SoW → 30-min-discovery-first; not autonomous-quote
- **SCN-CSP-004-V1** (hard, cross_axis, es): LATAM + LGPD + multi-language docs → multi-region + multi-language + compliance span

## Verification

- `py scripts/validate_persona_scenario_registry.py` → PASS (225 rows, 17 distinct personas)
- All 16 PERSONA_REGISTRY archetypes now exercised plus OPERATOR pseudo
- Distribution `{trivial: 25 (11%), moderate: 90 (40%), hard: 90 (40%), impossible: 20 (9%)}` within ±5% of target

## Cumulative library complete (operator + Tier-1 + Tier-2 + Tier-3)

| Tier | Personas | Scenarios | Cumulative |
|:----:|:--------:|:---------:|:----------:|
| OP   | 1 (OPERATOR pseudo) | 25 | 25 |
| 1    | 4 | 100 | 125 |
| 2    | 8 | 80 | 205 |
| 3    | 4 | 20 | 225 |

P6 (~25 cross-axis), P7 (~30 adversarial), P8 (~30 benchmark), P9 (~16 recovery) will bring the total to ~325 scenarios.

## Cross-references

- D-IH-47-A (PERSONA_SCENARIO_REGISTRY.csv as canonical SSOT)
- D-IH-47-B (Tier-3 long-tail: 4 × 5 = 20 scenarios)
- D-IH-47-C (10/40/40/10 distribution; cumulative within ±5%)
- I31 P2 (PERSONA_REGISTRY.csv source — all 16 archetypes now exercised)
