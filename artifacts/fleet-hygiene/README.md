# Fleet hygiene sweep artifacts

Machine-readable + human-readable output from [`scripts/workspace_fleet_hygiene_sweep.py`](../../scripts/workspace_fleet_hygiene_sweep.py).

- `fleet-hygiene-<YYYY-MM-DD>.md` — operator skim table
- `fleet-hygiene-<YYYY-MM-DD>.json` — same findings for tooling

Run: `py scripts/workspace_fleet_hygiene_sweep.py --sweep` (INFO at release-gate; FAIL when AKOS worktree dirty without `--strict` waiver).

Standing OPS rows rechecked: OPS-81-1, OPS-86-1, OPS-86-9, OPS-90-6.
