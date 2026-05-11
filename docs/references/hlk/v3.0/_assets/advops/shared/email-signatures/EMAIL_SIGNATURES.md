---
status: active
classification: canonical
access_level: 4
language: en
register: external
artifact_kind: email_signature_templates
role_owner: Brand Manager
area: MKT
entity: Think Big
linked_initiative: I66
linked_decisions:
  - D-IH-66-A
  - D-IH-66-O
governance:
  - BRAND_TEMPLATE_REGISTRY.md
  - BRAND_LOGO_SYSTEM.md
last_review: 2026-05-09
---

# Email Signature Templates

> External-register signature source. Keep signatures short; the email body carries context. The signature only proves identity, legal entity, and brand architecture.

## Standard Founder Signature

```text
Faycal Njoya
Founder, Holistika Research SL

Holistika
Strategy. Execution. Technology.
holistikaresearch.com
```

## Standard Team Signature

```text
[Name]
[Role], Holistika Research SL

Holistika
Strategy. Execution. Technology.
holistikaresearch.com
```

## Sub-Mark Context Line

Use only when the conversation is already about a specific delivery mode.

```text
[Name]
[Role], Holistika Research SL
[Holistika R&S / Think Big / HLK Tech Lab]

holistikaresearch.com
```

## Legal Footer (Optional, Long-Form Threads)

```text
Holistika Research SL is a Spanish limited liability company. Holistika, Holistika R&S, Think Big, HLK Tech Lab, MADEIRA, KiRBe, and ENVOY are trademarks or pending trademarks of Holistika Research SL.
```

Use the legal footer only on contracts, proposals, funding, legal, or formal partner threads. Do not add it to every short email.

## HTML Skeleton

```html
<table role="presentation" cellpadding="0" cellspacing="0" style="font-family: Inter, Arial, sans-serif; color: #282d36;">
  <tr>
    <td style="font-size: 14px; line-height: 20px; font-weight: 600;">[Name]</td>
  </tr>
  <tr>
    <td style="font-size: 13px; line-height: 20px; color: #62666f;">[Role], Holistika Research SL</td>
  </tr>
  <tr>
    <td style="padding-top: 8px; font-size: 13px; line-height: 20px;">Holistika</td>
  </tr>
  <tr>
    <td style="font-size: 12px; line-height: 18px; color: #62666f;">Strategy. Execution. Technology.</td>
  </tr>
  <tr>
    <td style="padding-top: 8px; font-size: 12px; line-height: 18px;"><a href="https://holistikaresearch.com" style="color: #2b9077;">holistikaresearch.com</a></td>
  </tr>
</table>
```

## Rules

- Use `Holistika Research SL` for the legal entity.
- Use `Holistika` for the umbrella brand.
- Do not use stylized diacritics in plain-text legal signatures.
- Do not include internal codenames, private repo names, or operator-only process labels.
- Do not list every product brand unless the thread is legal, funding, or IP-specific.
