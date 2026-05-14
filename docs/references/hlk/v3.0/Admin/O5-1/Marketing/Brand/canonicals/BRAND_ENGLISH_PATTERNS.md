---
language: en
status: active
sop_id: BRAND-ENGLISH-PATTERNS-001
role_owner: Brand & Narrative Manager
area: Marketing
entity: Holistika Research SL
program_id: shared
topic_ids:
  - topic_brand_voice
artifact_role: canonical
intellectual_kind: brand_asset
authority: Founder + Brand Manager
last_review: 2026-05-14
ssot: true
authored: 2026-05-14
companion_to:
  - BRAND_VOICE_FOUNDATION.md
  - BRAND_REGISTER_MATRIX.md
  - BRAND_FRENCH_PATTERNS.md
  - BRAND_SPANISH_PATTERNS.md
  - BRAND_COPYWRITING_DISCIPLINE.md
  - BRAND_LLM_TONE_TELLS.md
---

# BRAND_ENGLISH_PATTERNS — English brand voice canonical

> **Status — Active (Initiative 71 P1; mints the EN locale canonical alongside the existing FR + ES siblings).** Author the same patterns-to-follow + patterns-to-refuse coverage the FR + ES canonicals provide, calibrated for the EN audiences Holistika actually addresses: investors (US + UK), advisors (multi-jurisdictional), regulators (EU-EN procedural English), partners (Big-Tech-adjacent SaaS / consultancies), recruiters (EU-EN technical), and SME clients (typically EU-FR-EN bilingual or UK-mid-market). The validator pack `scripts/validate_brand_voice_register.py` (extended at I71 P1 Pack A1) consumes this canonical for EN-locale register checks. The companion `BRAND_LLM_TONE_TELLS.md` (also I71 P1) covers the more advanced anti-LLM-tone catalog; this file covers the foundational register matrix + salutation system + patterns to follow + patterns to refuse.

## 1. Why this canonical exists

The brand voice charter and archetype in [`BRAND_VOICE_FOUNDATION.md`](BRAND_VOICE_FOUNDATION.md) are language-agnostic. English requires its own canonical because:

- **English is the LLM-default authoring language.** AI-authored prose is most natively English; the patterns that read as "automated" (per `BRAND_COPYWRITING_DISCIPLINE.md` §2 + this canonical §12) are most easily smuggled into EN drafts. Discipline at the EN locale is the primary line of defense against tone-drift.
- **EN serves at least four register tiers Holistika ships into.** Peer-consulting (advisor + SME-client tier; warm-formal); investor-aspirational (deck headlines + dossier titles; concise + claim-forward); regulator-neutral (procedural-EN; ENISA + GDPR + EU-AI-Act counterparts; deflated and precise); formal-legal (counsel-side; instrument-driven). Each tier requires distinct openers, closers, and prohibited tokens.
- **British vs American spelling is a brand-identity signal.** Holistika defaults to **British English** for European-facing prose (programme; organisation; recognise; whilst; analyse) and **American English** only when the recipient surface is explicitly US-only (US investor deck; US advisor email; US partner pitch). The default avoids accidental code-switching mid-document.
- **Anglicisms are not an EN problem — but corporate-MBA jargon is.** EN cannot defend itself against anglicism (the language *is* the source); but EN audiences read MBA-deck jargon (`leverage synergies`, `bandwidth`, `disrupt`, `circle back`, `unpack`) as automated cadence. The §5 refuse-list focuses on this.
- **EN is the boilerplate-rendered default at `holistikaresearch.com/en/`.** The validator (`validate_brand_voice_register.py`) scans `boilerplate/messages/en.json` + `hlk-erp/messages/en.json` (when present) for §5 violations + §12 LLM-tone tells.

## 2. Core register matrix

