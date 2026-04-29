# UAT — Initiative 26 (Ops hardening + persistent triggers)

**Date:** 2026-04-29
**Phases under UAT:** P0, P1, P2, P3, P4 (DEFERRED), P5.
**Run by:** Cursor Agent (composer-2-fast) on Windows 10.0.26200, Python 3.14.2, in workspace `c:\Users\Shadow\cd_shadow\openclaw-akos`.
**Authority:** [`akos-planning-traceability.mdc`](../../../../.cursor/rules/akos-planning-traceability.mdc) §"UAT evidence contract".

## Verification matrix

| # | Step | Result | Notes |
|:-:|:-----|:------:|:------|
| 1 | `py scripts/validate_hlk.py` | **PASS** | OVERALL: PASS. The SOP-HLK_GOIPOI §6.1 service_role rotation runbook lands as new prose under an existing canonical document; no schema or validator change required. |
| 2 | `py scripts/validate_hlk_vault_links.py` | **PASS** | All internal `.md` links resolve, including the 6 new cross-links from re-eval-trigger templates → I07/I22/I23 master roadmaps + decision logs + planning README. |
| 3 | `py scripts/validate_hlk_km_manifests.py` | **N/A** | No manifest changes in this initiative. |
| 4 | Operator: `npm i -g @mermaid-js/mermaid-cli@^11` + `mmdc --version` | OPERATOR-PENDING | Documented in [`CONTRIBUTING.md`](../../../../../CONTRIBUTING.md) §"`mmdc` install". Operator runs at their own pace; the install is **idempotent**, version pin makes future installs reproducible. |
| 5 | Operator: GTK3 install + `py -c "from weasyprint import HTML"` | OPERATOR-PENDING (Windows-only) | Documented in [`CONTRIBUTING.md`](../../../../../CONTRIBUTING.md) §"WeasyPrint GTK3 install". The renderer chain falls back to fpdf2 transparently if GTK3 is absent; PDF smoke profile passes either way. |
| 6 | Operator: first quarterly `service_role` rotation | DEFERRED to Q3 2026 | Procedure documented in [`SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md) §6.1. Calendar reminder pattern in place. |
| 7 | Conditional `compliance/<plane>/` physical relocation (P4) | **DEFERRED — trigger not met** | Per D-IH-26-E: I23-P6 KIR onboarding completed smoothly (no file-naming friction); no second canonical CSV joined any plane; the deprecation alias map in [`compliance/README.md`](../../../references/hlk/compliance/README.md) remains the single forward-target reference. Persistent template at [`reports/re-eval-trigger-compliance-plane-relocation.md`](re-eval-trigger-compliance-plane-relocation.md) captures the trigger conditions. |
| 8 | Persistent re-eval-trigger templates (3) created | **PASS** | [`re-eval-trigger-finops-techops-second-csv.md`](re-eval-trigger-finops-techops-second-csv.md), [`re-eval-trigger-compliance-plane-relocation.md`](re-eval-trigger-compliance-plane-relocation.md), [`re-eval-trigger-graph-mcp-tooling-promotion.md`](re-eval-trigger-graph-mcp-tooling-promotion.md). Each template carries trigger conditions, evidence schema (YAML record), force-action checklist, cursor-rule guardrails, cross-references. |
| 9 | `py scripts/release-gate.py` | **DEFERRED** | Full release gate runs in CI on the closure PR. Local pre-push runs the strict matrix (validate_hlk + vault_links + km_manifests where applicable). |

**Overall verdict: PASS for I26 phases P0+P1+P2+P3+P5.** P4 explicitly DEFERRED with persistent trigger contract.

## Phase deliverables shipped

| Phase | Deliverable | Path / location |
|:-----:|:------------|:----------------|
| **P0** | Initiative folder + 6 standard artifacts | [`docs/wip/planning/26-hlk-ops-hardening/`](.) — `master-roadmap.md` + `decision-log.md` (D-IH-26-A..E) + `asset-classification.md` + `evidence-matrix.md` + `risk-register.md` (PR-26-1..PR-26-7) + `reports/` |
| **P0** | Persistent re-eval-trigger templates (3) | `reports/re-eval-trigger-{finops-techops-second-csv,compliance-plane-relocation,graph-mcp-tooling-promotion}.md` |
| **P1** | Pinned `mmdc@^11` install runbook | [`CONTRIBUTING.md`](../../../../../CONTRIBUTING.md) §"`mmdc` install" — workstation install + Linux CI extras (`libgbm1`, `fonts-liberation`, `fonts-noto-color-emoji`, `--no-sandbox`) |
| **P2** | `service_role` quarterly rotation runbook | [`SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md) §6.1 — dashboard path + credential-store update + smoke + log-in-decision-log + rollback procedure + calendar reminder pattern |
| **P3** | WeasyPrint GTK3 Windows install runbook | [`CONTRIBUTING.md`](../../../../../CONTRIBUTING.md) §"WeasyPrint GTK3 install (Windows)" — installer link + smoke command + fallback note (fpdf2 transparently when GTK3 absent) |
| **P4** | Conditional `compliance/<plane>/` relocation | **DEFERRED** — re-eval-trigger template is the deliverable; physical move waits on trigger fire |
| **P5** | UAT + closure | This report + closure note in [`master-roadmap.md`](../master-roadmap.md) |

