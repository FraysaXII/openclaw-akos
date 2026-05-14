---
language: en
status: active
sop_id: BRAND-LLM-TONE-TELLS-001
role_owner: Brand & Narrative Manager
area: Marketing
entity: Holistika Research SL
program_id: shared
topic_ids:
  - topic_brand_voice
artifact_role: canonical
intellectual_kind: brand_asset
authority: Founder + Brand Manager + Copywriter
last_review: 2026-05-14
ssot: true
authored: 2026-05-14
companion_to:
  - BRAND_VOICE_FOUNDATION.md
  - BRAND_ENGLISH_PATTERNS.md
  - BRAND_FRENCH_PATTERNS.md
  - BRAND_SPANISH_PATTERNS.md
  - ../Copywriter/canonicals/BRAND_COPYWRITING_DISCIPLINE.md
---

# BRAND_LLM_TONE_TELLS — Anti-LLM-tone catalog (EN-primary)

> **Status — Active (Initiative 71 P1; minted as a Round 3 brand-DNA addition to Pack A1). Severity: strict-day-1** per operator override at C-71-8 (the conundrum-resolution gate during plan finalization). This catalog is the load-bearing surface for Layer 8 of the brand voice register validator. Patterns flagged here **fail** the release gate on day one of I71 P1's commit; soft-30-day default was rejected in favor of immediate enforcement because the operator's lived experience is that LLM-tone smuggles into deliverables faster than the validator's annual review cycle can chase.

This canonical is **complementary** to `BRAND_COPYWRITING_DISCIPLINE.md` §2 (the 7 AI-tone tic families):

- The discipline catalog (`COPYWRITING_DISCIPLINE.md` §2) lists **structural tics** (contrastive sentence shapes; chained negation-affirmation; triadic abstract-noun stacks; false-singularity epigrams; repeated openings; instruction-echo).
- This catalog (`LLM_TONE_TELLS.md`) lists **lexical tics** (specific word + phrase choices that telegraph LLM authorship even when the sentence structure is otherwise clean).

A given LLM-authored passage typically exhibits both — but discipline-level surgery on the structure does not fix the lexicon, and vice versa. Validator coverage is the union.

## 1. The thesis

LLM-authored EN-corporate prose has a **lexical signature**: a small set of high-frequency LLM-default words and phrases that humans use rarely outside MBA-deck contexts. Even when the prose is grammatically clean, the lexical signature reads as automated because:

1. **Frequency-amplification.** The LLM-default training distribution amplifies a few tokens (`delve`, `meticulous`, `tapestry`, `landscape`, `realm`, `journey`, `unlock`, `transform`) into a much higher per-sentence rate than human writers exhibit.
2. **Hedge-cadence.** LLMs hedge with `it is important to note that`, `it should be noted`, `it is worth noting`, `crucially`, `notably`, `importantly` — at frequencies that human technical writers do not match.
3. **Adjective-stacking.** LLMs stack adjectives in pairs (`robust and scalable`, `comprehensive and intuitive`, `seamless and efficient`) at a rate that human prose does not match.
4. **Coda-cadence.** LLMs close paragraphs with summary-cadence sentences (`In conclusion,`, `In summary,`, `Overall,`, `Ultimately,`) at a rate that exceeds human technical writing.
5. **Tri-cadence headers.** LLMs default to triadic header structures (Plan / Build / Scale; Discover / Design / Deploy; Strategy / Execution / Outcomes) where the triad is filler rather than load-bearing.

Holistika prose **refuses** the lexical signature even when the content is otherwise correct. The validator at I71 P1 Pack A1 Layer 8 enforces this refusal automatically.

## 2. Severity classification

Each pattern in §3-§7 below carries one of three severities. The validator's Layer 8 default is **error**; per-token soft-mode is available via `register-pack.yml`.

- **error** — release gate fails on any hit. Used for the most LLM-default tokens that have direct human-prose replacements with no ambiguity (e.g., `delve into`, `it is important to note`, `tapestry`).
- **warning** — release gate logs but does not fail. Used for tokens that may be legitimate in some contexts (e.g., `landscape` is fine in real-estate, problematic in MBA-deck).
- **info** — release gate logs at debug verbosity only. Used for tokens that warrant operator awareness without blocking (e.g., `journey` is sometimes the right metaphor; over-use in onboarding flows is the actual problem).

The C-71-8 verdict (operator override; strict-day-1) means the validator treats **error**-severity tokens as immediate FAIL, not soft-INFO. The 30-day soft window is **not** the default.

## 3. LLM-default verbs (lexical tells)

