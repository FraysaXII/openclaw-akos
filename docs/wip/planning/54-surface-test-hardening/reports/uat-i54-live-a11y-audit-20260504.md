---
language: en
status: active
initiative: 54-surface-test-hardening
report_kind: uat
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-04
related_ops: OPS-54-1
---

# OPS-54-1 — Live axe-core a11y audit (Initiative 54 P3 residual)

Closes the residual operator cycle on **OPS-54-1** that was forwarded out of the I54 dispatcher-validation closure on 2026-05-03. Real Playwright run, real axe-core, real findings. Verdict per **D-IH-54-A**: **PASS** (Critical=0; Serious=2 warn-only first cycle).

## Three-lights summary

| Light | Signal | Status | Detail |
|:------|:-------|:------:|:-------|
| **Conversational** | Surface still ships and functions normally | green | 18 / 18 PASS in `browser-smoke.py --playwright --axe`; control-plane scenarios all green; no functional regression on locale buttons or `#handoff-example` |
| **Operator (a11y)** | WCAG severity bar | green | 0 Critical, 2 Serious (`color-contrast`, `scrollable-region-focusable`); D-IH-54-A treats Serious as warn-only on the first audited cycle |
| **Surface (CI)** | `playwright_a11y_smoke` profile gate | green | Smoke exit_code=0; release-gate posture preserved (Critical-only blocks per D-IH-54-A) |

Combined verdict: **OPS-54-1 closed; ship**.

## Host environment

| Field | Value |
|:------|:------|
| Run timestamp | `20260504T193914` |
| Python interpreter | `3.14.2` (free-threading variant `python3.14t.exe`) |
| Playwright | `1.58.0` |
| axe-playwright-python | `0.1.7` (axe-core 4.11) |
| Browser engine | `msedge` |
| OS | Windows 10.0.26200 |
| FastAPI control plane | `127.0.0.1:8420` (PID 18880) |
| OpenClaw gateway | `127.0.0.1:18789` (PID 10820) |
| Helper | [`scripts/audit_a11y_live.py`](../../../../scripts/audit_a11y_live.py) — emits `findings.json` + per-surface screenshots |
| Aggregate runner | [`scripts/browser-smoke.py --playwright --axe`](../../../../scripts/browser-smoke.py) — surfaces aggregate counts in the `playwright_a11y_smoke` step |
| Artifact dir (gitignored) | `artifacts/uat/i54-live-a11y/20260504T193914/` |

A previous run on Python 3.14 free-threading without both gateways live (release-gate context, FastAPI 8420 not started) crashed Playwright workers with `STATUS_ACCESS_VIOLATION` (`exit=3221225477`). Phase A boot of both gateways resolved the crash, since the failure mode was an early `Page.goto: net::ERR_CONNECTION_REFUSED` cascading inside the worker. The Cursor IDE Browser MCP fallback contemplated by the plan was therefore not required this cycle.

## Surface coverage

| Surface | URL | Engine | Counts |
|:--------|:----|:-------|:-------|
| `axe_madeira_control` | `http://127.0.0.1:8420/madeira/control` | `msedge` | **0 C / 2 S / 0 M / 0 m** |

`AXE_IN_SCOPE_SURFACES` in [`scripts/browser-smoke.py`](../../../../scripts/browser-smoke.py) currently has only `/madeira/control` per **D-IH-54-C** (in-scope: `static/madeira_control.html` + dossier HTML output template; not deck assets). Expanding to dossier HTML is a follow-up registered as `OPS-54-1.b` below.

## Findings detail

### F-1 — `color-contrast` (Serious × 3 nodes)

