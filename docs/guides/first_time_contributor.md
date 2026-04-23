# First-time contributor (happy path)

**Audience:** developers opening their first PR against this repo (code, tests, or config).

This page is a **tutorial**: one path that should work. For **exact** command lists and optional scripts, use [DEVELOPER_CHECKLIST](../DEVELOPER_CHECKLIST.md) and [reference/DEV_VERIFICATION_REFERENCE](../reference/DEV_VERIFICATION_REFERENCE.md). Product context: [README](../../README.md), architecture: [ARCHITECTURE](../ARCHITECTURE.md).

## 1. Clone and environment

- **Python:** [pyproject.toml](../../pyproject.toml) requires `>=3.10`; the repo may pin a version in `.python-version` for local alignment.
- **Node:** [README Quick Start](../../README.md#quick-start) (typically Node 22+ for OpenClaw-related tooling).
- **Fork / branch** per [CONTRIBUTING.md](../../CONTRIBUTING.md#submitting-changes).

## 2. Bootstrap the runtime (once per machine or after big upstream changes)

From the repo root (see [README](../../README.md#quick-start) for Windows PowerShell):

```bash
python scripts/bootstrap.py
```

Use `python scripts/bootstrap.py --skip-ollama` or `--skip-mcp` if you only need a subset. If you manually copied `mcporter.json` from the example, run `py scripts/resolve-mcporter-paths.py` as the README says.

## 3. See what you would run before a commit (no side effects)

The verification **profile** `pre_commit` is defined in [config/verification-profiles.json](../../config/verification-profiles.json). To print the resolved steps without executing:

```bash
py scripts/verify.py pre_commit --dry-run
```

List all profiles:

```bash
py scripts/verify.py --list
```

## 4. Run a *narrow* test loop while you iterate

The full pre-commit path includes a long `test.py all` and `release-gate` (and can run the same full test suite more than once). For fast feedback on a small change, use **pytest groups**:

```bash
py scripts/test.py --list
py scripts/test.py api
py scripts/test.py madeira
py scripts/test.py intent
```

Pick the group that matches your change (see [DEVELOPER_CHECKLIST](../DEVELOPER_CHECKLIST.md#when-to-use-what)).

## 5. Before you push: full gate (when you are ready)

When your branch is feature-complete, run the same bar as the [DEVELOPER_CHECKLIST](../DEVELOPER_CHECKLIST.md#golden-path-default):

- `py scripts/verify.py pre_commit` (or the discrete steps in the config if you prefer), and  
- set `AKOS_EVAL_RUBRIC=1` for `release-gate` when you need the offline governance eval slice (see [understanding_verification](understanding_verification.md)).

## 6. Update docs if you changed contracts

[CONTRIBUTING.md](../../CONTRIBUTING.md) and [`.cursor/rules/akos-docs-config-sync.mdc`](../../.cursor/rules/akos-docs-config-sync.mdc) list what to update when you touch `config/`, `akos/`, `scripts/`, or HLK files.

## See also

- [Documentation map (docs/README)](../README.md) — where everything else lives.
- [Understanding verification](understanding_verification.md) — how `verify` / `release-gate` / `run-evals` fit together.
- [GLOSSARY](../GLOSSARY.md) — terms like SSOT, HLK, profile.
