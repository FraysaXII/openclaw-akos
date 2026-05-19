---
status: active
classification: governance-shape
intellectual_kind: render-pending-tracker
authority: Brand Manager + System Owner (joint)
artifact_role: durable
ratifying_decisions: [D-IH-86-P, D-IH-86-Q]
parent_rule: .cursor/rules/akos-external-render-discipline.mdc
parent_skill: .cursor/skills/external-render-craft/SKILL.md
paired_runbook: docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/SOP-EXTERNAL_RENDER_GATE_PROMOTION_001.md
language: en
last_review: 2026-05-19
audience: J-OP
gate_state: strict
gate_promoted_at: 2026-05-19
gate_promoted_by: D-IH-86-Q
---

# External-Render Pending Tracker

> **GATE STATE — STRICT (2026-05-19).** The render-trail validator was promoted from INFO advisory to FAIL blocking on 2026-05-19 via **D-IH-86-Q** (Wave F doctrine closure). The validator now runs with `--strict --strict-freshness` in both [`config/verification-profiles.json`](../../../../config/verification-profiles.json) (`validate_external_render_trail` step) and [`scripts/release-gate.py`](../../../../scripts/release-gate.py) (`run_external_render_trail_validation`). Any new external-tagged surface authored after this date must co-mint a render trail OR file a tracker entry below. Demotion procedures (soft via `AKOS_RENDER_TRAIL_NO_STRICT=1` env or hard via argv revert) are documented in the paired runbook [`SOP-EXTERNAL_RENDER_GATE_PROMOTION_001`](../../../references/hlk/v3.0/Admin/O5-1/Tech/System%20Owner/canonicals/SOP-EXTERNAL_RENDER_GATE_PROMOTION_001.md) §6.

**Purpose** — Durable governance shape (per `akos-external-render-discipline.mdc` RULE 6) that tracks every external-facing markdown surface known to the workspace that lacks a paired render artifact (PDF / Web / ERP / Mail / Slide / Broadcast). Same shape as the blocker-tracker pattern from Wave A (D-IH-86-O / `akos-conflict-surfacing-and-blocker-trackers.mdc`).

**Why this exists** — When a surface tagged for an external audience cannot be rendered today (missing tooling, incomplete content, deferred to next initiative), the agent **must NOT silently degrade** by attaching the markdown. Instead, the agent files a tracker entry here. This makes the gap durable and visible; it is the difference between "we know this is render-pending" (governed) and "we forgot about this surface" (drift).

**Drift gate ramp** — Originally ran at INFO while this tracker had > 0 entries. Promoted to FAIL on 2026-05-19 via D-IH-86-Q closure decision after the tracker reached zero entries AND the strict + strict-freshness modes both passed at the closure commit. Same posture pattern as `validate_brand_baseline_reality_drift.py` (INFO at I66 P2 → FAIL at I66 P7).

## Tracker entries

> Empty at mint commit (2026-05-19). All 6 external-tagged surfaces in scope passed the validator at INFO + STRICT modes after Wave-D-aware re-renders landed at this commit:
>
> 1. [`enisa_evidence/dossier_es.md`](../../../references/hlk/v3.0/_assets/advops/2026-holistika-incorporation/enisa_evidence/dossier_es.md) (J-ENISA) → `artifacts/exports/dossier-enisa-PRJ-HOL-FOUNDING-2026-2026-05-19.pdf`
> 2. [`enisa_evidence/cover_email_es.md`](../../../references/hlk/v3.0/_assets/advops/2026-holistika-incorporation/enisa_evidence/cover_email_es.md) (J-ENISA) → `artifacts/exports/email-cover-PRJ-HOL-FOUNDING-2026-2026-04-29.pdf` *(see render-staleness note below)*
> 3. [`enisa_company_dossier/cover_email_company_dossier_es.md`](../../../references/hlk/v3.0/_assets/advops/2026-holistika-incorporation/enisa_company_dossier/cover_email_company_dossier_es.md) (J-ENISA) → matched via mail PDF heuristic
> 4. [`enisa_company_dossier/deck_story_es.md`](../../../references/hlk/v3.0/_assets/advops/2026-holistika-incorporation/enisa_company_dossier/deck_story_es.md) (J-ENISA) → Figma + `artifacts/exports/holistika-company-dossier-enisa-2026-05-19.pdf`
> 5. [`Think Big/Advisers/.../legal-constitutor-handoff-2026-05-18.md`](../../../references/hlk/v3.0/Think%20Big/Advisers/2026-holistika-incorporation/01-our-pack/legal-constitutor-handoff-2026-05-18.md) (J-AD) → `artifacts/exports/adviser-handoff-legal-PRJ-HOL-FOUNDING-2026-2026-05-19.pdf`
> 6. [`Think Big/Advisers/.../cover_email_legal_constitutor_es.md`](../../../references/hlk/v3.0/Think%20Big/Advisers/2026-holistika-incorporation/01-our-pack/cover_email_legal_constitutor_es.md) (J-AD) → matched via mail PDF heuristic

