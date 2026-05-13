---
language: en
status: active
role_owner: Brand Manager
area: Marketing
entity: Holistika Research SL
program_id: shared
topic_ids:
  - topic_brand_visual_identity
  - topic_brand_voice
artifact_role: canonical
intellectual_kind: brand_asset
authority: Founder + Brand Manager
last_review: 2026-05-10
ssot: true
references_decisions:
  - D-12-5
  - D-12-11
references_goipoi:
  - GOI-PRT-EFA-2026
---

# BRAND_COBRANDING_PATTERN — host / guest visual + verbal pattern

> **Status — Active (Initiative 67 P12.2; founder + Brand Manager-authored 2026-05-10).** Codifies decision [D-12-11](../../../../../../wip/planning/68-cicd-discipline-and-observability-maturity/decision-log.md) (cross-program: also referenced from the SUEZ delivery plan, P12 track) — when a Holistika-led engagement is co-presented with another partnered organisation, this canonical defines how the two brand systems coexist on a single surface without dilution. Owned by the Brand Manager (CMO chain); reviewed at every new co-branded engagement and at the brand annual review.

## Why this exists

Holistika operates in a partnership ecosystem (`partner` and `collaborator` GOI/POI classes per [`GOI_POI_REGISTER.csv`](../../../../../../../docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/GOI_POI_REGISTER.csv)). Some engagements are **brought to us** by a partner who introduces, vouches for, or operates alongside us with the customer. The natural temptation in such cases is to either:

1. **Erase the partner from the surface** — which under-credits the introduction and can damage the partnership over time, or
2. **Equal-share the brand surface** — which collapses the host's identity, dilutes the customer's read of who is accountable for delivery, and creates a "joint venture" optical that neither side intended.

Neither posture serves the engagement. This canonical defines a third posture: **host / guest semantics**, where one brand owns the surface (the host) and the other appears as a present, named, but visually-deferring presence (the guest). The host is whoever is leading the delivery; the role flips per engagement. The pattern is symmetric in principle and asymmetric in any given execution.

This canonical is the cursor-side companion to slide-02 host-card spec used in the SUEZ engagement, and to any subsequent co-branded dossier, deck, proposal, or one-pager.

## 1. Host / guest semantics

### 1.1 Who is the host

The **host** is the entity that:

- Owns the **delivery scope** for the engagement (does the work, signs the engagement letter, carries the legal counterparty risk).
- Owns the **artefact** (decides cover, structure, voice, version history).
- Owns the **palette** (their brand tokens are the canvas).

The host is named first in any combined attribution. The host's monogram or wordmark sits at canonical clearspace and full scale. The host's typeface governs the surface (no font mixing).

### 1.2 Who is the guest

The **guest** is the entity that:

- **Introduced** the engagement, **vouches for** the host with the customer, or **operates** at the customer site in a complementary role.
- Has **no direct commercial counterparty** to the customer in this engagement (or has a **separate** counterparty contract that is acknowledged but not the surface).
- Is **named** on the artefact and **visible** through their own logo, but at a deferring scale.

The guest is named second. The guest's mark appears once per surface (cover-strip + slide-02 host-card on a deck; cover-strip + acknowledgement page on a dossier). Never as a watermark; never on every page.

### 1.3 The default-host rule

Holistika is the **default host** when:

- The engagement is delivered under a Holistika engagement letter or under any Holistika sub-mark (Holistika R&S / Think Big / HLK Tech Lab).
- The artefact is generated from an AKOS canonical template via [`akos/hlk_pdf_render.py`](../../../../../../../akos/hlk_pdf_render.py).
- The customer-facing audience is unfamiliar with the partner brand (default-deference posture).

Holistika is the **guest** when:

- The engagement is delivered under the partner's engagement letter or contract.
- The artefact is the partner's template adapted to acknowledge Holistika contribution.
- The customer-facing audience knows the partner brand and would be confused by Holistika fronting.

