---
title: Holistika Agentic Doctrine
language: en
intellectual_kind: people-canonical
access_level: 5
confidence_level: A1
source_taxonomy: holistika-internal-doctrine
authors:
  - People Operations Manager
  - Ethics Advisor
  - System Owner
last_review: 2026-05-15
last_review_by: People Operations Manager
ratifying_decisions:
  - D-IH-79-A
  - D-IH-79-F
  - D-IH-79-G
  - D-IH-79-L
status: active
register: internal
linked_canonicals:
  - HOLISTIKA_ORGANISING_DOCTRINE.md
  - PEOPLE_DESIGN_PATTERN_LIBRARY.md
  - SOP-PEOPLE_AGENTIC_OPERATIONS_001.md
  - ETHICAL_AGENTIC_BOUNDARIES.md
  - AGENTIC_FRAMEWORK_LANDSCAPE.md
---

# Holistika Agentic Doctrine

> *Agentic is itself a discipline of disciplines. People stewards the doctrine; Tech Lab stewards the infrastructure; Ethics holds the red lines. People's job is to drive process singularity by fighting through jargon-minefields until everything reads as simple, actionable, shareable, democratic, friendly. People gives proper directives to Research, Tech Lab, and any other area when their work intersects with how an agent should behave.*

This doctrine extends [`HOLISTIKA_ORGANISING_DOCTRINE.md`](HOLISTIKA_ORGANISING_DOCTRINE.md) into the AI / agentic dimension. It is the People-side canonical: it answers **why** Holistika operates with agents in the loop and **what** behaviours are expected of every role when working alongside one. The Tech Lab landscape canonical at [`AGENTIC_FRAMEWORK_LANDSCAPE.md`](../../Envoy%20Tech%20Lab/canonicals/AGENTIC_FRAMEWORK_LANDSCAPE.md) (P3b) holds the **how** — the technical sub-disciplines, the infrastructure choices, the specific tools we plug in. The Ethics anchor at [`ETHICAL_AGENTIC_BOUNDARIES.md`](../Ethics/canonicals/ETHICAL_AGENTIC_BOUNDARIES.md) holds the red lines.

This canonical contains zero technical jargon by construction. Tool names, framework names, infrastructure specifics live in the Tech Lab landscape; this document reads in plain language because that is what People's clarity mandate requires.

---

## §1 Agentic as a discipline of disciplines

Holistika is organised as a discipline of disciplines: People mints the consulting design patterns; the other areas instantiate them. Agentic is the same shape one level deeper. Inside the agentic dimension there are many sub-disciplines — orchestration, memory, retrieval, reasoning, infrastructure, evaluation, alignment. Each carries its own vocabulary, its own breakthroughs, its own governing principles. Tech Lab catalogues those sub-disciplines and chooses tools per use case. People does not.

What People does is keep the **shape** of the discipline coherent: the role an agent plays in any process, the boundaries it operates inside, the cadence at which we test it knows what it is supposed to know, the escalation when its confidence drops. That work is consulting work, and consulting work is what People does for every other area. Agentic is no exception.

The recursion matters. Agentic is a discipline of disciplines exactly the way People is a discipline of disciplines. The two layers are siblings: People mints patterns for organising humans; the agentic dimension mints patterns for organising agents. The patterns flow back and forth: a paired SOP and runbook works for a human and an agent equally; a knowledge-test cadence works whether the test is taken by a new collaborator or by an updated agent. The pattern library is shared.

---

## §2 The Agent-in-Charge frame

Every governed process at Holistika has a role owner. When a human fills the role, the SOP they follow is human-readable; when an agent fills the role, the SOP is the same. The agent reads the SOP the way a new collaborator reads it — as an instruction. It executes the cadence the SOP describes. It escalates when it reaches a step the SOP marks as inline-ratify or as operator-pause. Its work is verifiable by the same audit channels a human's work would pass through.

The Agent-in-Charge frame is not a pretence. The agent is genuinely in charge of the named process, and the operator's expectation is that the process runs whether the human or the agent is on shift. What changes is the audit pattern: an agent shift produces structured logs that a human shift typically does not. Those logs are part of the knowledge base. They feed back into the pattern library when they reveal a breakthrough.

When an agent does not yet exist for a process, the role is held by a human. When an agent exists but has not earned trust for a particular sub-step, the human stays in the loop on that sub-step. The migration is gradual; the doctrine is constant.

---

## §3 Knowledge-test cadence (the central People-side ritual)