| Token | Severity | Plain replacement | Rationale |
|:---|:---:|:---|:---|
| `delve into` | error | `look at`, `study`, `examine`, `dig into` | One of the strongest LLM-tells in 2024-2026 EN-corporate prose. |
| `unpack` (transitive, for "explain") | error | `walk through`, `explain`, `break down` | LLM-default verb when the content is conceptual. |
| `unlock` (transitive, for "enable") | warning | `enable`, name the specific outcome | Acceptable in physical contexts; LLM-default in B2B-marketing. |
| `leverage` (transitive verb, non-lever) | error | `use`, `apply`, `draw on` | MBA-deck adjacent; reads automated. |
| `harness` (for "use") | warning | `use`, `apply` | LLM-default for tech / energy contexts. |
| `tap into` (transitive, for "use") | warning | `use`, `draw on` | LLM-default verb. |
| `revolutionise / revolutionize` | warning | the specific change | Marketing-fluff. |
| `transform` (vague) | warning | the specific change | LLM-default verb at end-of-sentence; refused when the object is unnamed. |
| `streamline` | warning | the specific friction removed | LLM-default verb. |
| `optimise / optimize` (no object) | warning | the specific operation | Acceptable when paired with a specific metric. |
| `empower` (for "enable") | warning | `let`, `enable` | LLM-default verb for B2B-marketing. |
| `embark on` (a journey / process) | warning | `start`, `begin` | LLM-default phrasal verb. |
| `navigate` (a domain / landscape) | warning | the specific operation | LLM-default verb when the object is abstract. |
| `foster` (collaboration / understanding) | warning | `build`, `support`, `create` | LLM-default verb in HR + community contexts. |
| `cultivate` (relationships / culture) | warning | `build`, `grow` | LLM-default verb in HR + leadership contexts. |

## 4. LLM-default nouns (lexical tells)

| Token | Severity | Plain replacement | Rationale |
|:---|:---:|:---|:---|
| `tapestry` (of features / experiences / etc.) | error | a specific noun (`set`, `range`, `collection`) | LLM-tic in 2024-2026 EN-corporate prose. |
| `landscape` (of solutions / industry / market) | warning | `market`, `sector`, `industry` | Acceptable in geography; LLM-default in MBA-deck. |
| `realm` (of possibility / business / etc.) | error | drop or replace with the specific domain | LLM-tic. |
| `journey` (customer / digital / transformation) | warning | the specific process | LLM-default when the journey is unnamed. |
| `paradigm` | warning | the specific change | LLM-default abstract noun. |
| `synergy / synergies` | error | name the specific combination | MBA-deck adjacent; reads automated. |
| `ecosystem` (of partners / tools) | warning | the specific set | LLM-default abstract noun. |
| `framework` (vague) | warning | the specific approach | Acceptable in technical contexts; LLM-default in MBA-deck. |
| `paradigm shift` | error | the specific change | MBA-deck cliché. |
| `value proposition` | warning | what the offering does | MBA-deck term; acceptable in finance-deck only. |
| `pain point` | warning | the specific problem | MBA-deck term; over-used in B2B-marketing. |
| `north star` (metric / vision) | warning | the specific goal | LLM-default abstract metaphor. |
| `golden thread` | warning | the specific connection | LLM-default metaphor. |
| `single pane of glass` | warning | the specific unified view | LLM-default IT-marketing metaphor. |
| `holistic` (as adjective) | warning | the specific scope | Ironic given the brand name; refused unless precise. |

## 5. LLM-default adjectives (lexical tells)

| Token | Severity | Plain replacement | Rationale |
|:---|:---:|:---|:---|
| `meticulous` | warning | `careful`, `thorough`, name the specific care | LLM-tic; over-used adjective. |
| `robust` (for "good") | warning | the specific reliability claim | LLM-default adjective; vague. |
| `seamless` | warning | the specific friction removed | LLM-default adjective; vague. |
| `intuitive` (for "easy") | warning | the specific UX claim | LLM-default adjective. |
| `comprehensive` (for "complete") | warning | the specific scope | LLM-default adjective. |
| `cutting-edge` | warning | the specific technical claim | Vendor-template adjective. |
| `state-of-the-art` | warning | the specific technical claim | Vendor-template adjective. |
| `world-class` | warning | a specific quality claim | Vendor-template adjective. |
| `bespoke` (for "custom") | warning | `custom`, the specific adaptation | LLM-default adjective. |
| `tailored` (for "custom") | warning | `custom`, the specific adaptation | LLM-default adjective. |
| `crucial` | warning | drop or use sparingly | LLM-default emphasis-adjective. |
| `pivotal` | warning | drop or use sparingly | LLM-default emphasis-adjective. |
| `vibrant` (community / culture / ecosystem) | warning | the specific quality | LLM-default community-adjective. |
| `dynamic` (team / environment) | warning | the specific quality | LLM-default HR-adjective. |
| `transformative` (impact / change) | warning | the specific change | LLM-default investor-deck adjective. |

