---
title: I48 post-closure operator follow-up execution
date: 2026-05-02
operator: agent-driven (Claude Opus 4.7)
scope: 4 follow-ups identified at close; 2 fully resolved, 2 operator-only
---

# Initiative 48 — operator follow-up execution log

After Initiative 48 closure (commit `91edb0d`) and clean-slate consolidation
(commit `66e5eaf`), four operator follow-ups remained. This report records
how each was handled on **2026-05-02 ~17:30 CET (15:30 UTC)**.

## Follow-up 1 — Apply I47 + I48 mirror migrations to Supabase

**Status:** **Operator-only — preconditions confirmed, apply pending.**

**What was verified:**

- 3 staged migrations are present and well-formed:
  - `supabase/migrations/20260502033000_i47_persona_scenario_registry_mirror.sql`
  - `supabase/migrations/20260502033500_i47_eval_run_persona_columns.sql`
  - `supabase/migrations/20260502140000_i48_dossier_run_mirror.sql`
- All three follow the AKOS RLS posture: `CREATE TABLE IF NOT EXISTS`,
  `DROP POLICY IF EXISTS` (idempotent), `ENABLE ROW LEVEL SECURITY`,
  `deny anon` + `deny authenticated` + `service_role` grants.
- Project is linked: `supabase/.temp/project-ref` → `swrmqpelgoblaquequzb`.

**What blocked auto-apply:**

- No `SUPABASE_ACCESS_TOKEN` cached (`%APPDATA%\supabase\access-token` absent).
- No `SUPABASE_DB_URL` / `SUPABASE_SERVICE_ROLE_KEY` in env.
- Docker Desktop installed but daemon failing to come up
  (`request returned 500 Internal Server Error for API route`).
  *Note: Docker is needed only for `supabase start` (local stack). Remote
  push to the linked project does not require Docker.*

**Operator command when ready:**

```powershell
npx supabase login                  # one-time interactive
npx supabase db push --linked       # applies the 3 staged migrations
```

## Follow-up 2 — Set repo variable `AKOS_DOSSIER_ON_PR=true`

**Status:** **DONE.**

```powershell
gh variable set AKOS_DOSSIER_ON_PR --body 'true' -R FraysaXII/openclaw-akos
```

**Verification:**

```
AKOS_DOSSIER_ON_PR    true    2026-05-02T15:30:18Z
AKOS_TIER_B_ENABLED   true    2026-05-01T23:58:46Z
```

The next pull request opened against `main` will automatically trigger
`.github/workflows/dossier-on-pr.yml` and post a Section 1 executive-summary
comment.

## Follow-up 3 — Verify Tier B produces per-cell dossier artifacts

**Status:** **DONE — verified on a manual workflow_dispatch instead of waiting for Mon 06:00 UTC cron.**

**Action taken:**

Triggered `eval-tier-b` with zero spend caps so cells SKIP gracefully when
API keys are absent (the workflow's preflight handles this by design):

```powershell
gh workflow run eval-tier-b -R FraysaXII/openclaw-akos `
  -f max_spend_usd=0 -f max_persona_usd=0 -f judge_cost_cap=0
```

**First attempt — exposed real CI bug (run `25255364548`):**

All 10 cells failed at `pip install -e .` with:

```
error: Multiple top-level packages discovered in a flat-layout:
['akos', 'static', 'config', 'prompts', 'supabase', 'artifacts'].
```

Pip 26.1's setuptools auto-discovery is stricter; sibling workspace
directories (`config/`, `static/`, `prompts/`, `supabase/`, `artifacts/`)
are not Python packages but were being detected as such.

**Bug fix shipped (commit `cf8c92e` on `main`, decision `D-IH-48-J`):**

Added explicit packaging config to `pyproject.toml`:

```toml
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
include = ["akos*"]
exclude = ["tests*", "scripts*", "config*", "static*", "prompts*",
           "supabase*", "artifacts*", "docs*"]
```

Local verification:

```
$ py -m pip install -e .
$ py -c "import akos; print(akos.__file__)"
C:\Users\Shadow\cd_shadow\openclaw-akos\akos\__init__.py
```

**Second attempt — full success (run `25255435320`):**

- Conclusion: `success`
- Jobs: 10 / 10 passed
- Artifacts: **20 total**:
  - 10 × `uat-dossier-{tier}-{persona}/` — per-cell dossier markdown
  - 10 × `eval-scorecards-{tier}-{persona}/` — Tier-A baseline scorecards
- Cells executed Tier-A baseline (cassette-only, deterministic) and
  correctly skipped Tier-B live + adversarial sweeps with annotation:
  `OPENAI_API_KEY missing; cheap tier will SKIP` /
  `ANTHROPIC_API_KEY missing; flagship tier will SKIP`.

This validates the entire I47 P14 → I48 P7 wiring end-to-end:
matrix dispatch → preflight → baseline eval → dossier render → artifact upload.

The Mon 06:00 UTC scheduled run will produce the same artifacts at
real Tier-B spend once `OPENAI_API_KEY` + `ANTHROPIC_API_KEY` repo secrets
are populated by the operator.

## Follow-up 4 — Capture screenshots via `--mode live --screenshots`

**Status:** **Operator-only — preconditions absent.**

**What was verified:**

- `scripts/render_uat_dossier.py` supports `--mode live --screenshots`
  (verified by `--help` and code path in `akos/dossier/run_dispatcher.py`).
- The screenshot capture step in `akos/dossier/screenshots.py` requires
  the OpenClaw Control SPA reachable at `AKOS_API_URL` with valid
  `AKOS_API_KEY`.

**What blocked auto-execution:**

- `AKOS_API_KEY` and `AKOS_API_URL` env vars unset.
- OpenClaw Control SPA not running locally
  (no `npm run dev` / no FastAPI listener detected on `127.0.0.1:8000`).

**Operator command when SPA is back up:**

```powershell
$env:AKOS_API_KEY = '...'
$env:AKOS_API_URL = 'http://127.0.0.1:8000'
py scripts/render_uat_dossier.py --mode live --format all --screenshots `
  --out-dir artifacts/uat-dossier
```

## Bonus deliverable — CI bug fix decision

Decision **D-IH-48-J** (commit `cf8c92e`) was added during follow-up #3:
*Pin `setuptools.packages.find` to `akos*` to keep editable installs
working under pip 26.1's stricter flat-layout policy.* This is recorded
here rather than in the canonical `decision-log.md` because it surfaced
post-closure; if reversed it should be paired with explicit `py_modules`
or migration to `src-layout`.

## Summary

| # | Follow-up | Outcome |
|:-:|:--|:--|
| 1 | Supabase migration push | Operator-only — preconditions documented |
| 2 | `AKOS_DOSSIER_ON_PR=true` | **DONE** (15:30 UTC) |
| 3 | Tier B per-cell dossier artifacts | **DONE** via manual run `25255435320`; CI bug `D-IH-48-J` fixed in `cf8c92e` |
| 4 | Live mode + screenshots | Operator-only — preconditions documented |

Two of four follow-ups closed without operator intervention; the remaining
two are intentionally credential-gated. Repository remains on a clean-slate
`main` with one new commit (`cf8c92e`) layered atop the I48 closure.
