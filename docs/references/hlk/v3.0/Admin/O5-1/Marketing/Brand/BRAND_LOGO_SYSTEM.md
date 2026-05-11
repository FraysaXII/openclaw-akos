---
language: en
status: active
role_owner: Brand Manager
area: Marketing
entity: Holistika Research SL
program_id: shared
topic_ids:
  - topic_brand_visual
artifact_role: canonical
intellectual_kind: brand_asset
authority: Founder + Brand Manager
last_review: 2026-05-08
ssot: true
---

# BRAND_LOGO_SYSTEM — Logo audit + canonical decisions

> **Status — Active (Initiative 66 P1; founder + Brand Manager-authored 2026-05-08).** Codifies decision [D-IH-66-O](../../../../wip/planning/66-brand-vision-ops-sweep/decision-log.md#d-ih-66-o) — operator-presented four logo candidates audited and resolved into a multi-context system: one primary mark, one formal canonical wordmark, one deprecated mark, and a stylized-vs-prose split rule. Owned by the Brand Manager (CMO chain); annual review cadence in `process_list.csv` row "BRAND_LOGO_SYSTEM annual review" (I66 P3).

## 1. Audit — what the operator presented (2026-05-08)

| Candidate | Description | Operator framing |
|:---|:---|:---|
| **Hi monogram** | Compact symbol; "Hi" derived from Holistika; works at favicon scale | "What we already use in social avatars and the app icon" |
| **HOLÍSTIKA Research wordmark** | Full wordmark with diacritic on Í; formal serif-ish display lettering | "The formal version that conveys research-grade rigor" |
| **Holistika RGB-rings chromatic mark** | Three colored rings (red, green, blue overlapping) | "Older version; reads 2010s tech-startup; not consistent with the new positioning" |
| **Duplicate of Holistika RGB-rings** | Color variant of above | "Same lineage as the RGB-rings; consider both deprecated" |

## 2. Resolved canonical (per D-IH-66-O)

### 2.1 Primary mark — Hi monogram

- **Status.** Canonical. Primary mark for compact contexts.
- **Use cases.**
  - Favicon (16×16, 32×32, 96×96).
  - Social avatar (LinkedIn, X, GitHub org, Slack workspace, all platforms with circular crops).
  - App icon (`hlk-erp` PWA; future native app installs).
  - Mobile-first hero contexts (where the wordmark would not breathe).
  - Email signature compact-context.
  - One-pager bottom-strip mark.
- **Constraints.**
  - Always full-color on light surface; reverse (white) on dark surface.
  - Minimum size 16px; smaller scales prohibited.
  - Clear-space ≥ 0.5 × monogram height on all sides.
  - Never modify (no shadow, no glow, no gradient overlay, no stroke).
- **File location.** `boilerplate/public/brand/logo/hi-monogram-color.svg` + `hi-monogram-white.svg` (light + dark surface variants). Boilerplate is the upstream live source per [`BRAND_VISUAL_PATTERNS.md`](BRAND_VISUAL_PATTERNS.md); AKOS canonical mirrors via `_assets/brand/logo/`.

### 2.2 Formal canonical — HOLÍSTIKA Research wordmark (with diacritic on Í)

- **Status.** Canonical. Formal canonical wordmark for trademark filings, legal documents, formal contexts.
- **Use cases.**
  - Letterhead (top-left).
  - Business cards (front-face primary).
  - Investor + advisor + ENISA + recruiter + partner deck cover slide.
  - Legal contracts (header).
  - SiteFooter on `boilerplate` (legal block; `<small>` tag with the trademark posture line per I66 P5).
  - Press kit (canonical wordmark download).
  - Investor dossier cover (`_assets/advops/PRJ-HOL-FOUNDING-2026/`).
  - Trademark filings (EUIPO + OEPM applications per I66 P4) target this wordmark as the design + word mark.
- **Constraints.**
  - Diacritic on Í is **required** in this canonical form. Substituting plain "I" produces the prose form (see §2.4), not the canonical form.
  - Always full-color on light; reverse (white) on dark.
  - Minimum width 120px; smaller scales prohibited.
  - Clear-space ≥ 1 × cap-height on all sides.
  - Never separate "HOLÍSTIKA" from "Research" (the wordmark is the pair; using "HOLÍSTIKA" alone is not canonical).
- **File location.** `boilerplate/public/brand/logo/holistika-research-wordmark-color.svg` + `holistika-research-wordmark-white.svg`.

### 2.3 Deprecated — Holistika RGB-rings chromatic mark + duplicate

- **Status.** Deprecated. Retired from production by I66 P5 close.
- **Rationale.** Reads 2010s-era "tech startup"; doesn't carry research weight; the chromatic-rings convention is saturated in the consulting + adtech segment.
- **Transition.**
  - Existing assets that use the RGB-rings mark are inventoried by I66 P5 and replaced with the Hi monogram (compact contexts) or HOLÍSTIKA Research wordmark (formal contexts).
  - Asset directory `boilerplate/public/brand/logo/DEPRECATED/` holds historical SVGs for archive purposes only; never linked from production code.
  - No third-party site, partner deck, or vendor portal may use the RGB-rings mark after 2026-06-30. Operator-owned communication (cease-and-desist not required; standard "we've updated our brand identity" notification) for any partner using legacy assets.
- **Re-rating clause.** A future visual identity review may revive a chromatic accent system — but it will be paired with the Hi monogram or HOLÍSTIKA wordmark, not as a standalone mark. The RGB-rings as a primary identity is closed.

### 2.4 Stylized-vs-prose split rule (D-IH-66-O canonical)

Stylized **and** plain forms coexist for legitimate reasons. Use the stylized form in brand contexts, the plain form in legal prose.

| Context | Form |
|:---|:---|
| Brand assets, decks, hero sections, landing pages, marketing materials | **Stylized:** Hi monogram (compact) or HOLÍSTIKA Research wordmark (formal) |
| Legal contracts, MSA, SOW, NDA, DPA, terms-of-service prose | **Plain:** "Holistika Research SL" (no diacritic; Latin-1 only) |
| Email signature line | **Stylized:** Hi monogram inline (96px height) + plain "Holistika Research SL · Madrid" beneath in plain text |
| Body prose on `boilerplate` (any prose paragraph that names the company) | **Plain:** "Holistika" (umbrella brand) or "Holistika Research SL" (legal entity, when legal context required) |
| Body prose on `hlk-erp` (operator surface) | **Plain:** "Holistika" (umbrella brand) — the chrome already carries the visual mark |
| Investor dossier prose | **Plain in body**, **stylized on cover + section dividers** |
| Press kit canonical text-form | **Plain:** "Holistika Research SL is a Madrid-registered Sociedad Limitada operating under the umbrella brand Holistika." |

Reason: stylized prose with diacritic-Í in monospaced legal contracts becomes unreadable in B&W print; plain prose preserves contractual clarity; the brand identity remains anchored to the stylized canonical for visual contexts.

### 2.5 Sub-mark + product mark conventions

Per [`BRAND_ARCHITECTURE.md`](BRAND_ARCHITECTURE.md) Layer 3 + Layer 4:

| Mark | Stylized form | Plain prose form | Trademark scope (P4) |
|:---|:---|:---|:---|
| Holistika R&S | `Holistika R&S` (plain wordmark) | "Holistika R&S" or "Holistika Research & Strategy" | Brand sub-mark filing under Holistika Research SL ownership; Nice 35 + 42 |
| Think Big | `Think Big` (plain wordmark) | "Think Big" | Brand sub-mark filing; Nice 35 + 42 (consulting services) |
| HLK Tech Lab | `HLK Tech Lab` (plain wordmark) | "HLK Tech Lab" | Brand sub-mark filing; Nice 9 + 42 (technology + software services) |
| MADEIRA | `MADEIRA` (plain wordmark; future stylization may add diacritic-styling) | "MADEIRA" | Product mark filing; Nice 9 + 42 (computer software; software-as-a-service); EUIPO + OEPM. **Risk: collision with the Portuguese island + wine region; Nice 33/39/41 are off-limits.** |
| KiRBe | `KiRBe` (mixed-case wordmark; "iRBe" lowercase to evoke "internal RBe" — internal Retrieval-augmented-generation engine; "K" capitalized) | "KiRBe" | Product mark filing; Nice 9 + 42 |
| ENVOY | `ENVOY` (plain wordmark uppercase) | "ENVOY" | Product mark filing; Nice 9 + 42 |
| MADEIRA Agent | `MADEIRA Agent` (paired wordmark; "Agent" in italic-display) | "MADEIRA Agent" | Sub-product variant; filed alongside MADEIRA |

Sub-mark + product marks **never** stand alone visually. The umbrella mark (HOLÍSTIKA Research) appears in the same surface (header / footer / sidebar) so that umbrella never disappears.

### 2.6 Co-branding (host / guest pattern)

When a Holistika-led engagement is co-presented with a partner organisation (a `partner` or `collaborator` GOI/POI row), see [`BRAND_COBRANDING_PATTERN.md`](BRAND_COBRANDING_PATTERN.md) for the canonical host/guest pattern. Summary of logo-system implications:

- The **host** (typically Holistika in a Holistika-delivered engagement) keeps full clearspace and chromatic rendering of its primary mark (Hi monogram) and / or formal canonical wordmark per §2.1 / §2.2.
- The **guest** logo appears at **0.7× host scale**, mono-flattened to the host's foreground tone (charcoal `hsl(220 12% 18%)` on light surfaces; off-white `hsl(210 15% 90%)` on dark) on the host-card slide-02 primitive and on cover-strip ornaments.
- The cover-strip extends from 3 fields to **4 fields** (Programme / Date / Discipline / `En collaboration avec`); the localized strip-label key is `EN COLLABORATION` (FR), `IN COLLABORATION WITH` (EN), `EN COLABORACIÓN CON` (ES).
- A polarity flip applies when the host posture inverts (Holistika is the guest on a partner-led artefact); same primitives, host and guest swapped. Holistika's eligible borrow tone in that case is the muted slate `--border` `hsl(220 8% 88%)` — never teal or amber.

The full host/guest semantics, host-card primitive specification, color-bridge rules, and anti-patterns live in [`BRAND_COBRANDING_PATTERN.md`](BRAND_COBRANDING_PATTERN.md).

## 3. Color + accent guardrails

Per [`BRAND_VISUAL_PATTERNS.md`](BRAND_VISUAL_PATTERNS.md):

- **Hi monogram color.** Default state: charcoal `hsl(220 12% 18%)` on light surface; warm-off-white `hsl(210 15% 90%)` on dark surface.
- **HOLÍSTIKA wordmark color.** Same as Hi monogram. The wordmark is monochromatic (charcoal or off-white); chromatic variants are forbidden.
- **Trademark-specific TM symbol placement.** Per I66 P4 trademark filings: "Holistika™" (TM after main wordmark) used in marketing materials post-application; "Holistika®" (registered symbol) used only after registration is granted in the relevant jurisdiction.

## 4. File-naming convention

```
boilerplate/public/brand/logo/
  hi-monogram-color.svg
  hi-monogram-white.svg
  hi-monogram-color@2x.png        (raster fallback, 96px)
  hi-monogram-color@4x.png        (raster fallback, 192px)
  hi-monogram-white@2x.png
  hi-monogram-white@4x.png
  holistika-research-wordmark-color.svg
  holistika-research-wordmark-white.svg
  holistika-research-wordmark-color@2x.png
  holistika-research-wordmark-white@2x.png
  DEPRECATED/
    holistika-rgb-rings-2024.svg
    holistika-rgb-rings-duplicate-2024.svg
    README.md                       (deprecation rationale + retirement timeline)
```

AKOS mirror at `_assets/brand/logo/` (canonical reference path; mirrors boilerplate live source).

## 5. Drift gate

`validate_brand_logo_usage.py` (proposed; deferred to a future initiative beyond I66 — current drift gates in P2 cover canon-token + jargon + voice register + baseline-reality, not logo-asset usage). Manual annual review per process_list row covers logo drift until automated.

`validate_brand_jargon.py` (P2) catches one related drift: any `boilerplate` rendered DOM containing "RGB rings" or referring to the deprecated mark by name flags as forbidden.

## 6. Trademark filing scope (cross-reference; details in P4)

Per [`BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md`](../../People/Legal/BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md) (rewritten I66 P1) and [`TRADEMARK_FILING_STRATEGY_2026-05.md`](../../People/Legal/TRADEMARK_FILING_STRATEGY_2026-05.md) (created I66 P4):

- **EUIPO** (one filing covers all EU member states): Holistika (umbrella, word + design), HLK Tech Lab (sub-mark, word), MADEIRA (product, word + design — design specifically for MADEIRA wordmark to differentiate from generic MADEIRA in non-relevant Nice classes), KiRBe (product, word + design), ENVOY (product, word). Think Big intentionally NOT filed at EUIPO (high collision; brand-only protection sufficient via use-in-trade in EU).
- **OEPM (Spain national)**: Holistika (national protection in Spain alongside EUIPO; national filing is faster than EUIPO and provides bridge protection during EUIPO pendency), Think Big (national-only).
- **Filing forms** (ready-to-sign per D-IH-66-C): EUIPO TM-1 (5 marks × 1 jurisdiction = 5 forms), OEPM equivalent (2 marks × 1 jurisdiction = 2 forms). Total ~7 forms in P4 deliverable.

## 7. Maintenance

- **Annual review.** `process_list.csv` row "BRAND_LOGO_SYSTEM annual review" (created I66 P3); cadence: yearly.
- **Trigger for off-cycle review.** Operator-flagged drift; new sub-mark or product brand introduction; trademark filing decision; partner / press inquiry about logo usage.
- **Authority for changes.** Founder (final) + Brand Manager (proposes + maintains).

## 8. Related canonicals

- [`BRAND_ARCHITECTURE.md`](BRAND_ARCHITECTURE.md) — Branded House architecture (defines the marks this system canonicalizes).
- [`BRAND_VISUAL_PATTERNS.md`](BRAND_VISUAL_PATTERNS.md) — visual tokens + typography + layout primitives (which this complements with logo-specific decisions).
- [`BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md`](../../People/Legal/BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md) — trademark posture (this canon's filing-scope cross-reference).
- [`BRAND_ABBREVIATIONS.md`](BRAND_ABBREVIATIONS.md) — HLK / MA / KB governance (this canon's abbreviation cross-reference).
- [`BRAND_DO_DONT.md`](BRAND_DO_DONT.md) — voice rules that complement these visual rules.
- [`BRAND_COBRANDING_PATTERN.md`](BRAND_COBRANDING_PATTERN.md) — host / guest pattern for co-branded surfaces (cross-referenced in §2.6).
- [`TRADEMARK_FILING_STRATEGY_2026-05.md`](../../People/Legal/TRADEMARK_FILING_STRATEGY_2026-05.md) (created I66 P4) — full filing strategy.
