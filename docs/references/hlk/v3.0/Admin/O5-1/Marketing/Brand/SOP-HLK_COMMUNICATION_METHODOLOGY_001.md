---
sop_id: SOP-HLK_COMMUNICATION_METHODOLOGY_001
status: review
role_owner: Brand Manager
co_owners:
  - PMO
  - Compliance Manager
area: Marketing
entity: Holistika
program_id: shared
topic_ids:
  - topic_communication_methodology
artifact_role: canonical
intellectual_kind: methodology_map
related_process_ids:
  - thi_mkt_prj_1
  - thi_mkt_dtp_NN_communication_methodology_maintenance
authority: Initiative 24 P1 + Wave-2 plan §"D-IH-10"
last_review: 2026-04-29
---

# SOP-HLK_COMMUNICATION_METHODOLOGY_001 — Four-Layer Communication Methodology

**Owner**: Brand Manager (CMO chain)  
**Co-owners**: PMO, Compliance Manager  
**Initiative**: 24 P1 (2026-04-29).  
**Operator approval gate**: G-24-2 (`process_list.csv` named tranche under `thi_mkt_prj_1`).

## 1. Purpose

Codify how every operator-authored outbound message at Holistika is constructed across **four layers** so that:

1. **Brand foundation** (Layer 1) sets the voice envelope — non-negotiable across every message.
2. **Concept** (Layer 2) anchors every claim in canonical CSV facts and topic manifests — no inventions.
3. **Use-case** (Layer 3) resolves the recipient, lens, sharing label, and discipline — recipient-specific.
4. **Eloquence** (Layer 4) tunes voice register, language, and pronoun — within the bounds Layer 1 set.

Eloquence operates **inside** the brand voice envelope. It does **not** override it.

## 2. Scope

In scope:

- All adviser-facing messages (Legal/Fiscal/IP/Banking/Certification/Notary).
- All client and prospect outbound messages.
- All internal messages that cross discipline boundaries (e.g. PMO updates, founder briefings).

Out of scope:

- Auto-generated transactional messages (e.g. Stripe billing receipts) — those follow product/UX standards, not this SOP.
- Internal informal chat — voice register is `casual_internal` (per [`BRAND_REGISTER_MATRIX.md`](BRAND_REGISTER_MATRIX.md)) but full SOP discipline is over-spec for ad-hoc messages.

## 3. The four layers

### Layer 1 — Brand foundation (canonical SSOT: [`BRAND_VOICE_FOUNDATION.md`](BRAND_VOICE_FOUNDATION.md))

- **Voice charter** — one sentence describing how Holistika speaks.
- **Archetype** — single token (`expert_peer`, `trusted_advisor`, …).
- **Narrative pillars** — 3 themes that anchor every message.
- **Voice IS / IS NOT** — see [`BRAND_DO_DONT.md`](BRAND_DO_DONT.md).
- **Register matrix** — see [`BRAND_REGISTER_MATRIX.md`](BRAND_REGISTER_MATRIX.md).

> **D-IH-17**: brand-craft is operator's lived knowledge. The SOP CITES the foundation; we do **not** invent it from CSVs. Until the operator fills YAML Section 2, the foundation MDs are scaffold-staged (`status: scaffold-awaiting-discovery`).

### Layer 2 — Concept (what is true)

- Recipient and topic facts come from canonical CSVs only:
  - [`GOI_POI_REGISTER.csv`](../../../../../compliance/GOI_POI_REGISTER.csv) — recipient identity (ref_id, sensitivity, voice profile).
  - [`ADVISER_ENGAGEMENT_DISCIPLINES.csv`](../../../../../compliance/ADVISER_ENGAGEMENT_DISCIPLINES.csv) — discipline default register and reading speed.
  - [`ADVISER_OPEN_QUESTIONS.csv`](../../../../../compliance/ADVISER_OPEN_QUESTIONS.csv) and [`FOUNDER_FILED_INSTRUMENTS.csv`](../../../../../compliance/FOUNDER_FILED_INSTRUMENTS.csv) — what we know and what we're filing.
  - [`PROGRAM_REGISTRY.csv`](../../../../../compliance/dimensions/PROGRAM_REGISTRY.csv) — which program the message scopes to.
  - KM topic manifests under [`_assets/<plane>/<program_id>/<topic_id>/`](../../../../../v3.0/_assets/) — per-topic projections.
- **No facts may appear in the message that are not citable to one of the above.**
- For sensitive content, sharing label gates apply: `restricted` rows never leave their plane.

### Layer 3 — Use-case (recipient context)

