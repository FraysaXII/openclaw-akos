---
intellectual_kind: phase_report
initiative_id: INIT-OPENCLAW_AKOS-90
authored: 2026-06-01
linked_decisions:
  - D-IH-90-W
language: en
---

# Post–GATE #2 sibling mirror realign

## Commands

```powershell
py scripts/bless_external_repo.py --repo-slug hlk-erp
py scripts/bless_external_repo.py --repo-slug kirbe-platform
py scripts/check_external_repo_contract.py
```

## Result

- **bless:** Wrote `akos-mirror.mdc` in local clones (`root_cd/hlk-erp`, `root_cd/kirbe`).
- **contract check:** `external repo contract: OK -- 2 repo(s) validated`.

## Operator follow-up

Commit + push in **each sibling repo** (not in AKOS):

- `hlk-erp` — `.cursor/rules/akos-mirror.mdc` + `.cursor/rules/.akos-mirror.sha256`
- `kirbe-platform` — same paths under `root_cd/kirbe`

Suggested message: `chore(governance): realign akos-mirror.mdc to AKOS template (I90 GATE #2)`.
