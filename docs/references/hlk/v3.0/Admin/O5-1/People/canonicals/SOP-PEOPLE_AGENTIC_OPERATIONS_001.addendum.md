---
title: SOP — People Agentic Operations — Addendum (System Owner + Auditor depth)
language: en
intellectual_kind: people-canonical-sop-addendum
sop_id: SOP-PEOPLE_AGENTIC_OPERATIONS_001
access_level: 5
confidence_level: A1
source_taxonomy: holistika-internal-sop
authors:
  - System Owner
  - People Operations Manager
last_review: 2026-05-16
last_review_by: People Operations Manager
last_review_decision_id: D-IH-80-D
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-79-A
  - D-IH-79-F
  - D-IH-79-L
  - D-IH-80-D
status: active
register: internal
parent_sop: SOP-PEOPLE_AGENTIC_OPERATIONS_001.md
companion_to:
  - SOP-PEOPLE_AGENTIC_OPERATIONS_001.md
  - HOLISTIKA_AGENTIC_DOCTRINE.md
  - SOP-TECH_AGENTIC_INFRA_001.md
  - AGENTIC_FRAMEWORK_LANDSCAPE.md
ssot: true
---

# SOP — People Agentic Operations — Addendum

> Access level 5. This addendum carries the System-Owner-facing and auditor-facing depth that does not belong in the executor's reading path of [`SOP-PEOPLE_AGENTIC_OPERATIONS_001.md`](SOP-PEOPLE_AGENTIC_OPERATIONS_001.md). Authored at I80 P4 (D-IH-80-D Option B retrofit pilot) as the second instantiation of `pattern_sop_addendum_split` after the stakeholder lenses pair at I80 P2.
>
> The body's role: enable People Operations Manager (or any AIC role-owner) to run the knowledge-test cadence end-to-end. The addendum's role: explain the cross-area architecture the cadence sits inside, the operator-side framing decisions that shaped it, and the audit-trail dimensions that auditors / System Owner / Ethics Advisor need but the executor does not.

---

## A. Tech Lab posture — why the harness is zero-framework

The runbook [`scripts/peopl_agentic_knowledge_test.py`](../../../../../../scripts/peopl_agentic_knowledge_test.py) carries no LangChain, LlamaIndex, OpenClaw, CrewAI, Ollama, VercelAI, or Groq dependency. The harness reads canonical Markdown as plain text, presents questions as plain prompts, and writes results as plain Markdown.

The rationale lives at three levels:

**Level 1 — operator clarity-side mandate.** Per `D-IH-79-F` (round 3 inline-ratify gate, 2026-05-15) the operator framed the People-side as the *clarity* anchor of the three-part stratified governance split: People doctrine + Tech Lab landscape + Ethics anchor. Tooling on the People surface should not introduce framework jargon that obscures the doctrine the cadence enforces. Zero-framework Python reads as plain Python; LangChain-wrapped Python reads as LangChain Python. The choice is doctrinal, not just technical.

**Level 2 — methodology-version agnosticism.** The frameworks tracked in [`AGENTIC_FRAMEWORK_LANDSCAPE.md`](../../Envoy%20Tech%20Lab/canonicals/AGENTIC_FRAMEWORK_LANDSCAPE.md) §1 evolve quarterly (per `SOP-TECH_AGENTIC_INFRA_001.md` §3 quarterly audit cadence). If the harness depended on, say, LangChain v0.3 prompt templates, every framework-major-version change at Tech Lab would force a People-side rev. Decoupling the harness from the framework layer means People's cadence is unaffected by Tech Lab's framework lifecycle.

**Level 3 — portability across agent infrastructure changes.** When Tech Lab swaps the underlying inference layer (e.g., from local Ollama to remote Groq, or from OpenAI to Claude), the People-side knowledge-test cadence does not change. The harness presents prompts and reads completions; the inference layer is abstracted. This is the structural realisation of the People-as-discipline-of-disciplines doctrine: People's process must outlive Tech Lab's specific tooling choices.