| Field | Value |
|:------|:------|
| Rule ID | `color-contrast` |
| Help | [Elements must meet minimum color contrast ratio thresholds](https://dequeuniversity.com/rules/axe/4.11/color-contrast?application=axeAPI) |
| WCAG | 2.1 AA 1.4.3 |
| EN-301-549 | 9.1.4.3 |
| RGAA | 3.2.1 |
| ACT | yes |
| First target | `button[data-locale-set="es"]` |
| Total nodes affected | 3 |

The three locale switcher buttons (`data-locale-set="en|es|fr"`) ship with subtle dark-on-dark contrast. Operator can verify visually in the screenshot at `artifacts/uat/i54-live-a11y/20260504T193914/axe_madeira_control.png`. Recommendation: bump button foreground or background to clear the 4.5:1 AA threshold; alternatively, add a `:focus-visible` outline ring with sufficient contrast that satisfies the keyboard-affordance subset of this rule. **D-IH-54-A defers this fix to a future audit cycle (Serious warn-only first-run); not blocking ship.**

### F-2 — `scrollable-region-focusable` (Serious × 1 node)

| Field | Value |
|:------|:------|
| Rule ID | `scrollable-region-focusable` |
| Help | [Scrollable region must have keyboard access](https://dequeuniversity.com/rules/axe/4.11/scrollable-region-focusable?application=axeAPI) |
| WCAG | 2.1 A 2.1.1 + 2.1.3 |
| EN-301-549 | 9.2.1.1 + 9.2.1.3 |
| RGAA | 7.3.2 |
| First target | `#handoff-example` |
| Total nodes affected | 1 |

The handoff-example block scrolls but has no `tabindex` so keyboard users cannot pan its content. Smallest fix: add `tabindex="0"` to `#handoff-example`. Larger fix: convert the scrollable region into a proper landmark (`<section role="region" aria-label="…">`). **D-IH-54-A defers this fix to a future audit cycle (Serious warn-only first-run); not blocking ship.**

## Findings as follow-up backlog (D-IH-54-D defer-policy)

Per **D-IH-54-D** (defer-policy for Moderate/Minor findings; here applied analogously to first-cycle Serious warn-only per D-IH-54-A), both findings are registered as follow-ups on the I54 risk register:

- **OPS-54-1.a** `static/madeira_control.html` locale-button color-contrast (WCAG 1.4.3) — operator-fix, single-line CSS change candidate.
- **OPS-54-1.b** `static/madeira_control.html` `#handoff-example` keyboard access (WCAG 2.1.1) — operator-fix, single-line `tabindex` candidate. Plus a parallel coverage extension to dossier HTML in `AXE_IN_SCOPE_SURFACES`.

These do **not** re-open Initiative 54; they live as residual operator-side fixes on the OPS-54-1 ledger. After both ship, a clean audit re-run produces 0 Serious and the `Serious warn-only first cycle` clause in **D-IH-54-A** can elevate to a hard gate in the next cycle.

## Verification

```text
$ py scripts/browser-smoke.py --playwright --axe
  PASS: 18  |  SKIP: 0  |  FAIL: 0
  axe_madeira_control PASS — axe-core: 0 Critical / 2 Serious / 0 Moderate / 0 Minor on /madeira/control
  (Serious warn-only first cycle per D-IH-54-A)

$ py scripts/audit_a11y_live.py
  wrote artifacts/uat/i54-live-a11y/20260504T193914/findings.json
  wrote artifacts/uat/i54-live-a11y/20260504T193914/findings.md
  wrote 1 screenshot(s)
```

Both invocations completed cleanly on Python 3.14.2 free-threading once both gateways were live.

## Cross-references

- I54 master-roadmap: [docs/wip/planning/54-surface-test-hardening/master-roadmap.md](../master-roadmap.md)
- Closure UAT (dispatcher-validation): [reports/uat-i54-closure-2026-05-03.md](uat-i54-closure-2026-05-03.md)
- D-IH-54-A severity bar: [decision-log.md](../decision-log.md)
- I49 impeccable critique that surfaced the OPS line: [docs/wip/planning/49-madeira-management-rollup/reports/impeccable-critique-madeira-control-2026-05-03.md](../../49-madeira-management-rollup/reports/impeccable-critique-madeira-control-2026-05-03.md)
- Aggregate axe runner: [scripts/browser-smoke.py](../../../../scripts/browser-smoke.py)
- Detail audit helper: [scripts/audit_a11y_live.py](../../../../scripts/audit_a11y_live.py)