## 6. LLM-default hedge / coda / cadence phrases

| Phrase | Severity | Plain replacement | Rationale |
|:---|:---:|:---|:---|
| `It is important to note that...` | error | just state the noted thing | LLM hedge-cadence; reads as automated. |
| `It should be noted that...` | error | just state the noted thing | LLM hedge-cadence. |
| `It is worth noting that...` | error | just state the worthwhile thing | LLM hedge-cadence. |
| `Crucially,` (sentence-opener) | warning | drop or use sparingly | LLM hedge-cadence. |
| `Notably,` (sentence-opener) | warning | drop or use sparingly | LLM hedge-cadence. |
| `Importantly,` (sentence-opener) | warning | drop or use sparingly | LLM hedge-cadence. |
| `In conclusion,` (coda) | warning | drop entirely or restate the key claim | LLM coda-cadence; rarely needed. |
| `In summary,` (coda) | warning | drop entirely | LLM coda-cadence. |
| `Overall,` (coda) | warning | drop or replace with the specific takeaway | LLM coda-cadence. |
| `Ultimately,` (coda) | warning | drop or replace | LLM coda-cadence. |
| `To put it simply,` | warning | drop and just put it simply | LLM hedge-cadence. |
| `That said,` (sentence-opener overused) | warning | use sparingly | LLM cadence-tic. |
| `It's worth mentioning that...` | warning | just state the worthwhile thing | LLM hedge-cadence. |
| `Furthermore,` (sentence-opener) | warning | drop or replace with `And` | LLM cadence-tic. |
| `Moreover,` (sentence-opener) | warning | drop or replace with `And` | LLM cadence-tic. |
| `In essence,` | warning | drop or restate | LLM coda-cadence. |

## 7. LLM-default constructions (sentence-level structures)

| Construction | Severity | Plain replacement | Rationale |
|:---|:---:|:---|:---|
| `not just X, but also Y` | warning | `X and Y` | LLM amplifier-cadence; over-used. |
| `more than just X` | warning | `X and more`, name the more | LLM amplifier-cadence. |
| `whether you're X or Y, ...` | warning | name the specific audiences | LLM template for second-person address. |
| `at the heart of [our X] is [Y]` | warning | just state Y | LLM marketing-cadence. |
| `we believe that...` (followed by an opinion) | warning | state the opinion directly | LLM hedge-cadence. |
| `our mission is to...` | warning | what the company does | LLM mission-statement-cadence. |
| `as the world becomes increasingly [X], ...` | warning | name the specific change | LLM intro-cadence. |
| `in today's fast-paced [X] landscape, ...` | error | name the specific market shift | LLM-cliché intro-cadence. |
| `in an era of [X], ...` | warning | name the specific market reality | LLM intro-cadence. |
| `the future of [X] is [Y]` | warning | state the specific direction | LLM coda-cadence. |
| Triadic adjective stacks (`robust and scalable and intuitive`) | warning | pick the load-bearing adjective | LLM adjective-cadence. |
| Triadic noun stacks (`Plan, Build, Scale` / `Discover, Design, Deploy`) when filler | warning | use only when each is load-bearing | LLM header-cadence. |

## 8. Per-rule allowlist mechanism

For each pattern above, the validator supports an inline allowlist comment:

- Markdown / prose: `<!-- llm-tone-allow: T-3-delve-into -->` placed on the line immediately preceding the deliberate use.
- JSON i18n message file: a sibling key with suffix `_llm_tone_allow` (e.g., `hero.title_llm_tone_allow: "T-5-meticulous"`).

Allowlist tokens map to the row's reference handle (T-<section>-<token-slug>). Operators can also downgrade per-rule severity in `Brand/canonicals/_validators/register-pack.yml` for false-positive cases without flipping the global strict-day-1 default.

## 9. Detection notes

The validator's Layer 8 implementation:

1. Scans EN-locale prose (i18n message files at `boilerplate/messages/en.json` + `hlk-erp/messages/en.json`; markdown surfaces under `docs/references/hlk/v3.0/**/canonicals/` when frontmatter `language: en` is present and the artifact is external-facing).
2. Tokenizes per-leaf-string (JSON) or per-line (markdown).
3. Matches each leaf/line against the §3-§7 catalog. Word-boundary matches by default; phrase-level matches use exact substring with case-insensitivity.
4. Emits per-hit row: `(file, json_path_or_line, locale, token, severity, replacement_template, canonical_source)`.
5. On any **error**-severity hit (strict-day-1 default), the validator returns exit 1; the release gate FAILs.

