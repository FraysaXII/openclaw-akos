---
report_type: experiential-uat-walk
intellectual_kind: uat_evidence
parent_initiative: INIT-OPENCLAW_AKOS-96
phase: P-G6-production-uat
authored: 2026-06-16
audience: J-OP;J-AIC
verdict: PASS-WITH-FOLLOWUP
ladder_tier: L4-Production
capture_session: artifacts/uat-screenshots/i96-research-center-production-2026-06-16/
linked_charter: reports/uat-i96-research-center-production-charter-2026-06-13.md
inherit_journey_evidence: artifacts/uat-screenshots/i96-research-center-v2-b15-2026-06-13/
verdict_history:
  - verdict: FAIL
    date: 2026-06-16
    reason: BLOCKED-AUTH — magic-link rate limit + PKCE paste class; 0 signed-in journey PNGs on prod host
  - verdict: PASS-WITH-FOLLOWUP
    date: 2026-06-16
    reason: Operator ratified B1.5 L3 journey evidence (8/8) satisfies experiential bar; prod host shell PASS; signed-in prod PNGs deferred
verdict_followup_rationale:
  followup_class: deferred-work-with-tracker
  closure_target: I99 OPS-99-1 Resend SMTP live + prod signed-in re-capture
  owner: System Owner
  tracker_path: docs/wip/planning/96-research-data-plane-and-research-center/reports/uat-i96-research-center-production-charter-2026-06-13.md
  notes: >-
    Production sign-in shell and redirect code verified on erp.holistikaresearch.com.
    Operator confirms magic link works in normal browser. L4 signed-in journey PNGs
    not captured — Supabase built-in email rate limit blocks further OTP sends;
    PKCE prevents paste-to-chat automation. Journey proof inherited from B1.5 L3
    localhost dev-password (8/8 operator+director discover→audit). Carryover scheduled
    not dropped — prod PNGs after Resend custom SMTP (SUPA-AUTH-09) or cooldown window.
---

# I96 Research Center — Production L4 experiential walk (2026-06-16)

> **Functional name:** browser proof that the live Research Center works for signed-in operator and director journeys on the production host — not localhost.

## Verdict

**PASS-WITH-FOLLOWUP** — Production **host + sign-in shell PASS**; full **signed-in journey PNGs on prod host deferred** with tracker (not dropped). Operator ratified inheriting **B1.5 L3** journey evidence (`8/8` @1280, dev-password, no email) until Resend SMTP removes rate-limit pain.

## Evidence captured (production host)

| # | Check | Result |
|:---|:---|:---|
| P-01 | `erp.holistikaresearch.com` loads Holistika sign-in | **PASS** — redirects to `/sign-in?next=/research-center` |
| P-01b | Vercel production URL sign-in | **PASS** — `hlk-erp-git-main-holistika.vercel.app` same shell |
| P-02 | Magic-link sign-in → Research Center signed-in | **DEFERRED** — rate limit; no further OTP sends |
| P-03..P-06 | Full operator/director journey on prod | **INHERITED** — B1.5 L3 captures (see below) |

Screenshot: `artifacts/uat-screenshots/i96-research-center-production-2026-06-16/01-sign-in-production-host-1280.png`

## Inherited journey evidence (B1.5 L3 — operator ratified)

| Source | Tier | Auth | Journeys |
|:---|:---|:---|:---|
| [`uat-i96-research-center-b15-experiential-2026-06-13.md`](uat-i96-research-center-b15-experiential-2026-06-13.md) | L3 localhost | dev-password | Operator + Director discover → triage → drawer → audit **8/8 PASS** |
| Manifest | `artifacts/uat-screenshots/i96-research-center-v2-b15-2026-06-13/MANIFEST.json` | | sha256 verified |

Same UI stack as production `main`; prod-specific gap is **signed-in session on charter hostname only**.

## Auth notes (system, not operator)

- **Rate limit:** Supabase built-in demo SMTP — repeated magic-link attempts hit **email rate limit exceeded**. **No further magic-link sends** this session.
- **PKCE:** Paste-to-chat verify URLs fail even when redirect is correct.
- **Prod code OK:** Bundle sends `https://erp.holistikaresearch.com/auth/callback` from `window.location.origin`.
- Full RCA: [`i96-auth-redirect-root-cause-2026-06-16.md`](i96-auth-redirect-root-cause-2026-06-16.md)

## Follow-up (scheduled)

1. **I99 OPS-99-1** — Resend custom SMTP on Supabase (removes demo rate limit).
2. Re-capture operator + director journeys @1280 on `erp.holistikaresearch.com` with signed-in session (one magic link after SMTP, or Preview dev-password fix for automation).
3. Close L4 follow-up in production charter checklist P-02..P-06.

## Verification

```powershell
py scripts/validate_uat_report.py docs/wip/planning/96-research-data-plane-and-research-center/reports/uat-i96-research-center-production-2026-06-16.md
```
