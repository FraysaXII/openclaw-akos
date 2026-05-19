---
description: Render external-delivery surfaces correctly (PDF / Web / ERP / Mail / Slide / Broadcast). Use when authoring or shipping any artifact destined for J-IN, J-CU, J-PT, J-AD, J-ENISA, J-RC, or J-CO recipients. Pairs with the cursor rule akos-external-render-discipline.mdc — that rule governs WHEN to render; this skill governs HOW.
---

# External-Render Craft Skill

This skill carries the *how* layer of the external-render discipline. It is paired with [`.cursor/rules/akos-external-render-discipline.mdc`](../../rules/akos-external-render-discipline.mdc), which carries the *when* layer. Read both before posting any external-render workflow.

The skill answers six concrete questions per surface: *which command*, *what input*, *where output lands*, *what manifest looks like*, *what soft-success means*, and *how to verify*. Future agents and operators inherit a deterministic playbook so external delivery never silently degrades to "attach the .md".

## When to load this skill

Load (read) this skill before any of the following moves:

- Authoring an external-facing markdown (dossier, deck, cover email, partner brief, adviser handoff, press kit, recruiter copy).
- Proposing to "send X to Y" where Y is a non-cleared audience.
- Implementing a new render script.
- Investigating a render-trail validator failure.
- Triaging an entry in the [external-render-pending-tracker](../../../docs/wip/planning/_trackers/external-render-pending-tracker.md).
- Reviewing or amending [`AUDIENCE_REGISTRY.csv`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/AUDIENCE_REGISTRY.csv) when the change implies a new render path.

## Surface 0 — Audience × Channel × Language × Objective lookup (run BEFORE picking a surface)

Per [`akos-external-render-discipline.mdc`](../../rules/akos-external-render-discipline.mdc) RULE 7 (Wave F, 2026-05-19), every external surface answers three questions, not two. Surface 0 is the lookup procedure that runs *before* you pick which of the six render surfaces (1–6 below) to author. Skipping Surface 0 is how surfaces end up technically rendered but tonally / strategically mis-aimed — the right format reaches the right audience through the wrong channel in the wrong language for the wrong objective.

### The 4-question pre-flight

Run these four questions in order. Each question's answer narrows the surface-picker space for the next.

1. **Audience — who is the recipient?** Look up the audience-class tag (J-IN / J-CU / J-PT / J-AD / J-ENISA / J-RC / J-CO / J-OP) from [`AUDIENCE_REGISTRY.csv`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/AUDIENCE_REGISTRY.csv). RULE 2's audience-class matrix tells you which subset of the six surfaces is acceptable. J-ENISA narrows immediately to `pdf` (mandatory). J-OP exempts the surface entirely from render-trail enforcement — operator-internal markdown is fine.
2. **Channel — through what inbound / outbound path is the surface reaching them?** Look up the channel code from [`CHANNEL_TOUCHPOINT_REGISTRY.csv`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/CHANNEL_TOUCHPOINT_REGISTRY.csv). Examples: CHAN-EMAIL-OUTBOUND (you initiate); CHAN-EMAIL-INBOUND (they initiated; you respond); CHAN-LINKEDIN-DM (live conversational); CHAN-WEB-FORM (they submitted a form); CHAN-CAL-SCHEDULE (they booked a slot); CHAN-EVENT-MEETING (in-person / video). Channel narrows surface differently than audience: a J-IN reached via CHAN-EMAIL-OUTBOUND wants a `pdf` (sealed deck) plus a `mail` body (cover); the same J-IN reached via CHAN-EVENT-MEETING wants a `slide` (live-pitch deck) plus a `pdf` (leave-behind). Record the chosen channel in the surface's `channel:` frontmatter for downstream auditability (Wave F validator FK-resolves the value INFO-only).
3. **Language — which BRAND_<LANG>_PATTERNS contract governs the prose?** Look up the audience's working language (or fall back to the project default per [`BRAND_MULTILINGUAL_CONTRACT.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_MULTILINGUAL_CONTRACT.md)). Set `language:` frontmatter (es / fr / en or locale variant). Language gates the orthography validator + the per-locale brand-voice register pack. A Spanish J-IN wants BRAND_SPANISH_PATTERNS-aligned prose; a French J-ENISA wants BRAND_FRENCH_PATTERNS + cybersécurité-discipline vocabulary; an English J-CO wants BRAND_ENGLISH_PATTERNS + smart-quote discipline.
4. **Objective — what concrete decision / action does the recipient walk away with?** This is the question the discipline most often skips. Examples: "investor agrees to a 30-minute follow-up call"; "regulator marks dossier as compliant"; "advisor signs the NDA"; "customer requests a SOW". Write the objective in one sentence in the surface's frontmatter (`objective:` field — informal; not yet validator-gated). This is the test against which `change_summary` + `notes` columns in `files-modified.csv` get written when the surface lands.

