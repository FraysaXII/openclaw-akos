---
parent_initiative: INIT-OPENCLAW_AKOS-96
report_kind: reconciliation-proposal
authored: 2026-06-13
updated: 2026-06-13
audience: J-OP;J-AIC
status: operator-ratified-intent
operator_ratification: 2026-06-13
requires_operator_gate: yes
canonical_target: docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/Repositories/SUBDOMAINS_REGISTRY.md
operator_intent: DELETE holistika.com from KB — not reconcile-in-place
---

# SUBDOMAINS registry — holistikaresearch.com-only proposal (2026-06-13)

> **Functional name:** The subdomain registry — the canonical table that records which Holistika hostnames are active, reserved, or archived, and which Vercel project serves each.

## Operator ratification (binding — 2026-06-13)

**`holistika.com` is NOT Holistika's domain** — it is owned by an unknown external party. Operator intent:

1. **DELETE** all `holistika.com` apex rows from `SUBDOMAINS_REGISTRY.md` — not archived, not reserved, not drift notes.
2. **STRIP `holistika.com` from the KB forever** via a follow-on purge tranche (checklist below).
3. **holistikaresearch.com-only** topology is the sole registry surface for Holistika product hosts.

Canonical registry edit still requires the normal CSV/markdown gate before commit (`validate_subdomains_registry.py` + `validate_hlk.py`), but the approved shape is **removal + replacement**, not in-place reconciliation.

## Is SUBDOMAINS_REGISTRY OK for I96 ratify?

**No** until canonical commit lands with holistika.com rows **removed** and holistikaresearch.com rows **active**. Operator intent is ratified; mechanical commit is pending Composer gate.

---

## Proposed registry table (holistikaresearch.com only)

Replace the entire registry table body with these rows (markdown-ready for operator approve → commit):

| subdomain | apex | state | data_mode | auth | brand_register | vercel_project | repo | linked_initiative | notes |
|-----------|------|-------|-----------|------|----------------|----------------|------|-------------------|-------|
| `erp` | `holistikaresearch.com` | active | live | required | internal | `hlk-erp` | `hlk-erp` | [I96](../../../../wip/planning/96-research-data-plane-and-research-center/) | Operator ERP production + Research Center ratify host. Auth callback: `https://erp.holistikaresearch.com/auth/callback`. |
| `showcase` | `holistikaresearch.com` | active | demo | none | external | `hlk-erp-showcase` | `hlk-erp` | [I62](../../../../wip/planning/62-mission-control/) | Public demo (`showcase.holistikaresearch.com`). CTA to `erp.holistikaresearch.com/sign-in`. |
| `kirbe` | `holistikaresearch.com` | active | live | required | internal | `kirbe` | `kirbe-platform` | [I90](../../../../wip/planning/90-routing-and-wiring/) | KiRBe API on Render. SSOT: `KIRBE_ROUTING_AND_HOSTING.md`. |
| `status` | `holistikaresearch.com` | reserved | live | none | external | rewrite from `hlk-erp` | `hlk-erp` | [I62](../../../../wip/planning/62-mission-control/) | Public status page — mint when production status host confirmed on holistikaresearch.com. |
| `api` | `holistikaresearch.com` | reserved | live | required | internal | _(none yet)_ | _(future `hlk-api`)_ | _(future)_ | Future stable API surface. |
| `docs` | `holistikaresearch.com` | reserved | none | none | external | _(none yet)_ | _(future)_ | _(future)_ | Static docs deploy from USER_GUIDE / SOP / ARCHITECTURE. |

## Rows to **DELETE** from canonical (all `holistika.com` apex)

| subdomain | apex | current state | **action** |
|-----------|------|---------------|------------|
| `erp` | `holistika.com` | active | **DELETE row** |
| `madeira` | `holistika.com` | active | **DELETE row** |
| `status` | `holistika.com` | active | **DELETE row** |
| `holistika.com` | `holistika.com` | reserved | **DELETE row** |
| `api` | `holistika.com` | reserved | **DELETE row** |
| `docs` | `holistika.com` | reserved | **DELETE row** |
| `kirbe` | `holistika.com` | reserved | **DELETE row** |

After delete: registry cross-links and I62 narrative must cite `showcase.holistikaresearch.com` + `erp.holistikaresearch.com` only.

---

## KB purge checklist (holistika.com strip tranche)

