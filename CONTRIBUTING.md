# Contributing to OpenCLAW-AKOS

Thank you for your interest in contributing. This document provides guidelines to ensure a smooth collaboration process.

## How to Contribute

### Reporting Issues

- Use GitHub Issues for bug reports, feature requests, and documentation improvements
- Search existing issues before creating a new one to avoid duplicates
- Provide clear reproduction steps, expected behavior, and actual behavior

### Submitting Changes

1. **Fork** the repository
2. **Create a feature branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** following the code and documentation standards below
4. **Commit** with clear, descriptive messages
5. **Push** to your fork and open a **Pull Request** against `main`

### Pull Request Guidelines

- Keep PRs focused on a single concern
- Reference related issues using `Closes #<issue-number>`
- Update documentation if your changes affect any SOP procedures, architecture descriptions, or configuration examples
- All MCP server configurations must include valid JSON syntax — validate before submitting

## Documentation Standards

This is primarily a documentation and configuration repository. Contributions should:

- Use clear, precise technical language
- Maintain the existing document structure and heading hierarchy
- Include version and date metadata where applicable
- Cite sources using numbered references consistent with the SOP format

### SOP Modifications

Changes to the Standard Operating Procedure (`docs/SOP.md`) require:

- A clear rationale in the PR description
- Verification that step-by-step procedures are accurate and reproducible
- Security impact assessment if the change touches sandboxing, networking, or credential management

## Python Code Standards

The `akos/` orchestration library and all scripts under `scripts/` follow these conventions:

- **Type hints required** on all function signatures and return types.
- **Pydantic models** for all configuration schemas -- never hand-write `assert` chains for JSON validation. Define a model in `akos/models.py` and call `Model.model_validate(data)`.
- **Shared utilities** live in `akos/io.py`. Never duplicate `load_json`, `deep_merge`, `resolve_openclaw_home`, or similar helpers in scripts.
- **Structured logging** via `akos/log.py`. All scripts call `setup_logging(json_output=args.json_log)` at startup and use `logging.getLogger(__name__)` instead of `print()`.
- **Subprocess calls** go through `akos/process.run()` with explicit timeouts. Never use bare `subprocess.run()` or `os.system()`.
- **Cross-platform**: use Python `pathlib.Path` and `os.environ` instead of shell-specific constructs. All scripts must work on Windows, macOS, and Linux without modification.

## Dependency Policy

- **Prefer stdlib.** Only add third-party packages when they eliminate significant complexity or duplication.
- **Security justification required.** Every new dependency must have a rationale documented in the PR description, per [SECURITY.md](SECURITY.md).
- **Current dependencies and justification:**
  - `pydantic>=2.0` -- Eliminates ~150 lines of hand-written assertions, provides runtime type safety for all config schemas, Rust-backed core.
  - `langfuse>=2.0` -- Activates the eval infrastructure (langfuse.env.example, baselines.json, alerts.json); graceful no-op when unconfigured.
  - `pytest>=7.0` -- Test runner.

## Testing Standards

- All Pydantic models must have corresponding tests in `tests/test_akos_models.py` covering both valid and invalid input.
- Alert conditions must have tests in `tests/test_akos_alerts.py` with synthetic log entries.
- Run the full suite before submitting: `py -m pytest tests/ -v`

## Security Contributions

Given the Zero-Trust posture of this project:

- **Never** commit API keys, tokens, or credentials
- **Never** add dependencies without a security justification
- All new skill integrations must pass `skillvet` scanning
- Review [SECURITY.md](SECURITY.md) before proposing changes to security-related procedures

## Code of Conduct

- Be respectful and constructive in all interactions
- Focus on technical merit when reviewing contributions
- Assume good intent from fellow contributors

## Questions?

Open a GitHub Discussion or reach out via the issue tracker.
