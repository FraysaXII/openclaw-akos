---
authored: 2026-06-16
revised: 2026-06-16
parent_initiative: INIT-OPENCLAW_AKOS-76
phase: alpha-1-prep
status: forward_charter
linked_closure: docs/wip/planning/76-madeira-elevation/reports/uat-i76-v32-alpha0-closure-2026-06-16.md
linked_research: docs/wip/intelligence/madeira-brand-capability-harmonization-v32-alpha-2026-06-14/research-synthesis-alpha1-next-spine-2026-06-16.md
---

# I76 v3.2 — α1 design-partner readiness (forward charter)

> **Functional name:** what must be true before you invite **5–10 external design partners** into MADEIRA closed alpha — the next program gate after internal α0.

## α0 closed (2026-06-16)

| Check | Result |
|:---|:---|
| Closure UAT | **PASS** — `uat-i76-v32-alpha0-closure-2026-06-16.md` |
| Dossier three-lights | **GO** — `artifacts/uat-dossier/uat-dossier-20260615T015632Z/` |
| Adversarial eval | **15/15 PASS** (CO-MBH-009 satisfied) |
| LangGraph spike | **PASS** — CI run 27520939620 (CO-MBH-011 satisfied) |
| Commits | `f9360233` α0 · `dbb23ae5` spike recovery · `0423c824` spike re-close |

## α1 entry criteria (draft — ratify at gate)

| # | Criterion | Status | Proof class | Notes |
|:---|:---|:---|:---|:---|
| 1 | Internal α0 PASS | **Done** | Closure UAT + dossier GO | |
| 2 | Scenario A + B experiential PASS or PWF with closed followups | **Partial** | L3 PNGs PASS; L4 PWF | CO-MBH-010 prod signed-in PNGs after Resend |
| 3 | Cohort list + NDA posture documented | **Not started** | Cohort intake doc + Legal MOU/NDA | EXT-041/042 research |
| 4 | Finops attribution per cohort tag in Langfuse | **Partial** | T2 fields landed; cohort wiring spec TBD | |
| 5 | Support channel + feedback loop defined | **Not started** | Written support spec (Slack/email cadence) | EXT-041 weekly sync norm |
| 6 | `D-IH-76-ALPHA0` in DECISION_REGISTER.csv | **Done** | CSV row + validate_hlk | Minted 2026-06-16 |

## Critical path (research-ranked — not optional fluff)

```text
I99 Resend SMTP (OPS-99-1)  →  α1 prep pack  →  α1 OPEN ratify gate
```

(`D-IH-76-ALPHA0` CSV — **done** 2026-06-16.)

LangGraph **pilot** mint is **not** on this path — requires PostgresSaver proof first (EXT-043/044).

## Scheduled before α1 open (not dropped)

| ID | Item | Owner | Blocker for α1? |
|:---|:---|:---|:---:|
| CO-MBH-010 | I96 L4 prod signed-in PNGs | PMO / I99 | **Soft** — L3 covers journeys; L4 closes PWF |
| OPS-99-1 | Resend + Supabase custom SMTP | I99 / System Owner | **Hard** for prod auth evidence |
| CO-MBH-008 | Multi-tenant voice spec | System Owner | No (post-α2) |

## Parallel lanes (no α1 blocker)

| Lane | Posture |
|:---|:---|
| LangGraph PostgresSaver CI | **Scheduled** — required before substrate pilot mint |
| I97 join forward | Prep only — separate CSV gates |
| Python 3.13 shadow box | Local dev parity — CI already green |

## Operator ratify gate (when ready)

Opening α1 means: **external humans** use MADEIRA + Research Center under v3.2 rules, with finops attribution and support expectations. This is a **different gate** from α0 PASS.

Research backing: [`research-synthesis-alpha1-next-spine-2026-06-16.md`](../../intelligence/madeira-brand-capability-harmonization-v32-alpha-2026-06-14/research-synthesis-alpha1-next-spine-2026-06-16.md)

Cross-ref: [`v32-closed-alpha-program-annex-2026-06-14.md`](v32-closed-alpha-program-annex-2026-06-14.md) § Alpha phases.
