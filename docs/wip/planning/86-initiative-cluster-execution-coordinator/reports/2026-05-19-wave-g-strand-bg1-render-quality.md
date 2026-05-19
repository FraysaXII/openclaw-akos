---
status: active
classification: closure-report
intellectual_kind: wave_closure_appendix
authority: PMO
artifact_role: derived
ratifying_decisions: [D-IH-86-Q, D-IH-86-R]
parent_decision: D-IH-86-R
language: en
last_review: 2026-05-19
audience: J-OP
---

# Wave G Bundle B-G1 — Render Quality (closure appendix)

Follow-up to the [Wave F external-render doctrine closure report](2026-05-19-wave-f-external-render-doctrine-closure.md) and the [Wave F UAT-evidence pass](uat-render-quality-2026-05-19.md). Wave G Bundle B-G1 lands the **first two forward enhancements** listed in §7 of the UAT report (items 1 + 2) — the render-step auto-curl pass and the strict-EN orthography promotion — in a single chained commit per the user's bundle instruction.

## Why this is "Wave G Bundle B-G1"

Wave F (commit `4736027`) ratified **D-IH-86-Q** and flipped the external-render trail gate from INFO to FAIL. Wave F's UAT-evidence report listed six forward enhancements deferred to the next wave:

1. **Render-step auto-curl** (option (a) for the 68 EN smart-quote findings on `deck-visual-system.md` + `legal-constitutor-handoff-2026-05-18.md`).
2. **Strict-EN orthography promotion** (once option (a)/(b)/(c) ratifies + the EN findings clear).
3. LLM-eval for naturalness dimension (forward-charter; suggested I88+).
4. Visual-polish automated audit (`axe-core` + playwright snapshots).
5. `process_list.csv` row for the SOP+runbook pair.
6. Channel-canonical drift gate INFO → FAIL promotion.

Wave G **Bundle B-G1** scopes items 1 + 2 — the render-quality strands that pair tightly into a single dependency chain (F+1 enables F+2). Items 3-6 land in sibling bundles (B-G2 governance closure handles items 4-6 per the existing `D-IH-86-S` row already in the decision register; item 3 forward-charters to I88+).

## What landed (2 strands; 9 file touches + 1 new doctrine row + 1 new test file)

### Strand F+1 — Render-step auto-curl (`apply_smart_quotes`)

| File | Change |
|---|---|
| [`akos/orthography.py`](../../../../akos/orthography.py) | NEW `apply_smart_quotes(text, language)` function + helpers (`_AUTOCURL_PROTECT_PATTERNS`, `_stash_protected_regions`, `_unstash_protected_regions`, `_apply_quotes_en`, `_apply_quotes_guillemet`, `_AUTOCURL_DISPATCH`). Multi-pass placeholder protection of code blocks + HTML tags (including attribute values) + URLs + HTML comments + markdown fenced/inline code. State-machine regex curl on remaining text. EN: U+201C/U+201D + U+2018/U+2019. ES + FR: U+00AB/U+00BB + U+2018/U+2019. Module docstring extended with the Wave G B-G1 scope contract + decision lineage. |
| [`akos/hlk_pdf_render.py`](../../../../akos/hlk_pdf_render.py) | MODIFIED `render_pdf_branded` — after `body_html = _md_lib.markdown(...)` + `_friendly_callout_labels_html(...)`, calls `apply_smart_quotes(body_html, language=language_hint)` (local import to dodge circular at module load). Rendered HTML body carries locale-correct curly quotes pre-WeasyPrint. Comment block documents the rationale + cites operator stance per Wave F UAT §7. |
| [`scripts/validate_locale_orthography.py`](../../../../scripts/validate_locale_orthography.py) | MODIFIED `_scan_en_smart_quotes(body)` — now applies `apply_smart_quotes(body, "en")` before counting straight double-quotes. Gate semantics shifted from "source must be curly" to "delivery surface (post-curl) must be curly". Single-quote scan still omitted (apostrophe ambiguity). Docstring records the shift + cites operator stance. |
| [`tests/test_orthography.py`](../../../../tests/test_orthography.py) | NEW test file. 26 tests across 5 classes: `TestEnglishSmartQuotes` (4 tests — basic pairs, apostrophes, multiple balanced, nested singles); `TestSpanishSmartQuotes` (3 tests — guillemets, multiple, apostrophes); `TestFrenchSmartQuotes` (2 tests — guillemets, apostrophe-in-prose); `TestProtectedRegions` (8 tests — pre/code/HTML-attr/URL/comment/markdown-fenced/markdown-inline protection); `TestIdempotenceAndEdgeCases` (7 tests — already-curly, empty, no-quotes, unknown-language, mixed-HTML, unicode, leading-apostrophe); `TestValidatorIntegrationPostCurlCount` (2 tests — end-to-end balanced-prose-to-zero + protected-attr-survives). |
| [`tests/test_validate_locale_orthography.py`](../../../../tests/test_validate_locale_orthography.py) | MODIFIED `TestEnglishSmartQuoteScan` — 2 existing raw-count tests amended to post-curl semantics (renamed `test_below_threshold_balanced_prose_post_curls_to_zero` + `test_balanced_multi_quote_post_curls_to_zero`); 2 new tests added (`test_quotes_inside_protected_html_attr_survive`, `test_quotes_inside_code_block_survive`); the already-curly test stays. |

