---
language: en
status: review
canonical: true
role_owner: SMO
classification: way_of_working + fact
intellectual_kind: SLA_specification
ssot: true
authored: 2026-05-12
last_review: 2026-05-12
---

# SLA_MATRIX — Service-level commitments per tier + incident severity

> Authored I70 P8 (§8.6) per `SOP-SERVICE_MGMT_001.md` §2.2. Codifies 3 service tiers + 4 incident severities + escalation paths. Status `review` pending operator ratification of specific time commitments + cost-model implications.

## 1. Three SLA tiers

| Tier | Label | Response time (initial) | Resolution time (target) | Uptime commitment | Cost-model implication |
|:---|:---|:---|:---|:---|:---|
| **Tier 1** | Premium | ≤ 4 business hours | P1: ≤ 1 business day; P2: ≤ 3 days; P3: ≤ 10 days; P4: best-effort | 99.5% (over rolling 90 days) | + 50% over base service forfait |
| **Tier 2** | Standard | ≤ 1 business day | P1: ≤ 2 business days; P2: ≤ 5 days; P3: ≤ 14 days; P4: best-effort | 99.0% (over rolling 90 days) | base service forfait |
| **Tier 3** | Light | ≤ 3 business days | P1: ≤ 5 business days; P2: ≤ 10 days; P3: ≤ 21 days; P4: best-effort | 98.0% (over rolling 90 days) | – 30% off base service forfait |

**Operating-hours definition.** Business hours = 9:00–18:00 Madrid time (Holistika Research SL primary office), Monday–Friday, excluding Spanish national holidays. EFA Académie partner-lead operates Cameroon-time (WAT) with overlap window 11:00–17:00 Madrid time on Monday–Thursday. Per-engagement override allowed (e.g., SUEZ procurement primary contact in France could trigger 9:00–18:00 Paris time override).

## 2. Four incident severities

| Severity | Label | Definition | Default tier | Customer-facing impact |
|:---|:---|:---|:---|:---|
| **P1** | Critical | Service unavailable; primary use-case blocked; no workaround | All tiers | Blocking |
| **P2** | Major | Partial unavailability; primary use-case degraded; manual workaround possible | All tiers | Significant |
| **P3** | Minor | Cosmetic / non-blocking issue; secondary use-case affected | All tiers | Minimal |
| **P4** | Enhancement | Feature request / improvement; no current functional impact | All tiers | None (feature-roadmap candidate) |

## 3. Escalation paths

- **P1** triggers immediate notification to operator (Holistika Research SL CEO + EFA Académie partner-lead per per-engagement notification list). Resolution work begins within initial-response-time window.
- **P2** triggers next-business-day notification. Operator + SMO co-triage; assigns delivery role per service catalog.
- **P3** triggers weekly batch review. SMO bundles for next scheduled change window.
- **P4** triggers monthly batch review. Feeds the customer's feature-roadmap conversation (Account Management territory per Marketing/Resonance/).

## 4. SUEZ engagement (worked example)

SUEZ-WeBuy maintenance service (SVC-001) is **Tier 2 Standard** per `SERVICE_CATALOG.csv`:
- Initial response time: ≤ 1 business day.
- P1 resolution: ≤ 2 business days; P2: ≤ 5 days; P3: ≤ 14 days; P4: best-effort.
- Uptime: 99.0% over rolling 90 days.
- Operating hours: 9:00–18:00 Paris time (override per per-engagement contact).
- Notification list: SUEZ procurement primary contact + EFA Académie partner-lead + Holistika Research SL CEO.

Per-incident response is owned by EFA Académie partner-lead (incumbent operator) with Holistika Research SL escalation backup; full posture detail at `2026-suez-webuy/02-customer-pack/proposal.customer.fr.md` §3 Continuité opérationnelle posture A.

## 5. Cross-references

- Parent SOP: [`SOP-SERVICE_MGMT_001.md`](SOP-SERVICE_MGMT_001.md) §2.2 (service-level management).
- Sister: [`SERVICE_CATALOG.csv`](SERVICE_CATALOG.csv) — per-service tier assignment.
- Future cross-link: per-engagement SLA-rider docs at `<engagement>/01-operator-pack/sla-rider.md` when SLA varies per engagement.
- HLK_ERP_ARCHITECTURE.md §4 — `/operator/operations/smo/` panel reserves SLA-tier visibility surface.