This applies at the **artefact** level. A single engagement may produce some artefacts where Holistika hosts (proposals to partner-introduced customers) and others where the partner hosts (status reports to the partner's own operating board). Each artefact picks one host posture and stays consistent with it.

### 1.4 Cover-strip attribution

Per [`BRAND_VISUAL_PATTERNS.md`](BRAND_VISUAL_PATTERNS.md) §3.1 cover-page primitive, the cover-strip carries metadata in left-to-right reading order. In a co-branded surface the strip extends from 3 fields (Programme / Date / Discipline) to 4 fields:

| Field | Value | Renderer |
|:---|:---|:---|
| Programme | Engagement code (e.g. `ENG-SUEZ-WEBUY-2026`) | host |
| Date | ISO date | host |
| Discipline | Surface kind (Présentation commerciale / Dossier / etc.) | host |
| **En collaboration avec** | Guest entity name (e.g. `EFA Académie`) | guest, named only |

The localized strip-label key is `EN COLLABORATION` (FR), `IN COLLABORATION WITH` (EN), `EN COLABORACIÓN CON` (ES). Implemented in [`akos/hlk_pdf_render.py`](../../../../../../../akos/hlk_pdf_render.py) `_COVER_STRIP_LABELS` and threaded through `_build_cover_html`'s `collaboration_partner` keyword.

When the guest's entity name does not fit (over ~22 characters), the field truncates to the partner's short-form (e.g. `EFA` instead of `EFA Académie`); the host-card on slide 02 carries the full name.

## 2. Host-card primitive

### 2.1 What the host-card is

The host-card is a **single slide-level CSS primitive** that introduces the host / guest pair on a deck or proposal cover-adjacent slide. It is named `host-card` in [`akos/hlk_pdf_render.py`](../../../../../../../akos/hlk_pdf_render.py) profile=`slides`. Layout shape:

```
+───────────────────────────────────────────────────────────────+
|  [eyebrow] Mission portée conjointement                       |
|                                                               |
|  [H2] Holistika et EFA Académie, une lecture croisée.         |
|                                                               |
|  [slide-sub] Cette mission est portée par Holistika Research  |
|  et EFA Académie. La discipline méthodologique vient de l'une, |
|  la lecture opérationnelle du quotidien vient de l'autre.      |
|                                                               |
|  +─────────────────────+  +─────────────────────+              |
|  |  [host-mark]        |  |  [guest-mark]       |              |
|  |  Holistika Research |  |  EFA Académie       |              |
|  |  Recherche, ops…    |  |  Lecture op…        |              |
|  +─────────────────────+  +─────────────────────+              |
|                                                               |
|  [slide-foot] Holistika cadre la règle, conçoit l'application |
|  logicielle, et transfère la maîtrise. EFA Académie porte la  |
|  lecture opérationnelle, valide chaque livrable au plus près  |
|  du terrain, et accompagne la continuité.                     |
+───────────────────────────────────────────────────────────────+
```

### 2.2 Host-card asymmetry rules

Both cards in the pair are **same-sized** boxes (the cards are visually peers). The asymmetry lives **inside** each card:

| Property | Host card | Guest card |
|:---|:---|:---|
| Logo placement | Centered, full clearspace; mark at 28mm height | Centered, with min-padding 8mm; mark at **0.7×** host scale (≈19mm) |
| Logo color | Full color, on host palette canvas | Mono-color, on host palette canvas (the guest mark is **flattened** to a single tone — typically the host's foreground charcoal — so that no chromatic clash arises) |
| Title | Host wordmark or entity name (e.g. *Holistika Research*) | Guest entity name (e.g. *EFA Académie*) |
| Body | One sentence describing the host's contribution to the engagement | One sentence describing the guest's contribution to the engagement |
| Border | Hairline 1px in `--border` (host palette) | Hairline 1px in `--border` (host palette) plus a 1px guest accent on the **bottom edge only** (color-bridge per §3) |

The 0.7× logo scale and the mono-flattened guest logo together encode "guest visible, host primary" without verbal hierarchy. The body sentences are equally weighted (same length, same formality, same voice register), reinforcing peer-collaboration in prose while the visuals encode the host-anchor.

### 2.3 Where the host-card lives in a deck

In a Holistika-hosted slide deck, the host-card is **slide 02** (immediately after the cover, before the substantive content begins). Putting it earlier than substantive content frames the engagement as joint-from-the-start; putting it later reads as a credit roll, which under-states the partnership. The slide-02 placement is canonical for co-branded customer-facing decks.

In a co-branded one-pager or dossier, the host-card is the **inside-cover** (page 2 of a portrait surface). The cover (page 1) carries the host's mark and the cover-strip's `En collaboration avec` field; page 2 is the host-card.

In a co-branded email or letterhead, no host-card exists; the cover-strip's 4-field attribution is the only co-branding signal.

## 3. Color-bridge rules

The single hardest decision in co-branded surfaces is the **palette**. Mixing two brand systems on one surface produces visual noise unless one of them is the canvas and the other contributes a single accent.

### 3.1 The borrow-one rule

The host's palette **is** the canvas (background, body type, primary headings, primary callouts, table chrome). The guest contributes **exactly one** color, used **exactly once or twice** on the surface, in a deliberately neutral or warm tone.

The borrowed color must satisfy three tests:

1. **Tonal compatibility.** It is a warm, neutral, or muted tone from the guest's palette. Saturated brand reds, electric blues, or signature highlights from the guest **are not eligible** — those would compete with the host's accent system.
2. **Single point of contact.** It appears on **one element** per surface: most often the host-card guest-side bottom-edge accent (per §2.2 table), or the inside-back-cover ornament rule. Never on body type, never on H1/H2, never on primary callouts.
3. **Print-safe.** Renders cleanly at 1px-3px stroke width on B&W laser print without becoming muddy or invisible.

For the SUEZ engagement (Holistika hosting EFA Académie):

- Host palette: Holistika light variant (`--background` cream-warm, `--foreground` charcoal, `--accent-primary` teal, `--accent-secondary` amber).
- Guest borrow: a single warm-cream tone lifted from the EFA Académie print materials (visible on their internal presentation deck). Approximate HSL: `hsl(35 25% 88%)` — lighter than the host's amber, neutral enough to read as "border accent" rather than "second brand". Used once: as the 1px bottom-edge of the guest-side host-card box.

### 3.2 The never-collapse rule

The host palette **never** collapses to accommodate the guest. Holistika's teal accent does not soften toward the guest's color; the guest accent does not promote toward Holistika's tokens. The palette stays **fixed at the host's spec**. The borrowed color is a guest, in the most literal sense.

If the guest's brand has no warm/neutral tone that satisfies §3.1 (e.g. a saturated-red brand with no neutral), the host-card uses the host's own `--border` token at 2px on the guest-side bottom-edge — i.e. **no color bridge**, just a slightly thicker hairline. This is preferable to importing a tone that would clash with the host palette.

### 3.3 Logo color flattening

The guest's logo, by default, is flattened to a single tone (the host's foreground charcoal `hsl(220 12% 18%)` on light surfaces, or off-white `hsl(210 15% 90%)` on dark surfaces) before placement on the host-card. This avoids the "two competing chromatic systems" effect that arises when both logos display in their full brand colors on the same surface.

Exception: when the guest's brand identity **is** primarily monochrome (no color logo exists in their identity system), the guest's logo appears in its native form. The flattening is for visually rich logos only.

The flattened guest logo asset is stored in the AKOS `_assets/` folder under the engagement's `_external_marks/` subdirectory, generated once, then referenced from the render pipeline. The original full-color guest logo is preserved in the same folder (suffix `-full-color`) for cases where the host posture flips and the guest becomes the host.

## 4. Typography deference

The host's typeface governs **all type on a host-anchored surface**. For a Holistika-hosted surface that is Inter, per [`BRAND_VISUAL_PATTERNS.md`](BRAND_VISUAL_PATTERNS.md) §2 — body, headings, captions, monogram-adjacent text, host-card, guest-card. The guest's display face does not appear, even on the guest's own card.

Rationale: typography is the most invisible carrier of brand identity. A reader does not consciously notice when two faces coexist on a page, but the surface feels noisy. Limiting to the host's face preserves the host-anchored read while logos and palette do the visible co-branding work.

If the guest's name in their own brand uses a stylized form (italic, small-caps, custom kerning), the host-card guest-card title renders the guest's name in **the host's typeface set to a similar weight** — never the guest's stylized form. The guest's logo carries the stylized identity; the host-card title is a neutral type-set rendering.

The one exception is the guest's logo asset itself, which is rendered as an image (SVG / PNG), not as type. The logo image carries whatever stylization the guest's brand requires.

## 5. Polarity-flip clause

Co-branding is symmetric in principle. A future engagement may invert the SUEZ-stage posture: EFA Académie hosts a customer-facing artefact and Holistika is the named guest. When that happens:

1. **Same primitives apply, with host and guest swapped.** EFA's palette becomes the canvas, EFA's typeface governs, EFA's logo at full clearspace, the cover-strip's `En collaboration avec` field carries `Holistika Research`, slide 02 host-card has EFA on the host side and Holistika on the guest side at 0.7× scale and mono-flattened.
2. **Holistika's borrowed color** becomes the guest accent. Per §3.1 tests, the eligible borrow tone from Holistika's palette is the muted slate `--border` (`hsl(220 8% 88%)`) — neutral and print-safe. Holistika's teal/amber are NOT eligible (too saturated; would compete with EFA's accent).
3. **Holistika's monogram is flattened** to EFA's foreground tone for the guest-card placement.
4. **The artefact lives in the EFA folder structure**, not the AKOS Think Big/Clients/ tree, since the host owns the artefact (per §1.1).