False-positive triage path: operator inspects hit; if legitimate, adds inline allowlist comment OR downgrades severity in `register-pack.yml`. The canonical catalog (this file) is the source of truth; the YAML pack carries operator overrides.

## 10. Cross-pollination with existing surfaces

Several patterns in this catalog overlap with `BRAND_ENGLISH_PATTERNS.md` §5 (MBA-deck jargon) and `BRAND_COPYWRITING_DISCIPLINE.md` §3 (anti-pattern seeds). The overlaps are intentional — this catalog is the **lexical-signature** instantiation while the others provide structural / FR-anchored / replacement-template coverage.

When patterns appear in multiple catalogs:

- This catalog (LLM_TONE_TELLS) is the SSOT for the **token list**.
- `BRAND_ENGLISH_PATTERNS.md` §5 provides the **broader register context** (peer-consulting / investor-aspirational / regulator-neutral / formal-legal tiers).
- `BRAND_COPYWRITING_DISCIPLINE.md` §3 provides the **positive-claim replacement template** for the deck-revision worked examples (SUEZ engagement).

The validator de-duplicates: each token hits exactly once even when listed in multiple catalogs.

## 11. Maintenance

- **Append-only** for now — every operator-flagged drift hit (false-positive or new pattern surfaced in real deliverables) gets a new row in the relevant §3-§7 table.
- **Source citation:** when a pattern is added because a real deliverable shipped with it, cite the engagement-id and the deliverable path (operator-private; cite `ref_id` only).
- **Annual review** with the Brand Manager + Copywriter in lockstep with `BRAND_COPYWRITING_DISCIPLINE.md` (joint cadence).
- **Trigger for off-cycle review:** new LLM-tic identified in operator-reviewed deliverables; broad EN-LLM-tone catalog updates from external research; new sub-mark-specific severity calibration.

## 12. Open follow-ups (deferred to future initiative)

- **Multilingual extension** — the lexical-signature problem exists in FR and ES too (`approfondir`, `dévoiler`, `méticuleux`; `profundizar`, `desvelar`, `meticuloso`). Locale-specific catalogs deferred to a future initiative; FR/ES coverage at I71 P1 remains at the structural-tic level (§2 of COPYWRITING_DISCIPLINE.md).
- **LLM-version-specific calibration** — patterns evolve with LLM training distributions; catalog versioning (e.g., `gpt-4-tells`, `gpt-5-tells`, `claude-3-tells`) deferred to a future initiative.
- **In-line replacement suggestions** — currently the validator emits the replacement template; an IDE-extension or pre-commit hook that auto-applies the replacement is deferred to a future initiative.

## 13. Related canonicals

- [`BRAND_VOICE_FOUNDATION.md`](BRAND_VOICE_FOUNDATION.md) — language-agnostic charter + archetype + pillars.
- [`BRAND_ENGLISH_PATTERNS.md`](BRAND_ENGLISH_PATTERNS.md) — EN register matrix + MBA-deck jargon + performative-EN refuse-list (this canonical's foundational sibling).
- [`BRAND_COPYWRITING_DISCIPLINE.md`](../Copywriter/canonicals/BRAND_COPYWRITING_DISCIPLINE.md) §2 — 7 AI-tone structural tic families (this canonical's structural sibling).
- [`BRAND_FRENCH_PATTERNS.md`](BRAND_FRENCH_PATTERNS.md) §5 — FR-specific anglicism + performative-FR refuse-list.
- [`BRAND_SPANISH_PATTERNS.md`](BRAND_SPANISH_PATTERNS.md) §13 — ES-specific anglicism + performative-ES refuse-list.
- [`BRAND_DO_DONT.md`](BRAND_DO_DONT.md) — voice IS / IS NOT (locale-agnostic).
- [`BRAND_JARGON_AUDIT.md`](BRAND_JARGON_AUDIT.md) — jargon-free rule (locale-agnostic; superset of this catalog's §3-§5).
- I71 P1 plan: [`.cursor/plans/i71_p1_pack_a1_brand_voice_register_bcb06a90.plan.md`](../../../../../../../.cursor/plans/i71_p1_pack_a1_brand_voice_register_bcb06a90.plan.md).
- I71 P1 evidence sweep: [`docs/wip/planning/71-cicd-discipline-and-aiops-baseline-maturity/reports/p1-evidence-sweep-2026-05-14.md`](../../../../../../wip/planning/71-cicd-discipline-and-aiops-baseline-maturity/reports/p1-evidence-sweep-2026-05-14.md).
- C-71-8 conundrum resolution (strict-day-1 verdict): inline-ratify gate during plan finalization 2026-05-14; codified as `D-IH-71-K` (Round 3 scope) at P1.8.
