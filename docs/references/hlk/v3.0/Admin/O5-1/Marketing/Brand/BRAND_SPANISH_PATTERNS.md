---
status: active
role_owner: Brand Manager
area: Marketing
entity: Holistika
program_id: shared
topic_ids:
  - topic_brand_voice
artifact_role: canonical
intellectual_kind: brand_asset
authority: Operator (lived protocols)
last_review: 2026-04-29
---

# BRAND_SPANISH_PATTERNS

> **Status — Active (Initiative 24 follow-up; Operator-supplied 2026-04-29).** Hand-authored companion to [`BRAND_VOICE_FOUNDATION.md`](BRAND_VOICE_FOUNDATION.md) capturing concrete Spanish-language patterns from real Holistika ↔ external-counsel exchanges. Cited by the composer (`scripts/compose_adviser_message.py`) when `language_preference: es` resolves at Layer 4. Operator-curated; **not** auto-rendered by the wave2 scaffolder. Edits land via direct PR.

## Why this exists

The brand voice charter and archetype (in [`BRAND_VOICE_FOUNDATION.md`](BRAND_VOICE_FOUNDATION.md)) are language-agnostic. Spanish is a deeply registered language — *tú/usted*, regional formality conventions, professional-services etiquette — and our adviser engagements are predominantly Spanish. This companion captures **lived patterns from real exchanges** so the composer (and the operator at Layer 4) can land messages that read naturally to Spanish-speaking advisers.

## Reference exchange — `POI-LEG-ENISA-LEAD-2026` ↔ Founder (2026-04-07)

