---
title: Holistika Stakeholder Lenses
language: en
intellectual_kind: people-canonical
access_level: 4
confidence_level: A1
source_taxonomy: holistika-internal-doctrine
register: internal
authors:
  - People Operations Manager
  - Founder
last_review: 2026-05-16
last_review_by: People Operations Manager
last_review_decision_id: D-IH-80-C
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-80-A
  - D-IH-80-C
status: active
ssot: true
companion_to:
  - HOLISTIKA_STAKEHOLDER_LENSES.addendum.md
  - HOLISTIKA_ORGANISING_DOCTRINE.md
  - HOLISTIKA_AGENTIC_DOCTRINE.md
---

# Holistika Stakeholder Lenses

This document is the canonical answer to one question: **what does Holistika look like, depending on who is looking at it?**

Holistika serves many stakeholders. Each stakeholder reads the company through their own lens — what matters to them, what they expect to see, what they would dismiss, what they would investigate, what they would value. The lenses below are a self-aware mapping of those views: how a Chief People Officer running People-as-a-discipline-of-disciplines experiences the company day-to-day; what the Tech Lab side of the System Owner role sees; what the Founder watches for; what an investor in due diligence cares about; what a cleared collaborator joining a contract reads first; what an apprentice or low-trust collaborator can and cannot see; what a regulator can audit.

The document is **internal-team** access by default (level 4). The addendum carries the Founder's personal reflection and agent-side narrative at level 5.

This is **not** marketing material. It is honest stakeholder mapping — a structural understanding of what Holistika offers, expects, and communicates to each role. Anyone authoring an external piece of communication for any of these stakeholders should read the relevant lens first and translate to the audience's external register from there.

---

## Lens 1 — Chief People Officer

The Chief People Officer is the role accountable for People as the discipline of disciplines. From this lens, the company is a small set of areas — Marketing, Research, Tech Lab, Operations, Legal, Finance, Ethics — each speaking its own dialect, with People holding the doctrine that the dialects share.

Day-to-day, the role is less about hiring and more about minting the patterns the other areas inherit. When a Marketing process and an Operations process and a Research process all reach for the same shape of register or the same shape of paired procedure, that shape lives in the People design pattern library. The other areas read the pattern and instantiate it inside their own canonical surfaces. Process singularity is the lever — every process declares its parent pattern, and the count of how many processes inherit each pattern is queryable.

The rhythms are clear. Quarterly review of the manifesto plus the design pattern library plus the agentic doctrine. Monthly review of the agentic operations cadence — knowledge-test sessions for any agent acting as a named role. Event-triggered review of any specific canonical that gains a substantive revision. Cross-area breakthrough propagation when a new pattern is minted: the consuming areas receive the announcement and decide whether and how to migrate.

The leverage points are the canonical CSV files and the SOPs paired with them. Editing a canonical CSV is a deliberate gate; the diff is reviewable; the implications are mechanical. The role's most important skill is judgement about when to mint a new pattern versus extend an existing one.

The hardest part is restraint. People is a discipline of disciplines, not a master of disciplines. Marketing speaks marketing; Tech Lab speaks tech; Finance speaks finance; the role's job is to keep the patterns clear and the dialects intact, not to flatten them into a single prose.

---

## Lens 2 — Chief Technology Officer (System Owner)

The Tech Lab side of the System Owner role serves the other areas as a sibling discipline. From this lens, the company is a software-shaped substrate where canonical CSVs, validators, mirror tables, and runbooks are the primary surface, and the SOPs are the human-readable companion.

Tech Lab carries jargon legitimately. Tools, frameworks, infrastructure, integration vendors — Tech Lab canonicals speak tech. The body of a Tech Lab document is allowed to name systems by their real names. The body of a People document, by contrast, stays plain — and the cross-area technical depth lives in the addendum companion.

The validators are the load-bearing piece. Every canonical surface is guarded by a script that catches drift mechanically — header changes that drift from the Pydantic model, foreign keys that don't resolve, jargon leaking into a People canonical body, manifest paths that don't exist on disk. The pre-commit profile bundles all of these so a single command tells the operator the state of the world.

The mirror tables are the second load-bearing piece. Every canonical CSV is projected into Postgres as a mirror table; consuming areas query the mirror, not the file. The mirror is read-only; the file is the source of truth. The forward-schema plane (table definitions) and the data plane (row inserts) are separate by design — schema changes go through migration files; row changes go through CSV edits and emit-then-apply cycles.

The Tech Lab role's responsibility is to keep this substrate quietly working. When everything is green, every other area's work is faster. When something drifts, the validator names the file, the line, and the failure — within seconds. The role's measure of success is how invisible Tech Lab feels to the other areas while still doing all the load-bearing work.

---

## Lens 3 — Chief Executive Officer / Founder

The Founder reads the company through one structural question: **does Holistika continue if I step away for six months?** Everything important must be encoded in canonicals, validators, and procedures — not in the Founder's head, not in unwritten convention, not in tribal memory.

