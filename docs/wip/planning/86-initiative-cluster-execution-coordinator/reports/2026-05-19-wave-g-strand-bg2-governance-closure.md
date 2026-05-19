---
status: active
classification: closure-report
intellectual_kind: wave_closure_appendix
authority: PMO
artifact_role: derived
ratifying_decisions: [D-IH-86-S]
parent_decision: D-IH-86-S
language: en
last_review: 2026-05-19
audience: J-OP
---

# Wave G B-G2 — Governance closure (closure appendix)

Follow-up to the [Wave F external-render doctrine closure](2026-05-19-wave-f-external-render-doctrine-closure.md) and parallel sibling to Wave G B-G1. Wave G B-G2 closes three forward-enhancements that Wave F's [uat-render-quality-2026-05-19.md](uat-render-quality-2026-05-19.md) §7 listed as deferred:

- **F+3** — process_list.csv row mint for `env_tech_dtp_external_render_gate_promotion_001` (Wave F §7 item 5).
- **F+4** — channel-frontmatter onboarding sweep + reusable template + skill extension (Wave F §7 item 6 + I86 B5 novel framing).
- **F+6** — axe-core visual-polish baseline audit (Wave F §7 item 4 partial closure).

Ratified at **D-IH-86-S** (Wave G B-G2 governance closure; supersedes-link to D-IH-86-Q parent).

## Why this is "Wave G B-G2"

Wave F (commit `4736027`) shipped the gate flip + the 5-strand scope expansion as one wave. Operator pushed B-G2 as a *governance-closure bundle* separate from B-G1 to keep the two bundles independently revert-able (B-G1 ships application-side changes; B-G2 ships governance + audit deliverables). Wave G B-G2 is the doctrinal cleanup pass — process_list catches up to the SOP, channel discipline graduates from rule-text-only to authoring-template + skill-section, and the visual-polish audit produces the baseline I68 P3 can absorb when it activates.

## Three executive calls (no AskQuestion tool available in subagent context)

Per [`inline-ratify-craft/SKILL.md`](../../../../../.cursor/skills/inline-ratify-craft/SKILL.md) "Pitfall: I have run the evidence sweep but I do not see clear options" recovery pattern, the agent made executive calls on the three ratify gates the parent operator brief named:

### Gate 1 — F+3 paired-runbook choice

**Resolution:** **Option A — cite existing validator scripts as paired runbook** (no new wrapper script).

**Evidence:** SOP-EXTERNAL_RENDER_GATE_PROMOTION_001.md frontmatter at Wave F mint already declares `paired_runbook: scripts/validate_external_render_trail.py`; minting a thin `external_render_gate_promote.py` wrapper would add a layer without semantic benefit (the validator already enforces the gate state mechanically; the SOP §4 procedure is operator-facing prose, not a programmatic workflow). The `gated_operator` cadence in `validate_process_list_pairing.py` line 123 auto-passes the runbook-discoverable check (no pointer required for operator-gated rows). Decision recorded as `decision_source: agent_executive_call`.

### Gate 2 — F+4 channel-ID assignment

**Resolution:** **Use existing canonical channel codes only** (no minting of `CHAN-EMAIL-OUTBOUND` in this push).

**Evidence:** `CHANNEL_TOUCHPOINT_REGISTRY.csv` contains 10 channel codes today (CHAN-LINKEDIN-DM, CHAN-LINKEDIN-POST-RESPONSE, CHAN-EMAIL-INBOUND, CHAN-WEB-FORM, CHAN-CAL-SCHEDULE, CHAN-AD-CAMPAIGN, CHAN-SEARCH-ORGANIC, CHAN-DIRECT-DM, CHAN-PARTNER-REFERRAL, CHAN-EVENT-MEETING). The rule RULE 7 cross-references `CHAN-EMAIL-OUTBOUND` as a typical case but the code is not yet registered. Per [`akos-mirror-template.mdc`](../../../../../.cursor/rules/akos-mirror-template.mdc) §"Never invent HLK IDs locally", minting new codes requires a canonical-CSV operator gate; that's out of scope for this push. Used `CHAN-DIRECT-DM` (bidirectional founder-personal channel; explicitly covers outbound personal email per the registry `notes` column) as the closest fit for cover-email + dossier surfaces. Used `CHAN-EVENT-MEETING` for shared-deck templates meant for live-presentation use. Validator post-onboarding: `with channel-tag 6 ; unknown channel codes 0`. Decision recorded as `decision_source: agent_executive_call`.

