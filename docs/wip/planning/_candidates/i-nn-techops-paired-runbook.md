---
candidate_id: I-NN-TECHOPS-PAIRED-RUNBOOK
title: TechOps paired runbook — scripts/techops_reliability_check.py for TECHOPS_DISCIPLINE.md status:charter → status:active flip
status: candidate
authored: 2026-05-21
last_review: 2026-05-21
parent_initiatives: [86]
related_initiatives: [68, 79, 82, 87]
priority: 3
language: en
audience: J-OP;J-AIC
access_level: 3
parent_lane: I86 Wave M Cluster B (engrave-properly mint of 4 Quality Fabric specialty canonicals)
charter_decisions:
  - D-IH-86-BU
  - D-IH-86-AZ
forward_charter_authority: D-IH-86-BU (operator override 2026-05-21: "As we sweep we clean and mint properly")
linked_canonicals:
  - docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/TECHOPS_DISCIPLINE.md
  - docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_QUALITY_FABRIC.md
  - .cursor/rules/akos-techops-discipline.mdc
  - .cursor/rules/akos-deploy-health.mdc
  - .cursor/rules/akos-executable-process-catalog.mdc
linked_ops_action_ids:
  - OPS-86-9
---

# I-NN-TECHOPS-PAIRED-RUNBOOK — paired runbook for TechOps discipline

> **Spawned by I86 Wave M Cluster B engrave-properly mint** (2026-05-21). [`TECHOPS_DISCIPLINE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/TECHOPS_DISCIPLINE.md) landed at `status:charter` with 7 system-reliability dimensions and a paired Cursor rule. This candidate names the runbook scope that flips charter → active.

## 1. Activation gates

- **A1.** Operator approves promotion from `_candidates/` to `docs/wip/planning/<NN>-techops-paired-runbook/master-roadmap.md`.
- **A2.** Vercel + Render + Sentry + Supabase MCP servers are wired into the workspace and authenticated (per `mcp_auth` per server) so the runbook has live signal sources.
- **A3.** A baseline incident playbook exists (or is minted in P0 of the promoted initiative) so the runbook has somewhere to file an incident row when TECH-07 surfaces drift.

## 2. Scope

- **Mint** [`scripts/techops_reliability_check.py`](../../../../scripts/techops_reliability_check.py) executing the 7-dimension reliability bar from `TECHOPS_DISCIPLINE.md` §2:
  - TECH-01 uptime SLO (last 30-day uptime ≥ committed SLO; consumes Vercel + Render MCP `services list` + status).
  - TECH-02 Web Vitals (LCP / INP / CLS within budget on production routes; consumes Vercel Analytics MCP).
  - TECH-03 error budget (Sentry error count vs allotted error budget for the period; consumes Sentry MCP `search-issues`).
  - TECH-04 deploy posture (every production deploy has a recorded promotion event + rollback path; consumes Vercel + Render MCP `deployments list`).
  - TECH-05 security posture (no critical open `get_advisors security` findings on Supabase; no known-CVE deps in the latest `npm audit` / `pip-audit`).
  - TECH-06 observability posture (Sentry breadcrumb coverage on every Edge Function + critical API route).
  - TECH-07 incident hygiene (every Sentry `unresolved` issue ≥ 7 days old has either an owner or an explicit ack note).
- **Mint** `akos/hlk_techops_reliability_check.py` — Pydantic SSOT model.
- **Mint** `tests/test_techops_reliability_check.py` — ≥ 14 tests under `@pytest.mark.techops` (mocked MCP responses for offline CI).
- **Wire** into `verification-profiles.json` + `release-gate.py` (advisory mode at first; promote to FAIL when 30-day baseline stable).
- **Flip** `TECHOPS_DISCIPLINE.md` `status: charter` → `status: active`.
- **Flip** `HOLISTIKA_QUALITY_FABRIC.md` §6 row for TechOps `status` column.

## 3. Effort estimate

- ~5 person-days for the runbook + Pydantic + tests + wiring (more than DataOps/MKTOps because of multi-MCP integration + mocked-MCP test strategy).
- ~1 person-day for the `status:active` flip + cross-references.
- Total: ~6 person-days. RICE-effort 1.2 person-weeks.

## 4. Cross-references

- Parent OPS: [`OPS-86-9`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/OPS_REGISTER.csv).
- Sibling candidates: `i-nn-dataops-paired-runbook.md` + `i-nn-mktops-paired-runbook.md` + `i-nn-ux-paired-sop.md`.
- Rule: [`akos-techops-discipline.mdc`](../../../../.cursor/rules/akos-techops-discipline.mdc).
- Rule: [`akos-deploy-health.mdc`](../../../../.cursor/rules/akos-deploy-health.mdc) — TECH-04 deploy posture grounding.
- Decision: [`D-IH-86-BU`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv).
