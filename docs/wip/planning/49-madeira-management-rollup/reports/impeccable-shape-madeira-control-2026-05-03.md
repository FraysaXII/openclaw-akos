---
language: en
status: active
initiative: 49-madeira-management-rollup
report_kind: impeccable-shape
program_id: shared
plane: ops
authority: System Owner
last_review: 2026-05-03
---

# Impeccable shape — `static/madeira_control.html`

> **Phase 14 artefact.** Operator approval gate for P15 craft redesign.
> Anchors: [SOP-MADEIRA_UX_REVIEW_001.md](../../../references/hlk/v3.0/Admin/O5-1/Tech/System%20Owner/SOP-MADEIRA_UX_REVIEW_001.md), [`master-roadmap.md`](../master-roadmap.md), Impeccable design laws (loaded from `.cursor/skills/impeccable/SKILL.md`).

## 1. Audience and job-to-be-done

Operators flipping the **Madeira interaction mode** between *ask* (compact) and *plan_draft* (standard + overlay). The single primary task on this surface is: **flip mode → confirm mode → open WebChat**. Secondary tasks: read a handoff JSON example, copy it to clipboard, refresh status.

## 2. What the page is today (audit)

| Aspect | Today | Issue |
|:---|:---|:---|
| Layout | Single column, 52rem max width, system fonts | Feels like a generated example, not an operator surface |
| Hierarchy | All sections sit at the same weight | The verb-row gets lost; the JSON example dominates |
| Status | Plain `<div class="status">` updates with `innerHTML` text | No live-region semantics, no role/aria, no contrast tier separation |
| Feedback | Blocking `alert("Copied")` | Breaks keyboard flow, Windows screen-reader Trojan |
| Accessibility | No `<main>`, no `aria-live`, no focus rings, no color-contrast verification, no language toggle | Initiative 31 set the brand-voice expectation across `en`/`es`/`fr`; this page hard-codes English |
| Color | Buttons rely on raw hex `#111` and `#fff`; status uses `#f9fafb` | No OKLCH tokens, no respect for `prefers-color-scheme`, no error palette |
| Microcopy | "Set Ask (compact)", "Set Plan draft (standard + overlay)" | Operator already knows the modes — labels should be verbs naming the *outcome* |

## 3. Brand and Impeccable laws applied

- **OKLCH palette tinted to brand hue.** Use a single `--brand-h` plus L/C scales for surface, ink, accent, and ring states.
- **Type scale ≥1.25 ratio.** Operator title h1 set above eyebrow + body; line-length capped under 75ch.
- **No side-stripe borders, no glassmorphism, no gradient text.** The control plane is functional; flashy chrome distracts.
- **Reduced motion respected.** Status transitions use opacity only when `prefers-reduced-motion: no-preference`.
- **Keyboard-first.** Tab order: Ask → Plan draft → Refresh → Copy JSON. `aria-pressed` on Ask / Plan toggle pair so the active mode is announced.
- **Live-region status.** `role="status" aria-live="polite"` on the status panel; errors use `role="alert"` only when fetch fails.
- **Locale toggle.** `data-i18n` attributes drive en / es / fr copy from a small inline JSON dictionary; query param `?lang=es` selects locale; default is the browser's `navigator.language` first segment.

## 4. Information architecture

```
[Header]
  Eyebrow:   AKOS · MADEIRA Control plane
  Title:     Madeira interaction mode
  Subtitle:  Flip the mode, confirm it on WebChat. Mutations still go through Orchestrator (Run path).
  Locale:    [EN] [ES] [FR]

[Action card]
  Mode group       <- aria-pressed pair
  [ Ask (compact) ]  [ Plan draft (standard + overlay) ]
  [Refresh status]   <- secondary

[Status panel]    <- role="status" aria-live="polite"
  Mode:                ask
  Prompt variant:      compact
  Global variant:      ...
  Plan overlay:        off
  Last applied:        2026-05-03 09:42 UTC

[Handoff card]
  Path:    config/schemas/madeira-plan-handoff.schema.json
  Pre:     pre-formatted JSON, syntax-light
  Action:  [Copy example JSON]

[Footer link]
  WebChat:  open at … (in the operator's locale)
```

## 5. Acceptance criteria for P15

| ID | Criterion | Verification |
|:---|:---|:---|
| S-1 | OKLCH palette + tokens defined as CSS custom properties; no raw hex except `transparent` | Manual diff of `static/madeira_control.html` |
| S-2 | Tab focus visible on every actionable element; keyboard Enter triggers each button | Manual + Playwright when wired (P15 acceptance) |
| S-3 | `role="status"` panel exists; `aria-live="polite"` set; errors switch to `role="alert"` | `tests/test_madeira_control_a11y.py` HTML-only assertions |
| S-4 | en / es / fr dictionaries declared inline; copy never hard-coded outside dictionary | `tests/test_madeira_control_i18n.py` parity assertions |
| S-5 | Reduced-motion respected (no transitions when user prefers reduce) | `prefers-reduced-motion` media query present |
| S-6 | Brand voice fast-lint clean on the file's text content | `py scripts/lint_brand_voice_offline.py static/madeira_control.html --quiet` |
| S-7 | No external CDN; everything inline (operator may run offline) | Source review |
| S-8 | Native `<dialog>` not used (some operators run very old browsers) | Source review |
| S-9 | `<main>` landmark wraps actionable content | HTML-only assertion |

## 6. Out-of-scope follow-ups

- WebChat shell redesign (upstream OpenClaw; tracked outside Initiative 49).
- Server-side rendering of locale (operators select on the page; server stays static).
- Dark-mode visual exploration (P15 includes `prefers-color-scheme` token branch but no theme switcher).

## 7. Approvals

> **Shape approved by:** _Operator review pending (this report is the gate; once an operator marks this line, P15 may proceed.)_
>
> Approval line should read: `Shape approved by: <operator name> on <YYYY-MM-DD>`.
>
> P15 enters PR review only after that line is filled.

## 8. References

- Vault SOP — [SOP-MADEIRA_UX_REVIEW_001.md](../../../references/hlk/v3.0/Admin/O5-1/Tech/System%20Owner/SOP-MADEIRA_UX_REVIEW_001.md)
- Cursor rule — [`akos-madeira-management.mdc`](../../../../.cursor/rules/akos-madeira-management.mdc)
- Roadmap — [`../master-roadmap.md`](../master-roadmap.md) (P14 / P15 / P16)
- Brand voice — [BRAND_JARGON_AUDIT.md](../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_JARGON_AUDIT.md), [BRAND_VOICE_FOUNDATION.md](../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_VOICE_FOUNDATION.md)
