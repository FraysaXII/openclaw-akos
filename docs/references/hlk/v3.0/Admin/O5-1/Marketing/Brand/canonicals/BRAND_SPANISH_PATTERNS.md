---
language: en
status: active
role_owner: Brand & Narrative Manager
area: Marketing
entity: Holistika Research SL
program_id: shared
topic_ids:
  - topic_brand_voice
artifact_role: canonical
intellectual_kind: brand_asset
authority: Founder + Brand Manager
last_review: 2026-05-08
ssot: true
---
# BRAND_SPANISH_PATTERNS

> **Status — Active (Initiative 24 follow-up; Operator-supplied 2026-04-29; substantially expanded Initiative 66 P1 2026-05-08).** Hand-authored companion to [`BRAND_VOICE_FOUNDATION.md`](BRAND_VOICE_FOUNDATION.md) capturing concrete Spanish-language patterns from real Holistika ↔ external-counsel + advisor + customer exchanges. Cited by the composer (`scripts/compose_adviser_message.py`) when `language_preference: es` resolves at Layer 4. Operator-curated; **not** auto-rendered by the wave2 scaffolder. Edits land via direct PR.
>
> **I66 P1 expansion (2026-05-08):** added §10 (additional patterns from operator-supplied 2026-04 transcripts), §11 (sub-mark voice differentiation), §12 (per-audience register sub-tables), §13 (boilerplate ES copy alignment), and updated cross-references for D-IH-66-D (deep voice canonicals) + D-IH-66-A (sub-mark architecture).

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

## 10. I66 P1 expansion — additional patterns from 2026-04 transcripts

Operator supplied multiple Spanish-language exchanges in 2026-04 covering: hospitality consulting (Consultoría Hostelería), founder incorporation calls (Constitución Sociedad — Alcance + Fiscal + ENISA), and internal Holistika onboarding (Researcher + Business Developer). PII redacted per [`SOP-HLK_TRANSCRIPT_REDACTION_001.md`](../../People/Compliance/SOP-HLK_TRANSCRIPT_REDACTION_001.md). The patterns below are **additive** to §1–§9 (preserved verbatim).

### 10.1 Hospitality consulting opener (peer, *tú* by mutual consent)

Hospitality-sector SME consulting reads warmer than legal counsel exchanges. Once the prospect initiates *tú*, the founder mirrors:

> Hola [Prénom], te paso lo que hablamos esta mañana:
>
> - Lo de la facturación y las propinas: lo dejamos para la próxima sesión, no es bloqueante.
> - El plan de admin que armamos: te mando el documento esta tarde antes de las 19h.
> - La duda de Purview: confirmo con el equipo y te respondo mañana antes del mediodía.

**Pattern signals:**

