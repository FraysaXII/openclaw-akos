---
intellectual_kind: discipline_charter
sharing_label: internal_only
authored: 2026-05-20
last_review: 2026-05-20
last_review_by: Founder
last_review_decision_id: D-IH-86-BB
methodology_version_at_review: v3.1
linked_canonicals:
  - HOLISTIKA_QUALITY_FABRIC.md
  - HOLISTIKA_ORGANISING_DOCTRINE.md
  - BRAND_BASELINE_REALITY_MATRIX.md
  - BRAND_DO_DONT.md
  - UAT_DISCIPLINE.md
  - access_levels.md
linked_canonical_csvs:
  - dimensions/OUTPUT_TYPE_REGISTRY.csv
  - dimensions/AUDIENCE_REGISTRY.csv
  - dimensions/CHANNEL_TOUCHPOINT_REGISTRY.csv
status: active
role_owner: Brand & Narrative Manager
co_owner_role: System Owner
language: en
audience: J-OP
---

# Output Type Library — Layer 1 of the 4-layer hierarchy

> **Layer 1 of the 4-layer output architecture** sitting beneath the 5-axis [Holistika Quality Fabric](HOLISTIKA_QUALITY_FABRIC.md). This library names the **medium / shape** of every output Holistika emits — prose, slide, image, voice, mermaid, gantt, web, PDF, video, audio. It does **not** name the *purpose* of the output (that's Layer 2 — [Artifact Class Library](ARTIFACT_CLASS_LIBRARY.md)) or the *primitives that compose it* (that's Layer 3 — [Component Primitive Library](COMPONENT_PRIMITIVE_LIBRARY.md)).
>
> **The fabric parametrises this library.** When the fabric composes its 5-axis context (audience × channel × scenario × brand × governance), it picks an output_type for each surface. The output_type then constrains:
>
> - Which render targets are valid (Render Surface, Layer 4 / RULE 2 of [akos-external-render-discipline.mdc](../../../../../../../../.cursor/rules/akos-external-render-discipline.mdc)).
> - Which authoring tools are appropriate.
> - Which accessibility concerns must be honoured.
> - Which brand visual anchors apply.
>
> **Forward-charter:** this library ships as a skeleton at I86 Wave K (D-IH-86-BB) with one fully-worked exemplar (OT-PROSE-EMAIL-RICH below). Other output_type doctrine pages mature when the corresponding initiative ships its first artifact at production quality. See [`I-NN-OUTPUT-ARCHITECTURE`](../../../../../../wip/planning/_candidates/i-nn-output-architecture.md) for the full P0..P7 plan.

## 1. The 17 output types

The canonical inventory lives in [`OUTPUT_TYPE_REGISTRY.csv`](Compliance/canonicals/dimensions/OUTPUT_TYPE_REGISTRY.csv). Quick orientation:

| Class | Members |
|:---|:---|
| **Text** | OT-PROSE-MARKDOWN · OT-PROSE-EMAIL-RICH · OT-PROSE-DM · OT-TABLE-CSV-RAW |
| **Visual** | OT-SLIDE-DECK · OT-IMAGE-RASTER · OT-IMAGE-VECTOR-SVG · OT-DIAGRAM-MERMAID · OT-DIAGRAM-EXCALIDRAW · OT-CHART-GANTT · OT-CHART-DATA · OT-TABLE-RENDERED |
| **Document** | OT-PDF-DOCUMENT |
| **Multimedia** | OT-VIDEO (planned) · OT-AUDIO-VOICE (planned) |
| **Interactive** | OT-WEB-PAGE · OT-WEB-FORM |

Status: 14 active, 2 planned (OT-VIDEO + OT-AUDIO-VOICE), 1 active-but-skeleton (OT-CHART-DATA matures with first dashboard chart deliverable per Initiative 81).

## 2. Doctrine-page contract (per output type)

Each output_type's doctrine page in this library contains the same 8 sections (see §3 below for the OT-PROSE-EMAIL-RICH worked example). The contract is borrowed from Shadcn's component-doctrine pattern (Open Code · Composition · Distribution · Beautiful Defaults · AI-Ready) adapted to Holistika's multi-modal output reality:

1. **Definition** — what this output_type is + 1-line distinguishing characteristic vs siblings.
2. **When to use it** — the 5-axis fabric pattern that selects this output_type.
3. **When NOT to use it** — sibling output_types that are better fits for adjacent shapes.
4. **Authoring tools** — recommended tools per platform.
5. **Render targets** — which Layer 4 surfaces this output_type renders to.
6. **Accessibility checklist** — non-negotiables before publishing.
7. **Brand visual anchor** — which brand canonicals apply.
8. **Composition** — which Layer 3 component primitives typically compose into this output_type.

