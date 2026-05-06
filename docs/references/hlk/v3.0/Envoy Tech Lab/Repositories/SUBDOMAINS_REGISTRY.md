---
language: en
---

# Holistika subdomains (canonical registry)

**Item type:** Canonical registry (see [PRECEDENCE.md](../../../compliance/PRECEDENCE.md))
**SSOT for DNS layout + Vercel project topology:** This file
**Revision:** Operators update rows when subdomains are added, repointed, archived, or change ownership.
**Created:** 2026-05-06 (Initiative 62 P0, decision D-IH-62-P)

---

## How to use

1. Add or edit a row when Holistika **starts using** a subdomain or reserves one for future use.
2. `subdomain` is the FQDN minus the apex (e.g. `madeira` for `madeira.holistika.com`).
3. `state` is one of:
   - **active** — DNS attached, Vercel project deployed, public.
   - **reserved** — registered intent, no DNS yet, no Vercel project. Prevents accidental reuse.
   - **archived** — historical; never reuse the slug for a different purpose without a registry PR.
4. `linked_initiative` points at the AKOS-side initiative folder that authored or last updated the row.
5. `data_mode` is one of `live` / `demo` / `none` (static-only or proxy).
6. `auth` is `required` / `none`.
7. `brand_register` is `internal` / `external` per [`BRAND_JARGON_AUDIT.md`](../../Admin/O5-1/Marketing/Brand/BRAND_JARGON_AUDIT.md) §3 — controls whether the brand-jargon CI lint applies to the surface.
8. Add or update the row through a PR; the validator (`scripts/validate_subdomains_registry.py`) runs in `release-gate.py`.

**Security:** Do not paste secrets, vendor account IDs that imply privilege, or anything not safe in a public repo. Subdomain names alone are public information.

---

## Registry table

| subdomain | apex | state | data_mode | auth | brand_register | vercel_project | repo | linked_initiative | notes |
|-----------|------|-------|-----------|------|----------------|----------------|------|-------------------|-------|
| `erp` | `holistika.com` | active | live | required | internal | `hlk-erp` | `hlk-erp` | [I62](../../../../wip/planning/62-mission-control/) | Operator-facing Mission Control. Production data, full RBAC, audit log. Cross-link CTA on `/sign-in`: "see a demo at madeira.holistika.com". |
| `madeira` | `holistika.com` | active | demo | none | external | `hlk-erp-showcase` | `hlk-erp` | [I62](../../../../wip/planning/62-mission-control/) | Public demo / showcase with seeded `demo.*` data. No `SUPABASE_SERVICE_ROLE_KEY`. Optional Vercel preview-password protection. CTA banner links to `erp.holistika.com/sign-in`. Brand-jargon CI gate applies (no `AKOS`, `topic_*`, `RBAC`, etc.). |
| `status` | `holistika.com` | active | live | none | external | rewrite from `hlk-erp` | `hlk-erp` | [I62](../../../../wip/planning/62-mission-control/) | Public status page. Reads only from `erp.vw_public_health` (anonymous SELECT). Implemented as a Vercel rewrite from the operator project rather than a separate Vercel project (D-IH-62-P). Brand-jargon CI gate applies. |
| `holistika.com` | `holistika.com` | reserved | none | none | external | _(none yet)_ | _(future)_ | _(future marketing site)_ | Apex domain. Reserved for the marketing site. Until a marketing site exists, redirects 301 to `madeira.holistika.com`. |
| `api` | `holistika.com` | reserved | live | required | internal | _(none yet)_ | _(future `hlk-api`)_ | _(future)_ | Reserved for a future stable API surface (currently the FastAPI control plane lives behind individual `127.0.0.1:8000` operator deploys). When promoted, `data_mode=live`, `auth=required` (API keys via Supabase). |
| `docs` | `holistika.com` | reserved | none | none | external | _(none yet)_ | _(future)_ | _(future)_ | Reserved for a static docs deploy (Mintlify or similar) generated from `docs/USER_GUIDE.md` + `docs/SOP.md` + `docs/ARCHITECTURE.md`. Brand-jargon CI gate will apply. |
| `kirbe` | `holistika.com` | reserved | live | required | internal | _(none yet)_ | _(future `kirbe`)_ | _(future)_ | Reserved for KirBe document workflow surface. Data plane separate from `erp.holistika.com`. Brand-jargon-gated as `internal` because kirbe surfaces are operator-only. |

### Cross-links

- New subdomain proposal flow: open a PR adding a row here. The validator catches duplicate slugs, missing fields, and out-of-vocabulary values for `state` / `data_mode` / `auth` / `brand_register`. CI gate via `release-gate.py`.
- Cross-link UX between `madeira.holistika.com` and `erp.holistika.com` is built in [I62 P3.4](../../../../wip/planning/62-mission-control/master-roadmap.md) via shared layout components.
- Vercel project assignments: actual project IDs live in Vercel; only the `vercel_project` slug is canonical here (allows project ID rotation without registry churn).

---

## Drift handling rule

1. This registry wins for **intent + state**. If a subdomain is `reserved` here but DNS exists, that's a drift incident — investigate and either flip to `active` (with a corresponding initiative reference) or remove the DNS.
2. Vercel UI wins for **operational state** (current deployment, current env vars). The registry tracks the assignment; Vercel tracks the build.
3. Any change to apex DNS (`MX`, `TXT`, `NS`, etc.) is out of scope for this registry — track that separately in `docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/DNS_RECORDS.md` if it grows beyond the four CNAMEs implied by active rows.

---

## Cross-references

- [`REPOSITORIES_REGISTRY.md`](REPOSITORIES_REGISTRY.md) — sister registry for GitHub repositories. Subdomain↔repo mapping is loose: `hlk-erp` powers two subdomains (`erp` + `madeira` + `status` rewrite); KirBe is reserved for `kirbe`.
- [`FIGMA_FILES_REGISTRY.md`](FIGMA_FILES_REGISTRY.md) — sister registry for Figma files (same governance shape).
- [`BRAND_JARGON_AUDIT.md`](../../Admin/O5-1/Marketing/Brand/BRAND_JARGON_AUDIT.md) §3 — brand register definitions referenced by the `brand_register` column.
- [`PRECEDENCE.md`](../../../compliance/PRECEDENCE.md) — overall compliance ranking; this file is canonical.
- I62 master roadmap: [`docs/wip/planning/62-mission-control/master-roadmap.md`](../../../../wip/planning/62-mission-control/master-roadmap.md).
- I62 D-IH-62-P decision: [`docs/wip/planning/62-mission-control/decision-log.md`](../../../../wip/planning/62-mission-control/decision-log.md#d-ih-62-p--subdomain-layout).

---

## Validation

`py scripts/validate_subdomains_registry.py` enforces:

1. Every row has all required columns populated.
2. `state ∈ {active, reserved, archived}`.
3. `data_mode ∈ {live, demo, none}`.
4. `auth ∈ {required, none}`.
5. `brand_register ∈ {internal, external}`.
6. No duplicate `subdomain` slugs within the same `apex`.
7. `state=active` rows have a non-empty `vercel_project` and `linked_initiative` (or `linked_initiative=_(future)_` for archived/reserved).
8. `state=reserved` rows have `linked_initiative` set or marked as `_(future)_`.

The validator is wired into `scripts/release-gate.py`.
