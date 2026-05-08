---
language: en
status: active
role_owner: Brand Manager
area: working_space
intellectual_kind: working_doc
authority: Founder + Brand Manager
last_review: 2026-05-08
ssot: false
access_level: 5
---

# Transcripts working space — curated reference exchanges

> **Status — Active (Initiative 66 P1; created 2026-05-08).** Working-space directory under `docs/_assets/transcripts/` for **curated, redacted, and decision-anchored** reference exchanges that pattern-source the brand voice canonicals (`BRAND_SPANISH_PATTERNS.md`, `BRAND_FRENCH_PATTERNS.md`, future `BRAND_ENGLISH_PATTERNS.md`) and the baseline-reality matrix (`BRAND_BASELINE_REALITY_MATRIX.md`).
>
> **Working space, not canonical.** Per [`PRECEDENCE.md`](../../references/hlk/compliance/PRECEDENCE.md): files here are reference-only sourcing material; the canonical registers are the BRAND_*.md files in `docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/`. Edits here do not propagate automatically to canonicals — patterns get extracted manually under operator + Brand Manager review.
>
> **Access level 5.** Operator + cleared collaborators only.

## 1. Why this directory exists

The brand voice canonicals are pattern-sourced from real exchanges between the founder and external counterparties (advisors, regulators, customers, investors, partners, recruiters, collaborators). Real exchanges contain three categories of content:

| Category | Disposition |
|:---|:---|
| **Generalisable voice patterns** (salutation forms, register-shift signals, refusal-language, structure-of-substance, anglicism handling) | Extract to BRAND_*_PATTERNS.md as numbered patterns |
| **Generalisable baseline-reality observations** (what the audience already assumes; first doubt triggers; bridge frames that worked) | Extract to BRAND_BASELINE_REALITY_MATRIX.md |
| **Specifics** (names, firms, deal terms, sector-specific facts, third-party PII, contract numbers) | **Stay in this working space; never propagate to canonicals.** Subject to redaction discipline per [`SOP-HLK_TRANSCRIPT_REDACTION_001.md`](../../references/hlk/v3.0/Admin/O5-1/People/Compliance/SOP-HLK_TRANSCRIPT_REDACTION_001.md) before any canonical extraction |

The working-space pattern lets the operator surface a real exchange to a curating agent, the agent extracts the generalisable patterns, the canonicals get updated, and the working-space copy remains under Access Level 5 controls (never indexed, never rendered, never shipped externally).

## 2. Naming convention

Files in this directory follow the schema:

```
<YYYY-MM-DD>-<context-slug>-<lang>.md
```

Examples:

- `2026-04-07-poi-leg-enisa-lead-es.md` — ENISA-track legal counsel (already pattern-sourced into BRAND_SPANISH_PATTERNS §1)
- `2026-04-01-fr-prospect-presentation-fr.md` — FR business prospect (already pattern-sourced into BRAND_FRENCH_PATTERNS §3)
- `2026-04-30-hosteleria-admin-tu-es.md` — hospitality SME consulting *tú* register (already pattern-sourced into BRAND_SPANISH_PATTERNS §10.1)

The `<context-slug>` is anonymised (uses GOI/POI ref-id when one exists; otherwise a context-only descriptor like `hosteleria-admin` or `fr-prospect-presentation`). **No real names, no firm names, no deal terms, no sector-specific PII** in filenames.

## 3. File structure (template)

Each file follows this structure:

```markdown
---
language: en
status: working_space
ref_id: <GOI/POI ref_id if applicable>
date_observed: <ISO-8601 date>
audience: <investor | customer | advisor | enisa | partner | recruiter | collaborator | internal>
language_observed: <es | fr | en | bilingual>
register_observed: <formal_legal | peer_consulting | regulator_neutral | investor_aspirational | casual_internal>
extraction_status: <pending | partial | complete | superseded>
canonical_extracted_to: <path-to-BRAND_*_PATTERNS.md or null>
access_level: 5
---

# <Date> · <Context slug> · <Language>

## Provenance + redaction note

<Brief: what was redacted, source citation, redaction discipline applied>

## Verbatim exchange

<Verbatim quote with PII redacted per SOP-HLK_TRANSCRIPT_REDACTION_001>

## Pattern observations (raw)

<Operator + Brand Manager notes on what patterns this exchange demonstrates>

## Generalisable extractions

<Numbered patterns suitable for canonical extraction>

## Decision

<Where the extracted patterns landed in the canonicals; ISO-8601 date of canonical update>

## Open follow-ups

<What about this exchange remains unextracted; what triggers re-extraction>
```

