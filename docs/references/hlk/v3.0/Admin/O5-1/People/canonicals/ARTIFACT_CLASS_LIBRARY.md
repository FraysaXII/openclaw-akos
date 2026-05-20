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
  - OUTPUT_TYPE_LIBRARY.md
  - COMPONENT_PRIMITIVE_LIBRARY.md
  - HOLISTIKA_ORGANISING_DOCTRINE.md
  - BRAND_BASELINE_REALITY_MATRIX.md
  - UAT_DISCIPLINE.md
linked_canonical_csvs:
  - dimensions/ARTIFACT_CLASS_REGISTRY.csv
  - dimensions/OUTPUT_TYPE_REGISTRY.csv
  - dimensions/AUDIENCE_REGISTRY.csv
  - dimensions/CHANNEL_TOUCHPOINT_REGISTRY.csv
status: active
role_owner: Brand & Narrative Manager
co_owner_role: System Owner
language: en
audience: J-OP
---

# Artifact Class Library — Layer 2 of the 4-layer hierarchy

> **Layer 2 of the 4-layer output architecture** sitting beneath the 5-axis [Holistika Quality Fabric](HOLISTIKA_QUALITY_FABRIC.md). This library names the **named purpose** of every output Holistika emits — dossier, cover-email, intro-message, founding-deck, advisor-pack, UAT-report, SOP, runbook-script, canonical-CSV, decision-log-row, initiative-charter, candidate-file, pause-record, wave-closure, operator-inbox, PMO-hub, WIP-dashboard, counterparty-brief, objections-brief, press-kit. **Layer 2 is where intent lives.**
>
> The shape (Layer 1) and the primitives (Layer 3) are technical decompositions. Layer 2 is the *purpose-naming* layer — the layer that answers "what is this artifact *for*?". Two artifacts of the same shape (e.g., both OT-PDF-DOCUMENT) can be different artifact classes (e.g., AC-DOSSIER vs AC-DECK-FOUNDING) because their purpose differs.
>
> **Forward-charter:** this library ships as a skeleton at I86 Wave K (D-IH-86-BB) with one fully-worked exemplar (AC-COVER-EMAIL below). Other artifact_class doctrine pages mature when the corresponding initiative ships its first artifact at production quality.

## 1. The 21 artifact classes

The canonical inventory lives in [`ARTIFACT_CLASS_REGISTRY.csv`](Compliance/canonicals/dimensions/ARTIFACT_CLASS_REGISTRY.csv). Quick orientation:

| Domain | Artifact classes |
|:---|:---|
| **External-delivery prose** | AC-DOSSIER · AC-COVER-EMAIL · AC-INTRO-MESSAGE · AC-PRESS-KIT (planned) |
| **External-delivery decks** | AC-DECK-FOUNDING · AC-DECK-ADVISOR-PACK · AC-DECK-ENGAGEMENT |
| **External-delivery evidence** | AC-UAT-REPORT |
| **Internal governance** | AC-SOP · AC-RUNBOOK-SCRIPT · AC-CANONICAL-CSV · AC-DECISION-LOG-ROW · AC-INITIATIVE-CHARTER · AC-CANDIDATE-FILE · AC-PAUSE-RECORD · AC-WAVE-CLOSURE |
| **Operator-facing dashboards** | AC-OPERATOR-INBOX · AC-PMO-HUB-RENDER · AC-WIP-DASHBOARD |
| **Internal-register CORPINT** | AC-COUNTERPARTY-BRIEF · AC-OBJECTIONS-BRIEF |

Status: 20 active + 1 planned (AC-PRESS-KIT — activates with first press release).

## 2. Doctrine-page contract (per artifact class)

Each artifact_class doctrine page contains the same 7 sections (see §3 below for the AC-COVER-EMAIL worked example):

1. **Purpose** — what this artifact achieves; what success looks like.
2. **Composing fabric pattern** — the 5-axis fabric.compose() context that produces this class.
3. **Component primitive inventory** — the standard Layer-3 primitives that compose into this artifact + variant menus per audience.
4. **Render path** — Layer-1 output_types + Layer-4 render surfaces + render scripts (when applicable).
5. **Quality bar** — the non-negotiable acceptance criteria before publish.
6. **Worked exemplars** — pointers to the best instances of this artifact class shipped so far.
7. **Anti-patterns** — common failures the discipline of this artifact has surfaced.

## 3. Worked example — AC-COVER-EMAIL

### 3.1 Purpose

A cover email accompanies a sealed deliverable (dossier, deck, handoff pack) and is the recipient's *first impression* of that deliverable. It does three things:

1. **Anchors** — names the why-now context that makes this email worth opening.
2. **Hooks** — gives the recipient one reason to open the attachment / click the link.
3. **Routes** — provides exactly one clear next step (CTA).