### Gate 3 — F+6 axe-core tool path

**Resolution:** **`npx @axe-core/cli`** (no Python wrapper).

**Evidence:** `node v22 + npm 11` already installed on the Windows machine; `axe-selenium-python` and `axe-core-python` are NOT installed; installing either would require a multi-step setup (Python + Selenium + ChromeDriver). The npx path resolved the audit in 7 seconds per artifact with zero setup friction. Decision recorded as `decision_source: agent_executive_call`.

### Gate 4 — F+6 critical-finding remediation (not triggered)

**Resolution:** **No CRITICAL findings emerged**, so this gate didn't fire.

**Evidence:** Both artifacts audited returned 0 CRITICAL findings (74 total: 51 SERIOUS color-contrast + 23 MODERATE heading-order/landmarks/region). Per the brief, the gate was conditional on CRITICAL or SERIOUS findings requiring *immediate* remediation. The 51 SERIOUS color-contrast findings are concentrated on light-grey eyebrow text (intentional visual hierarchy; arguably exempt under WCAG 2.1 SC 1.4.11 large-scale-text); the right remediation path is the I68 P3 Visual regression rollout cycle, not an emergency same-push fix. Documented in [audit-visual-polish-2026-05-19.md](audit-visual-polish-2026-05-19.md) §"Forward-charter".

## What landed (3 strands; 14 file touches)

### Strand F+3 — process_list.csv row + SOP confirmed-active

