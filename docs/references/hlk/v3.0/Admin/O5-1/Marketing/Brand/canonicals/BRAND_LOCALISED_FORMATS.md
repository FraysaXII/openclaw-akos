---
language: en
status: active
sop_id: BRAND-LOCALISED-FORMATS-001
role_owner: Brand & Narrative Manager
area: Marketing
entity: Holistika Research SL
program_id: shared
topic_ids:
  - topic_brand_voice
artifact_role: canonical
intellectual_kind: discipline_canonical
authority: Founder + Brand Manager + Copywriter
classification: way_of_working
last_review: 2026-05-14
ssot: true
authored: 2026-05-14
companion_to:
  - BRAND_MULTILINGUAL_CONTRACT.md
  - BRAND_FRENCH_PATTERNS.md
  - BRAND_SPANISH_PATTERNS.md
  - BRAND_ENGLISH_PATTERNS.md
  - ../UX Designer/canonicals/BRAND_GANTT_DISCIPLINE.md
  - ../../akos/brand_voice_register.py
---

# BRAND_LOCALISED_FORMATS — Per-locale number / currency / date format discipline

> **Status — Active (Initiative 71 P2; Addition 11 fold-in from the I71 P1 Round 3 Tier-3 surface).** This canonical codifies the **per-locale formatting rules** for numbers, currencies, and dates that any Holistika external-register deliverable must follow. The validator chassis at [`akos/brand_voice_register.py`](../../../../../../../akos/brand_voice_register.py) ships the typed `NumberFormatRule` / `CurrencyFormatRule` / `DateFormatRule` Pydantic surfaces that read these rules into the runtime; the surfaces stay empty (graceful no-op) until this canonical lands on disk, at which point the parser activates per the I71 P2 design-time pick (rule cardinality stays under the sibling-spinout threshold).

## 1. Number formats