## 4. Maintenance discipline

- **Append-only.** Files are not edited after they're committed; new observations go in new files.
- **Redaction first.** Real names, firm names, deal terms, contract numbers, third-party PII redacted **before** the file is written. The redaction-first discipline is non-negotiable per [`SOP-HLK_TRANSCRIPT_REDACTION_001.md`](../../references/hlk/v3.0/Admin/O5-1/People/Compliance/SOP-HLK_TRANSCRIPT_REDACTION_001.md).
- **Canonical extraction tracked.** Each working-space file's `extraction_status` field tracks whether the patterns have been moved into a BRAND_*_PATTERNS.md canonical. `pending` files are the operator + Brand Manager review queue.
- **Annual review.** All files older than 24 months get reviewed for archival. If a file's patterns are fully extracted + the source-context is no longer commercially live, the file moves to an archive subdirectory. If patterns are still valuable + the context is live, it remains.
- **No raw transcripts.** This directory holds **curated** exchanges (already redacted + structured per the §3 template). Raw audio + raw video files stay outside this directory entirely (operator-local; not in repo).

## 5. Access discipline

- **Repo-internal.** Access level 5 (cleared collaborators).
- **Never indexed by external systems.** Not exposed via `holistikaresearch.com`, `hlk-erp`, `kirbe`, or any consumer-facing surface.
- **Not rendered to PDF/DOCX.** No deliverable pipeline reads this directory.
- **Drift gate.** `validate_brand_baseline_reality_drift.py` (P2) flags any rendered DOM that contains verbatim transcript snippets — they should never reach external surfaces; if they do, the canonical extraction was too literal.

## 6. Currently tracked exchanges

The first commit of this directory contains **only this README** and a `.gitkeep` to anchor the structure. The first three real exchanges (the ones already pattern-sourced into the BRAND canonicals) are the priority working-space backfill in I66 P1; they will land as separate commits to keep the redaction-first discipline visible in git history:

1. `2026-04-07-poi-leg-enisa-lead-es.md` — ENISA-track legal counsel (already extracted to BRAND_SPANISH_PATTERNS §1)
2. `2026-04-01-fr-prospect-presentation-fr.md` — FR business prospect (already extracted to BRAND_FRENCH_PATTERNS §3)
3. `2026-04-30-hosteleria-admin-tu-es.md` — hospitality SME (already extracted to BRAND_SPANISH_PATTERNS §10.1)

These are queued under the I66 P1 follow-up tasks. The canonical extractions in BRAND_*_PATTERNS.md are operator-confirmed; the working-space backfill is the audit trail.

## 7. Related

- [`SOP-HLK_TRANSCRIPT_REDACTION_001.md`](../../references/hlk/v3.0/Admin/O5-1/People/Compliance/SOP-HLK_TRANSCRIPT_REDACTION_001.md) — redaction discipline (pre-condition for any file in this directory).
- [`BRAND_SPANISH_PATTERNS.md`](../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_SPANISH_PATTERNS.md) — ES canonical (consumer of these working-space files).
- [`BRAND_FRENCH_PATTERNS.md`](../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_FRENCH_PATTERNS.md) — FR canonical (consumer of these working-space files).
- [`BRAND_BASELINE_REALITY_MATRIX.md`](../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_BASELINE_REALITY_MATRIX.md) — per-audience baseline canonical (consumer of pattern-extracted observations).
- [`PRECEDENCE.md`](../../references/hlk/compliance/PRECEDENCE.md) — working-space asset classification (this directory's category).
- [I66 P1 deliverable list](../../wip/planning/66-brand-vision-ops-sweep/master-roadmap.md#p1-canon-hardening-and-voice-7-8d).