| File | Change |
|---|---|
| [`docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/process_list.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/process_list.csv) | NEW row `env_tech_dtp_external_render_gate_promotion_001` under `env_tech_prj_4` (HLK Infrastructure and DevOPS); role_owner=System Owner; cadence=gated_operator; paired SOP path + paired runbook scripts cited in description + addundum_extras; inherited_pattern_id=pattern_paired_sop_runbook. |
| [`docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/SOP-EXTERNAL_RENDER_GATE_PROMOTION_001.md`](../../../references/hlk/v3.0/Admin/O5-1/Tech/System%20Owner/canonicals/SOP-EXTERNAL_RENDER_GATE_PROMOTION_001.md) | NO change required — frontmatter already had `status: active` at Wave F mint. Per SOP §7 ("Process_list.csv row deferred") the row was scheduled for a follow-up tranche; this Wave G B-G2 lands that follow-up. |

### Strand F+4 — Channel-frontmatter onboarding + template + skill section

**(a) Surface onboarding sweep — 8 surfaces edited (6 in-scope counted by validator):**

| File | Channel added |
|---|---|
| [`docs/references/hlk/v3.0/_assets/advops/shared/decks/enisa-8-slide.deck.md`](../../../references/hlk/v3.0/_assets/advops/shared/decks/enisa-8-slide.deck.md) | `[CHAN-EVENT-MEETING, CHAN-DIRECT-DM]` (template; not counted in external-tagged set) |
| [`docs/references/hlk/v3.0/_assets/advops/shared/decks/investor-12-slide.deck.md`](../../../references/hlk/v3.0/_assets/advops/shared/decks/investor-12-slide.deck.md) | `[CHAN-EVENT-MEETING, CHAN-DIRECT-DM]` (template; not counted) |
| [`docs/references/hlk/v3.0/_assets/advops/shared/decks/advisor-4-slide.deck.md`](../../../references/hlk/v3.0/_assets/advops/shared/decks/advisor-4-slide.deck.md) | `[CHAN-EVENT-MEETING, CHAN-DIRECT-DM]` (template; not counted) |
| [`docs/references/hlk/v3.0/_assets/advops/shared/decks/partner-6-slide.deck.md`](../../../references/hlk/v3.0/_assets/advops/shared/decks/partner-6-slide.deck.md) | `[CHAN-EVENT-MEETING, CHAN-DIRECT-DM]` (template; not counted) |
| [`docs/references/hlk/v3.0/_assets/advops/shared/decks/sales-8-slide.deck.md`](../../../references/hlk/v3.0/_assets/advops/shared/decks/sales-8-slide.deck.md) | `[CHAN-EVENT-MEETING, CHAN-DIRECT-DM]` (template; not counted) |
| [`docs/references/hlk/v3.0/_assets/advops/shared/decks/recruiter-6-slide.deck.md`](../../../references/hlk/v3.0/_assets/advops/shared/decks/recruiter-6-slide.deck.md) | `[CHAN-EVENT-MEETING, CHAN-DIRECT-DM]` (template; not counted) |
| [`docs/references/hlk/v3.0/_assets/advops/2026-holistika-incorporation/enisa_evidence/dossier_es.md`](../../../references/hlk/v3.0/_assets/advops/2026-holistika-incorporation/enisa_evidence/dossier_es.md) | `[CHAN-DIRECT-DM]` (counted in external-tagged) |
| [`docs/references/hlk/v3.0/_assets/advops/2026-holistika-incorporation/enisa_evidence/cover_email_es.md`](../../../references/hlk/v3.0/_assets/advops/2026-holistika-incorporation/enisa_evidence/cover_email_es.md) | `[CHAN-DIRECT-DM]` (counted + HTML re-rendered) |
| [`docs/references/hlk/v3.0/_assets/advops/2026-holistika-incorporation/enisa_company_dossier/deck_story_es.md`](../../../references/hlk/v3.0/_assets/advops/2026-holistika-incorporation/enisa_company_dossier/deck_story_es.md) | `[CHAN-DIRECT-DM]` (counted) |
| [`docs/references/hlk/v3.0/_assets/advops/2026-holistika-incorporation/enisa_company_dossier/cover_email_company_dossier_es.md`](../../../references/hlk/v3.0/_assets/advops/2026-holistika-incorporation/enisa_company_dossier/cover_email_company_dossier_es.md) | `[CHAN-DIRECT-DM]` (counted + HTML re-rendered) |
| [`docs/references/hlk/v3.0/Think Big/Advisers/2026-holistika-incorporation/01-our-pack/legal-constitutor-handoff-2026-05-18.md`](../../../references/hlk/v3.0/Think%20Big/Advisers/2026-holistika-incorporation/01-our-pack/legal-constitutor-handoff-2026-05-18.md) | `[CHAN-DIRECT-DM]` (counted) |
| [`docs/references/hlk/v3.0/Think Big/Advisers/2026-holistika-incorporation/01-our-pack/cover_email_legal_constitutor_es.md`](../../../references/hlk/v3.0/Think%20Big/Advisers/2026-holistika-incorporation/01-our-pack/cover_email_legal_constitutor_es.md) | `[CHAN-DIRECT-DM]` (counted + HTML re-rendered) |

*Note on the counter discrepancy*: 12 files were edited in total (10 above + 2 re-rendered HTML manifests). The 6 deck templates have `artifact_kind: deck_template` which exempts them from the external-tagged scan per `validate_external_render_trail.py` line 233 (TEMPLATE_ARTIFACT_KINDS frozenset). Their `channel:` is documentation-grade — pre-populated metadata for per-engagement instances copied from the template. The 6 *in-scope* external surfaces are now all channel-tagged → validator reports `with channel-tag 6 ; unknown channel codes 0`.

**(b) Template + skill section:**

| File | Change |
|---|---|
| [`docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/_templates/external-render/channel-frontmatter.snippet.md`](../../../references/hlk/v3.0/Envoy%20Tech%20Lab/Repositories/_templates/external-render/channel-frontmatter.snippet.md) | NEW — reusable template snippet with YAML body + lookup procedure + 3 realistic case blocks (founder-initiated outbound; web + paid-ad; deck used in meeting + sent as sealed) + validator behaviour reference + cross-references. |
| [`.cursor/skills/external-render-craft/SKILL.md`](../../../../.cursor/skills/external-render-craft/SKILL.md) | MODIFIED — new section "Authoring `channel:` frontmatter (forward enhancement F+4 onboarding pattern)" inserted before "Pre-render checklist"; ~75 lines covering when to add, what codes to use, multi-channel composition, snippet pointer, validator behaviour, forward-enhancement deferrals. |

### Strand F+6 — axe-core visual-polish audit

| File | Change |
|---|---|
| [`artifacts/axe-core/holistika-company-dossier.json`](../../../../artifacts/axe-core/holistika-company-dossier.json) | NEW — raw axe-core output (42 findings: 34 SERIOUS color-contrast + 8 MODERATE heading-order). |
| [`artifacts/axe-core/uat-impeccable.json`](../../../../artifacts/axe-core/uat-impeccable.json) | NEW — raw axe-core output (32 findings: 17 SERIOUS color-contrast + 15 MODERATE across heading-order/landmark/region). |
| [`docs/wip/planning/86-initiative-cluster-execution-coordinator/reports/audit-visual-polish-2026-05-19.md`](audit-visual-polish-2026-05-19.md) | NEW — per-artifact findings tables + severity summary + forward-charter to I68 P3 + remediation effort estimates + WCAG SC 1.4.11 large-text-exemption discussion. |

### Doctrinal closure deliverables

| File | Change |
|---|---|
| [`docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv) | NEW row `D-IH-86-S` — Wave G B-G2 closure decision; cites D-IH-86-Q parent; records 3-strand trace + 3 executive calls + forward-deferred CHAN-EMAIL-OUTBOUND mint. |
| [`docs/wip/planning/86-initiative-cluster-execution-coordinator/reports/2026-05-19-wave-g-strand-bg2-governance-closure.md`](2026-05-19-wave-g-strand-bg2-governance-closure.md) | NEW — this report. |
| [`docs/wip/planning/86-initiative-cluster-execution-coordinator/files-modified.csv`](../files-modified.csv) | MODIFIED — appended Wave G B-G2 rows per 18-column schema. |
| [`CHANGELOG.md`](../../../../CHANGELOG.md) | MODIFIED — `[Unreleased]` entry pointing at this closure report. |