Per [Unicode CLDR](https://cldr.unicode.org/) + [ISO 80000-1](https://www.iso.org/standard/30669.html), each active Holistika locale carries its own thousands-separator + decimal-separator pair. Mixing pairs across a single deliverable is a **brand-discipline failure** (the deck reads as machine-translated rather than locale-native).

| Locale | Thousands separator | Decimal separator | Example (1234.56) | Source |
|:---|:---|:---|:---|:---|
| `en` | `,` (comma) | `.` (period) | `1,234.56` | CLDR `en` (en-US, en-GB share number format) |
| `fr` | `U+202F` (NARROW NO-BREAK SPACE) | `,` (comma) | `1 234,56` | CLDR `fr` + ISO 80000-1 §4.1.3 (Europe FR convention) |
| `es` | `.` (period) | `,` (comma) | `1.234,56` | CLDR `es` (Spain + most of LatAm) |

**Why NARROW NO-BREAK SPACE for FR thousands**: a regular space breaks across lines mid-number (`1 / 234,56`); a regular no-break space (`U+00A0`) is wider than typographic convention; `U+202F` (NARROW NO-BREAK SPACE) is the CLDR-recommended typographically-correct character. Validators MUST normalize to `U+202F` and reject `U+0020` / `U+00A0` in `language: fr` numeric prose.

**Negative numbers**: minus-sign prefix in all locales (`-1,234.56` en; `-1 234,56` fr; `-1.234,56` es). Parentheses for negatives (`(1,234.56)`) are a finance-deck variant — acceptable in `formal_legal` register, refused in `peer_consulting` / `investor_aspirational` (reads as accounting-template).

**Percentage**: locale-specific spacing. `en` no space (`12.5%`); `fr` no-break space before symbol (`12,5 %` with `U+00A0` — not `U+202F`; the percent symbol convention is the wider no-break space per CLDR-fr); `es` no space (`12,5%`).

## 2. Currency formats

EUR is the primary Holistika currency; USD / GBP / CHF appear in cross-border engagements and investor decks. Symbol position + symbol-separator rules are locale-specific (per CLDR + per the EU Inter-Institutional Style Guide §7.3 for EUR).

| Locale | Currency | Symbol position | Symbol separator | Example (1234.56) | Notes |
|:---|:---:|:---|:---:|:---|:---|
| `en` | EUR | prefix | none | `€1,234.56` | EN follows currency-symbol-prefix convention regardless of currency. |
| `fr` | EUR | suffix | `U+202F` (NARROW NO-BREAK SPACE) | `1 234,56 €` | EU Inter-Institutional Style Guide §7.3.3 (FR EUR convention). |
| `es` | EUR | suffix | `U+0020` (regular space) | `1.234,56 €` | ES uses regular space per CLDR-es. |
| `en` | USD | prefix | none | `$1,234.56` | Standard US convention. |
| `fr` | USD | prefix | none | `$1 234,56` | Symbol stays prefix (per source-currency convention), separators per `fr` locale. |
| `es` | USD | prefix | none | `$1.234,56` | Same — symbol per source, separators per locale. |
| `en` | GBP | prefix | none | `£1,234.56` | Standard UK convention. |
| `fr` / `es` | GBP | prefix | none | `£1 234,56` / `£1.234,56` | Symbol stays prefix; separators per locale. |
| `en` | CHF | prefix | none | `CHF 1,234.56` | CHF (Swiss Franc) uses 3-letter ISO code + space prefix in EN. |
| `fr` | CHF | suffix | `U+202F` | `1 234,56 CHF` | Swiss-French convention (suffix; NBSP separator). |
| `es` | CHF | suffix | `U+0020` | `1.234,56 CHF` | Swiss-Spanish (rare; aligns with EUR convention). |

**Three-letter ISO codes vs symbols**: prefer ISO codes in `regulator_neutral` + `formal_legal` register (e.g., `EUR 1,234.56` rather than `€1,234.56`). Use symbols in `investor_aspirational` + `peer_consulting` (e.g., `€1,234.56` reads more directly to the reader). The validator is symbol-tolerant; the SOP encodes the soft preference.

**Cents / fractional-currency**: always emit two decimal places for monetary values (`€1,234.56`, never `€1,234.5` or `€1,234`). Whole-euro amounts in `peer_consulting` may drop the decimal portion (`€1,234`) for round numbers; never drop in `formal_legal` / `regulator_neutral`.

## 3. Date formats

Three format classes per locale: ISO 8601 canonical (always), natural-long (per-locale), natural-short (per-locale). Mixing classes within a single deliverable is acceptable when the surface justifies it (a Gantt timeline uses ISO; the proposal cover page uses natural-long; the email signature uses natural-short).

### 3.1 ISO 8601 — canonical / technical (all locales)

`YYYY-MM-DD` (e.g., `2026-05-14`). Used in:

- All canonical compliance CSV cells (`last_review`, `decided_at`, `inception_date`, etc.).
- Frontmatter of every governed markdown artifact (`authored:`, `last_review:`).
- Render-manifest sha256 timestamps + audit logs.
- Validator output rows.
- File names with date prefix (`2026-suez-webuy/`, `2026-asesoria-hosteleria/`).

**Per [ISO 8601:2019](https://www.iso.org/standard/70907.html)**: `YYYY-MM-DD` is the **only** numeric date format that is locale-unambiguous (`05/14/26` reads as month-day-year in EN-US but day-month-year in EN-GB; ISO eliminates the ambiguity). All Holistika canonical surfaces use ISO; locale-specific natural formats are reserved for prose surfaces.

### 3.2 Natural-long format (per-locale prose surfaces)

Used in: cover-page dates, signature blocks, document-header dates, formal-letter datelines.

| Locale | Pattern | Example (May 14, 2026) | Notes |
|:---|:---|:---|:---|
| `en` | `Month D, YYYY` | `May 14, 2026` | US-EN convention; UK-EN may use `14 May 2026` (no comma). Default to US-EN; UK-EN as override per recipient region. |
| `fr` | `D mois YYYY` | `14 mai 2026` | French month names lowercase (per French typographic convention; `Mai` capitalized only at sentence start). Day number cardinal except first day of month: `1er mai 2026` (with `er` superscript). |
| `es` | `D de mes de YYYY` | `14 de mayo de 2026` | Spanish month names lowercase (per RAE convention). Triple `de` reads correctly: day-`de`-month-`de`-year. |

### 3.3 Natural-short format (per-locale prose surfaces)

Used in: in-prose dates ("we met on May 14"), table cells, time-bound deliverables.

| Locale | Pattern | Example (May 14, 2026) | Notes |
|:---|:---|:---|:---|
| `en` | `Mon D` or `Mon D, YYYY` | `May 14` / `May 14, 2026` | Year omitted when unambiguous from context. |
| `fr` | `D mois` or `D mois YYYY` | `14 mai` / `14 mai 2026` | Year omitted when unambiguous. |
| `es` | `D de mes` or `D de mes de YYYY` | `14 de mayo` / `14 de mayo de 2026` | Year omitted when unambiguous. |

**Forbidden numeric short formats in prose**: `5/14/26`, `14/5/26`, `14.5.26`, `2026-05-14` (the last is correct for canonical surfaces but reads as machine-formatted in prose — translate to natural-long or natural-short for any reader-facing surface).

## 4. Cross-language consistency

When the same numeric or date value appears in `README.fr.md` + `README.en.md` + `README.es.md` of the same engagement (the 3-file pattern per [`BRAND_MULTILINGUAL_CONTRACT.md`](BRAND_MULTILINGUAL_CONTRACT.md) §2 + `D-IH-70-P`), each version MUST use its locale-appropriate format. Cross-version consistency is **format-discipline** (each follows its locale rule), not **format-uniformity** (all match a single shape).

Example — engagement budget appearing in three locale READMEs:

- `README.en.md`: `Total budget: €123,456.78`
- `README.fr.md`: `Budget total : 123 456,78 €` (with `U+202F` thousands + `U+202F` symbol-separator)
- `README.es.md`: `Presupuesto total: 123.456,78 €` (with `U+0020` symbol-separator)

Validator surface — drift here is detected by the Pack A3 (multilingual locale-suffix) walker reading per-locale frontmatter + scanning per-locale prose for format violations. Per the I71 P2 design-time pick, format-rule scan stays co-located in the Pack A2 (Gantt confidence) walker since Gantt artifacts most frequently carry money + date prose; spin out `scripts/validate_brand_localised_formats.py` if rule cardinality grows beyond ~30 rules (currently ~14: 3 number + 5 currency + 6 date).

## 5. Validator hooks

The validator runtime resolves localised-format rules via the chassis at [`akos/brand_voice_register.py`](../../../../../../../akos/brand_voice_register.py):

```python
from pathlib import Path
from akos.brand_voice_register import (
    parse_localised_format_rules,
    CANONICAL_PATHS,
)

number_rules, currency_rules, date_rules = parse_localised_format_rules(
    Path(CANONICAL_PATHS["localised_formats"])
)
```

Surface choice (per the I71 P2 plan §P2 Step 2c design-time pick):

- **Co-located in Pack A2** (default): the Gantt-confidence walker reads frontmatter + scans cell prose; localised-format rules apply to the same prose. Rule cardinality (~14) stays under the sibling-spinout threshold.
- **Sibling validator** (forward-charter): if cardinality grows beyond ~30 rules, spin out `scripts/validate_brand_localised_formats.py` with its own thin CLI on the chassis. The chassis already exposes the typed surfaces; only the CLI script needs to land.

Operator override surface: `BrandGanttPack` (in `_validators/gantt-pack.yml`) carries `number_format_rules: []`, `currency_format_rules: []`, `date_format_rules: []` empty surfaces at day-1; operators populate these only when augmenting or overriding canonical defaults. The canonical (this file) is the SSOT for the rule list; the YAML pack is the operator override layer.

The `gantt-pack.yml` `layers_enabled.localised_formats: true` flag controls whether the Pack A2 walker scans for these rules (default: true; strict-day-1 per the I71 P2 plan default).

## 6. Cross-references

- [`BRAND_MULTILINGUAL_CONTRACT.md`](BRAND_MULTILINGUAL_CONTRACT.md) — 3-file pattern (`README.md` + `README.fr.md` + `README.en.md`); per-locale frontmatter cohesion; engagement-folder discipline for multilingual deliverables.
- [`BRAND_FRENCH_PATTERNS.md`](BRAND_FRENCH_PATTERNS.md) — FR voice canonical (anglicism + performative-FR refuse-list; §1-§5 register matrix).
- [`BRAND_SPANISH_PATTERNS.md`](BRAND_SPANISH_PATTERNS.md) — ES voice canonical (anglicism + performative-ES refuse-list; §13).
- [`BRAND_ENGLISH_PATTERNS.md`](BRAND_ENGLISH_PATTERNS.md) — EN voice canonical (MBA-deck jargon refuse-list; §5.1).
- [`../UX Designer/canonicals/BRAND_GANTT_DISCIPLINE.md`](../UX%20Designer/canonicals/BRAND_GANTT_DISCIPLINE.md) — Gantt artifact discipline (5-level confidence ladder; 4-quadrant audience matrix; the validator walker most likely to scan localised-format prose).
- [`akos/brand_voice_register.py`](../../../../../../../akos/brand_voice_register.py) — chassis surfaces (`NumberFormatRule`, `CurrencyFormatRule`, `DateFormatRule`, `parse_localised_format_rules`).
- [`scripts/validate_brand_gantt_confidence.py`](../../../../../../../scripts/validate_brand_gantt_confidence.py) — Pack A2 walker (default co-location host for Addition 11 rules at I71 P2).
- I71 P2 plan: [`.cursor/plans/i71-cicd-discipline-and-aiops-baseline-maturity_a71c0d6e.plan.md`](../../../../../../../.cursor/plans/i71-cicd-discipline-and-aiops-baseline-maturity_a71c0d6e.plan.md) §P2 Step 2c.
- I71 P2 phase report: [`docs/wip/planning/71-cicd-discipline-and-aiops-baseline-maturity/reports/p2-pack-a2-a3-addition-11-vale-2026-05-14.md`](../../../../../../wip/planning/71-cicd-discipline-and-aiops-baseline-maturity/reports/p2-pack-a2-a3-addition-11-vale-2026-05-14.md).
- D-IH-71-N — Addition 11 ratification (this canonical authored at I71 P2; minted in the same commit as Pack A2 + A3 + Tier 1 Vale).

## 7. External references

- [Unicode CLDR (Common Locale Data Repository)](https://cldr.unicode.org/) — authoritative source for per-locale number / currency / date formatting data.
- [ISO 80000-1:2009/AMD 1:2022](https://www.iso.org/standard/76921.html) — Quantities and units, Part 1: General (numerical formatting).
- [ISO 8601:2019](https://www.iso.org/standard/70907.html) — Date and time format (`YYYY-MM-DD` canonical).
- [EU Inter-Institutional Style Guide §7.3](https://publications.europa.eu/code/en/en-370300.htm) — Currency unit names + EUR formatting per official-document convention.
- [Real Academia Española (RAE) — Diccionario panhispánico de dudas](https://www.rae.es/dpd/) — Spanish month-name capitalisation.

## 8. Maintenance

- **Append-only** for the per-locale rule tables (§1 / §2 / §3) — adding a new currency or a new locale requires appending a row, not editing existing rows.
- **Annual review** with the Brand Manager + Copywriter in lockstep with `BRAND_FRENCH_PATTERNS.md` + `BRAND_SPANISH_PATTERNS.md` + `BRAND_ENGLISH_PATTERNS.md` (joint cadence; same review cycle as the per-locale brand canonicals).
- **Source citation** when adding a new rule: cite the CLDR locale ID, the ISO standard reference, OR the engagement-id where the format question first surfaced (operator-private; cite `ref_id` only).
- **Trigger for off-cycle review**: a new currency entering an engagement scope (e.g., GBP for a UK-counterparty fundraise); a new locale promoted to active status (e.g., `de` for a German-counterparty engagement); a CLDR data change (rare; check at annual review).

## 9. Open follow-ups (deferred to future initiative)

- **Locale extension** — `de` (German), `it` (Italian), `pt` (Portuguese; Brazil + Portugal variants), `nl` (Dutch) when an engagement counterparty enters scope. Each new locale requires appending one row to §1 + §2 + §3 plus extending the chassis `Locale` Literal in [`akos/brand_voice_register.py`](../../../../../../../akos/brand_voice_register.py) (additive-only; no signature changes to existing models).
- **Time-of-day formats** — `HH:MM` (24-hour, all locales for canonical surfaces); per-locale natural-language time formats deferred to a future initiative (low priority; most Holistika prose carries dates not times).
- **Time-zone handling** — engagement timestamps currently default to operator-local (`Europe/Madrid` for ES founder-residence; `Europe/Paris` for FR-counterparty engagements). Explicit time-zone qualifier convention (`14:30 CEST` vs `14:30 UTC+2`) deferred.
- **Sibling validator spin-out** — promotes when rule cardinality grows beyond ~30. Currently 14 rules (3 number + 5 currency + 6 date); next reassessment 2026-12 or when a new locale lands.
