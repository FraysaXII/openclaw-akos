---
title: TechOps Discipline
language: en
intellectual_kind: people-canonical
access_level: 4
audience: J-OP;J-AIC
confidence_level: A1
source_taxonomy: holistika-internal-doctrine
authors:
  - Founder/CEO
co_authors:
  - System Owner
  - PMO
last_review: 2026-06-04
last_review_by: System Owner
last_review_at: 2026-06-04
last_review_decision_id: D-IH-90-AC
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-86-BX
  - D-IH-90-AC
status: active
register: internal
linked_canonicals:
  - HOLISTIKA_QUALITY_FABRIC.md
  - UAT_DISCIPLINE.md
  - ../../../../Data/Governance/canonicals/DATAOPS_DISCIPLINE.md
  - INTER_WAVE_REGRESSION_DISCIPLINE.md
  - HOLISTIKA_ORGANISING_DOCTRINE.md
  - ../Compliance/canonicals/PRECEDENCE.md
linked_cursor_rules:
  - .cursor/rules/akos-techops-discipline.mdc
  - .cursor/rules/akos-deploy-health.mdc
  - .cursor/rules/akos-mirror-template.mdc
  - .cursor/rules/akos-quality-fabric.mdc
companion_to:
  - HOLISTIKA_QUALITY_FABRIC.md
  - ../../../../Data/Governance/canonicals/DATAOPS_DISCIPLINE.md
linked_runbooks:
  - scripts/techops_reliability_check.py
linked_sops:
  - docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/SOP-TECH_SYSTEM_RELIABILITY_001.md
forward_charters: []
---

# TechOps Discipline

> The People-area meta-doctrine that names how every Holistika system
> artefact's quality bar is derived — across uptime, Web Vitals,
> observability, deploy posture, security, and incident response.
> Minted at Wave M P5 per operator ratification 2026-05-21 (Cluster B
> rework-now, full canonical not stub). This canonical is the 9th
> specialty materialisation of
> [`HOLISTIKA_QUALITY_FABRIC.md`](HOLISTIKA_QUALITY_FABRIC.md).

## 1. Purpose

Tech operations span the **runtime substrate** that everything else
Holistika ships depends on — the AKOS dashboard, the sibling Vercel
apps (`hlk-erp`, `boilerplate`, `kirbe-platform`), the Render services,
the Supabase database + edge functions, the observability + alerting
infrastructure. When the substrate degrades, everything above it
degrades — investor decks load slowly, advisor PDFs fail to render,
ENISA evidence trails go stale.

Without an explicit discipline, technical quality drifts in three
predictable ways: (a) **uptime drift** — services degrade silently
between explicit operator checks; (b) **performance drift** — Web
Vitals creep upward without anyone watching; (c) **observability
drift** — incidents happen but no one knows because the alerting
chain breaks unnoticed.

TechOps Discipline names the quality bar that prevents these drifts.
It is owned by **System Owner** (primary) with **DevOPS** as co-owner.
It applies to every Vercel / Render / Supabase deploy, every Sentry
configuration change, every dependency upgrade, every observability
endpoint, and every incident-response runbook.

## 2. The 7 TechOps quality dimensions

| Dim | Quality property | Measurement | Drift signal |
|:---|:---|:---|:---|
| **TECH-01** Uptime SLO | 99.9% target on production endpoints with rolling 30-day window | External uptime monitor (Better Uptime / Pingdom) per service URL | Any service < SLO for the window; OR alerting fails to fire on confirmed outage |
| **TECH-02** Core Web Vitals | LCP < 2.5s, INP < 200ms, CLS < 0.1 (mobile P75) on every public route | Vercel Analytics + Lighthouse CI per route | Any threshold breach on a J-IN / J-CU / J-ENISA / J-RC public route |
| **TECH-03** Error budget tracking | Error rate within budget; Sentry issue count + severity within thresholds | Sentry MCP probe + per-project error-rate dashboard | Error rate > budget for 24h; OR new high-severity Sentry issue unacknowledged > 1h |
| **TECH-04** Deploy posture | Vercel + Render last-deploy state = success + rollback capability available | Vercel MCP `deployments_list` + Render MCP service-status probe | Failed deploy > 24h old; OR rollback target not retained per provider retention policy |
| **TECH-05** Security posture | RLS enabled on every public schema table; secrets rotated within policy; dependency audit clean | Supabase `get_advisors security` + `npm audit` / `pip-audit` per repo | RLS gap on new table; secret > rotation age; known CVE in production dependency |
| **TECH-06** Observability evidence | Log aggregation + trace + metrics covering every customer-facing request path | Sentry trace coverage + log emission audit per critical path | Critical path lacks trace; OR alerting endpoint unreachable |
| **TECH-07** Incident management | Runbook readiness per service; on-call rotation; post-mortem cadence on every Sev-1 / Sev-2 | Runbook freshness scan + on-call schedule audit + post-mortem completion tracking | Service without runbook; on-call gap; Sev-2 without post-mortem within 7 days |

These 7 dimensions are **mandatory** at every deploy + every observability
configuration change.

## 3. The compose_TECHOPS rule

```
compose_TECHOPS(audience, channel, scenario, brand, governance, *, service_tier)
  → technical_quality_bar
```

Where `service_tier` is one of: `production` / `staging` / `preview` /
`internal_dev`.