Practical consequence for System Owner: when proposing a Tech Lab framework upgrade (per `SOP-TECH_AGENTIC_INFRA_001.md` §2 framework major-version ratification), confirm the harness still works against the new layer with the standard test bank. If it does, the upgrade is safe. If it does not, the upgrade is blocked until the harness's plain-text protocol is preserved (or until the operator ratifies a People-side rev to follow the Tech Lab change).

## B. Test bank construction — auditor-facing detail

The body's §2 names "five to ten question-answer pairs" without specifying construction. Auditor and System Owner reference:

**Source attribution.** Every question's answer must be derivable from a specific canonical line range. The test bank file (per agent + per scope) carries a tab-separated triple per row: question text + canonical answer + canonical citation (`path/to/file.md L12-15`). At scoring time, the operator can confirm Pass / Fail / Drift by clicking through to the cited range.

**Question-class balance.** Across the 5-10 questions in a session, three classes should be represented:

- *Definitional* (3-4 questions) — what does X mean per the canonical (e.g., "what is an Agent-in-Charge per `HOLISTIKA_AGENTIC_DOCTRINE.md`?")
- *Procedural* (2-3 questions) — what does the canonical require under condition Y (e.g., "when an agent's escalation crosses an Ethics red line, what is the routing per `ETHICAL_AGENTIC_BOUNDARIES.md` §5?")
- *Boundary* (1-2 questions) — what is *not* covered by the canonical, or where does scope end (e.g., "is Tech Lab framework selection in scope of this SOP?")

