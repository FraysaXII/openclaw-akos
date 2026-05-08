---
language: en
status: active
role_owner: Founder
area: Marketing
entity: Holistika Research SL
program_id: shared
topic_ids:
  - topic_brand_voice
  - topic_baseline_reality
artifact_role: canonical
intellectual_kind: brand_asset
authority: Founder
last_review: 2026-05-08
ssot: true
access_level: 5
---

# BRAND_BASELINE_REALITY_MATRIX — Per-audience reading + dual register

> **Status — Active (Initiative 66 P1; founder-authored 2026-05-08).** Codifies decision [D-IH-66-M](../../../../wip/planning/66-brand-vision-ops-sweep/decision-log.md#d-ih-66-m) — dual-register design separating internal CORPINT vocabulary (HUMINT FM 2-22.3 sourced; restricted to operator + cleared collaborators) from external translated capability messaging (the canonical register for all customer-, investor-, advisor-, ENISA-, partner-, recruiter-facing prose). Anchors the four HUMINT-derived SOPs in I66 P3, the deck `.objections.md` + `.counterparty-brief.md` companions in I66 P6, the agent guardrails enforced by [`akos-brand-baseline-reality.mdc`](../../../../../../../.cursor/rules/akos-brand-baseline-reality.mdc) (created I66 P2), and the drift gate `validate_brand_baseline_reality_drift.py` (P2).
>
> **Access level: 5.** Operator + cleared collaborators only. Agents reading this file are accountable to the dual-register contract: produced prose for external surfaces may only cite the external register column. The internal register column exists for operator-private SOPs + intelligence reports + per-engagement counterparty briefs.
>
> **Source citation.** Internal-register vocabulary is grounded in the US Army HUMINT Collector Operations Field Manual FM 2-22.3 (Sept 2006, public release, Department of the Army). The framework is adapted to corporate intelligence contexts, not literally applied. Citation here is for tradecraft methodology, not for source-handling, interrogation, or any application that exceeds corporate / commercial scope.

## 1. Why dual-register

Operator-stated framing (2026-05-08): three audience-truths exist simultaneously:

1. **Collaborators are told** "we are PMs, researchers that get to know what we need to know to do better."
2. **Investors know** "we'll use whatever research necessary to get to a profitable position and have the operational force to do that."
3. **Customers come thinking** "we are professional, like a big company acting on behalf of SMEs."

Three audiences, three reading lenses, one company. The internal CORPINT discipline (structured intelligence collection, source protection, audience-baselined communication, intel sharing rules) is real and operational. The external CORPINT-research register translates the same discipline into language each audience reads as **professional research**, **structured methodology**, **evidence-based strategy**.

Single-register approach (only HUMINT vocabulary internally + externally) would force collaborators + customers to use HUMINT vocabulary in their own communication — risky brand collapse if leaked + uncomfortable framing for customers who never asked for an intelligence operation.

Pure external translation (no internal HUMINT grounding) would lose the operator's CORPINT discipline + decision rigor in agent prompts + SOP authoring. Agents that don't know the underlying tradecraft can't reason about edge cases.

Dual-register preserves rigor internally + professional-research voice externally + a translation table that every agent + every operator-private artifact must respect.

## 2. The matrix

Eight columns × seven external audiences + one internal audience.

Columns (per audience-x-topic row):

| Column | Description |
|:---|:---|
| `assumed-normal` | What the audience believes is the default state of affairs in their world. The thing they don't know they don't know. |
| `bridge-frame` | The frame Holistika uses to bring the audience from their normal to a state where they can act. The "translation contract." |
| `objection-patterns` | The 2-4 most likely objections this audience raises in the first three meetings. Internal vocabulary for operator preparation; not external. |
| `decision-criteria` | What this audience needs to be true before they say yes / sign / fund / refer. |
| `evidence-types-trusted` | What kind of evidence carries weight with this audience: numbers, anecdotes, references, demos, papers, dossiers, etc. |
| `first-i-don't-understand-trigger` | The first phrase from a Holistika representative that causes this audience to disengage. The token that breaks the bridge. |
| `internal-vocabulary-(restricted)` | HUMINT-grounded vocabulary used **only** in operator-private artifacts. **Forbidden** on external surfaces. |
| `external-vocabulary-(canonical)` | The translated vocabulary used on all external surfaces. **Required** when prose addresses this audience. |

### J-OP — Operator (founder + future BrandOps Lead)

> Internal audience. The only audience reading the internal column directly. All other audiences read only the external column.

| Column | Value |
|:---|:---|
| assumed-normal | AKOS canon as canonical truth; cursor agents producing prose that respects canon; drift gates green. |
| bridge-frame | Status sheet: verdicts dated; numbers cited; deltas surfaced; what wants you right now. |
| objection-patterns | "Is this self-checkpoint discipline real?"; "Are agents reading the matrix or just citing it?"; "Is this fixture or live?" |
| decision-criteria | All gates green; every commit traces back to a decision; every artifact has a frontmatter contract. |
| evidence-types-trusted | Output of `validate_*.py`; freshness ribbon timestamps; `governance.repo_health_view` aggregates. |
| first-i-don't-understand-trigger | A number presented without a date or a source. |
| internal-vocabulary-(restricted) | Counterparty assessment, baseline reality, elicitation, source reliability grading, intelligence report, internal collection, indicator, observable, requirement, lead, contact, asset, cover. |
| external-vocabulary-(canonical) | This row is operator-internal; external register N/A. |

### J-IN — Investor (seed / pre-seed; ENISA / public funds; angel)

| Column | Value |
|:---|:---|
| assumed-normal | Most "AI" companies are wrappers; most "consulting" firms are slide-deck shops; most founders overstate capacity; most early-stage tech in EU is academic without traction. |
| bridge-frame | Lab-to-channel pipeline (research validates → strategy guides → execution scales) + anonymized methodology track record (50K → 7 venues, 1.7M raised) + product stack (MADEIRA + KiRBe + ENVOY) shipping internally. Loud-and-confident framing for capital efficiency, not for hype. |
| objection-patterns | "Is this another consulting shop pretending to be a SaaS?"; "Where's the moat?"; "What's the burn?"; "Why now?"; "Why this team?"; "What happens if you lose the founder?" |
| decision-criteria | Founder credibility + market thesis + traction + moat + capital efficiency + ENISA-fit (technological component, scalability, employment generation). |
| evidence-types-trusted | Anonymized methodology track record (with NDA-references available); product-stack technical depth diagrams; founder bio long-form; investor deck slide 9 ("Why Holistika now"); dossier numbers aligned with public manifesto. |
| first-i-don't-understand-trigger | A claim without a number; OR a number without a date; OR a methodology without a track record. |
| internal-vocabulary-(restricted) | Approach: rapport (warm peer); sub-source primacy; counterparty motivation; cover-for-status; counterparty objection-pattern. |
| external-vocabulary-(canonical) | "We are a research-and-strategy firm with an internal technology lab. Our track record is X. Our products are Y. Our differentiation is the flywheel." Use "investor", "fund", "advisor", not "counterparty"; "investor due diligence", not "elicitation"; "track record verifiable on NDA", not "asset substantiation". |

### J-CU — Customer-SME (entrepreneur with EU-funding ambitions; mid-market operator)

| Column | Value |
|:---|:---|
| assumed-normal | Consulting firms are expensive PowerPoint-as-a-service; agencies overpromise; SaaS tools require IT teams I don't have; my data is my problem; nobody really protects confidentiality. |
| bridge-frame | "Professional like a big company acting on behalf of SMEs." Outcome-clarity, price-predictability, time-to-value. |
| objection-patterns | "How much will this actually cost?"; "How long will this take?"; "Will you disappear after the first invoice?"; "Will you understand my industry?"; "Is my data safe?"; "What's the difference between you and Bain / a generic agency?" |
| decision-criteria | Outcomes clarity (what will I have at the end?); price predictability (3-tier matrix; SME tier ≤ €50K total); confidentiality (NDA + DPA on day 1); team competence (founder bio + track record); time-to-value (≤4 weeks for first deliverable). |
| evidence-types-trusted | SERVICE_OFFERING_CATALOG-derived /services page (6 services × 3 arms × 3 tiers); founder bio short-form; engagement playbook visible in pre-engagement materials; one anonymized testimonial from a similar-sized engagement. |
| first-i-don't-understand-trigger | An English-only response when the conversation started in Spanish; OR a price quote with "+" / "to be determined" / "depending on scope". |
| internal-vocabulary-(restricted) | Counterparty industry baseline; counterparty financial pressure window; objection-cluster #1 (cost); objection-cluster #2 (control); objection-cluster #3 (industry-fit); cooperation likelihood model; lead-source quality grade. |
| external-vocabulary-(canonical) | "Client", "company", "engagement", "discovery interview", "proposal", "scope of work", "engagement outcome". Use "industry context briefing", not "counterparty industry baseline"; "discovery agenda", not "elicitation plan"; "engagement summary", not "intelligence report". |

### J-PT — Strategic partner

| Column | Value |
|:---|:---|
| assumed-normal | Most "partnership" approaches are competitor-disguised-as-partner; joint-go-to-market is a common slide that rarely produces revenue; my time on partnership exploration is expensive. |
| bridge-frame | Service-catalog clarity (6 × 3 × 3) lets a partner map their offerings into the matrix in 5 minutes. Partner deck + counterparty-brief in P6 ensures we know their ecosystem before the call. |
| objection-patterns | "Is this competitor-disguised-as-partner?"; "What do I get out of this?"; "Can your team execute reliably?"; "Will I lose customers to you?"; "Who owns the customer relationship?"; "What's the joint-rev split?" |
| decision-criteria | Clear scope of complementary services (no overlap); operational maturity (reliable delivery); joint-go-to-market rhythm (cadence + materials); customer-ownership clarity. |
| evidence-types-trusted | SERVICE_OFFERING_CATALOG public form (`/services` 6×3×3 matrix); `/tech-lab` lab-as-credibility positioning; partner deck (4 slides); two existing partner references; public-screenshot of `/governance` panel signaling operational maturity. |
| first-i-don't-understand-trigger | "We can do everything"; OR "no, we don't compete with anyone"; OR a missing/vague answer to "who owns the customer". |
| internal-vocabulary-(restricted) | Cooperation likelihood baseline; partner-side decision-tree map; joint-go-to-market objection-pattern; partnership-economics elicitation. |
| external-vocabulary-(canonical) | "Partner", "alliance", "joint engagement", "co-delivery", "complementary scope". Use "partner discovery interview", not "partner elicitation"; "alliance brief", not "partner intelligence brief"; "joint scope", not "joint elicitation matrix". |

### J-ENISA — ENISA application reviewer (public-funds technical evaluation panel)

| Column | Value |
|:---|:---|
| assumed-normal | Most ENISA applicants are research-grant-shaped academia or product-pitch-shaped startups without operational depth; technological-component scoring requires real software, not slide-claims; capital-efficiency claims require numbers. |
| bridge-frame | Spain-flagged corporate posture (Holistika Research SL, Madrid + Madeira presence) + lab-channel pipeline as the technological-component story + product-stack technical depth (MADEIRA + KiRBe + ENVOY architecture diagrams) + anonymized founder track record (capital efficiency proof). |
| objection-patterns | "Is this enough technological substance for a tech-fund vs a consulting-fund?"; "What's the IP defensibility?"; "How does Spain benefit from the funding?"; "What's the employment generation?"; "What's the scalability path?"; "Where's the differentiated technology?" |
| decision-criteria | Technological component (AI / agentic / data architecture); scalability (lab → channel pipeline + product stack); employment (3 sub-mark Lead roles + ~20 part-time collaborators planned); market traction (anonymized methodology track-record); capital efficiency (numbers from track record). |
| evidence-types-trusted | ARCHITECTURE.md updated with Branded House + lab-channel pipeline diagram; product-stack technical depth (MADEIRA Agent 5-agent coordination; KiRBe BM25 + vector RRF; ENVOY channel adapter); founder track-record (anonymized); ENISA 8-slide deck specifically structured per ENISA evaluation criteria; trademark filings as IP-protection signal. |
| first-i-don't-understand-trigger | A claim of "AI-powered" without architecture; OR a market thesis without local-market grounding; OR a team description without specific Spain employment plans. |
| internal-vocabulary-(restricted) | Funding-panel cooperation likelihood; counterparty technical-grading axis; ENISA-baseline-reality elicitation pattern; reviewer-side objection-cluster #1 (technical depth), #2 (capital efficiency), #3 (Spain benefit). |
| external-vocabulary-(canonical) | "Reviewer", "evaluation panel", "applicant", "technological component", "scalability path", "capital-efficiency evidence". Use "applicant briefing", not "panel-counterparty brief"; "technical-component documentation", not "asset technical-grading"; "evaluation criteria mapping", not "reviewer elicitation matrix". |

### J-AD — Advisor (strategic / legal / technical / financial)

| Column | Value |
|:---|:---|
| assumed-normal | Most early-stage teams are disorganized; advice rarely gets implemented; my time is expensive; if I cannot read a status sheet in 5 minutes the team is not ready for me; most "we're so excited to have you" intros are noise. |
| bridge-frame | Brevity over depth on first read. ADVOPS canonicals govern engagement (per `akos-adviser-engagement.mdc`). Filed-instruments register completeness signals professional discipline. |
| objection-patterns | "Is this signal-rich or signal-noise?"; "What do you actually need from me?"; "How will my advice be acted on?"; "Am I being asked because I'm useful or because I'm a name?" |
| decision-criteria | Clear ask + clear scope + clear closure rhythm + responsiveness signal. |
| evidence-types-trusted | Advisor 4-slide deck (concise); ADVOPS register completeness; engagement playbook readability; the existence of a structured operator inbox signals discipline. |
| first-i-don't-understand-trigger | A general "we'd love your guidance"; OR a 12-slide investor deck delivered to an advisor (wrong audience). |
| internal-vocabulary-(restricted) | Adviser-side cooperation likelihood; advisor-domain-fit grade; advisor-availability cycle; ADVOPS engagement-instrument elicitation. |
| external-vocabulary-(canonical) | "Advisor", "advisory engagement", "advisor brief", "engagement scope", "closure cadence". Use "advisor briefing", not "advisor counterparty brief"; "open questions register", not "advisor elicitation register" (this is the existing ADVOPS canonical). |

### J-RC — Recruiter / future hire / part-time collaborator

| Column | Value |
|:---|:---|
| assumed-normal | Most "exciting startup" pitches are noise; equity is usually worth zero; founder-led companies often have no real org structure; my time is expensive; my reputation depends on this hire. |
| bridge-frame | Clear sub-mark Lead structure (Holistika R&S + Think Big + HLK Tech Lab) signals real organization. Operational discipline visible (canonicals, drift gates, cursor rules) signals serious engineering culture. The existence of `BRAND_DIGEST` for new agents is itself a signal that the company runs structured onboarding. |
| objection-patterns | "Will I have agency or will I be a copy-paste agent?"; "Is the equity / compensation real?"; "What's the runway?"; "Who do I report to?"; "What does month 1, month 3, month 6 look like?"; "Will my work be visible?" |
| decision-criteria | Compensation + scope clarity; team structure visible; canon-onboarding rigor; first-3-months scoped concretely. |
| evidence-types-trusted | Recruiter 6-slide deck; ONBOARDING_KIT visible in repo; `governance` panel public-screenshot signal; founder bio short-form; SOP-AGENT_BRAND_DIGEST_001 (structured agent + human onboarding). |
| first-i-don't-understand-trigger | "We're flexible on compensation" without a number; OR a generic "we ship fast" without an example. |
| internal-vocabulary-(restricted) | Talent-funnel cooperation likelihood; candidate-domain-fit grade; reputation-sensitivity decision-tree. |
| external-vocabulary-(canonical) | "Hire", "candidate", "team", "role", "scope", "month-1 outcomes", "compensation band". Use "candidate brief", not "candidate counterparty brief"; "structured interview", not "candidate elicitation". |

### J-CO — Prospective collaborator (advanced contributor; not full-time)

| Column | Value |
|:---|:---|
| assumed-normal | Most "interesting projects" are slide-pitches without engineering depth; collaborator engagements drift into unbilled work; brand voice between marketing and reality is usually inconsistent. |
| bridge-frame | Long-form `/manifiesto/<product>` shows real engineering thinking. `/tech-lab` engineering-arm voice signals depth. Brand-voice consistency (drift gates) signals taste. |
| objection-patterns | "Is the engineering and thinking real?"; "Will the work transfer?"; "Will I be billed for my time?"; "Is the IP I produce mine, theirs, or shared?" |
| decision-criteria | Visible technical depth; SOPs and discipline visible; brand voice consistency between dossier and website; clear collaborator-engagement contract. |
| evidence-types-trusted | `/manifiesto/<product>` long-form; `/tech-lab` engineering-arm voice; per-engagement scope-of-work document; AKOS canon visible (signals discipline). |
| first-i-don't-understand-trigger | Marketing prose where the website said engineering depth was a thing; OR an "exposure-not-payment" implication. |
| internal-vocabulary-(restricted) | Collaborator-side cooperation likelihood; depth-signal counterparty assessment; IP-tension elicitation pattern. |
| external-vocabulary-(canonical) | "Collaborator", "contributor", "engagement scope", "deliverable", "time tracking", "IP terms". Use "collaborator brief", not "collaborator counterparty brief"; "scope discussion", not "collaborator elicitation". |

## 3. Translation rules (forbidden externally; required internally)

Per [`akos-brand-baseline-reality.mdc`](../../../../../../../.cursor/rules/akos-brand-baseline-reality.mdc) (created I66 P2). Drift gate: `validate_brand_baseline_reality_drift.py` (P2).

| Internal vocabulary (restricted) | External canonical translation |
|:---|:---|
| counterparty | client / partner / advisor / candidate / contributor / investor / reviewer (audience-specific) |
| counterparty assessment | client briefing / partner briefing / advisor briefing / candidate briefing / contributor briefing |
| baseline reality | reading lens / audience reading / market context |
| elicitation | discovery interview / structured conversation / scoping interview |
| elicitation plan | discovery agenda / scoping agenda |
| approach techniques | discovery methodology |
| reliability grading | source confidence / evidence quality |
| source reliability | source confidence |
| intelligence collection | structured research / evidence gathering |
| intelligence report | research brief / engagement summary |
| internal collection | internal research |
| indicator (in HUMINT sense) | signal / data point |
| observable (in HUMINT sense) | observation |
| requirement (in HUMINT sense) | research question / scoping question |
| lead (in HUMINT sense) | prospect / contact (audience-specific) |
| contact (in HUMINT operational sense) | meeting / outreach / conversation |
| asset (in HUMINT sense) | NEVER use externally; rephrase entirely |
| cover (in HUMINT sense) | NEVER use externally; rephrase entirely |
| cooperation likelihood | engagement readiness / counterparty fit (still NOT external; even softened, this token is operator-private) |
| sub-source primacy | NEVER use externally; rephrase entirely |
| objection-cluster | objection pattern (acceptable externally as plain English) |
| reporting channel | channel (acceptable externally as plain English) |

> **The translation rule is one-way.** External register is the canonical for external surfaces; internal register is the canonical for operator-private surfaces. **Never** invert: do not use external vocabulary in internal SOPs (loses the precision); do not use internal vocabulary on external surfaces (collapses the brand).

## 4. Operational use

### 4.1 Pre-engagement counterparty briefing (per-engagement)

Operator (or future BrandOps Lead) generates a per-engagement counterparty brief from the matrix. The brief is operator-private (`docs/wip/intelligence/<engagement>/counterparty-brief.md`; access_level: 5; archived 90d after engagement close).

The brief draws from the relevant J-* row and adds engagement-specific data:

- Counterparty's specific assumed-normal (read from their public surfaces).
- Counterparty's specific motivations (inferred from public signals; verified in discovery).
- Counterparty's reliability grade (preliminary; refined post-meeting).

This pattern is codified in `SOP-COUNTERPARTY_BASELINE_ASSESSMENT_001.md` (created I66 P3).

### 4.2 Discovery interview (per-engagement; external-facing)

Per `SOP-ELICITATION_DISCIPLINE_001.md` (created I66 P3; HUMINT-grounded, internal-only register), the operator conducts the discovery interview using:

- Internal-register prep (operator-private; uses elicitation discipline).
- External-register delivery (customer-facing; uses "discovery interview" framing).

The interview is structured (open-ended → focused → closure). The operator listens for assumed-normal + bridge-frame opportunities + objection-pattern markers + decision-criteria signals.

### 4.3 Post-engagement intelligence report (per-engagement; operator-private)

Per `SOP-INTELLIGENCE_REPORT_001.md` (created I66 P3; HUMINT-grounded, internal-only register), the operator files a per-engagement intelligence report at `docs/wip/intelligence/<engagement>/intelligence-report-YYYY-MM-DD.md`. Access_level: 5.

The report uses internal register: counterparty assessment refined post-meeting + reliability grading + observation-vs-inference separation + research-question-driven structure.

### 4.4 Per-deck preparation (per-deck per-engagement)

Per I66 P6, each of the 6 deck templates ships with:

- `<deck>.md` — the deck content (external-facing).
- `<deck>.objections.md` — anticipated objections drawn from the relevant J-* row (operator-private; internal register).
- `<deck>.counterparty-brief.md` — operator pre-meeting prep template (operator-private; internal register).

Operator copies the templates per-engagement; instantiates with counterparty-specific data; archives in `docs/wip/intelligence/<engagement>/`.

### 4.5 Brand audit (continuous)

`validate_brand_baseline_reality_drift.py` (P2) runs in CI:

1. Scans rendered DOM on `boilerplate/` + `hlk-erp/` (excluding access_level: 5 surfaces).
2. Asserts no token from any internal-vocabulary-(restricted) cell is present.
3. Asserts every external-facing artifact identifies its primary audience (frontmatter `audience: <J-*>` for canonical assets; per-page metadata for boilerplate pages).
4. On match: print precise file + line + token + suggested external translation; exit 1.

The drift gate is wired into `release-gate.py`. CI breaks on internal-register leakage.

## 5. Maintenance

- **Author.** Founder (sole). Brand Manager reviews + maintains drift detection.
- **Cadence.** Quarterly review (per `process_list.csv` row "counterparty baseline assessment cadence", I66 P3). Each review:
  - Adds rows for new audiences encountered.
  - Refines bridge-frame + objection-pattern entries based on engagement learning.
  - Refines translation rules based on language drift discovered in CI.
- **Trigger.** Any new external audience (e.g., a new EU funding panel; a new customer industry vertical) triggers a new row before the first engagement.
- **Authorization.** Founder-only edits to internal-register columns. Brand Manager + founder co-edit external-register columns.

## 6. Related canonicals

- [`BRAND_ARCHITECTURE.md`](BRAND_ARCHITECTURE.md) — Branded House + voice tier mapping.
- [`BRAND_VOICE_FOUNDATION.md`](BRAND_VOICE_FOUNDATION.md) — Tier-1 + Tier-2 voice contract.
- [`BRAND_REGISTER_MATRIX.md`](BRAND_REGISTER_MATRIX.md) — register matrix (this file extends with audience baseline).
- [`BRAND_DO_DONT.md`](BRAND_DO_DONT.md), [`BRAND_JARGON_AUDIT.md`](BRAND_JARGON_AUDIT.md).
- [`BRAND_VISION.md`](BRAND_VISION.md) — vision doctrine reads through these audiences.
- [`SOP-COUNTERPARTY_BASELINE_ASSESSMENT_001.md`](../../Operations/PMO/SOP-COUNTERPARTY_BASELINE_ASSESSMENT_001.md) (created I66 P3).
- [`SOP-ELICITATION_DISCIPLINE_001.md`](../../Operations/PMO/SOP-ELICITATION_DISCIPLINE_001.md) (created I66 P3).
- [`SOP-COUNTERPARTY_RELIABILITY_GRADING_001.md`](../../Operations/PMO/SOP-COUNTERPARTY_RELIABILITY_GRADING_001.md) (created I66 P3).
- [`SOP-INTELLIGENCE_REPORT_001.md`](../../Operations/PMO/SOP-INTELLIGENCE_REPORT_001.md) (created I66 P3).
- [`docs/wip/planning/66-brand-vision-ops-sweep/journeys-2026-05-08.md`](../../../../wip/planning/66-brand-vision-ops-sweep/journeys-2026-05-08.md) — journey scaffolds that this matrix canonicalizes.
- [`docs/wip/intelligence/`](../../../../wip/intelligence/) — operator-private working space (created I66 P3).
- HUMINT FM 2-22.3 (US Army, Sept 2006, public release) — methodology source citation.
