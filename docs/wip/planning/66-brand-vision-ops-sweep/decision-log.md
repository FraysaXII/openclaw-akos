---
language: en
status: charter
initiative: 66-brand-vision-ops-sweep
report_kind: decision-log
last_review: 2026-05-08
---

# I66 Decision Log

Format: ID · question · options considered · decision · rationale · implication · date · status.

20 decisions: D-IH-66-A through D-IH-66-T. All entered as **Active** at charter; transitions to **Approved** happen at the relevant operator pause; final transition to **Closed** at I66 closeout (P8 / DECISION_REGISTER.csv mirror).

## D-IH-66-A — Brand architecture pattern

- **Q.** Holistika Research SL is the only legal entity, but operator presents three teams (Holistika, Think Big, HLK Tech Lab) and a wide service catalog. How should the brand architecture be codified?
- **Options.**
  1. **Branded House** — one umbrella brand "Holistika"; three operational sub-marks; product brands beneath the lab.
  2. **House of Brands** — split into three legal entities to match three brands.
  3. **Hybrid endorsed** — sub-marks endorsed "by Holistika" at first mention.
- **Decision.** Option 1 — Branded House. Codified in new canonical `BRAND_ARCHITECTURE.md` (P1) and rewritten `BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04` (P1).
- **Rationale.** One legal entity ⇒ one umbrella brand is the cheapest, cleanest legal posture. Three sub-marks give the messaging force the operator wants without splitting the company. The lab → channel pipeline (research validates → strategy guides → consulting executes) becomes the **flywheel narrative** that explains why one company can credibly claim research-grade rigor + execution scale.
- **Implication.** "Think Big" is a brand sub-mark, not a legal entity. ALL prior copy implying "Think Big SL" or "Think Big subsidiary" is incorrect; PRODUCT.md fix in `hlk-erp` is one such. Trademark filings (P4) target Holistika + Think Big + HLK Tech Lab + MADEIRA + KiRBe (5 marks) under the SL.
- **Date.** 2026-05-08 · **Status.** Active.

## D-IH-66-B — Sub-mark voice tier

- **Q.** Should the three sub-marks share the master Holistika voice or carry distinct sub-voices?
- **Options.**
  1. **Single master voice** — all sub-marks speak Holistika.
  2. **Three distinct voices** — each sub-mark has independent voice canon.
  3. **Two-tier (Tier 1 master + Tier 2 sub-marks)** — one master cadence + per-sub-mark register modulation (Holistika R&S formal-academic; Think Big practical-operational; HLK Tech Lab technical-rigorous).
- **Decision.** Option 3 (operator confirmed: "Option B + C"). Tier-2 register variation is real and codified, but Tier-1 cadence (sentence rhythm, syntax, paragraph density) is held constant. Codified in `BRAND_VOICE_FOUNDATION.md` updates (P1).
- **Rationale.** Single voice (option 1) loses the messaging force of three teams. Three voices (option 2) shatters brand recognition and creates onboarding-burden for collaborators. Two-tier preserves recognition while letting Tech Lab read like Tech Lab and Think Big read like Think Big.
- **Implication.** Each sub-mark gets a register block in `BRAND_VOICE_FOUNDATION.md`; manifestos (P5) are written in Tier-2; investor decks (P6) are Tier-1; operator-private intelligence reports (P3 + P6) are a third internal-only register.
- **Date.** 2026-05-08 · **Status.** Active.

## D-IH-66-C — Trademark filing inside or outside I66

- **Q.** Should I66 deliver the trademark filings themselves, or only the strategy + handoff package?
- **Options.**
  1. **Strategy + clearance + handoff package only** — operator drives the EUIPO / OEPM filings outside I66.
  2. **Strategy + clearance + ready-to-sign forms + operator-handoff** — I66 delivers everything except the literal signature + fee + submission.
  3. **Full filings inside I66** — the agent files via OEPM API or EUIPO online filing.
- **Decision.** Option 2. Operator confirmed addition of ready-to-sign forms (TM-1 EUIPO equivalent + OEPM forms) for the 1-2 day extra effort.
- **Rationale.** Option 3 requires legal counsel of record and operator-only credentials; out of scope for an agent. Option 1 leaves too much friction at the handoff. Option 2 trims the operator's path to "sign + pay + submit" in three steps.
- **Implication.** P4 effort ↑ from 4-5d to 5-6d; ready-to-sign forms in `docs/references/hlk/v3.0/Admin/O5-1/Operations/Legal/TRADEMARK_FILING_FORMS_2026-05/` per mark per jurisdiction.
- **Date.** 2026-05-08 · **Status.** Active.