The bar derives multiplicatively from the 5 fabric axes + the 7
discipline dimensions + the tier modifier:

- **audience axis** → public routes targeting external classes
  (J-IN / J-CU / J-PT / J-ENISA / J-RC / J-CO) tighten TECH-01 +
  TECH-02 thresholds vs operator-internal routes (J-OP).
- **channel axis** → which surface emits the service (web / ERP /
  mail / broadcast); determines TECH-04 deploy-posture scope.
- **scenario axis** → which user journey is on the critical path;
  determines TECH-06 observability coverage priority.
- **brand axis** → consistency with brand-baseline-reality on any
  public-facing error message / 404 / maintenance page.
- **governance axis** → which decisions / runbooks / cursor-rules
  cover the service; per
  `akos-deploy-health.mdc` + `akos-holistika-operations.mdc`.

Production tier carries the tightest thresholds; preview tier carries
only TECH-04 (deploy success) and TECH-02 (Lighthouse smoke); internal
dev carries TECH-05 (security) only.

## 4. Cadence

This discipline fires:

1. **At every deploy** (Vercel / Render / Supabase) — TECH-04
   (deploy posture) + TECH-02 (Web Vitals smoke for the affected
   route).
2. **Continuously** for production services — TECH-01 (uptime) +
   TECH-03 (error rate) via external monitor + Sentry.
3. **Per security cycle** (monthly minimum; on-demand on CVE alert)
   — TECH-05 (security posture) via Supabase advisors + dependency
   audit.
4. **At every observability config change** — TECH-06 (coverage)
   re-audited; ensures alerting endpoint reachable.
5. **At every Sev-1 / Sev-2 incident** — TECH-07 (incident
   management) discipline fires; runbook invoked; post-mortem
   scheduled within 7-day SLO.
6. **At every wave-close** (per
   `akos-inter-wave-regression.mdc` DIM-06 + DIM-08) — TECH-04
   (deploy posture) is sampled across all sibling repos.

## 5. Integration with sister disciplines

- **`DATAOPS_DISCIPLINE.md`** — observability evidence (TECH-06)
  feeds DataOps's DATA-07 quality metrics signal; security posture
  (TECH-05) feeds DataOps's DATA-06 lineage RLS audit.
- **`UAT_DISCIPLINE.md`** — UAT's `deploy-class` row maps directly
  to TECH-04 (deploy posture); the deploy-class verdict in a UAT
  closure inherits this discipline's bar.
- **`MKTOPS_DISCIPLINE.md`** — landing-page Web Vitals (MKT-03)
  inherits TECH-02 thresholds; MKTOps consumes the bar TechOps sets.
- **`INTER_WAVE_REGRESSION_DISCIPLINE.md`** — DIM-06 (sibling-repo
  deploy posture) + DIM-08 (pre-existing release-gate fails) are
  TechOps's regression-class probes. The two disciplines compose:
  inter-wave regression FIRES the probes; TechOps DEFINES what they
  check.
- **`akos-deploy-health.mdc`** — operational governance for
  hotfix-validate-deploy workflow; TechOps inherits the per-deploy
  validation contract.

## 6. Cross-references

- Quality Fabric parent: [`HOLISTIKA_QUALITY_FABRIC.md`](HOLISTIKA_QUALITY_FABRIC.md)
  §6 row (this canonical materialises `compose_TECHOPS`).
- Sister specialty canonicals: [`UAT_DISCIPLINE.md`](UAT_DISCIPLINE.md),
  [`INTER_WAVE_REGRESSION_DISCIPLINE.md`](INTER_WAVE_REGRESSION_DISCIPLINE.md),
  [`DATAOPS_DISCIPLINE.md`](../../../../Data/Governance/canonicals/DATAOPS_DISCIPLINE.md),
  [`MKTOPS_DISCIPLINE.md`](MKTOPS_DISCIPLINE.md),
  [`UX_DISCIPLINE.md`](UX_DISCIPLINE.md).
- Paired cursor rule: [`.cursor/rules/akos-techops-discipline.mdc`](../../../../../../.cursor/rules/akos-techops-discipline.mdc).
- Deploy governance: [`.cursor/rules/akos-deploy-health.mdc`](../../../../../../.cursor/rules/akos-deploy-health.mdc),
  [`.cursor/rules/akos-mirror-template.mdc`](../../../../../../.cursor/rules/akos-mirror-template.mdc)
  (sibling-repo SSOT-from-AKOS contract).
- Observability infrastructure:
  Sentry MCP (this repo + sibling repos);
  Vercel MCP (deploy / analytics);
  Render MCP (service status);
  Supabase MCP (advisor / linter).
- External research grounding per
  `akos-applied-research-discipline.mdc` RULE 2: Google SRE Book
  (uptime SLO + error budget); Web.dev Core Web Vitals 2024
  (LCP/INP/CLS thresholds); ITIL 4 (change-management +
  incident-response patterns); NIST SP 800-53 (security posture
  baseline).
- Ratifying decision: D-IH-86-BX (Wave M P5 Cluster B sub-decision).
- Sibling decisions: D-IH-86-BU (Cluster B umbrella),
  D-IH-86-AZ (forward-charter precedent that this canonical
  fulfils), D-IH-86-AT (Vercel hotfix evidence that motivated
  deploy-class UAT axis).

@docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md
