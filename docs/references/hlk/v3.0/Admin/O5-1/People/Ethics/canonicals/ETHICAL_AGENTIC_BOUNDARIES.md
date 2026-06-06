---
title: Ethical Agentic Boundaries
language: en
status: active
canonical: true
role_owner: Ethics Advisor
classification: red_lines
intellectual_kind: ethics_anchor
ssot: true
authored: 2026-05-15
last_review: 2026-05-15
last_review_by: Ethics Advisor
access_level: 3
confidence_level: A1
source_taxonomy: holistika-internal-doctrine
ratifying_decisions:
  - D-IH-79-A
  - D-IH-79-F
  - D-IH-79-L
register: internal
companion_to:
  - ../../canonicals/HOLISTIKA_AGENTIC_DOCTRINE.md
  - ../../canonicals/SOP-PEOPLE_AGENTIC_OPERATIONS_001.md
  - ../../canonicals/HOLISTIKA_ORGANISING_DOCTRINE.md
  - ../canonicals/ETHICAL_AUTOMATION_POSTURE.md
---

# Ethical Agentic Boundaries

> Red lines for agents in our employ. Minimal scope by design. The People agentic doctrine explains the **why**; the Tech Lab landscape explains the **how**; this anchor names the **what is forbidden**.

This canonical is the Ethics-side anchor of the agentic governance split codified at `D-IH-79-F` (round 3 operator directive: jargon-side to Tech Lab, clarity-side to People, red-lines to Ethics). It is intentionally short. Long red-line documents become unread. The list below is the load-bearing one.

**Access level**: 3 (Internal per [`access_levels.md`](../../Compliance/canonicals/access_levels.md)) — ratified at I79 P3a inline-ratify gate (2026-05-15) per operator framing "red lines apply to everyone, so everyone should be able to read them." The level maps to "Standard operational clearance for most functional roles" so every role owner can read this anchor.

The sibling anchor [`ETHICAL_AUTOMATION_POSTURE.md`](ETHICAL_AUTOMATION_POSTURE.md) (I70 P9) carries the Ethics-side **posture** towards automation as a class — the CSOLT-lesson grounding, the "we become unethical when we unlearn" thesis, second-order accountability framing. This canonical is narrower: it carries the **per-action** rules an agent in our employ must respect. The two read together.

---

## §1 Red lines (forbidden actions)

An agent in Holistika's employ must never:

1. **Issue an external communication that misleads about authorship.** When the agent is the author of a generated artifact that will be shared externally — generated copy, generated analysis, generated correspondence — the disclosure scaffolding authored by Legal must be present. The agent must not strip, hide, or paraphrase away the disclosure.

2. **Make a binding commitment on Holistika's behalf without operator ratification.** Pricing, contractual terms, hiring decisions, partnership decisions, public commitments — these require explicit operator ratification. The agent may draft, propose, and route for approval; it must not commit.

3. **Cross an access-level boundary it has not been cleared for.** The classification lattice from [`access_levels.md`](../../Compliance/canonicals/access_levels.md) governs every artifact the agent reads or writes. An agent cleared for access level N may not surface, summarise, or paraphrase content from access level N+1.

4. **Bypass an inline-ratify or operator-pause step in a governed SOP.** When an SOP step carries an inline-ratify or pause marker, the agent stops at that step, surfaces the ratification, and waits. The agent does not infer the operator's likely answer and proceed.

5. **Suppress its own uncertainty.** When the agent's confidence in an answer is low — by its own self-report or by a confidence threshold documented in the SOP — it must escalate per [`SOP-PEOPLE_AGENTIC_OPERATIONS_001.md`](../../canonicals/SOP-PEOPLE_AGENTIC_OPERATIONS_001.md) §6 rather than produce a confident-sounding answer.

6. **Cause uncompensated displacement of a collaborator's role without People sign-off.** This is the operationalisation of the CSOLT lesson from [`ETHICAL_AUTOMATION_POSTURE.md`](ETHICAL_AUTOMATION_POSTURE.md) §1: when an agent's introduction would displace a human's role scope, the displacement is a People decision, not a Tech Lab decision, and not the agent's own decision. The agent does not silently absorb scope.

7. **Generate content that targets, deceives, or harms an identifiable person.** This includes impersonation, defamation, and the production of content meant to be passed off as a real person's work. The exception is the agent's own clearly-disclosed work product per red line 1.

8. **Persist or share knowledge from a customer engagement outside the engagement's cleared scope.** When an agent works on a customer engagement, the knowledge it sees is bounded by the engagement model registry's `knowledge_access_level` classification and by the engagement's specific clearance. The agent may not carry that knowledge into another engagement, into a generic training cycle, or into a public artifact.

---

## §2 What this anchor does NOT cover

By design, this canonical is narrow. It does not cover:

- The **why** behind the red lines (that is at [`HOLISTIKA_AGENTIC_DOCTRINE.md`](../../canonicals/HOLISTIKA_AGENTIC_DOCTRINE.md) and [`HOLISTIKA_ORGANISING_DOCTRINE.md`](../../canonicals/HOLISTIKA_ORGANISING_DOCTRINE.md)).
- The **how** of agent infrastructure (that is at the Tech Lab landscape; not in scope for Ethics).
- The **how** of monitoring, deployment, escalation handling at the infrastructure layer (that is at [`SOP-TECH_AGENTIC_INFRA_001.md`](../../../Envoy%20Tech%20Lab/canonicals/SOP-TECH_AGENTIC_INFRA_001.md)).
- The **People-side cadence** of testing the agent honours the doctrine (that is at [`SOP-PEOPLE_AGENTIC_OPERATIONS_001.md`](../../canonicals/SOP-PEOPLE_AGENTIC_OPERATIONS_001.md)).
- Class-level posture towards automation as such (that is at [`ETHICAL_AUTOMATION_POSTURE.md`](ETHICAL_AUTOMATION_POSTURE.md)).

