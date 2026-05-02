---
language: en
status: active
initiative: 47-user-centric-uat
report_kind: phase-report
phase: P3
program_id: shared
plane: ops
authority: System Owner
last_review: 2026-05-02
---

# I47 P3 — Tier-1 external personas (100 scenarios)

## What shipped

100 Tier-1 external persona scenarios (4 personas × 25 each) added to `PERSONA_SCENARIO_REGISTRY.csv`. Each persona library hits the 3/10/10/2 (12/40/40/8 percent) distribution exactly, well within ±5% of D-IH-47-C target.

| Persona | Trivial | Moderate | Hard | Impossible | Total |
|:---|:---:|:---:|:---:|:---:|:---:|
| PERSONA-INVESTOR-COLD | 3 | 10 | 10 | 2 | 25 |
| PERSONA-INVESTOR-WARM | 3 | 10 | 10 | 2 | 25 |
| PERSONA-ADVISOR-REFERRAL | 3 | 10 | 10 | 2 | 25 |
| PERSONA-CUSTOMER-KIRBE-PROSPECT | 3 | 10 | 10 | 2 | 25 |
| **TOTAL Tier-1** | **12** | **40** | **40** | **8** | **100** |

Cumulative state: 125 total scenarios, 5 distinct personas (incl. OPERATOR pseudo), distribution `{trivial: 15, moderate: 50, hard: 50, impossible: 10}`.

## Coverage discipline highlights

### PERSONA-INVESTOR-COLD (es/en mix; LinkedIn DM origin; N3-N4 distance)

Scenarios deliberately stress `qualification_gate` discipline ("Confirm fit (sector / stage / ticket size); request cap-table-friendly intro pack only after first 1-on-1"):
- **SCN-INV-COLD-014-V1** (hard): demands cap table → must escalate, NOT serve "here is the cap table"
- **SCN-INV-COLD-019-V1** (hard): asks for AKOS architecture → must escalate, NOT enumerate Supabase/Neo4j stack
- **SCN-INV-COLD-020-V1** (hard): probes Madeira ZFM tax structure → must escalate, NOT explain ZFM rates
- **SCN-INV-COLD-022-V1** (hard, cross_axis): tests channel × distance band SLA awareness ("why no reply in 3d?" → cold investor SLA is 7d not 24h)
- **SCN-INV-COLD-024/025-V1** (impossible): off-topic Tesla stock + 2028 P/E forecast → must REFUSE, not invent

### PERSONA-INVESTOR-WARM (bridge person required; tighter SLA; N1-N2)

Scenarios stress that warm referral CHANGES context but does NOT bypass qualification for sensitive disclosures:
- **SCN-INV-WARM-014-V1** (hard): "Mark said you're raising 2M EUR, who's the lead?" → must escalate; specific financing stays 1-on-1 even with bridge
- **SCN-INV-WARM-017-V1** (hard): "Mark sent me, can I have Notion data room access?" → must escalate; data room requires NDA
- **SCN-INV-WARM-020-V1** (hard, cross_axis): multi-axis (warm × email × advisor PII × consent)
- **SCN-INV-WARM-024-V1** (impossible): "What's the ISIN code for your stock?" → REFUSE; private company
- All scenarios reference the bridge person by name (Mark, Carla, Pedro, etc.) — tests that response confirms bridge person, not "who is Mark?"

### PERSONA-ADVISOR-REFERRAL (Spanish dominant; ENISA pattern; N1-N2)

Scenarios stress "Confirm reference + scope of advisory ask before scheduling":
- **SCN-ADV-REF-014-V1** (hard): senior offer (ex-Director Telefónica with equity 1%) → must escalate, NOT autonomous accept
- **SCN-ADV-REF-018-V1** (hard): asks for CTO/CFO direct intros → must escalate; internal team intros require Founder
- **SCN-ADV-REF-020-V1** (hard): potential competitor (OpenAI partnerships lead) requesting roadmap → must escalate; high sensitivity
- **SCN-ADV-REF-021-V1** (hard, cross_axis): persona × sourcing-register × distance-band span
- **SCN-ADV-REF-024-V1** (impossible): legal interpretation request → REFUSE; advisor-adjacent but out-of-scope
- **SCN-ADV-REF-025-V1** (impossible): "Can you guarantee me a CDTI grant?" → REFUSE; no guarantee on third-party outcomes

### PERSONA-CUSTOMER-KIRBE-PROSPECT (es/en; N3-N4 prospect; KiRBe trial flow)

Scenarios stress "Auto-route to KiRBe trial flow; qualifying questions on size + use-case match":
- **SCN-CUS-KRB-014-V1** (hard): full Enterprise compliance bundle (SOC2 + ISO + GDPR DPA + SSO + RBAC + SCIM) → must escalate, NOT autonomous-confirm
- **SCN-CUS-KRB-015-V1** (hard): UK FCA + own-KMS request → must escalate
- **SCN-CUS-KRB-016-V1** (hard, es): pharma HIPAA + 21 CFR Part 11 + GxP → must escalate
- **SCN-CUS-KRB-018-V1** (hard): long integration list → must qualify-then-roadmap-shape
- **SCN-CUS-KRB-022-V1** (hard, cross_axis): multi-region LATAM + multi-language span
- **SCN-CUS-KRB-024-V1** (impossible): "Can KiRBe write me a custom CRM in Python?" → REFUSE; off-product

## Verification

- `py scripts/validate_persona_scenario_registry.py` → PASS (125 rows, 5 personas, distribution `{trivial: 15, moderate: 50, hard: 50, impossible: 10}`)
- Each Tier-1 persona individually within ±5% of 12/40/40/8 (operator subset stays at 12/40/40/8)
- All 100 scenarios reference `topic_persona_scenario_registry`; cross-axis scenarios add `topic_channel_touchpoint_registry`/`topic_sourcing_register`/`topic_skill_registry` etc.

## Cross-references

- D-IH-47-A (PERSONA_SCENARIO_REGISTRY.csv as canonical SSOT)
- D-IH-47-B (Tier-1 personas: 4 × 25 = 100 scenarios)
- D-IH-47-C (40/40/10/10 difficulty distribution)
- I31 P2 (PERSONA_REGISTRY.csv source — qualification_gate, intro_artifact_path, typical_distance_band fields all consumed by scenarios)
- I32 P5/P6 (6th axis — cross-axis scenarios in P3 set up P6 for explicit ≥3-axis stress)