## D-IH-66-D — Spanish + French voice canonicals

- **Q.** The operator supplied 20+ transcripts (mostly Spanish, some French). Should language-specific voice canon be a small update or a deep enrichment?
- **Options.**
  1. **Light update** — keep `BRAND_SPANISH_PATTERNS.md` thin; defer French.
  2. **Deep Spanish enrichment + French canonical** — substantially expand BRAND_SPANISH_PATTERNS from transcripts; create new `BRAND_FRENCH_PATTERNS.md`.
  3. **All EU languages** — Spanish + French + Italian + Portuguese.
- **Decision.** Option 2.
- **Rationale.** Transcripts evidence rich ES + FR voice patterns (formal-vs-conversational register; specific cadence + lexicon; turn-taking discipline; how the operator translates Tier-1 master voice into market-language). Italian / Portuguese have no operator audio signal yet; deferring respects the AKOS principle of evidence-based canon.
- **Implication.** P1 effort ↑ from 4-5d to 7-8d. Transcripts curated to `docs/references/hlk/v3.0/_assets/transcripts/` with frontmatter (date, language, audience, topic, lens-tags). Lens-tags allow I66 voice-mining + I67 funnel-mining without re-curating.
- **Date.** 2026-05-08 · **Status.** Active.

## D-IH-66-E — Manifesto rewrite scope

- **Q.** `/manifiesto/holistika` was originally scoped as P4-follow-on. Should all 5 manifesto entries (holistika / madeira / madeira-agent / kirbe / envoy) be rewritten in I66?
- **Options.**
  1. **Holistika only** — defer the four product manifestos.
  2. **All five rewritten in P5** — register-aligned, voice-tested, drift-gated.
- **Decision.** Option 2.
- **Rationale.** Four product manifestos with old prose against a new vision doctrine is exactly the drift-divergence pattern P2 + P7 drift gates exist to prevent. Deferring would mean shipping known drift on day 1.
- **Implication.** P5 effort ↑ from 4d to 6d. Each manifesto is voice-tested against `BRAND_VOICE_FOUNDATION` Tier-2 + `BRAND_REGISTER_MATRIX` rows.
- **Date.** 2026-05-08 · **Status.** Active.

## D-IH-66-F — Other website content

- **Q.** Beyond manifestos, what else on `boilerplate` needs a sweep?
- **Options.**
  1. **Manifestos only** — leave home / services / tech-lab / contact alone.
  2. **Plus home + /services + /tech-lab** — but skip /how-we-work + /vision (defer).
  3. **All public surfaces in scope** — home flywheel + /services 6×3 matrix + /tech-lab + new /how-we-work + new /vision + i18n EN/ES/FR + SiteFooter trademark posture.
- **Decision.** Option 3.
- **Rationale.** Operator surfaced "you're not using our intellectual assets properly." That's a public-surface coherence problem, not a manifesto problem. Half-measures invite operator to surface it again next sprint.
- **Implication.** P5 ships home flywheel SVG (replacing flat connection line) + new `/services` rewrite as the 6 services × 3 arms × 3 tiers matrix + new `/how-we-work` page (lab → channel pipeline) + new `/vision` page (curated public subset of `BRAND_VISION.md`). Fixed indigo / slate drift in `app/manifiesto/data.ts` + `components/home/entities-section.tsx`. Default-theme decision (D-IH-66-G) lands here.
- **Date.** 2026-05-08 · **Status.** Active.

## D-IH-66-G — Boilerplate default theme

- **Q.** Operator nuance: "boilerplate is better dark; hlk-erp works better system default but color is hidden behind settings, poor UX." Should I66 change defaults?
- **Options.**
  1. **Migrate boilerplate dark → system** for parity.
  2. **Keep both as-is** but improve hlk-erp settings UX surface (color-mode picker visible in shell, not buried).
  3. **Investigate "system that really works"** for both repos.