### Surface-picker decision tree (after Surface 0)

```text
Audience answers narrow the format set per RULE 2 matrix.
   ↓
Channel answers select WHICH formats from that set actually fit.
   ↓
Language answers gate the orthography + voice-register quality.
   ↓
Objective answers gate the prose-craft (every sentence earns its place).
   ↓
NOW pick the surface(s) below (Surfaces 1-6) and author.
```

### Two-surface composition is normal

Most engagement-grade external touches compose at least two surfaces:
- **Investor outbound (CHAN-EMAIL-OUTBOUND, J-IN, es/en/fr):** `mail` (cover body) + `pdf` (sealed deck attachment) → see Surface 4 (Mail) + Surface 1 (PDF).
- **ENISA regulator filing (CHAN-EMAIL-OUTBOUND, J-ENISA, es):** `mail` (cover body) + `pdf` (sealed dossier with sha256 manifest) → see Surface 4 + Surface 1.
- **Adviser pre-NDA (CHAN-EMAIL-OUTBOUND, J-AD, es/en):** `mail` (cover body) + `pdf` (engagement brief; redacted to AL3) → see Surface 4 + Surface 1.
- **Founder bio publish (CHAN-AD-CAMPAIGN, J-CU / J-RC, en):** `web` (canonical page on holistikaresearch.com) + `broadcast` (shared link in adverts) → see Surface 2 (Web) + Surface 6 (Broadcast).

Per the Surface 0 contract, don't go to Surface 1 without first answering the four questions. The render trail will validate either way; the *taste* will only land if Surface 0 was honoured.

### Surface 0 anti-patterns (skip → render anyway → operator catches the mis-aim later)

- **Picking PDF for an audience that wanted `mail` (or vice versa).** A J-CU SME prospect reading on mobile prefers a `mail` body to a 12-page PDF attachment. A J-ENISA reviewer requires a sealed PDF — a mail body is non-compliant.
- **Picking the right format but in the wrong language.** A French J-AD adviser reading English copy parses you as "default-English company"; a Spanish J-IN reading auto-translated English copy parses you as "no Spanish-native authoring discipline". Both undermine the trust the surface is supposed to build.
- **Picking the right format + language but with no objective in the operator's head.** The surface lands; the recipient reads; nothing happens. The surface satisfied the render trail without satisfying the engagement objective.

## Surface 1 — `pdf` (Portable Document Format)

The default external-delivery surface for sealed dossiers, briefs, and one-pagers. Mandatory for J-ENISA (regulator integrity claim).

### Render commands by artifact class