The bus-factor mitigation is mechanical. Decisions are minted in the decision register with full rationale; initiatives carry workspace mirror folders with charters, decision logs, risk registers, and closure records; processes are listed with their parents declared; patterns are minted once and inherited by every consuming area. A new collaborator at the right access level can read the doctrine and pick up where the work was paused.

Investability is the related concern. The same artefacts that mitigate bus-factor risk also signal governance maturity to investors and partners. A diligence reviewer can browse the decision register, the initiative register, the canonical CSVs, the dependency map, the changelog, the planning workspace — and understand how the company makes decisions, executes initiatives, and closes them. The artefacts are diff-able; reviews leave a trail; closures are recorded.

The Founder's most important daily ritual is to operate as a co-pilot during initiative execution rather than a single-thread executor. When the agent asks for a doctrine call, the Founder answers; when the agent surfaces a candidate decision, the Founder ratifies or redirects; when the work hits an inline question gate, the Founder picks among ranked options. The pace of the company is set by how quickly this loop closes.

The hardest part is letting the doctrine speak when the Founder's instinct disagrees. The discipline is to surface the disagreement in the decision register with rationale, not to override silently. Override-by-edit corrupts the audit trail; override-by-decision-row preserves it.

---

## Lens 4 — Investor

The Investor reads Holistika as a diligence target. From this lens, the company is a sequence of legibility tests: can I, as an outsider, browse this company's substrate and form a judgement about its governance maturity, its team's craft, its defensibility, its operational risk?

The first test is the canonical surface. Initiative register, decision register, process list, organisational baseline, design pattern library — all in version control, all with declared schemas, all with frontmatter that names access levels and review dates. The Investor can clone the workspace and grep for what they want.

The second test is the closure record. Every closed initiative carries a pause record — mechanical evidence (files created, validators that ran, tests added), documentary evidence (decisions encoded, cross-canonical link integrity, changelog entries), an operator approval checklist. The closure trail is a substitute for war-room interviews — the Investor reads what closed, when, with what trade-offs, with what carry-overs.

The third test is the people doctrine itself. Holistika operates as a people-company-using-tech rather than a tech-company-using-people. The doctrine names this explicitly. People Operations Manager, Compliance Officer, Brand Manager, Holistik Researcher — each role is encoded in the organisational baseline with a clear purpose and clear acceptance criteria. The roles do not depend on specific individuals; the discipline does.

The fourth test is defensibility against intellectual property leak. The methodology is encoded in canonicals, but it is also bounded by access levels. Collaborators see what their level reveals; the methodology's most sensitive parts stay at level 5 or higher. A talent-poaching event — the recurring fear in research-intensive companies — does not exfiltrate the methodology because the methodology is structural, not procedural.

The Investor's typical conclusion after a diligence pass: this is governance discipline that compounds. Each initiative leaves the substrate stronger; each pattern minted compounds the next initiative's leverage; each canonical encoded reduces the cost of every future related decision.

---

## Lens 5 — Cleared collaborator (Holistik Researcher, named Operator, internal advisor)

A cleared collaborator joining a Holistika engagement reads the company at access level 4. From this lens, the experience is the opposite of most consulting onboarding — the doctrine is given to you up front; you are expected to internalise it; the engagement work is then framed by it.

The collaborator's first day is reading. The People manifesto explains why the company exists and what it operates on. The design pattern library explains how the company thinks about cross-area work. The agentic doctrine explains how human and named-role agent collaborators co-exist. The role-specific SOPs explain how the work is done in their area. By the end of the first day, the collaborator has the same mental model as the Founder.

The second day is mechanical orientation. The collaborator learns where the canonical CSVs live, how to read frontmatter, how to find the decision register entry for any architectural call, how to read the dependency map between initiatives, how to navigate the workspace planning folders. The validators are introduced — the collaborator runs them and watches them pass.

The third day is engagement-specific work. The collaborator is given access to the engagement's canonical brief, the counterparty understanding document, the ranked option set under consideration. The work begins.

What the collaborator is **not** given: the Founder's personal reflection at level 5, the most sensitive intellectual property fragments at level 5 or higher, certain raw discovery transcripts from past engagements. The boundary is explicit; the collaborator never wonders what they are missing because the access-level lattice is documented.

The experience is honest. The collaborator knows what they can see; knows what they cannot; knows why; knows the cadence at which their access might expand. The trust posture is earned, not assumed — and the substrate makes the earning legible.

---

## Lens 6 — Apprentice or external occasional collaborator

An apprentice or external occasional collaborator reads Holistika at access level 1 to 3. From this lens, the company shows a public surface (level 1 to 2), a partner-facing surface (level 2 to 3), and a curated mentoring surface for the apprentice's specific learning path. The internal doctrine, the decision register, the methodology depth — all stay invisible.

The apprentice experience is bounded by design. The bounding is not gatekeeping; it is protection — for the apprentice, who should not be loaded with doctrinal context they have not earned the time to internalise; and for the company, whose intellectual property substrate is the long-term moat.