| Recipient context | Address form | Salutation | Closing | Notes |
|:---|:---:|:---|:---|:---|
| First contact, business prospect (US / UK / EU-EN) | second person (no `Mr./Ms.`) | `Hi [First Name],` (US-warm) / `Hello [First Name],` (UK-neutral) | `Best,` (US) / `Kind regards,` (UK) | Default for unknown contacts; pick US vs UK by counterparty domain or LinkedIn region |
| First contact, advisor / counsel / regulator | second person (formal) | `Dear [First Name],` (UK) / `Dear Mr./Ms. [Last Name],` (only if title is signed) | `Yours sincerely,` (UK) / `Best regards,` (US) | Used for ENISA-equivalent + financial counsel + legal counsel |
| Ongoing peer rapport (advisor or partner) | second person | `Hi [First Name],` (warm-peer after 2-3 exchanges) | `Best,` (US) / `Kind regards,` then `Best wishes,` after the relationship deepens | The shift from `Best regards,` to `Best wishes,` is a peer-rapport signal in UK register |
| Internal Holistika team (EN speakers) | second person (informal) | `Hi [First Name],` or `[First Name],` | `Thanks,` or no closer | Internal-only; never carry over to external |
| Customer (SME, B2B context, EU-EN) | second person | `Hello [First Name],` | `Kind regards,` | Stay neutral-formal; SMEs in non-native-EN regions expect this |
| Press / journalist | second person | `Hello [First Name] [Last Name],` (full name on first contact) | `Kind regards,` | Always neutral-formal; press writes about brands they perceive as professional |
| LinkedIn DM (warm prospect) | second person | `Hi [First Name],` | `Best,` then no closer after the second exchange | DM register stays light; mirror counterparty's last reply |
| US investor (deck / dossier / outreach) | second person | `Hi [First Name],` | `Best,` | Investor-aspirational tier; concise + claim-forward language |
| UK / EU regulator (memo / letter) | second person formal | `Dear [Sir/Madam] / Dear [First Name] [Last Name],` | `Yours faithfully,` (if recipient name unknown) / `Yours sincerely,` (if named) | Procedural-EN; deflated and precise |

The composer's [`BRAND_REGISTER_MATRIX.md`](BRAND_REGISTER_MATRIX.md) lookup picks the **register**; this matrix picks the **opener / closer phrasing** within that register when `language_preference: en`.

## 3. Reference exchange — `2026-04-15 advisor introduction` (Founder ↔ EN advisor)

Operator-supplied reference exchange anchors the register decisions below. PII redacted per [`SOP-HLK_TRANSCRIPT_REDACTION_001.md`](../../People/Compliance/SOP-HLK_TRANSCRIPT_REDACTION_001.md).

### 3.1 Founder cold outreach to UK-domiciled advisor (formal, vous-equivalent UK register)

> Hello [First Name],
>
> I'm Fayçal Njoya, founder of Holistika. We help SMEs like yours on strategic projects where data and decision-making intersect.
>
> If the angle resonates, I'd welcome a thirty-minute exchange next week — Tuesday or Thursday early afternoon. I'll send a Calendly link in the follow-up.
>
> Kind regards,
> Fayçal

**Pattern signals:**

- Self-introduction with **first name + last name + role + company** in the first sentence.
- Verb choice: `help` (neutral) — avoid `assist` (over-formal), `partner with` (over-claim), `consult for` (sales-cadence).
- `SMEs like yours` — adopting the counterparty's frame ("we work with companies like yours") without over-claiming sector expertise.
- `data and decision-making intersect` — abstracting the offering into a **frame** (data + decision) rather than a **deliverable list** (more in §4).
- **`I'd welcome`** — UK-style polite invitation without performative humility.
- **Concrete time windows** (`Tuesday or Thursday early afternoon`) — avoids vague `at your convenience`.
- `Calendly` mentioned as a tool but not over-explained.

### 3.2 Founder transition to substance (mid-meeting summary)

> Concretely, we work on three axes:
>
> - One — mapping your current operation;
> - Two — identifying where information is missing or delays decision-making;
> - Three — building measurable processes that reduce that delay.

**Pattern signals:**

- `Concretely,` as a transition word — English B2B audiences expect a move from frame to substance, signaled with `Concretely`, `In practice`, or `Specifically`.
- Triadic structure (`three axes`) — works in EN as well, but lighter than in FR (FR triads are stronger rhetorical convention).
- `One — / Two — / Three —` numbering with em-dashes — formal but readable. Equivalent works with bullet hyphens.
- `reduce that delay` — outcome-oriented; not `improve performance` (vague).
- **`Concretely`** is a Holistika tic-tell because it's a literal translation from FR `Concrètement,` — operator should consider `Specifically` or `In practice` in pure-EN drafting.

### 3.3 Founder closer with concrete next step

> If this resonates, I can share a one-page note ahead of the call — it covers the three axes above with two worked examples.
>
> Best,
> Fayçal

**Pattern signals:**

- `If this resonates,` — softens the close; respects English B2B preference for non-pushy commerce.
- **`I can share`** — operator-explicit next step (matches the FR `Je vous envoie` pattern).
- `it covers ... with two worked examples` — concreteness about what the note contains.

## 4. Patterns to follow

