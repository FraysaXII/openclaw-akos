---
language: en
status: completed
phase: P11 — Slip-off remediation + customer slide deck
engagement_slug: 2026-suez-webuy-procure-to-pay
program_id: ENG-SUEZ-WEBUY-2026
artifact_role: agent_self_checkpoint
intellectual_kind: phase_record
checkpoint_for: docs/wip/intelligence/2026-05-10-suez-webuy-procure-to-pay/
date: 2026-05-10
---

# P11 — Slip-off remediation + customer slide deck

> **Trigger.** Operator review of the customer pack delivered in P10 surfaced
> three discrete defects and one missing surface:
>
> 1. *Visual slip-off.* "Some random letters in the background" overlapping
>    the cover subtitle ("Cadrer · prototyper · transférer") on the customer
>    proposal cover.
> 2. *Content slip-off.* The literal string "proposal.fr.md" leaking into a
>    customer-facing PDF — "a massive leakage and bad UX/CX/presentation,
>    and I'm sure there are more things".
> 3. *Solution explanation gap.* The customer proposal stopped at the
>    diagnosis ("Notre lecture") and skipped to the offer ("Ce que nous
>    proposons") without a beat that says **what we are actually building**.
> 4. *Missing surface.* The operator asked for a slide-deck version of the
>    customer proposal — "It will be a PDF but a slide version of this would
>    be nice. Don't port blindly, really design for impeccable slides".

## 1. Defects, root causes, and fixes

### 1.1 Cover overlap — `proposal.customer.fr.pdf` and `tarification.customer.fr.pdf`

**Symptom.** Subtitle "Cadrer · prototyper · transférer" appeared visually
adjacent to the cover-strip labels (PROGRAMME / DATE / DISCIPLINE), giving
the impression of "random letters" overlapping the subtitle area.

**Root cause.** The hero CSS used `min-height: 297mm` with the default
`box-sizing: content-box`. Combined with 30mm + 28mm vertical padding, the
hero box was ~355mm tall on a 297mm A4 page. A `position: absolute; bottom:
24mm;` strip then rendered relative to the *box*, not the *page*, so it
landed mid-flow under the still-flowing subtitle on the visible portion of
page 1. Result: visual overlap.

**Fix shipped.** `akos/hlk_pdf_render.py` →

- `.cover-hero { height: 297mm; box-sizing: border-box; overflow: hidden; }`
  (the box is now exactly the page, deterministic).
- New wrapper `.cover-title-block { position: absolute; bottom: 65mm; }`
  carries `<h1>` + `.cover-subtitle`. The strip stays at `bottom: 24mm`.
- Deterministic gap: subtitle bottom is at y≈658pt, strip top is at y≈746pt
  → 88pt = 31 mm of clear space. Verified via `pdfplumber` text positions
  (no rasterized eyeballing).

**Verification artefact.** `pdfplumber` extract on cover page:

```
y= 537.7  Proposition
y= 583.9  d'engagement
y= 643.8  Cadrer · prototyper · transférer
... (gap of 88pt) ...
y= 746.1  PROGRAMME / DATE / DISCIPLINE
y= 763.4  ENG-SUEZ-WEBUY-2026 / 2026-05-10 / Automatisation de la demande d'achat WeBuy
```

### 1.2 Filename leakage — `cdc-feasibility-shape.fr.md`, `deck-suez-webuy.fr.md`, `proposal.fr.md`

**Symptom.** Three places in the operator pack referenced internal `.md`
filenames in customer-visible prose:

- CDC §10 "Renvois utiles" cited `discovery-questionnaire.fr.md`,
  `proposal.fr.md`, `deck-suez-webuy.fr.md` by literal filename.
- Deck slide intro cited `proposal.fr.md`, `cdc-feasibility-shape.fr.md`,
  and `sales-8-slide.deck.md`.
- Proposal §1 metadata table cited `commercial-schedule.md` by literal
  filename, plus surfaced internal cell taxonomy ("Cellules de service
  principales: 1A → 1B → 5C → 6C") with a `SERVICE_OFFERING_CATALOG`
  reference.

**Root cause.** The operator pack is canonical scaffolding inherited from
internal templates that legitimately use AKOS file references. When the
operator reviewed the rendered customer pack and noticed
"proposal.fr.md" in plain prose, the leak surface was wider than just the
customer pack — the operator pack itself carried it.

**Fix shipped.**

- **CDC `cdc-feasibility-shape.fr.md`** § 10: section retitled "Documents
  associés" with three plain-French descriptions (questionnaire, proposal,
  deck) — no filenames.
- **Deck `deck-suez-webuy.fr.md`** opening blockquote rewritten without
  filenames; "La matrice de services" reframed as "Notre approche
  d'engagement" using `Temps` (1, 2, 3, 4) + `Discipline` columns instead
  of internal cell codes.
- **Proposal `proposal.fr.md`** § 1 metadata table: removed "Cellules de
  service principales" row and `SERVICE_OFFERING_CATALOG` reference;
  retitled "Calendrier commercial" row to "Annexes commerciales" with a
  plain-French description; § 2 variant tables now use a `Discipline`
  column with brand-canonical names (Diagnostic de processus,
  Conception conjointe, Construction, Formation et passation).

**Verification.** Repo-wide PDF scan for forbidden tokens after re-render:

```
LEAK HUNT — forbidden tokens in rendered PDFs:
  cdc-feasibility-shape.fr.pdf      -> clean
  discovery-questionnaire.fr.pdf    -> clean
  proposal.fr.pdf                   -> clean
  deck-suez-webuy.fr.pdf            -> clean
  proposal.customer.fr.pdf          -> clean
  tarification.customer.fr.pdf      -> clean
  deck.customer.fr.pdf              -> clean
```

Token list: `.fr.md`, `commercial-schedule.md`, `PROPOSAL_TEMPLATE`,
`SERVICE_OFFERING_CATALOG`, `sales-8-slide`, `BRAND_FRENCH`, `FOUNDER_BIO`,
`SOP-ENG_`, `TODO[OPERATOR`. Zero hits across all seven surfaces.

### 1.3 Em-dash usage in titles/subtitles

**Symptom.** Subtitles used em-dashes (`—`) as sentence-medial separators in
several surfaces (e.g., "Variantes A · B · C — édition mai 2026").

**Root cause.** Em-dashes are explicitly banned by the `Impeccable` skill in
UX copy and headlines. They're acceptable in long-form French body text but
not in branded headers/subtitles.

**Fix shipped.** `scripts/render_suez_engagement_pdfs.py` SURFACES dict
updated to replace em-dashes with commas or restored brand-canonical middle
dots. Body markdown was left intact (em-dashes are register-appropriate in
the body of a French operator-formal proposal).

### 1.4 Missing "what we are building" beat in customer proposal

**Symptom.** The customer proposal jumped from "Notre lecture de votre
situation" (diagnosis) to "Ce que nous proposons" (offer in three variants)
without a customer-readable rendition of *the actual artefact* we're
delivering. The CDC has the technical depth, but the CDC is operator-pack
material and uses F-01...F-24 functional codes that read as inventory, not
narrative.

**Fix shipped.** Added §1.5 "Ce que nous construisons" to
`proposal.customer.fr.md` with three load-bearing components:

1. **Before/after table** — "Le parcours d'une demande, avant et après". One
   row per friction point (time, fields, naming, tracking). Reads like a
   procurement-friendly outcomes table.
2. **Four-step parcours** — Lecture → Composition → Revue → Soumission.
   Explicit clause "Aucun champ n'est inscrit dans WeBuy sans cette
   validation" preserves the operator's authority and addresses the most
   common procurement objection (loss of human control).
3. **Four-of-twenty-four functionality cards** — distilled from F-01,
   F-05, F-12, F-24 of the CDC, but written in customer language
   (no F-codes, no internal taxonomy).

## 2. Customer slide deck — new surface

### 2.1 Design brief (interpreted from operator instruction)

> "I'd like a pptx version. It will be a PDF but a slide version of this
> would be nice. Don't port blindly, really design for impeccable slides,
> as it's not the same format and not that much text fit [but we need good
> text/framing, visuals/visualisation techniques and impeccable design]."

