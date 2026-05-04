---
language: en
status: closed
initiative: 57-cycle-closeout-live-validation
report_kind: phase-report
phase: P1
program_id: shared
plane: ops
authority: Founder + System Owner
last_review: 2026-05-04
---

# I57 P1 — Bucket 4 quick wins (2026-05-04)

## Outcome

All four Bucket 4 quick-wins shipped with regression tests:

1. **F-22a-EMIT-1** — `compliance_mirror_emit` now emits `NULL` for empty DATE columns instead of `''`. Closes the I22a Open follow-up that broke `sourcing_register_mirror.last_engagement_date` during the 2026-05-04 Supabase MasterData parity reconciliation.
2. **F-22a-EMIT-2** — `compliance_mirror_emit` now emits the documented blank-cell default (`false`) for known NOT-NULL bool columns, with a fail-loud `ValueError` for any future NOT-NULL bool column missing a documented default. Closes the I22a Open follow-up that broke `skill_registry_mirror.tools_required_waived`.
3. **OPS-54-1.a** — Single CSS rule `.locale button { color: var(--ink); border-color: var(--ink-2); }` pins inactive locale-button styling to high-contrast primitives. Closes the I54 live a11y audit F-1 (axe-core `color-contrast` Serious × 3 on `button[data-locale-set="en|es|fr"]`).
4. **OPS-54-1.b** — `tabindex="0"` + `aria-label` on `<pre id="handoff-example">` makes the scrollable region keyboard-focusable. Closes the I54 live a11y audit F-2 (axe-core `scrollable-region-focusable` Serious × 1).

