# UAT — Company dossier send (G-24-3 closure with the correct artifact)

**Initiative**: 28 — Investor-style Holistika Company Dossier
**Closure goal**: G-24-3 (operator sends the company dossier to `POI-LEG-ENISA-LEAD-2026`)
**Date authored**: 2026-04-30 (template; operator fills in at SMTP time)
**Author role**: Founder (Operator)
**Supersedes**: `docs/wip/planning/24-hlk-communication-methodology/reports/uat-adviser-email-sent-2026-04-29.md` for the **primary** external send. The previous report still applies if the operator chose to send the founder evidence dossier instead — kept for audit.

> **Estado**: TEMPLATE — pending operator fill-in immediately after pressing Send. Do not commit timestamps from a future date; commit the moment the email actually leaves the SMTP queue.

---

## 1. What is being sent

The **primary** external artifact is now the **company dossier** (Initiative 28), not the founder evidence dossier (Initiative 27). The founder evidence dossier is retained as an **adviser appendix** that goes only when the adviser asks for technical-legal detail.

| Artifact | Role | Path |
|:---|:---|:---|
| Company dossier PDF | **Primary attachment** | `artifacts/exports/holistika-company-dossier-enisa-2026-04-30.pdf` |
| Cover email DOCX (audit copy, not attached) | Audit | `artifacts/exports/email-cover-PRJ-HOL-FOUNDING-2026-2026-04-30.docx` (rendered post-merge if operator wants a Word copy) |
| Founder evidence dossier PDF (Initiative 27) | **Optional appendix on request** | `artifacts/exports/dossier-enisa-PRJ-HOL-FOUNDING-2026-2026-04-29.pdf` |
| Adviser handoff appendix (Initiative 27) | **Optional appendix on request** | `artifacts/exports/appendix-handoff-PRJ-HOL-FOUNDING-2026-2026-04-29.pdf` |

## 2. Pre-flight checklist (tick every box before pressing Send)

- [ ] **Recipient resolved off-repo** — real email address for `POI-LEG-ENISA-LEAD-2026` retrieved from the off-repo identity store and pasted into the email client at SMTP step (never written into git).
- [ ] **Cover email body** — copy from `cover_email_company_dossier_es.md` matches what's pasted into the email client. Subject line: `Holística Research — Dossier de Compañía + encaje ENISA (PRJ-HOL-FOUNDING-2026)`.
- [ ] **Sharing-label gate honoured** — body cites only `counsel_and_named_counterparty` or lower; no `restricted`-sensitivity content referenced. The Spanish body in `cover_email_company_dossier_es.md` references the deck and offers the appendix on request only.
- [ ] **Discipline-lens match** — `discipline=LEG` (Legal Counsel) maps to recipient lens `legal_certification`. Voice register `peer_consulting` × pronoun `tu` per `BRAND_REGISTER_MATRIX.md`.
- [ ] **Brand voice match** — opener `Hola Guillermo,` + closer `Un saludo,` + mixed peer register per `BRAND_SPANISH_PATTERNS.md` §"Founder reply pattern". Body length ≈ 165 words.
- [ ] **Jargon audit** — both the deck PDF and the email body have passed `BRAND_JARGON_AUDIT.md` §4 (zero internal codenames, zero `TODO[OPERATOR]` strings, zero stack jargon). Build script enforced this at deck render time.
- [ ] **Primary attachment staged** — `artifacts/exports/holistika-company-dossier-enisa-2026-04-30.pdf` exists locally (run `py scripts/build_company_deck.py && py scripts/export_company_deck_pdf.py --manifest artifacts/exports/holistika-company-dossier-enisa-2026-04-30.manifest.json` if not).
- [ ] **Appendix attachments staged but not attached** — the founder evidence PDF and the handoff appendix are present in `artifacts/exports/` but **not** attached unless the adviser asks for detail.
- [ ] **Founder sign-off recorded** — `operator-answers-wave2.yaml` Section 5 timestamp updated to today's date.

## 3. SMTP send manifest

> Operator fills these slots **immediately after** pressing Send. Do not pre-fill.

```
SMTP_Sent_UTC:        TODO[OPERATOR]    # ISO-8601 UTC, e.g. 2026-04-30T18:42:00Z
SMTP_Sent_TZ_local:   TODO[OPERATOR]    # local time as displayed in the email client
SMTP_Client:          TODO[OPERATOR]    # e.g. "Apple Mail 17.0" or "Gmail web"
SMTP_From_Address:    TODO[OPERATOR]    # founder address; goes off-repo verification only
Recipient_resolved:   POI-LEG-ENISA-LEAD-2026   # real address NOT pasted into git
```

## 4. Attachment integrity manifest

Captured at render time by `scripts/export_company_deck_pdf.py` (primary) and `scripts/render_dossier.py` + `scripts/export_adviser_handoff.py` (Initiative 27 appendices).

