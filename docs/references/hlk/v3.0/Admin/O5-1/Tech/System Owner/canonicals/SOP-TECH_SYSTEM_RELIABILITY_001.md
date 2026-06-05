---
title: SOP — Tech System Reliability Check
language: en
intellectual_kind: tech-canonical-sop
sop_id: SOP-TECH_SYSTEM_RELIABILITY_001
access_level: 4
confidence_level: A1
source_taxonomy: holistika-internal-sop
authors:
  - System Owner
co_authors:
  - DevOPS
  - PMO
last_review: 2026-06-04
last_review_by: System Owner
last_review_decision_id: D-IH-90-AC
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-86-BX
  - D-IH-90-AC
status: active
register: internal
linked_canonicals:
  - TECHOPS_DISCIPLINE.md
  - HOLISTIKA_QUALITY_FABRIC.md
  - DATAOPS_DISCIPLINE.md
linked_runbooks:
  - scripts/techops_reliability_check.py
  - scripts/release-gate.py
linked_processes:
  - env_tech_dtp_techops_reliability_001
cadence: event_triggered
cadence_trigger: deploy OR observability-config change OR monthly security cycle
---

# SOP — Tech System Reliability Check

## Purpose

Operationalise the seven TechOps dimensions in
[`TECHOPS_DISCIPLINE.md`](TECHOPS_DISCIPLINE.md).
Every production deploy, observability configuration change, or monthly
security cycle runs the TechOps reliability bar before the deploy is
declared READY or the wave UAT verdict is filled in.

## Scope

| In scope | Out of scope |
|:---|:---|
| Vercel + Render consumer repos in REPOSITORY_REGISTRY.csv | Local-only dev servers without deploy |
| Supabase security advisors on schema change | Non-Holistika client repos |
| Sentry release-format + error budget | Third-party SaaS outside registry |
| Core Web Vitals on public routes | Internal-only J-OP routes (relaxed TECH-02) |

## Steps (AC-HUMAN)

1. **Classify service tier** — `production` / `staging` / `preview` / `internal_dev`.
2. **Run TECH-01..07** from the doctrine section 2 table for the tier's fire-set.
3. **Disposition findings** via inline-ratify (rework-now default for deploy FAIL).
4. **Record evidence** in closure UAT deploy-class section or deploy-health craft output.

## Steps (AC-AUTOMATION)

```powershell
py scripts/techops_reliability_check.py --self-test
py scripts/techops_reliability_check.py --sweep --service-tier production
```

Vendor MCP checks per `.cursor/rules/akos-deploy-health.mdc` Step 1–3 supplement
TECH-04 and TECH-02 at deploy cadence.

## Acceptance criteria

| Surface | Human | Automation |
|:---|:---|:---|
| AC-HUMAN | System Owner or DevOPS walks TECH-01..07 per tier | N/A |
| AC-AUTOMATION | N/A | `--self-test` PASS at pre_commit; `--sweep` at deploy cadence |

## Cross-references

- Cursor rule: `.cursor/rules/akos-techops-discipline.mdc`
- Deploy health: `.cursor/rules/akos-deploy-health.mdc`
- I90 P3b: OPS-86-9 chassis mint
