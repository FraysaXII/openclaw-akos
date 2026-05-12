---
language: en
status: active
canonical: true
role_owner: UX Designer + PMO (joint)
classification: way_of_working
intellectual_kind: contract_canonical
ssot: true
authored: 2026-05-12
last_review: 2026-05-12
companion_to:
  - BRAND_MULTILINGUAL_CONTRACT.md
  - BRAND_DISCIPLINE_ONTOLOGY.md
  - "../UX Designer/canonicals/BRAND_UX_DESIGNER_CHARTER.md"
---

# BRAND_COUNTERPARTY_README_CONTRACT — Counterparty-facing README pattern

> Authored I70 P7 per plan section 7. Codifies the 3-rule pattern + path-portability + non-technical register for counterparty-facing READMEs at the engagement folder root. Bilingual / trilingual engagements ship 3 separate files per Conundrum 7 + D-IH-70-P + sibling `BRAND_MULTILINGUAL_CONTRACT.md` §2.

## 1. The thesis

The engagement-folder README is the counterparty's first read on opening the folder (via Drive link, GitHub link, or attached zip). It must:

1. **Read as if the counterparty owned the folder** — non-technical register; no operator-jargon; no AKOS-internal-codename references.
2. **Travel with the folder** — relative paths only; no absolute filesystem references; no GitHub-org-specific URLs that break if the folder is forked.
3. **Show, don't claim** — link directly to the customer-pack deliverables (deck.customer.fr.pdf, proposal.customer.fr.pdf, etc.); the README is a navigation surface, not a marketing surface.

## 2. The 3-rule pattern

### Rule 1 — Non-technical register

The counterparty README:

