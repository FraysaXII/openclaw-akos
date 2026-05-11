---
artifact_kind: inspiration_distillation
audience: internal
classification: source-grade
language: en
phase: P11
date: 2026-05-10
sources_status: redacted_then_deleted_at_source
---

# P11 inspiration distillation — competitor decks (redacted)

> Internal source-grade note. The originating PDFs were provided by the founder
> for inspiration only with explicit instruction "This is not it, I prefer what
> we have in AKOS + your expertise but maybe it can help." Source files were
> redacted at extraction and deleted from disk per AKOS confidentiality rule.
> Do not reproduce client name, competitor name, monetary figures, or any
> identifier that would tie this distillation back to the originating party.

## Sources (redacted handles only)

| handle | shape | notes |
|:---|:---|:---|
| `[INSPIRATION-A]` | 10-page narrative roadmap on data governance (single thesis per page) | Output of a public-sector readiness exercise. Not an offer. |
| `[COMPETITOR-A] / [CLIENT-X] v1` | ~51-page proposal slide-deck | Mid-market consultancy → higher-ed counterparty, "scaling plan" framing. |
| `[COMPETITOR-A] / [CLIENT-X] v2` | ~54-page revised proposal slide-deck | Same engagement, second revision. Same scaffolding as v1 with two added initiative cards and a richer economic-proposal section. |

## Patterns worth keeping

### 1. Roadmap-as-narrative (from `[INSPIRATION-A]`)

A 10-page roadmap where every page makes **one statement of intent** in plain
prose, not a deliverable list. Example shape (paraphrased, redacted of domain
specifics):

- "Put the reports in order before migrating anything."
- "Decide which data lives where, in which layer, under which rules."
- "All reports share one logic of data and of meaning."
- "Know who accesses what, and from where, without relying on memory."

This is a **thesis-per-page** model — closer to a doctrine than a plan. We
already use this register in our customer deck (slide 02 "Une mécanique
répétée…", slide 03 "Quatre signaux convergent…", etc.). Confirms our shape
is competitive at the executive level.

### 2. Initiative-numbered catalog (from `[COMPETITOR-A]`)

The proposal organizes its 18-22 work-streams as numbered initiatives
(`DAT01`...`DAT22` in their case), each with its own one-pager. This is
useful because:

- It gives the reader a stable address space to come back to.
- It separates the *catalog* from the *plan* (planning slides reference IDs).
- It produces a "we have a system" feeling.

We already have this with our **F-01...F-24** functional codes inside the
CDC (feasibility shape document). Our customer deck does not require this
density — keeping it in the CDC is correct.

### 3. Three-layer economic proposal (from `[COMPETITOR-A]`)

Their economic proposal is split into three slides (or three sections in
one):

1. **Breakdown by work-line** — "what each work-stream costs"
2. **Project total** — "what the project costs"
3. **Considerations** — "what is and is not included; assumptions"

Our `tarification.customer.fr.md` annex already maps to this:

- breakdown-by-variant table = §1 (variant-level breakdown)
- variant-level totals = §2 (total per variant)
- "modalités tarifaires + adhérences contractuelles" = §3 (considerations)

No change needed; we are already at this level of structural clarity.

### 4. Workshops by month (from `[COMPETITOR-A]`)

They dedicate a slide to "Talleres y entregables — Mes 1", another to "Mes 2",
another to "Mes 3". Each lists what is delivered that month and which
workshops are run.

Our customer deck handles this implicitly via the 5-step timeline (slide 06).
For a longer engagement (Variante C, 12-14 weeks) we may want to add a
*month-by-month* annex. Marked as a candidate for P12 if the operator agrees
that variant ships.

## Patterns we explicitly *do not* keep

- **49-page proposal density.** Their decks are ~50 pages. Our customer deck is
  9. The brand strategy is to be **tighter** than the comparable consultancy
  reference. We commit to 9 slides + 6-page proposal + 3-page tarification +
  4-page discovery questionnaire. Total customer-facing surface stays under
  ~22 pages.
- **Federated-model framing.** They lead with a "modelo federado | how it works
  / how it benefits you" 2-slide diptych. This is appropriate for a multi-team
  data-governance program. For a procurement-automation engagement on a
  single team, it would be over-engineered.
- **Generic risk slide.** Their "Riesgos" slide is generic ("technical risk /
  organisational risk / regulatory risk"). We prefer to embed risk language
  *inside* our criteria-de-réussite slide ("Continuité — aucune dépendance de
  production sur Holistika passé la fin de la mission") which is more
  contractual and less abstract.
- **`#PROJECT-CODE` last-slide watermark.** Their final slide is a project
  code (e.g., `#110841`). We rely on the cover-strip program ID
  (`ENG-SUEZ-WEBUY-2026`) for traceability and do not need a back-cover code.

## Anti-pattern observed

The v1 and v2 decks have **different page orders for the same content**.
Specifically, "Plan a corto plazo - Nuevas iniciativas" sits at p12 in v2 but
at p44 in v1, even though it's the same section. This signals an internal
reflow that probably did not get caught by their review process.

**Lesson:** our render manifest (sha-locked per surface) prevents this drift
across versions. Keep the manifest as the authoritative shape gate.

## Decisions taken from this review

- **No structural change** to `deck.customer.fr.md`. The current 9-slide shape
  beats the comparable reference at the executive register.
- **No change** to `proposal.customer.fr.md` content depth. Adding "Ce que
  nous construisons" (P11-4) was the right delta.
- **Backlog item (P12 candidate):** if Variante C is the retained variant,
  consider an "engagement par mois" annex for months 2-4. Track in the SUEZ
  risk/decision register.

## Disposal record

| source path (Downloads) | extracted at | deleted at | sha-256 trace |
|:---|:---|:---|:---|
| `[INSPIRATION-A].pdf` | 2026-05-10 09:30 UTC+2 | 2026-05-10 09:31 UTC+2 | not retained (per redaction rule) |
| `[COMPETITOR-A] / [CLIENT-X] v1.pdf` | 2026-05-10 09:30 UTC+2 | 2026-05-10 09:31 UTC+2 | not retained |
| `[COMPETITOR-A] / [CLIENT-X] v2.pdf` | 2026-05-10 09:30 UTC+2 | 2026-05-10 09:31 UTC+2 | not retained |

Cross-reference: this complements the earlier P0/P9 redacted competitor data
in `intelligence/2026-05-10-suez-webuy-procure-to-pay/` (the `Mdc v2.json`
and PDF prospection record). Both batches confirm the same finding: our
register is the right one; our scope is the right size.