| Artifact class | Command | Output | Notes |
|:---|:---|:---|:---|
| ENISA dossier (founding engagement) | `py scripts/render_dossier.py --program PRJ-HOL-FOUNDING-2026 --language es` | `artifacts/exports/dossier-enisa-PRJ-HOL-FOUNDING-2026-<date>.pdf` + `.manifest.json` sidecar | Soft-success: writes `.md` sidecar if no PDF renderer installed; exit 0 |
| Company-dossier deck (14 slides) | `py scripts/export_company_deck_pdf.py` | `artifacts/exports/holistika-company-dossier-enisa-<date>.pdf` + manifest | Reads HTML preview at `docs/presentations/holistika-company-dossier/index.html`; renders 1440×810 px page size via WeasyPrint |
| Adviser handoff pack | `py scripts/export_adviser_handoff.py --engagement <slug> --adviser <slug>` | `artifacts/exports/adviser-handoff-<engagement>-<adviser>-<date>.pdf` | Bundles cover email + dossier + ledger of open questions per [`akos-adviser-engagement.mdc`](../../rules/akos-adviser-engagement.mdc) |
| UAT dossier (per-engagement post-mortem) | `py scripts/render_uat_dossier.py --uat-report <path>` | `artifacts/exports/uat-<topic>-<date>.pdf` | For internal review packs that may end up shared with operator's external advisor |
| Suez-engagement deck export (legacy) | `py scripts/render_suez_engagement_pdfs.py` | `artifacts/exports/suez-*.pdf` | Reference example of multi-deck batch |

### Manifest schema (sha256 trail)

Every PDF render writes a JSON manifest at `<pdf-stem>.manifest.json`:

```json
{
  "source_path": "docs/references/hlk/v3.0/_assets/advops/2026-holistika-incorporation/enisa_evidence/dossier_es.md",
  "source_sha256": "...",
  "rendered_path": "artifacts/exports/dossier-enisa-PRJ-HOL-FOUNDING-2026-2026-04-29.pdf",
  "render_sha256": "...",
  "rendered_at": "2026-04-29T14:23:00+02:00",
  "render_tool": "weasyprint",
  "render_version": "60.0",
  "render_program": "PRJ-HOL-FOUNDING-2026",
  "render_language": "es"
}
```

The manifest is the integrity claim that backstops the PDF when an external recipient asks "is this the version you sent me?" or "is this the bytes you say it is?". J-ENISA recipients reference the `render_sha256` in their internal trail.

### Soft-success fallback

If no PDF renderer is available locally (WeasyPrint not installed, or installation broken), `render_dossier.py` writes a markdown sidecar at the output path, prints a warning, and exits 0. **The sidecar is NOT an external-delivery artifact** — it exists so the manifest still lands and the operator has a "this attempt was made" trail. The surface remains render-pending until a real PDF lands.

When you hit a soft-success, file an entry in [`docs/wip/planning/_trackers/external-render-pending-tracker.md`](../../../docs/wip/planning/_trackers/external-render-pending-tracker.md) with: surface path, audience tags, reason ("no PDF renderer installed locally; install WeasyPrint via `pip install weasyprint`"), remediation owner, ETA.

### Verification

After any render: `py scripts/verify.py compliance_mirror_emit` (catches manifest drift); ad-hoc `Get-FileHash <pdf> -Algorithm SHA256` cross-check against `render_sha256`.

## Surface 2 — `web` (Deployed page on registered domain)

For surfaces hosted at `holistikaresearch.com`, `kirbe.com`, `hlk-erp.app`, or any other registered Holistika domain. The recipient hits an HTTP(S) endpoint and reads HTML.

### Render path

1. Author content in markdown under `boilerplate/messages/<locale>/...` (i18n strings) or `boilerplate/app/...` (rendered DOM source).
2. Build via `npm run build` in the boilerplate repo.
3. Deploy via Vercel (auto-deploy from main branch).
4. Record the deployed URL in a sibling `web-link.md` next to the markdown SSOT, with:
   ```yaml
   ---
   surface: web
   url: https://holistikaresearch.com/<path>
   deployed_at: 2026-05-19T14:00:00+02:00
   commit_sha: <boilerplate-commit>
   ---
   ```
5. The drift-gate validator looks for `web-link.md` siblings and accepts a non-empty `https://` URL on a registered domain.

### Verification

`curl -sI <url>` → 200 OK. `grep -q "<expected-prose-snippet>"` against rendered HTML to confirm the deploy carried the latest content.

