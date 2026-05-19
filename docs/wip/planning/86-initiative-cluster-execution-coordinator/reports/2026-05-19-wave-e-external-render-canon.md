---
status: active
classification: closure-report
intellectual_kind: wave_closure_appendix
authority: PMO
artifact_role: derived
ratifying_decisions: [D-IH-86-P]
parent_decision: D-IH-86-P
language: en
last_review: 2026-05-19
audience: J-OP
---

# Wave E — External-Render Discipline Canon (closure appendix)

Follow-up to the [Bundle D closure handoff](2026-05-19-bundle-d-closure-handoff.md) authored at the prior chat closure. Operator named the missing canon at post-Bundle-D follow-up: *"i can't send .md. no one will see them except our collaborators. for externals, pdf only or a web or erp or mail or something like that. let it be canon"*. This appendix records the codification.

## Why this is "Wave E"

Bundle D was named A→D in the prior chat. Wave E continues the same chat session, codifying the load-bearing principle that surfaced once the dossier rewrite landed in Wave D: *external recipients receive rendered surfaces, not markdown*. The principle had been half-implemented across the workspace (BBR governs vocabulary; nine render scripts existed; no rule named the doctrine). Wave E names it.

Per Option 5 default posture (D-IH-86-O / `akos-conflict-surfacing-and-blocker-trackers.mdc`), the agent surfaced 4 architectural decisions baked into "let it be canon" via a single batched ratify gate. Operator picked the **maximum-doctrine path** on every axis:

1. **Rule shape:** split rule + paired skill (the *when* layer + the *how* layer).
2. **Surface enum:** 6 surfaces — PDF / Web / ERP / Mail / Slide / Broadcast (extending past the 4-surface "PDF/web/ERP/mail" framing the operator named, by recognising Slide as distinct from PDF and Broadcast as distinct from Web).
3. **Drift gate posture:** audience-tag-aware soft-fence extending the I85 scaffold (per-audience-class render-format matrix; J-OP markdown-OK; external classes require trail).
4. **Backfill scope:** full backfill of every external-facing markdown today, with render-pending tracker as the durable governance shape for any soft-failures.

## What landed (5 deliverables in 1 commit)

### 1. Canonical Cursor rule

[`.cursor/rules/akos-external-render-discipline.mdc`](../../../../.cursor/rules/akos-external-render-discipline.mdc) — 200+ line rule with 6 RULE sections:

- **RULE 1** — 6-surface canonical enum (PDF / Web / ERP / Mail / Slide / Broadcast) with extension protocol.
- **RULE 2** — audience-class → render-format matrix (mechanically enforced).
- **RULE 3** — markdown-as-SSOT, render-as-delivery (the orthogonal stack).
- **RULE 4** — render-trail detection heuristics (6 per-surface heuristics).
- **RULE 5** — self-discipline rules for agents (5 binding behaviors).
- **RULE 6** — backfill posture (full backfill + INFO→FAIL ramp).

Cross-references: BBR (vocabulary axis), adviser-engagement (advisor-specific render-pack), inline-ratification (gating gaps), conflict-surfacing-and-blocker-trackers (render-pending = same shape), mirror-template (external-repo prose), audience-registry (FK source).

### 2. Paired skill

[`.cursor/skills/external-render-craft/SKILL.md`](../../../../.cursor/skills/external-render-craft/SKILL.md) — 300+ line skill with the *how* layer:

- Per-surface render commands (which script, what input, where output, what manifest).
- Manifest schema (sha256 trail).
- Soft-success fallback policy.
- 10-item pre-render checklist.
- 7 anti-patterns (attaching .md, sharing GitHub raw URLs, rendering once and never re-rendering, skipping manifest, mixing audience tags, promoting .md to delivery, silent backfill).
- 4 recovery patterns.

### 3. Audience-tag-aware drift gate

[`scripts/validate_external_render_trail.py`](../../../../scripts/validate_external_render_trail.py) — 240 line validator:

- FK-resolves `audience:` against `AUDIENCE_REGISTRY.csv`.
- For each external-tagged surface, runs 6 heuristics (PDF / Web / ERP / Mail / Slide / Broadcast).
- Manifest reverse-lookup as primary signal (reads `*.manifest.json` files in `artifacts/exports/` and credits surfaces whose `source_path` is referenced).
- Per-stem PDF heuristic (no wildcard credit).
- Template-surface exemption (`artifact_kind: deck_template`).
- J-OP-only surface exemption.
- INFO → FAIL ramp via `--strict` flag or `AKOS_RENDER_TRAIL_STRICT=1` env.

Wired into `config/verification-profiles.json` `pre_commit` profile + `scripts/release-gate.py` INFO row.

### 4. Render-pending tracker

[`docs/wip/planning/_trackers/external-render-pending-tracker.md`](../../_trackers/external-render-pending-tracker.md) — durable governance shape per RULE 6. Empty at mint with render-staleness sub-tracker for cover emails awaiting send-event re-render. Tracker entry schema (entry_id / surface / audience tags / pending reason / remediation owner / ETA / created / closed) preserved as schema reference.

### 5. Full backfill — 3 fresh PDFs + 3 mail-render sidecars

Every external-tagged surface in scope reaches render parity at this commit:

| Surface | Audience | Render trail at this commit |
|:---|:---|:---|
| `enisa_evidence/dossier_es.md` | J-ENISA | `artifacts/exports/dossier-enisa-PRJ-HOL-FOUNDING-2026-2026-05-19.pdf` (NEW; Wave-D-aware re-render via `render_dossier.py`) |
| `enisa_evidence/cover_email_es.md` | J-ENISA | `artifacts/exports/email-cover-PRJ-HOL-FOUNDING-2026-2026-04-29.pdf` + `mail-render.md` sibling (NEW) |
| `enisa_company_dossier/cover_email_company_dossier_es.md` | J-ENISA | matched via `email-*.pdf` glob + `mail-render.md` sibling (NEW) |
| `enisa_company_dossier/deck_story_es.md` | J-ENISA | `figma-link.md` (existing) + `artifacts/exports/holistika-company-dossier-enisa-2026-05-19.pdf` (NEW; via `export_company_deck_pdf.py`) |
| `legal-constitutor-handoff-2026-05-18.md` | J-AD | `artifacts/exports/adviser-handoff-legal-PRJ-HOL-FOUNDING-2026-2026-05-19.pdf` (NEW; via `export_adviser_handoff.py`) |
| `cover_email_legal_constitutor_es.md` | J-AD | matched via `email-*.pdf` glob + `mail-render.md` sibling (NEW) |

6 deck templates under `_assets/advops/shared/decks/` (J-AD / J-ENISA / J-IN / J-PT / J-RC / J-CU) exempted via `artifact_kind: deck_template` per RULE 4.

## Verification

```
validate_hlk.py                          → PASS (0 hard FAILs)
validate_external_render_trail.py --strict → PASS (76 scanned ; 6 external-tagged ; 6 with trail ; 0 missing)
validate_brand_baseline_reality_drift.py → PASS (8 internal tokens checked; dual-register clean)
validate_audience_tags.py                → PASS (55 scanned ; 13 with audience: frontmatter ; FK-clean + J-OP exclusion clean)
test_audience_tags_drift.py (10 tests)   → PASS
```

## Decisions ratified

- **D-IH-86-P** (governance; reversibility low) — External-render discipline canonization. Operator quote captured verbatim in summary; 4-axis maximum-doctrine ratification recorded.

## OPS rows closed

- **OPS-86-7** (Wave E mint) — closed at mint commit. Companion to OPS-86-6 (Option 5 default posture rule mint, Wave A).

## Forward enhancements (deferred)

These are noted in the rule + skill + tracker but not minted in this Wave E:

1. **sha256-freshness drift gate.** Current validator checks existence; future enhancement reads each `*.manifest.json` and compares `source_sha256` against the source markdown's current sha256. Surfaces with stale renders flag without an explicit tracker entry. Probably lands as a follow-up I-NN initiative when the next major dossier rewrite happens.
2. **`scripts/render_cover_email.py`.** Cover emails currently render inline at SMTP-send time per `mail-render.md` siblings (Pattern A). When a Resend / SendGrid send-pipeline lands, mint the dedicated render script and update `mail-render.md` sidecars.
3. **Web / ERP / Broadcast heuristic infrastructure.** No surfaces in this repo currently use Web / ERP / Broadcast surfaces (everything external is PDF + Slide + Mail today). When the boilerplate rewrite (I66 P5/P7) adds web surfaces and HLK-ERP adds external panels, mint `web-link.md` / `erp-record.md` / `broadcast-link.md` sidecars per the schemas in the skill.
4. **Dedicated test suite** for `validate_external_render_trail.py`. Parallel to `test_audience_tags_drift.py` shape; lands when the validator promotes from INFO to FAIL.
5. **Cleanup of stale renders** in `artifacts/exports/`. The 2026-04-29 dated PDFs are now superseded by 2026-05-19 dated PDFs. They're gitignored so this is operator hygiene, not a CI concern.

## Cluster status (no change from Bundle D)

5-of-10 I86 cluster siblings closed (I79 + I80 + I84 + I85 + I87). 3 active (I76 + I81 + I82). 3 candidate-with-blocker-tracker (I74 + I75 + I83). Wave E is doctrine-level; doesn't touch sibling status.

## Next operator moves

1. Read [`.cursor/rules/akos-external-render-discipline.mdc`](../../../../.cursor/rules/akos-external-render-discipline.mdc) once to internalise the 6-surface enum (5-minute read).
2. Skim [`.cursor/skills/external-render-craft/SKILL.md`](../../../../.cursor/skills/external-render-craft/SKILL.md) §"Pre-render checklist (10 items)" before next external send-event.
3. When ready to send the founding dossier to the certifier or the legal constitutor, run `py scripts/render_dossier.py --program PRJ-HOL-FOUNDING-2026 --language es` and `py scripts/export_adviser_handoff.py --discipline legal --program-id PRJ-HOL-FOUNDING-2026 --format pdf --profile dossier --out <path>` to ensure freshness, then attach the dated PDFs to the corresponding cover email.
4. The render-pending tracker is empty today; if future external prose authoring hits a render gap, the agent (under this rule's RULE 5 §5 binding) files a tracker entry rather than silently degrading to .md attach.