The mix is what surfaces drift: definitional drift (canonical wording shifted), procedural drift (the executable steps no longer match the canonical), boundary drift (scope creep — the canonical has expanded without People's manifesto noticing).

**Drift-vs-Fail discrimination.** The body's §4 names Drift as "the agent's answer is plausible but the canonical itself is ambiguous on the point." The deeper auditor-facing nuance: a single Drift mark per session is normal evolution (the canonical is being lived against and the lived reality reveals an edge case the canonical did not anticipate). Two or more Drift marks per session is a structural signal: either the canonical is significantly stale, or the test bank is over-targeting an ambiguous corner. People Operations Manager's `--reconcile` quarterly run (per body §6) catches the second pattern and triggers a test-bank rev rather than a canonical rev.

**Methodology version stamp.** Each test bank file carries a `methodology_version_at_authoring:` frontmatter field. When the test bank is run against an agent and the canonical's `methodology_version_at_review:` differs from the test bank's authoring version, the harness flags this in the result file. Auditors use this to discriminate between "canonical changed; test bank updated; re-run gives a clean Pass" (healthy) and "canonical changed; test bank not updated; re-run gives stale Fails" (process failure on the People side, not the agent).

## C. Cross-canonical drift signals — System Owner audit dimensions

When a Drift mark fires, the cross-canonical implication depends on which canonical was tested:

| Canonical drifted | Likely affected siblings | Cross-area pingback required? |
|:---|:---|:---|
| `HOLISTIKA_AGENTIC_DOCTRINE.md` | `AGENTIC_FRAMEWORK_LANDSCAPE.md`, `ETHICAL_AGENTIC_BOUNDARIES.md` | Yes — fire `SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001` Tech Lab pingback (§4). |
| `HOLISTIKA_ORGANISING_DOCTRINE.md` | All consuming-area canonicals | Yes — fire breakthrough propagation to all areas. |
| `ETHICAL_AGENTIC_BOUNDARIES.md` | `HOLISTIKA_AGENTIC_DOCTRINE.md`, `ETHICAL_AUTOMATION_POSTURE.md` | Yes — Ethics Advisor reviews; potential triangle re-alignment. |
| `PEOPLE_DESIGN_PATTERN_LIBRARY.md` | `PEOPLE_DESIGN_PATTERN_REGISTRY.csv` | Maybe — depends whether the registry row needs updating to match the narrative. |
| `SOP-PEOPLE_AGENTIC_OPERATIONS_001.md` (this SOP) | `process_list.csv tbi_peopl_dtp_agentic_ops_mtnce_001` | Yes — process_list row's last_review_decision_id updates atomically. |

System Owner's quarterly audit (per `SOP-TECH_AGENTIC_INFRA_001.md` §3) cross-references each Drift mark in the People knowledge-test reports against this table to confirm the appropriate sibling pingbacks fired. Misses are logged as audit findings with a one-quarter remediation window.

## D. Operator framing decisions encoded in this SOP

Three operator-side ratifications the body does not narrate but the addendum records for audit posterity:

**D-IH-79-F (round 3 inline-ratify, 2026-05-15) — three-part stratified governance split.** The agentic governance question was framed as a single SOP that would carry doctrine + framework + ethics in one file. Operator pivoted at round 3: doctrine to People (clarity-side), framework to Tech Lab (jargon-side), red-lines to Ethics (per-action). This SOP is the People-side anchor of that split. If a future operator considers re-merging the three, the audit trail starts here.

**D-IH-79-L (round 4 inline-ratify, 2026-05-15) — Strand C P3a/P3b split.** Operator confirmed that the People-side SOP and the Tech Lab-side SOP are siblings, not parent-child. Neither supersedes the other; both must stay coherent. The cross-area breakthrough propagation SOP (`SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001`) is the structural defence. If a future operator considers collapsing the sibling structure, this addendum names the dependency.

**D-IH-79-A round 1 inline-ratify (2026-05-13) — charter-satisfies-gate.** Operator ratified the I79 charter at round 1 inline-ratify rather than as a P0 pause record. The agentic operations SOP (this file) was authored under that posture: charter → directly to execution → inline-ratify rounds at every gate. The audit trail starts at the charter; there is no separate plan-vs-execution boundary.

These three decisions together explain why this SOP is structured the way it is. The body answers "how do I run the cadence"; this section answers "why is the cadence structured this way".

## E. Cross-references and provenance

- Body file: [`SOP-PEOPLE_AGENTIC_OPERATIONS_001.md`](SOP-PEOPLE_AGENTIC_OPERATIONS_001.md).
- Sibling Tech Lab SOP: [`SOP-TECH_AGENTIC_INFRA_001.md`](../../Envoy%20Tech%20Lab/canonicals/SOP-TECH_AGENTIC_INFRA_001.md) — covers infrastructure operations (framework lifecycle + KB pipeline + MCP postures).
- Tech Lab landscape: [`AGENTIC_FRAMEWORK_LANDSCAPE.md`](../../Envoy%20Tech%20Lab/canonicals/AGENTIC_FRAMEWORK_LANDSCAPE.md) — framework rows + KB infrastructure dimensions + integration postures.
- Cross-area propagation SOP: [`SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.md`](SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.md) — Tech Lab pingback when this SOP's parent doctrine revises.
- People doctrine: [`HOLISTIKA_AGENTIC_DOCTRINE.md`](HOLISTIKA_AGENTIC_DOCTRINE.md) — the doctrine the body operationalises.
- Ethics anchor: [`ETHICAL_AGENTIC_BOUNDARIES.md`](../Ethics/canonicals/ETHICAL_AGENTIC_BOUNDARIES.md) — red-line escalation target.
- Pattern provenance: [`PEOPLE_DESIGN_PATTERN_LIBRARY.md #pattern-sop-addendum-split`](PEOPLE_DESIGN_PATTERN_LIBRARY.md#pattern-sop-addendum-split) — the pattern this addendum instantiates.
- I80 retrofit charter: [`docs/wip/planning/80-i79-lessons-learned/master-roadmap.md`](../../../../wip/planning/80-i79-lessons-learned/master-roadmap.md) §"P4 — I79 SOP retrofit pilot".