| When... | Holistika does | Holistika does NOT |
|:---|:---|:---|
| First-contact email | `Hello [First Name], thanks for the message.` | `Hey, thanks for the mail` (over-warm); `Greetings,` (cold) |
| Statement of capability | `We help SMEs like yours on strategic projects where...` | `We offer consulting services in...` (sales-template) |
| Acknowledging a referral | `[Referrer] mentioned your work, and from what they shared...` | `[Referrer] told me about you` (under-substantive) |
| Stating availability | `Tuesday or Thursday early afternoon` (concrete windows) | `at your convenience` or `whenever works for you` (vague) |
| Confirming a meeting slot | `Confirmed for Tuesday 2:00 pm CET.` | `Great, see you Tuesday!` (over-warm for first contact) |
| Closing after substance | `Best,` (US-warm) → `Kind regards,` (UK-neutral) → `Best wishes,` (peer-warm after 3+ exchanges) | `Cheers,` (over-casual for early relationship); `Yours sincerely,` (over-formal for ongoing) |
| Stating uncertainty | `I'll confirm after a check.` or `I'll come back once the analysis is done.` | `I think...` (uncommitted; reads weak in B2B EN) |
| Politely declining | `That's not our core focus — let me put you in touch with [First Name Last Name] who...` | `Sorry, we can't help.` (closes door without redirect) |
| Acknowledging a mistake | `You're right — I got that wrong. Here is the correction:` | Vague apology + no correction |
| Investor deck headline | `Mid-market SMEs decide three times slower than their data should allow.` (claim with implied evidence) | `We help enterprises unlock growth through digital transformation.` (MBA-deck-cadence) |
| Dossier opening line | `Holistika builds the discipline that makes data-informed decisions reproducible.` | `Holistika is a leading provider of innovative data solutions.` (template-vendor language) |

## 5. Patterns to refuse — corporate-MBA jargon, performative English, and template filler

Anchored in `voice_is_not` (Performative / Vague / Jargon-heavy) per [`BRAND_DO_DONT.md`](BRAND_DO_DONT.md). The EN refuse-list is structurally distinct from FR/ES: EN's failure mode is **MBA-deck jargon** + **template-vendor language** + **LLM-tone tics**, not anglicism (the language is the source).

### 5.1 MBA-deck jargon to reject

| Jargon (avoid) | Plain-English replacement | Rationale |
|:---|:---|:---|
| `leverage synergies` | `combine [the two things]` | The two-word combo signals MBA-deck; the underlying claim is usually empty |
| `bandwidth` (as a capacity metaphor) | `availability` or `time` | Stack-jargon repurposed; reads as substituting metaphor for concreteness |
| `circle back` | `come back to this` or state when | Vague-time language; signal-of-no-decision |
| `unpack` (as a verb for "explain") | `walk through` or `explain` | LLM-default verb; specific to consultancy / coaching cadence |
| `actionable insights` | `concrete recommendations` or `usable findings` | Two-word combo signals MBA-deck; the noun "insight" is fine alone |
| `value-add` (noun) | `the value` or specify the benefit | Stack-vendor jargon |
| `low-hanging fruit` | the specific opportunity, named | Cliché tells the reader you don't know what the specific opportunity is |
| `move the needle` | `change [the specific metric]` | MBA-deck filler; demand the specific metric |
| `at scale` | `for [N] customers` or `across [N] units` (concrete) | Acceptable when the scale is named; refused when used as MBA-deck adjective |
| `optimise / optimisation` (as a vague verb) | the specific operation (`reduce`, `consolidate`, `automate`) | Acceptable in technical contexts; refused when the verb does no work |
| `transformation` (as a noun for "change") | the specific change | Investor-deck cadence; reads cold |
| `holistic` (as a marketing adjective) | the specific scope | Ironic given the brand name; refused unless used precisely (covering all axes named) |
| `seamless` | the specific friction removed | LLM-default adjective; reads as marketing-fluff |
| `cutting-edge` / `state-of-the-art` | the specific technical claim | Vendor-template language |
| `mission-critical` | name the consequence of failure | MBA-deck filler |
| `next-generation` | the specific advance | Vendor-template language |
| `enterprise-grade` | the specific reliability claim | Stack-vendor language |
| `best-in-class` | a specific benchmark | Vendor-template language |
| `industry-leading` | a specific position with citation | Vendor-template language |
| `world-class` | a specific quality claim | Vendor-template language |
| `seasoned veteran` | years of experience + domain | Recruiter-template language |
| `synergy` | the specific combination | Empty word in 99% of contexts |
| `paradigm shift` | the specific change | Empty in most contexts |
| `low-touch / high-touch` | name the operator effort | Stack-vendor jargon |
| `disrupt` (transitive verb) | the specific change to the incumbent | Investor-deck cadence; over-used |
| `pivot` (as a verb for "change") | name the change | Investor-deck cadence |
| `iterate` (with no object) | iterate on what | Vague-engineering jargon |
| `align stakeholders` | name the decision being made | MBA-deck filler |
| `solutioning` | `solving` or `designing` | Verb-from-noun construction reads template |
| `operationalise` | `make operational` or `put into production` | Verb-from-noun construction reads template |
| `productise` | `turn into a product` | Verb-from-noun construction reads template |
| `incentivise` | `give incentives` or `motivate` | Verb-from-noun construction reads template (UK spelling here; US: `incentivize`) |

