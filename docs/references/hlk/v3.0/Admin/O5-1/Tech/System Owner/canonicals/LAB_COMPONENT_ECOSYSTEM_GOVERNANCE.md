---
title: Lab Component Ecosystem Governance
language: en
intellectual_kind: tech-canonical
access_level: 4
audience: J-OP;J-AIC
confidence_level: A1
source_taxonomy: holistika-internal-doctrine
authors:
  - System Owner
co_authors:
  - Data Governance Office
  - DevOPS
last_review: 2026-06-14
last_review_by: System Owner
last_review_at: 2026-06-14
last_review_decision_id: D-IH-100-A
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-100-A
  - D-IH-100-C
status: active
register: internal
linked_canonicals:
  - dimensions/COMPONENT_MODULE_REGISTRY.csv
  - dimensions/VERCEL_PROJECT_SETTINGS_REGISTRY.csv
  - dimensions/CLOUDFLARE_ZONE_SURFACE_REGISTRY.csv
  - dimensions/GITHUB_REPO_CI_POSTURE_REGISTRY.csv
  - SOP-TECH_LAB_PLATFORM_BINDING_001.md
  - SOP-LAB_COMPONENT_REGISTRY_MAINTENANCE_001.md
  - SOP-HLK_COMPONENT_SERVICE_MATRIX_MAINTENANCE_001.md
  - SOP-CICD_BASELINE_001.md
  - ../../Data/Governance/canonicals/dimensions/DATA_CONTRACT_REGISTRY.csv
  - ../../Data/Architecture/canonicals/SUPABASE_ECOSYSTEM_GOVERNANCE.md
inherited_pattern_id: pattern_register_csv_pydantic_validator_mirror
companion_to:
  - SOP-TECH_LAB_PLATFORM_BINDING_001.md
---

# Lab Component Ecosystem Governance

> **The System Owner governs the *whole* lab component ecosystem, not just env vars.** Operator mandate
> (2026-06-14, `D-IH-100-A`): extend the Supabase EG pattern — umbrella doctrine + module registry +
> dimension registries + maintenance SOP — across all 110 `COMPONENT_SERVICE_MATRIX.csv` rows, starting
> with the lab critical path (Vercel → Cloudflare → GitHub) that unblocks I96 Preview UAT.

## 1. Why this exists

BT-10 minted the **semantics** layer (`DC-HOL-LAB-PLATFORM-ENV-001`, `SOP-TECH_LAB_PLATFORM_BINDING_001`).
I99 closed Supabase EG-5. What remained ungoverned: **Vercel dashboard settings**, **Cloudflare edge/DNS**,
**GitHub as-built CI posture**, and a **repeatable method** for vendor documentation that changes weekly.
Initiative prose and dashboard screenshots are evidence — not SSOT.

## 2. SSOT — the module registry

`dimensions/COMPONENT_MODULE_REGISTRY.csv` is the **single classification** of every matrix `component_id`
into governance depth **D0–D3**, with `governed_status`, `module_family`, optional `dimension_registry_path`,
and Research Radar fields (`volatility_class`, `next_verify_by`).

Validated by `scripts/validate_component_module_registry.py` (wired into `validate_hlk.py`).

**Baseline (2026-06-14): 110 modules — 6 D3 · 7 D2 · 15 D1 · 82 D0** (includes alias rows).

| Family | Doctrine owner | Dimension registry |
|:---|:---|:---|
| `supabase` | Data Architect (`SUPABASE_ECOSYSTEM_GOVERNANCE.md`) | `SUPABASE_MODULE_REGISTRY.csv` |
| `vercel` | System Owner (this doc §3) | `VERCEL_PROJECT_SETTINGS_REGISTRY.csv` |
| `cloudflare` | System Owner | `CLOUDFLARE_ZONE_SURFACE_REGISTRY.csv` |
| `github` | System Owner | `GITHUB_REPO_CI_POSTURE_REGISTRY.csv` |
| Wave-2 | System Owner | `*_POSTURE_REGISTRY.csv` per vendor |

