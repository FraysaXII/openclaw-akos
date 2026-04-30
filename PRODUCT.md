# PRODUCT — Holística Research

> **Bridge file for Impeccable Style** (`.cursor/skills/impeccable/`). Per [`SOP-HLK_TOOLING_STANDARDS_001.md`](docs/references/hlk/v3.0/Admin/O5-1/Tech/System%20Owner/SOP-HLK_TOOLING_STANDARDS_001.md) §3.7, this file is a **thin redirect** to canonical brand SSOT under `docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/`. It does **not** duplicate brand content. Impeccable skills MUST read the canonical files before any command.

## Canonical brand SSOT (authoritative)

Every Impeccable command (`/critique`, `/polish`, `/audit`, `/shape`, `/craft`, etc.) operating on AKOS surfaces MUST consume:

- **Voice charter, archetype, narrative pillars** → [`docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_VOICE_FOUNDATION.md`](docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_VOICE_FOUNDATION.md)
- **Visual identity, design tokens, typography, hero gradient, layout primitives** → [`docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_VISUAL_PATTERNS.md`](docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_VISUAL_PATTERNS.md)
- **Voice IS / IS NOT, do/don't pairs** → [`docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_DO_DONT.md`](docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_DO_DONT.md)
- **Register matrix** (relationship × channel → tonal register) → [`docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_REGISTER_MATRIX.md`](docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_REGISTER_MATRIX.md)
- **Spanish-language patterns** (real exchanges, salutations, register matching) → [`docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_SPANISH_PATTERNS.md`](docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_SPANISH_PATTERNS.md)
- **Jargon audit (forbidden tokens externally)** → [`docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_JARGON_AUDIT.md`](docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_JARGON_AUDIT.md)

## Audience and product context (one-pager — full detail in the canonical files above)

**Who is the product for.** Three audiences served by the same artifact: ENISA legal advisers (Spanish, peer-consulting register, *tú* form, mixed warm + structured), ENISA / startup-certification reviewers (institutional but compelling), and investor-style readers (concrete proof, real numbers, no fluff). Read [`docs/wip/planning/28-investor-style-company-dossier/deck-brief.md`](docs/wip/planning/28-investor-style-company-dossier/deck-brief.md) for the full audience matrix.

**What we are.** Holística Research designs operating systems for companies that need to order their operation before they scale. Three lines: applied research, business engineering, productized knowledge software (KiRBe). Internal-first validation: we run our own products before we sell them. Five concrete production deliveries acknowledged in [Apéndice C of the appendix dossier](docs/references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_evidence/dossier_es.md).

**Brand voice in three words** (from `BRAND_VOICE_FOUNDATION.md`): rigorous, structured, plain. The voice charter: *"Holística speaks as the rigorous peer who removes uncertainty without performing expertise."* Plain words externally; jargon stays internal — that's the operational rule per `BRAND_JARGON_AUDIT.md`.

**What the interface should feel like.** Calm, trustworthy, fast. Operator confidence over flash. Cream-warm light surfaces; deep slate dark hero bands; teal `hsl(168 55% 38%)` and amber `hsl(38 80% 50%)` accents (never both as full backgrounds — they are signal devices). Inter typography. Generous whitespace. Numbered section indicators (`01` / `02`) instead of decorative ornaments.

**Visual references** (governed): the production marketing site sourced verbatim into [`BRAND_VISUAL_PATTERNS.md`](docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_VISUAL_PATTERNS.md). The Holística monogram and wordmark live at `c:\Users\Shadow\cd_shadow\root_cd\boilerplate\public\` (operator workstation hint; canonical reference is the `BRAND_VISUAL_PATTERNS.md` doc).

**Anti-references** (what we explicitly are not):

- Performative consultancy: *"We are delighted to announce..."* — refused (`BRAND_DO_DONT.md`).
- Stack-jargon dump: *"FastAPI + pgvector + Cohere reranking + Logfire..."* externally — replaced with outcome statements per `BRAND_JARGON_AUDIT.md` §5.
- Stock-photography hero shots, clip-art icons, gradient backdrops as decoration, more than two accent colors per slide.
- Internal codenames externally (`AKOS`, `topic_*`, `plane`, `ADVOPS`, `GOI/POI`, `ref_id`, etc.) — full forbidden list in `BRAND_JARGON_AUDIT.md` §4.

## Register

This file is the **brand**-register surface for Impeccable: external-facing dossiers, decks, marketing pages, partner-facing material. The **product**-register surfaces (HLK ERP, KiRBe SaaS, Madeira agent UI) live in their respective product repos and have their own design SSOTs.

## AKOS precedence rule (non-negotiable)

If an Impeccable command's suggestion conflicts with `.cursor/rules/akos-*.mdc` (governance, planning traceability, asset classification, jargon audit, brand foundation), the AKOS rule wins. In practice:

- Copy edits suggested by Impeccable MUST pass `BRAND_JARGON_AUDIT.md` §4 before any commit.
- Visual / token suggestions MUST use names from `BRAND_VISUAL_PATTERNS.md` §1; raw hex codes are forbidden when a token exists.
- Layout / motion suggestions stay phase-scoped per `akos-planning-traceability.mdc`; one commit per phase.

## How Impeccable consumes this file

The loader at `.cursor/skills/impeccable/scripts/load-context.mjs` reads `PRODUCT.md` + `DESIGN.md` at the repo root and passes their content into every command. This file is intentionally short and points outward — Impeccable's commands resolve the deep brand truth via the links above.

## Cross-references

- [`SOP-HLK_TOOLING_STANDARDS_001.md`](docs/references/hlk/v3.0/Admin/O5-1/Tech/System%20Owner/SOP-HLK_TOOLING_STANDARDS_001.md) §3.7 — Impeccable governance contract
- [`DESIGN.md`](DESIGN.md) — sister bridge file for visual / token / typography context
- `.cursor/skills/impeccable/SKILL.md` — Impeccable entry skill (loaded via Cursor agent skills)
