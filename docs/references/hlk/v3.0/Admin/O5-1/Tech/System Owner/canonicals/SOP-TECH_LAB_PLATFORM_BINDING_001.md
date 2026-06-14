---
title: SOP — Lab Platform Binding (hosting config → running app)
language: en
intellectual_kind: tech-canonical-sop
sop_id: SOP-TECH_LAB_PLATFORM_BINDING_001
access_level: 4
confidence_level: A1
source_taxonomy: holistika-internal-sop
authors:
  - System Owner
last_review: 2026-06-14
last_review_by: System Owner
last_review_decision_id: D-IH-99-A
methodology_version_at_review: v3.1
status: active
register: internal
linked_canonicals:
  - ../../../../Data/Governance/canonicals/dimensions/DATA_CONTRACT_REGISTRY.csv
  - ../../../../People/Compliance/canonicals/techops/COMPONENT_SERVICE_MATRIX.csv
  - ../../../../Data/Architecture/canonicals/dimensions/SUPABASE_AUTH_REGISTRY.csv
  - SOP-CICD_BASELINE_001.md
data_contract_id: DC-HOL-LAB-PLATFORM-ENV-001
cadence: event_triggered
cadence_trigger: new consumer repo Preview/Production env surface OR lab incident where runtime config disagrees with dashboard
---

# SOP — Lab platform binding

> **What this is:** How Holistika's **lab** (HLK Tech Lab hosting + consumer repos) turns dashboard settings into what the running app actually sees. This is the **operational companion** to data contract **`DC-HOL-LAB-PLATFORM-ENV-001`** — the contract is SSOT; this SOP is how System Owner keeps the lab honest.
>
> **Who sleeps at night:** System Owner — so operators, customers, and collaborators can trust the brand promise: *we have a lab; we translate requirements; we don't guess passwords when the gate was off.*

## 1. Single SSOT rule

| Layer | Role | Path |
|:---|:---|:---|
| **Contract (SSOT anchor)** | Cross-area binding | `DATA_CONTRACT_REGISTRY.csv` → `DC-HOL-LAB-PLATFORM-ENV-001` |
| **Component inventory** | What exists in the lab | `COMPONENT_SERVICE_MATRIX.csv` → Vercel + HLK-ERP rows (FK via `notes` / runbook pointer) |
| **Consumer bindings** | How a product uses the contract | e.g. `SUPABASE_AUTH_REGISTRY.csv` SUPA-AUTH-16 (Preview dev sign-in only) |
| **Initiative evidence** | Proof for a thread | `docs/wip/planning/<NN-…>/reports/` — **never** duplicate contract semantics |

If prose in a planning report disagrees with this SOP or the contract row, **the contract wins**. Planning reports link here; they do not re-define the lab.

## 2. Config kinds (read hosting docs before guessing)

Before changing env vars, read the **hosting platform docs** for the component row in the matrix (Vercel: Sensitive vs plain, build-time `NEXT_PUBLIC_*` vs runtime server vars).

| Kind | Example | Treat as | Vercel Sensitive? |
|:---|:---|:---|:---|
| **Secret** | Preview test password, automation bypass token | Encrypt / mask | Yes |
| **Runtime gate** | `ALLOW_PREVIEW_DEV_SIGNIN=1` | Plain on/off at runtime | **No** — Sensitive can leave runtime empty while dashboard shows a row |
| **Build flag** | `NEXT_PUBLIC_DEV_PASSWORD_AUTH=1` | Baked at deploy | **No** — requires redeploy after change |
| **Tier URL** | `NEXT_PUBLIC_APP_URL` | Per-environment host | Usually no |

**Worked example (2026-06-14):** Preview auth-probe showed `allow_preview_dev_signin: ""` while email/password were set. Root cause: **Sensitive toggle on a non-secret gate**, not wrong password. Fix: set `ALLOW_PREVIEW_DEV_SIGNIN=1`, **non-Sensitive**, redeploy, re-probe.

## 3. Investigation ladder (human + AIC)

Use this order **every time** — do not skip to credentials.

1. **Read component docs** — matrix row → platform env semantics (compulsory before first hypothesis).
2. **Probe non-secret signals** — consumer diagnostic route when present (e.g. hlk-erp `/api/dev/auth-probe`).
3. **Classify config kind** — secret vs gate vs build flag (§2).
4. **Redeploy if build-time** — then probe again.
5. **Credentials last** — only when probe shows gates healthy and `sign_in_test` still fails.
6. **Cross-area regression** — sweep area×role matrix + FK registries (methodology report template under active initiative).

Deploy-health **Failure 8** and UAT discipline reference this ladder.

## 4. HLK-ERP Preview binding (consumer reference)

Durable host + env names live here; initiative reports cite this section.

| Tier | Host |
|:---|:---|
| Production | `https://erp.holistikaresearch.com` |
| Preview (stable) | `https://preview.erp.holistikaresearch.com` |
| Preview (PR branch) | `https://hlk-erp-git-<branch>-holistika.vercel.app` |

Preview env vars (names must match code): `ALLOW_PREVIEW_DEV_SIGNIN`, `NEXT_PUBLIC_DEV_PASSWORD_AUTH`, `DEV_PREVIEW_EMAIL`, `DEV_PREVIEW_PASSWORD`, `VERCEL_AUTOMATION_BYPASS_SECRET`, Supabase URL/anon key. Production must **not** set Preview-only dev-password vars.

Auth consumer row: **SUPA-AUTH-16** in `SUPABASE_AUTH_REGISTRY.csv`. Magic link remains primary human UAT; dev-password is automation / L3.5 capture path.

## 5. Custom domain vs deployment alias

Vercel can show **Valid Configuration** while a custom host still serves an **older build** until redeploy rebinds aliases. Symptom: charter host on legacy UI while `*-git-main-*.vercel.app` serves current main. Fix: redeploy production deployment; verify POV strip + © year + `/sign-in` route.

## 6. Cross-references

- Data contract: `DC-HOL-LAB-PLATFORM-ENV-001`
- Capabilities: `CAP-LAB-PLATFORM-BINDING-GOVERNANCE`, `CAP-TECHOPS-RELIABILITY-OBSERVABILITY`, `CAP-CROSS-AREA-LAB-REGRESSION`, `CAP-AIC-MULTI-LENS-INVESTIGATION`
- CI/CD: [`SOP-CICD_BASELINE_001.md`](SOP-CICD_BASELINE_001.md) § Deployment Protection bypass
- Founder insight: [`LOGIC_CHANGE_LOG.md`](../../../../People/canonicals/LOGIC_CHANGE_LOG.md) BT-10-lab-governed-ssot
- Brand lab promise: [`BRAND_ARCHITECTURE.md`](../../../../Marketing/Brand/canonicals/BRAND_ARCHITECTURE.md) § lab-to-channel pipeline