Per [D-IH-57-C](../decision-log.md#d-ih-57-c--p1-commit-granularity-one-commit-per-fix-vs-one-bundled-commit) the fixes are intended to ship as **four separate commits** when this initiative lands; the engineering work itself is independent per fix.

## Files changed

| Fix | File | Change |
|:----|:-----|:-------|
| F-22a-EMIT-1 | [`scripts/sync_compliance_mirrors_from_csv.py`](../../../../scripts/sync_compliance_mirrors_from_csv.py) | `_emit_sourcing_register_upserts` rewritten to use the same `nullable_when_blank` idiom as `_emit_persona_scenario_registry_upserts`; new `DATE_COLUMNS = {"last_engagement_date"}` constant; doc-comment cites the I22a defect history |
| F-22a-EMIT-2 | [`scripts/sync_compliance_mirrors_from_csv.py`](../../../../scripts/sync_compliance_mirrors_from_csv.py) | `_emit_skill_registry_upserts` empty-bool branch now emits the column-keyed default; new `BOOL_COLUMN_DEFAULTS: dict[str, str \| None]` map enumerates `tools_required_waived → "false"`; missing entry raises `ValueError` so future NOT-NULL bool columns surface at emit time, not at apply time |
| OPS-54-1.a | [`static/madeira_control.html`](../../../../static/madeira_control.html) | New `.locale button { color: var(--ink); border-color: var(--ink-2); }` rule (single CSS line + comment block); aria-pressed=true rule unchanged (specificity wins for active state) |
| OPS-54-1.b | [`static/madeira_control.html`](../../../../static/madeira_control.html) | `<pre id="handoff-example">` gains `tabindex="0" aria-label="Madeira plan handoff schema example (scrollable)"` |

## Tests added

| Test | File | Locks |
|:-----|:-----|:------|
| `test_i57_emit_sourcing_register_empty_date_emits_null` | [`tests/test_sync_compliance_mirrors_from_csv.py`](../../../../tests/test_sync_compliance_mirrors_from_csv.py) | F-22a-EMIT-1 unit — empty DATE cell produces `NULL` |
| `test_i57_emit_sourcing_register_filled_date_round_trips` | same file | F-22a-EMIT-1 sanity — populated DATE round-trips as TEXT literal |
| `test_i57_emit_skill_registry_empty_bool_emits_documented_default` | same file | F-22a-EMIT-2 unit — empty bool produces `false`, never `NULL` |
| `test_i57_emit_skill_registry_truthy_bool_round_trips` | same file | F-22a-EMIT-2 sanity — all 10 documented truthy/falsy tokens map to the correct keyword |
| `test_i57_emit_skill_registry_full_csv_uses_documented_default_for_blanks` | same file | F-22a-EMIT-2 integration — full-CSV emit produces zero `, NULL,` substrings on the SKILL_REGISTRY mirror |
| `test_i57_emit_skill_registry_full_csv_includes_emitted_default_for_real_blanks` | same file | F-22a-EMIT-2 integration — at least one real CSV row emits `, false,` (proves the fix actually fires on the real data, not just the unit fixture) |
| `test_i57_locale_buttons_have_explicit_high_contrast_styling` | [`tests/playwright/test_madeira_control_a11y_dom.py`](../../../../tests/playwright/test_madeira_control_a11y_dom.py) | OPS-54-1.a regression — exact CSS rule presence in source HTML |
| `test_i57_handoff_example_is_keyboard_focusable` | same file | OPS-54-1.b regression — `tabindex="0"` + `aria-label` presence in source HTML |

**Test count delta:** +6 new tests in `test_sync_compliance_mirrors_from_csv.py` (5 → 11), +2 new tests in `test_madeira_control_a11y_dom.py` (15 → 17). Net +8 tests across the I57 P1 surface.

## Verification matrix

| Check | Command | Result |
|:------|:--------|:-------|
| Targeted regression sweep (mirror emit + a11y DOM) | `py -m pytest tests/test_sync_compliance_mirrors_from_csv.py tests/playwright/test_madeira_control_a11y_dom.py -v` | **PASS** (11 + 17 = 28 / 28) |
| Full pytest sweep | `py scripts/test.py all` | **PASS** (1764 passed / 7 skipped / 0 failed in 134.41s) |
| Live mirror emit profile | `py scripts/verify.py compliance_mirror_emit` | **PASS** (`compliance_mirror_count_only` + `compliance_mirror_write_sql`; 2.85 MB SQL written to `artifacts/sql/compliance_mirror_upsert.sql`) |
| Drift check | `py scripts/check-drift.py` | **PASS** (no drift; runtime matches repo state) |
| Inventory check | `py scripts/legacy/verify_openclaw_inventory.py` | **PASS** |
| HLK validator (full vault) | `py scripts/validate_hlk.py` | **PASS** (159 files / 0 errors) |

## Live SQL spot-checks (proof the fix lands on real CSV data)

Verified in `artifacts/sql/compliance_mirror_upsert.sql` after the P1 emit:

- **Line 1609 (`sourcing_register_mirror`)** — single VENDOR-EXAMPLE-001 row. The `last_engagement_date` cell is empty in the CSV; the SQL emits `NULL` (visible as `..., 'N4', 'N4', NULL, 'topic_sourcing_register', ...`). **Pre-fix:** would have emitted `''` and crashed at apply with PostgreSQL 22007 invalid_datetime_format.
- **Lines 1611-1615 (`skill_registry_mirror`)** — five rows. `tools_required_waived` is empty in 3 rows (`SKILL-MADEIRA-LOOKUP-V1`, `SKILL-ARCHITECT-PLAN-V1`, `SKILL-SHARED-LOCALE-DETECT-V1`); all three emit `false`. The two CSV rows with explicit `true` (`SKILL-EXECUTOR-RUN-V1`, `SKILL-VERIFIER-CHECK-V1`) round-trip as `true`. **Pre-fix:** the three blank rows would have emitted `NULL` and crashed at apply on the NOT-NULL constraint.

## Decisions captured during execution

- **D-IH-57-C affirmed** — Each of the four fixes carries its own regression test; the four are bisectable independently; commit grouping at land time should follow D-IH-57-C (one commit per fix), with the OPS-54-1.a + OPS-54-1.b CSS/DOM pair allowed to land as one a11y commit if their `git diff` lines overlap (they do not in this case — the CSS edit is at line 51, the DOM edit is at line 145; safe to ship as two commits).
- **No new D-IH-57-* needed** — All four fixes follow the existing `nullable_when_blank` idiom (F-22a-EMIT-1) or trivial DOM/CSS hardening (OPS-54-1.a/b); no new architectural decisions were forced.
- **F-22a-EMIT-2 fail-loud guard is a future-proof addition** — The new `BOOL_COLUMN_DEFAULTS: dict[str, str | None]` map raises `ValueError` if a future NOT-NULL bool column lacks a documented default. This trades emit-time noise for apply-time silence (the original defect was apply-time-only). Documented in the function's docstring; mitigated R-OUT-4 in the I57 risk register.

## Risks worth capturing

- **R-57-cycle1-C avoided** — Pre-existing failures (`test_validates_via_pydantic` + `test_agents_defaults_sandbox_strict`) noted in the I32 + I45 closure UATs are confirmed PASS in this 1764-test sweep. P2 + P3 verification matrix re-runs are expected to show only positive deltas (more tests passing), no regressions.
- **R-57-4 stable** — F-22a-EMIT fixes did not break any other `_emit_*_upserts` function. The 5 pre-existing test_sync_compliance_mirrors_from_csv tests still PASS unchanged.
- **OPS-54-1 axe re-run still operator-side** — These regression tests lock the **source-DOM contract** (CSS rule and `tabindex` attribute presence in the served HTML). The actual axe-core re-run that confirms 0 Critical / 0 Serious requires `pip install -r requirements-dev.txt` + `py -m playwright install chromium` + `py scripts/browser-smoke.py --playwright --axe`, which is the same operator-side step that I54 OPS-54-1 already documented. P6 closure UAT will request the operator runs this and records the new findings count.

## Next phase

P2 — Drive [I45](../../45-live-eval-harness/master-roadmap.md) to closure: rerun the verification matrix from the I45 master-roadmap; flip the master-roadmap.md `status: active → closed`; re-render WIP_DASHBOARD. The existing I45 closure UAT (2026-05-01) declares all 9 phases PASS; this work is the status flip + a confirm-and-close report.