## 3. Closure plan (phased waves)

| Wave | Scope | Closes |
|:---|:---|:---|
| **Wave-0 (BT-10 + I99)** | Lab env contract + Supabase EG | DC-HOL-LAB-PLATFORM-ENV-001; Supabase module registry |
| **Wave-1 (I100 P2)** | Vercel / Cloudflare / GitHub dimension registries | Preview alias, Node parity, deployment-check semantics, DNS/SPF |
| **Wave-2 (I100 P6)** | Sentry, Langfuse, Stripe, Make, N8n, Render scaffold | D2 integrations with active consumers |
| **Wave-3 (scheduled)** | Long-tail D1/D0 promotion | Carryover index CO-100-001 |

## 4. Component Documentation Trace

Method for dissecting vendor docs (paired research-action pack under
`docs/wip/intelligence/lab-component-ecosystem-governance-2026-06-14/`):

1. **Identify governable surfaces** from vendor docs (Build, Deploy, Security, DNS — not marketing pages).
2. **Classify each surface** as secret / gate / build flag per `SOP-TECH_LAB_PLATFORM_BINDING_001` §2.
3. **Record doc anchor**: URL + section + `doc_snapshot_date` + MCP tool if available.
4. **Define probe**: CLI, MCP read, or HTTP diagnostic (e.g. `/api/dev/auth-probe`).
5. **Set volatility**: `high` (Vercel/Cloudflare/GitHub), `medium`, `low` — drives `next_verify_by`.
6. **Synthesize to registry row** — initiative prose is evidence only.

External grounding: Vercel [Shared Responsibility Model](https://vercel.com/docs/security/shared-responsibility);
Cloudflare [DNS](https://developers.cloudflare.com/dns/manage-dns-records/);
GitHub [deployment protection](https://docs.github.com/en/actions/deployment/about-deployments/deploying-with-github-actions).

## 5. Drift prevention

1. **CI gate:** `validate_component_module_registry.py` + `validate_lab_platform_registries.py` in `validate_hlk.py`.
2. **Reconcile cadence:** `SOP-LAB_COMPONENT_REGISTRY_MAINTENANCE_001` + `scripts/lab_platform_registry_reconcile.py`.
3. **Inventory vs ecosystem split:** matrix maintenance (`SOP-HLK_COMPONENT_SERVICE_MATRIX_MAINTENANCE_001`) adds rows;
   this doctrine governs **depth promotion** (D0→D3).
4. **Deployment check semantics:** Vercel Deployment Check (`CI (hlk-erp)`) gates **Production** only — Preview deploys
   proceed without it; documented in `VERCEL_PROJECT_SETTINGS_REGISTRY.csv` row `VER-SET-003`.
5. **Stable alias:** `preview.erp.holistikaresearch.com` must track latest Preview deployment — probe + reconcile doc in
   `VERCEL_PROJECT_SETTINGS_REGISTRY.csv` row `VER-SET-005` and Cloudflare row `CF-SURF-001`.

## 6. Ownership

System Owner owns this doctrine and Wave-1/2 registries; Data Architect owns Supabase family (referenced, not duplicated);
DevOPS executes probes and reconcile; PMO tracks carryover rows. **Matrix inventory** remains Compliance/TechOps plane;
**ecosystem depth** is Tech/System Owner plane.

## 7. Cross-references

- Lab binding: `SOP-TECH_LAB_PLATFORM_BINDING_001.md` · contract `DC-HOL-LAB-PLATFORM-ENV-001`
- CI required bar: `SOP-CICD_BASELINE_001.md` (as-built → `GITHUB_REPO_CI_POSTURE_REGISTRY.csv`)
- Initiative: `docs/wip/planning/100-lab-component-ecosystem-governance/`
- I96 consumer: Preview UAT probe ladder (P5 integration report)