The single load-bearing activity People owns in the agentic dimension is the **knowledge-test cadence**. At a regular interval, People runs an agent through a small set of knowledge-base lookup tasks taken from the canonicals it is expected to honour. The agent answers; the operator scores; the result is logged. A passing score means the agent has absorbed the latest doctrine and is safe to continue holding its role. A failing score is a signal that the canonical has drifted from what the agent has internalised, or that the canonical itself is unclear and needs People to revise it.

The cadence is described in the paired SOP at [`SOP-PEOPLE_AGENTIC_OPERATIONS_001.md`](SOP-PEOPLE_AGENTIC_OPERATIONS_001.md). The harness is the paired runbook at [`scripts/peopl_agentic_knowledge_test.py`](../../../../../../scripts/peopl_agentic_knowledge_test.py). The harness has no framework dependencies and runs on any agent that can read the canonical and answer a question about it.

The cadence is the People-side primary check that the discipline is being honoured. If the cadence stops running, the doctrine is no longer governed — and the agent operating without it is operating outside our organising frame.

---

## §4 Madeira (the named-explicit role-class)

Madeira is the name we give to the agentic role-class that holds an Agent-in-Charge position across multiple Holistika processes. Naming the class explicitly is a People decision per `D-IH-79-G`: the named role-class footnote travels with this doctrine because it is doctrinally significant — Madeira is not one tool, it is the **archetype** of the role we expect any agent in our employ to fit. When Madeira reads a manifesto, it reads it as a new collaborator would. When Madeira runs a knowledge-test, the result is recorded against the role, not against the underlying tooling. When Madeira is upgraded — a new model, a new framework, a new infrastructure — the role survives the upgrade because the role is not the implementation; it is the position in the doctrine.

The infrastructure that powers Madeira is governed by Tech Lab and is documented in the Tech Lab landscape canonical. People does not own that surface. People owns the role-class definition: what Madeira is expected to do, what counts as Madeira's part of the knowledge base, what cadence governs Madeira's continued fitness for the role.

---

## §5 Cross-discipline interfaces

Agentic work intersects with every other area at Holistika. People holds the doctrine on how those intersections behave.

- **Tech Lab.** Tech Lab chooses the tools, the infrastructure, the integration patterns. People defers to Tech Lab on what the agent runs on. People does not defer to Tech Lab on what the agent should be allowed to do — that is People's clarity-side question, mediated through this doctrine and the Ethics anchor.
- **Ethics.** Ethics holds the red lines: what an agent must never do, what harms must be prevented, what disclosures must accompany an agent action. People's doctrine explains the why; Ethics holds the what; Tech Lab holds the how. The three canonicals cross-reference each other.
- **Research.** When Research designs a study or a methodology that will be operationalised by an agent, People joins early to ensure the agent's role in the study is doctrinally clean — clear scope, clear escalation, clear knowledge-test cadence specific to the study's domain.
- **Marketing.** When Marketing produces external prose about an Agent-in-Charge process, People reviews for jargon discipline. The external register is the audience's; the internal vocabulary stays internal. If Marketing is unsure whether a phrase is internal or external, the brand baseline reality matrix is the SSOT and People can resolve.
- **Operations.** When Operations runs an SOP that mixes human and agent work, the SOP carries both surfaces (paired SOP plus runbook). People audits the pair and the cadence; Operations runs the cadence.
- **Legal.** When an agent's work product is shared externally — generated copy, generated analysis, generated correspondence — Legal authors the disclosure scaffolding. People's doctrine cites Legal's templates rather than authoring them.

---

## §6 The five organising invariants — applied to agentic work

The five invariants of [`HOLISTIKA_ORGANISING_DOCTRINE.md`](HOLISTIKA_ORGANISING_DOCTRINE.md) §3 — simple, actionable, shareable, democratic, friendly — apply to agentic work the same way they apply to any other work at Holistika.

- **Simple.** An agent's job description fits in a paragraph. If it does not, the role is too large; split it.
- **Actionable.** Every governed step the agent runs traces back to an SOP step. If the agent is doing something that is not in an SOP, either the SOP is incomplete (People's job to fix) or the agent is out of bounds (Ethics' job to flag).
- **Shareable.** Knowledge-test results are part of the knowledge base. Agent shift logs are part of the knowledge base. The audit surface is operator-visible by default.
- **Democratic.** Any role owner can read the agent's doctrine, the Tech Lab landscape, and the Ethics anchor and understand what is expected. No specialised vocabulary is required to follow what governs an agent in our employ.
- **Friendly.** The doctrine is not adversarial. The agent is a collaborator. The cadence is the same cadence we apply to humans: regular knowledge-test, regular feedback, regular adjustment of the canonical when reality diverges from doctrine.

