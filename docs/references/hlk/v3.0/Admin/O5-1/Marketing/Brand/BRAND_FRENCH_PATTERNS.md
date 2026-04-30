---
language: en
status: stub
sop_id: BRAND-FRENCH-PATTERNS-001
role_owner: Brand Manager
area: Marketing / Brand
entity: Holistika Research
authority: Founder + Brand Manager
last_review: 2026-04-30
---

# BRAND_FRENCH_PATTERNS — French brand voice rules (stub)

> **Status: stub.** This file exists so French is discoverable as a locale option throughout the canonical surfaces (validator, frontmatter, sibling derivation), but **none of its rules are binding yet**. The first real French external deliverable will trigger a focused initiative that promotes this file from stub to canonical.

## 1. Why a stub?

Per [`SOP-HLK_LOCALISATION_001.md`](../../Tech/System%20Owner/SOP-HLK_LOCALISATION_001.md) §7, the canonical brand-voice rules per locale are authored when a real external deliverable forces the conversation (so the rules emerge from a concrete artifact rather than from theoretical brand guidelines). Today there is no FR external deliverable; therefore there are no binding FR rules. The stub keeps the surface discoverable — `language: fr` is a recognised value; the frontmatter validator does not reject it; the locale-derivation pipeline can target FR — without committing to authoring work.

## 2. Placeholder principles (informational)

Until promoted to canonical, the founder may use the following as a working baseline (subject to change at first real authoring session):

- **Address register** — Use the formal "vous" by default; switch to "tu" only after the recipient initiates it.
- **Tone** — Holistika's French voice mirrors the EN + ES baseline: precise, minimal jargon, peer-grade rather than salesy.
- **Brand signature** — `Holística Research` (with the accent) where space allows; otherwise `Holistika Research`.
- **Closer** — `Cordialement,` (formal) is the default; `À bientôt,` (warm) when the relationship is established.
- **Opener** — `Bonjour [Prénom],` (formal); `Salut [Prénom],` only when warm.

## 3. What promoting this file to canonical looks like

When the first FR deliverable lands:

1. A focused initiative bootstraps under `docs/wip/planning/<NN>-brand-french-canonical/`.
2. The deliverable's prose drives the rules: opener, closer, register, peer-vs-formal patterns, callout phrasing, jargon allow-list per the existing [`BRAND_JARGON_AUDIT.md`](BRAND_JARGON_AUDIT.md) framework.
3. This file's `status:` flips to `active`; placeholder principles are replaced or refined.
4. SOP-HLK_LOCALISATION_001.md §3 stub note is updated.
5. CHANGELOG records the promotion.

Until then, this file should not be cited as authoritative.

## 4. Cross-references

- [`BRAND_VOICE_FOUNDATION.md`](BRAND_VOICE_FOUNDATION.md) — locale-agnostic foundation
- [`BRAND_SPANISH_PATTERNS.md`](BRAND_SPANISH_PATTERNS.md) — the ES canonical equivalent (exemplar)
- [`BRAND_DO_DONT.md`](BRAND_DO_DONT.md) — locale-agnostic do/don't list
- [`BRAND_JARGON_AUDIT.md`](BRAND_JARGON_AUDIT.md) — jargon-free rule (applies to all locales)
- [`SOP-HLK_LOCALISATION_001.md`](../../Tech/System%20Owner/SOP-HLK_LOCALISATION_001.md) — locale policy
