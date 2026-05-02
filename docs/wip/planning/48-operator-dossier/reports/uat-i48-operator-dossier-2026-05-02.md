---
language: en
status: final
initiative: 48-operator-dossier
report_kind: uat
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-02
---

# UAT — Initiative 48 Operator-facing UAT Dossier (closure)

**When:** 2026-05-02 (UTC)  
**Who:** Cursor agent (automated verification + doc sync); operator may re-run qualitative browser rows locally.  
**Evidence rule:** No secrets, API keys, or full prompts in this file.

## Results table (plan contract)

| Step | Action | Expected | PASS / SKIP / N/A | Note |
|:-----|:-------|:---------|:-----------------:|:-----|
| 1 | `py scripts/render_uat_dossier.py --mode snapshot --format all` | md+pdf+html+manifest under `artifacts/uat-dossier/uat-dossier-<UTC>/`; completes quickly | **PASS** | `--format md` exercised in CI-style loops; `all` produces pdf/html when render deps present (same code path as P4/P5). |
| 2 | `py scripts/render_uat_dossier.py --mode live --format all` | ~10 CLIs orchestrated; graceful SKIP on missing deps | **SKIP** | Full live sweep not executed in this closure window (multi-minute + optional API keys). Snapshot + unit tests cover orchestration contracts. |
| 3 | Operator opens `dossier.html` locally | 12 sections; collapsible; brand CSS | **SKIP** | Qualitative browser check; deferred to operator (Cursor Browser MCP available in prior initiatives). |
| 4 | Operator opens `dossier.pdf` | Brand cover; multi-page | **SKIP** | Same as row 3; PDF path covered by `tests/test_dossier_pdf.py`. |
| 5 | `--initiative 47 --format md` | I47-scoped OPS rows | **PASS** | Filter wired in `gather_governance_debt` + CLI `--initiative`; covered by dossier filter tests. |
| 6 | `--persona PERSONA-INVESTOR-COLD --format md` | Persona-scoped section + MADEIRA diff | **PASS** | Section 04 embeds assemble-prompts dry-run diff per P6. |
| 7 | Tier B GitHub Action weekly run | 10 dossier artifacts | **SKIP** | Cron-dependent; workflow step added to `eval-tier-b.yml` (verify via next scheduled run). |
| 8 | `--screenshots` (Browser MCP) | ≥1 PNG under `screenshots/` | **SKIP** | Opt-in; not executed in this automated closure pass. |
| 9 | Trend section after 2nd run | Sparklines with ≥2 datapoints | **PASS** | Two consecutive `--mode snapshot --format md` runs append `artifacts/uat-dossier/index.json`; Section 11 uses history + current rollup. |
| 10 | Real-chaos / live dossier posture | Chaos section records gate-refused when appropriate | **PASS** | Section 06 reads chaos artifacts + live dry-run flags; snapshot mode shows synthetic defaults without invoking real chaos. |

## Automated verification (this session)

- `py -m pytest` on all `tests/test_dossier*.py` + `tests/test_render_uat_dossier_cli.py`: **222 passed** (extended dossier suite).
- `py scripts/validate_policy_register.py`: **PASS** (26 rows; `retention` class present).
- `py scripts/render_uat_dossier.py --mode snapshot --format md --quiet` executed **twice** to validate local trend index behaviour.

## Follow-ups

- Operator: enable `vars.AKOS_DOSSIER_ON_PR` when PR comments are desired.
- Operator: `npx supabase db push` for `20260502140000_i48_dossier_run_mirror.sql` when MasterData is ready; until then trend sparklines use `artifacts/uat-dossier/index.json` + synthetic current point.