The polarity-flip clause is what makes this canonical **partnership-symmetric**. We are not encoding "Holistika hosts and partners are guests forever"; we are encoding a deference primitive that works in either direction. EFA, or any other partner, can host us with the same toolkit.

A single engagement may, over its lifecycle, switch host posture between artefacts (e.g. Holistika hosts the proposal; EFA hosts a status update to her own operating board). The polarity flip is per-artefact, not per-engagement.

## 6. Anti-patterns specific to co-branding

- **Don't equal-size the two logos at full color.** The "we are equals" optical reads as "we are confused about who delivers" — the host-anchor disappears, and the customer reads the artefact as a JV pitch, not as a vendor proposal with credible introduction.
- **Don't use both brand-systems' accents on the same surface.** Even at low intensity, two accent systems compete; the eye reads "noisy". One accent system at a time.
- **Don't watermark the guest's mark across pages.** The guest is named once (cover-strip) and shown once (host-card or inside-cover). Repeating their mark over body pages reads as cross-promotion, not collaboration.
- **Don't translate the guest's tagline into the host's voice.** If the guest brings their own tagline (e.g. an EFA tagline, an EFA mission statement), it appears verbatim on the guest-card, not paraphrased into the host's prose register. The host's voice rules the host's prose; the guest's voice rules the guest's prose. The two voices coexist within their respective scopes.
- **Don't co-brand on legal documents.** Engagement letters, MSAs, NDAs, DPAs, SOWs are not co-branded. They are **single-counterparty** documents under the host's letterhead. The partner is acknowledged in a separate addendum if needed, never on the contract face. This is a legal-clarity rule that overrides any visual-design preference.
- **Don't introduce a third brand.** If a sub-supplier or sub-partner is involved (e.g. a research-only contributor who licensed their dataset to the engagement), they are acknowledged in source-citation captions, not on the cover-strip and not on the host-card. Co-branding is a binary host / guest relation; chains of three or more brands collapse the model.