### Don't

- Don't link `.md` from external prose; the recipient gets a GitHub raw URL or a 404. Link the deployed URL instead.
- Don't deploy with internal-register prose leaked in (BBR drift gate catches this).

## Surface 3 — `erp` (Sealed record inside HLK-ERP / KiRBe)

For records gated behind authenticated identity — engagement panels, partner portals, advisor dashboards.

### Render path

1. Author the record content as markdown SSOT (e.g., `engagement-summary.md`).
2. Render into the ERP via the panel-route loader (`hlk-erp/app/[panel]/[route].tsx` reads from the markdown via the data layer).
3. Record the ERP record id in a sibling `erp-record.md`:
   ```yaml
   ---
   surface: erp
   record_id: 8f4a2c1e-...-uuid
   panel: engagement
   environment: production
   created_at: 2026-05-19T14:00:00+02:00
   ---
   ```
4. The drift-gate validator looks for `erp-record.md` with a non-empty `record_id:` matching UUID-shape regex.

### Don't

- Don't expose ERP records on public routes; the surface is gated by design.
- Don't reuse markdown SSOT across the ERP panel and a public web page without two separate render trails.

## Surface 4 — `mail` (Rendered HTML body inside email)

For correspondence delivered to the recipient's inbox — not as an attachment, as the body itself.

### Render path

The pattern in this repo is: `cover_email_<topic>_<lang>.md` is the SSOT for the body content. At SMTP-send time, the markdown is rendered to HTML inline (via a future `scripts/render_cover_email.py` or via a Resend / SendGrid template flow per [`@cursor/skills`](../) email skills).

Two acceptable patterns:

**Pattern A — Inline render at send.**
- Markdown SSOT lives at `cover_email_<topic>_<lang>.md`.
- A sibling `mail-render.md` records the policy:
  ```yaml
  ---
  surface: mail
  render_policy: inline_at_send
  send_tool: resend  # or sendgrid, or smtp
  body_render_tool: markdown-it
  template_id: tpl_holistika_es_v1
  ---
  ```
- The drift-gate validator accepts `mail-render.md` siblings as render trail.

**Pattern B — Pre-rendered HTML body.**
- Markdown SSOT lives at `cover_email_<topic>_<lang>.md`.
- A paired `cover_email_<topic>_<lang>.html` is generated at author time.
- The drift-gate validator accepts paired `.html` siblings as render trail.

Pattern A is operationally simpler (no static HTML to keep in sync); Pattern B is auditable (you can see the bytes that were sent).

### Don't

- Don't put a link to the `.md` inside the email body. The recipient gets a GitHub link or worse a `file://` link that doesn't work.
- Don't paste the markdown verbatim and hope email clients render it. Markdown-as-pseudo-text in Outlook / Gmail looks wrong (literal `**bold**` markers leak through).

## Surface 5 — `slide` (Deck export — Figma frame export OR HTML-to-PDF deck render)

For 1:N or 1:1 deck-shaped artifacts.

### Render path

Two-track in this repo:

**Track A — Figma SSOT (visual + content together).**
- Visual SSOT: Figma file (recorded in `figma-link.md`).
- Slide content SSOT: `deck_slides.yaml` (parsed by `scripts/build_company_deck.py` → HTML preview).
- Export: PDF via `scripts/export_company_deck_pdf.py` (HTML → 1440×810 PDF via WeasyPrint).
- Send: PDF for sealed delivery; Figma share link for live edit collaboration.

**Track B — Markdown-to-deck (no Figma).**
- Content SSOT: `deck_<topic>.md` with section headers as slide breaks.
- Export: convert via `pandoc` → reveal.js or PDF; or via `marp-cli`.
- This pattern is rare in this repo today (the founding deck uses Track A).

### Don't

- Don't ship a Figma share link to a J-ENISA recipient (regulator wants sealed PDF, not live-edit link).
- Don't ship a `.pdf` without the Figma URL when the deck is meant to evolve (live deck stays in Figma; PDF is the snapshot at a point in time).