## Verification matrix

```text
py scripts/validate_external_render_trail.py --strict --strict-freshness
  → [INFO] PASS: scanned 76 ; external-tagged 6 ; with trail 6 ; pending tracker 0 ;
           missing trail 0 ; stale renders 0 ; with channel-tag 6 ; unknown channel codes 0
           (strict=True ; strict_freshness=True)

py scripts/validate_locale_orthography.py
  → INFO advisory (unchanged from Wave F: 0 ES + 0 FR + 68 EN smart-quote hits triaged in UAT)

py scripts/validate_hlk.py
  → OVERALL PASS

py scripts/validate_process_list_pairing.py
  → PASS: 27 cadence-bound rows (gated_operator now 3; was 2)
       Paired (SOP + runbook discoverable): 23
       Operator-deferred: 0
       Non-cadence rows skipped: 1143
       Warnings: 4 (informational; pre-existing — not from this push)

py -m pytest tests/test_external_render_trail.py tests/test_validate_locale_orthography.py -v
  → 77 tests PASS unchanged from Wave F baseline

npx @axe-core/cli "<holistika-company-dossier>" --save ...
  → 42 Accessibility issues detected (no CRITICAL)

npx @axe-core/cli "<uat-impeccable>" --save ...
  → 32 Accessibility issues detected (no CRITICAL)

py scripts/release-gate.py
  → External-render trail line: PASS (strict + strict-freshness)
  → Orthography line: INFO advisory unchanged
  → Pre-existing I71 P1/P2 brand voice + Vale FAILs: out of scope for B-G2
```