## 3. Worked example — OT-PROSE-EMAIL-RICH

### 3.1 Definition

A rich HTML email body intended to be read inline in the recipient's mail client. **Distinguishing characteristic vs OT-PROSE-MARKDOWN**: this is the *render shape* of an email body, including inline visual primitives (logo, signature image, CTA button, brand-coloured accent rules); OT-PROSE-MARKDOWN is the *source-of-truth shape* (a `.md` file authored before render).

### 3.2 When to use it

When the fabric composes:

- `audience: J-IN | J-CU | J-PT | J-AD | J-ENISA | J-RC` (any external recipient).
- `channel: CHAN-EMAIL-OUTBOUND` (the outbound transactional / 1:1 mail path; see [`CHANNEL_TOUCHPOINT_REGISTRY.csv`](Compliance/canonicals/dimensions/CHANNEL_TOUCHPOINT_REGISTRY.csv)).
- `scenario: cover-email` for a sealed deliverable, or `scenario: warm-followup` for a multi-touch sequence.
- `brand: brand-voice-register` per [BRAND_DO_DONT.md](../../Marketing/Brand/canonicals/BRAND_DO_DONT.md) + visual treatment per [BRAND_BASELINE_REALITY_MATRIX.md](../../Marketing/Brand/canonicals/BRAND_BASELINE_REALITY_MATRIX.md).
- `governance: external-render-trail` per [akos-external-render-discipline.mdc](../../../../../../../../.cursor/rules/akos-external-render-discipline.mdc) RULE 2.

### 3.3 When NOT to use it

- For the *source-of-truth* form, use OT-PROSE-MARKDOWN. The `.md` file is the canonical; this output_type is only the render.
- For conversational channel-bound short-form (LinkedIn DM, WhatsApp), use OT-PROSE-DM.
- For a fully sealed standalone artifact (multi-page deliverable), use OT-PDF-DOCUMENT and let the email body be an OT-PROSE-EMAIL-RICH cover only.

### 3.4 Authoring tools

- Source: any markdown editor (the `.md` is authored at canonical engagement path: `docs/references/hlk/v3.0/_assets/advops/<engagement>/cover_email_<locale>.md`).
- Render: [`scripts/render_cover_email.py`](../../../../../../../../scripts/render_cover_email.py) (forward-charter — current implementation may be partial; full implementation is gated under `I-NN-OUTPUT-ARCHITECTURE` P5).
- Preview: locally render to HTML + open in browser; mail-client preview (Litmus / Email on Acid for production-grade verification).

### 3.5 Render targets (Layer 4)

- Primary: **mail** (the body is the render).
- Secondary: **web** (some emails are mirrored to a public URL; e.g., release announcements rendered on `holistikaresearch.com/announcements/`).

Never `pdf` (use OT-PROSE-MARKDOWN → OT-PDF-DOCUMENT for sealed deliverables). Never `slide` (decks are OT-SLIDE-DECK). Never `erp` (ERP-gated reads use OT-WEB-PAGE).

### 3.6 Accessibility checklist