- **Decision.** Option 2.
- **Rationale.** Operator said: "leave it like it is for now." Boilerplate is photographed dark in Spotlight cards + brand assets; flipping to system breaks visual canon. hlk-erp UX improvement (color-mode picker on operator chrome) is a small fix that doesn't touch theme defaults.
- **Implication.** P5 includes a minor `hlk-erp` chrome change (move color-mode picker from settings drawer to operator app-bar). No theme migration. `BRAND_VISUAL_PATTERNS.md` documents the asymmetry (boilerplate `defaultTheme="dark"`, hlk-erp `defaultTheme="system"`) as intentional.
- **Date.** 2026-05-08 · **Status.** Active.

## D-IH-66-H — Legacy `/dashboard` + `/(authapp)/login` on boilerplate

- **Q.** Operator: "we have legacy ERP/testing site behind /dashboard and /auth, that I'd like to decommission one day. Not now. But I'd don't want that to impact Impeccable somehow." How should I66 treat legacy?
- **Options.**
  1. **Migrate everything to canonical** — including legacy.
  2. **Skip legacy entirely** — tag as out-of-scope in PRODUCT.md.
  3. **Skip legacy + add boundary signal** — declare OOS in PRODUCT.md + add a robots.txt noindex for `/dashboard` and `/auth/*` so search-engines stop indexing legacy.
- **Decision.** Option 3.
- **Rationale.** Legacy decommission is a separate initiative (out of I66 scope per operator). But search-engine indexing of legacy surfaces leaks legacy as if it were canonical, undoing brand-voice discipline. Robots noindex is a 1-line fix that respects operator's "not now" while protecting brand-voice discipline.
- **Implication.** `boilerplate/PRODUCT.md` Section 8 (out-of-scope) declares legacy explicitly. `boilerplate/public/robots.txt` adds `Disallow: /dashboard` + `Disallow: /auth/*` (P5 chore).
- **Date.** 2026-05-08 · **Status.** Active.

## D-IH-66-I — Vision artifact split (internal vs public)

- **Q.** Should `BRAND_VISION` be one document or two?
- **Options.**
  1. **One internal-only document.**
  2. **Two documents** — internal canonical + public-facing /vision page.
  3. **One document with public-region markers + drift gate** — `<!-- public-vision:start --> ... <!-- public-vision:end -->` annotations in the canonical; a P7 drift gate asserts boilerplate `/vision/page.tsx` prose matches the public-region.
- **Decision.** Option 3.
- **Rationale.** Two-document split (option 2) creates two SSOTs and the drift problem P2 + P7 gates are designed to prevent. Single canonical with public-region markers preserves "one document, one truth" while making the public/private boundary mechanically enforceable.
- **Implication.** `BRAND_VISION.md` (P1) ships with explicit public-region markers. `validate_brand_vision_drift.py` (P7) parses both and asserts equality. Operator pause #6 includes a live read of `/vision` rendered prose.
- **Date.** 2026-05-08 · **Status.** Active.

## D-IH-66-J — I67 paired-research input scope

- **Q.** Should the operator-supplied transcript dump feed both I66 (voice-mining) and I67 (funnel-mining), or only I66?
- **Options.**
  1. **I66 only** — I67 starts fresh.
  2. **I66 + I67 both** — same transcripts mined twice with two different lenses.
  3. **I67 only** — defer transcript curation entirely.
- **Decision.** Option 2.
- **Rationale.** Same evidence, two questions. I66 asks "how does the operator + collaborators speak in each register?" I67 will ask "where in the funnel did this conversation happen, what was the trigger, what was the objection, what was the close-or-not signal?" The operator hand-curates each transcript with multi-lens frontmatter (lens-tags include both `voice-pattern` and `funnel-stage`); two analyses, one curation pass.
- **Implication.** Transcript frontmatter schema includes both lens types. `docs/_assets/transcripts/INDEX.md` shows both indexes.
- **Date.** 2026-05-08 · **Status.** Active.

## D-IH-66-K — I67 scaffold strength at I66 closure

- **Q.** When I66 closes and creates the I67 RevOps Discovery folder, how complete should that scaffold be?
- **Options.**
  1. **Full plan** — scope, phases, decisions pre-locked.
  2. **Light charter** — outcome + scope-compendium + pause-points; phases TBD.
  3. **Research-first / near-empty** — charter + research-brief + starting-hypotheses tree of explicit `[UNKNOWN]` markers + decision-points list (operator-blocking, before any phase scopes) + sources-and-prior-art + AGENT_INSTRUCTIONS with binding mandates.
