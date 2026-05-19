---
status: active
classification: closure-report
intellectual_kind: wave_closure_appendix
authority: PMO
artifact_role: derived
ratifying_decisions: [D-IH-86-P, D-IH-86-Q]
parent_decision: D-IH-86-Q
language: en
last_review: 2026-05-19
audience: J-OP
---

# Wave F — External-Render Doctrine Closure (closure appendix)

Follow-up to the [Wave E external-render canon report](2026-05-19-wave-e-external-render-canon.md) and [Tier 1 commit 665a077](https://github.com/FraysaXII/openclaw-akos/commit/665a077). Wave F closes the INFO → FAIL ramp opened at D-IH-86-P by ratifying **D-IH-86-Q** and flipping the gate, in the same chat session that shipped the Wave E doctrine.

## Why this is "Wave F"

Wave E (commit `e32d21c`) shipped the canonical rule + skill + validator + tracker as INFO advisory. Tier 1 (commit `665a077`) added the sha256-freshness sub-validator, the `render_cover_email.py` paired runbook, and the test suite. Operator surfaced a substantive scope-expansion at the Wave F second axis-2 ratify gate (option **B1** strict-per-locale orthography + option **C3** channel-canonical FK-resolve INFO + option **A3** all-strands-in-wave-F) that named three additional concerns under the umbrella of the operator's verbatim feedback:

> *"the visual renders are correct but still have bugs, feel a little bit artificial at times, have orthography errors like no ñ where it must be, I guess French is the same and English too. And I fear we are not using our channel canonicals to ensure we get the correct message to the correct audience in the correct format to convey or achieve a concrete objective for a given goal task or else. With our best taste. I feel that this is only valid for the renders I immediately have been requested (and very focused on ENISA, like too much) and it's as if I don't have lots of formats in scope like any company like mine. That's why I need you to ensure our renders and copy are up to the task no matter what and that we are completely scalable."*

The five strands derived from this feedback all landed in Wave F before the gate flip:

1. **Strand 1 — Gate promotion (this report's headline).** D-IH-86-Q ratifies the INFO → FAIL flip in `config/verification-profiles.json` + `scripts/release-gate.py`.
2. **Strand 2 — Paired SOP+runbook for gate promotion.** [`SOP-EXTERNAL_RENDER_GATE_PROMOTION_001`](../../../references/hlk/v3.0/Admin/O5-1/Tech/System%20Owner/canonicals/SOP-EXTERNAL_RENDER_GATE_PROMOTION_001.md) under Tech/System Owner/canonicals — the human-readable promotion + demotion procedure, paired with the validator script as runbook. v3.1 quality bar: 9 sections + frontmatter `governance_rules` + `canonical_dependencies` + `paired_runbook` field.
3. **Strand 3a — Orthography validator (mechanical "taste" enforcement).** [`scripts/validate_locale_orthography.py`](../../../../scripts/validate_locale_orthography.py) + [`akos/orthography.py`](../../../../akos/orthography.py) Pydantic chassis — covers ES + FR + EN with per-locale strict modes; 31 ES anti-patterns + 27 FR anti-patterns + EN smart-quote threshold scan. Wired into release-gate as INFO advisory per B1 ratify (per-locale promotion deferred to next operator pass once UAT triages the 68 EN findings on 2 surfaces).
4. **Strand 3b — UAT-evidence pass on rendered artifacts.** [`uat-render-quality-2026-05-19.md`](uat-render-quality-2026-05-19.md) — per-artifact findings table over 6 external surfaces + 1 J-OP-only orthography-scope surface; operator sign-off checklist of 7 items; forward-enhancement list (render-step auto-curl, strict-EN promotion, LLM-eval, visual-polish audit).
5. **Strand 4 — Channel-canonical cross-reference axis.** §RULE 7 added to [`akos-external-render-discipline.mdc`](../../../../.cursor/rules/akos-external-render-discipline.mdc); Surface 0 pre-flight added to [`external-render-craft/SKILL.md`](../../../../.cursor/skills/external-render-craft/SKILL.md); [`validate_external_render_trail.py`](../../../../scripts/validate_external_render_trail.py) extended with `channel:` frontmatter FK-resolve against [`CHANNEL_TOUCHPOINT_REGISTRY.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/CHANNEL_TOUCHPOINT_REGISTRY.csv) (INFO-only per C3 ratify). Codifies the **audience × channel × format** three-axis framing the operator named (the original RULE 2 matrix is audience × format only; channel is the orthogonal third axis).

## What landed (5 strands; 13 file touches)

### Strand 1 — Gate promotion (this commit)

| File | Change |
|---|---|
| [`docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv) | NEW row `D-IH-86-Q` — Wave F closure decision; cites D-IH-86-P parent; records 5-strand ratification trace + 3-axis operator answers (B1 + C3 + axis-1 lane_d novel-framing) + reversibility low + demotion path via SOP §6. |
| [`.cursor/rules/akos-external-render-discipline.mdc`](../../../../.cursor/rules/akos-external-render-discipline.mdc) | MODIFIED RULE 6 — closure note added (`Gate flipped to FAIL on 2026-05-19 via D-IH-86-Q`) + cross-link to paired SOP for demotion. |
| [`config/verification-profiles.json`](../../../../config/verification-profiles.json) | MODIFIED `validate_external_render_trail` step — `argv` extended from `["scripts/validate_external_render_trail.py"]` to `["scripts/validate_external_render_trail.py", "--strict", "--strict-freshness"]`; description updated to record the promotion. |
| [`scripts/release-gate.py`](../../../../scripts/release-gate.py) | MODIFIED `run_external_render_trail_validation` — now invokes with `--strict --strict-freshness`; result row category flipped `INFO` → `FAIL` (PASS when validator returns 0; FAIL when 1); logger message + docstring updated to record the promotion trace. |
| [`docs/wip/planning/_trackers/external-render-pending-tracker.md`](../external-render-pending-tracker.md) | MODIFIED preamble — `gate_state: strict` frontmatter added; gate-state header block prepended explaining the flip + demotion procedure cross-link to SOP. |

### Strand 2 — Paired SOP+runbook

| File | Change |
|---|---|
| [`docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/SOP-EXTERNAL_RENDER_GATE_PROMOTION_001.md`](../../../references/hlk/v3.0/Admin/O5-1/Tech/System%20Owner/canonicals/SOP-EXTERNAL_RENDER_GATE_PROMOTION_001.md) | NEW — v3.1 SOP shape (frontmatter with `governance_rules` + `canonical_dependencies` + `paired_runbook`; 9 sections: Purpose / Scope / Preconditions / Promotion procedure 5 steps / Verification / Demotion procedure soft+hard / Acceptance criteria / Cross-references / Decision lineage). Paired runbook = `scripts/validate_external_render_trail.py` itself (the SOP describes the operator workflow; the script is the executable). |
| [`scripts/validate_external_render_trail.py`](../../../../scripts/validate_external_render_trail.py) | MODIFIED docstring — bidirectional cross-reference to the SOP added (`RULE 7` + SOP path); confirms the script is the paired runbook for SOP-EXTERNAL_RENDER_GATE_PROMOTION_001. |

### Strand 3a — Orthography validator

| File | Change |
|---|---|
| [`akos/orthography.py`](../../../../akos/orthography.py) | NEW — Pydantic chassis (`OrthographyAntiPattern` model with `locale` Literal + `ascii_form` + `canonical_form` + `category` enum + `rationale`); 31 ES anti-patterns + 27 FR anti-patterns + EN smart-quote threshold scan (EN word-list intentionally empty per scope contract); SSOT cites `BRAND_<LANG>_PATTERNS.md` per row. |
| [`scripts/validate_locale_orthography.py`](../../../../scripts/validate_locale_orthography.py) | NEW — sister validator to `validate_external_render_trail.py`; scans same SCAN_GLOBS; only acts on `language:`-tagged surfaces; strips frontmatter + code blocks + URLs + markdown link targets; `--strict` + `--strict-es` + `--strict-fr` + `--strict-en` flags; `AKOS_LOCALE_ORTHOGRAPHY_STRICT=1` env override. |
| [`tests/test_validate_locale_orthography.py`](../../../../tests/test_validate_locale_orthography.py) | NEW — 45 tests covering Pydantic chassis + language extraction + prose stripping + word-list scanning for ES + FR + EN smart quotes + end-to-end strict/advisory mode + env-var override. |
| [`config/verification-profiles.json`](../../../../config/verification-profiles.json) | MODIFIED — added `validate_locale_orthography` step to `pre_commit` profile as INFO advisory; per-locale strict flags documented in `description`. |
| [`scripts/release-gate.py`](../../../../scripts/release-gate.py) | MODIFIED — added `run_locale_orthography_validation()` function + INFO row in `main()` results list. |

### Strand 3b — UAT-evidence pass

| File | Change |
|---|---|
| [`docs/wip/planning/86-initiative-cluster-execution-coordinator/reports/uat-render-quality-2026-05-19.md`](uat-render-quality-2026-05-19.md) | NEW — per-artifact findings table over 6 external surfaces + 1 J-OP-only orthography-scope surface; 3 dimensions per artifact (orthography mechanical + visual polish mechanical-ish + naturalness operator-sign-off); 7-item operator sign-off checklist; mechanical evidence sections quoting validator output verbatim; 4 forward enhancements deferred to next wave. |

### Strand 4 — Channel-canonical cross-reference

| File | Change |
|---|---|
| [`.cursor/rules/akos-external-render-discipline.mdc`](../../../../.cursor/rules/akos-external-render-discipline.mdc) | MODIFIED — §RULE 7 added codifying audience × channel × format three-axis framing + channel × format compatibility matrix + advisory INFO-only drift gate behavior; CHANNEL_TOUCHPOINT_REGISTRY.csv cross-reference added to Cross-references section + @-reference at file bottom. |
| [`.cursor/skills/external-render-craft/SKILL.md`](../../../../.cursor/skills/external-render-craft/SKILL.md) | MODIFIED — Surface 0 added (Audience × Channel × Language × Objective pre-flight lookup); surface-picker decision tree + two-surface composition guidance + anti-patterns updated. |
| [`scripts/validate_external_render_trail.py`](../../../../scripts/validate_external_render_trail.py) | MODIFIED — `CHANNEL_REGISTRY_PATH` + `CHANNEL_FIELD_PATTERN` + `CHANNEL_CODE_PATTERN` regexes added; `_load_valid_channel_codes()` cached helper; `_extract_channel()` frontmatter parser; `validate()` integrates per-file channel FK-resolve at INFO advisory; summary row extended with `files_with_channel` + `unknown_channel_codes` counters. |
| [`tests/test_external_render_trail.py`](../../../../tests/test_external_render_trail.py) | MODIFIED — 8 new tests covering channel registry loading + channel extraction (single + multi + capitalized) + FK-resolve valid/invalid cases; 32 tests pass total. |

## Verification (P7)

```text
py scripts/validate_external_render_trail.py --strict --strict-freshness
  → [INFO] PASS: scanned 76 ; external-tagged 6 ; with trail 6 ; pending tracker 0 ;
           missing trail 0 ; stale renders 0 ; with channel-tag 0 ; unknown channel codes 0
           (strict=True ; strict_freshness=True)

py scripts/validate_locale_orthography.py
  → [INFO] PASS: scanned 38 ; language-tagged 38 ; with hits 2 ; total hits 68
           (es=0 fr=0 en=68 ; strict_es=False strict_fr=False strict_en=False)
           Findings: 2 EN surfaces (deck-visual-system.md J-OP-only;
                                    legal-constitutor-handoff-2026-05-18.md J-AD).
           Triaged in uat-render-quality-2026-05-19.md surface 6 + 7.

py scripts/validate_hlk.py
  → PASS (0 hard FAILs)

pytest tests/test_external_render_trail.py tests/test_validate_locale_orthography.py -v
  → 77 tests PASS (32 trail + 45 orthography)

py scripts/release-gate.py
  → External-render trail line now PASS row (was INFO; flipped per D-IH-86-Q)
  → Orthography line is INFO row (per B1 ratify)
  → Pre-existing I71 P1 BRAND voice register FAIL + I71 P2 Vale sibling FAIL: out of scope
```

## Decisions ratified

- **D-IH-86-Q** (governance; reversibility low) — Wave F closure: external-render trail gate promotion INFO → FAIL with sha256-freshness strict. Supersedes-link to D-IH-86-P (parent). Records 3-axis operator answers + 5-strand ship trace + demotion path.

## OPS rows status

- No new OPS rows. Wave F is the **closure** of the doctrine ramp; OPS-86-7 (Wave E mint) was already closed at the Wave E commit. The follow-up workstreams identified by the Strand 3b UAT (render-step auto-curl + strict-EN promotion + LLM-eval + visual-polish audit) are forward enhancements suitable for future I-NN initiatives or operator-driven candidate promotions. No OPS row is minted at this commit because each follow-up is either operator-triage-dependent (EN smart-quote findings on 2 surfaces) or successor-initiative-scoped.

## Forward enhancements (deferred)

These are noted in [`uat-render-quality-2026-05-19.md`](uat-render-quality-2026-05-19.md) §7 but not minted in this Wave F:

1. **Render-step auto-curl (option (a) for EN smart-quote findings).** Post-render step in `render_dossier.py` / `export_adviser_handoff.py` that runs a smart-quote conversion pass on the HTML/PDF output before the manifest seal. Systemic fix to the smart-quote leak class. Effort: small (1 commit; ~50 LoC).
2. **Strict-EN orthography promotion.** Once UAT surfaces 6 + 7 close (option (a) or (b) or (c) ratified), promote `validate_locale_orthography.py` to `--strict-en` in release-gate + verification-profiles. Mirror today's ES + FR posture (clean = ready for strict promotion).
3. **LLM-eval for naturalness dimension.** Per D-IH-71-S, an LLM-eval pass with per-locale rubric (pulling from `BRAND_<LANG>_PATTERNS.md`) can replace operator-naturalness sign-off for most surfaces. Forward-charter to successor initiative (suggested I88+ once I76 MADEIRA productization closes).
4. **Visual-polish automated audit.** Integrate `axe-core` + visual-regression snapshots (`playwright + snapshot`) over the 6 rendered artifacts as a release-gate INFO row, mirroring `playwright_a11y_smoke` precedent.
5. **`process_list.csv` row for the SOP+runbook pair.** Per SOP-META order (CSV-before-SOP), `env_tech_dtp_external_render_gate_promotion_001` row should land in next operator-approved tranche, then SOP frontmatter `status: review` flips to `status: active`. The SOP runs at `review` today (D-IH-86-Q ratified the SOP content; the canonical-CSV gate is a separate operator review).
6. **Channel-canonical promotion.** Once a handful of external-render surfaces carry `channel:` frontmatter and the unknown-channel-codes counter stays at zero across multiple commits, promote the RULE 7 drift gate from INFO to FAIL via a follow-up D-IH-86-* decision (mirroring the same INFO → FAIL ramp pattern this Wave F closes for the trail validator).

## Cluster status (no change from Wave E)

5-of-10 I86 cluster siblings closed (I79 + I80 + I84 + I85 + I87). 3 active (I76 + I81 + I82). 3 candidate-with-blocker-tracker (I74 + I75 + I83). Wave F is doctrine-level + tooling-level; doesn't touch sibling status.

## Next operator moves

1. **Read the Wave F report (this file) end-to-end** to internalise the 5-strand scope expansion + the gate flip + the deferred enhancements (5-minute read).
2. **Read the UAT report** [`uat-render-quality-2026-05-19.md`](uat-render-quality-2026-05-19.md) §3 (per-artifact findings table) + §6 (operator sign-off checklist). Mark each of the 7 rows PASS / REVIEW-PENDING / REVIEW-CLOSED.
3. **Triage the 2 EN smart-quote findings** (UAT surfaces 6 + 7): pick option (a) render-step auto-curl (recommended), option (b) hand-edit source markdown, or option (c) accept ASCII quotes. Record the choice in a follow-up commit + close the operator-sign-off-checklist item.
4. **When ready, ratify the strict-EN orthography promotion** by editing `scripts/release-gate.py` `run_locale_orthography_validation` to pass `--strict-en` (mirror the gate-promotion shape this Wave F just landed for the trail validator).
5. **When a new external-render surface is authored**, the rule's RULE 5 binding fires: the agent must co-mint a render trail OR file a render-pending tracker entry. The validator now FAILs CI if either is missing — this is the structural shift Wave F delivered. The render-pending tracker remains the durable safety valve for surfaces that can't render today.