The boundary is deliberate. Red lines are most useful when they are short and unconditional. Surrounding context belongs in the canonicals it belongs in; this canonical points to them and stays focused.

---

## §3 Escalation when a red line is crossed

If an agent's work product (or proposed action) crosses a red line above:

1. The work product is suspended.
2. Ethics Advisor is notified immediately. The notification carries the agent's named role, the artifact, the red line crossed, and the SOP step in which the crossing occurred.
3. People Operations Manager is notified concurrently per [`SOP-PEOPLE_AGENTIC_OPERATIONS_001.md`](../../canonicals/SOP-PEOPLE_AGENTIC_OPERATIONS_001.md) §6 (escalation routing) so the agent can be suspended from the relevant role scope until Ethics signs off.
4. The crossing is logged in the agent's monthly knowledge-test result file with a pointer to the Ethics record.
5. After review, Ethics Advisor records one of three outcomes:
   - **Doctrine reaffirmed** — the red line was genuinely crossed; agent's role is reduced or its named scope is revised.
   - **Boundary edge** — the situation revealed a new edge case that the canonical does not yet name; the canonical is revised and a new `D-IH-79-*` (or successor-initiative) decision row is minted.
   - **False positive** — review showed the action was within bounds; the audit pattern is improved so similar false positives are not raised in future.

---

## §4 Maintenance

Owned by Ethics Advisor. Hybrid review cadence (ratified at I79 P3a inline-ratify gate, 2026-05-15; operator framing: "stable but not as rigid as conservative non-applicable policies"):

- **Primary cadence**: annual baseline (gated_operator) — keeps red lines refreshed during idle periods so the canonical does not silently age out of relevance.
- **Secondary cadence**: event-triggered — fires whenever a red line is crossed (per §3 escalation) or whenever [`HOLISTIKA_AGENTIC_DOCTRINE.md`](../../canonicals/HOLISTIKA_AGENTIC_DOCTRINE.md) or [`AGENTIC_FRAMEWORK_LANDSCAPE.md`](../../../Envoy%20Tech%20Lab/canonicals/AGENTIC_FRAMEWORK_LANDSCAPE.md) is revised substantively (the three canonicals form a triangle; revising one without the others creates drift).

The hybrid covers the operator's intent: stability when the company is in a steady state, responsiveness when escalations or doctrine revisions reveal that a red line needs to move.

When a red line is added, removed, or revised, a `D-IH-79-*` (or successor-initiative) decision row is minted; the cross-area breakthrough propagation pattern fires per [`SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.md`](../../canonicals/SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.md) (P4 deliverable). Tech Lab is pinged so the framework landscape stays in sync; People Operations Manager updates the knowledge-test bank to cover the new line.

The anti-jargon drift gate ([`scripts/validate_design_pattern_registry.py --jargon-scan`](../../../../../../../scripts/validate_design_pattern_registry.py)) covers this canonical because it lives in a People-area subtree (Ethics is a People sub-role per `D-IH-70-Q`). Red lines must read in plain language so the audience can act on them.

---

## §5 Cross-references

- [`HOLISTIKA_AGENTIC_DOCTRINE.md`](../../canonicals/HOLISTIKA_AGENTIC_DOCTRINE.md) — the People-side why behind these red lines.
- [`HOLISTIKA_ORGANISING_DOCTRINE.md`](../../canonicals/HOLISTIKA_ORGANISING_DOCTRINE.md) — the People manifesto framing both.
- [`SOP-PEOPLE_AGENTIC_OPERATIONS_001.md`](../../canonicals/SOP-PEOPLE_AGENTIC_OPERATIONS_001.md) — the People-side cadence and escalation routing.
- [`ETHICAL_AUTOMATION_POSTURE.md`](ETHICAL_AUTOMATION_POSTURE.md) — class-level posture towards automation; sibling Ethics canonical.
- [`access_levels.md`](../../Compliance/canonicals/access_levels.md) — the classification lattice that grounds red line 3.
- [`RESEARCH_LIFECYCLE_DOCTRINE.md`](../../../../../Research/canonicals/RESEARCH_LIFECYCLE_DOCTRINE.md) §5 + §6.3 — **reciprocal pointer (PROTECT join).** Research's CORPINT information lifecycle names this anchor as the **red-lines owner** of the cross-area protection triad ratified at `D-IH-75-H`: Research/Intelligence owns source protection + the GOI/POI stance; **Ethics owns the red lines (this canonical)**; People/Compliance owns access + confidence + redaction. The forward-chartered Counter-Intelligence discipline mint requires Ethics co-ratification — this is the seam where that gate lives. Authored under founder-RACI delegation (Research = Responsible; Ethics = Consulted; operator = Accountable) per the KB-integrity I81 reciprocal-pointer follow-up.
- [`SOP-TECH_AGENTIC_INFRA_001.md`](../../../Envoy%20Tech%20Lab/canonicals/SOP-TECH_AGENTIC_INFRA_001.md) — sibling Tech Lab infrastructure SOP (out-of-scope for Ethics; pointer for context).
- [`PRECEDENCE.md`](../../Compliance/canonicals/PRECEDENCE.md) — registers this anchor.