Translated to constraints:

- Landscape A4 (297×210mm), one page per slide.
- Nine slides total (cover + seven content + closing) — sized for a 25-30
  minute reading-aloud cadence, not for a 2-hour reading session.
- Visual primitives, not text: anchor stat with sub-context, 2×2 grids,
  horizontal flows, timelines, variant comparison, dark closing.
- No re-use of the proposal's prose; each slide carries one idea, distilled.
- Customer audience (J-CU + enterprise overlay).

### 2.2 Slide inventory and visualisation technique

| # | Slide | Layout primitive | Function |
|:---|:---|:---|:---|
| 01 | Cover | Dark gradient + monogram + cover-strip | Anchor brand and engagement metadata |
| 02 | Le constat | Stat-narrative (asymmetric: anchor "20→40" + 3 context stats) | Frame magnitude without inflation |
| 03 | Notre lecture | 2×2 typographic grid (4 converging signals) | Diagnosis without listicle feel |
| 04 | Ce que nous construisons | 4-step horizontal flow (Lecture / Composition / Revue / Soumission) | Show the artefact's parcours |
| 05 | Ce que fait l'application | 2×2 grid (4 functionalities of 24) | Make the system tangible |
| 06 | Notre méthode | 5-step horizontal timeline (Découverte / Cadrage / Prototype / Mesure / Transfert) | Sequence the engagement |
| 07 | Trois variantes | 3-column comparison with featured-middle (B Prototype recommended) | Decision-ready variant choice |
| 08 | Critères de réussite | 2×2 grid (4 metric pairs) | Show how we'll be measured |
| 09 | Prochaine étape | Dark closing + 2-column split (your side / our side) | Pre-load the next interaction |

### 2.3 Render-pipeline addition

`akos/hlk_pdf_render.py` gained a `slides` profile alongside the existing
`dossier` profile:

