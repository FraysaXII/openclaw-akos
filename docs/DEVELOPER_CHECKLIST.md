# Developer Checklist

Per [CONTRIBUTING.md](../CONTRIBUTING.md), run this phase checklist before every commit that touches features or tooling.

## Pre-commit Checks

### Tests and Gates

| Step | Command | Purpose |
|:-----|:--------|:--------|
| 1 | `py scripts/test.py all` | 193+ tests pass |
| 2 | `py scripts/check-drift.py` | No drift (optionally includes MCP reachability) |
| 3 | `py scripts/browser-smoke.py [--playwright]` | If Playwright installed |
| 4 | `py scripts/release-gate.py` | Full gate; optionally verify MCP server reachability |

### Documentation Updates

| File | When to update |
|:-----|:----------------|
| `CHANGELOG.md` | Add entry under [Unreleased] or version |
| `README.md` | Version refs, new capabilities |
| `docs/ARCHITECTURE.md` | New components, diagrams |
| `docs/SOP.md` | New procedures (e.g., 9.12 Browser UAT) |
| `docs/USER_GUIDE.md` | New sections, UX changes |
| `SECURITY.md` | New deps, controls |
| `config/workspace-scaffold/README.md` | If scaffold changes |
| `CONTRIBUTING.md` | New test groups, deps |

## Playwright Setup (Optional)

For browser smoke DOM mode:

```bash
pip install playwright
playwright install chromium
py scripts/browser-smoke.py --playwright
```

## MCP Requirements

- **GitHub MCP:** Set `GITHUB_TOKEN` for repo metadata and future commit retrieval.
- **Custom AKOS MCP:** Requires `pip install mcp httpx`. Bootstrap deploys with resolved path.
- **cursor-ide-browser:** Cursor IDE built-in; enable in Cursor Settings if desired. Not required for AKOS.
