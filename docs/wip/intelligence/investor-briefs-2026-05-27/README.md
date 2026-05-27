---
title: Investor Briefs 2026-05-27 — Wave R+4 C4 outputs
language: en
intellectual_kind: wip_intelligence_index
sharing_label: internal_only
audience: J-OP
authored: 2026-05-27
last_review: 2026-05-27
status: draft
ratifying_decisions:
  - D-IH-86-FA
  - D-IH-86-FB
  - D-IH-86-FC
  - D-IH-86-FD
  - D-IH-86-FE
linked_research_sources:
  - docs/wip/intelligence/research-grounded-wave-r-plus-4-2026-05-27/source-ledger.csv
  - docs/wip/intelligence/research-grounded-wave-r-plus-4-2026-05-27/prong-c-investor-segmentation.md
  - docs/wip/intelligence/research-grounded-wave-r-plus-4-2026-05-27/prong-d-startup-online-presence-for-investors.md
linked_canonicals:
  - docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/PERSONA_REGISTRY.csv
  - docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_BASELINE_REALITY_MATRIX.md
  - docs/references/hlk/v3.0/Admin/O5-1/Marketing/canonicals/MARKETING_LIFECYCLE_TAXONOMY.md
linked_cursor_rules:
  - .cursor/rules/akos-brand-baseline-reality.mdc
  - .cursor/rules/akos-external-render-discipline.mdc
---

# Investor briefs 2026-05-27 — Wave R+4 C4 outputs

> Tier-1 WIP intelligence: persona-targeted investor 1-pager briefs +
> one program-scoping doc for the Online-Presence sub-persona. Authored
> against the 5 investor sub-personas ratified in C2
> (`PERSONA-INVESTOR-HIGH-CRAFT` / `-SHOWCASE` / `-PROGRAM-RADAR` /
> `-OPERATIONAL-TRUST` / `-ONLINE-PRESENCE`).

## Honest substance contract (binding for every brief)

Each brief MUST hold the following truths without softening or
exaggeration:

1. **The methodology stack is real and checked-in code.** 14 Quality
   Fabric specialties are documented in
   `docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/`, of which
   COLLABORATOR_SHARE_DOCTRINE and SYNTHESIS_BEFORE_TRANCHE_DISCIPLINE
   are the two most recent active specialties (Wave R+1 through Wave
   R+3). MKTOPS_DISCIPLINE was promoted to `active` at Wave R+4 C3a
   per `D-IH-86-EY`.
2. **The KiRBe knowledge platform and MADEIRA agent layer are in active
   development.** Both are real product surfaces under construction,
   not abstractions or vapor.
3. **SUEZ and Websitz are live commercial conversations, not signed
   engagements.** SUEZ POC has a CDC + proposal + cobranded customer
   pack authored (Wave R+3 demos at `docs/references/hlk/v3.0/Think Big/Clients/2026-suez-webuy/`).
   Websitz/Rushly is the operator's worked-example for the
   `deep_partner_65_35` `share_pattern` (Wave R+2 doctrine rewrite).
   Neither carries a signed purchase order or rendered invoice at the
   date of this folder.
4. **Founders + team is currently the Founder/CEO plus MADEIRA as
   AIC.** No fabricated additional team members.
5. **The investor sees the same internal-source-of-truth substance
   externally translated.** No internal CORPINT vocabulary leaks into
   any brief body. The dual-register contract from
   `BRAND_BASELINE_REALITY_MATRIX.md` applies.

These are the 5 anti-fabrication rails. Any brief revision that
softens or stretches the truth fails the bar and gets reworked.

## Files in this folder

| File | Sub-persona target | Decision row |
|:---|:---|:---|
| `brief-01-high-craft.md` | PERSONA-INVESTOR-HIGH-CRAFT | D-IH-86-FA |
| `brief-02-showcase.md` | PERSONA-INVESTOR-SHOWCASE | D-IH-86-FB |
| `brief-03-program-radar.md` | PERSONA-INVESTOR-PROGRAM-RADAR | D-IH-86-FC |
| `brief-04-operational-trust.md` | PERSONA-INVESTOR-OPERATIONAL-TRUST | D-IH-86-FD |
| `brief-05-online-presence.md` | PERSONA-INVESTOR-ONLINE-PRESENCE | D-IH-86-FE |
| `program-scope-online-presence-buildout.md` | PERSONA-INVESTOR-ONLINE-PRESENCE (companion) | D-IH-86-FE |

## How to use

When the operator (or AIC) prepares to engage a specific investor
(named in `GOI_POI_REGISTER.csv`):

1. Resolve the investor's sub-persona class against the 5 active
   `PERSONA-INVESTOR-*` rows in `PERSONA_REGISTRY.csv` (`MQS` qualification
   + cold/warm distance band + research from `RESEARCH_ACTION_DISCIPLINE`).
2. Pick the matching brief from this folder as the starting template.
3. Copy the brief to the matching engagement folder under
   `docs/references/hlk/v3.0/Think Big/Advisers/<engagement-slug>/`
   (when post-NDA) OR `docs/wip/intelligence/<engagement-slug>/`
   (pre-NDA).
4. Tailor the persona-specific opener and asks to the named investor
   using GOI/POI intelligence already captured.
5. Render to PDF via `scripts/render_dossier.py --variant <variant>` or
   an equivalent render trail per
   `akos-external-render-discipline.mdc` RULE 4.
6. Capture sha256 manifest sidecar at the render path.
7. Log the send via `OPERATOR_INBOX` and update the `GOI_POI_REGISTER`
   row.

These briefs are NOT broadcast assets. Per
`akos-external-render-discipline.mdc` RULE 1 and the
`CHANNEL_TOUCHPOINT_REGISTRY.csv` SLA for investor channels, each send
is 1:1 (mail surface) with optional PDF attachment, never bulk
distribution.

## Cross-references

- `PERSONA_REGISTRY.csv` (5 investor sub-persona rows added at C2).
- `MARKETING_LIFECYCLE_TAXONOMY.md` (lifecycle vocabulary).
- `MARKETING_AREA_M3_REDESIGN.md` §3.1 (channel-to-owner propagation
  matrix; investor briefs are Brand & Narrative-authored, Reach
  Manager-deployed).
- `EMAIL_OUTBOUND_DOCTRINE.md` (channel doctrine for sending).
- `BRAND_BASELINE_REALITY_MATRIX.md` (dual-register contract).
- `RESEARCH_ACTION_DISCIPLINE.md` (source-ledger gate for any new
  claim added at tailoring time).
- D-IH-86-FA through D-IH-86-FE (per-brief active decision rows).