- **Decision.** Option 3 (operator confirmed: "research-first").
- **Rationale.** Operator: "another agent will follow ... investigate further, not to be set in stone, actively upgrade or scope by researching, as that's what we do best." Pre-locked plan would betray that mandate. Research-first ensures the next agent reads, interviews, and proposes — not assumes.
- **Implication.** P8 Part C is the I67 scaffold. AGENT_INSTRUCTIONS.md contains six binding mandates including: do not lock tooling / pricing / channels without operator approval; treat scaffold as VERSION 0; challenge every starting hypothesis.
- **Date.** 2026-05-08 · **Status.** Active.

## D-IH-66-L — Packaging vs spinning out vision-only initiative

- **Q.** Operator: "I expected a 3-week plan or even more." Should I66 be packaged as one mega-initiative with explicit checkpoints, or split into two (I66 = brand canon + I66.5 = vision + ops integration)?
- **Options.**
  1. **Mega with checkpoints** (single initiative, 8 pause points, ~5.5 weeks).
  2. **Split into I66 + I66.5** — close I66 at end of P3 ish, open I66.5 for vision + drift gates + UAT.
  3. **Three smaller initiatives** — I66a / I66b / I66c.
- **Decision.** Option 1 (operator confirmed: "mega-with-checkpoints").
- **Rationale.** Vision + canon + ops integration are tightly coupled (vision drives architecture decisions; architecture drives process_list rows; process_list drives SOPs). Splitting would create artificial seams that operator pauses already provide without artificial closures.
- **Implication.** I66 stays as one initiative. Pause points serve as logical checkpoints; agent-checkpoint-discipline rule ensures context coherence across agent restarts inside a phase.
- **Date.** 2026-05-08 · **Status.** Active.

## D-IH-66-M — Baseline Reality canonical visibility (CORPINT vs HUMINT framing)

- **Q.** Operator framing: "this is internal only, only for people that will not think strangely of the fact we used inspiration from HUMINT. On the other hand, this is just part of our CORPINT Research business as SaaS. We have tons of references, not only that one. And that's why I say to collaborators that we are PMs, Researchers that get to know what we need to know to do better. Investors know we'll use whatever research necessary to get to a profitable position and have the operational force to do that. Customers come thinking we are professional, like a big company acting on behalf of SMEs."
- **Options.**
  1. **Internal-only matrix, with HUMINT citation visible** — full transparency about the source.
  2. **External-facing matrix** — translate concepts entirely; no HUMINT citation; brand it as CORPINT or "structured research methodology."
  3. **Dual-register matrix** — one internal vocabulary (HUMINT-grounded for operator + agents + cleared collaborators only) + one external translated capability messaging (BD onboarding voice: "we are PMs, researchers, professionals doing structured research") with an explicit translation table between the two.
- **Decision.** Option 3.
- **Rationale.** Operator's three audience-truths exist simultaneously and that's part of the conundrum (operator confirmed: "all three options are correct"). Single internal-only register would force collaborators + customers to use HUMINT vocabulary externally — risky brand collapse if leaked. Pure external translation would lose the operator's CORPINT discipline + decision rigor in agent prompts. Dual-register preserves rigor internally, professional-research voice externally, with a citation rule (`akos-brand-baseline-reality.mdc` enforces external-facing prose may only cite the external register).
- **Implication.** `BRAND_BASELINE_REALITY_MATRIX.md` (P1) ships dual-register: per audience-x-topic row contains `assumed-normal`, `bridge-frame`, `objection-patterns`, `decision-criteria`, `evidence-types-trusted`, `first-i-don't-understand-trigger`, `internal-vocabulary-(restricted)`, `external-vocabulary-(canonical)`. P3 SOPs (4 new HUMINT-derived) live in `v3.0/Admin/O5-1/Operations/IntelligenceOps/` with internal-only register. P6 deck companions (`.objections.md` + `.counterparty-brief.md`) draw from the matrix per deck. Founder bio + investor deck + press kit cite only the external register.
- **Date.** 2026-05-08 · **Status.** Active.

