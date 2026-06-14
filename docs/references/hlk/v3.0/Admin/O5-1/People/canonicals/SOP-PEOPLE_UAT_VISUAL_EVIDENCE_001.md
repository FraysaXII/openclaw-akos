---
title: SOP — People — UAT visual evidence (L3/L3.5 browser walks)
language: en
intellectual_kind: people-canonical-sop
sop_id: SOP-PEOPLE_UAT_VISUAL_EVIDENCE_001
access_level: 4
audience: J-OP;J-AIC
confidence_level: A1
source_taxonomy: holistika-internal-sop
authors:
  - PMO
co_authors:
  - System Owner
last_review: 2026-06-14
last_review_by: PMO
last_review_at: 2026-06-14
last_review_decision_id: D-IH-96-K
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-96-K
status: active
register: internal
parent_canonical: UAT_DISCIPLINE.md
companion_to:
  - SOP-PEOPLE_UAT_GOVERNANCE_001.md
  - UAT_DISCIPLINE.md
linked_canonicals:
  - UAT_DISCIPLINE.md
  - HOLISTIKA_QUALITY_FABRIC.md
linked_runbooks:
  - scripts/validate_uat_screenshot_evidence.py
linked_skills:
  - .cursor/skills/uat-discipline-craft/SKILL.md
linked_cursor_rules:
  - .cursor/rules/akos-uat-discipline.mdc
  - .cursor/rules/akos-planning-traceability.mdc
ssot: true
---

# SOP — People — UAT visual evidence (L3/L3.5 browser walks)

> **Functional name:** the rule that *capture is not review* — an agent must **read every journey screenshot** before a UAT verdict may cite browser evidence.
>
> Paired with [`SOP-PEOPLE_UAT_GOVERNANCE_001.md`](SOP-PEOPLE_UAT_GOVERNANCE_001.md) (closure-UAT document shape) and [`UAT_DISCIPLINE.md`](UAT_DISCIPLINE.md) §8.6 (experiential ladder). Paired runbook: [`scripts/validate_uat_screenshot_evidence.py`](../../../../../../scripts/validate_uat_screenshot_evidence.py).
>
> **Worked example / incident:** I96 Preview L3.5 UAT (2026-06-14) — subagent marked 8/8 VALID without reading PNGs; director captures were sidebar crops with duplicate sha256. Minted under **D-IH-96-K** after operator ratification.

## Purpose

Prevent PASS verdicts backed by favicon crops, duplicate frames, or manifest fiction on **L3 / L3.5 experiential walks** (localhost, Vercel Preview, production smoke) where `artifacts/uat-screenshots/<session>/` PNGs feed a `uat-*.md` verdict.

## Scope

- **In scope:** Any experiential UAT session with ≥8 journey PNGs @1280 (Operator + Director × discover/triage/drawer/audit) per initiative ladder or charter.
- **Out of scope:** Closure-UAT 11-section document validation (see `SOP-PEOPLE_UAT_GOVERNANCE_001` + `validate_uat_report.py`).
- **Owner area:** People / PMO (UAT governance). **Co-owner:** Tech Lab (browser capture tooling).

## AC-HUMAN (AIC execution seat)

1. **Capture hygiene:** viewport 1280×800; **collapse sidebar** before each shot; wait for page hero (not loader).
2. **Journey walk:** Discover → Triage → Act (drawer open) → Audit (accordion expanded; scroll audit into view).
3. **Visual review (non-delegable):** parent agent **Read** every canonical journey PNG; write `agent_visual_review.json` with `delegation_allowed: false`.
4. **Mechanical gate:** `py scripts/validate_uat_screenshot_evidence.py --session-dir …` exit 0 **before** UAT verdict line.
5. **Supersession:** retain v1 PNGs; mark SUPERSEDED in visual review when re-capturing.

**Forbidden:** Subagent-only visual sign-off; verdict citing PNGs the parent agent did not read.

## AC-AUTOMATION

- `py scripts/validate_uat_screenshot_evidence.py --self-test` exit 0.
- Session dir must contain `agent_visual_review.json` with VALID row per canonical journey file.
- Duplicate sha256 across journey stages → FAIL (`UAT-SS-01-DUP-HASH`).

## Cross-references

- Doctrine: [`UAT_DISCIPLINE.md`](UAT_DISCIPLINE.md) §8.6
- Sister SOP: [`SOP-PEOPLE_UAT_GOVERNANCE_001.md`](SOP-PEOPLE_UAT_GOVERNANCE_001.md)
- I96 worked example: [`docs/wip/planning/96-research-data-plane-and-research-center/reports/uat-i96-research-center-preview-2026-06-13.md`](../../../../../wip/planning/96-research-data-plane-and-research-center/reports/uat-i96-research-center-preview-2026-06-13.md)
