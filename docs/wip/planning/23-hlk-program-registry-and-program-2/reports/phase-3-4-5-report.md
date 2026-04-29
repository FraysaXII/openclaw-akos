# Initiative 23 — Phase 3 + 4 + 5 report

**Date:** 2026-04-29
**Phases closed:** P3 (cross-asset consistency validator), P4 (compliance mirror drift probe), P5 (cross-program glossary).
**PR:** [#14](https://github.com/FraysaXII/openclaw-akos/pull/14) — `feat(hlk,scripts,docs): Initiative 23 P3+P4+P5 - cross-asset validator, drift probe, glossary`.
**Status:** **CLOSED for P3+P4+P5.** I23 overall remains **in progress** — P6 (onboard program 2) is operator-gated; P7 (full docs sync) is partially landed and continues in the next branch; P8 (UAT + closure) follows P6.

## Deliverables shipped

| Phase | Deliverable | Path | Notes |
|:-----:|:------------|:-----|:------|
| **P3** | Cross-asset `program_id` validator | [`scripts/validate_program_id_consistency.py`](../../../../../scripts/validate_program_id_consistency.py) | Scans GOI/POI + open questions + filed instruments + `_assets/<plane>/<program_id>/` + vault `programs/<program_id>/`; integrated into [`validate_hlk.py`](../../../../../scripts/validate_hlk.py) after PROGRAM_REGISTRY validator; SKIPs gracefully when registry absent or empty |
| **P3** | Tests | [`tests/test_validate_program_id_consistency.py`](../../../../../tests/test_validate_program_id_consistency.py) | 7 tests; covers regex, reserved keywords, FK loading, repo-state PASS/SKIP |
| **P4** | Mirror drift probe | [`scripts/probe_compliance_mirror_drift.py`](../../../../../scripts/probe_compliance_mirror_drift.py) | Two modes: `--emit-sql` (operator pastes into MCP `execute_sql`); `--verify` reads `artifacts/probes/mirror-drift-<YYYYMMDD>.json` and reports PASS/FAIL row-by-row; SKIPs gracefully when no fresh artifact exists |
| **P4** | Verify profile | `compliance_mirror_drift_probe` in [`config/verification-profiles.json`](../../../../../config/verification-profiles.json) | Wraps `--verify`; CI never red on stale artifacts |
| **P4** | Operator runbook | [`artifacts/probes/README.md`](../../../../../artifacts/probes/README.md) | `--emit-sql` → paste JSON → `--verify` workflow; SOC notes; cross-references |
| **P4** | `.gitignore` rule | `artifacts/probes/*.json` excluded; `README.md` whitelisted | Operator-local pasted snapshots never enter history |
| **P4** | Tests | [`tests/test_probe_compliance_mirror_drift.py`](../../../../../tests/test_probe_compliance_mirror_drift.py) | 13 tests; covers contract coverage, SQL emission, `csv_counts`, verify PASS/FAIL/SKIP, malformed JSON, non-array payload rejection |
| **P5** | Cross-program glossary | [`docs/reference/glossary-cross-program.md`](../../../../reference/glossary-cross-program.md) | 5 vocabulary families: program codes (12), discipline codes (6), sensitivity bands (4), sharing labels (3), GOI/POI class taxonomy (15), status enums (`lifecycle_status` 5, `risk_class` 4, `default_plane` 7), voice registers (5); every entry cites canonical source |
| **P5** | Glossary cross-link | [`docs/GLOSSARY.md`](../../../../GLOSSARY.md) — added "Program", "Cross-program glossary", "Drift probe" rows | Per `akos-docs-config-sync.mdc` Human-facing index trigger |
| **P3+P4** | Defensiveness fix | `_origin_label()` helper in validator; try/except in probe `cmd_verify` | Both source scripts robust against `path.relative_to(REPO_ROOT)` failure on tmp paths (regression caught by tests) |
| **CHANGELOG** | `[Unreleased]` entry | [`CHANGELOG.md`](../../../../../CHANGELOG.md) | Single entry covering P3+P4+P5 |

## Verification results

Run on PR-#14 head before merge:

| Check | Result | Notes |
|:------|:------:|:------|
| `py scripts/validate_hlk.py` | **PASS** | org 65, processes 1091, 12 programs registered, PROGRAM_REGISTRY: PASS, PROGRAM_ID_CONSISTENCY: PASS, OVERALL: PASS |
| `py scripts/validate_hlk_vault_links.py` | **PASS** | No broken internal `.md` links |
| `py -m pytest tests/test_validate_program_id_consistency.py tests/test_probe_compliance_mirror_drift.py -v` | **PASS** | 20/20 |
| `py -m pytest` (combined: new + wave2_backfill + sync_compliance_mirrors) | **PASS** | 41/41 |
| `py scripts/wave2_backfill.py --check-only` | OK | Informational (sentinels expected; YAML still operator-pending in Sections 1/2/4/5) |

## Drift surfaced for separate operator action

The drift probe FOUND real drift on its first verify run:

| Mirror | Canonical CSV count | Live mirror count | Δ |
|:-------|:-------------------:|:-----------------:|:-:|
| `compliance.process_list_mirror` | 1091 | 1083 | **−8** |
| All other mirrors | match | match | 0 |

The 8-row delta represents `process_list.csv` rows added in earlier PRs (likely API lifecycle / ADVOPS workstreams) that have not been re-mirrored. **Remediation is out of scope for this PR**; the probe correctly surfaces it for separate operator action:

```bash
py scripts/verify.py compliance_mirror_emit
# review artifacts/sql/compliance_mirror_upsert.sql
# apply via user-supabase MCP execute_sql with service_role
py scripts/probe_compliance_mirror_drift.py --emit-sql
# re-run the probe SELECT, save fresh JSON, then:
py scripts/probe_compliance_mirror_drift.py --verify   # should now PASS
```

This is the intended operating loop: drift is detected, surfaced, and routed to the operator-SQL-gate workflow per [`akos-holistika-operations.mdc`](../../../../../.cursor/rules/akos-holistika-operations.mdc) §"Operator SQL gate".

## What's next for Initiative 23

| Phase | Status | Blocker |
|:-----:|:-------|:--------|
| **P6 — Onboard program 2 (G-23-2; conditionally G-23-3)** | **PENDING — OPERATOR GATES** | YAML `Section 4: kirbe_duality` (3 sentinels: `data_governance_lead_role`, `business_controller_role`, `has_paying_customers_today`); approval to add `process_list.csv` tranche if onboarding requires new role; the `consumes_program_ids` edge already exists in PROGRAM_REGISTRY (PRJ-HOL-KIR-2026 → PRJ-HOL-FOUNDING-2026) |
| **P7 — Full docs/rules sync** | **PARTIAL** | This PR adds CONTRIBUTING drift-probe runbook + glossary cross-links + CHANGELOG. Still pending: `docs/ARCHITECTURE.md` Operator Scripts table rows; `docs/USER_GUIDE.md` HLK Operator Model — drift probe section |
| **P8 — UAT + closure** | **BLOCKED on P6 + P7 completion** | Dated UAT report; closure note on `master-roadmap.md`; cursor-rules-hygiene checkbox |

## Cursor-rules hygiene check

No new rule patterns surfaced in P3+P4+P5 that warrant a new `.cursor/rules/*.mdc`. The trigger rows already added in PR #12 cover `wave2_backfill.py` + `operator-answers-wave2.yaml`. P3/P4/P5 fall under the existing **HLK compliance** + **Script changes** trigger families in [`akos-docs-config-sync.mdc`](../../../../../.cursor/rules/akos-docs-config-sync.mdc).

[posture: SSOT, DAMA, DI, DX, SOC, user-first SOTA]