What the apprentice does see: a clear curriculum aligned with the discipline they are apprenticing into. A specific role they are growing toward (Holistik Researcher, Brand Manager, Operator). A specific mentor who is the apprentice's named point of contact. A specific cadence of check-ins and exercises. The apprentice is never confused about what they are doing or why.

The external occasional collaborator — a one-off advisor, a workshop facilitator, a vendor performing a discrete service — sees the engagement scope and nothing else. The boundary is engagement-scoped, not role-scoped. When the engagement closes, access closes.

The lens is also the recruiter's lens for early-career talent. Holistika is honest about apprenticeship: it is a mutual investment. The apprentice contributes attention and follow-through; the company contributes mentorship and career compounding. Both sides are explicit about what they offer and what they expect.

---

## Lens 7 — Regulator

A regulator — financial, data-protection, sectoral — reads Holistika as an audit target. From this lens, the question is whether the company can produce evidence on demand: who decided what, when, on what basis, with what outcome, with what opportunity for revision.

The answer is yes, mechanically. The decision register names every architectural call by stable ID, with date, owner, summary, and rationale. The initiative register names every initiative by stable ID, with phase trail, closure record, linked decisions. The process list names every executable process by stable ID, with role owner, cadence, paired procedure, and parent pattern. The canonical CSVs are diff-able through git history; every change is attributable.

The regulator does not need a war-room interview. The regulator can clone the workspace at the relevant historical point, run the validators that were live at that point, browse the decision register entries that pre-date the audit horizon, and form a structured view. The audit cost is low because the substrate is structural, not anecdotal.

Sector-specific evidence is also queryable. Data classifications are encoded in frontmatter access levels. Source quality is encoded in confidence levels. Source taxonomy is encoded as a small enum on every artefact. A regulator asking "what data did you act on, and how reliable was it?" can answer their own question by query.

The relationship with the regulator is also a registered intelligence-collection contract. The Holistik Researcher role owns the contract; the cadence is set; the structured discovery questionnaire and the engagement design are written down. The regulator is a stakeholder, not a surprise.

---

## Looking ahead — Madeira and the Agent-in-Charge horizon

The current state of the doctrine assumes most named-role positions are held by humans. The forward state assumes some named-role positions can be held by agents acting as Agent-in-Charge — a defined role-class internal to People that operates as the role owner for specific scoped work.

The Madeira elevation is the named programme for taking this from designed posture to operational reality. Madeira is the Holistika operations centre — the integrated intelligence-and-execution surface where each area's daily work runs. Today, Madeira is the operator's own workspace plus a small set of agent-collaborators acting under direct co-pilot instruction. Tomorrow, Madeira hosts named-role agent positions — Agent-in-Charge of specific Operations work, Agent-in-Charge of specific Marketing work — that meet the same governance bar as human role-owners.

The doctrine prepares for this without depending on it. The agentic doctrine explains why Agent-in-Charge exists, what guardrails apply, what knowledge-tests gate the position, what the escalation path looks like when an agent's judgement is in tension with operator instinct. The pattern library has slots reserved for the patterns this elevation will need. The decision register will mint the architectural calls when the time comes.

The horizon does not change the lenses above. The Chief People Officer still mints patterns. The Chief Technology Officer still owns the substrate. The Founder still operates as co-pilot. The Investor still reads governance maturity. The cleared collaborator still onboards into the doctrine. The apprentice still grows on a curriculum. The regulator still audits structurally. What changes is the cast of role-owners, not the architecture they operate inside.

---

## Maintenance

This document is reviewed annually by the People Operations Manager with the Founder. Event-triggered review fires when major company state changes — funding round close, first regulated client engagement, executive role activation, regulatory submission, a substantive Agent-in-Charge promotion. Revisions are recorded in the decision register; the addendum companion is reviewed independently per its own cadence.

When stakeholder definitions change (a new stakeholder class becomes load-bearing; an existing class deprecates), the change is encoded as a new lens section or a rewritten one with a new ratifying decision row.

The companion addendum at access level 5 carries the Founder's personal reflection and the agent-side narrative on the moment this document was authored. Neither is required reading for any of the stakeholders above; both are available to internal-cleared readers as the deeper layer.

---

## Cross-references

- [`HOLISTIKA_ORGANISING_DOCTRINE.md`](HOLISTIKA_ORGANISING_DOCTRINE.md) — the People manifesto that frames why these lenses exist.
- [`HOLISTIKA_AGENTIC_DOCTRINE.md`](HOLISTIKA_AGENTIC_DOCTRINE.md) — the doctrine for human + named-role agent co-existence; informs lens 7 (looking ahead).
- [`PEOPLE_DESIGN_PATTERN_LIBRARY.md`](PEOPLE_DESIGN_PATTERN_LIBRARY.md) — the design pattern library; this file uses `pattern_sop_addendum_split` (body + addendum companion).
- [`HOLISTIKA_STAKEHOLDER_LENSES.addendum.md`](HOLISTIKA_STAKEHOLDER_LENSES.addendum.md) — level 5 companion carrying Founder reflection and agent-side narrative.
- [`PRECEDENCE.md`](../Compliance/canonicals/PRECEDENCE.md) — registers this canonical in the asset list.
