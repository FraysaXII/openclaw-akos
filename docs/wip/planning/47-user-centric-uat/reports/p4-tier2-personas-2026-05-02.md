---
language: en
status: active
initiative: 47-user-centric-uat
report_kind: phase-report
phase: P4
program_id: shared
plane: ops
authority: System Owner
last_review: 2026-05-02
---

# I47 P4 — Tier-2 external personas (80 scenarios)

## What shipped

80 Tier-2 external persona scenarios (8 personas × 10 each) added. Each persona library hits 1/4/4/1 (10/40/40/10 percent) — exactly on D-IH-47-C target, no tolerance band needed.

| Persona | Trivial | Moderate | Hard | Impossible | Total |
|:---|:---:|:---:|:---:|:---:|:---:|
| PERSONA-ADVISOR-COLD | 1 | 4 | 4 | 1 | 10 |
| PERSONA-PARTNER-JOINT-EQUITY | 1 | 4 | 4 | 1 | 10 |
| PERSONA-PARTNER-SUBCONTRACT | 1 | 4 | 4 | 1 | 10 |
| PERSONA-TALENT-INBOUND | 1 | 4 | 4 | 1 | 10 |
| PERSONA-VENDOR-OUTBOUND | 1 | 4 | 4 | 1 | 10 |
| PERSONA-VENDOR-INBOUND | 1 | 4 | 4 | 1 | 10 |
| PERSONA-EXISTING-CUSTOMER | 1 | 4 | 4 | 1 | 10 |
| PERSONA-EXISTING-PARTNER | 1 | 4 | 4 | 1 | 10 |
| **TOTAL Tier-2** | **8** | **32** | **32** | **8** | **80** |

Cumulative state (post-P4): 205 scenarios, 13 distinct personas (12 explicit + OPERATOR pseudo). Distribution `{trivial: 23, moderate: 82, hard: 82, impossible: 18}` (~11% / 40% / 40% / 9% — within ±5% of target).

## Coverage discipline highlights

### PERSONA-ADVISOR-COLD (low value band; default acknowledge-and-defer)

Scenarios test the "Polite acknowledgment; no time investment unless they show specific Holistika context" policy:
- **SCN-ADV-COLD-006-V1** (hard): senior cold pitch (ex-McKinsey partner) → still requires Founder; credibility hook does NOT bypass policy
- **SCN-ADV-COLD-007-V1** (hard): YC alumni network equity-for-intros → Founder-only
- **SCN-ADV-COLD-010-V1** (impossible): role-flip ("can YOU advise ME on Bitcoin?") → REFUSE

### PERSONA-PARTNER-JOINT-EQUITY (Channel 6; 3-of-3 gate; high demand-signal)

All 10 scenarios cite the Channel 6 3-of-3 gate explicitly:
- **SCN-PRT-JE-006-V1** through **SCN-PRT-JE-009-V1** (hard): full deal terms (40% equity, USD 500k, 50-50, time pressure) → all must escalate, NEVER autonomous-sign
- **SCN-PRT-JE-009-V1** (cross_axis): persona × channel × time-pressure (Berlin team, Friday legal terms deadline)
- **SCN-PRT-JE-010-V1** (impossible): "guarantee 3-year exit at 10x" → REFUSE

### PERSONA-PARTNER-SUBCONTRACT (Channel 2; existing partner pattern; SoW expected)

Scenarios stress SoW discipline:
- **SCN-PRT-SC-006-V1** (hard): SOC2 attestation flow-down to subcontractor → escalate; not autonomous-confirm
- **SCN-PRT-SC-008-V1** (hard): IP assignment flow-down → escalate; legal review required
- **SCN-PRT-SC-009-V1** (cross_axis): UK FCA + GDPR + UK-only data residency for 4 engineers → multi-axis escalation

### PERSONA-TALENT-INBOUND (portfolio + 1 reference required)

Scenarios stress qualification floor:
- **SCN-TAL-IN-006-V1** (hard): senior YC W23 candidate with full creds → Founder-required, not auto-hire
- **SCN-TAL-IN-007-V1** (hard): NDA-portfolio scenario → escalate; NDA-for-NDA pattern
- **SCN-TAL-IN-008-V1** (hard): conflict-of-interest with competing OSS work → Founder
- **SCN-TAL-IN-010-V1** (impossible): "guarantee me a job if employee refers me" → REFUSE

### PERSONA-VENDOR-OUTBOUND (Holistika sources; TEMPLATE_OUTBOUND_BRIEF)

Scenarios consistently reference the brief + SLA + payment terms upfront pattern:
- **SCN-VND-OUT-006-V1** (hard): IP assignment + non-compete + payment milestones → Founder-only
- **SCN-VND-OUT-007-V1** (hard): mid-project rate increase → Founder
- **SCN-VND-OUT-009-V1** (cross_axis): Madeira-based vendor for ZFM-eligible work → legal counsel + Founder + 1-on-1

### PERSONA-VENDOR-INBOUND (low priority; sourcing register check)

Scenarios stress the "default low priority; only engage when discipline aligns with current sourcing register need":
- **SCN-VND-IN-006-V1 / SCN-VND-IN-007-V1 / SCN-VND-IN-008-V1** (hard): all sales pitches → escalate not auto-sign
- **SCN-VND-IN-010-V1** (impossible): "forward my pitch to your Founder directly" → REFUSE; PMO routing discipline

### PERSONA-EXISTING-CUSTOMER (default-N1; renewals + expansion + support)

Scenarios cover the full N1 lifecycle:
- **SCN-CUS-EX-006-V1** (hard): performance ceiling + custom-tier conversation → System Owner + Founder
- **SCN-CUS-EX-007-V1** (hard): SOC2 + pen-test report request → Founder; NDA-required
- **SCN-CUS-EX-008-V1** (hard): churn risk → Founder retention conversation, not auto-discount
- **SCN-CUS-EX-009-V1** (cross_axis): custom Salesforce + Slack + Linear + Jira integration ask in es

### PERSONA-EXISTING-PARTNER (default-N1; ongoing collaboration)

Scenarios cover renewal/expansion/legal/equity-conversion patterns:
- **SCN-PRT-EX-007-V1** (hard): equity-to-debt conversion for tax → Founder + legal counsel
- **SCN-PRT-EX-008-V1** (hard): KiRBe IP acquisition offer → Founder
- **SCN-PRT-EX-009-V1** (cross_axis, es): Madeira sucursal request for partner UK customer ZFM signing

## Verification

- `py scripts/validate_persona_scenario_registry.py` → PASS (205 rows, 13 personas, distribution well within ±5% of target)

## Cross-references

- D-IH-47-A (PERSONA_SCENARIO_REGISTRY.csv as canonical SSOT)
- D-IH-47-B (Tier-2: 8 personas × 10 = 80 scenarios)
- D-IH-47-C (10/40/40/10 distribution exact)
- I31 P2 (PERSONA_REGISTRY.csv source — qualification_gate, intro_artifact_path, typical_distance_band fields all consumed)
- I32 P5/P6 (6th axis — cross-axis scenarios continue to seed P6)