### Strand F+2 — Strict-EN orthography promotion

| File | Change |
|---|---|
| [`config/verification-profiles.json`](../../../../config/verification-profiles.json) | MODIFIED `validate_locale_orthography` step — `argv` extended from `["scripts/validate_locale_orthography.py"]` to `["scripts/validate_locale_orthography.py", "--strict-en"]`. Description updated to record the Wave G B-G1 closure decision + the post-curl semantics shift + ES + FR remain advisory. |
| [`scripts/release-gate.py`](../../../../scripts/release-gate.py) | MODIFIED `run_locale_orthography_validation()` — now invokes the validator with `--strict-en`; result row category flipped from `INFO` to `PASS / FAIL` (mirrors `run_external_render_trail_validation` pattern). Logger message + docstring updated with the D-IH-86-R rationale. |
| [`tests/test_validate_locale_orthography.py`](../../../../tests/test_validate_locale_orthography.py) | EXTENDED `TestValidatorEndToEnd` — 3 new tests: `test_strict_en_clean_surface_passes` (balanced prose curls cleanly; --strict-en passes); `test_strict_en_excessive_protected_quotes_fails` (HTML-attr quotes trip threshold under --strict-en); `test_strict_en_does_not_force_es_fr` (per-locale strict respects locale scope). |
| [`docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/SOP-EXTERNAL_RENDER_GATE_PROMOTION_001.md`](../../../references/hlk/v3.0/Admin/O5-1/Tech/System%20Owner/canonicals/SOP-EXTERNAL_RENDER_GATE_PROMOTION_001.md) | MODIFIED — new section 6.1 "Sibling promotion: locale-orthography EN strict (Wave G B-G1; D-IH-86-R)" documenting the post-curl semantics + promotion mechanics + per-locale ES + FR advisory status + demotion path. `linked_decisions:` frontmatter extended to include D-IH-86-R. §8 Cross-references updated to cite D-IH-86-R. |
| [`docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv) | NEW row `D-IH-86-R` inserted between Q and S — Wave G B-G1 closure; cites D-IH-86-Q parent; records 2-strand ship trace + 3 executive design calls (algorithm choice; post-curl validator semantics; codepoint conventions) + verification matrix outcomes + demotion path. |

## Verification matrix (P7 of B-G1)

```text
py scripts/validate_external_render_trail.py --strict --strict-freshness
  → [INFO] PASS: scanned 76 ; external-tagged 6 ; with trail 6 ; pending tracker 0 ;
           missing trail 0 ; stale renders 0 ; with channel-tag 0 ; unknown channel codes 0
           (strict=True ; strict_freshness=True)
  → Wave F D-IH-86-Q gate remains PASS at the B-G1 commit.

py scripts/validate_locale_orthography.py --strict-en
  → [INFO] PASS: scanned 38 ; language-tagged 38 ; with hits 0 ; total hits 0
           (es=0 fr=0 en=0 ; strict_es=False strict_fr=False strict_en=True)
  → 68 EN findings from Wave F UAT eliminated under post-curl semantics. Strict-EN gate green.

py -m pytest tests/test_orthography.py tests/test_validate_locale_orthography.py -v
  → 76 tests PASS (26 new orthography + 50 amended/existing validator tests).

py scripts/validate_hlk.py
  → DECISION_REGISTER validator PASS (D-IH-86-R row schema-valid with 19 cols)
  → LANGUAGE_FRONTMATTER validator: 1 FAIL on a Wave G B-G2 work-in-progress file
    (docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/_templates/external-render/
    channel-frontmatter.snippet.md) — pre-existing in the workspace; out of scope for
    Wave G B-G1; the next agent shipping B-G2 must add the language: frontmatter key.
```

## Decisions ratified

- **D-IH-86-R** (governance; reversibility low) — Wave G B-G1 closure: render-step auto-curl + strict-EN orthography promotion. Supersedes-link to D-IH-86-Q (parent). Records 2-strand ship trace + 3 executive design calls (made under subagent execution context per the inline-ratify-craft skill recovery pattern, since AskQuestion tool is unavailable in this subagent) + verification matrix outcomes + demotion path.

## Three executive design calls (operator-reviewable)

Per the [`inline-ratify-craft skill`](../../../../.cursor/skills/inline-ratify-craft/SKILL.md) §"Pitfall: I have run the evidence sweep but I do not see clear options" recovery pattern, the subagent execution context lacks the `AskQuestion` tool. The user's task prompt explicitly named three inline-ratify gates; with operator ratification unreachable from a subagent, the agent made three executive calls. Each is recorded below for operator pivot if desired (every call is reversible by editing one function or one config field).

1. **Smart-quote algorithm choice** — Selected **multi-pass placeholder protection + state-machine regex** over (a) single-pass regex with negative look-behind for protection, (b) external library dependency (e.g., python-markdown's smartypants), (c) AST-walking the rendered HTML. Rationale: zero external deps, ~150 LoC, defensive protection of code blocks / HTML attributes / URLs / comments / markdown fenced+inline code in one pass before state-machine curls remaining text. Test coverage at 8 protected-region tests + 7 edge-case tests gives high confidence the algorithm is correct.

2. **Validator semantics: post-curl scan vs source-side cleanup** — Selected **post-curl scan in `_scan_en_smart_quotes`** over (a) source-side cleanup of the 2 flagged files, (b) operator-ratified deferral of source cleanup to a separate pass, (c) `apply_smart_quotes` as a separate command not wired into validation. Rationale: respects operator stance from Wave F UAT §7 (*"auto-curl is for rendered outputs, not for hand-authored markdown source-of-truth"*) — source markdown stays operator-author-friendly; delivery surface carries brand-correct typography; validator gates the delivery quality. Source files (`deck-visual-system.md`, `legal-constitutor-handoff-2026-05-18.md`) are untouched by this commit.

3. **Curly-quote codepoint conventions per locale** — Selected codepoints exactly as named in the user task prompt: EN → U+201C/U+201D (double) + U+2018/U+2019 (single); ES + FR → U+00AB/U+00BB (guillemets) + U+2018/U+2019 (single). Rationale: matches operator-provided spec verbatim; non-breaking spaces inside FR guillemets are deliberately NOT inserted (downstream CSS can polish letter-spacing if desired); helper stays renderer-agnostic and string-safe.

## Operator-acknowledged context: Wave G B-G2 work-in-progress in workspace

At the start of Wave G B-G1 execution, the workspace already carried in-flight Wave G B-G2 changes from an earlier coordinator pass (decision row `D-IH-86-S` was already minted in `DECISION_REGISTER.csv` referencing Wave G B-G2 closure). These files are present in the workspace but **not committed by this B-G1 push**, to preserve per-phase commit discipline per [`akos-governance-remediation.mdc`](../../../../.cursor/rules/akos-governance-remediation.mdc) §"Commit and phase discipline":

- `.cursor/skills/external-render-craft/SKILL.md` (channel-frontmatter authoring section)
- `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/process_list.csv` (B-G2 row)
- Multiple `cover_email_*.md` + `deck_*.md` + handoff markdowns (channel: frontmatter added)
- `docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/_templates/external-render/channel-frontmatter.snippet.md` (NEW; missing `language:` frontmatter — causes the LANGUAGE_FRONTMATTER FAIL noted above)
- `docs/wip/planning/86-initiative-cluster-execution-coordinator/reports/audit-visual-polish-2026-05-19.md` (B-G2 axe-core audit)
- `artifacts/axe-core/` (B-G2 audit artifacts)

The next coordinator agent shipping Wave G B-G2 must address the LANGUAGE_FRONTMATTER FAIL (one-line frontmatter addition to the snippet template) and commit those files under the `D-IH-86-S` decision row already prepared.

## OPS rows status

- No new OPS rows minted in B-G1. The forward enhancement "process_list.csv row for the SOP+runbook pair" (item 5 in the Wave F UAT §7) is scoped to Wave G B-G2 per the existing `D-IH-86-S` row already in the decision register.

## Forward enhancements (deferred to subsequent waves)

These remain forward-chartered from the Wave F UAT §7 list (items 3-6) — items 4-6 land in B-G2; item 3 is forward-charter to I88+:

1. **LLM-eval for naturalness dimension.** Per D-IH-71-S, an LLM-eval pass with per-locale rubric (pulling from `BRAND_<LANG>_PATTERNS.md`) can replace operator-naturalness sign-off for most surfaces. Forward-charter to successor initiative (suggested I88+ once I76 MADEIRA productization closes).
2. **Strict-ES + Strict-FR orthography promotion.** Both locales currently have 0 hits at the Wave G B-G1 commit. One operator-ratified decision away — append `--strict-es` and/or `--strict-fr` flag to the same argv in `config/verification-profiles.json` + `scripts/release-gate.py`. Mirrors today's --strict-en promotion shape.
3. **Visual-polish automated audit** (Wave G B-G2 in-flight; `D-IH-86-S`). Operator-acknowledged work-in-progress; not in scope for B-G1.
4. **`process_list.csv` row for the SOP+runbook pair** (Wave G B-G2 in-flight; `D-IH-86-S`).
5. **Channel-canonical drift gate INFO → FAIL promotion** (Wave G B-G2 in-flight; `D-IH-86-S`).

## Cluster status

Wave F closure left 5-of-10 I86 cluster siblings closed (I79 + I80 + I84 + I85 + I87). Wave G B-G1 is doctrine-level + tooling-level; doesn't touch sibling status. The cluster orchestrator's UAT-evidence + closure-report chain continues to grow.

## Next operator moves

1. **Verify the strict-EN gate flip end-to-end**: run `py scripts/release-gate.py` and confirm the Locale-orthography line now reports `[PASS]` (not `[INFO]`).
2. **If a future surface lands with intentionally straight quotes in HTML attribute values** (e.g., a new external-tagged template containing `<a href="...">` patterns at high density), the strict-EN gate may flag it. Either curl the HTML attribute values to single quotes (rare; usually the inverse) OR adjust `EN_STRAIGHT_QUOTE_THRESHOLD` higher.
3. **When ES + FR backfill scan stays clean across multiple commits**, ratify the strict-ES + strict-FR promotion via a follow-up `D-IH-86-*` decision row. One-line argv edit + this SOP §6.1 update mirror.
4. **Wave G B-G2** (channel-frontmatter onboarding + process_list tranche + axe-core audit) is in-flight in the workspace; the next coordinator agent should pick up there.

## Cross-references

- Parent doctrine: [`akos-external-render-discipline.mdc`](../../../../.cursor/rules/akos-external-render-discipline.mdc).
- Paired SOP+runbook: [`SOP-EXTERNAL_RENDER_GATE_PROMOTION_001`](../../../references/hlk/v3.0/Admin/O5-1/Tech/System%20Owner/canonicals/SOP-EXTERNAL_RENDER_GATE_PROMOTION_001.md) §6.1 (Wave G B-G1 extension).
- Parent decision: D-IH-86-Q (Wave F closure); sibling decision: D-IH-86-S (Wave G B-G2 in-flight).
- Operator framing source: [Wave F UAT §7](uat-render-quality-2026-05-19.md) deferred-enhancements list items 1 + 2.
- Inline-ratify recovery pattern: [`inline-ratify-craft skill`](../../../../.cursor/skills/inline-ratify-craft/SKILL.md) §"Pitfall: I have run the evidence sweep but I do not see clear options" (subagent execution-call discipline).
