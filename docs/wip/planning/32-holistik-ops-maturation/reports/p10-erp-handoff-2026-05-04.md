---
language: en
status: closed
initiative: 32-holistik-ops-maturation
report_kind: phase-report
phase: P10
program_id: shared
plane: ops
authority: System Owner
last_review: 2026-05-04
---

# I32 P10 — ERP deep handoff + architecture audit + bilingual cover-emails (2026-05-04)

> **Status retrospective.** P10 deliverables shipped 2026-04-30 alongside the broader I32 closure UAT; this report formalises the per-phase artefact inventory under the I57 P3 closeout. Work itself is unchanged from the 2026-04-30 UAT row "ERP deep handoff (COMPLETED)".

## Outcome

`hlk-erp` team received a complete, dated handoff bundle covering the AKOS ↔ ERP integration contract: 6 artefacts in [`erp-handoff-bundle-2026-04-30/`](erp-handoff-bundle-2026-04-30/), one architecture audit memo with 6 deltas + the Q10 supersession recommendation, and one PR patch + bilingual cover-emails (EN + ES) staged for operator forwarding. The ERP team's local `data-ssot.mdc` cursor rule contradicting AKOS PRECEDENCE.md is the headline finding (E13 → Q10).

## Deliverables

| Artefact | Path | Purpose |
|:---------|:-----|:--------|
| ERP handoff bundle README | [`erp-handoff-bundle-2026-04-30/00-README.md`](erp-handoff-bundle-2026-04-30/00-README.md) | Index of the 6-artefact bundle |
| Mirror schema map | [`erp-handoff-bundle-2026-04-30/01-mirror-schema-map.md`](erp-handoff-bundle-2026-04-30/01-mirror-schema-map.md) | All 16 AKOS mirrors enumerated for ERP read-side consumption (RLS read-only) |
| 5-axis integration spec | [`erp-handoff-bundle-2026-04-30/02-five-axis-integration-spec.md`](erp-handoff-bundle-2026-04-30/02-five-axis-integration-spec.md) | How ERP-side data flows project onto Persona / Channel / Sourcing / Skill / Touchpoint-kit cell axes |
| Operator SQL gate pointer | [`erp-handoff-bundle-2026-04-30/03-operator-sql-gate-pointer.md`](erp-handoff-bundle-2026-04-30/03-operator-sql-gate-pointer.md) | Cross-reference to AKOS operator SQL gate; ERP must not push back to AKOS authoring surfaces |
| Localisation policy pointer | [`erp-handoff-bundle-2026-04-30/04-localisation-policy-pointer.md`](erp-handoff-bundle-2026-04-30/04-localisation-policy-pointer.md) | Bilingual rendering must follow `SOP-HLK_LOCALISATION_001.md` |
| CHANGELOG snippet | [`erp-handoff-bundle-2026-04-30/05-changelog-snippet.md`](erp-handoff-bundle-2026-04-30/05-changelog-snippet.md) | Drop-in entry for the ERP team's CHANGELOG when they merge the contract |
| Team SOTA pointer | [`erp-handoff-bundle-2026-04-30/06-team-sota-pointer.md`](erp-handoff-bundle-2026-04-30/06-team-sota-pointer.md) | Where to find the canonical AKOS state-of-the-art docs |
| ERP architecture audit | [`erp-architecture-audit-2026-04-30.md`](erp-architecture-audit-2026-04-30.md) | 6 deltas vs current AKOS doctrine + Q10 supersession recommendation (the local `data-ssot.mdc` cursor rule that contradicts PRECEDENCE.md) |
| ERP PR patch + bilingual cover-emails | (see UAT report; staged for operator forwarding) | Light-touch PR adds `EXTERNAL_REPO_CONTRACT.md` + `akos-mirror.mdc` to the `hlk-erp` repo's `.cursor/rules/` directory; cover-emails EN+ES |

## Acceptance criteria (from I32 master-roadmap)

| Criterion | Status | Evidence |
|:----------|:------:|:---------|
| ERP team acknowledges the handoff bundle and the architecture audit | OPERATOR-PENDING | Per the I32 closure UAT operator follow-up queue (2026-04-30); reply expected on the GitHub PR thread or email after operator forwards |
| Bundle complete (6 artefacts) | PASS | All 6 files present under [`erp-handoff-bundle-2026-04-30/`](erp-handoff-bundle-2026-04-30/) |
| Jargon audit passes (no internal codenames in external prose per `BRAND_JARGON_AUDIT.md`) | PASS | Confirmed via the 2026-04-30 cover-email review |

## Decisions captured (from I32 closure UAT context)

- **D-IH-32-K — Cross-repo contract.** Both `hlk-erp` and `kirbe-platform` receive `EXTERNAL_REPO_CONTRACT.md` + `akos-mirror.mdc` as the canonical cross-repo discipline seed. Boilerplate is reference-only (D-IH-32-N).
- **D-IH-32-P — Bilingual cover-emails.** Every external-repo handoff ships EN + ES cover-email pairs per `SOP-HLK_LOCALISATION_001.md`.
- **D-IH-32-K extension** — The Q10 supersession recommendation in this audit memo is the operator-side decision: ERP team's local `data-ssot.mdc` should be retired in favour of `akos-mirror.mdc`.

## Cross-references

- I32 closure UAT [`reports/uat-i32-holistik-ops-maturation-2026-04-30.md`](uat-i32-holistik-ops-maturation-2026-04-30.md) "ERP deep handoff (COMPLETED)" section.
- KiRBe equivalent: [`p9-kirbe-handoff`](kirbe-handoff-memo-2026-04-30.md) + [`kirbe-architecture-audit-2026-04-30.md`](kirbe-architecture-audit-2026-04-30.md).
- I57 P3 closeout: [`docs/wip/planning/57-cycle-closeout-live-validation/reports/p3-i32-closure-2026-05-04.md`](../../57-cycle-closeout-live-validation/reports/p3-i32-closure-2026-05-04.md).
