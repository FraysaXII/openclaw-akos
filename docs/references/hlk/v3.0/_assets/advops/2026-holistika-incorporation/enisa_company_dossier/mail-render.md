---
status: active
classification: render-trail-sidecar
intellectual_kind: mail_render_policy
authority: Brand Manager
artifact_role: derived
ratifying_decisions: [D-IH-86-P]
parent_surface: cover_email_company_dossier_es.md
language: en
last_review: 2026-05-19
audience: J-OP
---

# Mail render policy — `cover_email_company_dossier_es.md`

Records the mail-rendering policy for [`cover_email_company_dossier_es.md`](cover_email_company_dossier_es.md) (J-ENISA cover email body for the 14-slide company dossier handoff) per `akos-external-render-discipline.mdc` RULE 4 mail heuristic + paired skill `.cursor/skills/external-render-craft/SKILL.md` Surface 4 Pattern A.

## Render policy

```yaml
surface: mail
render_policy: inline_at_send
send_tool: resend  # or sendgrid, smtp; selected at send-event
body_render_tool: markdown-it
template_id: tpl_holistika_es_v1
recipient_audience_codes: [J-ENISA]
recipient_program_id: PRJ-HOL-FOUNDING-2026
deck_attachment: artifacts/exports/holistika-company-dossier-enisa-<latest>.pdf
last_render_at_send: null
last_render_sha256: null
```

## Send-time render

When this email is sent to a J-ENISA recipient:

1. Read [`cover_email_company_dossier_es.md`](cover_email_company_dossier_es.md) as the body SSOT.
2. Render markdown → HTML inline via `markdown-it`.
3. Capture body sha256 at send-time and append to the OPS row that records the send.
4. Attach `artifacts/exports/holistika-company-dossier-enisa-<latest>.pdf` (the 14-slide deck) to the same email envelope. Latest at this commit: `holistika-company-dossier-enisa-2026-05-19.pdf`.

## Render trail check

This sidecar satisfies the mail heuristic of [`scripts/validate_external_render_trail.py`](../../../../../../../scripts/validate_external_render_trail.py) for the parent surface.