## Surface 6 — `broadcast` (Published 1:N surface)

For intentionally multicast surfaces — blog posts, press kits, shared deck links, registered case studies.

### Render path

1. Author content as markdown.
2. Publish to a stable URL on a registered domain.
3. Record the URL in a sibling `broadcast-link.md`:
   ```yaml
   ---
   surface: broadcast
   url: https://holistikaresearch.com/press/<topic>
   published_at: 2026-05-19T14:00:00+02:00
   audience_codes: [J-IN, J-PT]
   ---
   ```
4. The drift-gate validator looks for `broadcast-link.md` siblings.

### Distinction from `web`

- `web` is "this surface exists at a URL" — the URL might be deep-linked or hard-to-find.
- `broadcast` is "this surface is *intentionally* multicast" — promoted on social, indexed for search, reachable from the homepage.

The distinction matters for audience-tag reasoning: a press-kit page has multiple intended audiences (J-IN + J-PT + J-RC); a deep customer-portal page has one (J-CU).

## Authoring `channel:` frontmatter (forward enhancement F+4 onboarding pattern)

> Codified at Wave G B-G2 (D-IH-86-S; 2026-05-19). Companion section to Surface 0 above; this section is the *authoring craft* — when to add `channel:` to a surface's frontmatter, what registry to draw from, and what the validator does with the value at parse time.

### When to add `channel:`

Add `channel:` frontmatter when authoring or editing any markdown surface that:

