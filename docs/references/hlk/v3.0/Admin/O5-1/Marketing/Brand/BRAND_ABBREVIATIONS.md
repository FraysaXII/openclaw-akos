---
language: en
status: active
role_owner: Brand Manager
area: Marketing
entity: Holistika Research SL
program_id: shared
topic_ids:
  - topic_brand_voice
artifact_role: canonical
intellectual_kind: voice_registry
authority: Founder + Brand Manager
last_review: 2026-05-08
ssot: true
---

# BRAND_ABBREVIATIONS — Allowed / forbidden registry

> **Status — Active (Initiative 66 P1; founder + Brand Manager-authored 2026-05-08).** Codifies decision [D-IH-66-N](../../../../wip/planning/66-brand-vision-ops-sweep/decision-log.md#d-ih-66-n) — operator-surfaced "HLK" question resolved as part of a broader abbreviation-governance canonical. Scope: every short-form (≤4 char) reference to a brand entity, sub-mark, or product. Owned by the Brand Manager; reviewed annually + on-demand whenever a new sub-mark or product is introduced.

## 1. Why this canonical exists

Founder asked: "Should we be using HLK as a brand abbreviation?" The honest answer required three sub-decisions: (a) is HLK already in use somewhere, (b) what register should it inhabit if used, (c) what other abbreviations follow the same rule. This document encodes all three.

The deeper reason: short-forms drift faster than wordmarks. Once a contractor, partner, or vendor starts saying "HLK" in a Slack channel, that abbreviation propagates uncontrollably unless the brand canonical declares it allowed (and where) or forbidden (and why). The cost of late-stage abbreviation cleanup is high; declaring at canon-time is cheap.

## 2. Per-abbreviation registry

### 2.1 HLK

| Question | Decision |
|:---|:---|
| **Is "HLK" allowed externally?** | **Forbidden in external prose. Allowed in technical/engineering contexts.** |
| **Why?** | "HLK" reads as a tech-bro short-form (e.g., "HLR", "HCP", "HKR" are all common technical abbreviations). It dilutes the umbrella "Holistika" brand by suggesting an unpronounceable initialism. The umbrella brand survives only if it is consistently spoken in full. |
| **Where allowed?** | Internal tooling: AKOS-vault internal SOPs (e.g., this very file's `topic_id`, `program_id`); engineering directory names (`hlk-erp`, `hlk-mcp`, `hlk-vault-envoy-repos`); GitHub repository slugs; Cursor rule filenames (`akos-mirror-template.mdc`). These are technical artifacts, not brand artifacts. |
| **Where forbidden?** | Public web (boilerplate prose, DOM, og-tags); investor + advisor + ENISA + recruiter + partner deck text; any rendered surface served at `holistikaresearch.com` or any consumer-facing portal; press releases; legal contracts; founder bio (uses "Holistika"); any external email; any social media post; the Hi monogram + HOLÍSTIKA wordmark are the only umbrella abbreviation forms allowed externally. |
| **Sub-mark exception** | "HLK Tech Lab" is the **canonical** sub-mark name (per D-IH-66-A + BRAND_ARCHITECTURE.md). "HLK" alone is forbidden externally; "HLK Tech Lab" is allowed externally. The sub-mark name uses HLK because it is paired with "Tech Lab" — never HLK in isolation. |
| **Drift gate** | `validate_brand_jargon.py` (P2) flags rendered DOM containing standalone "HLK" (not followed by " Tech Lab"). Allowed contexts: code comments, GitHub commit messages, Cursor rules. Forbidden contexts: any HTML rendered to public web. |

### 2.2 MA (for "MADEIRA Agent")

| Question | Decision |
|:---|:---|
| **Is "MA" allowed?** | **Forbidden in all contexts.** |
| **Why?** | "MA" is two-letter; collides with countless usages (state of Massachusetts, "master of arts", many product names). No marketing or technical advantage to using it. |
| **Where allowed?** | Nowhere. Spell out "MADEIRA Agent" in full. |
| **Drift gate** | Manual review (no automated drift gate; impractical to filter "MA" without false-positive flooding). |

### 2.3 KB (for "KiRBe")

| Question | Decision |
|:---|:---|
| **Is "KB" allowed?** | **Forbidden in all contexts.** |
| **Why?** | "KB" reads as kilobyte (universal computing convention). Collides with the units. |
| **Where allowed?** | Nowhere. Spell out "KiRBe" in full. |
| **Drift gate** | Manual. |

### 2.4 EV (for "ENVOY")

| Question | Decision |
|:---|:---|
| **Is "EV" allowed?** | **Forbidden in all contexts.** |
| **Why?** | "EV" reads as "electric vehicle" (universal automotive convention). Major collision in any tech-adjacent context. |
| **Where allowed?** | Nowhere. Spell out "ENVOY" in full. |
| **Drift gate** | Manual. |

### 2.5 TB (for "Think Big")

| Question | Decision |
|:---|:---|
| **Is "TB" allowed?** | **Forbidden in all contexts.** |
| **Why?** | "TB" reads as terabyte. Collision. |
| **Where allowed?** | Nowhere. Spell out "Think Big" in full. |
| **Drift gate** | Manual. |

### 2.6 TL (for "HLK Tech Lab")

| Question | Decision |
|:---|:---|
| **Is "TL" allowed?** | **Forbidden in all contexts.** |
| **Why?** | "TL" reads as "team lead" or "transmission line" — both common professional abbreviations. Collision. The full name ("HLK Tech Lab") is short enough already (12 characters) and carries the brand pairing of HLK + Tech Lab; abbreviating it loses the sub-mark identity. |
| **Where allowed?** | Nowhere. Spell out "HLK Tech Lab" in full. |
| **Drift gate** | Manual. |

### 2.7 H (for "Holistika")

| Question | Decision |
|:---|:---|
| **Is "H" allowed as a brand short-form?** | **Forbidden as a brand short-form.** |
| **Why?** | One-letter abbreviation is meaningless in a competitive market context. The Hi monogram (H + i = "Hi") is the visual short-form; there is no text short-form. |
| **Allowed exception** | "H" inside the Hi monogram graphic — but the graphic is the abbreviation, not text. |
| **Drift gate** | Manual (impractical to gate single-letter usage automatically). |

### 2.8 HRS (for "Holistika Research SL")

| Question | Decision |
|:---|:---|
| **Is "HRS" allowed?** | **Forbidden in external prose. Allowed in internal financial / legal filing contexts.** |
| **Why?** | "HRS" is sometimes used internally by the operator's accountant + lawyer for filing purposes; allowed in those isolated contexts (internal tax filing labels, internal legal-document references). External use dilutes the umbrella brand and reads as initialism-heavy bureaucracy (which is the opposite of the brand voice). |
| **Where allowed?** | Internal: tax filings, accountant emails, lawyer-internal letters, accounting software entries. |
| **Where forbidden?** | Public web; decks; press; social; founder bio; legal contracts (use full "Holistika Research SL" in contracts). |
| **Drift gate** | Manual; relies on register-aware writing per BRAND_REGISTER_MATRIX. |

### 2.9 R+S (for "Research + Strategy" within "Holistika R+S")

| Question | Decision |
|:---|:---|
| **Is "R+S" allowed?** | **Allowed within the canonical sub-mark name only.** |
| **Why?** | "Holistika R+S" is the canonical Layer-3 sub-mark name (per BRAND_ARCHITECTURE.md). The "R+S" component is not a freestanding abbreviation; it always pairs with "Holistika". Using "R+S" alone is forbidden. |
| **Where allowed?** | "Holistika R+S" is the full name; "R+S" alone never appears. |
| **Drift gate** | Manual. |

## 3. Composition rules — when multiple short-forms cluster

If a single sentence would contain three or more brand abbreviations (e.g., "MADEIRA + KiRBe + ENVOY"), use the umbrella name once, then list the products:

> ✓ "Holistika ships MADEIRA, KiRBe, and ENVOY in production."  
> ✗ "We ship MA, KB, and EV in production."

Forbidden composition forms (any combination of disallowed abbreviations):

- "Holistika HLK"
- "HLK Tech Lab TL"
- Any combination using the forbidden short-forms in prose.

## 4. Cross-reference register — where this canonical is enforced

| Surface | Enforcement |
|:---|:---|
| `boilerplate/` rendered DOM | `validate_brand_jargon.py` (P2) flags forbidden short-forms |
| `boilerplate/messages/*.json` (i18n) | Same drift gate; matches forbidden tokens in localized strings |
| `hlk-erp/` operator-only surfaces | Internal short-forms allowed (operator context); jargon validator scopes only to `boilerplate/` |
| Investor + advisor + ENISA + recruiter + partner decks (`_assets/advops/`) | Manual review during P6 deck creation; companion `.objections.md` includes "did this deck dilute the brand by using forbidden short-forms?" check |
| Founder bio canonical (`SOP-PEOPLE_FOUNDER_BIO_001.md`, P3) | Hard-codes "Holistika" + "Holistika Research SL"; never uses HLK or HRS |
| Email signatures (P6) | Hard-coded "Holistika" + full sub-mark name; never abbreviated |
| Legal templates (MSA, SOW, NDA, DPA — P4) | "Holistika Research SL" full prose (legal entity); plain Latin-1 |
| AKOS-vault internal SOPs | Internal short-forms allowed (this canon's "internal" register) |
| Cursor rules + commit messages | Internal short-forms allowed |

## 5. Maintenance

- **Annual review.** `process_list.csv` row "BRAND_ABBREVIATIONS annual review" (created I66 P3); cadence: yearly.
- **Trigger for off-cycle review.** New sub-mark or product brand introduction (each new entity may bring its own short-form question); founder-flagged drift; partner/customer using a non-canonical abbreviation in trade.
- **Authority for changes.** Founder (final) + Brand Manager (proposes + maintains).

## 6. Related canonicals

- [`BRAND_ARCHITECTURE.md`](BRAND_ARCHITECTURE.md) — defines the entities being abbreviated.
- [`BRAND_LOGO_SYSTEM.md`](BRAND_LOGO_SYSTEM.md) — visual short-forms (Hi monogram + HOLÍSTIKA wordmark; the visual analogues of these text rules).
- [`BRAND_JARGON_AUDIT.md`](BRAND_JARGON_AUDIT.md) — broader external-jargon governance; this canonical is its short-form supplement.
- [`BRAND_DO_DONT.md`](BRAND_DO_DONT.md) — voice rules that this canonical instantiates for the abbreviation case.
- [`BRAND_REGISTER_MATRIX.md`](BRAND_REGISTER_MATRIX.md) — surface-by-surface register definitions; this canonical's "internal" vs "external" allowance maps to register-matrix surfaces.
- [`BRAND_BASELINE_REALITY_MATRIX.md`](BRAND_BASELINE_REALITY_MATRIX.md) — internal-register vocabulary (HUMINT-derived terms) governance; complements this canonical's brand-abbreviation governance.
