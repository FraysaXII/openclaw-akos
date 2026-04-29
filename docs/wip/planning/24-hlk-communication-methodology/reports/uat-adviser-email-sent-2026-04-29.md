# UAT — Adviser email sent (G-24-3 closure)

**Initiative**: 24 — HLK Communication Methodology
**Closure goal**: G-24-3 (operator sends the actual ENISA cover email to `POI-LEG-ENISA-LEAD-2026`)
**Date authored**: 2026-04-29 (template; operator fills in at SMTP time)
**Author role**: Founder (Operator)

> **Estado**: TEMPLATE — pending operator fill-in immediately after pressing Send. Do not commit timestamps from a future date; commit the moment the email actually leaves the SMTP queue.

---

## 1. Pre-flight checklist (tick every box before pressing Send)

- [ ] **Recipient resolved off-repo** — real email address for `POI-LEG-ENISA-LEAD-2026` retrieved from the off-repo identity store and pasted into the email client at SMTP step (never written into git).
- [ ] **Sharing-label gate honored** — body cites only `counsel_and_named_counterparty` or lower; no `restricted`-sensitivity rows referenced. The Spanish body in `cover_email_es.md` cites only Q-row ids and `GOI/POI` ref_ids; passes.
- [ ] **Discipline-lens match** — `discipline=LEG` (Legal Counsel) maps to recipient lens `legal_certification`. Voice register `peer_consulting` × pronoun `tu` per `BRAND_REGISTER_MATRIX.md`. Confirmed by composer Layer 4 metadata.
- [ ] **Brand voice match** — opener `Buenos días, Guillermo,` + closer `Un saludo,` + mixed peer register per `BRAND_SPANISH_PATTERNS.md` §"Founder reply pattern". Body length 145 words (within 120–150 plan target).
- [ ] **Operator decisions reviewed** — the dossier `TODO[OPERATOR]` blocks (objeto social text + CNAE pick, capital amount, EUR figures, PESTEL, workforce plan) reviewed by the founder. Either flipped to final values or kept as `TODO[OPERATOR]` deliberately to invite the adviser's input. (Recommended: keep as TODO and discuss live; the dossier framing is "we have a recommendation, we want your written confirmation".)
- [ ] **Attachments staged** — three artifacts present in `artifacts/exports/`:
    - `dossier-enisa-PRJ-HOL-FOUNDING-2026-2026-04-29.pdf` (full 4-pillar dossier + 5 apéndices; ~12-15 pages)
    - `appendix-handoff-PRJ-HOL-FOUNDING-2026-2026-04-29.pdf` (structured Q-tracker + fact-pattern + filed instruments)
    - `email-cover-PRJ-HOL-FOUNDING-2026-2026-04-29.docx` (cover email metadata wrapper; the operator copies the Layer 4 Spanish body into the email client; the DOCX is **not** sent as attachment, it's a paste-source for audit)
- [ ] **Founder sign-off recorded** — `operator-answers-wave2.yaml` Section 5 timestamp updated to today's date.

## 2. SMTP send manifest

> Operator fills these slots **immediately after** pressing Send. Do not pre-fill.

```
SMTP_Sent_UTC:        TODO[OPERATOR]    # ISO-8601 UTC, e.g. 2026-04-29T18:42:00Z
SMTP_Sent_TZ_local:   TODO[OPERATOR]    # local time as displayed in the email client
SMTP_Client:          TODO[OPERATOR]    # e.g. "Apple Mail 17.0" or "Gmail web"
SMTP_From_Address:    TODO[OPERATOR]    # founder address; goes off-repo verification only
Recipient_resolved:   POI-LEG-ENISA-LEAD-2026   # real address NOT pasted into git
```

## 3. Attachment integrity manifest

Captured at render time by `scripts/render_dossier.py` and `scripts/export_adviser_handoff.py`. Two render passes happened on 2026-04-29:

- **Pass 1 — initial render** (post-Initiative 27): functional output, basic visual styling, internal jargon present in body.
- **Pass 2 — Initiative 27 brand follow-up render**: jargon-free body per `BRAND_JARGON_AUDIT.md`; visual upgrade (numbered section openers, stat-grid, pull-quote, capability cards with tag pills, friendly open-question callouts replacing `TODO[OPERATOR]` markers); zero internal codenames in rendered PDF.

The hashes below reflect **Pass 2 (final)**. If a third render is required (e.g. operator flips a `TODO[OPERATOR]` to a final value), all three hashes change in lockstep with the markdown source; capture them again with the PowerShell command at the bottom.

| Artifact | Path | sha256 (full) | Bytes |
|:---|:---|:---|:---|
| Dossier PDF (Pass 2 — branded, jargon-free) | `artifacts/exports/dossier-enisa-PRJ-HOL-FOUNDING-2026-2026-04-29.pdf` | `248E0B7BE7A5C207566448B0F9420DCE3FF5008DCF2959DC24D70BBC62649C7E` | 238322 |
| Appendix handoff PDF (Pass 2) | `artifacts/exports/appendix-handoff-PRJ-HOL-FOUNDING-2026-2026-04-29.pdf` | `FB36EF6F78E72A7E36614216CAA1FB83BEAFE2EBC7E26FB765738E1D8DA23C3D` | 195674 |
| Cover email DOCX (audit copy, not attached) | `artifacts/exports/email-cover-PRJ-HOL-FOUNDING-2026-2026-04-29.docx` | `F7793B2EA2E8E597BE49D35E0AF4724C581E808C145D7B3DFE731DBF4CFD40A7` | 14260 |
| Render manifest (machine-readable; gitignored) | `artifacts/exports/dossier-enisa-PRJ-HOL-FOUNDING-2026-2026-04-29.manifest.json` | n/a | ~680 |

| Artifact (Pass 1, deprecated — kept for audit only) | sha256 (full) |
|:---|:---|
| Dossier PDF (Pass 1) | `6081B3B6246C844C2792C995406224B0B0779EC456D62EFC8B7139DE26CAA137` |
| Appendix handoff PDF (Pass 1) | `49BD66C045BC92DE3368BCAC2911B2FAB92ED7BB9FE83E078735ADF3046B52ED` |
| Cover email DOCX (Pass 1) | `EFBDEBBFBCF5884A85C29620924A1D2E30B2B49CE0912E1A6984AFECCC75AA78` |

> Operator re-captures sha256 hashes after any re-render via:
> ```powershell
> Get-FileHash -Algorithm SHA256 artifacts\exports\dossier-enisa-PRJ-HOL-FOUNDING-2026-2026-04-29.pdf, artifacts\exports\appendix-handoff-PRJ-HOL-FOUNDING-2026-2026-04-29.pdf, artifacts\exports\email-cover-PRJ-HOL-FOUNDING-2026-2026-04-29.docx | Select-Object Hash, Path
> ```
>
> Note: the render manifest at `dossier-enisa-PRJ-HOL-FOUNDING-2026-2026-04-29.manifest.json` records the `source_md_sha256` and the matching `rendered_pdf_sha256` for full source ↔ output traceability. If the operator re-renders, both hashes change in lockstep.

## 4. Adviser response (filled in when received)

```
Adviser_response_received_UTC:    TODO[OPERATOR]    # when reply arrives
Adviser_response_substance:       TODO[OPERATOR]    # short summary — Q-rows answered, scope confirmed, follow-ups requested
Adviser_call_window_proposed:     TODO[OPERATOR]    # if a call was scheduled
Q_rows_closed_in_response:        TODO[OPERATOR]    # Q-LEG-001, Q-LEG-002, ... — comma-separated ids that the adviser confirmed by writing
Q_rows_still_open:                TODO[OPERATOR]    # remaining Q-row ids
Next_action:                      TODO[OPERATOR]    # founder's next step (call schedule / clarification / sign-with-notary date)
```

When the adviser response lands, update each closed `Q-row` directly in `docs/references/hlk/compliance/ADVISER_OPEN_QUESTIONS.csv` (status → `closed_with_adviser_confirmation`) and reseed the `process_list_mirror` / `adviser_open_questions_mirror` per `scripts/sync_compliance_mirrors_from_csv.py`.

## 5. G-24-3 closure assertion

When all of:

1. SMTP_Sent_UTC has a real ISO timestamp (Section 2);
2. all four attachment sha256 lines are filled (Section 3);
3. Adviser_response_received_UTC has a real timestamp **OR** `+72h` watchdog has elapsed and a follow-up has been scheduled (Section 4);

then **G-24-3 is closed**. Update `docs/wip/planning/24-hlk-communication-methodology/master-roadmap.md` to set Initiative 24 status `Closed`, append the closure note to `decision-log.md` (D-IH-24-CLOSURE), and remove G-24-3 from the open-goals list at the top of `master-roadmap.md`.

## 6. Provenance

- Generator chain (this UAT report sources):
    - `scripts/render_dossier.py` (Initiative 27 P4) — emits dossier PDF + manifest.json
    - `scripts/export_adviser_handoff.py --profile dossier` (Initiative 27 P1 follow-up) — emits the appendix handoff PDF
    - `scripts/compose_adviser_message.py --body cover_email_es.md --profile dossier` (Initiative 27 P3) — emits the cover email DOCX/PDF
- Source-of-truth for the message body: [`cover_email_es.md`](../../../references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_evidence/cover_email_es.md)
- Source-of-truth for the dossier prose: [`dossier_es.md`](../../../references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_evidence/dossier_es.md)
- Brand visual tokens: [`BRAND_VISUAL_PATTERNS.md`](../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_VISUAL_PATTERNS.md)
- Brand voice: [`BRAND_VOICE_FOUNDATION.md`](../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_VOICE_FOUNDATION.md), [`BRAND_REGISTER_MATRIX.md`](../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_REGISTER_MATRIX.md), [`BRAND_DO_DONT.md`](../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_DO_DONT.md), [`BRAND_SPANISH_PATTERNS.md`](../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_SPANISH_PATTERNS.md)