- **Never references AKOS internal codenames** (`AKOS`, `topic_*`, `plane`, `KM`, `MASTER`, `dtp_*`, etc.). Per `BRAND_JARGON_AUDIT.md` §4 + D-IH-70-I `opt-strict`.
- **Uses peer_consulting register** (Tier 1 per `BRAND_REGISTER_MATRIX.md`) by default; never academic-formal Tier 2 unless the engagement explicitly targets investor / ENISA / advisor audiences.
- **Cross-references the customer-pack documents in their natural names** (`deck.customer.fr.pdf` is fine; the operator's internal `dtp_engagement_001` reference is not).

### Rule 2 — Path portability

The counterparty README:

- **Uses relative paths only** for cross-engagement-folder references. `[`proposal.customer.fr.pdf`](_exports/proposal.customer.fr.pdf)` is correct; `[`proposal.customer.fr.pdf`](docs/references/hlk/v3.0/Think Big/Clients/2026-suez-webuy/_exports/proposal.customer.fr.pdf)` is wrong (breaks when the engagement folder is shared in isolation).
- **Avoids GitHub-org-specific URLs** for in-folder content. If the engagement is shared via Drive (most common case), GitHub URLs return 404 to the counterparty.
- **External cross-links are explicit** — when referencing the operator's GitHub for context (rare), the link reads `(operator-internal: https://github.com/FraysaXII/openclaw-akos/...)` so the counterparty understands they're crossing into operator territory.

### Rule 3 — Show-don't-claim

The counterparty README:

- **Lists the customer-pack deliverables** first — deck + proposal + tarification + Gantt are the artifacts the counterparty consumes; the README's job is to make them findable.
- **Provides 1-2 sentences per artifact** describing what it is (not what it claims). "The proposal lays out three engagement variants and recommends Variant B." beats "Holistika offers a comprehensive engagement framework."
- **Includes a closing-contact line** with a single point of contact (email + phone optional + named human per H2 brand-first naming). Never lists multiple contact points to confuse routing.

## 3. Bilingual / trilingual file structure (per BRAND_MULTILINGUAL_CONTRACT §2)

When an engagement is multilingual, the engagement-folder root carries multiple READMEs:

```
2026-<slug>/
├── README.md            (5-line pointer; lists per-language READMEs + 1-line description per language)
├── README.fr.md         (full FR; if FR is in the engagement language inventory)
├── README.en.md         (full EN; if EN is in the engagement language inventory)
├── README.es.md         (full ES; if ES is in the engagement language inventory)
└── ...
```

**The 5-line pointer `README.md`:**

```markdown
# <Engagement title>

This engagement is bilingual. Per-language READMEs:
- [README.fr.md](README.fr.md) — version française (audience client + EFA Académie partenaire)
- [README.en.md](README.en.md) — English version (advisor + investor + AKOS-internal)
```

The pointer is brand-only (no personal names per H2). Per-language READMEs may carry the engagement's collaboration metadata (e.g., `collaboration_partner: EFA Académie` per cobranding pattern) but signature / contact lines defer to the customer-pack proposal cover (per H2 ratification: signatures only on the proposal cover for engagement-letter legitimacy).

## 4. Anti-patterns (forbidden in counterparty README)

| Pattern | Why forbidden | Replacement |
|:---|:---|:---|
| Operator's full name in body prose | H2 brand-first; signatures only on proposal cover | Brand-only voice + cobranding cross-link |
| Absolute filesystem path | Breaks when folder shared via Drive in isolation | Relative path |
| AKOS codename reference | D-IH-70-I `opt-strict`; customer-facing prose forbids `AKOS` | "Holistika OS" or "the Holistika methodology" |
| Internal-jargon token (`KM`, `MASTER`, `dtp_*`, `plane`) | BRAND_JARGON_AUDIT §4 forbids in customer-facing | Plain-language equivalent |
| Multiple contact points | Confuses routing | Single named-human contact line (per H2: signature/contact line carries named humans) |
| Marketing-fluff intro paragraph | Show-don't-claim rule | List the deliverables; describe what each is |
| Tier-2 academic-formal default | Default register is Tier 1 peer_consulting | Tier 2 only for investor / ENISA / advisor explicit overrides |
| `Présentation à votre direction des...` (operator-instruction echo) | F7 AI-tone tic per BRAND_COPYWRITING_DISCIPLINE | Imperative-form claim about what the deliverable does |

## 5. Slide-legibility QA gate (extends BRAND_UX_DESIGNER_CHARTER §3)

The counterparty README passes the slide-legibility QA gate's **Counterparty gate** (gate #5):

- No operator-jargon visible to counterparty.
- Proper register tier per `BRAND_REGISTER_MATRIX.md` (Tier 1 default).
- All cross-links are relative paths (Rule 2 path-portability).
- All artifact descriptions follow show-don't-claim (Rule 3).
- Multilingual file structure honors `BRAND_MULTILINGUAL_CONTRACT` §2.

## 6. Worked example — SUEZ engagement bilingual READMEs

The SUEZ engagement (FR + EN inventory) ships:

- `2026-suez-webuy/README.md` — 5-line pointer.
- `2026-suez-webuy/README.fr.md` — full FR README (audience: SUEZ counterparty + EFA Académie partner).
- `2026-suez-webuy/README.en.md` — full EN README (audience: advisor + investor + AKOS-internal).

These are authored as a sibling commit at the engagement folder. The existing `2026-suez-webuy/README.md` (per I12 P12) is rebuilt to the new 3-file pattern.

## 7. Validator hooks (forward-link to I71)

- `validate_brand_counterparty_readme_contract.py` (NEW; reserved): confirms engagement READMEs match the 3-file pattern when `language` inventory has 2+ languages; confirms 5-line pointer schema; confirms per-language README frontmatter; runs anti-pattern table (§4) as forbidden-token sweep.

## 8. Cross-references

- Sister canonical: [`BRAND_MULTILINGUAL_CONTRACT.md`](BRAND_MULTILINGUAL_CONTRACT.md) — per-engagement language inventory + 4-surface matrix.
- Brand register: `BRAND_REGISTER_MATRIX.md` (Marketing/Brand/canonicals/).
- Brand jargon audit: `BRAND_JARGON_AUDIT.md` (Marketing/Brand/canonicals/) §4.
- Brand voice charter: `BRAND_VOICE_FOUNDATION.md`.
- Brand copywriting discipline: `BRAND_COPYWRITING_DISCIPLINE.md` (Marketing/Brand/Copywriter/canonicals/) — F7 (operator-instruction echo) tic family.
- D-IH-70-P (P3 ratification): bilingual README pattern (3 separate files).
- Conundrum 7 — bilingual README pattern resolution.
- H2 (Pre-handoff ratification): brand-first naming applied to customer-facing artifacts.
- D-IH-70-I (P3 ratification): AKOS branding hygiene `opt-strict`.
- I70 plan section 7 — full P7 deliverable spec.
- Worked example: SUEZ bilingual READMEs (sibling commit).