| Artifact | Path | sha256 (full) | Bytes |
|:---|:---|:---|:---|
| Company dossier PDF (Initiative 28, primary) | `artifacts/exports/holistika-company-dossier-enisa-2026-04-30.pdf` | `C5DBAB04FEE04B2B0B1E0017A48CC50855487D3CAFBA1A8D73AF8431918493EF` | 66723 |
| Source HTML deck (preview) | `docs/presentations/holistika-company-dossier/index.html` | TODO[OPERATOR] re-capture if rebuilt | ~37000 |
| Render manifest | `artifacts/exports/holistika-company-dossier-enisa-2026-04-30.manifest.json` | n/a | ~470 |
| Founder evidence dossier PDF (Initiative 27, on-request appendix) | `artifacts/exports/dossier-enisa-PRJ-HOL-FOUNDING-2026-2026-04-29.pdf` | `248E0B7BE7A5C207566448B0F9420DCE3FF5008DCF2959DC24D70BBC62649C7E` | 238322 |
| Adviser handoff appendix (Initiative 27, on-request) | `artifacts/exports/appendix-handoff-PRJ-HOL-FOUNDING-2026-2026-04-29.pdf` | `FB36EF6F78E72A7E36614216CAA1FB83BEAFE2EBC7E26FB765738E1D8DA23C3D` | 195674 |

> Operator re-captures sha256 hashes after any re-render via:
>
> ```powershell
> Get-FileHash -Algorithm SHA256 artifacts\exports\holistika-company-dossier-enisa-2026-04-30.pdf, artifacts\exports\dossier-enisa-PRJ-HOL-FOUNDING-2026-2026-04-29.pdf, artifacts\exports\appendix-handoff-PRJ-HOL-FOUNDING-2026-2026-04-29.pdf | Select-Object Hash, Path
> ```

## 5. Visual SSOT — Figma file

The Figma file is the visual source of truth and remains editable for any visual refinement:

- URL: <https://www.figma.com/design/yiPav7BLxUulNFrrsoKJqW>
- File key: `yiPav7BLxUulNFrrsoKJqW`
- Page: `Company Dossier v1`
- 14 frames, named `01 · Cover` through `14 · Siguiente paso`
- Build pipeline: `scripts/build_company_deck.py` (HTML) + Figma MCP `use_figma` programmatic build (file)

If the operator re-edits the Figma file before sending, **backport the copy changes** to `deck_slides.yaml` so the next HTML / PDF rebuild stays aligned.

## 6. Adviser response (filled in when received)

```
Adviser_response_received_UTC:    TODO[OPERATOR]
Adviser_response_substance:       TODO[OPERATOR]    # short summary
Adviser_call_window_proposed:     TODO[OPERATOR]
Q_rows_closed_in_response:        TODO[OPERATOR]    # comma-separated Q-LEG-…, Q-CRT-… ids confirmed by writing
Q_rows_still_open:                TODO[OPERATOR]
Next_action:                      TODO[OPERATOR]
```

When the adviser response lands, update each closed Q-row directly in `docs/references/hlk/compliance/ADVISER_OPEN_QUESTIONS.csv` (status → `closed_with_adviser_confirmation`) and reseed the `adviser_open_questions_mirror`.

## 7. G-24-3 closure assertion

When all of:

1. SMTP_Sent_UTC has a real ISO timestamp (Section 3);
2. all four attachment sha256 lines for the **primary** send are filled (Section 4 — company dossier PDF + render manifest at minimum; appendix hashes only if attached);
3. Adviser_response_received_UTC has a real timestamp **OR** `+72h` watchdog has elapsed and a follow-up has been scheduled (Section 6);

then **G-24-3 is closed with the company dossier as the correct artifact**. Update both:

- `docs/wip/planning/24-hlk-communication-methodology/master-roadmap.md` — Initiative 24 status `Closed`, append closure note (D-IH-24-CLOSURE);
- `docs/wip/planning/28-investor-style-company-dossier/master-roadmap.md` — Initiative 28 status `Closed`, append closure note (D-IH-28-CLOSURE).

## 8. Provenance

- **Primary artifact pipeline**:
  - SSOT: [`deck_slides.yaml`](../../../references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_company_dossier/deck_slides.yaml)
  - Narrative SSOT mirror: [`deck_story_es.md`](../../../references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_company_dossier/deck_story_es.md)
  - Visual system: [`deck-visual-system.md`](../../../references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_company_dossier/deck-visual-system.md)
  - HTML preview build: [`scripts/build_company_deck.py`](../../../../scripts/build_company_deck.py) → [`docs/presentations/holistika-company-dossier/index.html`](../../../presentations/holistika-company-dossier/index.html)
  - PDF export: [`scripts/export_company_deck_pdf.py`](../../../../scripts/export_company_deck_pdf.py) → `artifacts/exports/holistika-company-dossier-enisa-2026-04-30.pdf`
  - Figma visual SSOT: [`figma-link.md`](../../../references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_company_dossier/figma-link.md)
  - Cover email: [`cover_email_company_dossier_es.md`](../../../references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_company_dossier/cover_email_company_dossier_es.md)
- **Brand framework applied**: [`BRAND_VISUAL_PATTERNS.md`](../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_VISUAL_PATTERNS.md), [`BRAND_VOICE_FOUNDATION.md`](../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_VOICE_FOUNDATION.md), [`BRAND_SPANISH_PATTERNS.md`](../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_SPANISH_PATTERNS.md), [`BRAND_JARGON_AUDIT.md`](../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_JARGON_AUDIT.md).
- **Tooling SOP applied**: [`SOP-HLK_TOOLING_STANDARDS_001.md`](../../../references/hlk/v3.0/Admin/O5-1/Tech/System%20Owner/SOP-HLK_TOOLING_STANDARDS_001.md).
