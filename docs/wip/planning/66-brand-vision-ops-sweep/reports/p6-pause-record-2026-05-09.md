---
phase: P6
phase_name: Marketing-ops + sales-ops template suite
initiative: I66
date: 2026-05-09
status: complete
operator_pause: pre-P7
gate_kind: template_and_operator_panel_pause
governance: D-IH-66-M, D-IH-66-Q, D-IH-66-S, BRAND_TEMPLATE_REGISTRY.md
---

# I66 P6 closure — pause record (2026-05-09)

> P6 closes with the reusable marketing, sales, advisor, partner, ENISA, recruiter, proposal, press, onboarding, and engagement-template suite in place, plus the read-only operator projections required to inspect them.

## Summary

P6 delivered:

- `FOUNDER_BIO.md` canonical with long, medium, short, one-line, audience variants, FAQ, and anonymized track-record block.
- `BRAND_TEMPLATE_REGISTRY.md` as the Markdown SSOT for the future operator registry.
- Email signatures, six outreach sequences, proposal template, engagement playbook, press kit, and onboarding kit under `_assets/advops/shared/`.
- Six deck templates: investor, sales, advisor, partner, ENISA, recruiter.
- Twelve deck companions: one `.objections.md` and one `.counterparty-brief.md` per deck.
- Supabase read-side migration for `governance.brand_template_registry` and `governance.engagement_intelligence_view`.
- Two hlk-erp operator pages:
  - `/governance/brand-templates` (access level 4)
  - `/governance/intelligence` (access level 5)

## Mechanical Evidence

### Canonical and template files

| Area | Files |
|:---|:---|
| Founder bio | `Admin/O5-1/People/FOUNDER_BIO.md` |
| Template registry | `Admin/O5-1/Marketing/Brand/BRAND_TEMPLATE_REGISTRY.md` |
| Signatures and sequences | `_assets/advops/shared/email-signatures/EMAIL_SIGNATURES.md`, `_assets/advops/shared/sequences/SEQUENCE_TEMPLATES.md` |
| Engagement assets | `_assets/advops/shared/proposals/PROPOSAL_TEMPLATE.md`, `_assets/advops/shared/engagement/ENGAGEMENT_PLAYBOOK.md` |
| Public packs | `_assets/advops/shared/press-kit/PRESS_KIT.md`, `_assets/advops/shared/onboarding/ONBOARDING_KIT.md` |
| Deck suite | `_assets/advops/shared/decks/*.deck.md` plus `.objections.md` and `.counterparty-brief.md` companions |

### Operator projections

| Surface | Source |
|:---|:---|
| `governance.brand_template_registry` | `BRAND_TEMPLATE_REGISTRY.md` projected via Supabase view |
| `governance.engagement_intelligence_view` | `docs/wip/intelligence/_templates/` plus deck companions projected via Supabase view |
| `/governance/brand-templates` | hlk-erp server page with static fallback rows |
| `/governance/intelligence` | hlk-erp server page with static fallback rows |

## Verification

| Command | Verdict |
|:---|:---|
| `ReadLints` on new AKOS Markdown + SQL + hlk-erp TS/TSX | **PASS** |
| `py scripts/validate_brand_jargon.py` | **PASS** |
| `py scripts/validate_brand_baseline_reality_drift.py` | **PASS** |
| `py scripts/validate_hlk.py` | **PASS** |
| `files-modified.csv` shape probe | **PASS** — 184 rows, 18 columns, 0 malformed rows before final P6 report append |
| `pnpm typecheck` in hlk-erp | **PARTIAL** — new brand-ops files are clean; command still fails on pre-existing type debt outside this work |

### hlk-erp typecheck residual

The P6 hlk-erp files initially introduced tuple-inference errors in `lib/brand-ops/fetcher.ts`; those were fixed. The remaining `pnpm typecheck` failures are pre-existing and unrelated to P6:

- `app/(operator)/mission-control/audit-log/page.tsx` expects fields not present on `AuditLogRow`.
- `app/api/me/delete/route.ts` and `app/api/me/export/route.ts` expect `CurrentUser.id`.
- `components/table-of-contents.tsx`, `components/ui/input-otp.tsx`, `utils/markdown-utils.ts` have nullability/type-shape debt.
- `scripts/seed-demo.ts` references missing `dotenv` and has string/undefined issues.
- `lib/auth/server.ts` Supabase generated types treat `audit_log` insert as `never`.

## Pre-P7 Checkpoint

P7 can now implement the drift gates promised by P6:

- `validate_brand_vision_drift.py` should compare the public vision canon to rendered `/vision` source text.
- `validate_dossier_companion_drift.py` should assert every deck has the required `.objections.md` and `.counterparty-brief.md` companions and that external deck files do not carry internal-register vocabulary.
- Release gate should wire both validators with tests and deliberate drift fixtures.

## Operator Review Queue

- Confirm P6 templates are structurally sufficient before any high-stakes send.
- Confirm `/governance/intelligence` should remain access-level 5 because it points to operator-private preparation materials.
- Apply the Supabase migration before expecting live remote rows in hlk-erp; fallback rows keep the panel usable before that.