### 5.2 Performative English to reject

- **Performative humility:** `I'd be honoured to collaborate with you` → use `Happy to collaborate.` (warm but not performative).
- **Performative gratitude:** `Thank you so much for your time and your thoughtful attention` → use `Thanks for the time.`
- **Performative deference:** `I'm reaching out to you regarding...` → use `I'm writing about...` or just lead with the substance.
- **Vague timeframes:** `I'll get back to you as soon as possible` → state when (`I'll come back Friday before 6 pm CET.`).
- **Performative apology:** `I want to sincerely apologise for the inconvenience this may have caused.` → use `Sorry about that.` (sincere because brief).
- **Performative enthusiasm:** `I'm super excited to share...` / `I'm thrilled to...` → drop the adjective; say what the news is.
- **Performative listening:** `I hear you` (without acting on what was heard) → acknowledge the specific point + state action.

### 5.3 Template-vendor filler to refuse

- `In light of the above...` → just say what's next (`Given that, ...` or just lead with the next thing).
- `It is our pleasure to inform you that...` → `Glad to share...` or just lead with the news.
- `Please do not hesitate to reach out` → just `Reach out anytime` (omit the negation).
- `We are committed to providing world-class service` → state the specific commitment.
- `Going forward, we will...` → just state what you will do.
- `As per our previous conversation...` → `In our last call, we...` or cite the specific point.
- `Touching base` → just state the purpose (`Quick update`, `Sharing the doc`).
- `Just wanted to follow up` → state what's pending (`The X is still pending. Can you confirm?`).
- `Hope this finds you well` → drop entirely; lead with the substance.
- `As discussed` → cite the specific thing discussed.

## 6. Salutation matrix — quick reference

| Recipient | Salutation | Closing |
|:---|:---|:---|
| First contact, US prospect | `Hi [First Name],` | `Best,` |
| First contact, UK prospect | `Hello [First Name],` | `Kind regards,` |
| First contact, EU-EN prospect | `Hello [First Name],` | `Kind regards,` |
| First contact, advisor/regulator (UK) | `Dear [First Name],` | `Yours sincerely,` (named) / `Yours faithfully,` (unnamed) |
| First contact, advisor/regulator (US) | `Dear Mr./Ms. [Last Name],` | `Best regards,` |
| Ongoing peer rapport | `Hi [First Name],` | `Best,` / `Best wishes,` |
| Internal Holistika (EN speakers) | `Hi [First Name],` or `[First Name],` | `Thanks,` or no closer |
| Last-name-only known | `Dear Sir/Madam,` (UK) / `Dear Mr./Ms. [Last Name],` (US) | `Yours faithfully,` (UK) / `Best regards,` (US) |
| Press | `Hello [First Name] [Last Name],` | `Kind regards,` |

## 7. How the composer uses this

When `language_preference: en` resolves at Layer 4:

1. The composer's draft scaffold (status: draft; frontmatter; "Layer 4 — Eloquence" TODO) remains in English — and since EN is the scaffolding language, the composer-default authoring **is** the EN canonical.
2. The operator-authored prose in Layer 4 should follow the patterns above.
3. The composer's per-discipline templates under `templates/email/` (when shipped) read these patterns to seed the salutation + closer based on `(relationship, channel, language_preference, recipient_region)` — note the additional `recipient_region` dimension (US / UK / EU-EN) which is EN-specific.

## 8. Boilerplate i18n EN copy — alignment

The boilerplate English copy (served at `holistikaresearch.com/en/` per I66 P5 deliverable) follows these patterns. The validator `validate_brand_voice_register.py` (extended at I71 P1 Pack A1) scopes to `boilerplate/messages/en.json` + `hlk-erp/messages/en.json` (when present) and flags forbidden MBA-deck jargon + performative-EN + LLM-tone tells. The EN locale is the primary scan target since EN is the LLM-default authoring language.

