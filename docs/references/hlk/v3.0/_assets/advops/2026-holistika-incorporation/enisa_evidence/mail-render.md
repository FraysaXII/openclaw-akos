---
status: active
classification: render-trail-sidecar
intellectual_kind: mail_render_policy
authority: Brand Manager
artifact_role: derived
ratifying_decisions: [D-IH-86-P]
parent_surface: cover_email_es.md
language: en
last_review: 2026-05-19
audience: J-OP
---

# Mail render policy — `cover_email_es.md`

Records the mail-rendering policy for [`cover_email_es.md`](cover_email_es.md) (J-ENISA cover email body) per `akos-external-render-discipline.mdc` RULE 4 mail heuristic + paired skill `.cursor/skills/external-render-craft/SKILL.md` Surface 4 Pattern A.

## Render policy

```yaml
surface: mail
render_policy: inline_at_send
send_tool: resend  # or sendgrid, smtp; selected at send-event
body_render_tool: markdown-it
template_id: tpl_holistika_es_v1
recipient_audience_codes: [J-ENISA]
recipient_program_id: PRJ-HOL-FOUNDING-2026
last_render_at_send: null  # populated at first SMTP send
last_render_sha256: null   # captured at SMTP send-time per akos-adviser-engagement.mdc
```

## Send-time render

When this email is sent to a J-ENISA recipient:

1. Read [`cover_email_es.md`](cover_email_es.md) as the body SSOT.
2. Render markdown → HTML inline via `markdown-it` (Resend SDK supports React Email templates which use markdown-it under the hood) OR via the `scripts/render_cover_email.py` (mint when first send happens, per the future enhancement note).
3. Capture body sha256 at send-time and append to the OPS row that records the send (per `akos-adviser-engagement.mdc` SOP-EXTERNAL_ADVISER_ENGAGEMENT_001 §"Send-time evidence trail").
4. Attach the corresponding sealed dossier PDF (`artifacts/exports/dossier-enisa-PRJ-HOL-FOUNDING-2026-<latest>.pdf`) to the same email envelope.

## Render trail check

This sidecar satisfies the mail heuristic of [`scripts/validate_external_render_trail.py`](../../../../../../../scripts/validate_external_render_trail.py) for the parent surface. Body content is rendered at send-time, not pre-rendered to a static `.html` on disk.
