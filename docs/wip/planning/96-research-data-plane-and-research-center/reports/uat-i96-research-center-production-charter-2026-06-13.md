---
report_type: uat-charter
intellectual_kind: uat_evidence
parent_initiative: INIT-OPENCLAW_AKOS-96
phase: P-G6-production-uat
sharing_label: internal_only
authored: 2026-06-13
audience: J-OP;J-AIC
deploy_tier: production
hostname: erp.holistikaresearch.com
badge_expected: Production
language: en
status: draft
verdict: PENDING-OPERATOR-WALK
prerequisites_charter: uat-i96-research-center-preview-charter-2026-06-13.md
linked_ladder: research-center-experiential-uat-ladder-2026-06-12.md
---

# UAT charter — Research Center Production deploy

> **Audience:** J-OP (ratify) + J-AIC (mechanical walk + manifest).
>
> **Production host:** `https://erp.holistikaresearch.com/research-center` — **not** `erp.holistika.com`.

## Deploy target

| Field | Value |
|:---|:---|
| **Tier** | Vercel Production |
| **Hostname** | `erp.holistikaresearch.com` |
| **Badge** | **Production** |
| **Branch** | `main` (or production branch per hlk-erp CI) |
| **Auth** | Magic-link (`/sign-in?next=%2Fresearch-center`) **+** dev-password only if production policy allows |

## Prerequisites (gate before walk)

- [ ] Preview UAT **PASS** or **PASS-WITH-FOLLOWUP** with followups **closed** ([`uat-i96-research-center-preview-charter-2026-06-13.md`](uat-i96-research-center-preview-charter-2026-06-13.md))
- [ ] Main merge completed; production deploy **READY** (Vercel MCP evidence)
- [ ] SUBDOMAINS reconciliation **ratified** or operator explicit waiver for domain drift (see proposal)
- [ ] IntelligenceOps population **committed** or honest empty-queue UX verified

## Thorough experiential bar (same as Preview + production-specific)

### Production-specific rows

| # | Check | PASS |
|:---|:---|:---|
| P-01 | Deploy badge reads **Production** on `erp.holistikaresearch.com` | Screenshot @ 1280 |
| P-02 | Magic-link sign-in → Research Center lands signed-in | Operator @ 1280 |
| P-03 | Auth callback allow-list includes `erp.holistikaresearch.com/auth/callback` | No redirect loop |
| P-04 | SSL / MCP walk succeeds or documented operator browser walk | Cursor MCP -107 = operator takeover |
| P-05 | Production `DATA_MODE=live` honesty — no fixture chips on T0 | Gate B |
| P-06 | Freshness strip + staleness cards reflect **live** register mirror | After P-G2 CSV |

### Full ladder checklist (inherit Preview charter)

- L3.0 agent self-verify on all PNGs
- Operator + Director discover → triage → act → audit @ 1280
- Navigate CTAs execute (not drawer-only) — VIS-B04 bar
- Drawer runbook outcome / when / command complete
- v1 accordion regression
- Impeccable v2 disposition
- Manifest ≥8 shots @1280 minimum; **≥25** for full P11 closure

## Auth matrix (binding)

| Prefix | Entry URL | Required |
|:---|:---|:---|
| `auth-magic-link` | `https://erp.holistikaresearch.com/sign-in?next=%2Fresearch-center` | Operator @ 1280 minimum |
| `auth-dev-password` | Only if production policy permits | SKIP with reason if disabled |

## Verdict line template

```yaml
verdict: PASS | PASS-WITH-FOLLOWUP | FAIL | PENDING-OPERATOR-WALK
closure_decision_source: operator_explicit | agent_inline_default | n/a
deploy_verification:
  platform: vercel
  deploy_id: dpl_<id>
  source_sha: <7-char>
  hostname: erp.holistikaresearch.com
  badge_observed: Production
ladder_tier: L4-Production
```

## Closure UAT shape (when closing I96 wave)

Mint **11-section** closure UAT per [`uat-closure-template.md`](../../_templates/uat-closure-template.md) when production walk completes wave closure — not required for interim production smoke.

## Operator L4 checklist (7 items — from ladder)

1. Lens differentiation visible
2. Plain-language headlines on T0
3. Primary CTA acts in ≤2 steps
4. Drawer runbook copy-complete
5. Freshness strip matches card severity
6. v1 accordion still expands
7. Would use page before five other tools

## Cross-references

- Master tranche P-G6: [`research-center-gap-closure-deploy-uat-tranche-2026-06-13.md`](research-center-gap-closure-deploy-uat-tranche-2026-06-13.md)
- Preview charter: [`uat-i96-research-center-preview-charter-2026-06-13.md`](uat-i96-research-center-preview-charter-2026-06-13.md)
- B1.5 localhost (does not substitute): [`uat-i96-research-center-b15-experiential-2026-06-13.md`](uat-i96-research-center-b15-experiential-2026-06-13.md)
