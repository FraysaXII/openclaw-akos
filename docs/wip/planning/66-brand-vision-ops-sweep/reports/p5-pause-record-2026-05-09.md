---
phase: P5
phase_name: Public surfaces rewrite + boilerplate code
initiative: I66
date: 2026-05-09
status: complete
operator_pause: pre-P6
gate_kind: public_surface_pause
governance: D-IH-66-AD, akos-agent-checkpoint-discipline.mdc, akos-brand-baseline-reality.mdc, akos-deploy-health.mdc
---

# I66 P5 closure — pause record (2026-05-09)

> P5 closes with the public-surface rewrite in a governed state. The final operator correction was to create `/services` and `/how-we-work`, but keep both as **direct-access only** until the RevOps/marketing sweep matures the surrounding audience journeys.

## Summary

P5 now has a deploy-clean and drift-clean boilerplate surface:

- `/services` exists as the 6 service-domain x 3 delivery-mode matrix from `SERVICE_OFFERING_CATALOG.md`, but is not linked from public chrome and is marked `noindex, nofollow`.
- `/how-we-work` exists as a direct-access engagement-rhythm page, also marked `noindex, nofollow`.
- Public navigation, footer, home hero, and home CTA no longer link to `/services`.
- `/vision` exists and is i18n-backed from the public vision doctrine.
- Mobile nav and manifesto mobile overlap issues found in visual smoke testing were fixed.
- Sentry source-map upload no longer blocks preview deploys; legacy Supabase build-time initialization was lazy-loaded.

## Operator correction encoded

Decision **D-IH-66-AD** records the route posture:

- Create the pages so the implementation work exists.
- Keep them available only by exact URL.
- Do not add them to visible navigation, footer, home CTAs, or sitemap exposure.
- Mark both routes `noindex, nofollow`.
- Promote them publicly only through an explicit future RevOps/I67 operator decision.

## Mechanical evidence

### Boilerplate changes

| Path | Change |
|:---|:---|
| `app/services/page.tsx` | Replaced the older public services page with a direct-access 6 x 3 matrix rendering. Added `metadata.robots.index=false` and `follow=false`. |
| `app/how-we-work/page.tsx` | Added direct-access engagement rhythm page: Discover, Shape, Build, Transfer, Close. Added `metadata.robots.index=false` and `follow=false`. |
| `components/ui/FloatingNavbar.tsx` | Removed `Services` from primary nav. |
| `components/layout/site-footer.tsx` | Removed Services company link and Services footer column. |
| `components/home/hero-section.tsx` | Removed the public Services CTA; primary CTA now points to Tech Lab and secondary CTA to Contact. |
| `components/home/cta-section.tsx` | Removed secondary View Services CTA. |
| `i18n/messages/{en,es,fr}.json` | Added the replacement contact CTA key for the home hero. |

### AKOS changes

| Path | Change |
|:---|:---|
| `docs/wip/planning/66-brand-vision-ops-sweep/decision-log.md` | Added D-IH-66-AD. |
| `docs/wip/planning/66-brand-vision-ops-sweep/files-modified.csv` | Added P5 direct-access traceability rows. |
| `CHANGELOG.md` | Added P5 increment 10 entry. |
| `docs/wip/planning/66-brand-vision-ops-sweep/reports/p5-pause-record-2026-05-09.md` | This record. |

## Verification

| Command | Verdict |
|:---|:---|
| `ReadLints` on edited boilerplate + AKOS files | **PASS** — no IDE diagnostics. |
| `py scripts/validate_brand_jargon.py` | **PASS** — 136 files scanned across 2 consumer repos; 0 forbidden tokens. |
| `py scripts/validate_brand_voice_register.py` | **PASS** — 3 message files scanned; 0 register violations. |
| `py scripts/validate_brand_baseline_reality_drift.py` | **PASS** — dual-register contract holds. |
| `py scripts/validate_brand_canon_drift.py` | **PASS** — 13 canonicals present + contract clean. |
| `py scripts/validate_hlk.py` | **PASS** — overall pass; existing advisory warnings remain advisory. |
| `node_modules/.bin/next.cmd build` with `NEXT_TELEMETRY_DISABLED=1` | **PASS** — production build completed; `/services` and `/how-we-work` included in route table. |

### Verification notes

- The repo's `npm run build` script is POSIX-style (`NEXT_TELEMETRY_DISABLED=1 next build`) and does not run directly in Windows PowerShell. The equivalent Windows-safe command was used for local verification.
- `npm ci` needed `YOUTUBE_DL_SKIP_PYTHON_CHECK=1` because this Windows environment exposes Python as `py`, while `youtube-dl-exec` checks for a `python` command name during preinstall.
- Build output includes pre-existing routes and unrelated local untracked files in the boilerplate checkout (`app/api/contact/`, `lib/schemas/contact.ts`, `utils/supabase/service.ts`). These were not part of the P5 direct-access increment.

## Pre-P6 checkpoint

P6 starts from the following state:

- Brand canon, legal posture, service matrix, and baseline-reality matrix exist.
- Boilerplate public surfaces are deploy-clean and drift-clean.
- Direct-access service/method pages are available for operator-mediated readers but not broadly discoverable.
- P6 can now focus on templates, decks, deck companions, founder bio, press kit, onboarding kit, engagement playbook, and the two governance views/panels without needing to reopen P5 routing scope.

## Operator review queue

- Confirm the known-route-only posture for `/services` and `/how-we-work` remains correct until I67.
- Confirm P6 can proceed with operator-mediated marketing/sales assets and deck companions.