**Carryover posture:** **scheduled** for P-G1b (not dropped) — fires after SUBDOMAINS canonical delete commit; tracked in master tranche.

### Grep commands (re-run before closure)

```powershell
rg "erp\.holistika\.com" docs config tests supabase .cursor
rg "madeira\.holistika\.com" docs config tests supabase .cursor
rg "holistika\.com" docs config tests supabase .cursor
```

### Hit estimate (2026-06-13 scan — AKOS repo)

| Pattern | Scope | Files | Line matches (approx.) |
|:---|:---|:---:|:---:|
| `holistika.com` | `docs/` | **33** | **~95** |
| `holistika.com` | `tests/` | 2 | **9** |
| `holistika.com` | `supabase/migrations/` | 1 | **1** |
| `holistika.com` | `.cursor/skills/` | 1 | **1** |
| `erp.holistika.com` | `docs/` (subset) | **20** | **~35** |
| `madeira.holistika.com` | `docs/` (subset) | **12** | **~20** |
| **Combined purge scope** | docs + config + tests + supabase + .cursor | **~36 unique files** | **~105–110** |

`config/` — **0** matches (clean).  
`artifacts/` — historical UAT notes only; purge or annotate as historical evidence, not live SSOT.

### Priority remediation files (must not cite live hosts)

| Priority | Path | Why |
|:---:|:---|:---|
| P0 | `docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/Repositories/SUBDOMAINS_REGISTRY.md` | Canonical — **DELETE holistika.com rows** |
| P0 | `docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/Repositories/KIRBE_ROUTING_AND_HOSTING.md` | Routing SSOT — 7 hits |
| P0 | `docs/USER_GUIDE.md` | Operator-facing — 6 hits |
| P0 | `docs/ARCHITECTURE.md` | Architecture — 3 hits |
| P1 | `docs/wip/planning/62-mission-control/**` | I62 legacy Mission Control — 13+ hits in decision-log |
| P1 | `tests/test_validate_subdomains_registry.py` | Validator fixtures — update to holistikaresearch.com only |
| P1 | `tests/test_external_repo_automation.py` | 3 hits |
| P1 | `supabase/migrations/20260506130100_i62_p2_erp_schema_views.sql` | Comment/migration prose — forward migration note only |
| P2 | `docs/wip/planning/90-routing-and-wiring/reports/kirbe-production-routing-ops-2026-06-01.md` | 6 hits |
| P2 | `docs/wip/intelligence/brand-domain-naming-2026-05-31/brand-domain-options-and-governance-gap.md` | 7 hits — may keep as *anti-example* with explicit "not our domain" banner |
| P2 | I96 reports citing holistika.com as **negative** ("do not use") | Retain only where documenting purge; remove as live host |

### hlk-erp sibling repo (out of AKOS grep — Composer tranche)

AKOS planning references hlk-erp deploy targets; **hlk-erp repo** must be grep-purged separately:

```powershell
# Run in hlk-erp workspace
rg "holistika\.com" --glob "!node_modules/**"
rg "erp\.holistika\.com" --glob "!node_modules/**"
```

Expected surfaces: `.env.example`, auth allow-list, `deploy-target.ts`, marketing cross-links, Playwright base URLs.

### Purge acceptance criteria

- [ ] `rg holistika\.com docs config tests supabase .cursor` → **0** live-host citations (historical purge banners OK if explicitly labeled)
- [ ] SUBDOMAINS registry has **zero** `holistika.com` apex rows
- [ ] `py scripts/validate_subdomains_registry.py` PASS
- [ ] hlk-erp sibling PR purged or tracked in REPOSITORY_REGISTRY carryover

---

## Post-commit verification

1. Edit `SUBDOMAINS_REGISTRY.md` — delete holistika.com rows; insert holistikaresearch.com table above
2. `py scripts/validate_subdomains_registry.py`
3. `py scripts/validate_hlk.py`
4. Run KB purge checklist until grep clean
5. Update check-links + domain SSOT

## Cross-references

- Master tranche P-G1 / P-G1b: [`research-center-gap-closure-deploy-uat-tranche-2026-06-13.md`](research-center-gap-closure-deploy-uat-tranche-2026-06-13.md)
- Domain CI/CD SSOT: [`research-center-domain-and-cicd-ssot-2026-06-13.md`](research-center-domain-and-cicd-ssot-2026-06-13.md)