Real-world exchange that anchors the patterns below. Captured here verbatim with surface PII (the adviser's direct phone + email signature) **redacted**. Adviser identity → `POI-LEG-ENISA-LEAD-2026` (canonical ref_id; real name, firm, and signature kept off-repo per Initiative 21 D-CH-1).

### Adviser opener (formal, *usted*)

> Buenos días,
>
> Soy Guillermo, asesor jurídico de [GOI-ADV-ENTITY-2026], ¡encantado!
>
> Voy a ser la persona encargada de gestionar el trámite de certificación de Start Up por ENISA, por lo que me gustaría me indicase su disponibilidad para poder llamarlo y que hablásemos acerca de la empresa.
>
> Muchas gracias,
>
> Un saludo

**Pattern signals**:

- Salutation: `Buenos días,` (not `Hola`).
- Self-introduction with **first name + role + firm** in the first sentence.
- Explicit purpose statement (**"Voy a ser la persona encargada de…"**).
- *Usted* form: `me indicase`, `llamarlo`, `acerca de la empresa`.
- Warm closer: `¡encantado!` and `Muchas gracias, Un saludo`.

### Founder reply (warm peer, *tú*)

> Buenos días, Guillermo,
>
> Muchas gracias por el contacto. Igualmente, un placer saludarte!
>
> Respecto a mi disponibilidad, hoy estaré disponible hasta el final de la tarde. Mañana podré atender tu llamada a partir de las 12:00 h.
>
> Un saludo,
>
> Fayçal Njoya

**Pattern signals**:

- Salutation: `Buenos días, [first name],` — adopts the adviser's first name (warmer than name-less `Buenos días,`).
- **Mixed register**: greeting acknowledges them as a peer (`saludarte`, *tú*), but the message body stays clear and structured (`Respecto a mi disponibilidad, hoy estaré disponible hasta…`).
- **Concrete availability**: "hoy estaré disponible hasta el final de la tarde. Mañana podré atender tu llamada a partir de las 12:00 h" — no vagueness, no "let me know what works"; specific windows.
- Warm but compact: `Igualmente, un placer saludarte!` once, then straight to substance.
- Closer: `Un saludo,` (not `Saludos cordiales,` which would be formal-cool, nor `Abrazos,` which would be too informal for a first contact).

### Adviser confirmation (terse, *usted*)

> Buenos días,
>
> Perfecto, mañana a las 13.15 le llamo.
>
> Un saludo

**Pattern signals**:

- One-line confirmations stay one-line; no padding.
- Spanish AM/PM uses 24h with a dot (`13.15`) or comma (`13,15`); the dot is more common in legal correspondence.
- *Usted* preserved (`le llamo`).

### Founder confirmation (warm, brief)

> Perfecto, hasta mañana!

**Pattern signals**:

- For confirmations, single-line replies are correct — over-formalising "Perfecto, hasta mañana!" to "Perfecto, quedamos así para mañana, le agradezco mucho su disponibilidad" would feel performative (matches `voice_is_not.Performative`).
- Exclamation `!` is acceptable for warm sign-off; advisers will not read it as unprofessional in B2B Spanish.

## Patterns to follow

| When... | Holistika does | Holistika does NOT |
|:--------|:---------------|:-------------------|
| First contact reply | "Buenos días, [name], Muchas gracias por el contacto." | "Hola [name], gracias por escribirnos." (too informal for legal contexts) |
| Acknowledging an adviser introduction | Mirror their first name + light warmth (`Igualmente, un placer saludarte!`) | Reciprocate the firm's branded sign-off back at them |
| Stating availability | Concrete windows (`hoy hasta el final de la tarde`, `mañana a partir de las 12:00 h`) | "Cuando le venga bien" or "Soy flexible" |
| Confirming a slot | Match the adviser's level of brevity ("Perfecto, hasta mañana!") | Re-quote the slot back ("Perfecto, quedamos a las 13:15…") unless a different time was proposed |
| Sign-off | `Un saludo,` (peer/warm) for ongoing rapport; `Saludos cordiales,` for first-contact formal | `Atentamente,` (over-formal) or `Cordialmente,` (lawyer-cold) for peer rapport |
| Pronoun register | Match the recipient's profile in `GOI_POI_REGISTER.csv` `pronoun_register` (already set: `tu` for ENISA-track adviser; `usted` for fiscal/banking) | Switch register mid-thread — keep it consistent |

## Patterns to refuse

Anchored in `voice_is_not` (Performative / Vague / Jargon-heavy):

- **Performative humility**: "Sería un honor poder colaborar con usted." → use "Encantado de colaborar.".
- **Performative gratitude**: "Le agradezco infinitamente su atención y dedicación a este asunto." → use "Muchas gracias por la gestión.".
- **Vague timeframes**: "Le confirmaré los detalles en breve" → state when (`Le confirmo el martes, antes de las 12:00`).
- **Empty corporate filler**: "En el contexto de nuestras conversaciones..." → just say what's true.
- **Anglicism stuffing**: "Vamos a aplicar un approach holístico para de-riskear el engagement" → use plain Spanish (`Vamos a estructurar la operación así para reducir el riesgo:`). The brand IS rigorous, NOT jargon-heavy ([`BRAND_DO_DONT.md`](BRAND_DO_DONT.md)).

## Salutation matrix (regional + register)

| Recipient context | Salutation | Closing |
|:------------------|:-----------|:--------|
| First contact, adviser firm (Spain) | `Buenos días,` (or `Buenas tardes,` after 14:00) | `Muchas gracias, Un saludo,` |
| Ongoing, peer-rapport adviser | `Buenos días, [first name],` | `Un saludo,` |
| Formal, regulator / banking desk | `Estimado/a [Sr./Sra.] [last name]:` | `Atentamente, [Founder name]` |
| Internal Holistika team (es) | `Hola [first name],` | `Un saludo,` |
| LinkedIn DM (warm, Spain) | `Hola [first name], encantado/a` | `Un saludo,` |

The composer's [`BRAND_REGISTER_MATRIX.md`](BRAND_REGISTER_MATRIX.md) lookup picks the **register** for each `(relationship, channel)`; this matrix picks the **opener / closer phrasing** within that register when `language_preference: es`.

## How the composer uses this

When `language_preference: es` resolves at Layer 4:

1. The composer's draft scaffold (status: draft, frontmatter, "Layer 4 — Eloquence" TODO) remains in English (operator authoring scaffold).
2. The **operator-authored prose** in Layer 4 should follow the patterns above.
3. The composer's **per-discipline templates** under `templates/email/` (when shipped) read these patterns to seed the salutation + closer based on `(relationship, channel, language_preference)`.

## Maintenance

- **Append-only** for now — every real exchange that surfaces a new pattern (regional variation, jargon to refuse, register edge case) gets a one-paragraph entry under "Patterns to follow" / "Patterns to refuse".
- **Source citation**: when a pattern comes from a real exchange, cite the GOI/POI `ref_id` and the date. Real names + raw transcripts stay off-repo per `SOP-HLK_TRANSCRIPT_REDACTION_001.md`.
- **Annual review** with the Brand Manager in lockstep with [`BRAND_VOICE_FOUNDATION.md`](BRAND_VOICE_FOUNDATION.md) (D-IH-17 cadence).

## Related

- [`BRAND_VOICE_FOUNDATION.md`](BRAND_VOICE_FOUNDATION.md) — language-agnostic charter + archetype + pillars.
- [`BRAND_REGISTER_MATRIX.md`](BRAND_REGISTER_MATRIX.md) — `(relationship, channel) → register` lookup (auto-rendered).
- [`BRAND_DO_DONT.md`](BRAND_DO_DONT.md) — voice IS / IS NOT (auto-rendered).
- [`SOP-HLK_COMMUNICATION_METHODOLOGY_001.md`](SOP-HLK_COMMUNICATION_METHODOLOGY_001.md) — 4-layer methodology; Layer 4 references this companion.
- [`SOP-HLK_TRANSCRIPT_REDACTION_001.md`](../../People/Compliance/SOP-HLK_TRANSCRIPT_REDACTION_001.md) — redaction discipline for transcripts and quoted exchanges.
- Cross-program glossary §"Voice register": [`docs/reference/glossary-cross-program.md`](../../../../../../reference/glossary-cross-program.md).