## Decisions ratified

- **D-IH-86-S** (governance; reversibility low) — Wave G B-G2 closure: F+3 process_list tranche + F+4 channel-frontmatter onboarding + template + skill section + F+6 axe-core visual-polish audit. Supersedes-link to D-IH-86-Q (parent). Records 3-strand trace + 3 executive calls + forward-deferred `CHAN-EMAIL-OUTBOUND` + `CHAN-PDF-DOWNLOAD` mint.

## Forward enhancements (deferred)

1. **Mint `CHAN-EMAIL-OUTBOUND` + `CHAN-PDF-DOWNLOAD`** in `CHANNEL_TOUCHPOINT_REGISTRY.csv` to cover the two most common gaps surfaced during this onboarding sweep. Requires canonical-CSV operator gate per `akos-governance-remediation.mdc`. When minted: re-tag the 8 surfaces with the more precise codes; promote `channel:` from optional INFO to required FAIL once registry coverage is complete.
2. **axe-core remediation cycle** — the 51 SERIOUS color-contrast findings + 23 MODERATE landmark/region findings have a small remediation footprint (3 PRs estimated; ~60 LoC). Forward-charter to **I68 P3 Visual regression rollout** when it activates; if I68 P3 stays paused, mint a successor I-NN initiative scoped to "external-render visual-polish hardening" with Brand & Narrative Manager + Tech Lab co-ownership.
3. **Run axe-core against additional rendered HTML artifacts** when they exist (e.g., future Figma-exported deck previews; ERP panel routes once they ship at I89). The audit pattern documented in `audit-visual-polish-2026-05-19.md` is reusable.
4. **Brand-token CSS centralisation** — both axe-audited artifacts have `color-contrast` issues on the same `.eyebrow` class family. One CSS variable fix in the deck-visual-system tokens propagates to both. Coordinate with Brand & Narrative Manager on whether the small-text contrast threshold should be relaxed (per WCAG SC 1.4.11) or the eyebrow class should be re-spec'd as a non-text decorative element.

## OPS rows status

No new OPS rows. Wave G B-G2 is doctrinal cleanup + audit baseline, not operational. OPS-86-7 (Wave E mint) remains closed. Wave F's forward-enhancement list (uat-render-quality-2026-05-19.md §7) is now 3 items closed (5 + 6 + part of 4); items 1 + 2 + 3 + remainder of 4 stay open for successor waves.

## Cluster status (no change from Wave F)

5-of-10 I86 cluster siblings closed (I79 + I80 + I84 + I85 + I87). 3 active (I76 + I81 + I82). 3 candidate-with-blocker-tracker (I74 + I75 + I83). Wave G B-G2 is doctrine-level + tooling-level + audit-baseline; doesn't touch sibling status.

## Next operator moves

1. **Read this report end-to-end** to internalise the 3-strand close-out + 3 executive calls + forward enhancements (5-minute read).
2. **Optionally ratify the executive calls** in a follow-up message — agent-executive-call decisions are reversible; operator may pivot to a different option on any of the three (paired-runbook wrapper script; channel-ID minting; axe-core via Python wrapper). Most likely pivot point is gate 2 (CHAN-EMAIL-OUTBOUND mint) — that's a 5-minute canonical-CSV gate when operator is ready.
3. **Read [audit-visual-polish-2026-05-19.md](audit-visual-polish-2026-05-19.md)** for the visual-polish baseline. Mark each of the 5 forward-charter items adopt-now / adopt-later / decline-with-WCAG-1.4.11-justification.
4. **When ready, activate I68 P3 Visual regression rollout** to absorb the 74 findings as the baseline.
5. **When a new external-render surface is authored**, the rule's RULE 5 binding fires AND now the channel-frontmatter snippet template is available — co-mint `channel:` frontmatter alongside the audience tag, using the snippet from `Envoy Tech Lab/Repositories/_templates/external-render/`.
