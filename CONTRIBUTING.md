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
