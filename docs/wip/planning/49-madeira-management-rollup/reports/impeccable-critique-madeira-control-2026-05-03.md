---
language: en
status: active
initiative: 49-madeira-management-rollup
report_kind: impeccable-critique
program_id: shared
plane: ops
authority: System Owner
last_review: 2026-05-03
---

# Impeccable critique — `static/madeira_control.html` (post-craft)

> **Phase 15 closure artefact.** Read by `akos/dossier/sources.py::gather_madeira_surface_signals` to compute the third light in MADEIRA dossier Section 1 (`flavor='madeira'`).

## Verdict: ship

The redesigned control plane satisfies the shape brief acceptance criteria S-1 through S-9 with the exceptions explicitly tracked under Out-of-scope follow-ups in [`impeccable-shape-madeira-control-2026-05-03.md`](impeccable-shape-madeira-control-2026-05-03.md).

## Critique table

| Criterion (shape) | Outcome | Evidence |
|:---|:---|:---|
| S-1 OKLCH tokens, no raw hex | Pass | `--brand-h`, `--surface`, `--ink`, `--accent`, `--ring` declared as CSS custom properties; only `transparent` used outside the token system |
| S-2 Visible focus rings on every action | Pass | `button:focus-visible { outline: 2px solid var(--ring); }` and matching style on `<a>` |
| S-3 `role="status"` panel + `role="alert"` on errors | Pass | Status panel toggles between roles in `renderStatusValues` and `renderError` |
| S-4 en / es / fr dictionaries; copy never hard-coded | Pass | Inline `i18n` dictionary mirrors every `data-i18n` key; locale toggle persists into `<html lang>` |
| S-5 Reduced-motion respected | Pass | `@media (prefers-reduced-motion: reduce)` removes button transitions |
| S-6 Brand voice fast-lint clean on body text | Pass | `py scripts/lint_brand_voice_offline.py static/madeira_control.html` returns 0 (file-targeted scan) |
| S-7 No external CDN | Pass | All CSS / JS inline; no `<link>` or `<script src=>` references |
| S-8 No native `<dialog>` | Pass | Status updates use a panel; clipboard feedback writes into the same status panel rather than a modal |
| S-9 `<main>` landmark | Pass | Page uses `<main>` wrapping all interactive cards |

## Accessibility highlights (axe pre-flight, manual)

- Tab order: locale buttons → Ask → Plan draft → Refresh → WebChat link → Copy JSON. Verified by source review (no `tabindex` overrides).
- ARIA pairs: `aria-pressed` on Ask/Plan/locale toggles; `aria-busy` flips on the status panel during fetch.
- Color contrast: tokens computed in OKLCH stay above WCAG AA on both light and dark schemes; manually verified `--ink` on `--surface` and `--accent-ink` on `--accent`.
- Live region: status panel is `aria-live="polite"`; switches to `role="alert"` only on error; never alters a user's focus.

## Internationalisation highlights

- Default locale picked from `?lang=` then `navigator.language`; falls back to `en`.
- Three locales declared with parity of all keys; `tests/test_madeira_control_i18n.py` enforces parity at CI time.
- `<html lang>` updated alongside `document.title` and `meta[name="description"]` when locale changes.

## Brand voice

External-prose lines on the surface ("Switch between ask and plan_draft. Mutations still go through the Orchestrator swarm.") deliberately stay short and remain inside operator-facing context (the file is internal per BRAND_JARGON_AUDIT §3 scope table). The `--filter madeira` dossier cycle treats this as Surface evidence, not external prose.

## Follow-ups (post-ship)

- Operator may wire a real Playwright + axe-core suite as part of `tests/test_madeira_control_a11y.py` once Initiative 49 closes; current tests exercise the HTML-only assertions and locale-dictionary parity.
- Dark-mode visual exploration (P15 supports it via `prefers-color-scheme` tokens but no manual switcher in UI).

## Source links

- File under review: [`static/madeira_control.html`](../../../../static/madeira_control.html)
- Shape brief: [`impeccable-shape-madeira-control-2026-05-03.md`](impeccable-shape-madeira-control-2026-05-03.md)
- Vault SOP: [SOP-MADEIRA_UX_REVIEW_001.md](../../../references/hlk/v3.0/Admin/O5-1/Tech/System%20Owner/SOP-MADEIRA_UX_REVIEW_001.md)
- Tests: `tests/test_madeira_control_a11y.py`, `tests/test_madeira_control_i18n.py`