## 7. Maintenance

- **Trigger to update.** Operator-flagged co-branding decision; new partner enters the GOI/POI register with `class: partner` and starts producing customer-facing artefacts; brand-system update on either side that affects palette, typography, or logo system.
- **Annual review.** This canonical's review cadence rides on the brand annual review (per `process_list.csv` umbrella row "BRAND_LOGO_SYSTEM annual review"; co-branding review folds into the same cycle).
- **Authority for changes.** Founder (final) + Brand Manager (proposes + maintains).
- **Drift detection.** [`scripts/validate_brand_drift_gates.py`](../../../../../../../scripts/validate_brand_drift_gates.py) (proposed extension) audits the host-card primitive selectors and the cover-strip 4-field key against the renderer's emitted CSS. If a future deck commits a 3-field cover-strip on a co-branded engagement, the gate flags the omission. (Extension scope deferred to the brand-ops sweep that owns the validator; tracked in [`I66 P3 process row`](../../../../../../../docs/wip/planning/66-brand-vision-ops-sweep/master-roadmap.md).)

## 8. Cross-references

- [`BRAND_LOGO_SYSTEM.md`](BRAND_LOGO_SYSTEM.md) — logo system canonical (this canon's logo-placement rules ride on §2.5 sub-mark conventions and §3 color guardrails).
- [`BRAND_VISUAL_PATTERNS.md`](BRAND_VISUAL_PATTERNS.md) — visual tokens + typography + cover-page primitive (this canon extends §3.1 cover-page to its 4-field co-branded variant).
- [`BRAND_VOICE_FOUNDATION.md`](BRAND_VOICE_FOUNDATION.md) — voice charter (this canon's "host's voice rules host's prose" rule rides on the foundation register).
- [`BRAND_REGISTER_MATRIX.md`](BRAND_REGISTER_MATRIX.md) — register matrix (relevant for how a guest's voice is acknowledged within a host-anchored surface).
- [`BRAND_DO_DONT.md`](BRAND_DO_DONT.md) — IS / IS NOT (the §6 anti-patterns above extend the IS NOT side for co-branded contexts).
- [`akos/hlk_pdf_render.py`](../../../../../../../akos/hlk_pdf_render.py) — the renderer whose primitives realise this canonical (`host-card` CSS class, `_COVER_STRIP_LABELS` localized keys, `_build_cover_html` `collaboration_partner` keyword, `{{GUEST_LOGO_URI}}` substitution).
- [`tests/test_render_dossier.py`](../../../../../../../tests/test_render_dossier.py) — drift safeguard for renderer-emitted selectors (extends to assert `.host-card` and `.method-anchors` selectors when co-branded surfaces are produced).
- [`GOI_POI_REGISTER.csv`](../../../../../../../docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/GOI_POI_REGISTER.csv) — partner / collaborator registry (a co-branded engagement requires the partner to have a row with `class: partner` or `class: collaborator` and a `lens: partner_engagement` notation; absence is a precondition violation).
