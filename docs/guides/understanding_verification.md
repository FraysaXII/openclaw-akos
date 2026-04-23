# Understanding verification (mental model)

**Audience:** anyone who can run `py scripts/verify.py` or `release-gate` and wants the **story** of how pieces connect—not a replacement for the **canonical argv** in [config/verification-profiles.json](../../config/verification-profiles.json).

**If this page disagrees with the JSON registry, the JSON wins.** Code loads that file via [akos/verification_profiles.py](../../akos/verification_profiles.py); docs only interpret.

## Why this exists

The repo has many scripts (`check-drift`, `test.py`, `browser-smoke`, `run-evals`, HLK validators). A **verification registry** keeps the *ordered* pre-commit **steps** and the **governance eval suite list** in one place so [scripts/verify.py](../../scripts/verify.py), [scripts/release-gate.py](../../scripts/release-gate.py), and [scripts/run-evals.py](../../scripts/run-evals.py) do not each hardcode different lists.

## The four pieces (simple picture)

1. **Registry (data)** — [config/verification-profiles.json](../../config/verification-profiles.json)  
   - `eval_rubric_governance_suites`: which eval **suite directory names** count as the “governance” rubric pass.  
   - `profiles.pre_commit.steps`: what `verify pre_commit` runs, in order, each with `argv`.

2. **Loader (library)** — [akos/verification_profiles.py](../../akos/verification_profiles.py)  
   - Loads and validates the JSON, exposes e.g. `governance_rubric_suites()`.

3. **Orchestrator (CLI)** — [scripts/verify.py](../../scripts/verify.py)  
   - `py scripts/verify.py pre_commit` runs each step as a subprocess.  
   - `py scripts/verify.py pre_commit --dry-run` only prints.  
   - **Kebab/underscore:** `pre-commit` and `pre_commit` are accepted for the same profile.

4. **Tooling that consumes the same lists**  
   - **Release gate** — [scripts/release-gate.py](../../scripts/release-gate.py): when `AKOS_EVAL_RUBRIC=1`, runs `run-evals` for each suite in `eval_rubric_governance_suites` (not a separate copy-pasted list in code).  
   - **Run evals** — `py scripts/run-evals.py run --governance-rubric` runs the same suite list for local checks.

## Profile: `compliance_mirror_emit` (Holistika mirrors)

**Not** part of `pre_commit`. Runs [`scripts/sync_compliance_mirrors_from_csv.py`](../../scripts/sync_compliance_mirrors_from_csv.py) twice: **`--count-only`** (preflight), then **`--output artifacts/sql/compliance_mirror_upsert.sql`**. Use after **`validate_hlk.py`** / release gate when git CSVs changed; review generated SQL before applying to Postgres. **Argv SSOT:** [`config/verification-profiles.json`](../../config/verification-profiles.json) profile `compliance_mirror_emit`.

**DDL vs data plane:** Schema changes are **not** orchestrated by `verify.py`. Use the Supabase CLI: after `supabase link`, run `npx supabase migration list` and ensure Local/Remote match before `db push` ([`supabase/README.md`](../../supabase/README.md), [`supabase/migrations/README.md`](../../supabase/migrations/README.md), [`docs/ARCHITECTURE.md`](../ARCHITECTURE.md) § Supabase schema and compliance mirror governance).

## `test.py` groups vs `verify pre_commit`

- **`py scripts/test.py <group>`** — a **pytest facade** for topic slices (`madeira`, `intent`, `api`, `graph`, …). Use this while editing to avoid always running 300+ tests.  
- **`py scripts/verify.py pre_commit`** — runs the **full** chain in the registry (inventory → drift → full tests → browser smoke → API+Madeira smoke → `release-gate`).

**Caveat:** the `pre_commit` profile includes `scripts/test.py all` and later `release-gate`, and `release-gate` **also** invokes the full test suite. That duplicates work; it matches the stricter pre-push bar. For daily iteration, prefer targeted `test.py` groups, then use the full profile when you are ready to merge.

## “Governance” evals vs a single suite

- **All governance suites in one go:** `py scripts/run-evals.py run --governance-rubric` (and `AKOS_EVAL_RUBRIC=1` on the release gate for the same set).  
- **One suite:** `py scripts/run-evals.py run --suite <id> --mode rubric` — see [tests/evals/README](../../tests/evals/README.md).

## See also

- [DEVELOPER_CHECKLIST](../DEVELOPER_CHECKLIST.md) — golden path and “when to use what”.  
- [reference/DEV_VERIFICATION_REFERENCE](../reference/DEV_VERIFICATION_REFERENCE.md) — optional tools and Playwright notes.  
- [Documentation map (docs/README)](../README.md) — other reader paths.  
- [GLOSSARY](../GLOSSARY.md) — SSOT, profile, release gate, UAT.