## Cursor-rules hygiene

No new repeatable Holistika ops pattern surfaced in I26 that warrants a new `.cursor/rules/*.mdc`. The patterns we documented (re-eval-trigger templates, pinned-dependency install runbooks, quarterly key rotation cadence) are encoded as decision-log rows + repo-level docs. Future ops-hardening cycles inherit the conventions. **Hygiene checkbox: CONFIRMED.**

## Operator follow-ups (non-blocking, scheduled)

1. **`mmdc` install** — Operator runs `npm i -g @mermaid-js/mermaid-cli@^11` + `mmdc --version`; updates [`docs/wip/planning/22a-i22-post-closure-followups/reports/post-closure-followups-20260429.md`](../../22a-i22-post-closure-followups/reports/post-closure-followups-20260429.md) §2 with the version string when installed. Closes PR-26-1 + PR-26-2.
2. **WeasyPrint GTK3** (Windows operator only) — install per CONTRIBUTING.md; smoke `py -c "from weasyprint import HTML"`. Closes PR-26-3.
3. **First quarterly `service_role` rotation** — schedule for Q3 2026 (last business day of Sep). Logs into I26 `decision-log.md` after rotation. Closes PR-26-4 first cycle.
4. **Periodic review of re-eval-trigger templates** — at every initiative closure, the cursor-rules-hygiene checkbox prompts a quick scan: any trigger fired? Closes PR-26-5 ongoing.

## Closure

Initiative 26 phases **P0 + P1 + P2 + P3 + P5 are CLOSED**. P4 is **DEFERRED** with persistent trigger contract.

The wave-2 ops-debt that drove this initiative is now **fully captured**: every deferred decision (D-IH-14, D-IH-15, D-IH-18) has a persistent template; every operator runbook (mmdc, WeasyPrint, service_role rotation) lives at the right canonical surface. The next ops-hardening cycle (whether triggered by D-IH-14/15/18 fire or by a new accumulation of small items) inherits this scaffolding.

## Cross-references

- [Initiative 26 master roadmap](../master-roadmap.md)
- [Initiative 26 decision log](../decision-log.md) (D-IH-26-A..E)
- [Initiative 26 risk register](../risk-register.md) (PR-26-1..PR-26-7)
- [Wave-2 plan §"Initiative 26"](~/.cursor/plans/hlk_scalability_wave_2_initiatives_639a02d7.plan.md)
- [I22 post-closure follow-ups](../../22a-i22-post-closure-followups/reports/post-closure-followups-20260429.md) (operator slot for mmdc install)
- [`CONTRIBUTING.md`](../../../../../CONTRIBUTING.md) §"`mmdc` install" + §"WeasyPrint GTK3 install"
- [`SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md) §6.1