- `_brand_pdf_css_slides()` — landscape `@page`, A4 size, full-page
  `.slide` containers (`width: 297mm; height: 210mm; box-sizing:
  border-box; page-break-after: always; overflow: hidden`).
- Layout primitives (`.stat-narrative`, `.grid-2x2`, `.flow-4`,
  `.timeline-5`, `.variants-3`, `.slide.closing`) implemented with
  `display: table` (WeasyPrint 52.5 has no `display: grid` support).
- `render_pdf_branded(profile="slides", ...)` suppresses the dossier
  cover-hero and footer-string injection, since the slide-deck markdown
  supplies its own self-contained cover slide.
- `{{MONOGRAM_URI}}` placeholder substitution lets slide markdown reference
  the monogram without hard-coding a `file://` URI.

`scripts/render_suez_engagement_pdfs.py` SURFACES gained a `deck_customer`
entry with `profile: "slides"`. The script now renders all seven surfaces
in one invocation.

### 2.4 Overflow defect (caught at first render, fixed)

**Symptom.** First render produced 10 pages instead of 9 — the variants
slide (07) overflowed: headline on page 7, three variant cards on page 8.

**Root cause.** Slide content (50pt headline + 12pt subtitle + 3 variant
cards each with 4 rows of 11pt copy) exceeded 210mm at the original margin
budget.

**Fix shipped.** Tuned `_brand_pdf_css_slides`:

- `.slide` padding `18mm 28mm 16mm 28mm` → `14mm 26mm 12mm 26mm`.
- `.slide-meta` margin-bottom `14mm` → `9mm`.
- `h2` font-size `32pt` → `30pt`, margin-bottom `6mm` → `5mm`.
- `.slide-sub` font-size `13pt` → `12pt`, margin-bottom `12mm` → `9mm`.
- `.variants-3 .variant` padding tightened (8mm → 6mm), `v-row` font-size
  10.5pt → 9.5pt, `v-row` margin-bottom 3mm → 2mm.

**Verification.** Re-render gave 9 pages, one per slide, with text
positions confirming each slide fits inside its 210mm height budget.

## 3. Inspiration distillation

The operator provided three competitor PDFs as inspiration (with the
explicit caveat "this is not it, I prefer what we have in AKOS + your
expertise"). They were extracted-then-deleted per AKOS redaction rule;
structural insights live in
`intelligence/.../inspiration-redacted.md`.

Key takeaways relevant to P11:

- **Confirmed**: our 1-thesis-per-page deck shape is competitive with the
  reference. No reflow needed.
- **Confirmed**: our 3-layer tarification annex (variant breakdown + total
  + considerations) matches their economic-proposal shape.
- **Rejected**: their 50-page proposal density. Our brand-strategy commits
  to a tighter customer surface (~22 pages total).
- **Rejected**: their abstract "Riesgos" slide. Our continuity-and-handoff
  language inside "Critères de réussite" is more contractual.
- **Backlog**: a "engagement par mois" annex is a candidate for P12 if
  Variante C is the retained option.

## 4. Final customer pack — what to send

### Customer-facing (J-CU + enterprise overlay)

| Surface | Format | Pages | When |
|:---|:---|:---|:---|
| `proposal.customer.fr.pdf` | A4 portrait, brand-impeccable | 6 | First send (without tarification) |
| `tarification.customer.fr.pdf` | A4 portrait, annex | 3 | Sent on operator decision after the meeting |
| `deck.customer.fr.pdf` | A4 landscape, slide-deck | 9 | Used live in the meeting; left as a written record |

### Operator + bridge collaborator (J-OP + J-CO)

| Surface | Format | Pages | When |
|:---|:---|:---|:---|
| `cdc-feasibility-shape.fr.pdf` | A4 portrait, dossier | 13 | Internal preparation reference |
| `discovery-questionnaire.fr.pdf` | A4 portrait, dossier | 4 | Used live in discovery call |
| `proposal.fr.pdf` (version complète) | A4 portrait, dossier | 8 | Internal pricing-aware companion to the customer proposal |
| `deck-suez-webuy.fr.pdf` | A4 portrait, dossier | 5 | Internal pre-meeting alignment |

All seven surfaces re-rendered in a single pipeline run; manifest written
to `artifacts/exports/2026-suez-webuy/render-manifest.json` with
deterministic SHA-256 traces per surface.

## 5. Drift gates re-confirmed

- WeasyPrint legacy-HSL safeguard (`tests/test_brand_pdf_css_drift.py`)
  passes — the slides profile uses the same `_to_legacy_hsl` emission
  boundary.
- Repo-wide leak hunt for `.md`, internal taxonomy, and operator codes
  comes back clean across all seven rendered PDFs.
- Cover-strip labels are localised (`fr` for the SUEZ pack, `es` default,
  `en` for English overlays).
- `slide_count: 9` invariant is enforced by `pdfplumber` page count check
  on `deck.customer.fr.pdf`.

## 6. What's next

This phase closes the SUEZ engagement pack. P12 is the post-meeting
phase, scoped on operator's outcome: contract signature triggers the
discovery-kickoff working brief, no signature triggers the rendezvous
report and decision-register update.