| Item | Requirement |
|:---|:---|
| Reader-platform compatibility | Render must pass Outlook (incl. Outlook 2016 Word renderer), Gmail (web + iOS + Android), Apple Mail (macOS + iOS), Yahoo, Thunderbird. Test with [Litmus](https://litmus.com) or equivalent before sending at scale. |
| Dark-mode support | Inline CSS must include `@media (prefers-color-scheme: dark)` rules; logo asset must have a dark-mode variant; never rely on auto-invert. |
| Screen reader | All inline images carry meaningful `alt`; logo's `alt` is the org name; decorative spacers are `alt=""`. Reading order matches DOM; no off-screen text traps. |
| Color contrast | All body text + button labels meet WCAG 2.2 AA (4.5:1 for body; 3:1 for large text). Brand color palette per [BRAND_BASELINE_REALITY_MATRIX.md](../../Marketing/Brand/canonicals/BRAND_BASELINE_REALITY_MATRIX.md) is AAA-certified for the standard pairs. |
| Plain-text fallback | Every rendered HTML body MUST be paired with a plain-text alternative for clients that do not render HTML or for accessibility tools. |
| Length budget | Body text under 300 words; preview text (preheader) under 100 chars; subject line under 60 chars (mobile-clip-safe). |
| Locale | If recipient locale ≠ default, use the locale-specific source (`cover_email_es.md`, `cover_email_fr.md`, etc.). Per [`scripts/validate_locale_orthography.py`](../../../../../../../../scripts/validate_locale_orthography.py), source must pass orthographic gate before render. |

### 3.7 Brand visual anchor

- Logo: locked in left-aligned header position; max-width 180px on desktop, 140px on mobile (responsive via `max-width:100%; height:auto`).
- Color palette: the subset of [BRAND_BASELINE_REALITY_MATRIX.md](../../Marketing/Brand/canonicals/BRAND_BASELINE_REALITY_MATRIX.md) approved for digital use; primary (text), accent (CTA buttons), neutral-1 (rule lines), neutral-2 (background).
- Type scale: system fallback stack (`-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif`) at 16px body, 14px secondary, 18-22px headings; line-height 1.5+.
- Signature: full-with-title variant (see CP-SIGNATURE in [Component Primitive Library](COMPONENT_PRIMITIVE_LIBRARY.md)) plus optional photo (96×96, circle-cropped) + confidentiality notice block when AL ≥ 3.
- Voice register: per [BRAND_DO_DONT.md](../../Marketing/Brand/canonicals/BRAND_DO_DONT.md) — never internal-register tokens (counterparty, elicitation, intelligence) per [akos-brand-baseline-reality.mdc](../../../../../../../../.cursor/rules/akos-brand-baseline-reality.mdc).

### 3.8 Composition (Layer 3 primitives)

A standard `OT-PROSE-EMAIL-RICH` body composes the following primitives, in order:

```
[CP-GREETING]
[CP-CONTEXT-ANCHOR]
[CP-HOOK]                 ← optional; some bodies are evidence-first not hook-first
[CP-BODY]                 ← 1-3 paragraphs OR 3-bullet list
[CP-CTA]                  ← 1 primary CTA; never stacked-primary-CTAs
[CP-SIGNATURE]
[CP-CONFIDENTIALITY-BLOCK]   ← only when AL ≥ 3
```

See each primitive's depth-page in the [Component Primitive Library](COMPONENT_PRIMITIVE_LIBRARY.md) for variant menus per audience × channel × scenario.

## 4. Forward-charter — output_type doctrine pages still to mature

The remaining 16 active+planned output_types each ship a similar 8-section doctrine page over `I-NN-OUTPUT-ARCHITECTURE` P5 (priority order):

1. **OT-PROSE-MARKDOWN** (highest leverage — every canonical is one).
2. **OT-PDF-DOCUMENT** (drives all sealed deliverables).
3. **OT-SLIDE-DECK** (drives all decks; partially covered today by [`docs/presentations/holistika-company-dossier/index.html`](../../../../../../presentations/holistika-company-dossier/index.html) implicit pattern).
4. **OT-WEB-PAGE** (drives all `holistikaresearch.com` pages).
5. **OT-DIAGRAM-MERMAID** (already partially covered by [akos-planning-traceability.mdc](../../../../../../../../.cursor/rules/akos-planning-traceability.mdc) plan-quality-bar §"Three mermaid diagrams").
6. **OT-PROSE-DM** (channel-bound conversational doctrine).
7. **OT-TABLE-RENDERED + OT-DATA-TABLE** (drives ERP planning panels).
8. Remaining 9 (image variants, gantt, excalidraw, web-form, video, audio, table-csv-raw, chart-data, chart-gantt) — backfill incrementally per first-instance-of-class.

## 5. Cross-references

- [HOLISTIKA_QUALITY_FABRIC.md](HOLISTIKA_QUALITY_FABRIC.md) — the 5-axis meta-doctrine that parametrises this library.
- [ARTIFACT_CLASS_LIBRARY.md](ARTIFACT_CLASS_LIBRARY.md) — Layer 2 (purpose).
- [COMPONENT_PRIMITIVE_LIBRARY.md](COMPONENT_PRIMITIVE_LIBRARY.md) — Layer 3 (granular primitives).
- [`OUTPUT_TYPE_REGISTRY.csv`](Compliance/canonicals/dimensions/OUTPUT_TYPE_REGISTRY.csv) — canonical inventory.
- [`I-NN-OUTPUT-ARCHITECTURE`](../../../../../../wip/planning/_candidates/i-nn-output-architecture.md) — the candidate initiative that matures every output_type's doctrine page.
- [akos-external-render-discipline.mdc](../../../../../../../../.cursor/rules/akos-external-render-discipline.mdc) — RULE 2 audience × format compatibility matrix.
- D-IH-86-BB — ratifying decision (4-layer architecture, 2026-05-20).
