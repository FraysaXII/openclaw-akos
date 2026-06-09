---
language: en
status: review
canonical: true
role_owner: SMO
classification: way_of_working
intellectual_kind: SOP
ssot: true
authored: 2026-05-12
last_review: 2026-05-12
companion_to:
  - SERVICE_CATALOG.csv
  - SLA_MATRIX.md
  - ../../PMO/WORKSPACE_BLUEPRINT_HOLISTIKA.md
  - ../../PMO/canonicals/HLK_ERP_ARCHITECTURE.md
Inherited Pattern: pattern_paired_sop_runbook
linked_runbooks:
  - scripts/validate_hlk.py
Paired Runbook: scripts/validate_hlk.py
Acceptance Criteria Human: SMO maintains SERVICE_CATALOG.csv weekly per §2.1 without automation.
Acceptance Criteria Automation: validate_hlk.py PASS includes catalog structural checks.
---

# SOP-SERVICE_MGMT_001 — SMO active charter (ITIL-derived)

> Authored I70 P8 (§8.6) per **D-IH-70-R** (SMO vs Account Management distinction) + Conundrum 9 ratification. Activates the **Service Management Office (SMO)** at `Operations/SMO/` with an ITIL-derived charter. SMO owns the WHAT (service catalog + SLAs + change/incident/release management); Account Management at `Marketing/Resonance/` owns the WHO (relationship + retention + customer success). Both active now per operator's Bâtard precedent + EFA pre-sold maintenance request.

## 1. Why activate SMO now

Pre-I70, the `Operations/SMO/` folder existed as an empty scaffold (per P2.5 v3.0 vault audit). Two signals motivated activation now (per Conundrum 9):

1. **EFA Académie pre-sold maintenance service** (per SUEZ engagement proposal §3 Continuité opérationnelle posture A; I12 P12). EFA is committed to post-launch maintenance; that service needs an explicit catalog entry + SLA + incident-response posture before delivery starts.
2. **Bâtard precedent** (operator-stated; see FOUNDER_TRAJECTORY_INTERNAL): post-engagement maintenance was deeply needed in operator's prior product-owner work; not having explicit SMO discipline cost the operator real engagements. SMO as active role prevents that recurrence.

## 2. SMO scope (ITIL-derived; Holistika-flavored)

SMO operates 5 ITIL practices, adapted for Holistika's engagement-shape work:

### 2.1 Service catalog management (SERVICE_CATALOG.csv)

- Maintains the active service inventory: per-service metadata (service_id + name + customer-facing-description + delivery-roles + cost-model + SLA-tier + active-engagements).
- Reviews weekly during active service delivery; quarterly during steady-state.
- Cross-references each service to the engagement(s) consuming it.
- Sibling: [`SERVICE_CATALOG.csv`](SERVICE_CATALOG.csv) (this commit; seed entry: SVC-001 SUEZ-WeBuy-maintenance per EFA pre-sold).

### 2.2 Service-level management (SLA_MATRIX.md)

- Per-service SLA tiers: response-time + resolution-time + uptime-commitment + incident-severity-mapping.
- Escalation paths per tier.
- Sibling: [`SLA_MATRIX.md`](SLA_MATRIX.md) (this commit; seed: 3 SLA tiers + 4 incident severities).

### 2.3 Change management

- Per-customer change-request flow: requester → SMO triage → impact assessment → operator approval → scheduled change → post-change verification.
- Lightweight today (operator + EFA partner-lead = small team); scales with operator + multi-operator invitation per HLK_ERP_ARCHITECTURE §8 trigger.

### 2.4 Incident management

- Per-incident severity assessment (P1-P4 per `SLA_MATRIX.md`).
- Initial response time + resolution-time commitment per severity.
- Post-incident review: cross-link to `LOGIC_CHANGE_LOG.md` (P9 forward-link) when incident reveals methodology drift.

### 2.5 Release management

- Per-engagement release planning: per-variant deliverable schedule (cross-link to `BRAND_GANTT_DISCIPLINE.md` Variant B + D Gantts).
- Release notes per delivered artifact.
- Cross-references to validate_*.py CI gate status.

## 3. SMO ownership boundary (D-IH-70-R codification)

To prevent dilution with Account Management (Marketing/Resonance/):

- **SMO owns the WHAT.** Service catalog + SLAs + change/incident/release management practices.
- **Account Management owns the WHO.** Per-account relationship + retention + customer success + per-engagement context-keeping.
- **Cross-area integration.** When a customer raises a concern: Account Management catches it (relationship signal), routes to SMO (service-level translation), SMO schedules + executes service-level response, Account Management closes the loop with the customer.
- **Shared artifacts.** Service catalog (SMO-authored) is consumed by Account Management for customer conversations. SLA matrix (SMO-authored) defines the commitments Account Management can make per account.
- **Both active now.** Per operator's Bâtard precedent + EFA pre-sold maintenance: neither role can be deferred without operational risk.

## 4. Service catalog seed (SVC-001 SUEZ-WeBuy-maintenance)

Per EFA Académie pre-sold maintenance service (proposal §3 Continuité opérationnelle posture A):

```
service_id: SVC-001
name: SUEZ-WeBuy maintenance (post-launch operations)
customer-facing-description: Continuité opérationnelle du processus WeBuy automatisé après mise en service
delivery_role_primary: EFA Académie partner-lead (incumbent operator)
delivery_role_secondary: Holistika Research (technology + governance)
cost_model: Forfait mensuel (à définir; reserved at engagement section 3 — tarification deferred-to-discovery)
sla_tier: Tier 2 (Standard)
active_engagements: 2026-suez-webuy
status: pre-sold; activates at engagement deliverable closure
```

Full SERVICE_CATALOG.csv seed at sibling [`SERVICE_CATALOG.csv`](SERVICE_CATALOG.csv).

## 5. Operating posture today

- This SOP at `status: review` (pending operator ratification of seed entries + SLA matrix).
- SVC-001 (SUEZ-WeBuy-maintenance) is the first active service; activates at SUEZ engagement deliverable closure.
- Future engagements declare service obligations at engagement-acceptance time; SMO catalog updated.
- Account Management (Marketing/Resonance/Account Management/) charter forward-link below; co-evolves with SMO.

## 6. Cross-references

- Sister canonical: [`SERVICE_CATALOG.csv`](SERVICE_CATALOG.csv) (this commit; SVC-001 seed).
- Sister canonical: [`SLA_MATRIX.md`](SLA_MATRIX.md) (this commit; 3 tiers + 4 severities).
- Account Management charter: `Marketing/Resonance/Account Management/canonicals/ACCOUNT_MANAGEMENT_CHARTER.md` (forward-link; sibling commit or P8 follow-on).
- `MARKETING_AREA_M3_REDESIGN.md` — Marketing M3 parent; Resonance sub-area home.
- `WORKSPACE_BLUEPRINT_HOLISTIKA.md` §16 (render pipeline ownership matrix; SMO is one of the 6 owners per active+future state).
- `HLK_ERP_ARCHITECTURE.md` §4 — `/operator/operations/smo/` panel reserves the SMO surface (P10.5 forward-link).
- D-IH-70-R (P3 ratification) — SMO vs Account Management distinction.
- Conundrum 9 — SMO + Account Management resolution.
- SUEZ engagement proposal §3 — EFA Académie pre-sold maintenance reference.
- I70 plan section 8.6 — full P8.6 deliverable spec.