## D-IH-66-N — HLK abbreviation governance

- **Q.** Operator surfaced: "HLK is a short for Holistika." Where + how is it allowed?
- **Options.**
  1. **No abbreviations** — always "Holistika."
  2. **Free use of HLK** — alongside Holistika.
  3. **Governed abbreviations** — HLK allowed only in (a) code identifiers, (b) internal docs after first introduction, (c) CLI / shell prompts; forbidden in (a) headlines, (b) cold-outreach first message, (c) any paragraph where Holistika has not been spelled out at least once. Apply same governance to MA / KB / EV / TB / TL.
- **Decision.** Option 3.
- **Rationale.** Operator's intent: HLK is shorthand earned through context, not a marketing token. Free use confuses trademark posture (HLK is not a registered mark in P4 strategy). Governed use lets it serve technical contexts (folder names, package prefixes, CLI commands) without diluting the master Holistika brand externally.
- **Implication.** New canonical `BRAND_ABBREVIATIONS.md` (P1) with allowed/forbidden table per term. `validate_brand_jargon.py` (P2) extends to flag abbreviation violations. `BRAND_JARGON_AUDIT.md §4` updated to cross-reference.
- **Date.** 2026-05-08 · **Status.** Active.

## D-IH-66-O — Logo audit + canonical decisions

- **Q.** Operator showed four logo candidates. What's canonical, what's deprecated, what's contextual?
- **Options.**
  1. **Choose one canonical**, retire all others.
  2. **Multi-context system** — one primary mark + accepted variants for specific contexts.
- **Decision.** Option 2 (multi-context). Specifically:
  - **Hi monogram** = primary mark, used in social avatars, favicons, app icons, compact contexts.
  - **HOLÍSTIKA Research wordmark with accent on Í** = formal canonical, used in legal documents, letterheads, footer, formal decks, trademark filings.
  - **Holistika RGB-rings chromatic version** = deprecated, retire from production by P5 close.
  - **Stylized-logo-vs-plain-prose split rule**: stylized logo allowed in brand assets, decks, hero sections; plain "Holistika" + "Holistika Research SL" in legal prose, contracts, headings.
- **Rationale.** Operator showed multiple logos; the Hi monogram is what works compactly + brand-recognized; the HOLÍSTIKA wordmark with the diacritic is what conveys the formal Spanish-rooted positioning. RGB-rings reads as 2010s-era "tech startup" and doesn't carry research weight. Stylized-vs-prose split is necessary because legal prose with stylized Í becomes unreadable in B&W contracts.
- **Implication.** `BRAND_LOGO_SYSTEM.md` (P1) codifies all four decisions + provides usage matrix + deprecation timeline. P5 boilerplate components updated to use Hi monogram in `<NavigationBar>` + HOLÍSTIKA wordmark in `<SiteFooter>` legal block. Asset directory cleaned in `boilerplate/public/brand/` with a `DEPRECATED/` subfolder for RGB-rings transition.
- **Date.** 2026-05-08 · **Status.** Active.

## D-IH-66-P — Agent-checkpoint discipline as cursor rule

- **Q.** I66 is ~5.5 weeks. Agent context degrades inside long phases. Should agent self-checkpointing be a one-off pattern in this initiative or a new cursor rule applicable to all initiatives?
- **Options.**
  1. **One-off** — described in master-roadmap, not generalized.
  2. **New cursor rule** — `.cursor/rules/akos-agent-checkpoint-discipline.mdc` codifies 8 operator pauses + ~18 agent self-checkpoints pattern; applies to any initiative with ≥3 phases or ≥2 calendar weeks of work.
