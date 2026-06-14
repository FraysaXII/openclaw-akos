---
language: en
status: active
initiative: 99-supabase-platform-eg5-tranche
report_kind: tranche-spec
parent_initiative: INIT-OPENCLAW_AKOS-99
related_initiatives: [INIT-OPENCLAW_AKOS-96, INIT-OPENCLAW_AKOS-68, INIT-OPENCLAW_AKOS-95]
authority: System Owner + DataOps
last_review: 2026-06-13
---

# Auth email stack + identity inbox governance (I99 P2 extension)

> **Wiring:** Lives under **I99** (Supabase EG-5), not `_candidates/`. Operator ratified parallel wave with I96 Preview UAT + I68 `process_list` tranche.

## Scope split

| Workstream | Owner initiative | What |
|:---|:---|:---|
| **Supabase custom SMTP + Auth redirect policy** | **I99** P2 / P5 | Resend (or SendGrid), `SUPABASE_MODULE_REGISTRY` Auth SMTP row, redirect allow-list doctrine |
| **Cloudflare Email Routing + SUBDOMAINS** | **I68** + Tech Lab | Forward-only aliases on `holistikaresearch.com` (DNS SSOT) |
| **Workspace `admin@`** | **I14** / existing GTM ops | Corporate human mail — already provisioned |
| **OSINT many-inbox registry** | **I99** P5 + **INTELLIGENCEOPS_REGISTER** | Deferred until research engagement; not Preview blocker |

## Auth email stack (near-term)

Supabase built-in mail is demo-grade. Production path: [Supabase Auth SMTP](https://supabase.com/docs/guides/auth/auth-smtp).

| Layer | Tool | Operator asset | Action |
|:---|:---|:---|:---|
| Send auth mail | **Resend** | — | Verify domain; SPF/DKIM in Cloudflare; paste SMTP in Supabase |
| Receive / alias | **Cloudflare Email Routing** | Zone on `holistikaresearch.com` | e.g. `preview-uat@` → Gmail inbox |
| Corporate | **Google Workspace** `admin@holistikaresearch.com` | Yes | Human/system owner; optional formal `From:` for auth |
| Azure / M365 | Entra | Admin, no O365 yet | Defer; app identity ≠ mail today |

### Tranche steps (operator dashboard)

1. **Resend** — add `holistikaresearch.com`; DNS records in Cloudflare.
2. **Supabase** — Authentication → Emails → SMTP; sender `noreply@holistikaresearch.com` (or `auth@`).
3. **Cloudflare** — Email Routing: `preview-uat@holistikaresearch.com` → operator Gmail.
4. **Supabase redirects** — add preview host `/auth/callback` rows (no `*.vercel.app` wildcard per operator security posture).
5. **SUBDOMAINS_REGISTRY** — canonical row when operator approves CSV gate.

### Governance mint (I68 P5 + I99 P5 — CSV gate)

- `process_list`: `env_tech_dtp_cicd_baseline_maintenance` + auth-email maintenance (I68 pause record).
- `SUPABASE_MODULE_REGISTRY`: Auth SMTP configured + hook registry rows (I99 Option B).
- Paired runbook under `docs/guides/` or v3.0 SOP (not ad-hoc markdown).

## Identity inbox tier model (OSINT + UAT — scheduled)

| Tier | Pattern | When |
|:---|:---|:---|
| T0a | **Magic link** (Supabase OTP) | **Active** — operator Preview PASS 2026-06-13 (D-IH-99-E) |
| T0b | Dev-password Preview (`DEV_PREVIEW_*`) | **Parked** — OPS-96-8; magic link sufficient for UAT |
| T1 | Gmail plus-alias (same inbox) | Optional dedicated Preview identity |
| T2 | Cloudflare forward `@holistikaresearch.com` | After Phase B above |
| T3 | Resend transactional | Production magic links |
| T4 | Workspace corporate | Already have `admin@` |
| T5 | OSINT burners (Proton / catch-all / alias registry) | **I99 P5** or dedicated research action — requires `IDENTITY_INBOX_REGISTRY` or INTELLIGENCEOPS extension |

**Deliverables (P5):** registry CSV row schema, paired SOP, research-action pack on burner providers (trust scores per research-to-decision discipline).

## OPS forward (mint at operator CSV gate)

| OPS id (proposed) | Initiative | Summary |
|:---|:---|:---|
| OPS-99-1 | I99 | Resend + Supabase SMTP configure + smoke magic link |
| OPS-99-2 | I99 | Cloudflare Email Routing aliases for Preview UAT |
| OPS-96-8 | I96 | Dev-password sync investigation (**parked** — magic link unblocks UAT) |
| OPS-99-3 | I99 | Google Workspace OAuth provider + redirect rows (**scheduled** P5) |
| OPS-99-4 | I99 | Supabase Auth custom email templates (HTML) after Resend domain verify |

## Cross-references

- I96 Preview SSOT: [`../../96-research-data-plane-and-research-center/reports/research-center-domain-and-cicd-ssot-2026-06-13.md`](../../96-research-data-plane-and-research-center/reports/research-center-domain-and-cicd-ssot-2026-06-13.md)
- Live DB auth triggers: [`../../96-research-data-plane-and-research-center/reports/supabase-live-db-health-discovery-2026-06-13.md`](../../96-research-data-plane-and-research-center/reports/supabase-live-db-health-discovery-2026-06-13.md)
- Research pack: [`../../../intelligence/supabase-platform-features-holistika-impact-2026-06-13/`](../../../intelligence/supabase-platform-features-holistika-impact-2026-06-13/)