- `Hola [Prénom],` opener (warm; matches initiated *tú*).
- **List with 3 items + concrete deadlines per item** (`esta tarde antes de las 19h`, `mañana antes del mediodía`).
- `no es bloqueante` — adopts **operator framing** (something either blocks the engagement or doesn't); SMEs in hospitality respond well to deblocking-language because their margin is tight.
- `lo dejamos para` — collaborative phrasing (we decide together, not "I decide for you").

### 10.2 Founder-incorporation kickoff (formal, *usted* default)

When the counterparty is the legal/fiscal advisor and the relationship is professional-services (not internal staff or hospitality SME):

> Buenos días, [Nombre]:
>
> Le confirmo que estaremos disponibles el lunes a las 11:00 h para la sesión de kick-off de constitución.
>
> Adjunto:
>
> - el borrador del business plan (versión 0.3),
> - la previsión a 18 meses (hoja "Forecast 18M"),
> - los KYC personales de los socios.
>
> Si necesita algún documento adicional antes del lunes, por favor indíquemelo hoy antes de las 18:00 h.
>
> Atentamente,
>
> Fayçal Njoya

**Pattern signals:**

- `Buenos días, [Nombre]:` opener with colon (`:`) instead of comma — formal Spanish convention for legal/fiscal correspondence.
- *Usted* maintained: `Le confirmo`, `indíquemelo`.
- **Document list with parenthetical version metadata** (`versión 0.3`, `hoja "Forecast 18M"`) — signals professional engagement.
- **Concrete deadline for upstream feedback** (`hoy antes de las 18:00 h`).
- `Atentamente,` (formal close; not `Un saludo,` which would be peer-warm).

### 10.3 Internal onboarding (Holistika team member, *tú* default)

Internal Spanish prose uses *tú* by default; this is the Holistika internal-team baseline:

> Hola [Prénom], bienvenido al equipo!
>
> Antes de la primera sesión del miércoles, te comparto el contexto:
>
> - Quiénes somos y qué hacemos: [link al brand brief]
> - Lo que estás a punto de aprender: cómo investigamos, cómo decidimos, cómo entregamos.
> - Lo que vamos a esperar de ti las primeras dos semanas: lectura + observación + dos preguntas a la semana mínimo.

**Pattern signals:**

- `Hola [Prénom], bienvenido al equipo!` — exclamation acceptable in internal/onboarding context.
- **Triadic structure** (`cómo investigamos, cómo decidimos, cómo entregamos`) — Spanish rhetorical preference for triads matches the internal voice (research → decision → delivery is the internal Holistika frame).
- **Concrete expectation** (`dos preguntas a la semana mínimo`) — sets the bar without sounding hierarchical.

## 11. Sub-mark voice differentiation (D-IH-66-A + D-IH-66-B)

Per the Branded House decision in [`BRAND_ARCHITECTURE.md`](BRAND_ARCHITECTURE.md) Layer 3, the three operational sub-marks (Holistika R&S, Think Big, HLK Tech Lab) carry slightly different ES voice flavors that **never break the umbrella voice**, only soften it for context:

<!-- vale off -->

| Sub-mark | ES voice flavor | Example phrase |
|:---|:---|:---|
| **Holistika R&S** | Most peer-grade; authoritative-but-warm; mirrors academic register without the academic stiffness | `Lo que la evidencia hasta ahora nos sugiere es que...` |
| **Think Big (consulting)** | Most action-oriented; less hedge-laden than R&S; closer to operational direction | `Recomendamos avanzar con la opción B; te explico por qué.` |
| **HLK Tech Lab (technology)** | Most technical; tolerates more anglicisms (API, SaaS, runtime) but never marketing-jargon (transformative, paradigm-shifting); precision-oriented | `El runtime ahora soporta tres proveedores; falla deterministamente si el primario cae.` |

<!-- vale on -->

The Tier-1 umbrella voice remains the master — sub-mark voices may **soften** that master, never contradict it. Operators copying from one sub-mark surface to another should re-read the target sub-mark's voice signature first.

## 12. Per-audience register sub-tables

Different external audiences in the Spanish-speaking world expect slightly different register signals. This sub-table extends §3's salutation-matrix:

### 12.1 Investor — Spain-based VC partner

| Pattern | Default |
|:---|:---|
| Opener | `Buenos días, [Prénom],` (peer-warm; investors prefer not to be addressed as `Estimado Sr./Sra.` in B2B Spain — that would feel old-school) |
| Address form | *usted* in first contact; *tú* if mutual rapport develops by exchange 3 |
| Closer | `Un saludo,` |
| Forbidden | Anglicism-stuffing; investors filter by **Spanish-language fluency signal** as a proxy for operator credibility |

### 12.2 Customer — Spain-based SME owner

| Pattern | Default |
|:---|:---|
| Opener | `Hola [Prénom],` (most SME owners initiate *tú* immediately; mirror them) |
| Address form | *tú* almost universally |
| Closer | `Un saludo,` then `Saludos,` after rapport |
| Critical move | **Concrete pricing language** — never `consulta el pricing` (anglicism + vague); say `el coste es 8.000 € por dos meses, IVA aparte` |

### 12.3 ENISA reviewer

| Pattern | Default |
|:---|:---|
| Opener | `Buenos días, [Prénom Nom],` (full name; formal) |
| Address form | *usted* throughout (regulatory context) |
| Closer | `Atentamente,` |
| Critical move | **Substantiation-density** — every claim followed by a number, document reference, or operator-confirmable fact |

### 12.4 Madrid-based legal counsel (extends §1's reference exchange)

(Already canonical in §1.)

### 12.5 LATAM-based partner or customer

LATAM Spanish has subtle differences from peninsular Spanish. The default pattern:

| Pattern | LATAM adjustment |
|:---|:---|
| Opener | `Buen día, [Prénom],` (Argentina, Mexico, Colombia variation; "Buenos días" works everywhere but "Buen día" reads warmer in LATAM) |
| Address form | *usted* in formal contexts (Mexico, Colombia, Peru lean formal); *tú* in Argentina/Chile peer contexts |
| Forbidden | Peninsular-Spanish-only forms (`coche` — use `auto` or `carro`; `móvil` — use `celular`; `vale` — drop entirely) |
| Closer | `Saludos cordiales,` (more universal in LATAM than `Un saludo,`) |

If the recipient's `GOI_POI_REGISTER.csv` field `pronoun_register` is `usted` and the country is in {MX, CO, PE, EC}, the LATAM-formal pattern applies.

## 13. Boilerplate ES copy alignment

The boilerplate Spanish copy (per [I66 P5](../../../../wip/planning/66-brand-vision-ops-sweep/master-roadmap.md#p5-public-surfaces-rewrite-6d) deliverable, served at `holistikaresearch.com/es/`) follows these patterns. The validator `validate_brand_voice_register.py` (P2) will scope to `boilerplate/messages/es.json` and flag:

- Performative humility (forbidden tokens: `humildemente`, `seríamos honrados`, etc.)
- Anglicism stuffing (forbidden in body prose: `pricing`, `engagement`, `mindset`, `growth`, `framework`; allowed in technical sections: `API`, `cloud`, `SaaS`).
- Vague-time language (`a la mayor brevedad posible` flagged as drift).
- Over-formal address forms in marketing prose (Holistika is peer-grade; `Estimados Sres.` reads as bureaucratic).

## Related

- [`BRAND_VOICE_FOUNDATION.md`](BRAND_VOICE_FOUNDATION.md) — language-agnostic charter + archetype + pillars.
- [`BRAND_FRENCH_PATTERNS.md`](BRAND_FRENCH_PATTERNS.md) — the FR canonical equivalent (parallel structure; promoted from stub I66 P1).
- [`BRAND_ARCHITECTURE.md`](BRAND_ARCHITECTURE.md) — Branded House layer-3 sub-marks (relevant to §11).
- [`BRAND_REGISTER_MATRIX.md`](BRAND_REGISTER_MATRIX.md) — `(relationship, channel) → register` lookup (auto-rendered).
- [`BRAND_DO_DONT.md`](BRAND_DO_DONT.md) — voice IS / IS NOT (auto-rendered).
- [`SOP-HLK_COMMUNICATION_METHODOLOGY_001.md`](SOP-HLK_COMMUNICATION_METHODOLOGY_001.md) — 4-layer methodology; Layer 4 references this companion.
- [`SOP-HLK_TRANSCRIPT_REDACTION_001.md`](../../People/Compliance/SOP-HLK_TRANSCRIPT_REDACTION_001.md) — redaction discipline for transcripts and quoted exchanges.
- Cross-program glossary §"Voice register": [`docs/reference/glossary-cross-program.md`](../../../../../../reference/glossary-cross-program.md).