## 9. Maintenance

- **Append-only** for now — every real EN exchange that surfaces a new pattern (UK / US / EU-EN regional variation, jargon to refuse, register edge case) gets a one-paragraph entry under §4 / §5.
- **Source citation:** when a pattern comes from a real exchange, cite the GOI/POI `ref_id` and the date. Real names + raw transcripts stay off-repo per [`SOP-HLK_TRANSCRIPT_REDACTION_001.md`](../../People/Compliance/SOP-HLK_TRANSCRIPT_REDACTION_001.md).
- **Annual review** with the Brand Manager in lockstep with [`BRAND_VOICE_FOUNDATION.md`](BRAND_VOICE_FOUNDATION.md) (D-IH-17 cadence).
- **Trigger for off-cycle review:** new EN regional market (US-first commercial reality; UK public-sector engagement; AU/NZ market); operator-flagged drift; new sub-mark-specific EN voice need (e.g., Holistika Tech Lab EN with developer-grade register).

## 10. Open follow-ups (deferred to future initiative)

These EN-specific patterns are **not** within I71 P1 scope; they are noted here as discoverable open work:

- **US-EN vs UK-EN vs EU-EN regional split-out into sub-canonicals** — currently consolidated; split if commercial reality demands per-region register precision.
- **Technical-developer EN register** (Tech Lab sub-mark; developer-facing API docs + repo READMEs + Stack Overflow-style answers) — deferred to a Tech-Lab-specific canonical.
- **Investor-pitch EN register sub-canonical** (one-pager + dossier + deck-specific calibration) — currently covered by I66 P6 deck templates; sub-canonical-extract deferred.
- **Cross-pollination with AI-tone-tells** — the §5.1 MBA-deck jargon list overlaps with `BRAND_LLM_TONE_TELLS.md` §3. A consolidation initiative could unify the two surfaces; deferred.

## 11. Related canonicals

- [`BRAND_VOICE_FOUNDATION.md`](BRAND_VOICE_FOUNDATION.md) — language-agnostic charter + archetype + pillars.
- [`BRAND_FRENCH_PATTERNS.md`](BRAND_FRENCH_PATTERNS.md) — the FR canonical equivalent (parallel structure).
- [`BRAND_SPANISH_PATTERNS.md`](BRAND_SPANISH_PATTERNS.md) — the ES canonical equivalent (parallel structure).
- [`BRAND_REGISTER_MATRIX.md`](BRAND_REGISTER_MATRIX.md) — `(relationship, channel) → register` lookup (auto-rendered).
- [`BRAND_DO_DONT.md`](BRAND_DO_DONT.md) — voice IS / IS NOT (locale-agnostic).
- [`BRAND_JARGON_AUDIT.md`](BRAND_JARGON_AUDIT.md) — jargon-free rule (locale-agnostic; this canonical's MBA-deck table is its EN-specific instantiation).
- [`BRAND_COPYWRITING_DISCIPLINE.md`](Copywriter/canonicals/BRAND_COPYWRITING_DISCIPLINE.md) — the 7 AI-tone tic families (locale-agnostic; the validator pack at I71 P1 Pack A1 cross-references both this canonical and the discipline document).
- [`BRAND_LLM_TONE_TELLS.md`](BRAND_LLM_TONE_TELLS.md) — sibling anti-LLM-tone catalog (EN-corporate-LLM patterns; strict-day-1 severity).
- [`SOP-HLK_LOCALISATION_001.md`](../../Tech/System%20Owner/SOP-HLK_LOCALISATION_001.md) — locale policy (this file's authoring triggers SOP-HLK_LOCALISATION §3 update on EN-default-locale-policy).
- [`SOP-HLK_TRANSCRIPT_REDACTION_001.md`](../../People/Compliance/SOP-HLK_TRANSCRIPT_REDACTION_001.md) — redaction discipline.
- Cross-program glossary §"Voice register": [`docs/reference/glossary-cross-program.md`](../../../../../../reference/glossary-cross-program.md).
- I71 P1 plan: [`.cursor/plans/i71_p1_pack_a1_brand_voice_register_bcb06a90.plan.md`](../../../../../../../.cursor/plans/i71_p1_pack_a1_brand_voice_register_bcb06a90.plan.md).
- I71 P1 evidence sweep: [`docs/wip/planning/71-cicd-discipline-and-aiops-baseline-maturity/reports/p1-evidence-sweep-2026-05-14.md`](../../../../../../wip/planning/71-cicd-discipline-and-aiops-baseline-maturity/reports/p1-evidence-sweep-2026-05-14.md).