It is **not** the deliverable itself. The deliverable lives in an attached PDF (AC-DOSSIER) or a linked deck (AC-DECK-*). The cover email's job is to ensure the deliverable gets read.

### 3.2 Composing fabric pattern

```
fabric.compose(
  audience: J-IN | J-CU | J-PT | J-AD | J-ENISA | J-RC,
  channel: CHAN-EMAIL-OUTBOUND,
  scenario: cover-for-dossier | cover-for-deck | cover-for-handoff,
  brand: brand-voice-register-formal-or-warm-per-audience,
  governance: external-render-trail (PDF attachment carries sha256 manifest),
)
→ output_type: OT-PROSE-EMAIL-RICH
→ render_script: scripts/render_cover_email.py
→ render_surface: mail
```

### 3.3 Component primitive inventory

A standard AC-COVER-EMAIL composes (see [Component Primitive Library](COMPONENT_PRIMITIVE_LIBRARY.md) for variants):

| Slot | Primitive | Default variant | Variants per audience |
|:---|:---|:---|:---|
| 1 | CP-GREETING | warm-named (Hi X) | J-ENISA → formal-named (Dear X); J-IN → formal-named or warm-named depending on relationship; J-CU/J-PT/J-AD/J-RC → warm-named |
| 2 | CP-CONTEXT-ANCHOR | shared-research-anchor | J-IN → market-trigger-anchor or shared-acquaintance-anchor; J-AD → shared-acquaintance-anchor; J-ENISA → regulatory-trigger-anchor |
| 3 | CP-HOOK *(optional)* | data-point-hook | J-IN → contrarian-claim-hook; J-CU → question-hook; J-AD → omitted (let context-anchor speak); J-ENISA → omitted |
| 4 | CP-BODY | 1-paragraph-body | J-IN → 3-bullet-body; J-CU → 1-paragraph-body; J-AD → sectioned-body-with-subheads; J-ENISA → sectioned-body-with-subheads |
| 5 | CP-CTA | cta-button-primary | J-IN → cta-cal-com-embedded (deeper-conversation); J-CU → cta-button-primary (discovery-call); J-AD → cta-button-primary (retainer-meeting); J-ENISA → cta-prose-only (evidence-review); J-RC → cta-button-primary (interview-slot) |
| 6 | CP-SIGNATURE | full-with-title | J-IN → full-with-title-with-photo; J-AD → full-with-title-with-confidentiality; J-ENISA → full-with-title-with-confidentiality; J-CU/J-PT/J-RC → full-with-title |
| 7 | CP-CONFIDENTIALITY-BLOCK | omitted | only when AL ≥ 3 (most J-AD post-NDA + J-ENISA + sometimes J-IN) |

### 3.4 Render path

- **Source-of-truth:** `docs/references/hlk/v3.0/_assets/advops/<engagement>/cover_email_<locale>.md` (output_type: OT-PROSE-MARKDOWN).
- **Render script:** [`scripts/render_cover_email.py`](../../../../../../../../scripts/render_cover_email.py).
- **Render output:** an HTML body string (output_type: OT-PROSE-EMAIL-RICH) consumed by the SMTP-send pipeline at send-time. Per [akos-external-render-discipline.mdc](../../../../../../../../.cursor/rules/akos-external-render-discipline.mdc) RULE 4 mail heuristic, the source `.md` carries a `mail-render.md` sibling that records the render policy.
- **Render surface (Layer 4):** mail.

### 3.5 Quality bar (acceptance criteria before send)

| Bar | Check |
|:---|:---|
| **Subject line** | ≤ 60 chars; mobile-clip-safe; reflects the body's hook (not the body's CTA). |
| **Preheader (preview text)** | ≤ 100 chars; complements the subject (does not repeat it); often the first sentence of the body. |
| **Body length** | ≤ 300 words. Longer cover emails are anti-pattern (the deliverable is the deliverable). |
| **CTA count** | Exactly 1 primary. Optional 1 secondary (cta-link-styled). Never 2+ primaries. |
| **Locale** | If recipient locale ≠ default English, render from the locale-specific source (`cover_email_es.md`, `cover_email_fr.md`); orthographic gate per [`scripts/validate_locale_orthography.py`](../../../../../../../../scripts/validate_locale_orthography.py) must PASS. |
| **Brand voice** | No internal-register tokens per [akos-brand-baseline-reality.mdc](../../../../../../../../.cursor/rules/akos-brand-baseline-reality.mdc). Validator: [`scripts/validate_brand_baseline_reality_drift.py`](../../../../../../../../scripts/validate_brand_baseline_reality_drift.py). |
| **Render trail** | Per [akos-external-render-discipline.mdc](../../../../../../../../.cursor/rules/akos-external-render-discipline.mdc) RULE 4 mail heuristic — `mail-render.md` sibling exists OR rendered HTML companion exists. Validator: [`scripts/validate_external_render_trail.py`](../../../../../../../../scripts/validate_external_render_trail.py). |
| **Plain-text fallback** | Auto-derived from source `.md` by render pipeline; verified non-empty. |
| **Sealed-attachment integrity** | If accompanying a sealed PDF (AC-DOSSIER), the attachment carries its sha256 manifest sidecar; the cover email body cites the manifest hash for the recipient to verify. |
| **A11y** | Color contrast ≥ AAA on text + buttons; alt-text on logo + signature photo; reading order matches DOM. |

