---
report_type: impeccable-audit
parent_initiative: INIT-OPENCLAW_AKOS-96
authored: 2026-06-11
register: product
surface: /research-center
status: review
IMPECCABLE_PREFLIGHT: context=nudged product=inferred-from-page-spec baseline_reality=not_required command_reference=product.md shape=spec-only-not-operator-confirmed image_gate=skipped craft=audit-only
P7_full_bar: partial-pass-with-followup
P7_pending_items:
  - axe mechanical run (Playwright + axe-core on Python 3.12 or hlk-erp a11y.spec.ts) — MCP/CDP blocked 2026-06-12
  - Mockup/prototype preview step (Figma or Excalidraw+) per MADEIRA experiential UAT charter
kirbe_spec_disposition:
  decision: relabel-in-ui
  rationale: Panel subtitle already reads "Vault document index via existing KiRBe BFF (read-only)" — honest relabel path chosen over hybrid-search BFF proxy for v1
  spec_followup: Update research-center-page-spec §Panel 4 title/copy to match shipped UI (hybrid search deferred to I92+)
  env_followup: KIRBE_API_URL + kirbe.vw_simpledir_documents_unified required for green health badge
---

# Impeccable audit — Research Center v1 (HLK-ERP)

Product-register audit against [`research-center-page-spec-2026-06-11.md`](research-center-page-spec-2026-06-11.md). **Code audit + live browser walk (session 5, 2026-06-12)** after role-mapping fix — four panels + freshness strip captured at 375/768/1280; KiRBe spec drift **dispositioned as relabel-in-ui** (see frontmatter). axe mechanical run **SKIP** (documented in browser UAT §3.2).

## One job (spec)

*Show ledger progress, radar queue, WIP packs, and vault search in under 90s — read-only.*

## Findings

| Axis | Verdict | Detail |
|:---|:---:|:---|
| **Information architecture** | **Partial PASS** | Four panels + freshness strip match spec layout (`research-center-client.tsx`). Hero copy explains read-only contract. |
| **Visual hierarchy** | **PASS (baseline)** | shadcn cards, consistent with Mission Control / planning panels. Not yet tuned to Impeccable OKLCH tokens (I65 planning palette not applied). |
| **Cognitive load** | **PASS** | 2×2 grid on lg; strip summarizes health before panels. |
| **Empty / error states** | **PASS** | Honest warnings for missing `GH_PAT_PLANNING_READER`; KiRBe error surface. |
| **Accessibility** | **SKIP (mechanical)** | Tables use `ResponsiveTable`; axe blocked in MCP/CDP + Playwright 3.14 crash — see browser UAT §3.2 |
| **Responsive** | **PASS** | Signed-in captures `11`/`12`/`13` at 375/768/1280; panel close-ups `18`–`20` |
| **Spec fidelity — KiRBe** | **PWF (relabel)** | UI honestly relabeled "Vault document index"; spec §4 still says hybrid search — update spec, not UI |
| **Spec fidelity — RBAC** | **PASS** | Level 4 enforced server + route matrix. |
| **Brand / dual register** | **REVIEW** | Internal operator copy appropriate; no external render. |

## Anti-patterns (spec §5)

| Rejected pattern | Status |
|:---|:---:|
| Placeholder cards without data | **Fixed** — panels wired to BFF |
| Write path to canonical CSV | **PASS** — read-only |
| Duplicate I89 rollup | **PASS** |

## Required fixes before Track D PASS

1. **KiRBe panel — CLOSED (relabel path):** shipped UI subtitle = "Vault document index via existing KiRBe BFF (read-only)". **Follow-up:** sync [`research-center-page-spec-2026-06-11.md`](research-center-page-spec-2026-06-11.md) §Panel 4; configure `KIRBE_API_URL` + DB view for green health.
2. **Impeccable tokens:** optional pass aligning with I65 planning OKLCH strip (not blocking function).
3. **Browser evidence:** [`uat-i96-research-center-browser-2026-06-11.md`](uat-i96-research-center-browser-2026-06-11.md) updated session 5 — verdict **PASS-WITH-FOLLOWUP**.
4. **axe sweep:** SKIP 2026-06-12 — add `/research-center` to `hlk-erp` `a11y.spec.ts` and run on Python 3.12 workstation (Playwright 3.14 `0xC0000005` on Windows).
5. **Design preview:** mockup/prototype step (Figma or Excalidraw+) — still open per MADEIRA charter.

## Cross-references

- SOP-MADEIRA UX review pattern: `SOP-MADEIRA_UX_REVIEW_001.md`
- Deploy health craft: four-panel sibling smoke + multi-viewport