- **Decision.** Option 2.
- **Rationale.** I65 ran 6 phases; I64 ran 5 phases; future initiatives will routinely span >2 weeks. Codifying once produces the discipline for every initiative, not just I66. Aligns with [Cursor's large-codebases guidance](https://docs.cursor.com/guides/advanced/large-codebases) on staying close to plan-creation context.
- **Implication.** P2 ships `akos-agent-checkpoint-discipline.mdc`. Updated `akos-planning-traceability.mdc` cross-references it. I65 / I64 / I63 retroactively gain compliance posture (no retroactive checkpointing required, but new phases on those initiatives will follow it).
- **Date.** 2026-05-08 · **Status.** Active.

## D-IH-66-Q — Methodology track-record evidence integration

- **Q.** Operator shared the fitness-franchise track record (anonymized: 50K€ → 7 venues at +250K€ each, plus mkt-agency follow-on, plus 2 customer cross-pollinations, plus 3 cold offers/year). Should this evidence be integrated into public-facing materials?
- **Options.**
  1. **No integration** — keep operator's history out of brand prose.
  2. **Integrate verbatim** — name + recognizable details.
  3. **Anonymized methodology track record** — "in a prior co-founder role I built a fitness-franchise from concept to 7 venues in <X period> with <Y capital efficiency>; the same structured-research + dossier discipline drove the result; references available under NDA."
- **Decision.** Option 3.
- **Rationale.** Operator's literal example name (batard.es) is requested out of public materials per operator's verbatim instruction. Anonymized methodology evidence does the brand work (transferable proof of capability) without breaching the example confidentiality. Cross-references to BD onboarding transcripts confirm operator already speaks of "I have built one franchise myself, scaling 7 venues, raising €1.7M with €50K..." in private collaborator context.
- **Implication.** `FOUNDER_BIO.md` (P6) includes a "Methodology track record" block at three lengths (long / medium / short). Investor deck (P6) slide 9 ("Why Holistika now") cites the anonymized record. Press kit (P6) contains the anonymized version + a "verifiable references on NDA" footnote. ENISA deck (P6) uses the methodology track record as the operational-experience signal.
- **Date.** 2026-05-08 · **Status.** Active.

## D-IH-66-R — `docs/wip/intelligence/` as working space

- **Q.** Where do CORPINT artifacts live during operations? They're not master canon (those are SOPs in `v3.0/`), they're not registers (those are CSVs), they're per-engagement intelligence reports + counterparty briefs that get drafted, used, archived.
- **Options.**
  1. **In `v3.0/_assets/`** — alongside other reference assets.
  2. **In `docs/wip/intelligence/`** — new working directory; sibling to `docs/wip/planning/`.
  3. **In each engagement's dossier folder** under `docs/wip/dossiers/`.
- **Decision.** Option 2.
- **Rationale.** Intelligence artifacts are operationally distinct from planning (they're per-counterparty, per-engagement, time-bounded). They shouldn't live in `v3.0/_assets/` (that's stable reference). Per-engagement folders (option 3) lose cross-engagement pattern recognition. New dedicated working directory mirrors the `docs/wip/planning/` pattern (operator-facing, time-aware, discoverable).
- **Implication.** P3 creates `docs/wip/intelligence/` with `INDEX.md`, `templates/` subfolder (counterparty-baseline-template.md, intelligence-report-template.md, elicitation-plan-template.md), and a `2026-05-08-i66-illustrative/` folder showing one fully-worked example for training. Access-level: 5 (operator + cleared collaborators only).
- **Date.** 2026-05-08 · **Status.** Active.

## D-IH-66-S — Impeccable v3.1 BASELINE_REALITY 5th setup gate

- **Q.** Impeccable currently has 4 setup gates (PRODUCT.md, DESIGN.md, MOTION.md, ACCESSIBILITY.md). Should baseline-reality be a 5th gate?
- **Options.**
  1. **Skip** — baseline-reality is brand-canon, not Impeccable.
  2. **Standalone fifth gate** — `BASELINE_REALITY.md` as a required setup file alongside PRODUCT.md.
  3. **Extension of PRODUCT.md** — add a "Baseline Reality" section.
- **Decision.** Option 2 (standalone fifth gate).
- **Rationale.** Baseline reality is per-audience reading, not per-product positioning; merging into PRODUCT.md would mix concerns (operator-truth ≠ counterparty-truth). Skipping would mean Impeccable produces UI for a "single audience" assumption that I66 explicitly rejects. Standalone gate forces Impeccable to ask "for which audience am I designing this surface?" before producing any prose.
- **Implication.** `.cursor/skills/impeccable/SKILL.md` (P0) updates to v3.1 with the 5th gate + load-context.mjs reads it. `hlk-erp/BASELINE_REALITY.md` + `boilerplate/BASELINE_REALITY.md` scaffolds shipped (P0 carry-over).
- **Date.** 2026-05-08 · **Status.** Active.

## D-IH-66-T — I67 RevOps Discovery kickoff naming + scope

- **Q.** Operator considered MarOps vs MktOps. Which discipline + which kickoff?
- **Options.**
  1. **MarOps** — Marketing Operations only (campaigns, content, attribution).
  2. **MktOps** — same as MarOps, more startup-vernacular.
  3. **RevOps** — Revenue Operations: positioning + acquisition + activation + retention + referral + partner channels + pricing.
- **Decision.** Option 3 — RevOps Discovery.
- **Rationale.** Operator described the gap as "actual marops or mktops marketing full sweep," but the surface they need covers acquisition (marketing) + sales (closing) + onboarding (activation) + retention (CS) + referral + partnership economics. That's RevOps, not just marketing. Naming it RevOps signals the broader scope to the next agent and to operator's advisors. RevOps maps to standard SaaS / consultancy benchmarks the next agent will reference (HubSpot, Stripe, Linear).
- **Implication.** I67 charter title: "RevOps Discovery." First initiative; chartered at I66 close; P0 of I67 will be operator-driven research definition; agent does NOT lock vocabulary to "MarOps" or "MktOps" without operator approval (one of 8 decision-points in I67 scaffold).
- **Date.** 2026-05-08 · **Status.** Active.

## D-IH-66-AD — Direct-access service and method pages

- **Q.** P5 requires `/services` and `/how-we-work`, but the operator is not ready to expose those routes through normal public navigation because the RevOps/marketing sweep has not yet matured the surrounding journeys. Should the pages ship publicly, be deferred, or exist only for known-route access?
- **Options.**
  1. **Public navigation now** — add both routes to the main navigation, footer, CTAs, and sitemap.
  2. **Defer entirely** — leave the P5 deliverable unimplemented until I67.
  3. **Direct-access only** — create the routes, keep them out of visible navigation and sitemap exposure, and mark them `noindex` until I67 decides whether/how to promote them.
- **Decision.** Option 3. `/services` renders the SERVICE_OFFERING_CATALOG 6 x 3 matrix; `/how-we-work` renders the engagement rhythm. Both are direct-access pages: available by exact URL, absent from navigation/footer/home CTAs, and marked `noindex, nofollow`.
- **Rationale.** This preserves the P5 implementation obligation and gives operator-mediated readers a precise route, while preventing premature market leakage before the RevOps Discovery initiative clarifies audience journeys, channel strategy, and offer packaging.
- **Implication.** Promotion from direct-access to public navigation becomes an I67/P8 operator decision, not a silent code change. Any future nav/footer/sitemap addition must cite this decision and update the route metadata intentionally.
- **Date.** 2026-05-09 · **Status.** Active.

## Cross-references

- All 20 decisions targeted for `DECISION_REGISTER.csv` mirror at I66 closure (P8).
- D-IH-66-A, D-IH-66-O, D-IH-66-N affect `BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04` rewrite (P1).
- D-IH-66-M, D-IH-66-S affect Impeccable + the new baseline-reality drift gate.
- D-IH-66-K, D-IH-66-T affect I67 scaffold (P8 Part C).
- D-IH-66-P affects two new cursor rules (P2).
- D-IH-66-AD affects boilerplate `/services` and `/how-we-work` direct-access routing (P5).

## Status transitions

- All 20 entered as **Active** at charter (2026-05-08).
- Each transitions to **Approved** at the relevant operator pause:
  - Pause #1 (P0 close): D-IH-66-A, D-IH-66-S
  - Pause #2 (P1 close): D-IH-66-B, D-IH-66-D, D-IH-66-I, D-IH-66-M, D-IH-66-N, D-IH-66-O
  - Pause #3 (P2 close): D-IH-66-P
  - Pause #4 (P3 close, CSV gate): D-IH-66-R
  - Pause #5 (P4 close): D-IH-66-C
  - Pause #6 (P5 close, live review): D-IH-66-E, D-IH-66-F, D-IH-66-G, D-IH-66-H
  - Pause #7 (P6 close): D-IH-66-Q
  - Pause #8 (P7 close): no decision transitions; gate is mechanical
  - I66 closure (P8): D-IH-66-J, D-IH-66-K, D-IH-66-L, D-IH-66-T → all to **Closed** in DECISION_REGISTER mirror
- D-IH-66-CLOSURE entered at P8 final commit.
