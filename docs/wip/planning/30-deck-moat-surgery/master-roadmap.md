# Initiative 30 — Deck moat surgery: MADEIRA, joint-equity, governance metrics

**Folder:** `docs/wip/planning/30-deck-moat-surgery/`
**Status:** Open (started 2026-04-30)
**Authoritative Cursor plan:** `~/.cursor/plans/deck_moat_surgery_d6e5e47b.plan.md`

## Outcome

Surface the missing halves of the knowledge base onto the company dossier deck so it reads as product-led and operationally-credible instead of services-biased. Three structural injections:

1. **MADEIRA agentic platform** — already first-class in the repo (`SOP-MADEIRA-*` SOPs, `Think Big/`, KIR onboarding) but absent from the deck. Project it onto slides 04 / 05 / 06 / 11 / 12.
2. **Joint-equity SaaS-pilot channel** — real inbound demand pattern (POC_TO_COMMERCIAL_MAP partner rows) but not registered as a channel. Add as Channel 6 in `CHANNEL_STRATEGY.md`; surface on slides 09 / 10.
3. **Quantified governance moat** — 17 governed topics, 1,093 governed processes, 65 governed roles, deterministic validators + drift probes. Currently treated as plumbing. Promote to a costly investor-grade signal on slide 11.

## Scope decisions

- **In scope.** New strategy artifacts (`MADEIRA_PLATFORM.md`, `GOVERNANCE_MOAT.md`); new channel section in `CHANNEL_STRATEGY.md`; deck restructure across 7 slides; deck-story Spanish narrative mirror; tests; CHANGELOG; UAT; PR.
- **Out of scope.** Filling the existing 9 `TODO[OPERATOR-x]` markers from Initiative 29 P4 (founder-decision territory). Naming partners (Websitz, Rushly) on the deck (keeps I28 D-IH-28 rule). Productizing MADEIRA itself (deck announces direction, not GA date). Figma backport (separate next-pass per the I29 P1 drift-handling rule).

## Asset classification (per [`PRECEDENCE.md`](../../../references/hlk/compliance/PRECEDENCE.md))

| Class | Paths | Rule |
|:------|:------|:-----|
| **New canonical (planning)** | `docs/wip/planning/30-deck-moat-surgery/{master-roadmap,decision-log,asset-classification,evidence-matrix,risk-register}.md` | Standard six-artifact contract |
| **New canonical (strategy)** | `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/business-strategy/{MADEIRA_PLATFORM,GOVERNANCE_MOAT}.md` | Two new strategy artifacts joining the I29 P4 layer |
| **Modified canonical** | `docs/references/hlk/compliance/dimensions/TOPIC_REGISTRY.csv` (+2 rows) | `topic_madeira_platform`, `topic_governance_moat` |
| **Modified canonical** | `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/business-strategy/CHANNEL_STRATEGY.md` (+Channel 6) | Existing canonical, additive section |
| **Modified canonical (deck SSOT)** | `docs/references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_company_dossier/deck_slides.yaml` | Slides 04, 05, 06, 09, 10, 11, 12; YAML wins for content |
| **Derived (mirrors YAML)** | `docs/references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_company_dossier/deck_story_es.md` | Spanish narrative mirror — every YAML edit backported |
| **Re-rendered** | `docs/presentations/holistika-company-dossier/index.html` + `artifacts/exports/holistika-company-dossier-enisa-2026-04-30.pdf` | Deterministic from YAML |
| **Mirror reseed (operator-applied)** | `artifacts/sql/i30_topic_registry_business_strategy_upsert.sql` | Staged for `npx supabase db push` or MCP `execute_sql` |
| **Reference-only** | Phase reports under `reports/` | Standard initiative artifact |

## Phase dependency

```mermaid
flowchart LR
    P0[P0_bootstrap]
    P1[P1_madeira_artifact_topic]
    P2[P2_joint_equity_channel]
    P3[P3_governance_moat_artifact_topic]
    P4[P4_deck_restructure]
    P5[P5_rebuild_and_verify]
    P6[P6_tests_changelog_uat_pr]
    P0 --> P1
    P0 --> P2
    P0 --> P3
    P1 --> P4
    P2 --> P4
    P3 --> P4
    P4 --> P5
    P5 --> P6
```

## Phase at a glance

| Phase | Deliverable | Acceptance |
|:------|:------------|:-----------|
| **P0** | Initiative folder + 5 standard artifacts + reports/ | Folder exists; decision-log carries D-IH-30-A..D |
| **P1** | `MADEIRA_PLATFORM.md` (deck-bound, 1 TODO[OPERATOR-x]) + `topic_madeira_platform` row | `validate_topic_registry.py` PASS at 18 rows |
| **P2** | `CHANNEL_STRATEGY.md` Channel 6 (joint-equity, 1 TODO[OPERATOR-x]); deck-bound facts updated | `sync_deck_from_strategy.py --check-only` reports the new TODO marker |
| **P3** | `GOVERNANCE_MOAT.md` (deck-bound, 4 hero numbers from `validate_hlk`) + `topic_governance_moat` row | Topic registry at 19 rows; governance metrics match `validate_hlk` output |
| **P4** | 7 slides edited in `deck_slides.yaml` + matching narrative in `deck_story_es.md` | Jargon-audit gate stays clean; YAML schema PASS |
| **P5** | HTML rebuild + PDF re-export + sync_deck_from_strategy + validate_hlk + mirror reseed SQL staged | All builds clean; new SHA256 in PDF manifest; validate_hlk reports 19 topics |
| **P6** | Tests (extend test_business_strategy + test_company_deck + new test_governance_moat_metrics) + CHANGELOG + UAT + PR + admin-merge | `pytest tests/` 0 new failures; PR squash-merged |

## Drift-handling rule (carried from I29 P1)

YAML / Markdown SSOT wins for content; Figma wins for visual layout; HTML preview deck is fast iteration; PDF is disposable; **any Figma copy edit must be backported to YAML before initiative close**. This initiative does not touch Figma — the company-dossier Figma file at `https://www.figma.com/design/yiPav7BLxUulNFrrsoKJqW` is left intentionally on its current frame copy. A separate later initiative will Figma-backport the I30 YAML edits when the founder picks a Figma working session window.

## Estimated effort

3-4 hours of focused execution. Hard dependency: `validate_hlk` numbers must be current (re-run before authoring `GOVERNANCE_MOAT.md` so the hero metrics quoted there are accurate at write-time).