| Entry id | Surface | Audience tags | Pending reason | Remediation owner | Remediation ETA | Tracker entry created | Closed |
|:---|:---|:---|:---|:---|:---|:---|:---|

> *(no entries — table preserved as schema reference)*

## Render-staleness sub-tracker (sha256 freshness)

The current validator checks **existence** of a paired render artifact, not **freshness** (whether the PDF's `source_sha256` matches the current source markdown's sha256). This is a known limitation per `akos-external-render-discipline.mdc` RULE 6 ("forward enhancement"). Surfaces below are flagged when their paired PDF was rendered before the source markdown's last material edit:

| Surface | Last source edit | Last paired-PDF render | Stale? | Notes |
|:---|:---|:---|:---|:---|
| [`enisa_evidence/cover_email_es.md`](../../../references/hlk/v3.0/_assets/advops/2026-holistika-incorporation/enisa_evidence/cover_email_es.md) | 2026-05-18 (frontmatter `last_review`) | 2026-04-29 (`email-cover-PRJ-HOL-FOUNDING-2026-2026-04-29.pdf`) | possibly-stale | Cover email body itself may not have changed substantively in Wave D; awaits operator confirm before re-render |
| [`enisa_company_dossier/cover_email_company_dossier_es.md`](../../../references/hlk/v3.0/_assets/advops/2026-holistika-incorporation/enisa_company_dossier/cover_email_company_dossier_es.md) | 2026-05-18 (frontmatter `last_review`) | (no paired PDF found by stem; matched via fallback `email-*.pdf` glob) | unknown | Should be re-rendered at next adviser-engagement send-event |

> Operator action: when ready to send to advisers/regulators, run `py scripts/render_dossier.py --program PRJ-HOL-FOUNDING-2026 --language es` and `py scripts/export_company_deck_pdf.py` to ensure freshness; cover emails render inline at SMTP-send time per the `mail-render.md` policy (see paired siblings).

## How to add an entry

When the agent or operator discovers a surface that needs an external render but cannot ship one today:

1. Pick a unique entry id (e.g., `RP-2026-05-NN`).
2. Append a row to the table above with: surface path; audience tags; pending reason (one line; e.g., "WeasyPrint not installed locally"; "content not yet operator-ratified"); remediation owner (role name from `BASELINE_ORGANISATION.csv`); ETA (ISO date or quarter-tag like `Q3-2026`); tracker entry created (today); closed (empty until remediated).
3. Update the surface's frontmatter to add `render_pending: RP-2026-05-NN` (optional but helpful for grep).
4. Commit alongside whatever surface change triggered the entry.

When the surface's render trail lands:

1. Verify the validator now reports the surface in the "with trail" count (run `py scripts/validate_external_render_trail.py --strict`).
2. Mark the tracker row's `closed` column with the ISO date.
3. Reference the closure in a decision-register row if the closure is non-trivial.

## Cross-references

- Parent rule: [`.cursor/rules/akos-external-render-discipline.mdc`](../../../../.cursor/rules/akos-external-render-discipline.mdc) — the *when* layer.
- Paired skill: [`.cursor/skills/external-render-craft/SKILL.md`](../../../../.cursor/skills/external-render-craft/SKILL.md) — the *how* layer.
- Sister tracker shape: [`docs/wip/planning/_blockers/i74-promotion-blocker-tracker.md`](../_blockers/i74-promotion-blocker-tracker.md) (Wave A precedent for blocker-trackers as durable governance shapes).
- Drift gate: [`scripts/validate_external_render_trail.py`](../../../../scripts/validate_external_render_trail.py).
- Audience FK: [`AUDIENCE_REGISTRY.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/AUDIENCE_REGISTRY.csv).
- Decision row: D-IH-86-P in `DECISION_REGISTER.csv`.