1. Carries an external `audience:` tag (J-IN / J-CU / J-PT / J-AD / J-ENISA / J-RC / J-CO); AND
2. Has a known delivery path you can name (founder's outbound email; a scheduled investor meeting; a paid-ad landing page; etc.); AND
3. Is **not** a template skeleton (`artifact_kind: deck_template` etc. — those are template canonicals; downstream per-engagement instances copied from the template should carry `channel:`, not the template itself).

When you do **not** know the channel yet — e.g., you're authoring a draft that may go to multiple recipients across different paths — omit `channel:`. Per [`akos-external-render-discipline.mdc`](../../rules/akos-external-render-discipline.mdc) RULE 7, the validator no-ops on absent `channel:` (absence is not a finding). Add the field when delivery is committed.

### What channel codes to use

Pull only from existing canonical codes in [`CHANNEL_TOUCHPOINT_REGISTRY.csv`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/CHANNEL_TOUCHPOINT_REGISTRY.csv). Do NOT invent local codes per [`akos-mirror-template.mdc`](../../rules/akos-mirror-template.mdc) §"Never invent HLK IDs locally". Current registered set (Wave G B-G2 baseline):

- `CHAN-LINKEDIN-DM`, `CHAN-LINKEDIN-POST-RESPONSE` — LinkedIn-class
- `CHAN-EMAIL-INBOUND` — inbound to holistika@ shared inbox
- `CHAN-DIRECT-DM` — bidirectional founder-personal-channel (covers founder's outbound personal email + WhatsApp + SMS)
- `CHAN-WEB-FORM`, `CHAN-SEARCH-ORGANIC`, `CHAN-AD-CAMPAIGN` — site-class inbound
- `CHAN-CAL-SCHEDULE` — scheduled-meeting inbound
- `CHAN-PARTNER-REFERRAL` — bridged inbound
- `CHAN-EVENT-MEETING` — bidirectional live event / video meeting

When no existing code fits cleanly (e.g., you're authoring a J-ENISA cover email and want `CHAN-EMAIL-OUTBOUND` specifically — not minted as of Wave F), prefer:

1. The closest existing bidirectional code (`CHAN-DIRECT-DM` covers founder-outbound personal email per the registry `notes` column).
2. Omit `channel:` until the new code is minted via canonical-CSV gate.
3. **Never** invent a local code. The drift gate reports unknown codes at INFO advisory, but the discipline is to keep the unknown-code counter at 0 — every populated `channel:` field FK-resolves cleanly.

### Multi-channel composition

Compose multiple channels when delivery is multi-path. Common patterns:

```yaml
channel: [CHAN-EVENT-MEETING, CHAN-DIRECT-DM]   # deck presented + sealed-PDF follow-up
channel: [CHAN-SEARCH-ORGANIC, CHAN-AD-CAMPAIGN] # public page + paid amplification
channel: [CHAN-DIRECT-DM]                        # founder-initiated outbound (default)
```

### Reusable snippet template

The canonical authoring template lives at [`docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/_templates/external-render/channel-frontmatter.snippet.md`](../../../docs/references/hlk/v3.0/Envoy%20Tech%20Lab/Repositories/_templates/external-render/channel-frontmatter.snippet.md). It carries the snippet body + lookup procedure + 3 realistic case blocks (founder-initiated outbound; web + paid-ad; deck used in meeting + sent as sealed). Copy from there when adding `channel:` to a new surface.

### What happens at validation time

When the surface lands in CI:

1. [`scripts/validate_external_render_trail.py`](../../../scripts/validate_external_render_trail.py) parses the YAML frontmatter and extracts the `channel:` value.
2. Each `CHAN-*` code is FK-resolved against the registry's `channel_id` column.
3. Unknown codes emit a per-file INFO finding `unknown-channel-code: <CHAN-X> at <surface>`. Never fails CI.
4. The validator summary line includes `with channel-tag <N>` and `unknown channel codes <M>` counters. The discipline is `M == 0` always; `N` grows over time as more surfaces get tagged.

### Forward enhancement (out of Wave G scope)

- **Mint `CHAN-EMAIL-OUTBOUND` + `CHAN-PDF-DOWNLOAD`** in `CHANNEL_TOUCHPOINT_REGISTRY.csv` to cover the two most common gaps surfaced during the Wave G B-G2 onboarding sweep. Requires canonical-CSV operator gate per [`akos-governance-remediation.mdc`](../../rules/akos-governance-remediation.mdc) §"HLK compliance governance". Until minted, use `CHAN-DIRECT-DM` (bidirectional founder-personal) as the closest fit for outbound dossier/cover-email surfaces.
- **Promote `channel:` from optional to required** for in-scope external surfaces once the registry covers all common gaps. The promotion would mirror the RULE 6 INFO→FAIL ramp pattern (Wave F precedent); deferred to a successor wave.

## Pre-render checklist (10 items; walk before any render)

Before invoking any render command:

1. **Is the source markdown jargon-clean?** Run `py scripts/validate_brand_baseline_reality_drift.py` against the source path; fix any internal-register tokens before rendering.
2. **Is the audience tag correct?** Source markdown's `audience:` frontmatter must list exactly the audience class(es) this render targets. If multiple audiences will receive the same render, list multiple codes.
3. **Is the output path under `artifacts/exports/`?** PDFs and other rendered binaries go there, never under `docs/`.
4. **Will the manifest land?** Confirm the render script writes a `.manifest.json` sidecar; if not, the script needs updating before this render counts as a real render-trail.
5. **Is the source-of-truth path correct?** When a deck or dossier exists in multiple language versions, render the language the recipient reads — `--language es` for Spanish-speaking advisors; `--language en` for ENISA-EN if applicable.
6. **Is the program / engagement context correct?** Most render scripts take a `--program` flag (e.g., `PRJ-HOL-FOUNDING-2026`); double-check it's the right one.
7. **Will the soft-success path produce a misleading artifact?** If WeasyPrint isn't installed, the script writes a `.md` sidecar; if you ship that to the recipient, you've shipped markdown. Always verify the rendered file is actually a PDF (`file <path>.pdf` should report PDF document, not ASCII text).
8. **Has the prior render's sha256 been logged for diff comparison?** When re-rendering an updated dossier, you want the manifest to show the source change, not just a new timestamp on identical bytes.
9. **Is the recipient's identity registered?** External delivery to advisors / certifiers / regulators should be logged in `OPS_REGISTER.csv` per [`akos-adviser-engagement.mdc`](../../rules/akos-adviser-engagement.mdc) — the OPS row carries the recipient + send method + render artifact + delivery confirmation.
10. **Do you actually need to render right now?** If the recipient hasn't asked yet, pre-rendering creates time-stamped artifacts that may go stale before send. Render at the point of send.

## Anti-patterns (what NOT to do)

- **Anti-pattern 1: Attaching `.md` to email.** External recipients should not see raw markdown ever. If you can't render a PDF right now, defer the send and file a render-pending tracker entry. Don't degrade to attaching markdown.
- **Anti-pattern 2: Sharing GitHub raw URLs.** A `https://github.com/.../raw/main/<path>.md` URL exposes both internal commit SHAs and the markdown view. External recipients shouldn't be reading from your version control surface.
- **Anti-pattern 3: Rendering once and never re-rendering.** When the source markdown changes, the rendered artifact goes stale. Re-render at every send-event, and update the manifest.
- **Anti-pattern 4: Skipping the manifest.** A PDF without a manifest is bytes without provenance. The manifest is the integrity claim.
- **Anti-pattern 5: Mixing audience-tags incorrectly.** A surface tagged `audience: [J-IN, J-OP]` violates the J-OP exclusion rule (D-IH-85-D); J-OP is internal-only. Re-tag accordingly.
- **Anti-pattern 6: Promoting `.md` SSOT to be the delivery artifact.** "But the recipient is technical and can read markdown" — no. The discipline is the discipline. Render anyway.
- **Anti-pattern 7: Silent backfill.** Authoring a new external surface without a paired render trail and assuming "we'll get to it later" is how render debt accumulates. Co-mint render trail in the same commit.

## Recovery patterns (when things go wrong)

- **No PDF renderer installed.** Install WeasyPrint via `pip install weasyprint` (Linux/macOS) or `pip install weasyprint && python -c "import weasyprint"` to confirm. On Windows: WeasyPrint requires GTK; alternative is to use `wkhtmltopdf` (binary install) or render via cloud function. File a render-pending entry while the install lands.
- **Render succeeded but content is wrong.** Re-render with the corrected source markdown; update the manifest to point at the new `source_sha256`; commit both atomically.
- **Manifest drift detected.** `validate_external_render_trail.py` flags the surface as render-stale. Re-render and update.
- **Recipient asks for a markdown copy.** Render to PDF and send the PDF; if the recipient genuinely needs markdown (rare; most don't), confirm via inline-ratify gate and consider whether the recipient should be tagged J-CO (collaborator, internal-trust-tier) instead of an external class.

## Cross-references

- [`.cursor/rules/akos-external-render-discipline.mdc`](../../rules/akos-external-render-discipline.mdc) — the *when* layer of this skill.
- [`.cursor/rules/akos-brand-baseline-reality.mdc`](../../rules/akos-brand-baseline-reality.mdc) — the vocabulary-register axis (orthogonal to delivery format).
- [`.cursor/rules/akos-adviser-engagement.mdc`](../../rules/akos-adviser-engagement.mdc) — adviser-specific render-pack discipline.
- [`AUDIENCE_REGISTRY.csv`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/AUDIENCE_REGISTRY.csv) — the FK source for audience tags.
- [`scripts/validate_external_render_trail.py`](../../../scripts/validate_external_render_trail.py) — the drift gate.
- [`docs/wip/planning/_trackers/external-render-pending-tracker.md`](../../../docs/wip/planning/_trackers/external-render-pending-tracker.md) — the render-pending governance shape.
- [`scripts/render_dossier.py`](../../../scripts/render_dossier.py), [`scripts/export_company_deck_pdf.py`](../../../scripts/export_company_deck_pdf.py), [`scripts/export_adviser_handoff.py`](../../../scripts/export_adviser_handoff.py) — the primary three render scripts for current external-delivery flows.