- **Recipient**: `ref_id` (POI-* or GOI-*) from `GOI_POI_REGISTER.csv`. Real names stay off-repo (composer never inlines them; operator does at SMTP step).
- **Lens**: discipline-specific framing (e.g. `entity_readiness`, `fiscal_readiness`, `incorporation`). Pulled from the open-questions or filed-instruments lens column.
- **Sharing label**: derived from the recipient's sensitivity band (`public`, `internal`, `confidential`, `restricted`).
- **Discipline**: `LEG`, `FIS`, `IPT`, `BNK`, `CRT`, `NOT`. Provides default register and reading-speed expectations.

### Layer 4 — Eloquence (voice tuning)

- **`voice_register`** — one of `formal_legal`, `peer_consulting`, `casual_internal`, `regulator_neutral`, `investor_aspirational`. Read from `GOI_POI_REGISTER.csv` (per-recipient override; see Initiative 24 P2).
- **`language_preference`** — `es` / `en` / `bilingual`.
- **`pronoun_register`** — `tu` / `usted` / empty.
- **Length budget** — short for transactional (≤200 words); medium for discipline questions (≤600 words); long-form for strategic memos (≥1500 words, structured headings).

**Precedence** (highest first):

1. **Recipient profile** — `voice_register` + `language_preference` + `pronoun_register` from the GOI/POI row.
2. **Discipline default** — when recipient profile is empty, the discipline's default register applies (per `ADVISER_ENGAGEMENT_DISCIPLINES.csv`).
3. **Brand foundation default** — when neither, the archetype-implied register kicks in.
4. **Global default** — `peer_consulting`, `bilingual`, no pronoun.

## 4. Per-message workflow

```mermaid
flowchart TD
  start[Operator opens compose_adviser_message.py]
  l1[Layer 1: Brand voice envelope]
  l2[Layer 2: Resolve facts from canonical CSVs]
  l3[Layer 3: Use-case (recipient, lens, sharing label)]
  l4[Layer 4: Eloquence (voice register, language, pronoun)]
  draft[Draft emitted to artifacts/exports/]
  review[Operator reviews]
  send[Operator sends via SMTP outside repo]
  l1 --> l2
  l2 --> l3
  l3 --> l4
  start --> l1
  l4 --> draft
  draft --> review
  review --> send
```

The composer (`scripts/compose_adviser_message.py`, Initiative 24 P4) automates the resolution; the operator finalises and sends. The composer **never** writes a real recipient email address or sends — those are operator actions at SMTP time.

## 5. Approval gates

| Gate | When | What |
|:----:|:-----|:-----|
| **G-24-2** | This SOP lands | `process_list.csv` named tranche `thi_mkt_dtp_NN` "Communication methodology maintenance" under `thi_mkt_prj_1`. |
| **G-24-3** | Real adviser email send | **IRREVERSIBLE.** Pre-flight checklist (off-repo recipient resolved, sharing-label gate green, discipline-lens match, brand voice match per `BRAND_REGISTER_MATRIX.md`, archive copy committed, `.gitignore` review, SMTP `Sent` timestamp captured, founder sign-off in YAML Section 5). |

## 6. Drift detection

- If the methodology SOP's citations stop resolving (e.g. `BRAND_VOICE_FOUNDATION.md` is `status: scaffold-awaiting-discovery`), the next composer run fails loudly with a `BRAND_FOUNDATION_NOT_READY` error code unless `--allow-scaffold-tokens` is set explicitly for dry-run.
- Annual Brand Manager review (D-IH-17 re-evaluation trigger).
- Quarterly cross-program glossary review for new voice registers / discipline codes.

## 7. References

- [`BRAND_VOICE_FOUNDATION.md`](BRAND_VOICE_FOUNDATION.md) — Layer 1 SSOT
- [`BRAND_REGISTER_MATRIX.md`](BRAND_REGISTER_MATRIX.md) — (relationship, channel) → register lookup
- [`BRAND_DO_DONT.md`](BRAND_DO_DONT.md) — Voice IS / IS NOT
- [`docs/reference/glossary-cross-program.md`](../../../../../../reference/glossary-cross-program.md) §"Voice register" + §"Discipline codes"
- [`scripts/compose_adviser_message.py`](../../../../../../../scripts/compose_adviser_message.py) — composer (Initiative 24 P4)
- [`SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md`](../../Operations/PMO/SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md) — ADVOPS plane SOP (Initiative 21)
- Initiative 24 master roadmap: [`docs/wip/planning/24-hlk-communication-methodology/master-roadmap.md`](../../../../../../wip/planning/24-hlk-communication-methodology/master-roadmap.md)
- Decision log: D-IH-10 (4 layers), D-IH-11 (voice columns), D-IH-17 (brand foundation prerequisite), D-IH-24-A (scaffold→active flip).