---

## §7 What People does NOT own in the agentic dimension

This section is load-bearing. People's doctrine is comprehensive on the **why**, **what**, and **cadence** of agentic work. It is silent on:

- **Specific tools, frameworks, libraries, infrastructure.** All of that lives at [`AGENTIC_FRAMEWORK_LANDSCAPE.md`](../../Envoy%20Tech%20Lab/canonicals/AGENTIC_FRAMEWORK_LANDSCAPE.md) (Tech Lab; System Owner stewardship). People does not endorse specific tools. People does not maintain the catalogue of which tool fits which use case.
- **Infrastructure operations** (deployment, monitoring, upgrades, version pinning). All of that lives at [`SOP-TECH_AGENTIC_INFRA_001.md`](../../Envoy%20Tech%20Lab/canonicals/SOP-TECH_AGENTIC_INFRA_001.md) (Tech Lab).
- **Ethical red lines.** That is the Ethics anchor at [`ETHICAL_AGENTIC_BOUNDARIES.md`](../Ethics/canonicals/ETHICAL_AGENTIC_BOUNDARIES.md). People's doctrine cites the anchor; Ethics owns the rules.

The split is per `D-IH-79-F` (round 3 operator directive: jargon-side to Tech Lab, clarity-side to People, red-lines to Ethics) and `D-IH-79-L` (Strand C P3a/P3b split). It is the operationalisation of the operator's "all jargon goes to Tech Lab" rule.

When a question arrives about an agent at Holistika, the routing is:

- *Why does the agent exist in this process?* → People (this canonical).
- *How is the agent expected to behave?* → People (this canonical + the SOP).
- *Which tool runs the agent?* → Tech Lab (the framework landscape).
- *What is the agent allowed to do?* → People + Ethics (this canonical + the anchor).
- *What is the agent forbidden to do?* → Ethics (the anchor).
- *How is the agent deployed and monitored?* → Tech Lab (the infra SOP).

---

## §8 Maintenance

This canonical is owned by People Operations Manager with co-stewardship from Ethics Advisor (Ethics anchor cross-link) and System Owner (Tech Lab landscape cross-link). Annual review minimum; any substantive revision requires a new `D-IH-79-*` decision row.

When the doctrine changes, the cross-area breakthrough propagation pattern fires per [`SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.md`](SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.md) (P4 deliverable). Tech Lab is pinged when the agentic doctrine row changes so the framework landscape stays in sync.

The anti-jargon drift gate ([`scripts/validate_design_pattern_registry.py --jargon-scan`](../../../../../../scripts/validate_design_pattern_registry.py)) runs on every commit that touches this canonical. Forbidden tokens are flagged at CI time.

---

## §9 Cross-references

- [`HOLISTIKA_ORGANISING_DOCTRINE.md`](HOLISTIKA_ORGANISING_DOCTRINE.md) — the People manifesto this doctrine extends.
- [`PEOPLE_DESIGN_PATTERN_LIBRARY.md`](PEOPLE_DESIGN_PATTERN_LIBRARY.md) — the cross-area pattern library; agentic work uses the same patterns.
- [`SOP-PEOPLE_AGENTIC_OPERATIONS_001.md`](SOP-PEOPLE_AGENTIC_OPERATIONS_001.md) — paired SOP for the knowledge-test cadence and escalation.
- [`ETHICAL_AGENTIC_BOUNDARIES.md`](../Ethics/canonicals/ETHICAL_AGENTIC_BOUNDARIES.md) — Ethics anchor; red lines.
- [`AGENTIC_FRAMEWORK_LANDSCAPE.md`](../../Envoy%20Tech%20Lab/canonicals/AGENTIC_FRAMEWORK_LANDSCAPE.md) — Tech Lab landscape; technical sub-disciplines; carries all framework jargon legitimately.
- [`SOP-TECH_AGENTIC_INFRA_001.md`](../../Envoy%20Tech%20Lab/canonicals/SOP-TECH_AGENTIC_INFRA_001.md) — Tech Lab infrastructure ops SOP.
- [`PRECEDENCE.md`](../Compliance/canonicals/PRECEDENCE.md) — registers this canonical.
- Cursor rule [`akos-people-discipline-of-disciplines.mdc`](../../../../../../.cursor/rules/akos-people-discipline-of-disciplines.mdc) — operationalises the recursive framing across cursor sessions.