### 3.6 Worked exemplars

- **`docs/references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/cover_email_es.md`** — ENISA cover for the founding dossier; Spanish; AL3 confidentiality.
- **(Forward-charter)** — `docs/references/hlk/v3.0/_assets/advops/<future-engagement>/cover_email_en.md` exemplars to land per `I-NN-OUTPUT-ARCHITECTURE` P5.

### 3.7 Anti-patterns

- **The cover-email-as-deliverable.** Body length over 500 words because "the email tries to do too much". Solution: the deliverable is the deliverable; the cover is 3 sentences + 1 CTA.
- **The 3-CTA fork.** "Click here to schedule | reply to this | forward to your team". Choice-paralysis. Solution: 1 primary CTA only.
- **The internal-register leak.** "Find attached our intelligence report on the counterparty's elicitation pattern." For external recipients. Solution: per [akos-brand-baseline-reality.mdc](../../../../../../../../.cursor/rules/akos-brand-baseline-reality.mdc), translate to "Find attached our research brief on this client's discovery pattern."
- **The locale-mismatch.** English subject line + Spanish body. Solution: locale-locked source files; render the matching one.
- **The sealed-attachment integrity gap.** Cover email cites a PDF that has no sha256 manifest. Solution: per [akos-external-render-discipline.mdc](../../../../../../../../.cursor/rules/akos-external-render-discipline.mdc) RULE 3, every sealed PDF carries a `.manifest.json` sidecar.

## 4. Forward-charter — artifact_class doctrine pages still to mature

Priority order (per `I-NN-OUTPUT-ARCHITECTURE` P5):

1. **AC-DOSSIER** (highest external-delivery leverage; standardises sha256 sealing for ENISA / J-IN / J-AD).
2. **AC-DECK-FOUNDING** (the founding-deck page is the most-linked-to deliverable today).
3. **AC-INTRO-MESSAGE** (channel-bound; LinkedIn/WhatsApp/email opener doctrines).
4. **AC-UAT-REPORT** (already sketched in [UAT_DISCIPLINE.md](UAT_DISCIPLINE.md); migrate to this library's shape).
5. **AC-SOP + AC-RUNBOOK-SCRIPT** (already sketched in [akos-executable-process-catalog.mdc](../../../../../../../../.cursor/rules/akos-executable-process-catalog.mdc); migrate the human-facing surface here).
6. **AC-OPERATOR-INBOX + AC-PMO-HUB-RENDER + AC-WIP-DASHBOARD** (the 3 ERP dashboards; doctrine page matures when ERP panel implementations land per Initiative 81).
7. **AC-COUNTERPARTY-BRIEF + AC-OBJECTIONS-BRIEF** (already partially covered by [akos-brand-baseline-reality.mdc](../../../../../../../../.cursor/rules/akos-brand-baseline-reality.mdc); migrate to library shape).
8. Remaining classes — backfill incrementally per first-production-instance-of-class.

## 5. Cross-references

- [HOLISTIKA_QUALITY_FABRIC.md](HOLISTIKA_QUALITY_FABRIC.md) — the 5-axis meta-doctrine.
- [OUTPUT_TYPE_LIBRARY.md](OUTPUT_TYPE_LIBRARY.md) — Layer 1 (shape).
- [COMPONENT_PRIMITIVE_LIBRARY.md](COMPONENT_PRIMITIVE_LIBRARY.md) — Layer 3 (primitives).
- [`ARTIFACT_CLASS_REGISTRY.csv`](Compliance/canonicals/dimensions/ARTIFACT_CLASS_REGISTRY.csv) — canonical inventory.
- [UAT_DISCIPLINE.md](UAT_DISCIPLINE.md) — sister discipline doctrine for AC-UAT-REPORT.
- [`I-NN-OUTPUT-ARCHITECTURE`](../../../../../../wip/planning/_candidates/i-nn-output-architecture.md) — the candidate initiative that matures every artifact_class doctrine page.
- [akos-external-render-discipline.mdc](../../../../../../../../.cursor/rules/akos-external-render-discipline.mdc) — render-trail discipline applied to external-delivery artifact classes.
- [akos-executable-process-catalog.mdc](../../../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) — pairing rule for AC-SOP + AC-RUNBOOK-SCRIPT.
- D-IH-86-BB — ratifying decision (4-layer architecture, 2026-05-20).
